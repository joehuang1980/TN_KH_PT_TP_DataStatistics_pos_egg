# Results


## Taipei


### Statistical Analysis

## Statistical Correlation Analysis: Taipei

### Overview

Spearman rank correlations were calculated between 175 environmental and demographic features and outcome variables (POS and EGG) using 3,264 observations from Taipei.


### Correlations with POS

Of 175 features analyzed, 119 showed statistically significant correlations with POS after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- M_temp_lag_rolling1: ρ = 0.705, p < 0.001
- M_temp_lag_rolling2: ρ = 0.700, p < 0.001
- M_temp_lag_rolling3: ρ = 0.691, p < 0.001
- M_temp_lag_rolling4: ρ = 0.684, p < 0.001
- H_temp_lag_rolling1: ρ = 0.675, p < 0.001

**Strongest negative correlations:**

- feed: ρ = -0.208, p < 0.001
- feedelder: ρ = -0.182, p < 0.001
- feedchild: ρ = -0.174, p < 0.001
- density: ρ = -0.136, p < 0.001
- NDVImedian_lag1: ρ = -0.037, p = 0.035

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.495, strongest = M_temp_lag_rolling1 (ρ = 0.705, p < 0.001)
- Rainfall: mean |ρ| = 0.217, strongest = R_lag_rolling7 (ρ = 0.440, p < 0.001)
- Ndvi: mean |ρ| = 0.054, strongest = NDVIsum_11 (ρ = 0.142, p < 0.001)
- Demographic: mean |ρ| = 0.124, strongest = feed (ρ = -0.208, p < 0.001)

*See Figure: Top 30 feature correlations with POS (heatmap)*


### Correlations with EGG

Of 175 features analyzed, 117 showed statistically significant correlations with EGG after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- M_temp_lag_rolling1: ρ = 0.679, p < 0.001
- M_temp_lag_rolling2: ρ = 0.674, p < 0.001
- M_temp_lag_rolling3: ρ = 0.662, p < 0.001
- M_temp_lag_rolling4: ρ = 0.654, p < 0.001
- M_temp_lag_rolling5: ρ = 0.643, p < 0.001

**Strongest negative correlations:**

- feed: ρ = -0.206, p < 0.001
- feedelder: ρ = -0.185, p < 0.001
- feedchild: ρ = -0.166, p < 0.001
- density: ρ = -0.160, p < 0.001
- NDVImedian_lag1: ρ = -0.043, p = 0.014

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.480, strongest = M_temp_lag_rolling1 (ρ = 0.679, p < 0.001)
- Rainfall: mean |ρ| = 0.201, strongest = R_lag_rolling7 (ρ = 0.415, p < 0.001)
- Ndvi: mean |ρ| = 0.057, strongest = NDVIsum_10 (ρ = 0.151, p < 0.001)
- Demographic: mean |ρ| = 0.132, strongest = feed (ρ = -0.206, p < 0.001)

*See Figure: Top 30 feature correlations with EGG (heatmap)*


### PCA and Clustering

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


### Temporal Lag Analysis

## Temporal Lag Analysis: Taipei

### Overview

Temporal lag effects were analyzed for 7 environmental variables across 1-12 week intervals using 3,264 observations.


### Optimal Lag Periods for POS

**Simple lag features:**

- H_temp: 1 weeks (ρ = 0.632)
- M_temp: 1 weeks (ρ = 0.635)
- L_temp: 1 weeks (ρ = 0.599)
- R: 2 weeks (ρ = 0.078)
- NDVImean: 12 weeks (ρ = 0.049)
- NDVImedian: 12 weeks (ρ = 0.050)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.675)
- M_temp: 1 weeks (ρ = 0.705)
- L_temp: 1 weeks (ρ = 0.617)
- R: 7 weeks (ρ = 0.440)
- NDVImean: 12 weeks (ρ = 0.020)
- NDVImedian: 1 weeks (ρ = -0.037)

Mean optimal lag (simple): 4.8 weeks. 
Mean optimal lag (rolling): 3.8 weeks.


*See Figures: Lag correlation heatmaps and line plots for POS*


### Optimal Lag Periods for EGG

**Simple lag features:**

