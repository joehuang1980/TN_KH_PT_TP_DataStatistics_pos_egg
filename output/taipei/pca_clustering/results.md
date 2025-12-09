## PCA and Clustering Analysis: Taipei

### Principal Component Analysis

PCA reduced 175 features to 16 principal components, explaining 90.6% of the total variance. 
The first three components explained 36.5%, 28.9%, and 6.0% of variance, respectively.


### Clustering Analysis

Optimal clustering identified k = 2 clusters based on silhouette score (0.342). Additional validation metrics supported this choice: Calinski-Harabasz index = 1330.0, Davies-Bouldin index = 1.286.


**Cluster characteristics:**

- Cluster 0: n = 681.0
  - POS: 0.386 ± 0.285
  - EGG: 17.779 ± 20.314
- Cluster 1: n = 2,583.0
  - POS: 0.424 ± 0.302
  - EGG: 20.899 ± 24.005

### Cluster-Outcome Relationships


Kruskal-Wallis test for POS: H = 7.577(1), p = 0.006. 
Significant differences in POS were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).

Kruskal-Wallis test for EGG: H = 6.773(1), p = 0.009. 
Significant differences in EGG were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).


*See Figures: PCA scree plot, t-SNE cluster visualization, and cluster boxplots for POS/EGG*
