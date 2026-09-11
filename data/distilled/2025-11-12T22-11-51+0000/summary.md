# 2025-11-12T22-11-51+0000  (ai)

- code: 318 lines, 44% exon (141 lines in 20 decisions)
- intron: print 107, comment 54, import 10, glue 5, config 1
- prose: 268 lines, 82 claims (29 action, 53 result)
- links: 68 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 3
- R_only_consistent_negative: 3
- result_claims_deferred: 53

## All decisions

- `34-36` [high] **linked x3** — load the player-referee dyad dataset from soccer.csv as the analysis population
- `47-49` [high] **linked x1** — average the two raters' skin-tone codings into a single continuous skin-tone score
- `50-54` [low] **linked x1** — assess inter-rater agreement on skin tone via correlation and exact-match rate rather than adjudicating or discarding disagreements
- `59-62` [high] **linked x3** — dichotomize the skin-tone score at the 0.5 midpoint to define dark vs light exposure groups
- `63-65` [high] **linked x2** — collapse red-card counts into a binary any-red-card outcome rather than modeling counts or severity
- `77-84` [high] **linked x2** — restrict the analytic sample to complete cases on the outcome, exposure, and chosen covariate list, dropping rows missing any of them
- `100-104` [medium] **linked x4** — compute the unadjusted red-card rate difference and relative risk by skin-tone group as the baseline comparison
- `115-121` [high] **linked x5** — z-score standardize the continuous covariates before entering them in the model
- `122-124` [medium] **linked x2** — encode player position and league as categorical fixed effects rather than continuous or omitted variables
- `133-136` [high] **linked x7** — fix the adjustment covariate set (games, height, weight, implicit-bias score, experience, position, league) for the primary regression
- `137-142, 194-198, 243-246, 267-271` [high] **linked x3** — fit a logistic regression via smf.logit with standard errors clustered on player identity
- `153-157, 204-206, 230-233` [high] **linked x2** — exponentiate the model coefficient to obtain an adjusted odds ratio with a Wald 95% CI on the coefficient scale
- `163-171, 199-203, 221-225, 247-250, 284-287` [high] **linked x6** — use the average marginal effect of the exposure as the risk-difference estimator, with a normal-approximation 95% CI
- `185-193` [high] **linked x6** — redefine exposure as very-dark vs very-light at 0.75/0.25 and drop the middle skin-tone group for this sensitivity check
- `214-217, 226-229` [high] **linked x5** — re-specify skin tone as a continuous exposure and rescale the resulting effect to a 0.25-unit change for interpretability
- `218-220` [medium] **linked x1** — swap the variance estimator to heteroskedasticity-robust (HC1) instead of player-clustered for the continuous-exposure model
- `240-242` [high] **linked x1** — specify an unadjusted single-predictor model as a formal comparator to the adjusted estimate
- `263-266, 272-273` [high] **linked x5** — add a dark_skin by implicit-bias interaction term to test whether referee bias moderates the skin-tone effect
- `278-283` [high] **linked x5** — recompute standard errors clustered by referee instead of by player as an alternative dependence structure
- `301-302` [high] **linked x4** — declare the hypothesis 'not supported' whenever the primary p-value exceeds 0.05 or the risk-difference CI crosses zero, else 'supported'
