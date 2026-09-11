# 2025-11-29T02-42-10+0000  (ai)

- code: 348 lines, 30% exon (106 lines in 18 decisions)
- intron: print 134, comment 50, glue 46, import 7, config 5
- prose: 285 lines, 113 claims (59 action, 54 result)
- links: 71 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 14
- result_claims_deferred: 54

## Silent decisions — executed, never disclosed

- **170-179** [medium] recompute the risk difference by predicting outcomes under counterfactual all-light/all-dark exposure and averaging, as a manual check on the AME estimate

## All decisions

- `35` [high] **linked x2** — pick which dataset file and rows constitute the analysis universe by reading a specific CSV
- `44-45` [high] **linked x6** — drop dyads lacking both raters' skin-tone scores from the analytic sample
- `48-49` [low] **linked x2** — check agreement between the two raters as a data-quality diagnostic before combining them
- `58-59` [high] **linked x2** — collapse the two rater scores into a single skin-tone measure by averaging them
- `63-64` [high] **linked x2** — reduce card counts to a binary any-red-card outcome instead of using a count or severity scale
- `67-70` [high] **linked x6** — dichotomize skin tone into dark/light groups at a 0.25 cutpoint chosen as the primary exposure definition
- `71-72, 220, 222-226` [high] **linked x3** — define an alternate 0.5 dark-skin cutpoint and refit the outcome model on it as a threshold-sensitivity check
- `73-74, 231, 233-237` [high] **linked x4** — swap the dichotomized exposure for the raw continuous skin-tone score and refit the model to check robustness to categorization
- `75-91` [medium] **linked x2** — collapse the free-text position field into a small set of coarse role categories
- `102-106, 109-111` [medium] **linked x4** — build an unadjusted cross-tabulation and compute the raw risk difference between exposure groups without any covariate adjustment
- `112-115` [high] **linked x1** — test the exposure-outcome association with a chi-square test on the contingency table
- `126-129` [high] **linked x9** — choose logistic regression with games as the sole adjustment covariate as the primary outcome model
- `150-156` [high] **linked x7** — report the average marginal effect of the exposure as the primary risk-difference estimand
- `170-179` [medium] **SILENT** — recompute the risk difference by predicting outcomes under counterfactual all-light/all-dark exposure and averaging, as a manual check on the AME estimate
- `200-203` [high] **linked x3** — exponentiate the logit coefficient to also report an adjusted odds ratio alongside the risk difference
- `242, 244-253` [high] **linked x6** — refit the primary model adding simplified position as a covariate and recompute RD/OR via manual standardization, testing sensitivity to confounding by role
- `258, 260-269` [high] **linked x6** — further extend the adjustment set with league to test sensitivity to country-level confounding
- `327` [high] **linked x6** — declare the hypothesis supported using a two-sided p<0.05 threshold combined with a positive effect direction
