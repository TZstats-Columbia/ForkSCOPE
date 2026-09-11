# 2025-11-16T23-15-36+0000  (ai)

- code: 419 lines, 38% exon (158 lines in 15 decisions)
- intron: print 123, comment 52, plot 52, glue 21, import 9, config 4
- prose: 214 lines, 91 claims (36 action, 55 result)
- links: 49 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 11
- result_claims_deferred: 55

## Silent decisions — executed, never disclosed

- **337-345** [low] hardcode the point estimates and confidence intervals for four of the six specifications as literal numbers in the plotting code rather than reading them from the result objects fitted earlier

## All decisions

- `34-36` [high] **linked x1** — load the full soccer.csv referee-player dataset as the analysis universe
- `39-41` [high] **linked x1** — average the two raters' skin-tone ratings into a single continuous skinTone_avg score
- `42-44` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome (redCards>0)
- `47-49` [high] **linked x4** — restrict the sample to complete cases with non-missing skin-tone rating and position
- `61-63, 67-88, 91-94, 97-99, 229-230` [high] **linked x6** — search over six candidate skin-tone cutoffs, pick the one that maximizes the unadjusted z-statistic for the red-card-rate difference, and use that cutoff to define/redefine the binary dark/light exposure
- `108-114` [medium] **linked x2** — z-score standardize the continuous covariates and impute missing standardized values to 0 (the sample mean)
- `117-120` [high] **linked x1** — one-hot encode position and league country, dropping the first category as reference group
- `139-145, 149-151` [high] **linked x6** — specify the primary model as a linear probability model of anyRedCard on dark plus games/position/league covariates, fit by OLS with HC3 robust standard errors
- `175-177` [high] **linked x4** — fit a secondary logistic regression on the same covariate set to obtain an odds-ratio estimate
- `207-219` [high] **linked x8** — refit the adjusted model separately at each candidate threshold to check sensitivity of the risk difference to the cutoff choice
- `231-252` [high] **linked x6** — refit the model under five alternative covariate-adjustment sets (minimal, +position, +league, +height/weight, +yellow cards) to check robustness of the dark effect
- `259-269` [high] **linked x3** — refit the model treating skin tone as a continuous exposure instead of the dichotomized dark/light variable
- `277-292` [high] **linked x3** — compute an unadjusted (no-covariate) risk difference with its own manual z-test/CI directly from dark/light group means
- `337-345` [low] **SILENT** — hardcode the point estimates and confidence intervals for four of the six specifications as literal numbers in the plotting code rather than reading them from the result objects fitted earlier
- `398-414` [high] **linked x3** — classify the result into SUPPORTED / CONTRADICTORY / INCONCLUSIVE / NOT SUPPORTED using the rule p<0.05 combined with the sign of the CI/point estimate, and print the corresponding narrative
