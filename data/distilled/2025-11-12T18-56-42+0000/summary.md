# 2025-11-12T18-56-42+0000  (ai)

- code: 224 lines, 40% exon (89 lines in 15 decisions)
- intron: print 73, comment 33, glue 15, import 8, config 6
- prose: 263 lines, 146 claims (41 action, 105 result)
- links: 42 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 12
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 8
- result_claims_deferred: 105

## Silent decisions — executed, never disclosed

- **21-22** [high] load the specific source CSV as the analysis input
- **28-29** [high] average the two rater columns into one continuous skin-tone score
- **96** [high] encode player identity as a numeric ID to use as the clustering unit

## All decisions

- `21-22` [high] **SILENT** — load the specific source CSV as the analysis input
- `28-29` [high] **SILENT** — average the two rater columns into one continuous skin-tone score
- `31-33` [medium] **linked x2** — restrict inter-rater correlation check to dyads with non-missing rater1 and rater2
- `35-40, 46` [high] **linked x5** — collapse continuous skin tone into a binary light/dark grouping using ≤0.25 / ≥0.75 cutoffs, dropping the middle range from the analysis sample
- `42-43` [high] **linked x1** — binarize the red card outcome as any red card (redCards > 0) vs none
- `78-79` [high] **linked x2** — restrict modeling sample to complete cases on position, treating it as a key confounder to require
- `84-85` [medium] **linked x1** — treat position and league country as unordered categorical covariates
- `86-88` [high] **linked x1** — standardize games, yellowCards, and height covariates to z-scores before modeling
- `90-93` [high] **linked x3** — select the final adjustment/covariate set for modeling and drop any remaining rows with missing values on those columns
- `96` [high] **SILENT** — encode player identity as a numeric ID to use as the clustering unit
- `110-111` [high] **linked x9** — specify the logistic regression model formula and covariate/adjustment set for the primary outcome model
- `114-119` [high] **linked x5** — fit logistic regression via IRLS with player-clustered robust standard errors instead of default SEs
- `131-137` [high] **linked x5** — report the adjusted odds ratio (exponentiated coefficient) with Wald CI and p-value as a secondary estimand
- `147-163` [high] **linked x4** — compute the adjusted risk difference as the primary estimand via g-computation: set all dyads to light then dark counterfactually, predict outcome probabilities from the fitted model, and average the difference
- `169-197` [high] **linked x4** — derive the standard error, 95% CI, and p-value for the adjusted risk difference via the delta method (analytic gradient of predicted-probability contrast propagated through the model covariance)
