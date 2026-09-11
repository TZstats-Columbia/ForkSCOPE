# 2025-11-21T01-32-10+0000  (ai)

- code: 342 lines, 44% exon (150 lines in 17 decisions)
- intron: print 119, comment 55, import 9, config 5, glue 4
- prose: 288 lines, 117 claims (37 action, 80 result)
- links: 76 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 4
- result_claims_deferred: 80

## All decisions

- `33-34` [medium] **linked x3** — load the raw referee-player dyad dataset from a fixed CSV path
- `39` [high] **linked x2** — drop dyads that are missing either rater's skin-tone score
- `48-49` [high] **linked x1** — average the two raters' scores into one continuous skin_tone measure
- `50` [high] **linked x5** — dichotomize continuous skin tone into dark vs. light using a 0.5 cutoff
- `51-52` [high] **linked x3** — collapse red-card counts into a binary any-red-card outcome
- `65-71` [high] **linked x5** — restrict the sample to complete cases on position, height, weight, and mean IAT score
- `89-95` [high] **linked x1** — z-score standardize height, weight, games, meanIAT, and meanExp before modeling
- `104-115` [high] **linked x10** — assemble the model's covariate/adjustment set: skin_dark plus standardized covariates and one-hot position/league dummies (baseline dropped), with an intercept
- `125-126` [high] **linked x9** — choose logistic regression as the outcome model and fit it by maximum likelihood
- `137-162` [high] **linked x5** — estimate two-way (player and referee) clustered standard errors via the Cameron-Gelbach-Miller combination of one-way cluster and robust covariance matrices
- `163-171` [medium] **linked x4** — test and interval-estimate the skin_dark coefficient via a normal-approximation (Wald) z-test using the two-way clustered SE
- `178-182` [medium] **linked x4** — re-express the skin_dark coefficient and CI on the odds-ratio scale as a secondary estimand
- `198-212` [high] **linked x5** — compute the average marginal effect of skin_dark by predicting outcomes under all-dark and all-light counterfactuals and averaging the difference
- `224-227, 231-266, 269-271` [high] **linked x2** — cluster-bootstrap by resampling players with replacement 200 times, refitting the logistic model and recomputing the AME each iteration, silently discarding iterations that fail to fit
- `278-284` [medium] **linked x6** — derive the primary estimand's SE and 95% CI from the empirical bootstrap distribution via the percentile method, and test it with a normal z-statistic
- `302-308` [high] **linked x6** — declare the hypothesis supported or not using a 0.05 significance threshold on the bootstrap p-value
- `337-338` [low] **linked x5** — compute the raw unadjusted difference in red-card rates between dark and light skin groups as a descriptive comparison to the adjusted estimate