- H_temp: 1 weeks (ρ = 0.602)
- M_temp: 1 weeks (ρ = 0.613)
- L_temp: 1 weeks (ρ = 0.584)
- R: 7 weeks (ρ = 0.077)
- NDVImean: 12 weeks (ρ = 0.032)
- NDVImedian: 1 weeks (ρ = -0.043)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.641)
- M_temp: 1 weeks (ρ = 0.679)
- L_temp: 1 weeks (ρ = 0.600)
- R: 7 weeks (ρ = 0.415)
- NDVImean: 1 weeks (ρ = -0.012)
- NDVImedian: 1 weeks (ρ = -0.043)

Mean optimal lag (simple): 3.8 weeks. 
Mean optimal lag (rolling): 2.0 weeks.


*See Figures: Lag correlation heatmaps and line plots for EGG*


## Kaohsiung


### Statistical Analysis

## Statistical Correlation Analysis: Kaohsiung

### Overview

Spearman rank correlations were calculated between 175 environmental and demographic features and outcome variables (POS and EGG) using 11,535 observations from Kaohsiung.


### Correlations with POS

Of 175 features analyzed, 166 showed statistically significant correlations with POS after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- R_lag_rolling8: ρ = 0.269, p < 0.001
- R_lag_rolling7: ρ = 0.268, p < 0.001
- R_lag_rolling6: ρ = 0.268, p < 0.001
- R_lag_rolling9: ρ = 0.267, p < 0.001
- R_lag_rolling10: ρ = 0.260, p < 0.001

**Strongest negative correlations:**

- density: ρ = -0.059, p < 0.001
- feedelder: ρ = -0.026, p = 0.007
- elderindex: ρ = -0.022, p = 0.019
- feed: ρ = -0.021, p = 0.028

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.204, strongest = M_temp_lag_rolling8 (ρ = 0.258, p < 0.001)
- Rainfall: mean |ρ| = 0.160, strongest = R_lag_rolling8 (ρ = 0.269, p < 0.001)
- Ndvi: mean |ρ| = 0.064, strongest = NDVImean_lag10 (ρ = 0.087, p < 0.001)
- Demographic: mean |ρ| = 0.019, strongest = density (ρ = -0.059, p < 0.001)

*See Figure: Top 30 feature correlations with POS (heatmap)*


### Correlations with EGG

Of 175 features analyzed, 172 showed statistically significant correlations with EGG after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- R_lag_rolling8: ρ = 0.254, p < 0.001
- R_lag_rolling9: ρ = 0.253, p < 0.001
- R_lag_rolling7: ρ = 0.252, p < 0.001
- R_lag_rolling6: ρ = 0.251, p < 0.001
- R_lag_rolling10: ρ = 0.247, p < 0.001

**Strongest negative correlations:**

- density: ρ = -0.048, p < 0.001
- feedelder: ρ = -0.044, p < 0.001
- elderindex: ρ = -0.042, p < 0.001
- feed: ρ = -0.037, p < 0.001

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.182, strongest = H_temp_lag_6 (ρ = 0.233, p < 0.001)
- Rainfall: mean |ρ| = 0.162, strongest = R_lag_rolling8 (ρ = 0.254, p < 0.001)
- Ndvi: mean |ρ| = 0.082, strongest = NDVImean_lag_rollingmean1 (ρ = 0.101, p < 0.001)
- Demographic: mean |ρ| = 0.032, strongest = density (ρ = -0.048, p < 0.001)

*See Figure: Top 30 feature correlations with EGG (heatmap)*


### PCA and Clustering

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


### Temporal Lag Analysis

## Temporal Lag Analysis: Kaohsiung

### Overview

Temporal lag effects were analyzed for 7 environmental variables across 1-12 week intervals using 11,535 observations.


### Optimal Lag Periods for POS

**Simple lag features:**

- H_temp: 1 weeks (ρ = 0.240)
- M_temp: 1 weeks (ρ = 0.228)
- L_temp: 1 weeks (ρ = 0.213)
- R: 3 weeks (ρ = 0.146)
- NDVImean: 10 weeks (ρ = 0.087)
- NDVImedian: 11 weeks (ρ = 0.068)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.224)
- M_temp: 8 weeks (ρ = 0.258)
- L_temp: 1 weeks (ρ = 0.237)
- R: 8 weeks (ρ = 0.269)
- NDVImean: 12 weeks (ρ = 0.082)
- NDVImedian: 1 weeks (ρ = 0.047)

