## PCA and Clustering Analysis: Kaohsiung

### Principal Component Analysis

PCA reduced 175 features to 17 principal components, explaining 90.6% of the total variance. 
The first three components explained 33.3%, 29.3%, and 7.4% of variance, respectively.


### Clustering Analysis

Optimal clustering identified k = 4 clusters based on silhouette score (0.302). Additional validation metrics supported this choice: Calinski-Harabasz index = 3962.6, Davies-Bouldin index = 1.242.


**Cluster characteristics:**

- Cluster 0: n = 5,064.0
  - POS: 0.414 ± 0.346
  - EGG: 15.112 ± 25.839
- Cluster 1: n = 4,412.0
  - POS: 0.274 ± 0.322
  - EGG: 9.519 ± 22.619
- Cluster 2: n = 1,225.0
  - POS: 0.443 ± 0.383
  - EGG: 26.363 ± 55.921
- Cluster 3: n = 369.0
  - POS: 0.460 ± 0.388
  - EGG: 34.854 ± 65.871

### Cluster-Outcome Relationships


Kruskal-Wallis test for POS: H = 509.602(3), p < 0.001. 
Significant differences in POS were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).

Kruskal-Wallis test for EGG: H = 472.911(3), p < 0.001. 
Significant differences in EGG were observed across clusters. Dunn's post-hoc tests revealed specific pairwise differences (see supplementary tables).


*See Figures: PCA scree plot, t-SNE cluster visualization, and cluster boxplots for POS/EGG*
