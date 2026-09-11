# 2025-11-29T11-47-15+0000  (ai)

- code: 331 lines, 37% exon (121 lines in 21 decisions)
- intron: print 100, plot 55, comment 39, import 9, config 4, glue 3
- prose: 266 lines, 77 claims (40 action, 37 result)
- links: 56 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 7
- result_claims_deferred: 37

## Silent decisions — executed, never disclosed

- **32** [high] load the match/dyad dataset from a single fixed CSV file path
- **52-53** [high] derive player age by subtracting birth year from a fixed reference year (2013)

## All decisions

- `32` [high] **SILENT** — load the match/dyad dataset from a single fixed CSV file path
- `35-36` [high] **linked x2** — average the two raters' ratings into one continuous skin-tone score
- `37-39` [high] **linked x1** — collapse the red-card count into a binary any-red-card indicator
- `40-42` [high] **linked x3** — drop dyads with no skin-tone rating (missing player photo)
- `52-53` [high] **SILENT** — derive player age by subtracting birth year from a fixed reference year (2013)
- `54-55, 164-168` [high] **linked x1** — create a log-transformed games-played covariate and substitute it for the linear term in a sensitivity model
- `56-60` [medium] **linked x1** — z-score standardize height, weight, and age
- `61-64` [high] **linked x1** — threshold skin-tone rating at 0.75 to define a binary dark-skin exposure indicator
- `65-67` [high] **linked x4** — restrict the analysis sample to the two extreme skin-tone groups, dropping intermediate ratings
- `70-74` [high] **linked x4** — exclude goalkeepers from the primary analysis sample
- `75-78` [high] **linked x1** — restrict the primary sample to rows with complete data on the outcome, exposure, and covariates
- `93-106` [high] **linked x13** — fit a linear-probability model of red cards on skin tone adjusting for games and position with HC3 robust errors, and convert the exposure coefficient into a percentage-point effect with CI and two-sided p-value
- `107-111` [high] **linked x2** — compute a one-sided p-value testing the directional hypothesis that dark-skinned players receive more red cards
- `128-137` [high] **linked x4** — fit a logistic regression of the same specification and convert the exposure coefficient into an odds ratio with a normal-approximation confidence interval
- `151-157` [high] **linked x2** — refit the primary model on a sample that keeps goalkeepers in
- `175-186` [high] **linked x1** — redefine the light/dark skin-tone cutoffs (0-0.25 vs 0.75-1.0) and refit the model on this alternative sample
- `193-198` [high] **linked x4** — refit the primary model with standard errors clustered by player
- `205-210` [high] **linked x4** — refit the primary model with standard errors clustered by referee
- `226-227` [high] **linked x2** — compute unadjusted red-card rates for the light and dark groups
- `233` [high] **linked x3** — scale the adjusted effect as a percentage of the light-group baseline rate
- `308-326` [high] **linked x3** — convert the primary model's p-value and effect direction into a categorical supported/not-supported verdict with narrative framing of the finding
