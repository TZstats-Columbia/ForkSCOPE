# 2025-11-17T15-56-59+0000  (ai)

- code: 324 lines, 25% exon (82 lines in 18 decisions)
- intron: comment 88, print 79, plot 52, glue 10, import 8, config 5
- prose: 320 lines, 133 claims (51 action, 82 result)
- links: 79 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 7
- result_claims_deferred: 82

## Silent decisions — executed, never disclosed

- **45-46** [high] derive player age by anchoring to a fixed reference year (2012) rather than to game date or current date
- **53-56** [high] pick which columns enter the modeling dataset, fixing the covariate and identifier set for everything downstream

## All decisions

- `27` [high] **linked x1** — load the raw referee-player dyad dataset from CSV as the full source population for the analysis
- `31` [high] **linked x2** — drop dyads lacking both skin-tone rater scores, restricting the sample to rated players only
- `35` [high] **linked x1** — collapse the two raters' scores into a single continuous skin-tone measure by averaging them
- `38` [high] **linked x1** — reduce the red-card count to a binary any/none outcome for the dyad
- `41, 277` [high] **linked x1** — split the continuous skin-tone score into dark/light groups at a 0.5 cutoff, and mark that same cutoff on the ratings plot
- `45-46` [high] **SILENT** — derive player age by anchoring to a fixed reference year (2012) rather than to game date or current date
- `53-56` [high] **SILENT** — pick which columns enter the modeling dataset, fixing the covariate and identifier set for everything downstream
- `59` [high] **linked x4** — handle missing covariate data by complete-case deletion rather than imputation
- `65` [high] **linked x1** — log-transform games played instead of using the raw count
- `68-72` [high] **linked x1** — z-score the continuous covariates before entering them into the model
- `91-93` [high] **linked x5** — compute the raw, unadjusted rate gap between dark- and light-skinned groups as a descriptive baseline
- `109-112` [high] **linked x11** — choose logistic regression with skinDark plus position, playing time, age, height, weight and league as the main effect model
- `119-123` [high] **linked x9** — convert the skinDark coefficient to an odds ratio with a Wald-based 95% interval as the secondary effect measure
- `124, 134, 211, 216` [medium] **linked x3** — declare the adjusted risk difference as the primary estimand and the adjusted odds ratio as secondary, shaping how results are framed and reported
- `138-149, 177-184` [high] **linked x14** — estimate the adjusted risk difference by g-computation: set everyone's skin tone to light then dark, predict, and average the gap, repeating the same recipe inside each bootstrap resample
- `161-162, 169-171, 174, 185-186, 190-192, 195-196` [high] **linked x10** — quantify uncertainty by resampling dyads with replacement 200 times, refitting the model each time, and taking the empirical percentile interval and a normal-approximation p-value from the resulting bootstrap distribution
- `230-236` [high] **linked x7** — re-run the model dropping the position covariate to check robustness of the skin-tone effect
- `242-248` [high] **linked x8** — re-run the model adding yellow-card count as an extra covariate to check robustness of the skin-tone effect