Mean optimal lag (simple): 4.5 weeks. 
Mean optimal lag (rolling): 5.2 weeks.


*See Figures: Lag correlation heatmaps and line plots for POS*


### Optimal Lag Periods for EGG

**Simple lag features:**

- H_temp: 6 weeks (ρ = 0.233)
- M_temp: 6 weeks (ρ = 0.215)
- L_temp: 7 weeks (ρ = 0.197)
- R: 3 weeks (ρ = 0.158)
- NDVImean: 1 weeks (ρ = 0.100)
- NDVImedian: 11 weeks (ρ = 0.075)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.174)
- M_temp: 11 weeks (ρ = 0.227)
- L_temp: 8 weeks (ρ = 0.211)
- R: 8 weeks (ρ = 0.254)
- NDVImean: 1 weeks (ρ = 0.101)
- NDVImedian: 1 weeks (ρ = 0.078)

Mean optimal lag (simple): 5.7 weeks. 
Mean optimal lag (rolling): 5.0 weeks.


*See Figures: Lag correlation heatmaps and line plots for EGG*


## Pingtung


### Statistical Analysis

## Statistical Correlation Analysis: Pingtung

### Overview

Spearman rank correlations were calculated between 175 environmental and demographic features and outcome variables (POS and EGG) using 2,799 observations from Pingtung.


### Correlations with POS

Of 175 features analyzed, 160 showed statistically significant correlations with POS after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- M_temp_lag_rolling1: ρ = 0.503, p < 0.001
- M_temp_lag_rolling2: ρ = 0.500, p < 0.001
- L_temp_lag_rolling1: ρ = 0.493, p < 0.001
- L_temp_lag_rolling2: ρ = 0.489, p < 0.001
- M_temp_lag_1: ρ = 0.487, p < 0.001

**Strongest negative correlations:**

- NDVImedian_lag_rollingmedian2: ρ = -0.156, p < 0.001
- NDVImedian_lag1: ρ = -0.156, p < 0.001
- NDVImedian_lag_rollingmedian3: ρ = -0.153, p < 0.001
- NDVImedian_lag_rollingmedian1: ρ = -0.152, p < 0.001
- NDVImedian_lag2: ρ = -0.150, p < 0.001

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.358, strongest = M_temp_lag_rolling1 (ρ = 0.503, p < 0.001)
- Rainfall: mean |ρ| = 0.199, strongest = R_lag_rolling8 (ρ = 0.403, p < 0.001)
- Ndvi: mean |ρ| = 0.118, strongest = NDVImedian_lag_rollingmedian2 (ρ = -0.156, p < 0.001)
- Demographic: mean |ρ| = 0.099, strongest = density (ρ = 0.166, p < 0.001)

*See Figure: Top 30 feature correlations with POS (heatmap)*


### Correlations with EGG

Of 175 features analyzed, 152 showed statistically significant correlations with EGG after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- M_temp_lag_rolling1: ρ = 0.463, p < 0.001
- M_temp_lag_rolling2: ρ = 0.460, p < 0.001
- L_temp_lag_rolling1: ρ = 0.455, p < 0.001
- L_temp_lag_1: ρ = 0.449, p < 0.001
- L_temp_lag_rolling2: ρ = 0.448, p < 0.001

**Strongest negative correlations:**

- feed: ρ = -0.149, p < 0.001
- feedelder: ρ = -0.147, p < 0.001
- NDVImedian_lag_rollingmedian2: ρ = -0.141, p < 0.001
- NDVImedian_lag_rollingmedian1: ρ = -0.140, p < 0.001
- NDVImedian_lag1: ρ = -0.140, p < 0.001

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.306, strongest = M_temp_lag_rolling1 (ρ = 0.463, p < 0.001)
- Rainfall: mean |ρ| = 0.174, strongest = R_lag_rolling8 (ρ = 0.352, p < 0.001)
- Ndvi: mean |ρ| = 0.104, strongest = NDVImedian_lag_rollingmedian2 (ρ = -0.141, p < 0.001)
- Demographic: mean |ρ| = 0.112, strongest = density (ρ = 0.168, p < 0.001)

*See Figure: Top 30 feature correlations with EGG (heatmap)*


### PCA and Clustering

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


### Temporal Lag Analysis

## Temporal Lag Analysis: Pingtung

