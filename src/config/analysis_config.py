"""
Configuration file for multi-city statistical analysis.

This module contains all configuration parameters for analyzing mosquito surveillance
data across four cities (Taipei, Kaohsiung, Pingtung, Tainan).
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ==============================================================================
# CITY CONFIGURATIONS
# ==============================================================================

CITIES = {
    'taipei': {
        'name_zh': '台北',
        'name_en': 'Taipei',
        'abbr': 'TP',
        'path': '/home/joe/Documents/2025_TPE_model/DATA/2020to2024allfeatures_labels_台北_pos_egg.csv',
        'color': '#E74C3C'  # Red
    },
    'kaohsiung': {
        'name_zh': '高雄',
        'name_en': 'Kaohsiung',
        'abbr': 'KH',
        'path': '/home/joe/Documents/2024_semi_supervised_learning/Grid_Village/2019to2024allfeatures_labels_高雄_pos_egg.csv',
        'color': '#3498DB'  # Blue
    },
    'pingtung': {
        'name_zh': '屏東',
        'name_en': 'Pingtung',
        'abbr': 'PT',
        'path': '/home/joe/Documents/2024_semi_supervised_learning/Grid_Village/2019to2024allfeatures_labels_屏東_pos_egg.csv',
        'color': '#2ECC71'  # Green
    },
    'tainan': {
        'name_zh': '台南',
        'name_en': 'Tainan',
        'abbr': 'TN',
        'path': '/home/joe/Documents/2023_semi_supervised_learning/Data/2019to2024allfeatures_labels_recent_pos_egg_data.csv',
        'color': '#F39C12'  # Orange
    }
}

# City order for consistent processing and visualization
CITY_ORDER = ['taipei', 'kaohsiung', 'pingtung', 'tainan']

# ==============================================================================
# FEATURE GROUPS
# ==============================================================================

# Features to ignore (not used for modeling)
IGNORE_COLUMNS = ['date', 'townvill', '縣市']

# Target variables
TARGETS = ['pos', 'egg']

# Feature groups for analysis
FEATURE_GROUPS = {
    'temperature': {
        'variables': ['H_temp', 'M_temp', 'L_temp'],
        'description': 'High, mean, and low temperature',
        'n_features': 72  # 3 variables × (12 lag + 12 rolling)
    },
    'rainfall': {
        'variables': ['R'],
        'description': 'Precipitation',
        'n_features': 24  # 1 variable × (12 lag + 12 rolling)
    },
    'ndvi': {
        'variables': ['NDVImean', 'NDVImedian', 'NDVIsum'],
        'description': 'Normalized Difference Vegetation Index',
        'n_features': 72  # 3 variables × (12 lag + 12 rolling)
    },
    'demographic': {
        'variables': ['sex', 'home', 'density', 'feed', 'feedchild', 'feedelder', 'elderindex'],
        'description': 'Sociodemographic characteristics',
        'n_features': 7  # Static features (no lag/rolling)
    }
}

# Total number of features for modeling
TOTAL_FEATURES = 175  # 72 temp + 24 rainfall + 72 NDVI + 7 demographic

# ==============================================================================
# LAG ANALYSIS PARAMETERS
# ==============================================================================

# Lag weeks range (1-12 weeks)
LAG_RANGE = list(range(1, 13))

# Lag feature patterns
LAG_PATTERNS = {
    'simple': '{variable}_lag_{week}',     # e.g., H_temp_lag_1
    'rolling': '{variable}_lag_rolling{week}'  # e.g., H_temp_lag_rolling1
}

# Variables with lag features
LAG_VARIABLES = ['H_temp', 'M_temp', 'L_temp', 'R', 'NDVImean', 'NDVImedian', 'NDVIsum']

# ==============================================================================
# STATISTICAL ANALYSIS PARAMETERS
# ==============================================================================

# Correlation method
CORRELATION_METHOD = 'spearman'  # Non-parametric, suitable for non-normal distributions

# Multiple comparison correction
BONFERRONI_ALPHA = 0.05
BONFERRONI_CORRECTED_ALPHA = BONFERRONI_ALPHA / TOTAL_FEATURES  # 0.000286

# Number of top correlations to report
N_TOP_CORRELATIONS = 20

# Number of features to show in heatmaps
N_HEATMAP_FEATURES = 30

# ==============================================================================
# PCA PARAMETERS
# ==============================================================================

# PCA variance retention thresholds
PCA_VARIANCE_MIN = 0.85  # Minimum 85% variance
PCA_VARIANCE_TARGET = 0.90  # Target 90% variance
PCA_VARIANCE_MAX = 0.95  # Maximum 95% variance

# Number of components to show in scree plot
PCA_SCREE_COMPONENTS = 50

# ==============================================================================
# CLUSTERING PARAMETERS
# ==============================================================================

# K-means cluster number range for testing
CLUSTERING_K_MIN = 2
CLUSTERING_K_MAX = 10
CLUSTERING_K_RANGE = list(range(CLUSTERING_K_MIN, CLUSTERING_K_MAX + 1))

# K-means parameters
KMEANS_N_INIT = 100  # Number of initializations (for stability)
KMEANS_MAX_ITER = 300  # Maximum iterations

# Clustering validation metrics
CLUSTERING_METRICS = ['silhouette', 'calinski_harabasz', 'davies_bouldin']

# t-SNE parameters for visualization
TSNE_PERPLEXITY = 30
TSNE_MAX_ITER = 1000
TSNE_SAMPLE_SIZE = 5000  # Maximum samples for t-SNE (computational efficiency)

# ==============================================================================
# CROSS-CITY COMPARISON PARAMETERS
# ==============================================================================

# Universal predictor thresholds
UNIVERSAL_PREDICTOR_RHO_THRESHOLD = 0.3  # |ρ| > 0.3
UNIVERSAL_PREDICTOR_P_THRESHOLD = 0.001  # p < 0.001

# ==============================================================================
# VISUALIZATION PARAMETERS
# ==============================================================================

# Figure settings
FIGURE_DPI = 300  # Publication quality
FIGURE_FORMAT = 'png'  # Primary format (can also export to PDF)

# Color schemes
COLORMAP_DIVERGING = 'RdBu_r'  # For correlation heatmaps (red-blue)
COLORMAP_SEQUENTIAL = 'viridis'  # For other heatmaps
COLORMAP_CATEGORICAL = 'tab10'  # For categorical data (clusters, cities)

# Font settings (English labels as per user preference)
FONT_SIZE_TITLE = 14
FONT_SIZE_LABEL = 12
FONT_SIZE_TICK = 10
FONT_SIZE_LEGEND = 10

# ==============================================================================
# OUTPUT PATHS
# ==============================================================================

# Base output directory
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# City-specific output structure
CITY_OUTPUT_STRUCTURE = {
    'statistical': 'statistical',
    'pca_clustering': 'pca_clustering',
    'lag_rolling': 'lag_rolling',
    'summary': 'summary'
}

# Comparison output directory
COMPARISON_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'comparison')

# Compiled paper output directory
PAPER_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'compiled_paper')

# ==============================================================================
# REPRODUCIBILITY PARAMETERS
# ==============================================================================

# Random seed for all stochastic processes
RANDOM_SEED = 42

# ==============================================================================
# ACADEMIC PAPER PARAMETERS
# ==============================================================================

# Language for academic paper sections
PAPER_LANGUAGE = 'english'  # As per user preference

# Paper section types
PAPER_SECTIONS = ['methods', 'results']

# Statistical reporting format
STAT_REPORTING = {
    'decimal_places': 3,
    'p_value_threshold': 0.001,  # Report p < 0.001 instead of exact value
    'correlation_threshold': 0.1  # Minimum |ρ| to report as meaningful
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_city_output_dir(city_key, analysis_type=None):
    """
    Get output directory path for a specific city and analysis type.

    Parameters
    ----------
    city_key : str
        City key ('taipei', 'kaohsiung', 'pingtung', 'tainan')
    analysis_type : str, optional
        Analysis type ('statistical', 'pca_clustering', 'lag_rolling', 'summary')
        If None, returns the city's base output directory

    Returns
    -------
    str
        Output directory path
    """
    city_name_en = CITIES[city_key]['name_en'].lower()
    if analysis_type is None:
        return os.path.join(OUTPUT_DIR, city_name_en)
    else:
        return os.path.join(OUTPUT_DIR, city_name_en, CITY_OUTPUT_STRUCTURE[analysis_type])


def get_feature_columns_pattern():
    """
    Get list of all feature column patterns.

    Returns
    -------
    list
        List of feature column patterns for dynamic matching
    """
    patterns = []

    # Temperature lag features
    for var in ['H_temp', 'M_temp', 'L_temp']:
        for week in LAG_RANGE:
            patterns.append(f'{var}_lag_{week}')
            patterns.append(f'{var}_lag_rolling{week}')

    # Rainfall lag features
    for week in LAG_RANGE:
        patterns.append(f'R_lag_{week}')
        patterns.append(f'R_lag_rolling{week}')

    # NDVI lag features
    for var in ['NDVImean', 'NDVImedian', 'NDVIsum']:
        for week in LAG_RANGE:
            patterns.append(f'{var}_lag{week}')  # Note: NDVImean uses 'lag1' not 'lag_1'
            patterns.append(f'{var}_lag_rollingmean{week}' if var == 'NDVImean'
                          else f'{var}_lag_rollingmedian{week}' if var == 'NDVImedian'
                          else f'{var}_lag_rollingsum{week}')

    # Demographic features
    patterns.extend(FEATURE_GROUPS['demographic']['variables'])

    return patterns


def validate_config():
    """
    Validate configuration parameters.

    Raises
    ------
    ValueError
        If configuration is invalid
    """
    # Check city paths exist
    for city_key, city_info in CITIES.items():
        if not os.path.exists(city_info['path']):
            raise ValueError(f"Data file not found for {city_info['name_en']}: {city_info['path']}")

    # Check parameter consistency
    if BONFERRONI_CORRECTED_ALPHA <= 0:
        raise ValueError("Bonferroni corrected alpha must be positive")

    if not (0 < PCA_VARIANCE_MIN <= PCA_VARIANCE_TARGET <= PCA_VARIANCE_MAX <= 1):
        raise ValueError("PCA variance thresholds must be between 0 and 1 in ascending order")

    if CLUSTERING_K_MIN < 2:
        raise ValueError("Minimum cluster number must be at least 2")

    print("✓ Configuration validated successfully")


# ==============================================================================
# MODULE INITIALIZATION
# ==============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("CONFIGURATION SUMMARY")
    print("=" * 80)

    print(f"\nCities: {len(CITIES)}")
    for city_key in CITY_ORDER:
        city = CITIES[city_key]
        print(f"  - {city['name_en']} ({city['abbr']}): {city['name_zh']}")

    print(f"\nFeatures: {TOTAL_FEATURES} total")
    for group_name, group_info in FEATURE_GROUPS.items():
        print(f"  - {group_name.capitalize()}: {group_info['n_features']} features")

    print(f"\nTargets: {', '.join(TARGETS)}")

    print(f"\nAnalysis parameters:")
    print(f"  - Correlation method: {CORRELATION_METHOD}")
    print(f"  - Bonferroni α: {BONFERRONI_CORRECTED_ALPHA:.6f}")
    print(f"  - PCA variance target: {PCA_VARIANCE_TARGET*100:.0f}%")
    print(f"  - Clustering k range: {CLUSTERING_K_MIN}-{CLUSTERING_K_MAX}")
    print(f"  - Random seed: {RANDOM_SEED}")

    print(f"\nOutput directory: {OUTPUT_DIR}")

    print("\n" + "=" * 80)
    print("Validating configuration...")
    print("=" * 80)

    try:
        validate_config()
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
