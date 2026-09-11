# 2025-11-29T06-09-11+0000  (ai)

- code: 243 lines, 49% exon (120 lines in 21 decisions)
- intron: glue 57, print 52, import 9, config 5
- prose: 278 lines, 108 claims (60 action, 48 result)
- links: 42 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 20
- R_only_consistent_negative: 13
- result_claims_deferred: 48

## Silent decisions — executed, never disclosed

- **74-75** [high] derive a numeric player identifier to serve as the clustering unit for standard errors

## All decisions

- `21` [high] **linked x1** — pick the input dataset/file to load as the analysis source
- `23-24` [high] **linked x1** — combine the two raters' skin tone ratings into a single average score
- `26-27` [high] **linked x1** — collapse the red card count into a binary any-red-card indicator
- `29-31` [high] **linked x2** — exclude dyads with missing skin tone rating from the analysis sample rather than imputing them
- `41-44, 183-184` [high] **linked x2** — choose the cutpoint(s) used to dichotomize continuous skin tone into a dark/light category, including the primary 0.25 cut and the alternate 0.5 cut used later as a sensitivity variant
- `57-59` [high] **linked x2** — impute missing height values with the sample median
- `61-62` [high] **linked x2** — impute missing weight values with the sample median
- `64-65` [high] **linked x1** — recode missing player position as its own 'Unknown' category rather than dropping or imputing
- `67-69` [high] **linked x3** — impute missing referee implicit/explicit bias measures with their sample means
- `71-72` [high] **linked x1** — log-transform games played to use as an exposure/opportunity adjustment term
- `74-75` [high] **SILENT** — derive a numeric player identifier to serve as the clustering unit for standard errors
- `85-100` [high] **linked x9** — specify the primary model's covariate/adjustment set and functional form (position, log games, league country, referee bias measures, height, weight, goals, yellow cards) alongside the binary dark_skin exposure
- `105-111` [high] **linked x2** — fit the primary model as logistic regression with standard errors clustered by player to account for repeated dyads per player
- `117-121` [medium] **linked x1** — extract the coefficient, SE, p-value and CI for the exposure term as the primary reported statistics
- `128-130` [high] **linked x3** — convert the exposure coefficient into an adjusted odds ratio and its CI for reporting
- `136-139` [high] **linked x2** — compute an adjusted risk difference as a marginal-effect contrast between predicted probabilities at dark_skin=0 vs 1
- `145-167` [high] **linked x2** — derive a confidence interval for the risk difference via a numerical delta-method approximation instead of a closed-form or bootstrap approach
- `185-196` [high] **linked x2** — refit the primary adjusted model using the alternate 0.5 threshold exposure as a sensitivity check and recompute its OR/RD/p-value
- `203-210` [high] **linked x1** — fit an unadjusted logistic model dropping all covariates to check the exposure effect without adjustment
- `216-226` [high] **linked x1** — refit the adjusted model using continuous (undichotomized) skin tone as the exposure instead of a binary cut
- `240-242` [medium] **linked x3** — declare the hypothesis 'SUPPORTED' and frame the primary risk-difference estimate as a directional conclusion in the final printed statement
