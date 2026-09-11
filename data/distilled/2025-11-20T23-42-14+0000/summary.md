# 2025-11-20T23-42-14+0000  (ai)

- code: 337 lines, 33% exon (112 lines in 17 decisions)
- intron: print 87, comment 47, plot 45, glue 32, import 12, config 2
- prose: 263 lines, 111 claims (45 action, 66 result)
- links: 57 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 6
- result_claims_deferred: 66

## Silent decisions — executed, never disclosed

- **82-85** [high] test the unadjusted group difference in red-card rates with a two-proportion z-test

## All decisions

- `26-28` [high] **linked x3** — load the raw soccer referee dataset from a fixed CSV path, defining the full analysis population
- `33-35` [high] **linked x2** — average two independent skin-tone ratings into a single continuous skinTone score
- `36-38, 196` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome
- `39-47, 282-283` [high] **linked x3** — cut the continuous skinTone score into light/medium/dark bands at the 0.25 and 0.75 cutpoints
- `52-57` [high] **linked x4** — drop the medium skin-tone band and recode the remaining light/dark split as a 0/1 darkSkin indicator
- `67-76` [high] **linked x3** — compute the unadjusted risk difference in red-card rates between dark- and light-skinned players
- `82-85` [high] **SILENT** — test the unadjusted group difference in red-card rates with a two-proportion z-test
- `95-99, 190-194` [medium] **linked x3** — one-hot encode position and league country with the first category dropped as reference
- `103-105, 197-198` [high] **linked x3** — restrict the regression sample to complete cases on height and weight rather than imputing
- `114-118, 154-157, 201-202` [high] **linked x7** — fix the adjustment set (games, height, weight, plus position and league dummies) reused across the primary, logistic, and sensitivity models
- `125-128, 208-210` [high] **linked x11** — fit a linear probability model with standard errors clustered by player as the effect estimator
- `148-149, 224-225, 322-323` [medium] **linked x3** — adopt a 0.05 alpha threshold for declaring an effect statistically significant / the hypothesis supported
- `158-160` [medium] **linked x3** — fit a logistic regression with ordinary (non-clustered) standard errors as the secondary odds-ratio model
- `161-168` [medium] **linked x3** — build the odds-ratio confidence interval with a normal-approximation Wald formula (coef ± 1.96·SE) before exponentiating
- `186-187, 199-200` [high] **linked x5** — swap the dichotomized exposure for continuous skinTone and widen the sample to everyone with a non-missing rating
- `234-241, 245-246` [medium] **linked x1** — flag multicollinearity using a variance-inflation-factor greater-than-10 cutoff
- `247-250, 253-255` [medium] **linked x1** — check the linear probability model's validity by counting fitted probabilities that fall outside the [0,1] range
