"""
Base analyzer class for all statistical analyses.

This module defines an abstract base class that all specific analyzers
(statistical, PCA/clustering, lag/rolling, comparison) must inherit from.
It enforces a consistent interface and provides common functionality.
"""

from abc import ABC, abstractmethod
import os
import pandas as pd
import numpy as np
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import analysis_config as config


class BaseAnalyzer(ABC):
    """
    Abstract base class for all analyzers.

    All concrete analyzer classes must implement the abstract methods defined here.
    This ensures a consistent interface across all analysis types.
    """

    def __init__(self, name):
        """
        Initialize base analyzer.

        Parameters
        ----------
        name : str
            Name of the analyzer (e.g., 'statistical', 'pca_clustering')
        """
        self.name = name
        self.results = {}
        self.figures = {}
        self.metadata = {}

    @abstractmethod
    def analyze(self, df, city_key=None, **kwargs):
        """
        Perform the analysis on the provided data.

        This method must be implemented by all concrete analyzer classes.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data to analyze
        city_key : str, optional
            City key if analyzing a single city
        **kwargs : dict
            Additional parameters specific to the analyzer

        Returns
        -------
        dict
            Analysis results
        """
        pass

    @abstractmethod
    def generate_methods_section(self):
        """
        Generate the Methods section for academic paper.

        This method must be implemented by all concrete analyzer classes.

        Returns
        -------
        str
            Methods section text in English (markdown format)
        """
        pass

    @abstractmethod
    def generate_results_section(self):
        """
        Generate the Results section for academic paper.

        This method must be implemented by all concrete analyzer classes.

        Returns
        -------
        str
            Results section text in English with statistics (markdown format)
        """
        pass

    @abstractmethod
    def save_outputs(self, output_dir):
        """
        Save all outputs (CSV files, plots, text files) to specified directory.

        This method must be implemented by all concrete analyzer classes.

        Parameters
        ----------
        output_dir : str
            Directory to save outputs

        Returns
        -------
        dict
            Dictionary of saved file paths
        """
        pass

    def _create_output_dir(self, output_dir):
        """
        Create output directory if it doesn't exist.

        Parameters
        ----------
        output_dir : str
            Directory path to create

        Returns
        -------
        str
            Absolute path of created directory
        """
        os.makedirs(output_dir, exist_ok=True)
        return os.path.abspath(output_dir)

    def _save_dataframe(self, df, output_dir, filename):
        """
        Save dataframe to CSV file.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe to save
        output_dir : str
            Output directory
        filename : str
            Filename (should include .csv extension)

        Returns
        -------
        str
            Path to saved file
        """
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"  ✓ Saved: {filename}")
        return filepath

    def _save_figure(self, fig, output_dir, filename, dpi=None):
        """
        Save matplotlib figure.

        Parameters
        ----------
        fig : matplotlib.figure.Figure
            Figure to save
        output_dir : str
            Output directory
        filename : str
            Filename (should include extension, e.g., .png)
        dpi : int, optional
            DPI for raster formats (default: from config)

        Returns
        -------
        str
            Path to saved file
        """
        if dpi is None:
            dpi = config.FIGURE_DPI

        filepath = os.path.join(output_dir, filename)
        fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
        print(f"  ✓ Saved: {filename}")
        return filepath

    def _save_text(self, text, output_dir, filename):
        """
        Save text content to file.

        Parameters
        ----------
        text : str
            Text content
        output_dir : str
            Output directory
        filename : str
            Filename (should include extension, e.g., .md, .txt)

        Returns
        -------
        str
            Path to saved file
        """
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"  ✓ Saved: {filename}")
        return filepath

    def get_summary(self):
        """
        Get summary of analysis results.

        Returns
        -------
        dict
            Summary information
        """
        summary = {
            'analyzer_name': self.name,
            'n_results': len(self.results),
            'n_figures': len(self.figures),
        }
        summary.update(self.metadata)
        return summary

    def __repr__(self):
        """String representation of analyzer."""
        return f"{self.__class__.__name__}(name='{self.name}')"


