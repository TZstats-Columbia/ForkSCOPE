# 2025-11-29T17-19-34+0000  (ai)

- code: 294 lines, 42% exon (123 lines in 16 decisions)
- intron: print 104, comment 42, other 14, import 6, config 5
- prose: 188 lines, 70 claims (41 action, 29 result)
- links: 57 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 11
- result_claims_deferred: 29

## Silent decisions — executed, never disclosed

- **39-41, 72, 186, 197** [high] define the outcome as a binary indicator for whether any red card was received, collapsing card count and ignoring yellow cards

## All decisions

- `33` [high] **linked x1** — load the full soccer referee-player dyad dataset from a fixed CSV path without any pre-filtering
- `36-38` [high] **linked x1** — average the two independent raters' skin-tone scores into a single composite skinTone measure
- `39-41, 72, 186, 197` [high] **SILENT** — define the outcome as a binary indicator for whether any red card was received, collapsing card count and ignoring yellow cards
- `52-53` [high] **linked x2** — drop dyads lacking a skin-tone rating (no player photo) before any further analysis
- `56-62` [high] **linked x2** — split skinTone into light (<=0.125), dark (>0.25) and middle groups using fixed, asymmetric cutoffs chosen to maximize contrast
- `68-71` [high] **linked x4** — discard the middle skin-tone group entirely and encode the remaining dark group as a binary exposure variable isDark
- `75-77` [high] **linked x3** — drop remaining dyads with missing player position before fitting any model
- `105-116` [high] **linked x7** — fit a logistic regression of the red-card outcome on skin-tone exposure, choosing log(games), position and league country as the adjustment set
- `128-131` [medium] **linked x3** — convert the primary model's exposure coefficient and confidence interval into an odds ratio for secondary reporting
- `136-147` [high] **linked x5** — estimate the adjusted risk difference by predicting every dyad's outcome under counterfactual isDark=0 and isDark=1 and averaging the difference (marginal standardization / G-computation)
- `148-157` [medium] **linked x6** — approximate the risk difference's standard error, 95% CI and two-sided p-value with a simple binomial-variance formula and normal approximation rather than a model-based method
- `164-171` [high] **linked x4** — refit the primary model adding yellow-card count as an extra covariate to probe robustness
- `172-180` [high] **linked x3** — restrict to dyads with known height and weight and refit the model including those physical covariates
- `181-185, 187-192` [high] **linked x4** — recompute exposure using a single median-split threshold (skinTone>0.25) on the full non-middle-excluded sample instead of the three-way cutoff, as an alternative categorization
- `193-196, 198-203` [high] **linked x4** — model skin tone as a continuous predictor rescaled by 10 instead of a binary exposure, and report the effect over the full range
- `269-289` [medium] **linked x8** — declare the hypothesis 'SUPPORTED' and frame the risk-difference effect as statistically significant, substantively meaningful, and robust across specifications
