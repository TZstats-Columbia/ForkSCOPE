# 2025-11-19T03-21-59+0000  (ai)

- code: 317 lines, 42% exon (133 lines in 16 decisions)
- intron: print 77, comment 47, plot 45, import 9, config 3, glue 3
- prose: 269 lines, 124 claims (54 action, 70 result)
- links: 76 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 10
- result_claims_deferred: 70

## All decisions

- `24-26` [high] **linked x2** — load the raw soccer referee/player dataset from CSV as the full analysis scope
- `30-32` [high] **linked x1** — average the two independent raters' scores into a single continuous skin-tone measure
- `33-39, 253-256` [high] **linked x7** — dichotomize continuous skin tone at the 0.50 midpoint into dark/light categories, excluding exactly-neutral or missing ratings
- `40-42` [high] **linked x3** — collapse the red card count into a binary any-red-card outcome using a >0 threshold
- `52-54` [high] **linked x2** — restrict the analytic sample to dyads with a non-missing, non-neutral skin tone category
- `55-58` [high] **linked x1** — drop dyads with missing height, weight, position, or league covariates
- `65-80` [high] **linked x16** — build the model design matrix: one-hot encode position and league (dropping a reference level) and choose the full covariate/adjustment set alongside darkSkin as predictors of any red card
- `81-87` [medium] **linked x4** — drop remaining rows with any missing predictor value and designate player identity as the clustering unit for later SE estimation
- `100-103` [high] **linked x1** — compute the unadjusted risk difference as the raw difference in red-card rates between dark- and light-skin groups
- `115-118, 125-130` [high] **linked x3** — fit a logistic regression of any red card on skin tone and covariates with cluster-robust standard errors grouped by player
- `133-138` [medium] **linked x1** — treat the darkSkin coefficient from the fitted model as the focal adjusted effect to report
- `143-146` [high] **linked x6** — exponentiate the darkSkin coefficient and its CI to report an adjusted odds ratio as a secondary effect measure
- `158-171` [high] **linked x8** — estimate an adjusted, covariate-standardized risk difference via g-computation by scoring every observation under counterfactual darkSkin=1 vs darkSkin=0 and averaging
- `172-199` [high] **linked x6** — derive the risk difference's standard error via the delta method and construct a 95%-level Wald confidence interval and two-sided z-test p-value
- `220-233` [high] **linked x9** — declare the hypothesis supported or not based on whether the risk-difference CI excludes zero and p<=0.05
- `301-303` [low] **linked x6** — choose which covariates (key_vars subset) to display coefficients for in the diagnostics table
