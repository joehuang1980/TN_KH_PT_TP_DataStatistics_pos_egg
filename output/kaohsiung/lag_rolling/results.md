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
