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
