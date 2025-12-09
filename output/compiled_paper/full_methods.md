# Methods

## Study Design and Data Collection

This multi-city surveillance study analyzed ovitrap-based mosquito monitoring data from four cities in Taiwan: Taipei, Kaohsiung, Pingtung, and Tainan. Data included 175 environmental and demographic features and two outcome variables: ovitrap positive rate (POS) and average egg count (EGG).


## Statistical Correlation Analysis

### Statistical Correlation Analysis

Spearman rank correlation coefficients (ρ) were calculated between 175
environmental and demographic features and two outcome variables: ovitrap positive
rate (POS) and average egg count (EGG), for each city independently. Spearman's
method was chosen due to its robustness to non-normal distributions and outliers,
which are common in ecological surveillance data.

Statistical significance was assessed using two-tailed tests with Bonferroni
correction for multiple comparisons (α = 0.000286, derived from family-wise
error rate of 0.05 divided by 175 tests). Features were ranked by
absolute correlation strength, and the top 20 positive and negative correlations
were identified for each outcome variable.

Features were categorized into four groups for interpretation: (1) temperature
variables (high, mean, and low temperature with temporal lags), (2) rainfall
variables (precipitation with temporal lags), (3) vegetation indices (NDVI mean,
median, and sum with temporal lags), and (4) demographic variables (population
characteristics).

## Dimensionality Reduction and Clustering

### Dimensionality Reduction and Clustering

Principal Component Analysis (PCA) was applied to standardized feature matrices
(z-score normalization using StandardScaler) to reduce dimensionality while
retaining ≥90% of cumulative variance. The number of
components was determined individually for each city based on the scree plot
and explained variance ratios.

K-means clustering was performed on PCA-reduced data to identify distinct
environmental-demographic profiles. The optimal number of clusters (k) was
determined using three complementary validation metrics: (1) Silhouette score
(range: -1 to 1, higher indicates better-defined clusters), (2) Calinski-Harabasz
index (higher indicates better separation), and (3) Davies-Bouldin index (lower
indicates better separation). K-means was tested for k = 2 to 10 with
100 random initializations to ensure stability.

Associations between cluster membership and outcome variables (POS and EGG) were
assessed using Kruskal-Wallis H-tests, a non-parametric alternative to ANOVA
suitable for non-normal distributions. When significant differences were detected
(p < 0.05), Dunn's post-hoc tests with Bonferroni correction were performed for
pairwise cluster comparisons.

t-distributed Stochastic Neighbor Embedding (t-SNE) was used to visualize
high-dimensional clusters in two dimensions, with perplexity = 30
and 1000 iterations.

## Temporal Lag Analysis

### Temporal Lag Effect Analysis

To assess temporal relationships between environmental variables and mosquito
activity, we analyzed correlation patterns across 1-12 week lag
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

## Cross-City Comparison

### Cross-City Comparison Analysis

Statistical comparisons across 4 cities were performed to identify
universal versus city-specific predictors of mosquito activity. Outcome variable
distributions (POS and EGG) were compared using Kruskal-Wallis H-tests, followed
by Dunn's post-hoc tests with Bonferroni correction for pairwise comparisons.

Feature importance rankings were compared across cities by calculating Spearman
correlations between each city's ranked feature lists. Universal predictors were
defined as features meeting two criteria in all cities: (1) |ρ| > 0.3
and (2) p < 0.001. City-specific predictors
were defined as features meeting these criteria in only one or two cities.

Clustering patterns (optimal k and cluster-outcome relationships) and temporal
lag effects (optimal lag periods) were also compared across cities to identify
consistent versus location-specific patterns.