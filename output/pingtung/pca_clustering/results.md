## PCA and Clustering Analysis: Pingtung

### Principal Component Analysis

PCA reduced 175 features to 17 principal components, explaining 90.2% of the total variance. 
The first three components explained 36.9%, 28.7%, and 5.5% of variance, respectively.


### Clustering Analysis

Optimal clustering identified k = 3 clusters based on silhouette score (0.323). Additional validation metrics supported this choice: Calinski-Harabasz index = 1428.1, Davies-Bouldin index = 1.098.


**Cluster characteristics:**

- Cluster 0: n = 1,014.0
  - POS: 0.171 ± 0.145
  - EGG: 5.438 ± 7.322
- Cluster 1: n = 280.0
  - POS: 0.252 ± 0.191
  - EGG: 10.610 ± 13.451
- Cluster 2: n = 1,406.0
  - POS: 0.341 ± 0.205
  - EGG: 12.807 ± 13.367

### Cluster-Outcome Relationships


Kruskal-Wallis test for POS: H = 435.713(2), p < 0.001. 
Significant differences in POS were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).

Kruskal-Wallis test for EGG: H = 311.216(2), p < 0.001. 
Significant differences in EGG were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).


*See Figures: PCA scree plot, t-SNE cluster visualization, and cluster boxplots for POS/EGG*
