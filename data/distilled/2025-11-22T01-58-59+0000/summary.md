# 2025-11-22T01-58-59+0000  (ai)

- code: 455 lines, 29% exon (131 lines in 21 decisions)
- intron: plot 127, print 115, comment 54, import 14, glue 10, config 4
- prose: 242 lines, 81 claims (40 action, 41 result)
- links: 55 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 6
- result_claims_deferred: 41

## Silent decisions — executed, never disclosed

- **126** [high] drop any dyad with a missing modeling covariate instead of imputing (complete-case analysis)
- **131-135** [medium] one-hot encode position and league into dummy columns, keeping all levels at encoding time

## All decisions

- `37-38` [high] **linked x1** — load the full soccer referee-dyad dataset from a fixed CSV path with no filtering at read time
- `40-42` [high] **linked x2** — average the two independent raters' skin-tone scores into one continuous score per player
- `43-45, 47` [medium] **linked x3** — quantify inter-rater agreement (Pearson correlation, mean absolute difference) restricted to dyads where both raters scored the player
- `54-57, 59-60` [high] **linked x2** — split the continuous skin-tone score into light (<=0.25) and dark (>=0.75) groups using fixed cutoffs
- `58` [medium] **linked x2** — drop players who have no averaged skin-tone score
- `61-65` [high] **linked x3** — keep only the light and dark extremes, discard medium-tone players, and collapse to a single dark-vs-light exposure indicator
- `66-68` [high] **linked x3** — collapse the red-card count into a binary any-red-card outcome
- `82-85` [medium] **linked x1** — compute the raw (unadjusted) difference in red-card rate between the dark and light groups
- `95-112` [high] **linked x1** — recode free-text playing position into five buckets (Goalkeeper/Forward/Midfielder/Defender/Other/Unknown) via keyword matching
- `121-125, 139, 148` [high] **linked x6** — choose which covariates (games, yellow cards, goals, position, league) enter the outcome model and assemble the final design matrix
- `126` [high] **SILENT** — drop any dyad with a missing modeling covariate instead of imputing (complete-case analysis)
- `131-135` [medium] **SILENT** — one-hot encode position and league into dummy columns, keeping all levels at encoding time
- `136, 140-141` [high] **linked x2** — manually pick Goalkeeper and England as the omitted reference categories for the position/league dummies
- `150` [high] **linked x2** — cluster observations by player identity for the correlation structure
- `151-152, 154-155` [high] **linked x6** — fit a GEE logistic regression with an exchangeable within-player correlation structure as the outcome model
- `167-185` [high] **linked x8** — estimate the adjusted risk difference by setting everyone's exposure to dark vs light and averaging the model's predicted probabilities (marginal standardization)
- `190-191, 193-214` [high] **linked x5** — build a 95% CI for the adjusted risk difference via a 1000-draw parametric bootstrap over the coefficient covariance, using the percentile method
- `215-218` [medium] **linked x3** — report the GEE model's Wald-based coefficient and p-value for the exposure term as the significance test
- `235-239` [high] **linked x3** — convert the exposure coefficient to an odds ratio and derive its CI from the model's Wald confidence interval rather than the bootstrap
- `261-267` [medium] **linked x1** — check multicollinearity via VIF computed only on the four continuous/base predictors, excluding the categorical dummy sets
- `272-276` [medium] **linked x1** — assess model discrimination with in-sample AUC, without a held-out test set
