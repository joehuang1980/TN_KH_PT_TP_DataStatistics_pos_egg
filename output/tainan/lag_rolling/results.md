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
