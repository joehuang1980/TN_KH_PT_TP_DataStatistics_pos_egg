## PCA and Clustering Analysis: Tainan

### Principal Component Analysis

PCA reduced 175 features to 15 principal components, explaining 90.5% of the total variance. 
The first three components explained 34.0%, 31.9%, and 6.4% of variance, respectively.


### Clustering Analysis

Optimal clustering identified k = 3 clusters based on silhouette score (0.319). Additional validation metrics supported this choice: Calinski-Harabasz index = 38645.2, Davies-Bouldin index = 1.114.


**Cluster characteristics:**

- Cluster 0: n = 15,818.0
  - POS: 0.358 ± 0.231
  - EGG: 154.794 ± 159.964
- Cluster 1: n = 37,560.0
  - POS: 0.339 ± 0.184
  - EGG: 121.321 ± 108.801
- Cluster 2: n = 26,847.0
  - POS: 0.141 ± 0.141
  - EGG: 48.137 ± 71.052

### Cluster-Outcome Relationships


Kruskal-Wallis test for POS: H = 19993.480(2), p < 0.001. 
Significant differences in POS were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).

Kruskal-Wallis test for EGG: H = 15957.677(2), p < 0.001. 
Significant differences in EGG were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).


*See Figures: PCA scree plot, t-SNE cluster visualization, and cluster boxplots for POS/EGG*