### Overview

Temporal lag effects were analyzed for 7 environmental variables across 1-12 week intervals using 2,799 observations.


### Optimal Lag Periods for POS

**Simple lag features:**

- H_temp: 1 weeks (ρ = 0.384)
- M_temp: 1 weeks (ρ = 0.487)
- L_temp: 1 weeks (ρ = 0.486)
- R: 3 weeks (ρ = 0.103)
- NDVImean: 2 weeks (ρ = -0.099)
- NDVImedian: 1 weeks (ρ = -0.156)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.393)
- M_temp: 1 weeks (ρ = 0.503)
- L_temp: 1 weeks (ρ = 0.493)
- R: 8 weeks (ρ = 0.403)
- NDVImean: 7 weeks (ρ = -0.103)
- NDVImedian: 2 weeks (ρ = -0.156)

Mean optimal lag (simple): 1.5 weeks. 
Mean optimal lag (rolling): 3.3 weeks.


*See Figures: Lag correlation heatmaps and line plots for POS*


### Optimal Lag Periods for EGG

**Simple lag features:**

- H_temp: 1 weeks (ρ = 0.339)
- M_temp: 1 weeks (ρ = 0.444)
- L_temp: 1 weeks (ρ = 0.449)
- R: 3 weeks (ρ = 0.075)
- NDVImean: 5 weeks (ρ = -0.087)
- NDVImedian: 1 weeks (ρ = -0.140)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.357)
- M_temp: 1 weeks (ρ = 0.463)
- L_temp: 1 weeks (ρ = 0.455)
- R: 8 weeks (ρ = 0.352)
- NDVImean: 8 weeks (ρ = -0.092)
- NDVImedian: 2 weeks (ρ = -0.141)

Mean optimal lag (simple): 2.0 weeks. 
Mean optimal lag (rolling): 3.5 weeks.


*See Figures: Lag correlation heatmaps and line plots for EGG*


## Tainan


### Statistical Analysis

## Statistical Correlation Analysis: Tainan

### Overview

Spearman rank correlations were calculated between 175 environmental and demographic features and outcome variables (POS and EGG) using 82,805 observations from Tainan.


### Correlations with POS

Of 175 features analyzed, 175 showed statistically significant correlations with POS after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- M_temp_lag_rolling1: ρ = 0.617, p < 0.001
- M_temp_lag_rolling2: ρ = 0.610, p < 0.001
- M_temp_lag_rolling3: ρ = 0.601, p < 0.001
- M_temp_lag_rolling4: ρ = 0.597, p < 0.001
- M_temp_lag_rolling5: ρ = 0.592, p < 0.001

**Strongest negative correlations:**

- density: ρ = -0.136, p < 0.001
- feed: ρ = -0.083, p < 0.001
- feedelder: ρ = -0.065, p < 0.001
- elderindex: ρ = -0.028, p < 0.001
- feedchild: ρ = -0.013, p < 0.001

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.465, strongest = M_temp_lag_rolling1 (ρ = 0.617, p < 0.001)
- Rainfall: mean |ρ| = 0.267, strongest = R_lag_rolling10 (ρ = 0.496, p < 0.001)
- Ndvi: mean |ρ| = 0.135, strongest = NDVImean_lag_rollingmean12 (ρ = 0.146, p < 0.001)
- Demographic: mean |ρ| = 0.078, strongest = density (ρ = -0.136, p < 0.001)

*See Figure: Top 30 feature correlations with POS (heatmap)*


### Correlations with EGG

Of 175 features analyzed, 174 showed statistically significant correlations with EGG after Bonferroni correction (α = 0.000286).


**Strongest positive correlations:**

- M_temp_lag_rolling1: ρ = 0.547, p < 0.001
- M_temp_lag_rolling2: ρ = 0.536, p < 0.001
- M_temp_lag_rolling3: ρ = 0.525, p < 0.001
- M_temp_lag_rolling4: ρ = 0.519, p < 0.001
- H_temp_lag_rolling1: ρ = 0.515, p < 0.001

**Strongest negative correlations:**

- density: ρ = -0.165, p < 0.001
- feed: ρ = -0.087, p < 0.001
- feedelder: ρ = -0.075, p < 0.001
- elderindex: ρ = -0.045, p < 0.001

**Correlations by feature group:**

