# 2025-11-15T02-22-25+0000  (ai)

- code: 391 lines, 22% exon (87 lines in 25 decisions)
- intron: comment 103, print 87, plot 71, glue 31, import 8, config 4
- prose: 222 lines, 84 claims (44 action, 40 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: 4
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 13
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **43** [high] collapse the red-card count into a binary any-red-card outcome
- **209-210** [medium] discard a bootstrap replicate if it has fewer than 1000 dyads or fewer than 10 red-card events
- **222** [low] cap bootstrap model fitting at 50 iterations and suppress convergence warnings
- **235-236** [medium] silently drop any bootstrap replicate whose fit raises an exception

## All decisions

- `37` [high] **linked x1** — load the raw player-referee dyad dataset from a fixed CSV path
- `41` [high] **linked x2** — drop dyads where either skin-tone rater score is missing
- `42` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `43` [high] **SILENT** — collapse the red-card count into a binary any-red-card outcome
- `51-54, 96` [high] **linked x3** — bin the continuous skin-tone score into light/medium/dark at 0.25 and 0.75, then derive a binary dark-skin indicator from that binning
- `57` [high] **linked x2** — restrict the primary analytic sample to light and dark categories, dropping medium
- `67-80, 99` [medium] **linked x1** — collapse free-text position strings into a small set of position groups via keyword matching, then apply that mapping to the data
- `83-87` [high] **linked x3** — further restrict to complete cases with non-missing position, height, and weight
- `102` [medium] **linked x1** — log-transform the games-played count to address skew
- `103-104` [medium] **linked x2** — z-score standardize height and weight
- `107` [high] **linked x2** — one-hot encode position category and league country, dropping the first level as reference
- `116-120` [medium] **linked x2** — report unadjusted red-card rate and count by dark-skin group as the headline descriptive comparison
- `124-127` [low] **linked x1** — check position-category balance across skin-tone groups as a reported diagnostic
- `137-139, 141, 214` [high] **linked x8** — choose the covariate/adjustment set for the regression and apply it to both the main model matrix and each bootstrap replicate
- `148, 152-154` [high] **linked x4** — use cluster-robust standard errors grouped by player to account for repeated dyads per player
- `151, 221` [high] **linked x3** — choose logistic regression as the outcome model for both the main fit and every bootstrap replicate
- `166-168, 171-173, 176-178, 225-231, 233` [high] **linked x7** — estimate the adjusted risk difference via marginal standardization/g-computation, setting the whole sample to dark then to light and averaging predicted probabilities, repeated identically inside the bootstrap loop
- `191` [low] **linked x2** — fix the number of bootstrap resamples at 500
- `195-196, 203, 206` [high] **linked x1** — resample at the player level (with replacement) rather than the dyad level to preserve clustering in the bootstrap
- `209-210` [medium] **SILENT** — discard a bootstrap replicate if it has fewer than 1000 dyads or fewer than 10 red-card events
- `222` [low] **SILENT** — cap bootstrap model fitting at 50 iterations and suppress convergence warnings
- `235-236` [medium] **SILENT** — silently drop any bootstrap replicate whose fit raises an exception
- `242-243` [high] **linked x2** — build the 95% CI for the risk difference from the 2.5/97.5 percentiles of the bootstrap distribution
- `246` [high] **linked x1** — derive a two-sided p-value from the proportion of bootstrap replicates crossing zero
- `259-261` [medium] **linked x4** — report the secondary effect estimate on the odds-ratio scale by exponentiating the coefficient and its CI
