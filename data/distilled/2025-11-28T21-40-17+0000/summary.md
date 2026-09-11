# 2025-11-28T21-40-17+0000  (ai)

- code: 357 lines, 45% exon (160 lines in 19 decisions)
- intron: print 98, comment 82, import 11, config 5, other 1
- prose: 246 lines, 99 claims (44 action, 55 result)
- links: 54 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 7
- result_claims_deferred: 55

## Silent decisions — executed, never disclosed

- **58** [high] collapse the red card count into a binary any-red-card outcome
- **61-63** [high] derive player age at a fixed 2013-01-01 season-midpoint reference date from birthday

## Misaligned — code and prose disagree

- code: restrict to complete cases on position, height, weight, and the two IAT/exposure covariates
  - prose: excluded 9,164 dyads (6.3% of remaining) for missing covariates: position, height/weight, referee country
  - why: code restricts complete cases on meanIAT/meanExp; claim lists referee country as the additional missing covariate

## All decisions

- `30` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path, defining the full analysis universe
- `41` [high] **linked x3** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `54` [high] **linked x1** — drop dyads lacking a skin tone score before any modeling
- `58` [high] **SILENT** — collapse the red card count into a binary any-red-card outcome
- `61-63` [high] **SILENT** — derive player age at a fixed 2013-01-01 season-midpoint reference date from birthday
- `66, 207` [high] **linked x1** — dichotomize skin tone into dark/light using a 0.25 cut point and reuse that exposure in the binary sensitivity model formula
- `69-83` [high] **linked x1** — collapse the many detailed field positions into four broad position categories
- `86` [high] **linked x2** — restrict to complete cases on position, height, weight, and the two IAT/exposure covariates
- `94-99` [high] **linked x1** — z-score the continuous covariates (age, height, weight, games, yellow cards) before entering them in the model
- `110` [high] **linked x6** — specify the primary model's exposure and adjustment set (skin tone plus position, league country, and yellow cards)
- `113-117, 208-213, 270-275, 284-289` [high] **linked x4** — fit a logistic regression with standard errors clustered on player to account for repeated dyads per player
- `123-128, 214-219, 276-277, 290-291` [high] **linked x5** — convert the fitted coefficient to an odds ratio and derive its CI/p-value from a normal approximation to the Wald statistic
- `142-145, 148-149, 152-154, 226-230, 231-233, 295-298, 299-301` [high] **linked x5** — estimate the risk difference by g-computation: set exposure to its two extreme values and average the model-predicted probabilities
- `161-166, 169-170, 173-186, 236-241, 242-244, 245-257` [high] **linked x5** — quantify uncertainty in the risk difference by simulating parameter draws from the model's covariance matrix and recomputing the contrast for each draw
- `192-193` [medium] **linked x4** — test the primary risk difference with a Wald z-statistic built from the simulated standard error
- `264, 265-268, 269` [high] **linked x5** — sweep the skin-tone binarization cut point across four alternative thresholds to check robustness
- `283` [high] **linked x1** — refit the primary exposure model with no covariate adjustment at all
- `341-351` [high] **linked x4** — classify the finding as supported / marginally supported / not supported using fixed 0.05 and 0.10 p-value cutoffs plus a CI-excludes-zero check
- `352` [medium] **linked x4** — additionally report a one-sided version of the p-value alongside the two-sided result
