# 2025-11-12T11-24-34+0000  (ai)

- code: 316 lines, 27% exon (85 lines in 18 decisions)
- intron: print 126, comment 82, glue 13, import 9, config 1
- prose: 279 lines, 113 claims (48 action, 65 result)
- links: 65 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 6
- result_claims_deferred: 65

## All decisions

- `27` [high] **linked x4** — read in the raw player-referee dyad table as the analysis population
- `33` [high] **linked x3** — drop dyads lacking a skin-tone rating from either coder before any further work
- `38-39` [medium] **linked x2** — quantify how well the two coders agree using both a Pearson and a Spearman coefficient
- `44` [high] **linked x2** — collapse the two raters' scores into one skin_tone value by simple averaging
- `52-54, 56` [high] **linked x6** — split skin tone into dark (>0.5) vs light (<=0.25) groups and discard the middle band entirely
- `62` [high] **linked x2** — turn the red-card count into a yes/no indicator of ever receiving one
- `69-75` [high] **linked x2** — restrict to complete cases on the confounders that will enter the model
- `81-82, 149-150, 152, 155-156` [high] **linked x4** — treat position and league as categorical factors and fit the fully-adjusted logistic model on the dark/light exposure
- `85-89` [high] **linked x6** — rescale each continuous covariate to a z-score before it enters the model
- `108-110, 122, 127-130, 132-135` [high] **linked x4** — get the unadjusted association from a 2x2 table: risk difference plus a hand-computed odds ratio with Wald CI
- `153-154, 211-212, 224-225, 237-238` [high] **linked x4** — obtain standard errors clustered by player rather than treating dyads as independent
- `170-172` [high] **linked x6** — designate the average-marginal-effect risk difference as the headline result
- `189-191` [high] **linked x2** — exponentiate the model coefficient into an adjusted odds ratio as a second-tier result
- `207-210, 213-214` [high] **linked x5** — re-run the model treating skin tone as continuous rather than dichotomized, as a robustness check
- `221-223, 226-227` [high] **linked x2** — refit the model with position removed from the adjustment set to check its influence
- `234, 236, 239-240` [high] **linked x2** — limit the sample to dyads with at least two games and refit the primary model on that subset
- `253-256, 258-261` [medium] **linked x3** — fix the power/alpha assumptions (80% power, two-sided 0.05) used to back out a minimum detectable effect
- `304-310` [high] **linked x6** — weigh the effect size against the MDE and p-value and declare the hypothesis unsupported
