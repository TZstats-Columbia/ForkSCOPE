# 2025-11-22T05-51-21+0000  (ai)

- code: 396 lines, 32% exon (127 lines in 20 decisions)
- intron: print 136, plot 61, comment 58, import 9, config 3, glue 2
- prose: 274 lines, 93 claims (36 action, 57 result)
- links: 56 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 2
- result_claims_deferred: 57

## All decisions

- `28-29` [high] **linked x2** — pick the input dataset and load it wholesale as the analysis universe
- `37-38` [high] **linked x1** — collapse two raters' independent skin-tone codings into a single score by averaging
- `39-41` [high] **linked x2** — drop dyads lacking a skin tone rating rather than imputing
- `45-46` [high] **linked x3** — collapse red card counts into a binary any-red-card outcome
- `47-53, 59-61` [high] **linked x6** — split the continuous skin-tone score at fixed cutoffs (<=0.125 light, >=0.75 dark), discard the middle range, and recode into a light/dark binary exposure
- `69-86` [high] **linked x1** — bucket free-text player positions into five categories via keyword matching
- `87-89` [high] **linked x2** — restrict to complete cases on height and weight, dropping the rest
- `103-109` [low] **linked x1** — choose which variables and summary statistics characterize each skin-tone group
- `120-126` [high] **linked x1** — compute the crude (unadjusted) percentage-point gap in red-card rate between dark and light skin groups
- `135-136` [medium] **linked x1** — test the crude group difference with a two-proportion z-test
- `147-150` [high] **linked x1** — z-standardize the continuous covariates before entering them in the model
- `151-157` [high] **linked x1** — dummy-code player position with Goalkeeper held out as the reference level
- `158-162` [high] **linked x1** — dummy-code league country with Germany held out as the reference level
- `164-168` [high] **linked x5** — settle on the covariate set (games, position, league, height, weight) that adjusts the primary model
- `169-172, 258-261, 272-275` [high] **linked x5** — fit a logistic regression with standard errors clustered by player rather than treating dyads as independent
- `200-219` [high] **linked x10** — re-derive the model via an explicit design matrix and report the primary effect as an average marginal effect (risk-difference scale) rather than a log-odds coefficient
- `236-238` [high] **linked x6** — report a secondary effect size as an odds ratio by exponentiating the model coefficient
- `253, 255-257` [high] **linked x1** — re-specify the model dropping height/weight to check sensitivity to physical covariates
- `266-271` [high] **linked x1** — add standardized yellow-card count as an extra adjustment covariate for a second sensitivity model
- `360-364` [high] **linked x5** — declare the hypothesis supported using a specific rule: two-sided p<0.05 and the marginal-effect CI lower bound above zero
