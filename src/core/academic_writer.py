"""
Academic writing utilities for generating Methods and Results sections.

This module provides functions to format statistical results, generate academic
text in English, and create publication-ready content for research papers.
"""

import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import analysis_config as config


class AcademicWriter:
    """
    Utility class for generating academic paper sections.
    """

    def __init__(self, language='english'):
        """
        Initialize academic writer.

        Parameters
        ----------
        language : str, default='english'
            Language for output ('english' or 'chinese')
        """
        self.language = language
        self.decimal_places = config.STAT_REPORTING['decimal_places']
        self.p_threshold = config.STAT_REPORTING['p_value_threshold']

    def format_p_value(self, p):
        """
        Format p-value for reporting.

        Parameters
        ----------
        p : float
            P-value

        Returns
        -------
        str
            Formatted p-value string
        """
        if pd.isna(p):
            return "p = NA"
        elif p < self.p_threshold:
            return f"p < {self.p_threshold}"
        else:
            return f"p = {p:.{self.decimal_places}f}"

    def format_correlation(self, rho, p=None):
        """
        Format correlation coefficient with optional p-value.

        Parameters
        ----------
        rho : float
            Correlation coefficient
        p : float, optional
            P-value

        Returns
        -------
        str
            Formatted correlation string
        """
        rho_str = f"ρ = {rho:.{self.decimal_places}f}"

        if p is not None:
            p_str = self.format_p_value(p)
            return f"{rho_str}, {p_str}"
        else:
            return rho_str

    def format_test_statistic(self, stat_name, stat_value, p_value, df=None):
        """
        Format test statistic with p-value.

        Parameters
        ----------
        stat_name : str
            Name of test statistic (e.g., 'H', 't', 'F')
        stat_value : float
            Test statistic value
        p_value : float
            P-value
        df : int or tuple, optional
            Degrees of freedom

        Returns
        -------
        str
            Formatted test statistic string
        """
        stat_str = f"{stat_name} = {stat_value:.{self.decimal_places}f}"

        if df is not None:
            if isinstance(df, tuple):
                df_str = f"({df[0]}, {df[1]})"
            else:
                df_str = f"({df})"
            stat_str += df_str

        p_str = self.format_p_value(p_value)

        return f"{stat_str}, {p_str}"

    def format_mean_sd(self, mean, sd):
        """
        Format mean ± SD.

        Parameters
        ----------
        mean : float
            Mean value
        sd : float
            Standard deviation

        Returns
        -------
        str
            Formatted string
        """
        return f"{mean:.{self.decimal_places}f} ± {sd:.{self.decimal_places}f}"

    def format_range(self, min_val, max_val):
        """
        Format range.

        Parameters
        ----------
        min_val : float
            Minimum value
        max_val : float
            Maximum value

        Returns
        -------
        str
            Formatted range string
        """
        return f"{min_val:.{self.decimal_places}f}–{max_val:.{self.decimal_places}f}"

    def format_percentage(self, value, total=None):
        """
        Format percentage.

        Parameters
        ----------
        value : float
            Value (0-1 if total not provided, otherwise raw count)
        total : float, optional
            Total for calculating percentage

        Returns
        -------
        str
            Formatted percentage string
        """
        if total is not None:
            pct = (value / total) * 100
        else:
            pct = value * 100

        return f"{pct:.1f}%"

    def create_descriptive_table(self, df, variables, caption="Descriptive statistics"):
        """
        Create descriptive statistics table in markdown format.

        Parameters
        ----------
        df : pandas.DataFrame
            Data
        variables : list
            List of variable names
        caption : str
            Table caption

        Returns
        -------
        str
            Markdown table
        """
        stats = []

        for var in variables:
            if var in df.columns:
                data = df[var].dropna()
                stats.append({
                    'Variable': var,
                    'N': len(data),
                    'Mean': data.mean(),
                    'SD': data.std(),
                    'Min': data.min(),
                    'Median': data.median(),
                    'Max': data.max()
                })

        stats_df = pd.DataFrame(stats)

        # Format numbers
        for col in ['Mean', 'SD', 'Min', 'Median', 'Max']:
            if col in stats_df.columns:
                stats_df[col] = stats_df[col].apply(lambda x: f"{x:.{self.decimal_places}f}")

        # Convert to markdown
        table = self._dataframe_to_markdown(stats_df, caption)

        return table

    def create_correlation_table(self, correlations, p_values, top_n=10,
                                caption="Top correlations"):
        """
        Create correlation table with p-values.

        Parameters
        ----------
        correlations : pandas.Series
            Correlation coefficients
        p_values : pandas.Series
            P-values
        top_n : int, default=10
            Number of top correlations to include
        caption : str
            Table caption

        Returns
        -------
        str
            Markdown table
        """
        # Combine and sort by absolute correlation
        df = pd.DataFrame({
            'Feature': correlations.index,
            'Correlation': correlations.values,
            'P-value': p_values.values
        })

        df = df.sort_values('Correlation', key=abs, ascending=False).head(top_n)

        # Format
        df['Correlation'] = df['Correlation'].apply(
            lambda x: f"{x:.{self.decimal_places}f}"
        )
        df['P-value'] = df['P-value'].apply(self.format_p_value)

        # Convert to markdown
        table = self._dataframe_to_markdown(df, caption)

        return table

    def _dataframe_to_markdown(self, df, caption=None):
        """
        Convert pandas DataFrame to markdown table.

        Parameters
        ----------
        df : pandas.DataFrame
            Data to convert
        caption : str, optional
            Table caption

        Returns
        -------
        str
            Markdown table string
        """
        lines = []

        if caption:
            lines.append(f"**{caption}**\n")

        # Header
        header = "| " + " | ".join(df.columns) + " |"
        separator = "|" + "|".join(["---"] * len(df.columns)) + "|"

        lines.append(header)
        lines.append(separator)

        # Rows
        for _, row in df.iterrows():
            row_str = "| " + " | ".join(str(v) for v in row.values) + " |"
            lines.append(row_str)

        return "\n".join(lines)

    def generate_methods_template(self, analysis_type, **kwargs):
        """
        Generate methods section template for specific analysis type.

        Parameters
        ----------
        analysis_type : str
            Type of analysis ('statistical', 'pca_clustering', 'lag_rolling', 'comparison')
        **kwargs : dict
            Additional parameters specific to analysis type

        Returns
        -------
        str
            Methods section text
        """
        if analysis_type == 'statistical':
            return self._generate_statistical_methods(**kwargs)
        elif analysis_type == 'pca_clustering':
            return self._generate_pca_clustering_methods(**kwargs)
        elif analysis_type == 'lag_rolling':
            return self._generate_lag_rolling_methods(**kwargs)
        elif analysis_type == 'comparison':
            return self._generate_comparison_methods(**kwargs)
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")

    def _generate_statistical_methods(self, **kwargs):
        """Generate methods section for statistical analysis."""
        n_features = kwargs.get('n_features', config.TOTAL_FEATURES)
        alpha = kwargs.get('alpha', config.BONFERRONI_CORRECTED_ALPHA)

        text = f"""
### Statistical Correlation Analysis

Spearman rank correlation coefficients (ρ) were calculated between {n_features}
environmental and demographic features and two outcome variables: ovitrap positive
rate (POS) and average egg count (EGG), for each city independently. Spearman's
method was chosen due to its robustness to non-normal distributions and outliers,
which are common in ecological surveillance data.

Statistical significance was assessed using two-tailed tests with Bonferroni
correction for multiple comparisons (α = {alpha:.6f}, derived from family-wise
error rate of 0.05 divided by {n_features} tests). Features were ranked by
absolute correlation strength, and the top 20 positive and negative correlations
were identified for each outcome variable.

Features were categorized into four groups for interpretation: (1) temperature
variables (high, mean, and low temperature with temporal lags), (2) rainfall
variables (precipitation with temporal lags), (3) vegetation indices (NDVI mean,
median, and sum with temporal lags), and (4) demographic variables (population
characteristics).
"""
        return text.strip()

    def _generate_pca_clustering_methods(self, **kwargs):
        """Generate methods section for PCA and clustering analysis."""
        variance_target = kwargs.get('variance_target', config.PCA_VARIANCE_TARGET)
        k_min = kwargs.get('k_min', config.CLUSTERING_K_MIN)
        k_max = kwargs.get('k_max', config.CLUSTERING_K_MAX)
        n_init = kwargs.get('n_init', config.KMEANS_N_INIT)

        text = f"""
### Dimensionality Reduction and Clustering

Principal Component Analysis (PCA) was applied to standardized feature matrices
(z-score normalization using StandardScaler) to reduce dimensionality while
retaining ≥{variance_target*100:.0f}% of cumulative variance. The number of
components was determined individually for each city based on the scree plot
and explained variance ratios.

K-means clustering was performed on PCA-reduced data to identify distinct
environmental-demographic profiles. The optimal number of clusters (k) was
determined using three complementary validation metrics: (1) Silhouette score
(range: -1 to 1, higher indicates better-defined clusters), (2) Calinski-Harabasz
index (higher indicates better separation), and (3) Davies-Bouldin index (lower
indicates better separation). K-means was tested for k = {k_min} to {k_max} with
{n_init} random initializations to ensure stability.

Associations between cluster membership and outcome variables (POS and EGG) were
assessed using Kruskal-Wallis H-tests, a non-parametric alternative to ANOVA
suitable for non-normal distributions. When significant differences were detected
(p < 0.05), Dunn's post-hoc tests with Bonferroni correction were performed for
pairwise cluster comparisons.

t-distributed Stochastic Neighbor Embedding (t-SNE) was used to visualize
high-dimensional clusters in two dimensions, with perplexity = {config.TSNE_PERPLEXITY}
and {config.TSNE_MAX_ITER} iterations.
"""
        return text.strip()

    def _generate_lag_rolling_methods(self, **kwargs):
        """Generate methods section for lag/rolling analysis."""
        lag_min = min(config.LAG_RANGE)
        lag_max = max(config.LAG_RANGE)

        text = f"""
### Temporal Lag Effect Analysis

To assess temporal relationships between environmental variables and mosquito
activity, we analyzed correlation patterns across {lag_min}-{lag_max} week lag
intervals. Two types of temporal features were examined: (1) simple lag features,
representing values from t-n weeks prior, and (2) rolling window features,
representing moving averages from t-n to t weeks.

For each environmental variable (high/mean/low temperature, rainfall, and NDVI),
Spearman correlations were calculated between lag features and outcome variables
(POS and EGG) at each weekly interval. The optimal lag period was identified as
the interval with the highest absolute correlation coefficient. This analysis
was performed separately for each city to account for regional differences in
mosquito lifecycle dynamics and environmental response times.

Correlation patterns were visualized using heatmaps (features × lag weeks) and
line plots (correlation strength × lag period). Significance was assessed using
two-tailed tests with p < 0.05 threshold.
"""
        return text.strip()

    def _generate_comparison_methods(self, **kwargs):
        """Generate methods section for cross-city comparison."""
        n_cities = kwargs.get('n_cities', len(config.CITY_ORDER))

        text = f"""
### Cross-City Comparison Analysis

Statistical comparisons across {n_cities} cities were performed to identify
universal versus city-specific predictors of mosquito activity. Outcome variable
distributions (POS and EGG) were compared using Kruskal-Wallis H-tests, followed
by Dunn's post-hoc tests with Bonferroni correction for pairwise comparisons.

Feature importance rankings were compared across cities by calculating Spearman
correlations between each city's ranked feature lists. Universal predictors were
defined as features meeting two criteria in all cities: (1) |ρ| > {config.UNIVERSAL_PREDICTOR_RHO_THRESHOLD}
and (2) p < {config.UNIVERSAL_PREDICTOR_P_THRESHOLD}. City-specific predictors
were defined as features meeting these criteria in only one or two cities.

Clustering patterns (optimal k and cluster-outcome relationships) and temporal
lag effects (optimal lag periods) were also compared across cities to identify
consistent versus location-specific patterns.
"""
        return text.strip()


