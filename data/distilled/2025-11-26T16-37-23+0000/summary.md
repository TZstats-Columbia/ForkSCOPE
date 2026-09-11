# 2025-11-26T16-37-23+0000  (ai)

- code: 309 lines, 24% exon (75 lines in 15 decisions)
- intron: print 161, comment 47, import 8, glue 8, config 5, other 5
- prose: 277 lines, 147 claims (77 action, 70 result)
- links: 67 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 45
- R_only_consistent_negative: 10
- result_claims_deferred: 70

## All decisions

- `32-33` [high] **linked x1** — pull in the raw player-referee dyad table from a fixed CSV path as the universe for analysis
- `47-48` [high] **linked x1** — average the two raters' ratings into one continuous skin-tone score per player
- `67-68` [high] **linked x5** — drop dyads missing skin tone or position to form the analytic sample
- `83-87` [high] **linked x3** — dichotomize continuous skin tone into a binary dark/light indicator at a 0.125 cutoff
- `88-89` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `94-101` [high] **linked x3** — fill missing height/weight with the median value within each player's position group
- `115-118` [medium] **linked x4** — compute crude (unadjusted) red-card rates by skin-tone group and their difference as a baseline comparison
- `125-127` [medium] **linked x2** — test skin-tone/red-card association with a chi-square test on the 2x2 contingency table
- `130, 132-140` [medium] **linked x9** — aggregate red-card rate and mean skin tone by playing position and rank positions by red-card rate
- `151-153, 158` [high] **linked x10** — specify and fit the primary logistic regression of any-red-card on dark skin adjusting for position, league, games, yellow cards, height and weight
- `173-175` [high] **linked x10** — summarize the dark-skin effect as an average marginal effect (risk-difference scale) rather than the raw coefficient
- `201-205` [high] **linked x6** — exponentiate the dark-skin logit coefficient (and its CI) into an odds ratio as the secondary effect measure
- `221, 223-226, 227-229, 230-232` [high] **linked x4** — restrict to extreme skin-tone dyads (>=0.75 vs <=0.125) and refit the same adjusted model on that subsample as a robustness check
- `240, 242-244, 245-247` [high] **linked x4** — refit the model using continuous skin tone in place of the dichotomized indicator as a robustness check
- `252, 254-256, 257-259` [high] **linked x4** — refit the model dropping height and weight covariates to check sensitivity of the result to that adjustment set
