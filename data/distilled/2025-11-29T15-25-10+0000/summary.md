# 2025-11-29T15-25-10+0000  (ai)

- code: 186 lines, 44% exon (82 lines in 14 decisions)
- intron: print 61, comment 34, import 5, config 4
- prose: 169 lines, 91 claims (51 action, 40 result)
- links: 42 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 19
- R_only_consistent_negative: 9
- result_claims_deferred: 40

## All decisions

- `20-22` [medium] **linked x1** — load the full soccer referee dataset from csv as the analysis population
- `23-25` [high] **linked x2** — average the two raters' skin-tone scores into a single consensus skinTone measure
- `26-28` [high] **linked x2** — collapse red card counts into a binary any-red-card indicator
- `29-33` [high] **linked x1** — derive player age from birthday relative to a fixed 2013-01-01 reference date
- `34-37` [high] **linked x4** — drop dyads missing skinTone or key covariates (height, weight, position, meanIAT, meanExp) from the modeling sample
- `47-52` [high] **linked x6** — binarize skin tone at a 0.375 cutoff, chosen via specification search, to define the dark-skin exposure group
- `64-68` [high] **linked x1** — compute and report the unadjusted (crude) red-card rate difference between dark- and light-skin groups
- `77-83` [high] **linked x7** — fit the primary logistic regression of anyRedCard on darkSkin adjusting for age, height, weight, position, leagueCountry, games, meanIAT, and meanExp
- `90-100` [high] **linked x5** — compute the overall average marginal effect for darkSkin as the primary risk-difference estimand, expressed in percentage points
- `113-120` [high] **linked x4** — convert the darkSkin coefficient to an odds ratio with a 1.96-SE Wald confidence interval as a secondary estimand
- `136-142` [high] **linked x1** — refit the model with skin tone binarized at an alternate 0.25 cutoff as a sensitivity check
- `148-154` [high] **linked x1** — refit the model with skin tone binarized at an alternate 0.50 cutoff as a sensitivity check
- `160-165` [high] **linked x3** — refit the model using continuous skinTone in place of the binarized exposure as a sensitivity check
- `171-177` [high] **linked x4** — refit the model dropping the referee-bias covariates meanIAT and meanExp from the adjustment set as a sensitivity check
