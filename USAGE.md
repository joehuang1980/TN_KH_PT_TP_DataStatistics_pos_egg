# Multi-City Statistical Analysis System - Usage Guide

## Overview

This system performs comprehensive statistical analysis on mosquito surveillance data across 4 cities (Taipei, Kaohsiung, Pingtung, Tainan), including:

- **Statistical correlation analysis** (Spearman correlations with Bonferroni correction)
- **PCA and clustering** (auto-optimized k using Silhouette scores)
- **Temporal lag analysis** (1-12 week lag/rolling features)
- **Cross-city comparison** (universal vs city-specific predictors)
- **Academic paper generation** (Methods and Results sections in English)

## Quick Start

### Run Complete Analysis on All Cities

```bash
cd /home/joe/Documents/TN_KH_PT_TP_DataStatistics_pos_egg
python src/run_full_analysis.py
```

This will:
1. Load data for all 4 cities
2. Run 3 analyses per city (statistical, PCA/clustering, lag/rolling)
3. Perform cross-city comparison
4. Compile academic paper sections
5. Save ~140 output files (33 per city + comparison + paper)

**Expected runtime**: ~15-30 minutes for all cities

### Test on Single City (Taipei)

```bash
python src/test_pipeline.py
```

**Expected runtime**: ~3-5 minutes

## Output Structure

After running the full analysis:

```
output/
├── taipei/
│   ├── statistical/
│   │   ├── correlations_pos.csv                 # All feature-POS correlations
│   │   ├── correlations_egg.csv                 # All feature-EGG correlations
│   │   ├── top_features_pos_positive.csv        # Top 20 positive correlations
│   │   ├── top_features_pos_negative.csv        # Top 20 negative correlations
│   │   ├── correlation_heatmap_pos.png          # Visualization (300 DPI)
│   │   ├── correlation_heatmap_egg.png
│   │   ├── methods.md                           # Academic Methods section
│   │   └── results.md                           # Academic Results section
│   ├── pca_clustering/
│   │   ├── pca_components.csv                   # PCA explained variance
│   │   ├── clustering_metrics.csv               # Metrics for k=2-10
│   │   ├── cluster_characteristics.csv          # Cluster statistics
│   │   ├── optimal_clusters_data.csv            # Data with cluster labels
│   │   ├── pca_scree_plot.png                   # Variance explained plot
│   │   ├── tsne_visualization.png               # 2D cluster visualization
│   │   ├── cluster_boxplots_pos_egg.png         # Outcome by cluster
│   │   ├── methods.md
│   │   └── results.md
│   └── lag_rolling/
│       ├── lag_correlations_pos.csv             # Simple lag correlations
│       ├── rolling_correlations_pos.csv         # Rolling window correlations
│       ├── optimal_lags_summary_pos.csv         # Best lag per variable
│       ├── lag_heatmap_pos.png                  # Correlation heatmap
│       ├── rolling_heatmap_pos.png
│       ├── lag_line_plots_pos.png               # Temporal patterns
│       ├── [same for EGG]
│       ├── methods.md
│       └── results.md
├── kaohsiung/  [same structure]
├── pingtung/   [same structure]
├── tainan/     [same structure]
├── comparison/
│   ├── descriptive_stats.csv                    # Cross-city summary
│   ├── universal_predictors_pos.csv             # Features significant in ALL cities
│   ├── universal_predictors_egg.csv
│   ├── clustering_comparison.csv                # Optimal k by city
│   ├── lag_comparison_pos.csv                   # Optimal lags by city
│   ├── lag_comparison_egg.csv
│   ├── methods.md
│   └── results.md
└── compiled_paper/
    ├── full_methods.md                          # Complete Methods section
    └── full_results.md                          # Complete Results section
```

## Key Results

### Statistical Analysis
- **119 significant features** for POS in Taipei (Bonferroni α = 0.000286)
- **Top predictor**: M_temp_lag_rolling1 (ρ = 0.705 with POS)
- **Feature groups**: Temperature (72), Rainfall (24), NDVI (72), Demographic (7)

### PCA & Clustering
- **16 PCA components** explain 90.6% variance in Taipei
- **Optimal k = 2** clusters (Silhouette = 0.342)
- **Significant cluster-outcome relationships** (Kruskal-Wallis p < 0.01)

