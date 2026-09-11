# 2025-11-19T16-04-43+0000  (ai)

- code: 270 lines, 28% exon (75 lines in 12 decisions)
- intron: print 127, comment 53, import 9, config 6
- prose: 267 lines, 134 claims (42 action, 92 result)
- links: 74 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 12
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 5
- result_claims_deferred: 92

## All decisions

- `32` [high] **linked x3** — load the full player-referee dyad dataset from a fixed CSV path with no filtering applied at load time
- `36` [high] **linked x1** — average the two raters' skin-tone scores into one continuous score
- `39-40` [high] **linked x2** — dichotomize continuous skin tone into a dark/light indicator at a 0.5 cutoff, leaving originally-missing scores as missing
- `43` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `53-58, 63` [high] **linked x4** — restrict to dyads with both raters present and quantify rater agreement via Pearson/Spearman correlation, a 5-level binning of the ratings for Cohen's kappa, and an exact-match percentage
- `74-75` [high] **linked x7** — build the modeling sample by selecting a fixed set of covariates and dropping any row with a missing value among them
- `85-86, 93-96, 108-110` [high] **linked x4** — stratify the sample by skin-tone group to get group sizes and red-card rates, then derive unadjusted contrast measures (risk difference, risk ratio, odds ratio) between groups
- `125-126, 139-142` [high] **linked x20** — fit a logistic regression of any_red_card on dark_skin adjusting for position, league country, and games, then convert the exposure coefficient and its Wald interval into an odds ratio
- `158-169` [high] **linked x10** — estimate an adjusted (standardized) risk difference by g-computation: predict outcome probability under counterfactual all-light and all-dark exposure and average the difference across the sample
- `179-208` [high] **linked x12** — quantify uncertainty for the standardized risk difference by drawing 5000 simulated parameter vectors from the model's asymptotic normal distribution, recomputing the counterfactual risk difference for each draw, and taking the empirical percentile interval, SD, and a Wald-style p-value of the simulated distribution
- `226-227` [high] **linked x5** — refit the adjusted model with games dropped from the covariate set, as a robustness check on the adjustment set
- `234-235` [high] **linked x5** — refit the model using continuous skin_tone_avg in place of the dichotomized exposure, as a robustness check on exposure coding
