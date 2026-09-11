# 2025-11-22T06-59-05+0000  (ai)

- code: 337 lines, 34% exon (115 lines in 17 decisions)
- intron: print 137, comment 46, glue 29, import 8, config 2
- prose: 251 lines, 117 claims (52 action, 65 result)
- links: 58 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 10
- result_claims_deferred: 65

## Silent decisions — executed, never disclosed

- **102-107** [high] choose which columns carry forward into the modeling dataset

## All decisions

- `33-34` [high] **linked x2** — read the raw player-referee dyad CSV as the analysis starting point
- `39-40` [high] **linked x1** — average the two independent raters' skin-tone ratings into a single continuous score
- `41-43` [high] **linked x3** — drop dyads lacking a skin-tone score before any further analysis
- `45-47` [high] **linked x3** — collapse the red-card count into a yes/no indicator of any red card
- `56-64` [high] **linked x2** — cut continuous skin tone into three named bands (Light up to 0.25, Medium 0.25-0.5, Dark above 0.5)
- `65-68` [high] **linked x2** — drop the Medium band and treat only Light vs Dark as the exposure contrast
- `102-107` [high] **SILENT** — choose which columns carry forward into the modeling dataset
- `108-112` [high] **linked x4** — drop dyads with any missing covariate via listwise deletion
- `131-138` [high] **linked x11** — specify which covariates enter the primary regression (games, position, league, height, weight, referee bias measures)
- `139-140, 143, 228, 231, 254, 257, 280, 283` [high] **linked x3** — model the binary red-card outcome with a linear probability model (OLS) rather than a nonlinear binary model, reused for every sensitivity variant
- `141-142, 187-188, 229-230, 255-256, 281-282` [high] **linked x1** — cluster standard errors by player to account for repeated dyads per player, applied to every fitted model
- `149-150, 199-200, 236-237, 262-263, 288-289` [high] **linked x5** — build 95% confidence intervals as point estimate plus or minus 1.96 times the standard error (normal approximation), used for every estimate reported
- `157, 207, 310, 316, 319-332` [high] **linked x5** — declare significance at p<0.05 and combine that with the sign of the estimate to decide whether the hypothesis is supported
- `184-186, 190` [high] **linked x5** — fit a separate logistic-regression model to get an odds-ratio estimate for the same contrast
- `221-222, 225-227` [high] **linked x2** — swap referee-level bias covariates for referee fixed effects as a robustness check
- `242-243, 246-253` [high] **linked x4** — rerun the model using continuous skin tone instead of the binary dark/light split, rebuilding the analytic sample for it
- `270-271, 275-279` [high] **linked x5** — refit the primary model separately within each of the four league countries