class CityAnalyzer(BaseAnalyzer):
    """
    Base class for analyzers that process individual cities.

    This extends BaseAnalyzer with city-specific functionality.
    """

    def __init__(self, name):
        """Initialize city analyzer."""
        super().__init__(name)
        self.city_results = {}  # Store results per city

    def analyze_city(self, df, city_key, **kwargs):
        """
        Analyze a single city's data.

        Parameters
        ----------
        df : pandas.DataFrame
            City data
        city_key : str
            City identifier
        **kwargs : dict
            Additional parameters

        Returns
        -------
        dict
            City-specific results
        """
        # Call the main analyze method
        results = self.analyze(df, city_key=city_key, **kwargs)

        # Store in city_results
        self.city_results[city_key] = results

        return results

    def analyze_all_cities(self, city_dataframes, **kwargs):
        """
        Analyze all cities sequentially.

        Parameters
        ----------
        city_dataframes : dict
            Dictionary of {city_key: dataframe}
        **kwargs : dict
            Additional parameters

        Returns
        -------
        dict
            Results for all cities {city_key: results}
        """
        all_results = {}

        for city_key, df in city_dataframes.items():
            city_name = config.CITIES[city_key]['name_en']
            print(f"\nAnalyzing {city_name}...")
            print("-" * 60)

            results = self.analyze_city(df, city_key, **kwargs)
            all_results[city_key] = results

        return all_results

    def save_city_outputs(self, city_key, base_output_dir):
        """
        Save outputs for a specific city.

        Parameters
        ----------
        city_key : str
            City identifier
        base_output_dir : str
            Base output directory (will create city subdirectory)

        Returns
        -------
        dict
            Dictionary of saved file paths
        """
        # Get city-specific output directory
        city_dir = config.get_city_output_dir(city_key, self.name)

        # Ensure results exist for this city
        if city_key not in self.city_results:
            raise ValueError(f"No results found for city: {city_key}")

        # Call the standard save_outputs method
        return self.save_outputs(city_dir)


class ComparisonAnalyzer(BaseAnalyzer):
    """
    Base class for analyzers that compare across cities.

    This extends BaseAnalyzer with cross-city comparison functionality.
    """

    def __init__(self, name='comparison'):
        """Initialize comparison analyzer."""
        super().__init__(name)
        self.city_order = config.CITY_ORDER

    def analyze_comparison(self, city_results, **kwargs):
        """
        Analyze and compare results across cities.

        Parameters
        ----------
        city_results : dict
            Dictionary of {city_key: city_specific_results}
        **kwargs : dict
            Additional parameters

        Returns
        -------
        dict
            Comparison results
        """
        # Call the main analyze method
        results = self.analyze(city_results, **kwargs)

        return results


# ==============================================================================
# HELPER FUNCTIONS FOR COMMON STATISTICAL OPERATIONS
# ==============================================================================

def calculate_correlation(df, features, target, method='spearman'):
    """
    Calculate correlations between features and target.

    Parameters
    ----------
    df : pandas.DataFrame
        Input data
    features : list
        List of feature column names
    target : str
        Target column name
    method : str, default='spearman'
        Correlation method ('spearman' or 'pearson')

    Returns
    -------
    pandas.Series
        Correlations (index=feature names, values=correlation coefficients)
    pandas.Series
        P-values (index=feature names, values=p-values)
    """
    from scipy import stats

    correlations = {}
    p_values = {}

    for feature in features:
        # Get non-null pairs
        valid_mask = df[[feature, target]].notna().all(axis=1)
        x = df.loc[valid_mask, feature]
        y = df.loc[valid_mask, target]

        if len(x) > 0:
            if method == 'spearman':
                corr, pval = stats.spearmanr(x, y)
            elif method == 'pearson':
                corr, pval = stats.pearsonr(x, y)
            else:
                raise ValueError(f"Unknown correlation method: {method}")

            correlations[feature] = corr
            p_values[feature] = pval
        else:
            correlations[feature] = np.nan
            p_values[feature] = np.nan

    return pd.Series(correlations), pd.Series(p_values)


def bonferroni_correction(p_values, alpha=0.05):
    """
    Apply Bonferroni correction to p-values.

    Parameters
    ----------
    p_values : array-like
        P-values to correct
    alpha : float, default=0.05
        Significance level

    Returns
    -------
    float
        Corrected alpha threshold
    array-like
        Boolean array indicating significance
    """
    n_tests = len(p_values)
    corrected_alpha = alpha / n_tests
    significant = np.array(p_values) < corrected_alpha

    return corrected_alpha, significant


# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("BASE ANALYZER MODULE")
    print("=" * 80)

    print("\n✓ BaseAnalyzer class defined")
    print("✓ CityAnalyzer class defined (for individual city analyses)")
    print("✓ ComparisonAnalyzer class defined (for cross-city comparisons)")
    print("✓ Helper functions available:")
    print("  - calculate_correlation()")
    print("  - bonferroni_correction()")

    print("\nAbstract methods that must be implemented by concrete analyzers:")
    print("  1. analyze() - Perform the analysis")
    print("  2. generate_methods_section() - Generate Methods text")
    print("  3. generate_results_section() - Generate Results text")
    print("  4. save_outputs() - Save all outputs")

    print("\n" + "=" * 80)
    print("✓ MODULE LOADED SUCCESSFULLY")
    print("=" * 80)
