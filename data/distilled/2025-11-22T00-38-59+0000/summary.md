# 2025-11-22T00-38-59+0000  (ai)

- code: 339 lines, 24% exon (82 lines in 19 decisions)
- intron: print 119, comment 92, plot 34, import 10, config 1, glue 1
- prose: 192 lines, 83 claims (43 action, 40 result)
- links: 59 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 11
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **65-67** [medium] compute the unadjusted red-card rate difference between dark- and light-skinned groups

## All decisions

- `29` [high] **linked x3** — load the raw player-referee dyad dataset from a fixed CSV path, setting the analysis's data source and scope
- `34` [high] **linked x1** — average the two raters' skin-tone ratings into a single continuous skin-tone score
- `37, 272` [high] **linked x3** — dichotomize skin tone at 0.50 into a binary dark/light exposure
- `40` [high] **linked x2** — define the outcome as receiving any red card at all in the dyad (binarize redCards)
- `43` [high] **linked x2** — exclude dyads with missing skin-tone data from the analysis sample
- `47` [high] **linked x5** — restrict to complete cases on position, height, and weight for the modeling sample
- `65-67` [medium] **SILENT** — compute the unadjusted red-card rate difference between dark- and light-skinned groups
- `83-85, 238-240` [medium] **linked x2** — standardize games/height/weight to z-scores before entering them as covariates, at both dyad and player level
- `91-92` [high] **linked x5** — specify the adjusted logistic regression model: darkSkin exposure plus games, position, league, height, weight as the covariate/adjustment set, fit by MLE
- `112-116, 119-120, 123-124` [high] **linked x4** — build dark/light counterfactual copies of the sample and average the model's predicted-probability contrast into an average marginal effect (adjusted risk difference)
- `127-128, 131-133, 136-137` [medium] **linked x3** — derive the standard error of the marginal effect via the delta method using the average predicted-probability derivative
- `140-141, 144-145` [medium] **linked x2** — form a 95% Wald confidence interval and a two-sided p-value for the marginal effect using a normal approximation
- `161-164` [high] **linked x3** — report the adjusted odds ratio (exponentiated coefficient) with its model-based Wald CI and p-value as a secondary estimand
- `179-183` [high] **linked x3** — redefine the exposure via a median split of skin tone and refit the adjusted model as a sensitivity check
- `191-197` [high] **linked x3** — restrict to the top and bottom skin-tone terciles, dropping the middle third, and refit the model comparing darkest vs lightest thirds
- `205-207, 210-211` [high] **linked x3** — treat skin tone as a continuous exposure in the model and rescale the reported effect to a per-0.1-unit odds ratio
- `223-232, 243-244, 245-249` [high] **linked x7** — collapse dyad rows to one row per player (max of ever-red-carded, first of demographic/exposure fields, sum of games) and refit the adjusted model at player level as a robustness check
- `268` [medium] **linked x1** — drop skin-tone bins with fewer than 50 observations before plotting rates by skin tone
- `330-334` [high] **linked x7** — interpret the dyad-level p=0.037 result as supporting the hypothesis overall, despite the effect not being significant at the player level
