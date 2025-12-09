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
