# 2025-11-17T23-27-27+0000  (ai)

- code: 352 lines, 32% exon (114 lines in 20 decisions)
- intron: print 156, comment 63, import 8, glue 7, config 4
- prose: 298 lines, 89 claims (41 action, 48 result)
- links: 48 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: -1
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 11
- result_claims_deferred: 48

## All decisions

- `32` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path, fixing the source and initial scope of the analysis
- `36-37` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `39` [high] **linked x2** — drop dyads with no skin-tone rating (no player photo) from the working sample
- `44` [high] **linked x3** — collapse the red-card count into a binary any-red-card outcome using a >0 cutoff
- `45` [high] **linked x2** — dichotomize continuous skin tone into dark vs. light using a 0.5 cutpoint
- `46-47` [medium] **linked x1** — log-transform the number of games in the dyad for use as a covariate
- `59` [low] **linked x1** — define rater agreement as scores differing by no more than 0.25 points
- `73-76` [medium] **linked x1** — compute the crude (unadjusted) red-card rate difference between dark- and light-skin groups as a baseline comparison
- `91-94, 96-97` [high] **linked x5** — choose which variables must be present and drop any dyad missing one of them (complete-case analysis instead of imputation)
- `114-116, 129` [high] **linked x6** — specify and fit a logistic regression of any-red-card on dark skin, adjusting for game exposure, position, league, height, weight, and referee-country implicit/explicit bias
- `130-131` [high] **linked x1** — cluster standard errors at the player level to account for repeated dyads per player
- `153-158, 160-162, 164-167` [high] **linked x4** — estimate the adjusted risk difference via marginal standardization (g-computation): set every dyad to dark then to light skin, predict outcome probabilities under each, and average the difference
- `175-203` [high] **linked x2** — quantify uncertainty in the adjusted risk difference via a parametric bootstrap that redraws model coefficients from their asymptotic covariance 1000 times and recomputes the standardized risk difference each draw
- `205-207` [medium] **linked x1** — derive a two-sided p-value for the risk difference via a normal-approximation z-test using the bootstrap standard error
- `222-225` [high] **linked x3** — convert the primary model's dark-skin coefficient into an odds ratio with a Wald (±1.96 SE) confidence interval
- `241-243, 244-249, 250-255` [high] **linked x3** — refit the model using continuous skin tone in place of the dichotomized exposure and rescale the effect to an odds ratio per 0.1-unit increase
- `263-268, 269-273` [high] **linked x1** — refit a minimally-adjusted model containing only exposure and game count to check sensitivity to covariate adjustment
- `277-282, 283-287` [high] **linked x1** — refit a partially-adjusted model adding position and league to check incremental confounding control
- `299-300` [high] **linked x2** — declare the hypothesis 'supported' only when the p-value is below 0.05 and the CI lower bound exceeds zero
- `341` [medium] **linked x2** — compute a relative percentage increase in red-card probability by dividing the absolute risk difference by the light-skin baseline probability
