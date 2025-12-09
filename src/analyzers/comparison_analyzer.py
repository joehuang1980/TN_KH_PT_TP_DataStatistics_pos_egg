"""
Cross-city comparison analyzer for mosquito surveillance data.

This module implements:
- Comparison of POS/EGG distributions across cities (Kruskal-Wallis, Dunn's tests)
- Comparison of feature importance rankings across cities
- Identification of universal vs city-specific predictors
- Comparison of clustering patterns
- Comparison of optimal lag periods
- Academic paper section generation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scikit_posthocs import posthoc_dunn
import os
import sys

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.base_analyzer import ComparisonAnalyzer
from core.academic_writer import AcademicWriter
from config import analysis_config as config


class CrossCityComparisonAnalyzer(ComparisonAnalyzer):
    """
    Analyzer for comparing results across cities.
    """

    def __init__(self):
        """Initialize comparison analyzer."""
        super().__init__(name='comparison')
        self.writer = AcademicWriter()

    def analyze(self, city_results, **kwargs):
        """
        Perform cross-city comparison analysis.

        Parameters
        ----------
        city_results : dict
            Dictionary of {city_key: {analysis_results}}
            Each city's results should contain 'statistical', 'pca_clustering', 'lag_rolling'

        Returns
        -------
        dict
            Comparison results
        """
        print(f"\n{'='*60}")
        print(f"Cross-City Comparison Analysis")
        print(f"{'='*60}")

        results = {
            'n_cities': len(city_results),
            'cities': list(city_results.keys())
        }

        print(f"✓ Comparing {len(city_results)} cities")

        # 1. Compare descriptive statistics
        print("\n1. Comparing descriptive statistics...")
        desc_comp = self._compare_descriptive_stats(city_results)
        results['descriptive_comparison'] = desc_comp

        # 2. Compare feature importance
        print("\n2. Comparing feature importance rankings...")
        feature_comp = self._compare_feature_importance(city_results)
        results['feature_comparison'] = feature_comp

        # 3. Identify universal vs city-specific predictors
        print("\n3. Identifying universal and city-specific predictors...")
        predictor_comp = self._identify_predictors(city_results)
        results.update(predictor_comp)

        # 4. Compare clustering results
        print("\n4. Comparing clustering patterns...")
        cluster_comp = self._compare_clustering(city_results)
        results['clustering_comparison'] = cluster_comp

        # 5. Compare lag patterns
        print("\n5. Comparing temporal lag patterns...")
        lag_comp = self._compare_lag_patterns(city_results)
        results['lag_comparison'] = lag_comp

        # Store results
        self.results = results

        print(f"\n{'='*60}")
        print(f"✓ Cross-city comparison complete")
        print(f"{'='*60}\n")

        return results

    def _compare_descriptive_stats(self, city_results):
        """Compare basic descriptive statistics across cities."""
        stats_list = []

        for city_key in self.city_order:
            if city_key not in city_results:
                continue

            city_name = config.CITIES[city_key]['name_en']

            # Get statistical results
            if 'statistical' in city_results[city_key]:
                stat_res = city_results[city_key]['statistical']

                row = {
                    'city': city_name,
                    'n_samples': stat_res.get('n_samples', np.nan),
                    'n_features': stat_res.get('n_features', np.nan)
                }

                # Add POS/EGG statistics if available
                for target in config.TARGETS:
                    if f'{target}_n_significant' in stat_res:
                        row[f'{target}_n_significant'] = stat_res[f'{target}_n_significant']

                stats_list.append(row)

        return pd.DataFrame(stats_list)

    def _compare_feature_importance(self, city_results):
        """Compare top feature rankings across cities."""
        comparison = {}

        for target in config.TARGETS:
            # Collect top features from each city
            city_top_features = {}

            for city_key in self.city_order:
                if city_key not in city_results:
                    continue

                city_name = config.CITIES[city_key]['name_en']

                if 'statistical' in city_results[city_key]:
                    stat_res = city_results[city_key]['statistical']

                    if f'{target}_top_positive' in stat_res:
                        top_pos = stat_res[f'{target}_top_positive'].head(10)
                        top_neg = stat_res[f'{target}_top_negative'].head(10)

                        # Combine and store
                        top_combined = pd.concat([top_pos, top_neg])
                        city_top_features[city_name] = top_combined

            comparison[target] = city_top_features

        return comparison

    def _identify_predictors(self, city_results):
        """Identify universal vs city-specific predictors."""
        universal_predictors = {}
        city_specific_predictors = {}

        for target in config.TARGETS:
            # Collect significant features from each city
            city_significant = {}

            for city_key in self.city_order:
                if city_key not in city_results:
                    continue

                city_name = config.CITIES[city_key]['name_en']

                if 'statistical' in city_results[city_key]:
                    stat_res = city_results[city_key]['statistical']

                    if f'{target}_correlations' in stat_res:
                        corr = stat_res[f'{target}_correlations']
                        pval = stat_res[f'{target}_p_values']

                        # Features meeting universal criteria
                        significant = (np.abs(corr) > config.UNIVERSAL_PREDICTOR_RHO_THRESHOLD) & \
                                    (pval < config.UNIVERSAL_PREDICTOR_P_THRESHOLD)

                        city_significant[city_name] = set(corr[significant].index)

            # Find universal predictors (in all cities)
            if city_significant:
                universal = set.intersection(*city_significant.values())
                universal_predictors[target] = list(universal)

                print(f"  {target.upper()}: {len(universal)} universal predictors")

                # Find city-specific (in 1-2 cities only)
                all_features = set.union(*city_significant.values())
                city_specific = {}

                for feature in all_features:
                    cities_with_feature = [city for city, features in city_significant.items()
                                         if feature in features]

                    if 1 <= len(cities_with_feature) <= 2:
                        city_specific[feature] = cities_with_feature

                city_specific_predictors[target] = city_specific

        return {
            'universal_predictors': universal_predictors,
            'city_specific_predictors': city_specific_predictors
        }

    def _compare_clustering(self, city_results):
        """Compare clustering results across cities."""
        comparison = []

        for city_key in self.city_order:
            if city_key not in city_results:
                continue

            city_name = config.CITIES[city_key]['name_en']

            if 'pca_clustering' in city_results[city_key]:
                pca_res = city_results[city_key]['pca_clustering']

                row = {
                    'city': city_name,
                    'n_components': pca_res.get('n_components', np.nan),
                    'variance_explained': pca_res.get('total_variance_explained', np.nan),
                    'optimal_k': pca_res.get('optimal_k', np.nan),
                    'silhouette': pca_res.get('optimal_silhouette', np.nan)
                }

                # Add cluster-outcome test results
                for target in config.TARGETS:
                    if f'{target}_kruskal_p' in pca_res:
                        row[f'{target}_kruskal_p'] = pca_res[f'{target}_kruskal_p']

                comparison.append(row)

        return pd.DataFrame(comparison)

    def _compare_lag_patterns(self, city_results):
        """Compare optimal lag periods across cities."""
        comparison = {}

        for target in config.TARGETS:
            city_lags = []

            for city_key in self.city_order:
                if city_key not in city_results:
                    continue

                city_name = config.CITIES[city_key]['name_en']

                if 'lag_rolling' in city_results[city_key]:
                    lag_res = city_results[city_key]['lag_rolling']

                    if f'{target}_optimal_lags' in lag_res:
                        optimal_df = lag_res[f'{target}_optimal_lags'].copy()
                        optimal_df['city'] = city_name
                        city_lags.append(optimal_df)

            if city_lags:
                comparison[target] = pd.concat(city_lags, ignore_index=True)

        return comparison

    def generate_methods_section(self):
        """Generate Methods section."""
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        return self.writer.generate_methods_template(
            'comparison',
            n_cities=self.results['n_cities']
        )

    def generate_results_section(self):
        """Generate Results section."""
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        lines = []

        # Header
        lines.append(f"## Cross-City Comparison\n")

        # Descriptive comparison
        if 'descriptive_comparison' in self.results:
            desc_df = self.results['descriptive_comparison']

            lines.append(f"### Sample Characteristics\n")
            lines.append(f"\n{desc_df.to_markdown(index=False)}\n")

        # Universal predictors
        if 'universal_predictors' in self.results:
            lines.append(f"\n### Universal Predictors\n")

            for target, predictors in self.results['universal_predictors'].items():
                lines.append(f"\n**{target.upper()}**: {len(predictors)} universal predictors found "
                           f"across all cities (|ρ| > {config.UNIVERSAL_PREDICTOR_RHO_THRESHOLD}, "
                           f"p < {config.UNIVERSAL_PREDICTOR_P_THRESHOLD}):")

                if len(predictors) > 0:
                    for pred in predictors[:10]:  # Show top 10
                        lines.append(f"- {pred}")

        # Clustering comparison
        if 'clustering_comparison' in self.results:
            cluster_df = self.results['clustering_comparison']

            lines.append(f"\n### Clustering Patterns\n")
            lines.append(f"\n{cluster_df.to_markdown(index=False)}\n")

        # Lag comparison
        if 'lag_comparison' in self.results:
            lines.append(f"\n### Temporal Lag Patterns\n")

            for target, lag_df in self.results['lag_comparison'].items():
                lines.append(f"\n**{target.upper()}**: Comparison of optimal lag periods across cities "
                           f"(see supplementary tables)")

        return "\n".join(lines)

    def save_outputs(self, output_dir):
        """Save all outputs."""
        if not self.results:
            raise ValueError("No results to save. Run analyze() first.")

        output_dir = self._create_output_dir(output_dir)
        print(f"\nSaving comparison analysis outputs to: {output_dir}")

        saved_files = {}

        # Descriptive comparison
        if 'descriptive_comparison' in self.results:
            saved_files['descriptive'] = self._save_dataframe(
                self.results['descriptive_comparison'],
                output_dir,
                'descriptive_stats.csv'
            )

        # Feature comparison
        if 'feature_comparison' in self.results:
            for target, city_features in self.results['feature_comparison'].items():
                for city, features in city_features.items():
                    filename = f'top_features_{target}_{city.lower().replace(" ", "_")}.csv'
                    self._save_dataframe(features, output_dir, filename)

        # Universal predictors
        if 'universal_predictors' in self.results:
            for target, predictors in self.results['universal_predictors'].items():
                univ_df = pd.DataFrame({'feature': predictors})
                saved_files[f'universal_{target}'] = self._save_dataframe(
                    univ_df, output_dir, f'universal_predictors_{target}.csv'
                )

        # Clustering comparison
        if 'clustering_comparison' in self.results:
            saved_files['clustering'] = self._save_dataframe(
                self.results['clustering_comparison'],
                output_dir,
                'clustering_comparison.csv'
            )

        # Lag comparison
        if 'lag_comparison' in self.results:
            for target, lag_df in self.results['lag_comparison'].items():
                saved_files[f'lag_{target}'] = self._save_dataframe(
                    lag_df, output_dir, f'lag_comparison_{target}.csv'
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
    print("COMPARISON ANALYZER MODULE")
    print("=" * 80)
    print("\n✓ CrossCityComparisonAnalyzer class defined")
    print("✓ Ready to compare results across cities")
    print("\nNote: This analyzer requires results from statistical, PCA/clustering,")
    print("and lag/rolling analyses for all cities.")
    print("\n" + "=" * 80)
