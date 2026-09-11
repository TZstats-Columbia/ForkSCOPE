# 2025-11-20T07-33-53+0000  (ai)

- code: 386 lines, 22% exon (86 lines in 16 decisions)
- intron: print 135, comment 77, glue 75, import 9, config 4
- prose: 301 lines, 113 claims (46 action, 67 result)
- links: 56 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 3
- result_claims_deferred: 67

## Silent decisions — executed, never disclosed

- **208-209** [low] silently drop bootstrap iterations whose model fit throws an exception, excluding them from the CI

## All decisions

- `32` [medium] **linked x2** — load the full soccer referee-player dyad dataset as the analysis population, with no pre-filtering of rows or columns
- `37` [high] **linked x2** — average the two raters' scores into a single continuous skin_tone measure
- `40` [high] **linked x3** — exclude dyads with a missing skin_tone rating from the analysis sample
- `44, 110` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome per dyad
- `47` [high] **linked x6** — dichotomize continuous skin_tone at a 0.5 cutoff into dark vs. light skin groups
- `69-70` [low] **linked x1** — compute the raw (unadjusted) difference in red-card rate between dark- and light-skin groups as a descriptive comparison
- `83` [high] **linked x3** — one-hot encode position and leagueCountry, dropping the first category as reference level
- `86-90` [high] **linked x1** — impute missing height and weight values with each column's median
- `93-95, 109, 163` [medium] **linked x7** — select the confounders to adjust for (games, yellow cards, height, weight, position dummies, league dummies) and use that list plus the exposure to build the model design matrices
- `121-123, 194-195` [high] **linked x5** — specify the outcome model as a binomial GLM (logistic regression) and, for the primary fit, cluster standard errors by player
- `137-146, 198-205` [high] **linked x7** — define the primary effect as the average predicted-probability difference between counterfactually setting dark_skin to 1 vs 0 for every dyad
- `172-173, 176, 187-188, 215-218` [high] **linked x6** — build a percentile confidence interval and normal-approximation p-value for the risk difference via a 200-iteration bootstrap that resamples players with replacement (cluster bootstrap)
- `208-209` [low] **SILENT** — silently drop bootstrap iterations whose model fit throws an exception, excluding them from the CI
- `237-244` [high] **linked x4** — exponentiate the dark_skin coefficient and its confidence interval to report an adjusted odds ratio as a secondary estimand
- `282, 286, 288-289, 291-294` [high] **linked x4** — refit the outcome model using continuous skin_tone in place of the binary dark_skin threshold, as a robustness/sensitivity check on how exposure is operationalized
- `309-325` [high] **linked x3** — classify the hypothesis as SUPPORTED only if the bootstrap p-value is below 0.05 and the CI lower bound exceeds zero, otherwise NOT SUPPORTED/inconclusive
