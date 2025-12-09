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