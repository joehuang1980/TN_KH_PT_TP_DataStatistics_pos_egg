"""
Data loading and preprocessing utilities for multi-city analysis.

This module provides functions to load mosquito surveillance data from individual
cities or merge data from all cities, extract feature columns, and preprocess
data for analysis.
"""

import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import analysis_config as config


class DataLoader:
    """
    Data loader for mosquito surveillance data across multiple cities.
    """

    def __init__(self):
        """Initialize data loader with configuration."""
        self.cities = config.CITIES
        self.city_order = config.CITY_ORDER
        self.ignore_columns = config.IGNORE_COLUMNS
        self.targets = config.TARGETS

    def load_city_data(self, city_key, preprocess=True):
        """
        Load data for a specific city.

        Parameters
        ----------
        city_key : str
            City key ('taipei', 'kaohsiung', 'pingtung', 'tainan')
        preprocess : bool, default=True
            Whether to preprocess data (drop NaN, remove ignore columns)

        Returns
        -------
        pandas.DataFrame
            Loaded city data
        dict
            Metadata about the loaded data

        Raises
        ------
        ValueError
            If city_key is invalid
        FileNotFoundError
            If city data file doesn't exist
        """
        if city_key not in self.cities:
            raise ValueError(f"Invalid city key: {city_key}. Must be one of {list(self.cities.keys())}")

        city_info = self.cities[city_key]
        city_path = city_info['path']

        if not os.path.exists(city_path):
            raise FileNotFoundError(f"Data file not found: {city_path}")

        print(f"Loading data for {city_info['name_en']} ({city_info['abbr']})...")

        # Load CSV
        df = pd.read_csv(city_path)

        # Metadata
        metadata = {
            'city_key': city_key,
            'city_name_en': city_info['name_en'],
            'city_name_zh': city_info['name_zh'],
            'city_abbr': city_info['abbr'],
            'n_rows_original': len(df),
            'n_cols_original': len(df.columns),
            'file_path': city_path
        }

        # Preprocess if requested
        if preprocess:
            df = self.preprocess_data(df, city_key)
            metadata['n_rows_processed'] = len(df)
            metadata['n_cols_processed'] = len(df.columns)

        print(f"  ✓ Loaded {len(df):,} rows × {len(df.columns)} columns")

        return df, metadata

    def load_all_cities(self, preprocess=True, add_city_column=True):
        """
        Load and optionally merge data from all cities.

        Parameters
        ----------
        preprocess : bool, default=True
            Whether to preprocess each city's data
        add_city_column : bool, default=True
            Whether to add a 'city' column to identify city of origin

        Returns
        -------
        dict or pandas.DataFrame
            If add_city_column is True: merged DataFrame with city column
            If add_city_column is False: dict of {city_key: dataframe}
        dict
            Metadata for all cities

        """
        print(f"\nLoading data for all {len(self.city_order)} cities...")
        print("=" * 80)

        city_dataframes = {}
        all_metadata = {}

        for city_key in self.city_order:
            df, metadata = self.load_city_data(city_key, preprocess=preprocess)
            city_dataframes[city_key] = df
            all_metadata[city_key] = metadata

        if add_city_column:
            # Add city identifier and merge
            print("\nMerging all cities...")
            merged_dfs = []

            for city_key, df in city_dataframes.items():
                df_copy = df.copy()
                df_copy['city'] = self.cities[city_key]['name_en']
                df_copy['city_zh'] = self.cities[city_key]['name_zh']
                df_copy['city_abbr'] = self.cities[city_key]['abbr']
                merged_dfs.append(df_copy)

            merged_df = pd.concat(merged_dfs, axis=0, ignore_index=True)

            print(f"  ✓ Merged data: {len(merged_df):,} rows × {len(merged_df.columns)} columns")

            # Summary metadata
            all_metadata['merged'] = {
                'n_cities': len(self.city_order),
                'n_rows_total': len(merged_df),
                'n_cols': len(merged_df.columns),
                'cities': [self.cities[ck]['name_en'] for ck in self.city_order]
            }

            return merged_df, all_metadata
        else:
            return city_dataframes, all_metadata

    def preprocess_data(self, df, city_key=None):
        """
        Preprocess data: drop NaN values and remove ignore columns.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        city_key : str, optional
            City key for logging purposes

        Returns
        -------
        pandas.DataFrame
            Preprocessed dataframe
        """
        df_processed = df.copy()

        city_name = self.cities[city_key]['name_en'] if city_key else "data"

        # Initial size
        n_rows_before = len(df_processed)

        # Drop columns to ignore (if they exist)
        cols_to_drop = [col for col in self.ignore_columns if col in df_processed.columns]
        if cols_to_drop:
            df_processed = df_processed.drop(columns=cols_to_drop)
            print(f"  ✓ Dropped ignore columns: {cols_to_drop}")

        # Drop rows with missing values in target variables
        if any(target in df_processed.columns for target in self.targets):
            before_dropna = len(df_processed)
            df_processed = df_processed.dropna(subset=[t for t in self.targets if t in df_processed.columns])
            n_dropped = before_dropna - len(df_processed)
            if n_dropped > 0:
                print(f"  ✓ Dropped {n_dropped:,} rows with missing target values")

        return df_processed

    def get_feature_columns(self, df, include_targets=False):
        """
        Extract feature column names from dataframe.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        include_targets : bool, default=False
            Whether to include target columns (pos, egg)

        Returns
        -------
        list
            List of feature column names
        """
        # Get all columns
        all_cols = df.columns.tolist()

        # Remove ignore columns and target columns (unless requested)
        exclude_cols = set(self.ignore_columns)
        if not include_targets:
            exclude_cols.update(self.targets)

        # Also exclude any city-related columns added during merging
        exclude_cols.update(['city', 'city_zh', 'city_abbr'])

        feature_cols = [col for col in all_cols if col not in exclude_cols]

        return feature_cols

    def get_lag_features(self, df, variable, lag_type='simple'):
        """
        Get lag feature columns for a specific variable.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        variable : str
            Base variable name (e.g., 'H_temp', 'R', 'NDVImean')
        lag_type : str, default='simple'
            Type of lag: 'simple' (lag_1, lag_2, ...) or 'rolling' (lag_rolling1, ...)

        Returns
        -------
        list
            List of lag feature column names found in dataframe
        """
        lag_cols = []

        if lag_type == 'simple':
            # Pattern: variable_lag_N or variable_lagN (for NDVI)
            for week in config.LAG_RANGE:
                col_pattern1 = f'{variable}_lag_{week}'
                col_pattern2 = f'{variable}_lag{week}'

                if col_pattern1 in df.columns:
                    lag_cols.append(col_pattern1)
                elif col_pattern2 in df.columns:
                    lag_cols.append(col_pattern2)

        elif lag_type == 'rolling':
            # Pattern: variable_lag_rollingN or variable_lag_rolling{aggregation}N
            for week in config.LAG_RANGE:
                # Standard pattern
                col_pattern1 = f'{variable}_lag_rolling{week}'

                # NDVI special patterns
                col_pattern2 = f'{variable}_lag_rollingmean{week}'
                col_pattern3 = f'{variable}_lag_rollingmedian{week}'
                col_pattern4 = f'{variable}_lag_rollingsum{week}'

                if col_pattern1 in df.columns:
                    lag_cols.append(col_pattern1)
                elif col_pattern2 in df.columns:
                    lag_cols.append(col_pattern2)
                elif col_pattern3 in df.columns:
                    lag_cols.append(col_pattern3)
                elif col_pattern4 in df.columns:
                    lag_cols.append(col_pattern4)

        return lag_cols

    def get_feature_groups(self, df):
        """
        Categorize features into groups (temperature, rainfall, NDVI, demographic).

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe

        Returns
        -------
        dict
            Dictionary of {group_name: [column names]}
        """
        feature_cols = self.get_feature_columns(df, include_targets=False)

        groups = {
            'temperature': [],
            'rainfall': [],
            'ndvi': [],
            'demographic': []
        }

        for col in feature_cols:
            # Temperature features
            if any(col.startswith(var) for var in ['H_temp', 'M_temp', 'L_temp']):
                groups['temperature'].append(col)
            # Rainfall features
            elif col.startswith('R_'):
                groups['rainfall'].append(col)
            # NDVI features
            elif any(col.startswith(var) for var in ['NDVImean', 'NDVImedian', 'NDVIsum']):
                groups['ndvi'].append(col)
            # Demographic features
            elif col in config.FEATURE_GROUPS['demographic']['variables']:
                groups['demographic'].append(col)

        return groups

    def get_data_summary(self, df, city_key=None):
        """
        Get summary statistics for a dataframe.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        city_key : str, optional
            City key for identification

        Returns
        -------
        dict
            Summary statistics
        """
        feature_cols = self.get_feature_columns(df, include_targets=False)
        feature_groups = self.get_feature_groups(df)

        summary = {
            'n_rows': len(df),
            'n_cols': len(df.columns),
            'n_features': len(feature_cols),
            'n_temperature_features': len(feature_groups['temperature']),
            'n_rainfall_features': len(feature_groups['rainfall']),
            'n_ndvi_features': len(feature_groups['ndvi']),
            'n_demographic_features': len(feature_groups['demographic']),
        }

        # Target statistics
        for target in self.targets:
            if target in df.columns:
                target_data = df[target].dropna()
                summary[f'{target}_count'] = len(target_data)
                summary[f'{target}_mean'] = target_data.mean()
                summary[f'{target}_std'] = target_data.std()
                summary[f'{target}_min'] = target_data.min()
                summary[f'{target}_max'] = target_data.max()

        if city_key:
            summary['city'] = self.cities[city_key]['name_en']

        return summary

    def validate_data_structure(self, df, expected_n_features=None):
        """
        Validate that dataframe has expected structure.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        expected_n_features : int, optional
            Expected number of features (default: config.TOTAL_FEATURES)

        Raises
        ------
        ValueError
            If data structure is invalid
        """
        if expected_n_features is None:
            expected_n_features = config.TOTAL_FEATURES

        feature_cols = self.get_feature_columns(df, include_targets=False)
        n_features = len(feature_cols)

        # Check feature count
        if n_features != expected_n_features:
            print(f"⚠ Warning: Expected {expected_n_features} features, found {n_features}")

        # Check target columns exist
        for target in self.targets:
            if target not in df.columns:
                raise ValueError(f"Target column '{target}' not found in dataframe")

        # Check for missing values in features
        feature_missing = df[feature_cols].isnull().sum().sum()
        if feature_missing > 0:
            print(f"⚠ Warning: {feature_missing:,} missing values in feature columns")

        print(f"✓ Data structure validated: {n_features} features, {len(df):,} rows")


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def load_city(city_key, preprocess=True):
    """
    Convenience function to load a single city's data.

    Parameters
    ----------
    city_key : str
        City key ('taipei', 'kaohsiung', 'pingtung', 'tainan')
    preprocess : bool, default=True
        Whether to preprocess data

    Returns
    -------
    pandas.DataFrame, dict
        Data and metadata
    """
    loader = DataLoader()
    return loader.load_city_data(city_key, preprocess=preprocess)