### Temporal Lag Analysis
- **Temperature**: Optimal lag at 1 week (ρ ~ 0.67-0.71)
- **Rainfall**: Optimal lag at 7 weeks with rolling windows (ρ ~ 0.44)
- **NDVI**: Variable patterns across 12-week period

## Configuration

All parameters are centralized in `src/config/analysis_config.py`:

```python
# Key parameters
TOTAL_FEATURES = 175
BONFERRONI_CORRECTED_ALPHA = 0.000286  # 0.05 / 175
PCA_VARIANCE_TARGET = 0.90             # 90% variance
CLUSTERING_K_RANGE = range(2, 11)      # Test k=2-10
RANDOM_SEED = 42                       # Reproducibility
FIGURE_DPI = 300                       # Publication quality
```

## Running Individual Analyses

### Statistical Analysis Only

```python
from src.core.data_loader import DataLoader
from src.analyzers.statistical_analyzer import StatisticalAnalyzer

loader = DataLoader()
df, meta = loader.load_city_data('taipei')

analyzer = StatisticalAnalyzer()
results = analyzer.analyze(df, city_key='taipei')
analyzer.save_outputs('output/taipei/statistical')
```

### PCA/Clustering Only

```python
from src.analyzers.pca_clustering_analyzer import PCAClusteringAnalyzer

analyzer = PCAClusteringAnalyzer()
results = analyzer.analyze(df, city_key='taipei')
analyzer.save_outputs('output/taipei/pca_clustering')
```

### Lag/Rolling Analysis Only

```python
from src.analyzers.lag_rolling_analyzer import LagRollingAnalyzer

analyzer = LagRollingAnalyzer()
results = analyzer.analyze(df, city_key='taipei')
analyzer.save_outputs('output/taipei/lag_rolling')
```

## Academic Paper Output

The compiled academic paper sections are ready for journal submission:

### Methods Section (`compiled_paper/full_methods.md`)
- Study design and data collection
- Statistical correlation analysis (Spearman, Bonferroni)
- PCA and clustering methodology
- Temporal lag analysis approach
- Cross-city comparison methods

### Results Section (`compiled_paper/full_results.md`)
- City-specific results (4 cities × 3 analyses)
- Cross-city comparison findings
- Universal predictor identification
- Statistical test results with p-values

## System Architecture

```
src/
├── config/
│   └── analysis_config.py          # Centralized configuration
├── core/
│   ├── data_loader.py              # Data loading utilities
│   ├── base_analyzer.py            # Abstract base classes
│   └── academic_writer.py          # Academic text generation
├── analyzers/
│   ├── statistical_analyzer.py     # Correlation analysis
│   ├── pca_clustering_analyzer.py  # PCA + clustering
│   ├── lag_rolling_analyzer.py     # Temporal lag analysis
│   └── comparison_analyzer.py      # Cross-city comparison
├── run_full_analysis.py            # Main pipeline
└── test_pipeline.py                # Single-city test
```

## Requirements

The system uses:
- pandas, numpy - Data manipulation
- scipy - Statistical tests
- scikit-learn - PCA, clustering, scaling
- matplotlib, seaborn - Visualization
- scikit-posthocs - Dunn's post-hoc tests

## Reproducibility

All analyses use `random_state=42` for:
- PCA initialization
- K-means clustering (100 initializations)
- t-SNE dimensionality reduction

## Troubleshooting

### Memory Issues
If analysis fails due to memory, reduce `TSNE_SAMPLE_SIZE` in config (default: 5000)

### Missing Data
The system handles missing values automatically:
- Drops rows with missing POS/EGG values
- Uses pairwise deletion for correlations
- Handles NaN in lag feature detection

### Custom Cities
To add a new city, edit `analysis_config.py`:
```python
CITIES['new_city'] = {
    'name_zh': '新城市',
    'name_en': 'New City',
    'abbr': 'NC',
    'path': '/path/to/data.csv',
    'color': '#HEXCOLOR'
}
```

## Performance

- **Taipei (3,264 samples)**: ~3-5 minutes
- **All 4 cities**: ~15-30 minutes (sequential processing)
- **Outputs**: ~140 files, ~50 MB total

## Support

For issues or questions:
1. Check CLAUDE.md for critical rules
2. Review this USAGE.md
3. Test on single city first (`test_pipeline.py`)
4. Check configuration in `analysis_config.py`
