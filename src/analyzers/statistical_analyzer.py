"""
Statistical correlation analysis for mosquito surveillance data.

This module implements comprehensive statistical analysis including:
- Spearman correlation between all features and targets (POS/EGG)
- Significance testing with Bonferroni correction
- Top feature identification
- Feature grouping by type
- Correlation heatmaps
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
from core.base_analyzer import CityAnalyzer, calculate_correlation, bonferroni_correction
from core.academic_writer import AcademicWriter
from core.data_loader import DataLoader
from config import analysis_config as config


class StatisticalAnalyzer(CityAnalyzer):
    """
    Analyzer for statistical correlation analysis between features and targets.
    """

    def __init__(self):
        """Initialize statistical analyzer."""
        super().__init__(name='statistical')
        self.writer = AcademicWriter()
        self.loader = DataLoader()

    def analyze(self, df, city_key=None, **kwargs):
        """
        Perform statistical correlation analysis.

        Parameters
        ----------
        df : pandas.DataFrame
            Input data with features and targets
        city_key : str, optional
            City identifier
        **kwargs : dict
            Additional parameters

        Returns
        -------
        dict
            Analysis results including correlations, p-values, top features
        """
        city_name = config.CITIES[city_key]['name_en'] if city_key else "Unknown"
        print(f"\n{'='*60}")
        print(f"Statistical Correlation Analysis: {city_name}")
        print(f"{'='*60}")

        # Get feature columns
        features = self.loader.get_feature_columns(df, include_targets=False)
        feature_groups = self.loader.get_feature_groups(df)

        print(f"✓ Analyzing {len(features)} features")

        results = {
            'city_key': city_key,
            'city_name': city_name,
            'n_features': len(features),
            'n_samples': len(df),
            'feature_groups': {k: len(v) for k, v in feature_groups.items()}
        }

        # Analyze each target
        for target in config.TARGETS:
            if target not in df.columns:
                print(f"⚠ Warning: Target '{target}' not found in data")
                continue

            print(f"\nAnalyzing correlations with {target.upper()}...")

            # Calculate correlations
            correlations, p_values = calculate_correlation(
                df, features, target, method=config.CORRELATION_METHOD
            )

            # Bonferroni correction
            corrected_alpha, significant = bonferroni_correction(
                p_values, alpha=config.BONFERRONI_ALPHA
            )

            n_significant = significant.sum()
            print(f"  ✓ Computed {len(correlations)} correlations")
            print(f"  ✓ Significant features (Bonferroni α = {corrected_alpha:.6f}): {n_significant}")

            # Store full results
            results[f'{target}_correlations'] = correlations
            results[f'{target}_p_values'] = p_values
            results[f'{target}_significant'] = significant
            results[f'{target}_n_significant'] = n_significant

            # Get top correlations
            top_pos, top_neg = self._get_top_correlations(
                correlations, p_values,
                n_top=config.N_TOP_CORRELATIONS
            )

            results[f'{target}_top_positive'] = top_pos
            results[f'{target}_top_negative'] = top_neg

            print(f"  ✓ Top positive correlation: {top_pos.iloc[0]['feature']} "
                  f"(ρ = {top_pos.iloc[0]['correlation']:.3f})")
            print(f"  ✓ Top negative correlation: {top_neg.iloc[0]['feature']} "
                  f"(ρ = {top_neg.iloc[0]['correlation']:.3f})")

            # Group correlations by feature type
            grouped_corr = self._group_correlations_by_type(
                correlations, p_values, feature_groups
            )
            results[f'{target}_grouped_correlations'] = grouped_corr

            # Create correlation heatmap
            fig = self._create_correlation_heatmap(
                correlations, p_values,
                target=target,
                city_name=city_name,
                n_features=config.N_HEATMAP_FEATURES
            )
            self.figures[f'{target}_heatmap'] = fig

        # Store results
        self.results = results
        self.metadata['bonferroni_alpha'] = corrected_alpha

        print(f"\n{'='*60}")
        print(f"✓ Statistical analysis complete")
        print(f"{'='*60}\n")

        return results

    def _get_top_correlations(self, correlations, p_values, n_top=20):
        """
        Get top positive and negative correlations.

        Parameters
        ----------
        correlations : pandas.Series
            Correlation coefficients
        p_values : pandas.Series
            P-values
        n_top : int
            Number of top correlations to return

        Returns
        -------
        pandas.DataFrame
            Top positive correlations
        pandas.DataFrame
            Top negative correlations
        """
        # Combine into dataframe
        df = pd.DataFrame({
            'feature': correlations.index,
            'correlation': correlations.values,
            'p_value': p_values.values,
            'abs_correlation': np.abs(correlations.values)
        })

        # Remove NaN correlations
        df = df.dropna()

        # Top positive
        top_positive = df[df['correlation'] > 0].sort_values(
            'correlation', ascending=False
        ).head(n_top)

        # Top negative
        top_negative = df[df['correlation'] < 0].sort_values(
            'correlation', ascending=True
        ).head(n_top)

        return top_positive, top_negative

    def _group_correlations_by_type(self, correlations, p_values, feature_groups):
        """
        Group correlations by feature type (temperature, rainfall, NDVI, demographic).

        Parameters
        ----------
        correlations : pandas.Series
            Correlations
        p_values : pandas.Series
            P-values
        feature_groups : dict
            Dictionary of {group_name: [feature_names]}

        Returns
        -------
        dict
            Grouped correlations {group_name: dataframe}
        """
        grouped = {}

        for group_name, features in feature_groups.items():
            # Get correlations for this group
            group_corr = correlations[correlations.index.isin(features)]
            group_p = p_values[p_values.index.isin(features)]

            # Create dataframe
            group_df = pd.DataFrame({
                'feature': group_corr.index,
                'correlation': group_corr.values,
                'p_value': group_p.values
            })

            # Sort by absolute correlation
            group_df = group_df.sort_values('correlation', key=abs, ascending=False)

            grouped[group_name] = group_df

        return grouped

    def _create_correlation_heatmap(self, correlations, p_values, target,
                                   city_name, n_features=30):
        """
        Create correlation heatmap for top features.

        Parameters
        ----------
        correlations : pandas.Series
            Correlations
        p_values : pandas.Series
            P-values
        target : str
            Target variable name (pos or egg)
        city_name : str
            City name for title
        n_features : int
            Number of top features to show

        Returns
        -------
        matplotlib.figure.Figure
            Heatmap figure
        """
        # Get top features by absolute correlation
        abs_corr = correlations.abs().sort_values(ascending=False).head(n_features)
        top_features = abs_corr.index.tolist()

        # Create data for heatmap (single column)
        heatmap_data = correlations[top_features].values.reshape(-1, 1)

        # Create figure
        fig, ax = plt.subplots(figsize=(6, max(8, n_features * 0.3)))

        # Create heatmap
        sns.heatmap(
            heatmap_data,
            yticklabels=top_features,
            xticklabels=[target.upper()],
            cmap=config.COLORMAP_DIVERGING,
            center=0,
            vmin=-1,
            vmax=1,
            annot=True,
            fmt='.3f',
            cbar_kws={'label': 'Spearman ρ'},
            ax=ax
        )

        # Format
        ax.set_title(f'Top {n_features} Feature Correlations with {target.upper()}\n{city_name}',
                    fontsize=config.FONT_SIZE_TITLE, fontweight='bold')
        ax.set_xlabel('Target Variable', fontsize=config.FONT_SIZE_LABEL)
        ax.set_ylabel('Features', fontsize=config.FONT_SIZE_LABEL)

        # Rotate labels
        plt.xticks(rotation=0, fontsize=config.FONT_SIZE_TICK)
        plt.yticks(rotation=0, fontsize=config.FONT_SIZE_TICK)

        plt.tight_layout()

        return fig

    def generate_methods_section(self):
        """
        Generate Methods section for academic paper.

        Returns
        -------
        str
            Methods section text (English, markdown format)
        """
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        return self.writer.generate_methods_template(
            'statistical',
            n_features=self.results['n_features'],
            alpha=self.metadata.get('bonferroni_alpha', config.BONFERRONI_CORRECTED_ALPHA)
        )

    def generate_results_section(self):
        """
        Generate Results section for academic paper.

        Returns
        -------
        str
            Results section text with statistics (English, markdown format)
        """
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        city_name = self.results['city_name']
        n_features = self.results['n_features']
        n_samples = self.results['n_samples']

        lines = []

        # Header
        lines.append(f"## Statistical Correlation Analysis: {city_name}\n")

        # Overview
        lines.append(f"### Overview\n")
        lines.append(f"Spearman rank correlations were calculated between {n_features} "
                    f"environmental and demographic features and outcome variables (POS and EGG) "
                    f"using {n_samples:,} observations from {city_name}.\n")

        # Results for each target
        for target in config.TARGETS:
            if f'{target}_correlations' not in self.results:
                continue

            lines.append(f"\n### Correlations with {target.upper()}\n")

            # Number of significant features
            n_sig = self.results[f'{target}_n_significant']
            corr_alpha = self.metadata.get('bonferroni_alpha', config.BONFERRONI_CORRECTED_ALPHA)

            lines.append(f"Of {n_features} features analyzed, {n_sig} showed statistically "
                        f"significant correlations with {target.upper()} after Bonferroni "
                        f"correction (α = {corr_alpha:.6f}).\n")

            # Top positive correlations
            top_pos = self.results[f'{target}_top_positive']
            if len(top_pos) > 0:
                lines.append(f"\n**Strongest positive correlations:**\n")

                for i, row in top_pos.head(5).iterrows():
                    corr_str = self.writer.format_correlation(row['correlation'], row['p_value'])
                    lines.append(f"- {row['feature']}: {corr_str}")

            # Top negative correlations
            top_neg = self.results[f'{target}_top_negative']
            if len(top_neg) > 0:
                lines.append(f"\n**Strongest negative correlations:**\n")

                for i, row in top_neg.head(5).iterrows():
                    corr_str = self.writer.format_correlation(row['correlation'], row['p_value'])
                    lines.append(f"- {row['feature']}: {corr_str}")

            # Feature group summary
            grouped = self.results[f'{target}_grouped_correlations']
            lines.append(f"\n**Correlations by feature group:**\n")

            for group_name, group_df in grouped.items():
                if len(group_df) > 0:
                    mean_abs_corr = group_df['correlation'].abs().mean()
                    max_corr = group_df.iloc[0]  # Already sorted by abs correlation

                    lines.append(f"- {group_name.capitalize()}: mean |ρ| = {mean_abs_corr:.3f}, "
                                f"strongest = {max_corr['feature']} "
                                f"({self.writer.format_correlation(max_corr['correlation'], max_corr['p_value'])})")

            # Reference to figure
            lines.append(f"\n*See Figure: Top {config.N_HEATMAP_FEATURES} feature correlations "
                        f"with {target.upper()} (heatmap)*\n")

        return "\n".join(lines)

    def save_outputs(self, output_dir):
        """
        Save all outputs to directory.

        Parameters
        ----------
        output_dir : str
            Output directory

        Returns
        -------
        dict
            Dictionary of saved file paths
        """
        if not self.results:
            raise ValueError("No results to save. Run analyze() first.")

        # Create output directory
        output_dir = self._create_output_dir(output_dir)
        print(f"\nSaving statistical analysis outputs to: {output_dir}")

        saved_files = {}

        # Save correlations for each target
        for target in config.TARGETS:
            if f'{target}_correlations' not in self.results:
                continue

            # Full correlations
            corr_df = pd.DataFrame({
                'feature': self.results[f'{target}_correlations'].index,
                'correlation': self.results[f'{target}_correlations'].values,
                'p_value': self.results[f'{target}_p_values'].values,
                'significant': self.results[f'{target}_significant']
            })
            corr_df = corr_df.sort_values('correlation', key=abs, ascending=False)

            saved_files[f'correlations_{target}'] = self._save_dataframe(
                corr_df, output_dir, f'correlations_{target}.csv'
            )

            # Top positive
            saved_files[f'top_positive_{target}'] = self._save_dataframe(
                self.results[f'{target}_top_positive'],
                output_dir,
                f'top_features_{target}_positive.csv'
            )

            # Top negative
            saved_files[f'top_negative_{target}'] = self._save_dataframe(
                self.results[f'{target}_top_negative'],
                output_dir,
                f'top_features_{target}_negative.csv'
            )

            # Heatmap
            if f'{target}_heatmap' in self.figures:
                saved_files[f'heatmap_{target}'] = self._save_figure(
                    self.figures[f'{target}_heatmap'],
                    output_dir,
                    f'correlation_heatmap_{target}.png'
                )

        # Save methods and results sections
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
    print("TESTING STATISTICAL ANALYZER")
    print("=" * 80)

    # Load test data (Taipei)
    print("\nLoading Taipei data for testing...")
    loader = DataLoader()
    df_taipei, metadata = loader.load_city_data('taipei', preprocess=True)

    # Create analyzer
    analyzer = StatisticalAnalyzer()

    # Run analysis
    results = analyzer.analyze(df_taipei, city_key='taipei')

    # Print summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)

    print(f"\nCity: {results['city_name']}")
    print(f"Features analyzed: {results['n_features']}")
    print(f"Samples: {results['n_samples']:,}")

    for target in config.TARGETS:
        if f'{target}_n_significant' in results:
            print(f"\n{target.upper()}:")
            print(f"  Significant features: {results[f'{target}_n_significant']}")
            print(f"  Top positive: {results[f'{target}_top_positive'].iloc[0]['feature']} "
                  f"(ρ = {results[f'{target}_top_positive'].iloc[0]['correlation']:.3f})")
            print(f"  Top negative: {results[f'{target}_top_negative'].iloc[0]['feature']} "
                  f"(ρ = {results[f'{target}_top_negative'].iloc[0]['correlation']:.3f})")

    # Generate academic sections
    print("\n" + "=" * 80)
    print("METHODS SECTION (first 500 chars)")
    print("=" * 80)
    print(analyzer.generate_methods_section()[:500] + "...")

    print("\n" + "=" * 80)
    print("RESULTS SECTION (first 500 chars)")
    print("=" * 80)
    print(analyzer.generate_results_section()[:500] + "...")

    # Save outputs
    print("\n" + "=" * 80)
    print("SAVING OUTPUTS")
    print("=" * 80)

    test_output_dir = os.path.join(config.OUTPUT_DIR, 'test_statistical')
    saved_files = analyzer.save_outputs(test_output_dir)

    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED")
    print("=" * 80)
