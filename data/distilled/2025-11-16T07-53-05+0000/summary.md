# 2025-11-16T07-53-05+0000  (ai)

- code: 426 lines, 44% exon (188 lines in 21 decisions)
- intron: print 151, comment 48, glue 27, import 6, config 5, other 1
- prose: 234 lines, 88 claims (48 action, 40 result)
- links: 57 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 3
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **149-154** [low] choose a set of covariates and compute their unadjusted group means to check pre-adjustment balance
- **339-347** [high] refit the model excluding yellow cards from the adjustment set to check whether it acts as a mediator
- **359-361** [high] restrict the sample to only the most extreme rater scores (0.00 vs 1.00) as an alternative exposure contrast

## All decisions

- `32-33` [high] **linked x1** — load the raw player-referee dyad dataset from the soccer.csv source file
- `37-38` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `53-54` [high] **linked x3** — drop dyads lacking a skin-tone rating (no player photo available)
- `58-61` [high] **linked x1** — drop dyads where recorded yellow+red cards exceed games played, treating them as data-entry errors
- `73-74, 362` [high] **linked x1** — define the binary outcome as whether the dyad received at least one red card
- `76-84` [high] **linked x8** — dichotomize skin tone into light (<=0.25) vs dark (>=0.75) groups and build the primary analytic sample from only those two groups, dropping the middle range
- `92-95` [medium] **linked x1** — compute player age at a chosen mid-season reference date (2012-07-01) from birthday
- `98-112` [high] **linked x2** — collapse detailed playing positions into six broader position categories via custom mapping rules
- `113-118` [high] **linked x2** — impute missing height and weight with the sample median and flag which rows were imputed
- `121-125, 364-367, 391-394` [high] **linked x2** — one-hot encode position group and league country, dropping the first level as reference category
- `142-143, 146` [medium] **linked x1** — compute the unadjusted (crude) red-card rate difference between dark and light skin-tone groups
- `149-154` [low] **SILENT** — choose a set of covariates and compute their unadjusted group means to check pre-adjustment balance
- `164-176, 369-372` [high] **linked x13** — specify and fit the primary logistic regression of red cards on skin-tone group adjusted for games, age, height, weight, yellow cards, position, and league, weighted by games with HC1 robust errors
- `181-184, 352, 382, 413` [high] **linked x4** — report the exponentiated dark-vs-light coefficient (and its CI) as an odds-ratio effect size
- `193-211, 349-351, 374-381, 405-412` [high] **linked x9** — standardize predicted probabilities under counterfactual dark=1 vs dark=0 (games-weighted) to obtain an adjusted risk difference
- `228-229, 232-242, 244-261` [high] **linked x2** — run a parametric bootstrap (10,000 draws from the fitted coefficients' asymptotic multivariate normal) to simulate the risk-difference distribution
- `263-265` [high] **linked x3** — form the 95% CI from the 2.5th/97.5th percentiles of the bootstrap risk-difference draws
- `268-269` [high] **linked x2** — derive an empirical two-sided p-value from the proportion of bootstrap draws on each side of zero
- `339-347` [high] **SILENT** — refit the model excluding yellow cards from the adjustment set to check whether it acts as a mediator
- `359-361` [high] **SILENT** — restrict the sample to only the most extreme rater scores (0.00 vs 1.00) as an alternative exposure contrast
- `390, 396-403` [high] **linked x1** — model skin tone as a continuous predictor instead of a dichotomized group
