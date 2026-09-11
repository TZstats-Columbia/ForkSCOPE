# 2025-11-20T20-40-17+0000  (ai)

- code: 267 lines, 31% exon (84 lines in 16 decisions)
- intron: print 90, comment 53, glue 27, import 12, config 1
- prose: 352 lines, 143 claims (55 action, 88 result)
- links: 56 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 14
- result_claims_deferred: 88

## Silent decisions — executed, never disclosed

- **235-243** [low] curate which three estimates (primary risk difference, referee-clustered risk difference, odds ratio) get featured in the final summary table, leaving the continuous-exposure result out

## All decisions

- `30-31` [high] **linked x2** — load the raw player-referee dyad dataset from the source CSV
- `37-39` [high] **linked x1** — drop dyads that lack a skin-tone rating from either rater
- `41-43` [high] **linked x2** — combine the two raters' scores into a single average skin-tone measure
- `52-58` [high] **linked x5** — collapse skin tone into light vs dark groups at the 0.25/0.5 cutoffs and throw out the ambiguous middle band
- `59, 195` [high] **linked x1** — define the outcome as ever receiving a red card, ignoring how many
- `73-77` [high] **linked x5** — split the sample by skin-tone group and compute raw, unadjusted red-card rates for each
- `87-88` [high] **linked x3** — keep only rows with non-missing position, height and weight (complete-case deletion)
- `94-98, 196-198` [high] **linked x1** — rescale height, weight and games played onto a standardized (z-score) scale
- `99-104, 199-203` [high] **linked x1** — turn position and league into dummy indicators, dropping one category as reference
- `105-111` [high] **linked x7** — pick which variables enter the adjustment set and stack them into the model design matrix
- `124-126` [high] **linked x11** — choose a linear probability model with player-clustered standard errors as the primary estimator
- `135, 164, 184, 244-246, 258` [high] **linked x3** — call a result 'statistically significant' using a 0.05 p-value cutoff
- `152-155` [high] **linked x3** — refit the same adjustment set with logistic regression to get an odds ratio instead of a risk difference
- `174-175` [high] **linked x6** — recompute standard errors clustering on referee instead of player as a robustness check
- `194, 204-209, 213-214` [high] **linked x5** — rerun the model on the full (non-thresholded) sample using continuous skin tone as the exposure instead of the binary split
- `235-243` [low] **SILENT** — curate which three estimates (primary risk difference, referee-clustered risk difference, odds ratio) get featured in the final summary table, leaving the continuous-exposure result out
