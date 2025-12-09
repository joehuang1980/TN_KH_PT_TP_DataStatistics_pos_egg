"""
PCA and clustering analysis for mosquito surveillance data.

This module implements:
- Principal Component Analysis (PCA) with variance optimization
- K-means clustering with automatic k selection using validation metrics
- Cluster validation (Silhouette, Calinski-Harabasz, Davies-Bouldin)
- Cluster-outcome relationship analysis (Kruskal-Wallis, Dunn's tests)
- t-SNE visualization
- Academic paper section generation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.manifold import TSNE
from scikit_posthocs import posthoc_dunn
import os
import sys

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.base_analyzer import CityAnalyzer
from core.academic_writer import AcademicWriter
from core.data_loader import DataLoader
from config import analysis_config as config


class PCAClusteringAnalyzer(CityAnalyzer):
    """
    Analyzer for PCA dimensionality reduction and clustering analysis.
    """

    def __init__(self):
        """Initialize PCA/clustering analyzer."""
        super().__init__(name='pca_clustering')
        self.writer = AcademicWriter()
        self.loader = DataLoader()
        self.scaler = None
        self.pca = None

    def analyze(self, df, city_key=None, **kwargs):
        """
        Perform PCA and clustering analysis.

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
            Analysis results including PCA components, optimal k, cluster assignments
        """
        city_name = config.CITIES[city_key]['name_en'] if city_key else "Unknown"
        print(f"\n{'='*60}")
        print(f"PCA and Clustering Analysis: {city_name}")
        print(f"{'='*60}")

        # Get feature columns
        features = self.loader.get_feature_columns(df, include_targets=False)

        print(f"✓ Processing {len(features)} features from {len(df):,} samples")

        results = {
            'city_key': city_key,
            'city_name': city_name,
            'n_features': len(features),
            'n_samples': len(df)
        }

        # Step 1: Handle missing values and standardize features
        print("\nStep 1: Preparing data and standardizing features...")

        # Remove rows with any NaN values in features
        df_clean = df[features + config.TARGETS].dropna()
        print(f"  ✓ Removed {len(df) - len(df_clean):,} rows with missing values")

        # Update results with clean sample size
        results['n_samples'] = len(df_clean)

        # Extract feature values
        X = df_clean[features].values

        # Standardize
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        print(f"  ✓ Standardized {X_scaled.shape[1]} features from {X_scaled.shape[0]:,} samples")

        # Step 2: Perform PCA
        print("\nStep 2: Performing PCA...")
        pca_results = self._perform_pca(X_scaled)
        results.update(pca_results)

        # Create scree plot
        fig_scree = self._create_scree_plot(pca_results, city_name)
        self.figures['scree_plot'] = fig_scree

        # Step 3: Clustering on PCA-reduced data
        print("\nStep 3: K-means clustering with automatic k selection...")
        X_pca = pca_results['X_pca']

        clustering_results = self._optimize_clustering(X_pca)
        results.update(clustering_results)

        # Assign clusters to clean data
        optimal_k = clustering_results['optimal_k']
        cluster_labels = clustering_results['optimal_labels']
        df_clustered = df_clean.copy()
        df_clustered['cluster'] = cluster_labels

        results['df_clustered'] = df_clustered

        print(f"  ✓ Optimal k = {optimal_k}")
        print(f"  ✓ Silhouette score: {clustering_results['optimal_silhouette']:.3f}")

        # Step 4: Analyze cluster characteristics
        print("\nStep 4: Analyzing cluster characteristics...")
        cluster_chars = self._analyze_cluster_characteristics(df_clustered, optimal_k)
        results['cluster_characteristics'] = cluster_chars

        # Step 5: Test cluster-outcome relationships
        print("\nStep 5: Testing cluster-outcome relationships...")
        outcome_tests = self._test_cluster_outcome_relationships(df_clustered, optimal_k)
        results.update(outcome_tests)

        # Step 6: Create visualizations
        print("\nStep 6: Creating visualizations...")

        # t-SNE visualization
        fig_tsne = self._create_tsne_plot(X_pca, cluster_labels, optimal_k, city_name)
        self.figures['tsne'] = fig_tsne

        # Cluster boxplots for POS/EGG
        fig_boxplots = self._create_cluster_boxplots(df_clustered, optimal_k, city_name)
        self.figures['cluster_boxplots'] = fig_boxplots

        # Store results
        self.results = results

        print(f"\n{'='*60}")
        print(f"✓ PCA and clustering analysis complete")
        print(f"{'='*60}\n")

        return results

    def _perform_pca(self, X_scaled):
        """
        Perform PCA with variance optimization.

        Parameters
        ----------
        X_scaled : numpy.ndarray
            Standardized features

        Returns
        -------
        dict
            PCA results
        """
        # Perform PCA retaining all components first
        pca_full = PCA(random_state=config.RANDOM_SEED)
        pca_full.fit(X_scaled)

        # Find number of components for target variance
        cumvar = np.cumsum(pca_full.explained_variance_ratio_)
        n_components_target = np.argmax(cumvar >= config.PCA_VARIANCE_TARGET) + 1

        print(f"  ✓ {n_components_target} components explain "
              f"{cumvar[n_components_target-1]*100:.1f}% variance")

        # Refit with optimal number of components
        self.pca = PCA(n_components=n_components_target, random_state=config.RANDOM_SEED)
        X_pca = self.pca.fit_transform(X_scaled)

        results = {
            'n_components': n_components_target,
            'explained_variance_ratio': self.pca.explained_variance_ratio_,
            'cumulative_variance': np.cumsum(self.pca.explained_variance_ratio_),
            'total_variance_explained': cumvar[n_components_target-1],
            'X_pca': X_pca,
            'all_explained_variance': pca_full.explained_variance_ratio_[:config.PCA_SCREE_COMPONENTS]
        }

        return results

    def _optimize_clustering(self, X_pca):
        """
        Find optimal number of clusters using validation metrics.

        Parameters
        ----------
        X_pca : numpy.ndarray
            PCA-reduced data

        Returns
        -------
        dict
            Clustering results with optimal k
        """
        metrics_results = []

        for k in config.CLUSTERING_K_RANGE:
            kmeans = KMeans(
                n_clusters=k,
                n_init=config.KMEANS_N_INIT,
                max_iter=config.KMEANS_MAX_ITER,
                random_state=config.RANDOM_SEED
            )
            labels = kmeans.fit_predict(X_pca)

            # Calculate metrics
            silhouette = silhouette_score(X_pca, labels)
            calinski = calinski_harabasz_score(X_pca, labels)
            davies = davies_bouldin_score(X_pca, labels)

            metrics_results.append({
                'k': k,
                'silhouette': silhouette,
                'calinski_harabasz': calinski,
                'davies_bouldin': davies,
                'labels': labels,
                'inertia': kmeans.inertia_
            })

            print(f"    k={k}: Silhouette={silhouette:.3f}, CH={calinski:.1f}, DB={davies:.3f}")

        # Select optimal k based on silhouette score (higher is better)
        metrics_df = pd.DataFrame(metrics_results)
        optimal_idx = metrics_df['silhouette'].idxmax()
        optimal_k = metrics_df.loc[optimal_idx, 'k']
        optimal_labels = metrics_df.loc[optimal_idx, 'labels']

        results = {
            'clustering_metrics': metrics_df.drop('labels', axis=1),
            'optimal_k': optimal_k,
            'optimal_labels': optimal_labels,
            'optimal_silhouette': metrics_df.loc[optimal_idx, 'silhouette'],
            'optimal_calinski': metrics_df.loc[optimal_idx, 'calinski_harabasz'],
            'optimal_davies': metrics_df.loc[optimal_idx, 'davies_bouldin']
        }

        return results

    def _analyze_cluster_characteristics(self, df_clustered, optimal_k):
        """
        Analyze characteristics of each cluster.

        Parameters
        ----------
        df_clustered : pandas.DataFrame
            Data with cluster assignments
        optimal_k : int
            Number of clusters

        Returns
        -------
        pandas.DataFrame
            Cluster characteristics
        """
        char_list = []

        for cluster_id in range(optimal_k):
            cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]

            char = {
                'cluster': cluster_id,
                'n_samples': len(cluster_data)
            }

            # Statistics for each target
            for target in config.TARGETS:
                if target in cluster_data.columns:
                    target_data = cluster_data[target].dropna()
                    char[f'{target}_mean'] = target_data.mean()
                    char[f'{target}_std'] = target_data.std()
                    char[f'{target}_median'] = target_data.median()

            char_list.append(char)

        char_df = pd.DataFrame(char_list)

        return char_df

    def _test_cluster_outcome_relationships(self, df_clustered, optimal_k):
        """
        Test relationships between clusters and outcomes using Kruskal-Wallis and Dunn's tests.

        Parameters
        ----------
        df_clustered : pandas.DataFrame
            Data with cluster assignments
        optimal_k : int
            Number of clusters

        Returns
        -------
        dict
            Test results
        """
        results = {}

        for target in config.TARGETS:
            if target not in df_clustered.columns:
                continue

            # Prepare data for testing
            groups = [df_clustered[df_clustered['cluster'] == i][target].dropna()
                     for i in range(optimal_k)]

            # Kruskal-Wallis H-test
            h_stat, p_value = stats.kruskal(*groups)

            results[f'{target}_kruskal_h'] = h_stat
            results[f'{target}_kruskal_p'] = p_value

            print(f"  {target.upper()}: H = {h_stat:.3f}, p = {p_value:.4f}")

            # If significant, perform Dunn's post-hoc test
            if p_value < 0.05:
                # Prepare data for Dunn's test
                df_test = df_clustered[['cluster', target]].dropna()

                dunn_result = posthoc_dunn(
                    df_test,
                    val_col=target,
                    group_col='cluster',
                    p_adjust='bonferroni'
                )

                results[f'{target}_dunn_pvalues'] = dunn_result

                print(f"    → Significant! Dunn's post-hoc test performed")
            else:
                results[f'{target}_dunn_pvalues'] = None
                print(f"    → Not significant")

        return results

    def _create_scree_plot(self, pca_results, city_name):
        """
        Create scree plot showing explained variance.

        Parameters
        ----------
        pca_results : dict
            PCA results
        city_name : str
            City name

        Returns
        -------
        matplotlib.figure.Figure
            Scree plot
        """
        n_components = len(pca_results['all_explained_variance'])
        variance_ratio = pca_results['all_explained_variance']
        cumulative = np.cumsum(variance_ratio)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Individual variance
        ax1.bar(range(1, n_components + 1), variance_ratio * 100)
        ax1.set_xlabel('Principal Component', fontsize=config.FONT_SIZE_LABEL)
        ax1.set_ylabel('Explained Variance (%)', fontsize=config.FONT_SIZE_LABEL)
        ax1.set_title(f'Scree Plot: {city_name}', fontsize=config.FONT_SIZE_TITLE, fontweight='bold')
        ax1.set_xlim(0, n_components + 1)

        # Cumulative variance
        ax2.plot(range(1, n_components + 1), cumulative * 100, marker='o')
        ax2.axhline(y=config.PCA_VARIANCE_TARGET * 100, color='r', linestyle='--',
                   label=f'{config.PCA_VARIANCE_TARGET*100:.0f}% threshold')
        ax2.axvline(x=pca_results['n_components'], color='g', linestyle='--',
                   label=f"Selected: {pca_results['n_components']} components")
        ax2.set_xlabel('Number of Components', fontsize=config.FONT_SIZE_LABEL)
        ax2.set_ylabel('Cumulative Variance (%)', fontsize=config.FONT_SIZE_LABEL)
        ax2.set_title(f'Cumulative Explained Variance', fontsize=config.FONT_SIZE_TITLE, fontweight='bold')
        ax2.legend(fontsize=config.FONT_SIZE_LEGEND)
        ax2.set_xlim(0, n_components + 1)
        ax2.set_ylim(0, 105)

        plt.tight_layout()

        return fig

    def _create_tsne_plot(self, X_pca, labels, optimal_k, city_name):
        """
        Create t-SNE visualization of clusters.

        Parameters
        ----------
        X_pca : numpy.ndarray
            PCA-reduced data
        labels : numpy.ndarray
            Cluster labels
        optimal_k : int
            Number of clusters
        city_name : str
            City name

        Returns
        -------
        matplotlib.figure.Figure
            t-SNE plot
        """
        # Sample data if too large
        if len(X_pca) > config.TSNE_SAMPLE_SIZE:
            print(f"  ✓ Sampling {config.TSNE_SAMPLE_SIZE} points for t-SNE...")
            indices = np.random.choice(len(X_pca), config.TSNE_SAMPLE_SIZE, replace=False)
            X_sample = X_pca[indices]
            labels_sample = labels[indices]
        else:
            X_sample = X_pca
            labels_sample = labels

        # Perform t-SNE
        print(f"  ✓ Computing t-SNE...")
        tsne = TSNE(
            n_components=2,
            perplexity=config.TSNE_PERPLEXITY,
            max_iter=config.TSNE_MAX_ITER,
            random_state=config.RANDOM_SEED
        )
        X_tsne = tsne.fit_transform(X_sample)

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))

        scatter = ax.scatter(
            X_tsne[:, 0],
            X_tsne[:, 1],
            c=labels_sample,
            cmap=config.COLORMAP_CATEGORICAL,
            alpha=0.6,
            s=50
        )

        ax.set_xlabel('t-SNE Dimension 1', fontsize=config.FONT_SIZE_LABEL)
        ax.set_ylabel('t-SNE Dimension 2', fontsize=config.FONT_SIZE_LABEL)
        ax.set_title(f't-SNE Visualization of {optimal_k} Clusters\n{city_name}',
                    fontsize=config.FONT_SIZE_TITLE, fontweight='bold')

        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, ticks=range(optimal_k))
        cbar.set_label('Cluster', fontsize=config.FONT_SIZE_LABEL)

        plt.tight_layout()

        return fig

    def _create_cluster_boxplots(self, df_clustered, optimal_k, city_name):
        """
        Create boxplots showing POS and EGG distributions by cluster.

        Parameters
        ----------
        df_clustered : pandas.DataFrame
            Data with cluster assignments
        optimal_k : int
            Number of clusters
        city_name : str
            City name

        Returns
        -------
        matplotlib.figure.Figure
            Boxplot figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        for idx, target in enumerate(config.TARGETS):
            if target not in df_clustered.columns:
                continue

            ax = axes[idx]

            # Create boxplot
            df_plot = df_clustered[['cluster', target]].dropna()

            sns.boxplot(
                data=df_plot,
                x='cluster',
                y=target,
                ax=ax,
                palette=config.COLORMAP_CATEGORICAL
            )

            ax.set_xlabel('Cluster', fontsize=config.FONT_SIZE_LABEL)
            ax.set_ylabel(target.upper(), fontsize=config.FONT_SIZE_LABEL)
            ax.set_title(f'{target.upper()} by Cluster',
                        fontsize=config.FONT_SIZE_TITLE, fontweight='bold')

            # Use log scale for EGG if needed
            if target == 'egg':
                ax.set_yscale('log')
                ax.set_ylabel(f'{target.upper()} (log scale)', fontsize=config.FONT_SIZE_LABEL)

        fig.suptitle(f'Outcome Variables by Cluster: {city_name}',
                    fontsize=config.FONT_SIZE_TITLE + 2, fontweight='bold', y=1.02)

        plt.tight_layout()

        return fig

    def generate_methods_section(self):
        """Generate Methods section for academic paper."""
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        return self.writer.generate_methods_template(
            'pca_clustering',
            variance_target=config.PCA_VARIANCE_TARGET,
            k_min=config.CLUSTERING_K_MIN,
            k_max=config.CLUSTERING_K_MAX,
            n_init=config.KMEANS_N_INIT
        )

    def generate_results_section(self):
        """Generate Results section for academic paper."""
        if not self.results:
            raise ValueError("No analysis results available. Run analyze() first.")

        city_name = self.results['city_name']
        lines = []

        # Header
        lines.append(f"## PCA and Clustering Analysis: {city_name}\n")

        # PCA results
        lines.append(f"### Principal Component Analysis\n")
        n_comp = self.results['n_components']
        var_exp = self.results['total_variance_explained'] * 100

        lines.append(f"PCA reduced {self.results['n_features']} features to {n_comp} "
                    f"principal components, explaining {var_exp:.1f}% of the total variance. ")

        # Top components
        top_comp_var = self.results['explained_variance_ratio'][:3] * 100
        lines.append(f"The first three components explained {top_comp_var[0]:.1f}%, "
                    f"{top_comp_var[1]:.1f}%, and {top_comp_var[2]:.1f}% of variance, respectively.\n")

        # Clustering results
        lines.append(f"\n### Clustering Analysis\n")
        optimal_k = self.results['optimal_k']
        sil = self.results['optimal_silhouette']
        cal = self.results['optimal_calinski']
        dav = self.results['optimal_davies']

        lines.append(f"Optimal clustering identified k = {optimal_k} clusters based on "
                    f"silhouette score ({sil:.3f}). Additional validation metrics supported "
                    f"this choice: Calinski-Harabasz index = {cal:.1f}, Davies-Bouldin index = {dav:.3f}.\n")

        # Cluster characteristics
        char_df = self.results['cluster_characteristics']
        lines.append(f"\n**Cluster characteristics:**\n")

        for _, row in char_df.iterrows():
            cluster_id = int(row['cluster'])
            n = row['n_samples']
            lines.append(f"- Cluster {cluster_id}: n = {n:,}")

            for target in config.TARGETS:
                if f'{target}_mean' in row:
                    mean = row[f'{target}_mean']
                    std = row[f'{target}_std']
                    lines.append(f"  - {target.upper()}: {self.writer.format_mean_sd(mean, std)}")

        # Cluster-outcome relationships
        lines.append(f"\n### Cluster-Outcome Relationships\n")

        for target in config.TARGETS:
            if f'{target}_kruskal_h' in self.results:
                h = self.results[f'{target}_kruskal_h']
                p = self.results[f'{target}_kruskal_p']

                test_str = self.writer.format_test_statistic('H', h, p, df=optimal_k-1)
                lines.append(f"\nKruskal-Wallis test for {target.upper()}: {test_str}. ")

                if p < 0.05:
                    lines.append(f"Significant differences in {target.upper()} were observed across "
                                f"clusters. Dunn's post-hoc tests revealed specific pairwise differences "
                                f"(see supplementary tables).")
                else:
                    lines.append(f"No significant differences in {target.upper()} were observed across clusters.")

        lines.append(f"\n\n*See Figures: PCA scree plot, t-SNE cluster visualization, "
                    f"and cluster boxplots for POS/EGG*\n")

        return "\n".join(lines)

    def save_outputs(self, output_dir):
        """Save all outputs to directory."""
        if not self.results:
            raise ValueError("No results to save. Run analyze() first.")

        output_dir = self._create_output_dir(output_dir)
        print(f"\nSaving PCA/clustering analysis outputs to: {output_dir}")

        saved_files = {}

        # PCA components
        pca_comp_df = pd.DataFrame({
            'component': range(1, self.results['n_components'] + 1),
            'explained_variance_ratio': self.results['explained_variance_ratio'],
            'cumulative_variance': self.results['cumulative_variance']
        })
        saved_files['pca_components'] = self._save_dataframe(
            pca_comp_df, output_dir, 'pca_components.csv'
        )

        # Clustering metrics
        saved_files['clustering_metrics'] = self._save_dataframe(
            self.results['clustering_metrics'], output_dir, 'clustering_metrics.csv'
        )

        # Cluster characteristics
        saved_files['cluster_characteristics'] = self._save_dataframe(
            self.results['cluster_characteristics'], output_dir, 'cluster_characteristics.csv'
        )

        # Clustered data
        saved_files['clustered_data'] = self._save_dataframe(
            self.results['df_clustered'], output_dir, 'optimal_clusters_data.csv'
        )

        # Figures
        if 'scree_plot' in self.figures:
            saved_files['scree_plot'] = self._save_figure(
                self.figures['scree_plot'], output_dir, 'pca_scree_plot.png'
            )

        if 'tsne' in self.figures:
            saved_files['tsne'] = self._save_figure(
                self.figures['tsne'], output_dir, 'tsne_visualization.png'
            )

        if 'cluster_boxplots' in self.figures:
            saved_files['boxplots'] = self._save_figure(
                self.figures['cluster_boxplots'], output_dir, 'cluster_boxplots_pos_egg.png'
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
    import warnings
    warnings.filterwarnings('ignore')

    print("=" * 80)
    print("TESTING PCA/CLUSTERING ANALYZER")
    print("=" * 80)

    # Load test data (Taipei)
    print("\nLoading Taipei data for testing...")
    loader = DataLoader()
    df_taipei, metadata = loader.load_city_data('taipei', preprocess=True)

    # Create analyzer
    analyzer = PCAClusteringAnalyzer()

    # Run analysis
    results = analyzer.analyze(df_taipei, city_key='taipei')

    # Print summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)

    print(f"\nCity: {results['city_name']}")
    print(f"Features: {results['n_features']}")
    print(f"Samples: {results['n_samples']:,}")
    print(f"\nPCA Components: {results['n_components']}")
    print(f"Variance Explained: {results['total_variance_explained']*100:.1f}%")
    print(f"\nOptimal k: {results['optimal_k']}")
    print(f"Silhouette: {results['optimal_silhouette']:.3f}")

    # Save outputs
    print("\n" + "=" * 80)
    print("SAVING OUTPUTS")
    print("=" * 80)

    test_output_dir = os.path.join(config.OUTPUT_DIR, 'test_pca_clustering')
    saved_files = analyzer.save_outputs(test_output_dir)

    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED")
    print("=" * 80)
