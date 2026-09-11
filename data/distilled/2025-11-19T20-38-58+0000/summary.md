# 2025-11-19T20-38-58+0000  (ai)

- code: 312 lines, 22% exon (70 lines in 16 decisions)
- intron: print 142, comment 49, glue 41, import 10
- prose: 315 lines, 112 claims (58 action, 54 result)
- links: 62 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 12
- result_claims_deferred: 54

## Silent decisions — executed, never disclosed

- **67-70** [medium] choose which identifiers, outcome and candidate covariates are carried into the modeling dataset

## All decisions

- `31` [medium] **linked x2** — load the raw player-referee dyad dataset that defines the study population
- `41` [high] **linked x2** — average the two independent raters' skin-tone scores into a single continuous exposure measure
- `47-50, 57` [high] **linked x4** — cut the continuous skin-tone score into light/medium/dark bands at 0.25 and 0.75 and recode into a binary dark-skin exposure flag
- `53` [high] **linked x3** — collapse the red-card count into a binary any-red-card outcome
- `56` [high] **linked x2** — restrict the analysis sample to light and dark tones only, discarding medium-tone dyads
- `67-70` [medium] **SILENT** — choose which identifiers, outcome and candidate covariates are carried into the modeling dataset
- `73` [high] **linked x7** — drop dyads with missing covariate values, restricting to complete cases
- `76` [high] **linked x3** — log-transform the games-played count before using it as a covariate
- `90-96, 110, 112-114, 117-119, 122-123` [high] **linked x1** — estimate the unadjusted risk difference between dark- and light-skin groups with a normal-approximation z-test and Wald CI instead of an exact or resampling-based method
- `140-143` [high] **linked x9** — build the regression design matrix by dummy-coding categorical covariates with the first level dropped
- `146, 153, 191, 229, 241` [high] **linked x6** — cluster standard errors by player in every fitted model rather than treating dyads as independent
- `152, 156-160` [high] **linked x9** — model the binary outcome with a linear probability model to get a directly interpretable adjusted risk difference
- `190, 194-198, 201-203` [high] **linked x5** — fit a secondary logistic model on the same covariates and re-express the darkSkin effect as an odds ratio
- `224-228` [high] **linked x3** — refit the risk-difference model with the referee bias measures dropped, as an alternative adjustment set
- `237-240` [high] **linked x3** — refit with a bare-minimum adjustment set of only position and games as a further robustness check
- `256-261` [high] **linked x3** — compute the minimum detectable effect at a chosen 80% power and 0.05 two-sided alpha for the observed group sizes
