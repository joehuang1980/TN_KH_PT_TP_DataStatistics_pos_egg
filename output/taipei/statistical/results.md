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
