# 2025-11-12T17-10-55+0000  (ai)

- code: 365 lines, 48% exon (175 lines in 21 decisions)
- intron: print 116, glue 46, comment 9, import 9, other 6, config 4
- prose: 217 lines, 111 claims (44 action, 67 result)
- links: 78 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 2
- result_claims_deferred: 67

## All decisions

- `31-32` [high] **linked x1** — load the raw player-referee dyad dataset from a fixed CSV path as the full analysis universe
- `34-36` [high] **linked x1** — average the two raters' skin-tone codings into a single continuous skinTone score
- `43-46` [high] **linked x3** — dichotomize continuous skin tone into dark/light groups at the 0.50 midpoint, propagating missing ratings as NaN
- `47-49` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `58-60` [high] **linked x2** — drop dyads with missing skin-tone ratings from the analysis sample
- `62-64` [high] **linked x2** — drop dyads with missing player position from the analysis sample
- `66-69` [high] **linked x2** — impute missing height and weight with the sample median instead of dropping those rows
- `70-73` [medium] **linked x2** — treat player position and league as categorical factors for later adjustment
- `74-75` [high] **linked x2** — z-standardize height and weight before using them as covariates
- `76` [high] **linked x2** — log-transform games played to address skew before using it as a covariate
- `93-96, 99-101` [high] **linked x6** — compute the unadjusted (crude) red-card rate difference between dark- and light-skinned players by simple group comparison
- `112-113, 115-117` [high] **linked x7** — specify and fit the primary adjusted logistic regression of any red card on skin tone plus covariates (games, height, weight, position, league)
- `125-128` [high] **linked x5** — express the primary model's skin-tone effect as an odds ratio by exponentiating the logistic coefficient and its confidence interval
- `145-158` [high] **linked x8** — estimate the adjusted risk difference via G-computation: predict outcomes under counterfactual all-light and all-dark skin tone assignments and average the difference
- `171-210, 215-218` [high] **linked x7** — obtain uncertainty for the adjusted risk difference by nonparametric bootstrap: resample dyads with replacement, refit the model, recompute RD over 1000 iterations, and take the percentile interval
- `219-221` [medium] **linked x1** — derive a two-sided bootstrap p-value from the proportion of resampled RDs falling on each side of zero
- `234-236` [high] **linked x2** — define the clustering unit for robust inference as individual player, derived from playerShort
- `237-243, 249-251` [high] **linked x8** — refit the primary model with cluster-robust standard errors grouped by player and re-derive the odds ratio
- `264-282` [high] **linked x4** — sensitivity check restricting to extreme skin-tone deciles (<=0.25 or >=0.75), recoding as veryDark, and refitting the adjusted model with G-computation risk difference
- `288-295` [high] **linked x3** — sensitivity check keeping skin tone as a continuous predictor instead of dichotomizing it
- `299-327` [high] **linked x9** — sensitivity check refitting the adjusted model separately within each of four leagues to examine effect heterogeneity, printing per-league results and skipping leagues where the fit fails to converge