def load_all(preprocess=True, merge=True):
    """
    Convenience function to load all cities' data.

    Parameters
    ----------
    preprocess : bool, default=True
        Whether to preprocess data
    merge : bool, default=True
        Whether to merge into single dataframe

    Returns
    -------
    pandas.DataFrame or dict, dict
        Data (merged or dict) and metadata
    """
    loader = DataLoader()
    return loader.load_all_cities(preprocess=preprocess, add_city_column=merge)


# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("TESTING DATA LOADER")
    print("=" * 80)

    # Test 1: Load single city
    print("\n" + "=" * 80)
    print("TEST 1: Load single city (Taipei)")
    print("=" * 80)

    loader = DataLoader()
    df_taipei, metadata_taipei = loader.load_city_data('taipei', preprocess=True)

    print(f"\nData shape: {df_taipei.shape}")
    print(f"\nColumns: {list(df_taipei.columns[:10])}... (showing first 10)")

    # Get feature columns
    feature_cols = loader.get_feature_columns(df_taipei, include_targets=False)
    print(f"\nNumber of features: {len(feature_cols)}")

    # Get feature groups
    feature_groups = loader.get_feature_groups(df_taipei)
    print(f"\nFeature groups:")
    for group, cols in feature_groups.items():
        print(f"  - {group}: {len(cols)} features")

    # Get summary
    summary = loader.get_data_summary(df_taipei, city_key='taipei')
    print(f"\nData summary:")
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"  - {key}: {value:.3f}")
        else:
            print(f"  - {key}: {value}")

    # Test lag features
    print(f"\nLag features test:")
    h_temp_lag_simple = loader.get_lag_features(df_taipei, 'H_temp', lag_type='simple')
    h_temp_lag_rolling = loader.get_lag_features(df_taipei, 'H_temp', lag_type='rolling')
    print(f"  - H_temp simple lag features: {len(h_temp_lag_simple)}")
    print(f"  - H_temp rolling lag features: {len(h_temp_lag_rolling)}")

    # Validate structure
    print(f"\nValidating data structure...")
    loader.validate_data_structure(df_taipei)

    # Test 2: Load all cities (separate)
    print("\n" + "=" * 80)
    print("TEST 2: Load all cities (not merged)")
    print("=" * 80)

    city_dfs, metadata_all = loader.load_all_cities(preprocess=True, add_city_column=False)

    for city_key, df in city_dfs.items():
        print(f"  - {loader.cities[city_key]['name_en']}: {len(df):,} rows × {len(df.columns)} columns")

    # Test 3: Load all cities (merged)
    print("\n" + "=" * 80)
    print("TEST 3: Load all cities (merged)")
    print("=" * 80)

    df_merged, metadata_merged = loader.load_all_cities(preprocess=True, add_city_column=True)

    print(f"\nMerged data shape: {df_merged.shape}")
    print(f"Cities in merged data: {df_merged['city'].unique()}")
    print(f"\nRows per city:")
    print(df_merged['city'].value_counts())

    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED")
    print("=" * 80)
