# 2025-11-26T17-05-19+0000  (ai)

- code: 348 lines, 38% exon (131 lines in 17 decisions)
- intron: print 139, comment 50, glue 16, import 7, config 5
- prose: 260 lines, 78 claims (45 action, 33 result)
- links: 56 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 7
- result_claims_deferred: 33

## All decisions

- `33-34` [high] **linked x2** — read the raw player-referee dyad CSV as the full, unfiltered analysis input
- `47-49, 51` [high] **linked x2** — drop dyads missing either rater's skin-tone score
- `52-55` [high] **linked x1** — average the two raters into a single continuous skin_tone consensus score
- `56-59, 61` [high] **linked x1** — drop dyads missing height or weight, treating them as required confounder controls
- `73-74` [high] **linked x2** — collapse red-card count into a binary any-red-card outcome
- `77-80, 85-90` [high] **linked x5** — dichotomize skin tone by keeping only bottom/top quartiles and flagging the top quartile as 'dark', discarding the middle
- `128-137` [high] **linked x13** — specify the primary logistic model's covariate/adjustment set and fit it with HC3 robust standard errors
- `154-162, 179-183, 184-189, 195-200` [high] **linked x1** — choose a reference covariate profile (sample means for continuous vars, modal position/league) to hold fixed when generating standardized predictions
- `190-194, 205-211` [high] **linked x4** — predict outcome probability at the reference profile with exposure fixed at light vs dark and take the difference as the risk difference
- `212-231` [high] **linked x3** — quantify uncertainty in the risk difference via parametric bootstrap draws from the model's coefficient covariance, using 10,000 simulations
- `232-234` [high] **linked x3** — derive a two-sided p-value as twice the smaller tail proportion of bootstrap draws relative to zero
- `254-257` [high] **linked x3** — convert the dark coefficient to an odds ratio with a Wald-type (1.96 SE) 95% confidence interval
- `272, 274-277` [high] **linked x2** — refit the primary model with yellowCards dropped from the covariate set to test sensitivity to that adjustment
- `280-281, 283-285` [high] **linked x3** — refit on the full (non-quartile-restricted) sample using a fixed 0.5 midpoint to dichotomize skin tone instead of quartiles
- `289-290, 292-296` [high] **linked x3** — refit using a more extreme dark/light cutoff (>=0.75 vs <=0.25) instead of the quartile-based split
- `300-301, 303-306` [high] **linked x3** — refit treating skin tone as a continuous predictor rather than dichotomizing it
- `337-342` [medium] **linked x5** — declare the hypothesis 'supported' and characterize the risk difference as substantively meaningful, going beyond restating the computed numbers
