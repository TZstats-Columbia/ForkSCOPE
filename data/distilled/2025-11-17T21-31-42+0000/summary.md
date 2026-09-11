# 2025-11-17T21-31-42+0000  (ai)

- code: 344 lines, 45% exon (155 lines in 20 decisions)
- intron: print 133, comment 33, glue 12, import 7, config 4
- prose: 212 lines, 86 claims (39 action, 47 result)
- links: 54 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 11
- result_claims_deferred: 47

## Silent decisions — executed, never disclosed

- **33-37** [high] parse birthday strings and derive player age relative to a fixed mid-season reference date

## All decisions

- `25-26` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path
- `27-29` [high] **linked x1** — average the two independent raters' skin-tone scores into a single continuous score
- `30-32` [high] **linked x3** — collapse the red card count into a binary any-red-card outcome
- `33-37` [high] **SILENT** — parse birthday strings and derive player age relative to a fixed mid-season reference date
- `50-52` [high] **linked x2** — drop dyads lacking a skin-tone photo rating
- `55-64` [high] **linked x5** — dichotomize skin tone into light (<=0.25) vs dark (>=0.75), dropping intermediate ratings
- `69-83` [high] **linked x1** — collapse detailed playing position strings into five coarse categories
- `84-93` [high] **linked x8** — restrict the sample to complete cases on skin tone and the covariates used downstream
- `109-113` [medium] **linked x2** — assess inter-rater reliability using Pearson correlation and exact-agreement rate between the two raters
- `118-123` [medium] **linked x1** — compute the unadjusted (crude) red-card-rate difference between light- and dark-skin groups
- `158-163` [high] **linked x1** — standardize the continuous covariates (age, height, weight, games) before modeling
- `164-168` [high] **linked x5** — specify the regression formula: outcome, exposure, covariate set, and reference categories for position and league
- `169-171, 173-174` [high] **linked x4** — cluster standard errors by player to account for repeated dyads per player
- `172` [high] **linked x1** — model the binary outcome with logistic regression
- `200-221, 225-228` [high] **linked x5** — define and evaluate the risk difference as an average marginal effect via g-computation contrasting an all-light vs all-dark counterfactual
- `229-250` [high] **linked x2** — estimate the sampling variance of the risk difference via the delta method using a numerically computed Jacobian
- `251-256` [high] **linked x3** — construct the risk difference's confidence interval and p-value using a normal approximation (±1.96 SE)
- `264-275` [medium] **linked x1** — additionally report the effect as absolute predicted probabilities for each counterfactual group
- `292-297` [high] **linked x4** — report the secondary estimand as an odds ratio via exponentiated coefficient with a normal-approximation CI
- `336-339` [high] **linked x3** — declare statistical significance using a 0.05 alpha threshold
