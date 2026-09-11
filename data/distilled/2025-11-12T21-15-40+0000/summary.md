# 2025-11-12T21-15-40+0000  (ai)

- code: 272 lines, 34% exon (93 lines in 17 decisions)
- intron: print 118, comment 45, import 6, config 5, glue 5
- prose: 272 lines, 82 claims (39 action, 43 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 6
- result_claims_deferred: 43

## Silent decisions — executed, never disclosed

- **68-69** [medium] impute missing player position with the literal category 'Unknown'

## All decisions

- `25-26` [high] **linked x1** — read the raw player-referee dyad csv as the full dataset
- `33-34` [high] **linked x2** — drop dyads that are missing either skin-tone rating
- `37-38` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `41-50` [high] **linked x2** — bin the continuous skin-tone average into light/medium/dark categories at 0.25 and 0.5 cutpoints
- `52-53` [high] **linked x3** — restrict the primary-analysis sample to light and dark categories, excluding medium
- `56-58` [high] **linked x3** — dichotomize red cards into any_red_card and derive a binary dark_skin exposure indicator from the category
- `60-61` [high] **linked x3** — drop dyads with missing height or weight to form the complete-case analysis set
- `68-69` [medium] **SILENT** — impute missing player position with the literal category 'Unknown'
- `71-77` [high] **linked x2** — collapse positions outside a fixed list of seven main positions into an 'Other' bucket
- `101-103` [medium] **linked x1** — compute crude (unadjusted) red-card rates for each skin-tone group as a baseline comparison
- `118-125` [high] **linked x14** — specify and fit a logistic regression of any_red_card on dark_skin adjusting for games, grouped position and league country, with standard errors clustered by player
- `135-156` [high] **linked x2** — derive the average marginal effect (risk-difference scale) via counterfactual all-dark/all-light predictions and a delta-method standard error
- `158-166` [medium] **linked x7** — build a 95% CI and two-sided p-value for the marginal effect using a fixed z=1.96 normal critical value
- `180-181` [high] **linked x2** — report the dark_skin coefficient as an exponentiated odds ratio with CI as a secondary estimand
- `207-213` [high] **linked x1** — rebuild covariates on the full (non-binned) ratings sample for the sensitivity check, re-applying the height/weight completeness filter and outcome/position recoding
- `215-220` [high] **linked x6** — fit a sensitivity logistic model using the continuous skin_tone_avg measure in place of the binary dark_skin indicator, same covariates and clustering
- `259-262` [medium] **linked x2** — declare the hypothesis 'supported' only when the p-value is below 0.05 and the CI lower bound exceeds zero, otherwise 'not supported'
