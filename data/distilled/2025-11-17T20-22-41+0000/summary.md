# 2025-11-17T20-22-41+0000  (ai)

- code: 286 lines, 37% exon (106 lines in 22 decisions)
- intron: glue 71, print 65, comment 34, import 8, config 2
- prose: 326 lines, 149 claims (57 action, 92 result)
- links: 89 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 17
- result_claims_deferred: 92

## Silent decisions — executed, never disclosed

- **125-126** [high] code dark skin tone as the exposure indicator with light as reference
- **219** [medium] silently discard bootstrap iterations where the model fails to fit, rather than counting or flagging them

## All decisions

- `27` [high] **linked x2** — choose the input dataset file to load as the analysis population
- `33-34` [high] **linked x1** — collapse two independent skin-tone ratings into a single averaged score
- `36-40` [high] **linked x5** — cut the continuous skin-tone score into light/dark groups at 0.25 and 0.75, discarding the middle range
- `42-43` [high] **linked x2** — reduce the red-card count to a binary any-red-card outcome
- `45-47` [high] **linked x1** — derive player age from birth year using a fixed mid-season reference date
- `49-65` [high] **linked x1** — collapse free-text position strings into a small set of position categories via keyword matching
- `73-74` [high] **linked x7** — restrict the analysis sample to dyads with non-missing skin tone and age, using age as a proxy for photo availability
- `76-78` [high] **linked x1** — fill missing height and weight with the sample median rather than dropping those rows
- `95-102` [high] **linked x12** — choose which variables and summary functions to compute per skin-tone group
- `110-113` [high] **linked x1** — compute the unadjusted (crude) risk difference between dark and light groups as a percentage-point gap
- `125-126` [high] **SILENT** — code dark skin tone as the exposure indicator with light as reference
- `128-132` [high] **linked x2** — z-score standardize the continuous covariates before entering them in the model
- `134, 137-139, 142` [high] **linked x14** — fit a logistic regression as the outcome model, with fitting controls (max iterations, no display)
- `135` [high] **linked x9** — select the adjustment set of covariates included in the outcome model
- `140-141` [high] **linked x2** — cluster standard errors at the player level rather than treating dyads as independent
- `160-173` [high] **linked x9** — estimate the adjusted risk difference via marginal standardization (predict outcome under counterfactual all-dark and all-light exposure, then average and subtract)
- `188-189, 198-199, 201-202, 204-206, 208-215, 217` [high] **linked x4** — run a cluster (player-level) bootstrap that resamples players with replacement, refits the same model, and recomputes the marginal-standardization risk difference each iteration
- `219` [medium] **SILENT** — silently discard bootstrap iterations where the model fails to fit, rather than counting or flagging them
- `222, 224-225` [high] **linked x3** — form the 95% CI from the 2.5th/97.5th percentiles of the bootstrap distribution
- `229-230` [high] **linked x2** — compute a two-sided bootstrap p-value by doubling the smaller tail proportion on either side of zero
- `237-238` [high] **linked x7** — report the exposure effect as an odds ratio by exponentiating the logistic coefficient and its CI
- `274-277` [high] **linked x4** — define the criterion for declaring the hypothesis supported: p < 0.05 AND the bootstrap CI excludes zero on the low end