# ==============================================================================
# CONVENIENCE FUNCTIONS
# ==============================================================================

def format_results_header(city_name, analysis_type):
    """
    Create formatted header for results section.

    Parameters
    ----------
    city_name : str
        City name
    analysis_type : str
        Type of analysis

    Returns
    -------
    str
        Formatted header
    """
    return f"## Results: {analysis_type.replace('_', ' ').title()} - {city_name}\n"


def create_figure_caption(figure_number, description):
    """
    Create figure caption.

    Parameters
    ----------
    figure_number : int
        Figure number
    description : str
        Figure description

    Returns
    -------
    str
        Formatted caption
    """
    return f"**Figure {figure_number}.** {description}"


def create_table_caption(table_number, description):
    """
    Create table caption.

    Parameters
    ----------
    table_number : int
        Table number
    description : str
        Table description

    Returns
    -------
    str
        Formatted caption
    """
    return f"**Table {table_number}.** {description}"


# ==============================================================================
# MODULE TEST
# ==============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("ACADEMIC WRITER MODULE")
    print("=" * 80)

    writer = AcademicWriter(language='english')

    print("\n✓ AcademicWriter initialized")

    # Test formatting functions
    print("\nTesting formatting functions:")
    print(f"  P-value: {writer.format_p_value(0.0001)}")
    print(f"  P-value: {writer.format_p_value(0.045)}")
    print(f"  Correlation: {writer.format_correlation(0.654, 0.0001)}")
    print(f"  Test statistic: {writer.format_test_statistic('H', 15.234, 0.0001, df=3)}")
    print(f"  Mean ± SD: {writer.format_mean_sd(45.6, 12.3)}")
    print(f"  Range: {writer.format_range(10.5, 98.7)}")
    print(f"  Percentage: {writer.format_percentage(0.456)}")

    # Test methods generation
    print("\nTesting methods section generation:")
    print("\n" + "-" * 80)
    print("STATISTICAL METHODS:")
    print("-" * 80)
    print(writer.generate_methods_template('statistical'))

    print("\n" + "-" * 80)
    print("PCA/CLUSTERING METHODS:")
    print("-" * 80)
    print(writer.generate_methods_template('pca_clustering'))

    print("\n" + "-" * 80)
    print("LAG/ROLLING METHODS:")
    print("-" * 80)
    print(writer.generate_methods_template('lag_rolling'))

    print("\n" + "-" * 80)
    print("COMPARISON METHODS:")
    print("-" * 80)
    print(writer.generate_methods_template('comparison'))

    print("\n" + "=" * 80)
    print("✓ ALL TESTS PASSED")
    print("=" * 80)
