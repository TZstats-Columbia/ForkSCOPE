# 2025-11-29T19-18-15+0000  (ai)

- code: 246 lines, 59% exon (146 lines in 17 decisions)
- intron: print 66, comment 22, import 7, config 5
- prose: 243 lines, 127 claims (71 action, 56 result)
- links: 70 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 13
- result_claims_deferred: 56

## All decisions

- `23-25` [high] **linked x3** — load the raw soccer dyads csv as the analysis dataset
- `26-28` [high] **linked x1** — average the two raters' skin-tone scores into a single skinTone measure
- `29-31` [high] **linked x2** — collapse any red-card count into a binary gotRedCard outcome
- `32-34` [high] **linked x4** — drop dyads lacking a skin-tone rating (no photo available)
- `35-39, 58-60` [high] **linked x15** — define extreme skin-tone bins (dark >=0.75, light <=0.25, middle dropped) and restrict the primary sample to those extreme cases
- `40-57` [high] **linked x1** — map free-text position strings into five simplified role buckets (Defender/Midfielder/Forward/Goalkeeper/Other/Unknown)
- `61-64, 186-188` [high] **linked x5** — impute missing height/weight with the column median
- `65-67, 189-190, 224` [high] **linked x1** — log-transform games played for use as an exposure/offset variable
- `68-73, 191-195` [high] **linked x2** — z-standardize height, weight, and log-games before modeling
- `90-92` [high] **linked x7** — specify the primary model's covariate/adjustment set and functional form
- `93-99` [high] **linked x6** — fit the primary exposure-outcome association as logistic regression with standard errors clustered by referee
- `105-110` [medium] **linked x3** — derive a z-statistic and two-sided p-value for the primary exposure coefficient
- `123-138` [high] **linked x6** — estimate the adjusted risk difference via g-computation: predict outcomes under counterfactual all-dark vs all-light exposure and average
- `146-172` [high] **linked x5** — quantify uncertainty in the risk difference via a parametric bootstrap over the model's coefficient covariance, using a percentile CI
- `196-203` [high] **linked x4** — sensitivity check: re-fit using continuous skinTone instead of the binary extreme-group exposure
- `209-217` [high] **linked x2** — sensitivity check: re-code exposure via a median split instead of extreme groups
- `223, 225-231` [high] **linked x3** — sensitivity check: re-fit as a Poisson model with a log-games offset instead of logistic regression
