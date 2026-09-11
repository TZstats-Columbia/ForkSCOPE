# 2025-11-16T02-42-50+0000  (ai)

- code: 365 lines, 34% exon (125 lines in 15 decisions)
- intron: print 121, plot 50, comment 47, import 9, glue 9, config 4
- prose: 297 lines, 91 claims (35 action, 56 result)
- links: 47 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 5
- result_claims_deferred: 56

## All decisions

- `33-35` [high] **linked x2** — read the raw player-referee dyad CSV as the source dataset for the whole analysis
- `38-40` [high] **linked x1** — average the two independent raters' scores into a single continuous skin_tone measure
- `42-46` [high] **linked x3** — threshold continuous skin_tone at 0.5 to create a binary light/dark exposure group
- `47-49` [high] **linked x1** — collapse the red card count into a binary any-red-card outcome
- `50-66` [high] **linked x1** — recode twelve specific playing positions into four broader position categories
- `67-69` [high] **linked x1** — drop dyads with missing skin_tone to define the analysis sample
- `88-89, 94` [medium] **linked x3** — compute the crude (unadjusted) red-card rate difference and odds ratio between dark- and light-skinned groups
- `101-104` [high] **linked x3** — dummy-code league and position group, dropping the first level of each as the reference category
- `105-107` [high] **linked x2** — log-transform games played before entering it as a model covariate
- `123-126` [high] **linked x7** — fit a logistic regression of any_red_card on dark_skin adjusting for log_games, league, and position
- `136-139` [high] **linked x5** — exponentiate the dark_skin coefficient and its confidence interval to express the adjusted association as an odds ratio
- `155-172` [high] **linked x5** — estimate the adjusted risk difference by marginal standardization, averaging model predictions under all-light and all-dark counterfactual scenarios
- `186-224, 227, 228-232` [high] **linked x5** — bootstrap the risk difference by resampling dyads with replacement, refitting the logistic model per resample (bfgs, 500 iterations), and taking the 2.5/97.5 percentiles as the CI
- `269` [medium] **linked x4** — declare the finding 'supported' only when the adjusted p-value is below 0.05 and the bootstrap CI for the risk difference excludes zero
- `285-293` [high] **linked x4** — restrict to extreme skin-tone groups (<=0.25 vs >=0.75) and refit the adjusted model as a sensitivity check
