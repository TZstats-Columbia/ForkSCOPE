# 2025-11-22T09-40-01+0000  (ai)

- code: 419 lines, 40% exon (169 lines in 16 decisions)
- intron: print 124, plot 54, comment 50, import 10, glue 7, config 5
- prose: 341 lines, 141 claims (40 action, 101 result)
- links: 105 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 4
- result_claims_deferred: 101

## Silent decisions — executed, never disclosed

- **280-285** [high] exclude goalkeepers from the sample and refit the primary model as a sensitivity check

## All decisions

- `34-35` [high] **linked x3** — load the raw soccer dyad dataset from CSV as the source and scope of the whole analysis
- `38-39` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `40-46` [low] **linked x1** — check inter-rater reliability by dropping incomplete rating pairs and computing correlation and exact-agreement rate
- `47-55` [high] **linked x6** — collapse continuous skin tone into light (<=0.25) vs dark (>=0.5) groups, dropping the middle band as unclassified, and encode a binary dark-skin flag
- `56-58` [high] **linked x2** — define the outcome as any red card occurring in a dyad, binarizing the red card count
- `59-75` [high] **linked x2** — collapse twelve detailed field positions into four broad position categories
- `76-81` [high] **linked x8** — restrict the analysis sample to complete cases having both a skin tone rating and a position
- `97-103` [medium] **linked x5** — compute red-card rate and cards-per-100-games normalized by skin tone group
- `120-127` [high] **linked x25** — specify and fit the primary logistic regression of any_red on dark_skin adjusting for games, position, and league, with standard errors clustered by player
- `143-145` [medium] **linked x5** — re-express the log-odds coefficient and its CI as an odds ratio for reporting
- `157-164, 168-170` [high] **linked x9** — estimate the average marginal effect (risk difference) via counterfactual predictions setting dark_skin to 1 vs 0 for every dyad, and derive group-specific baseline risks
- `184-188, 191-213, 221-222` [high] **linked x24** — estimate a bootstrap CI and p-value for the risk difference by resampling players (clusters) with replacement 1000 times, refitting the model each time, and taking the 2.5/97.5 percentiles of the resulting AME distribution
- `261-274` [high] **linked x4** — recode skin tone into a 3-level ordinal variable (light/medium/dark) with the same cut points and refit the model as a sensitivity check
- `280-285` [high] **SILENT** — exclude goalkeepers from the sample and refit the primary model as a sensitivity check
- `292-301` [high] **linked x2** — restrict to the most extreme skin-tone contrast (<=0.125 vs >=0.875) and refit the model as a sensitivity check
- `379-412` [medium] **linked x8** — state the interpretive conclusion that the hypothesis is supported with caveats, weighing the bootstrap CI/p-value against the marginally non-significant Wald p-value and listing robustness findings and limitations
