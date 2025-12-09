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