- Temperature: mean |ρ| = 0.402, strongest = M_temp_lag_rolling1 (ρ = 0.547, p < 0.001)
- Rainfall: mean |ρ| = 0.225, strongest = R_lag_rolling10 (ρ = 0.435, p < 0.001)
- Ndvi: mean |ρ| = 0.167, strongest = NDVImean_lag_rollingmean12 (ρ = 0.179, p < 0.001)
- Demographic: mean |ρ| = 0.091, strongest = density (ρ = -0.165, p < 0.001)

*See Figure: Top 30 feature correlations with EGG (heatmap)*


### PCA and Clustering

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


### Temporal Lag Analysis

## Temporal Lag Analysis: Tainan

### Overview

Temporal lag effects were analyzed for 7 environmental variables across 1-12 week intervals using 82,805 observations.


### Optimal Lag Periods for POS

**Simple lag features:**

- H_temp: 1 weeks (ρ = 0.559)
- M_temp: 1 weeks (ρ = 0.579)
- L_temp: 1 weeks (ρ = 0.553)
- R: 3 weeks (ρ = 0.154)
- NDVImean: 1 weeks (ρ = 0.143)
- NDVImedian: 12 weeks (ρ = 0.135)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.572)
- M_temp: 1 weeks (ρ = 0.617)
- L_temp: 1 weeks (ρ = 0.585)
- R: 10 weeks (ρ = 0.496)
- NDVImean: 12 weeks (ρ = 0.146)
- NDVImedian: 12 weeks (ρ = 0.125)

Mean optimal lag (simple): 3.2 weeks. 
Mean optimal lag (rolling): 6.2 weeks.


*See Figures: Lag correlation heatmaps and line plots for POS*


### Optimal Lag Periods for EGG

**Simple lag features:**

- H_temp: 1 weeks (ρ = 0.500)
- M_temp: 1 weeks (ρ = 0.511)
- L_temp: 1 weeks (ρ = 0.483)
- R: 3 weeks (ρ = 0.130)
- NDVImean: 1 weeks (ρ = 0.174)
- NDVImedian: 12 weeks (ρ = 0.170)

**Rolling window features:**

- H_temp: 1 weeks (ρ = 0.515)
- M_temp: 1 weeks (ρ = 0.547)
- L_temp: 1 weeks (ρ = 0.513)
- R: 10 weeks (ρ = 0.435)
- NDVImean: 12 weeks (ρ = 0.179)
- NDVImedian: 12 weeks (ρ = 0.162)

Mean optimal lag (simple): 3.2 weeks. 
Mean optimal lag (rolling): 6.2 weeks.


*See Figures: Lag correlation heatmaps and line plots for EGG*


## Cross-City Comparison

## Cross-City Comparison

### Sample Characteristics


| city      |   n_samples |   n_features |   pos_n_significant |   egg_n_significant |
|:----------|------------:|-------------:|--------------------:|--------------------:|
| Taipei    |        3264 |          175 |                 119 |                 117 |
| Kaohsiung |       11535 |          175 |                 166 |                 172 |
| Pingtung  |        2799 |          175 |                 160 |                 152 |
| Tainan    |       82805 |          175 |                 175 |                 174 |


### Universal Predictors


**POS**: 0 universal predictors found across all cities (|ρ| > 0.3, p < 0.001):

**EGG**: 0 universal predictors found across all cities (|ρ| > 0.3, p < 0.001):

### Clustering Patterns


| city      |   n_components |   variance_explained |   optimal_k |   silhouette |   pos_kruskal_p |   egg_kruskal_p |
|:----------|---------------:|---------------------:|------------:|-------------:|----------------:|----------------:|
| Taipei    |             16 |             0.906031 |           2 |     0.342263 |    0.0059106    |    0.00925701   |
| Kaohsiung |             17 |             0.905914 |           4 |     0.301641 |    3.96065e-110 |    3.53903e-102 |
| Pingtung  |             17 |             0.901746 |           3 |     0.322704 |    2.43338e-95  |    2.63183e-68  |
| Tainan    |             15 |             0.905274 |           3 |     0.318642 |    0            |    0            |


### Temporal Lag Patterns


**POS**: Comparison of optimal lag periods across cities (see supplementary tables)

**EGG**: Comparison of optimal lag periods across cities (see supplementary tables)