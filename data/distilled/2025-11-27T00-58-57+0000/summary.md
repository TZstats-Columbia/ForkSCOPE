# 2025-11-27T00-58-57+0000  (ai)

- code: 442 lines, 40% exon (175 lines in 15 decisions)
- intron: print 211, comment 43, import 8, config 4, glue 1
- prose: 270 lines, 79 claims (49 action, 30 result)
- links: 44 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 19
- R_only_consistent_negative: 8
- result_claims_deferred: 30

## Silent decisions — executed, never disclosed

- **31-32** [high] load the raw soccer dataset from a fixed CSV path as the starting sample
- **41-57** [high] map detailed on-field positions into four broad position groups, with unmatched/other positions falling into Goalkeeper by default

## All decisions

- `31-32` [high] **SILENT** — load the raw soccer dataset from a fixed CSV path as the starting sample
- `36-37` [high] **linked x3** — average the two independent skin-tone raters into a single continuous skintone_avg score
- `38-40` [high] **linked x1** — collapse the red-card count into a binary any-red-card indicator by thresholding at zero
- `41-57` [high] **SILENT** — map detailed on-field positions into four broad position groups, with unmatched/other positions falling into Goalkeeper by default
- `58-63` [high] **linked x4** — restrict the analytic sample to dyads with non-missing skin-tone rating and non-missing position
- `94-95, 114-115` [high] **linked x1** — dichotomize the continuous skin-tone score at the 0.5 midpoint into light vs dark categories, later materialized as dark_binary
- `139-147` [high] **linked x9** — fit the primary model as a logistic regression of any_red on skin tone plus position-group and games, with standard errors clustered by referee
- `165-180` [high] **linked x4** — estimate the adjusted risk difference via g-computation, setting skin tone to 0 and 1 for the whole sample and averaging predicted probabilities
- `194-245` [high] **linked x3** — derive the standard error, confidence interval and p-value for the risk difference via the delta method using an analytically constructed gradient
- `260-265` [high] **linked x4** — convert the logistic-regression coefficient on skin tone into an odds ratio with confidence interval as a secondary effect measure
- `290-303` [high] **linked x3** — re-specify the exposure as the binary dark_binary variable instead of continuous skin tone, as a robustness check
- `312-324` [high] **linked x3** — add league country as an extra covariate in the model as a robustness check
- `334-346` [high] **linked x3** — swap the four-category position group for the full detailed position variable as covariate, as a robustness check
- `356-370` [high] **linked x3** — drop goalkeepers from the sample and refit the primary specification on the restricted sample
- `423, 424-425` [high] **linked x3** — declare the hypothesis 'supported' only when both the risk-difference and odds-ratio p-values fall under a 0.05 significance threshold
