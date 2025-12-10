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
