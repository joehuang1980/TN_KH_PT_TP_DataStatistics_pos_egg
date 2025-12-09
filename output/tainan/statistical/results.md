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
