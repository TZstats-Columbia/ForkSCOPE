# 2025-11-19T13-48-49+0000  (ai)

- code: 309 lines, 40% exon (125 lines in 21 decisions)
- intron: print 118, comment 46, import 9, glue 6, config 5
- prose: 248 lines, 132 claims (58 action, 74 result)
- links: 74 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 13
- result_claims_deferred: 74

## Silent decisions — executed, never disclosed

- **60-64** [high] derive player age by subtracting birthday from a fixed reference date and converting days to years
- **110-111** [medium] compute the raw, unadjusted red-card rate for each skin-tone group as a descriptive baseline

## All decisions

- `32-33` [high] **linked x4** — read in the full soccer referee-player dyad dataset from CSV as the analysis universe
- `36-38` [high] **linked x1** — average the two independent raters' skin-tone scores into a single continuous skin-tone measure
- `39-40` [low] **linked x2** — restrict to dyads with both rater scores present and use that subset to check inter-rater reliability
- `52-56` [high] **linked x3** — split the continuous skin-tone score into dark vs light groups at a 0.5 midpoint cutoff
- `57-59` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `60-64` [high] **SILENT** — derive player age by subtracting birthday from a fixed reference date and converting days to years
- `65-67` [medium] **linked x2** — log-transform games played to use as an exposure/adjustment covariate
- `68, 70-74` [high] **linked x3** — z-score standardize age, height, and weight before including them as covariates
- `75-78` [medium] **linked x2** — cast position and league country to categorical dtype for use as factor covariates
- `87-90` [high] **linked x9** — drop dyads missing skin tone, outcome, games, position, country, age, height, or weight to form the modeling sample
- `110-111` [medium] **SILENT** — compute the raw, unadjusted red-card rate for each skin-tone group as a descriptive baseline
- `124-126, 292-293` [high] **linked x4** — choose the covariate/adjustment set and functional form for the outcome model (skin tone plus games, position, league, age, height, weight)
- `136, 138, 201, 203-204, 295-296` [high] **linked x4** — fit a logistic regression as the model family linking covariates to the red-card outcome, including on resampled and threshold-varied data
- `141-146, 297-300` [high] **linked x9** — exponentiate the skin-tone coefficient into an odds ratio and report its Wald confidence interval and p-value
- `160-175, 205-214` [high] **linked x7** — estimate the adjusted risk difference via marginal standardization: predict outcomes under all-dark and all-light counterfactuals and difference the average predicted probabilities
- `189, 197-200` [high] **linked x3** — resample dyads with replacement 2000 times to build a bootstrap distribution of the risk difference
- `202, 216-219, 294, 303` [medium] **linked x1** — catch model-fitting failures on resampled or threshold-varied data and drop or flag them instead of stopping the run
- `223-227` [high] **linked x2** — derive the risk difference's 95% interval and standard error from percentiles and the spread of the bootstrap distribution
- `228-230` [high] **linked x2** — compute a two-sided p-value as twice the share of bootstrap draws at or below zero
- `263-273` [high] **linked x5** — translate the confidence interval into a supported / not-supported / inconclusive verdict using a 0.05 significance rule
- `284-285, 287-291` [high] **linked x10** — recompute the dark/light split at alternative skin-tone thresholds and refit the model to test robustness of the main result
