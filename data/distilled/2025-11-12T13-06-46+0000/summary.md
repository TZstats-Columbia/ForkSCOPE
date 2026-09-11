# 2025-11-12T13-06-46+0000  (ai)

- code: 369 lines, 26% exon (96 lines in 14 decisions)
- intron: print 122, comment 85, plot 55, import 9, config 1, glue 1
- prose: 301 lines, 113 claims (32 action, 81 result)
- links: 47 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 3
- result_claims_deferred: 81

## All decisions

- `26` [high] **linked x2** — load the raw player-referee dyad CSV as the full analysis dataset
- `32` [high] **linked x2** — drop dyads lacking both raters' skin-tone scores
- `37` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous measure
- `44-48, 54, 264` [high] **linked x3** — split continuous skin tone at the 0.5 midpoint into Light/Dark categories and a dark-skin binary indicator, later marked on the distribution plot
- `51` [high] **linked x2** — define the outcome as whether any red card occurred in the dyad
- `57` [high] **linked x2** — log-transform games played to use as an exposure-adjustment covariate
- `60` [high] **linked x3** — drop dyads with missing position data to form the final analysis sample
- `73, 259` [low] **linked x2** — collapse dyad-level rows to one row per player by keeping the first occurrence, for player-level description and plotting
- `98-101, 112-113` [high] **linked x12** — fit the primary logistic model of any_red_card on dark_skin adjusting for exposure, position and league with player-clustered standard errors, and express the effect as an odds ratio
- `126-172` [high] **linked x10** — compute the primary effect as an adjusted risk difference via average marginal effects, with delta-method standard errors (numerical gradient) and a normal-approximation 95% CI and p-value
- `195-198` [high] **linked x2** — fit a minimally-adjusted sensitivity model with only exposure as a covariate
- `202-208, 211-214` [high] **linked x2** — construct a per-player yellow-card rate and add it as a covariate in a sensitivity model
- `218-222, 225-228` [high] **linked x2** — restrict the sample to only the most extreme skin-tone scores and refit the model on this subsample
- `233-236` [high] **linked x2** — refit the model using the continuous skin-tone score instead of the dichotomized category
