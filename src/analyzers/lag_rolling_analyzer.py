"""
Lag and rolling window temporal analysis for mosquito surveillance data.

This module implements:
- Correlation analysis for lag features (lag_1 to lag_12)
- Correlation analysis for rolling window features (lag_rolling1 to lag_rolling12)
- Optimal lag period identification per variable
- Correlation heatmaps (variables × lag weeks)
- Line plots showing correlation vs lag period
- Academic paper section generation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import sys

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.base_analyzer import CityAnalyzer, calculate_correlation
from core.academic_writer import AcademicWriter
from core.data_loader import DataLoader
from config import analysis_config as config


class LagRollingAnalyzer(CityAnalyzer):
    """
    Analyzer for temporal lag and rolling window effects.
    """

    def __init__(self):
        """Initialize lag/rolling analyzer."""
        super().__init__(name='lag_rolling')
        self.writer = AcademicWriter()
        self.loader = DataLoader()

    def analyze(self, df, city_key=None, **kwargs):
        """
        Perform lag and rolling window analysis.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data with lag/rolling features
        city_key : str, optional
            City identifier
        **kwargs : dict
            Additional parameters

        Returns
        -------
        dict
            Analysis results including optimal lags, correlations
        """
        city_name = config.CITIES[city_key]['name_en'] if city_key else "Unknown"
        print(f"\n{'='*60}")
        print(f"Lag/Rolling Temporal Analysis: {city_name}")
        print(f"{'='*60}")

        results = {
            'city_key': city_key,
            'city_name': city_name,
            'n_samples': len(df)
        }

        # Analyze each target
        for target in config.TARGETS:
            if target not in df.columns:
                print(f"⚠ Warning: Target '{target}' not found in data")
                continue

            print(f"\nAnalyzing temporal patterns for {target.upper()}...")

            # Analyze simple lag features
            lag_results = self._analyze_lag_features(df, target, lag_type='simple')
            results[f'{target}_lag_simple'] = lag_results

            # Analyze rolling window features
            rolling_results = self._analyze_lag_features(df, target, lag_type='rolling')
            results[f'{target}_lag_rolling'] = rolling_results

            # Find optimal lags per variable
            optimal_lags = self._find_optimal_lags(lag_results, rolling_results)
            results[f'{target}_optimal_lags'] = optimal_lags

            print(f"  ✓ Analyzed {len(config.LAG_VARIABLES)} variables × {len(config.LAG_RANGE)} lag periods")

            # Create visualizations
            fig_heatmap_simple = self._create_lag_heatmap(
                lag_results, target, 'Simple Lag', city_name
            )
            self.figures[f'{target}_heatmap_simple'] = fig_heatmap_simple

            fig_heatmap_rolling = self._create_lag_heatmap(
                rolling_results, target, 'Rolling Window', city_name
            )
            self.figures[f'{target}_heatmap_rolling'] = fig_heatmap_rolling

            fig_line_plots = self._create_lag_line_plots(
                lag_results, rolling_results, target, city_name
            )
            self.figures[f'{target}_line_plots'] = fig_line_plots

        # Store results
        self.results = results

        print(f"\n{'='*60}")
        print(f"✓ Lag/rolling analysis complete")
        print(f"{'='*60}\n")

        return results

    def _analyze_lag_features(self, df, target, lag_type='simple'):
        """
        Analyze correlations for lag features.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data
        target : str
            Target variable (pos or egg)
        lag_type : str
            'simple' or 'rolling'

        Returns
        -------
        pandas.DataFrame
            Correlation matrix (variables × lag weeks)
        """
        correlation_matrix = []

        for variable in config.LAG_VARIABLES:
            # Get lag features for this variable
            lag_features = self.loader.get_lag_features(df, variable, lag_type=lag_type)

            if len(lag_features) == 0:
                print(f"    ⚠ No {lag_type} lag features found for {variable}")
                continue

            # Calculate correlations for each lag period
            row = {'variable': variable}

            for week in config.LAG_RANGE:
                # Find the feature for this week
                matching_features = [f for f in lag_features if f'{week}' in f]

                if matching_features:
                    feature = matching_features[0]

                    # Calculate correlation
                    valid_mask = df[[feature, target]].notna().all(axis=1)
                    if valid_mask.sum() > 0:
                        x = df.loc[valid_mask, feature]
                        y = df.loc[valid_mask, target]
                        corr, pval = stats.spearmanr(x, y)
                        row[f'lag_{week}'] = corr
                        row[f'lag_{week}_p'] = pval
                    else:
                        row[f'lag_{week}'] = np.nan
                        row[f'lag_{week}_p'] = np.nan
                else:
                    row[f'lag_{week}'] = np.nan
                    row[f'lag_{week}_p'] = np.nan

            correlation_matrix.append(row)

        return pd.DataFrame(correlation_matrix)

    def _find_optimal_lags(self, lag_simple_df, lag_rolling_df):
        """
        Find optimal lag period for each variable.

        Parameters
        ----------
        lag_simple_df : pandas.DataFrame
            Simple lag correlations
        lag_rolling_df : pandas.DataFrame
            Rolling lag correlations

        Returns
        -------
        pandas.DataFrame
            Optimal lags per variable
        """
        optimal_lags = []

        for _, row in lag_simple_df.iterrows():
            variable = row['variable']

            # Get correlations for all lag periods (simple)
            lag_cols = [f'lag_{week}' for week in config.LAG_RANGE]
            lag_corrs = pd.to_numeric(row[lag_cols], errors='coerce').values

            # Find optimal lag (highest absolute correlation)
            abs_corrs = np.abs(lag_corrs)
            if not np.all(np.isnan(abs_corrs)):
                optimal_idx = np.nanargmax(abs_corrs)
                optimal_week = config.LAG_RANGE[optimal_idx]
                optimal_corr = lag_corrs[optimal_idx]
            else:
                optimal_week = np.nan
                optimal_corr = np.nan

            # Get rolling optimal
            rolling_row = lag_rolling_df[lag_rolling_df['variable'] == variable]
            if len(rolling_row) > 0:
                rolling_corrs = pd.to_numeric(rolling_row.iloc[0][lag_cols], errors='coerce').values
                abs_rolling = np.abs(rolling_corrs)

                if not np.all(np.isnan(abs_rolling)):
                    optimal_rolling_idx = np.nanargmax(abs_rolling)
                    optimal_rolling_week = config.LAG_RANGE[optimal_rolling_idx]
                    optimal_rolling_corr = rolling_corrs[optimal_rolling_idx]
                else:
                    optimal_rolling_week = np.nan
                    optimal_rolling_corr = np.nan
            else:
                optimal_rolling_week = np.nan
                optimal_rolling_corr = np.nan

            optimal_lags.append({
                'variable': variable,
                'optimal_lag_simple_weeks': optimal_week,
                'optimal_lag_simple_correlation': optimal_corr,
                'optimal_lag_rolling_weeks': optimal_rolling_week,
                'optimal_lag_rolling_correlation': optimal_rolling_corr
            })

        return pd.DataFrame(optimal_lags)

    def _create_lag_heatmap(self, lag_df, target, lag_type_name, city_name):
        """
        Create heatmap of correlations across lag periods.

        Parameters
        ----------
        lag_df : pandas.DataFrame
            Lag correlation matrix
        target : str
            Target variable
        lag_type_name : str
            Name for title ('Simple Lag' or 'Rolling Window')
        city_name : str
            City name

        Returns
        -------
        matplotlib.figure.Figure
            Heatmap figure
        """
        # Extract correlation values
        lag_cols = [f'lag_{week}' for week in config.LAG_RANGE]
        heatmap_data = lag_df[lag_cols].values

        # Create figure
        fig, ax = plt.subplots(figsize=(12, max(6, len(lag_df) * 0.5)))

        # Create heatmap
        sns.heatmap(
            heatmap_data,
            yticklabels=lag_df['variable'].values,
            xticklabels=config.LAG_RANGE,
            cmap=config.COLORMAP_DIVERGING,
            center=0,
            vmin=-1,
            vmax=1,
            annot=True,
            fmt='.2f',
            cbar_kws={'label': 'Spearman ρ'},
            ax=ax
        )

        ax.set_title(f'{lag_type_name} Correlations with {target.upper()}\n{city_name}',
                    fontsize=config.FONT_SIZE_TITLE, fontweight='bold')
        ax.set_xlabel('Lag (weeks)', fontsize=config.FONT_SIZE_LABEL)
        ax.set_ylabel('Variable', fontsize=config.FONT_SIZE_LABEL)

        plt.xticks(rotation=0, fontsize=config.FONT_SIZE_TICK)
        plt.yticks(rotation=0, fontsize=config.FONT_SIZE_TICK)

        plt.tight_layout()

        return fig

    def _create_lag_line_plots(self, lag_simple_df, lag_rolling_df, target, city_name):
        """
        Create line plots showing correlation vs lag period.

        Parameters
        ----------
        lag_simple_df : pandas.DataFrame
            Simple lag correlations
        lag_rolling_df : pandas.DataFrame
            Rolling lag correlations
        target : str
            Target variable
        city_name : str
            City name

        Returns
        -------
        matplotlib.figure.Figure
            Line plot figure
        """
        n_vars = len(lag_simple_df)
        n_cols = 3
        n_rows = (n_vars + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 4))
        axes = axes.flatten() if n_vars > 1 else [axes]

        lag_cols = [f'lag_{week}' for week in config.LAG_RANGE]

        for idx, (_, row) in enumerate(lag_simple_df.iterrows()):
            if idx >= len(axes):
                break

            ax = axes[idx]
            variable = row['variable']

            # Simple lag line
            simple_corrs = row[lag_cols].values
            ax.plot(config.LAG_RANGE, simple_corrs, marker='o', label='Simple Lag',
                   linewidth=2, markersize=6)

            # Rolling lag line
            rolling_row = lag_rolling_df[lag_rolling_df['variable'] == variable]
            if len(rolling_row) > 0:
                rolling_corrs = rolling_row.iloc[0][lag_cols].values
                ax.plot(config.LAG_RANGE, rolling_corrs, marker='s', label='Rolling Window',
                       linewidth=2, markersize=6)

            ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
            ax.set_xlabel('Lag (weeks)', fontsize=config.FONT_SIZE_LABEL)
            ax.set_ylabel('Spearman ρ', fontsize=config.FONT_SIZE_LABEL)
            ax.set_title(f'{variable}', fontsize=config.FONT_SIZE_TITLE, fontweight='bold')
            ax.legend(fontsize=config.FONT_SIZE_LEGEND)
            ax.grid(alpha=0.3)
            ax.set_ylim(-1, 1)

        # Hide unused subplots
        for idx in range(n_vars, len(axes)):
            axes[idx].set_visible(False)

        fig.suptitle(f'Lag Correlation Patterns: {target.upper()} - {city_name}',
                    fontsize=config.FONT_SIZE_TITLE + 2, fontweight='bold', y=0.995)

        plt.tight_layout()

        return fig

    def generate_methods_section(self):
        """Generate Methods section for academic paper."""
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        return self.writer.generate_methods_template('lag_rolling')

    def generate_results_section(self):
        """Generate Results section for academic paper."""
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        city_name = self.results['city_name']
        lines = []

        # Header
        lines.append(f"## Temporal Lag Analysis: {city_name}\n")

        # Overview
        lines.append(f"### Overview\n")
        lines.append(f"Temporal lag effects were analyzed for {len(config.LAG_VARIABLES)} "
                    f"environmental variables across {min(config.LAG_RANGE)}-{max(config.LAG_RANGE)} "
                    f"week intervals using {self.results['n_samples']:,} observations.\n")

        # Results for each target
        for target in config.TARGETS:
            if f'{target}_optimal_lags' not in self.results:
                continue

            lines.append(f"\n### Optimal Lag Periods for {target.upper()}\n")

            optimal_df = self.results[f'{target}_optimal_lags']

            lines.append(f"**Simple lag features:**\n")
            for _, row in optimal_df.iterrows():
                var = row['variable']
                week = row['optimal_lag_simple_weeks']
                corr = row['optimal_lag_simple_correlation']

                if not np.isnan(week):
                    lines.append(f"- {var}: {int(week)} weeks "
                                f"(ρ = {corr:.3f})")

            lines.append(f"\n**Rolling window features:**\n")
            for _, row in optimal_df.iterrows():
                var = row['variable']
                week = row['optimal_lag_rolling_weeks']
                corr = row['optimal_lag_rolling_correlation']

                if not np.isnan(week):
                    lines.append(f"- {var}: {int(week)} weeks "
                                f"(ρ = {corr:.3f})")

            # Summary
            simple_weeks = optimal_df['optimal_lag_simple_weeks'].dropna()
            rolling_weeks = optimal_df['optimal_lag_rolling_weeks'].dropna()

            if len(simple_weeks) > 0:
                mean_simple = simple_weeks.mean()
                lines.append(f"\nMean optimal lag (simple): {mean_simple:.1f} weeks. ")

            if len(rolling_weeks) > 0:
                mean_rolling = rolling_weeks.mean()
                lines.append(f"Mean optimal lag (rolling): {mean_rolling:.1f} weeks.")

            lines.append(f"\n\n*See Figures: Lag correlation heatmaps and line plots for {target.upper()}*\n")

        return "\n".join(lines)

    def save_outputs(self, output_dir):
        """Save all outputs to directory."""
        if not self.results:
            raise ValueError("No results to save. Run analyze() first.")

        output_dir = self._create_output_dir(output_dir)
        print(f"\nSaving lag/rolling analysis outputs to: {output_dir}")

        saved_files = {}

        # Save results for each target
        for target in config.TARGETS:
            if f'{target}_lag_simple' in self.results:
                # Simple lag correlations
                saved_files[f'lag_simple_{target}'] = self._save_dataframe(
                    self.results[f'{target}_lag_simple'],
                    output_dir,
                    f'lag_correlations_{target}.csv'
                )

                # Rolling lag correlations
                saved_files[f'lag_rolling_{target}'] = self._save_dataframe(
                    self.results[f'{target}_lag_rolling'],
                    output_dir,
                    f'rolling_correlations_{target}.csv'
                )

                # Optimal lags
                saved_files[f'optimal_lags_{target}'] = self._save_dataframe(
                    self.results[f'{target}_optimal_lags'],
                    output_dir,
                    f'optimal_lags_summary_{target}.csv'
                )

                # Figures
                if f'{target}_heatmap_simple' in self.figures:
                    saved_files[f'heatmap_simple_{target}'] = self._save_figure(
                        self.figures[f'{target}_heatmap_simple'],
                        output_dir,
                        f'lag_heatmap_{target}.png'
                    )

                if f'{target}_heatmap_rolling' in self.figures:
                    saved_files[f'heatmap_rolling_{target}'] = self._save_figure(
                        self.figures[f'{target}_heatmap_rolling'],
                        output_dir,
                        f'rolling_heatmap_{target}.png'
                    )

                if f'{target}_line_plots' in self.figures:
                    saved_files[f'line_plots_{target}'] = self._save_figure(
                        self.figures[f'{target}_line_plots'],
                        output_dir,
                        f'lag_line_plots_{target}.png'
                    )

        # Academic sections
        methods_text = self.generate_methods_section()
        results_text = self.generate_results_section()

        saved_files['methods'] = self._save_text(methods_text, output_dir, 'methods.md')
        saved_files['results'] = self._save_text(results_text, output_dir, 'results.md')

        print(f"✓ Saved {len(saved_files)} files")

        return saved_files


# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("TESTING LAG/ROLLING ANALYZER")
    print("=" * 80)

    # Load test data (Taipei)
    print("\nLoading Taipei data for testing...")
    loader = DataLoader()
    df_taipei, metadata = loader.load_city_data('taipei', preprocess=True)

    # Create analyzer
    analyzer = LagRollingAnalyzer()

    # Run analysis
    results = analyzer.analyze(df_taipei, city_key='taipei')

    # Print summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)

    print(f"\nCity: {results['city_name']}")
    print(f"Samples: {results['n_samples']:,}")

    for target in config.TARGETS:
        if f'{target}_optimal_lags' in results:
            print(f"\n{target.upper()} - Optimal Lags:")
            print(results[f'{target}_optimal_lags'].to_string())

    # Save outputs
    print("\n" + "=" * 80)
    print("SAVING OUTPUTS")
    print("=" * 80)

    test_output_dir = os.path.join(config.OUTPUT_DIR, 'test_lag_rolling')
    saved_files = analyzer.save_outputs(test_output_dir)

    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED")
    print("=" * 80)
