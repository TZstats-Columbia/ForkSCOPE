# 2025-11-19T10-27-52+0000  (ai)

- code: 466 lines, 30% exon (142 lines in 17 decisions)
- intron: print 131, comment 111, plot 59, other 11, import 8, config 4
- prose: 297 lines, 78 claims (34 action, 44 result)
- links: 52 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 9
- result_claims_deferred: 44

## Silent decisions — executed, never disclosed

- **276-294** [medium] choose which covariate effects to report in detail: all listed continuous covariates but only the first five position categories
- **378-380** [medium] bin games-played into discrete exposure categories for the exposure-stratified plot
- **420-421** [high] compute a normal-approximation (Wald) confidence interval for the unadjusted risk difference for the summary table, a different method than the delta-method CI used for the adjusted estimate

## All decisions

- `34` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed local CSV path
- `38` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `46` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `51-53, 60, 347-348` [high] **linked x3** — dichotomize skin tone into light (<=0.25) vs dark (>=0.75) groups and drop intermediate-toned players from the analytic sample, later marked on the histogram
- `64-66` [high] **linked x2** — restrict the analytic sample to dyads with complete data on the outcome and all chosen adjustment covariates
- `85-92` [low] **linked x5** — pick which variables to summarize by skin-tone group in the descriptive comparison table
- `98, 106` [low] **linked x2** — cross-tabulate position and league distributions by skin-tone group as a balance check
- `117-119, 126-129` [high] **linked x3** — compute the crude, covariate-unadjusted association between skin tone and red cards via a raw rate difference and a bivariate logistic model, as a comparator to the adjusted analysis
- `150-153` [high] **linked x10** — specify the covariate adjustment set (games, position, league, height, weight, yellow cards) and fit the adjusted logistic model
- `171-174, 177-180, 183` [high] **linked x7** — estimate the adjusted risk difference via marginal standardization (g-computation): predict outcomes setting everyone's skin tone to dark vs light and take the mean difference
- `200-241` [high] **linked x3** — derive the standard error, confidence interval, and p-value for the adjusted risk difference analytically via the delta method (gradient of the predicted-probability difference), rather than by bootstrapping or another resampling approach
- `255-261` [high] **linked x3** — extract and exponentiate the adjusted model's darkSkin coefficient and its CI to report as an odds ratio
- `276-294` [medium] **SILENT** — choose which covariate effects to report in detail: all listed continuous covariates but only the first five position categories
- `304-306, 311-320` [high] **linked x3** — extend the adjusted model with referee-level implicit/explicit bias measures on an expanded complete-case sample, as a sensitivity check
- `378-380` [medium] **SILENT** — bin games-played into discrete exposure categories for the exposure-stratified plot
- `420-421` [high] **SILENT** — compute a normal-approximation (Wald) confidence interval for the unadjusted risk difference for the summary table, a different method than the delta-method CI used for the adjusted estimate
- `448-461` [high] **linked x7** — classify the result as supporting/marginally-supporting/not-supporting the hypothesis using p<0.05 combined with the CI excluding zero
