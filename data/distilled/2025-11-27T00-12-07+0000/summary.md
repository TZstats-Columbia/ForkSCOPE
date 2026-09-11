# 2025-11-27T00-12-07+0000  (ai)

- code: 374 lines, 36% exon (133 lines in 17 decisions)
- intron: print 181, glue 36, comment 14, import 5, config 5
- prose: 244 lines, 115 claims (53 action, 62 result)
- links: 64 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 13
- result_claims_deferred: 62

## Silent decisions — executed, never disclosed

- **110-114** [low] compute and report the crude (unadjusted) red-card-rate gap between dark- and light-skinned groups alongside the later adjusted estimates

## All decisions

- `33-34` [high] **linked x3** — load the raw player-referee dyad dataset from a fixed CSV path with no initial filtering
- `37-38` [high] **linked x4** — exclude dyads with no skin-tone rating, keeping only rated cases as the analytic sample
- `49-50` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `53-56` [high] **linked x6** — dichotomize continuous skin tone into dark vs. light using a 0.25 cutoff
- `57-59` [high] **linked x3** — collapse red-card counts into a binary any-red-card outcome
- `60-62` [high] **linked x2** — add a squared games term to let playing-time exposure enter non-linearly
- `63-79` [high] **linked x1** — collapse detailed playing positions into five coarse categories (Forward/Defender/Midfielder/Goalkeeper/Other/Unknown) via custom string-matching rules and apply it to every player
- `80-82, 225, 227-238` [high] **linked x3** — re-derive the dark/light split at a stricter 0.375 cutoff, refit the model, and recompute the risk difference and odds ratio to test sensitivity to the threshold choice
- `110-114` [low] **SILENT** — compute and report the crude (unadjusted) red-card-rate gap between dark- and light-skinned groups alongside the later adjusted estimates
- `141-146` [high] **linked x12** — specify the primary model: logistic regression of any-red-card on the dark-skin indicator, adjusted for league, position, games (linear+quadratic), yellow cards and referee implicit-bias score, with HC1 robust standard errors
- `160-174` [high] **linked x7** — estimate the average marginal risk difference by scoring every dyad twice under counterfactual dark=1 and dark=0 and averaging the predicted-probability gap
- `175-183` [high] **linked x2** — approximate the standard error and confidence interval of the risk difference via a delta-method linearization around the mean predicted-probability weight
- `202-206` [high] **linked x5** — report the effect as an adjusted odds ratio by exponentiating the model coefficient and its confidence bounds
- `242-243, 245-256` [high] **linked x5** — refit using the raw continuous skin-tone score instead of a binarized threshold, and compute the implied full-range (lightest-to-darkest) risk difference and odds ratio
- `260-261, 263-274` [high] **linked x3** — refit the model dropping the referee implicit-bias covariate to test whether adjustment for meanIAT drives the result
- `278-279, 281-292` [high] **linked x4** — refit with conventional (non-robust) standard errors instead of HC1 to check sensitivity of inference to the variance estimator
- `354-355` [high] **linked x3** — declare the hypothesis 'supported' using a two-sided p<0.05 cutoff combined with a positive effect direction
