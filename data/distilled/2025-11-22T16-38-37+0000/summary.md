# 2025-11-22T16-38-37+0000  (ai)

- code: 372 lines, 37% exon (136 lines in 21 decisions)
- intron: print 168, comment 57, import 5, config 4, glue 2
- prose: 289 lines, 136 claims (47 action, 89 result)
- links: 63 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 19
- R_only_consistent_negative: 3
- result_claims_deferred: 89

## All decisions

- `29-30` [high] **linked x1** — load the raw player-referee dyad dataset from CSV
- `36-37` [high] **linked x1** — average the two raters' skin-tone scores into one continuous skin_avg score
- `39-41` [low] **linked x1** — assess inter-rater reliability via Pearson correlation and exact-agreement rate, restricted to dyads with both raters present
- `55` [high] **linked x1** — drop dyads lacking a skin-tone rating from the analysis sample
- `60-61` [high] **linked x1** — collapse red-card count into a binary any-red-card outcome
- `63-65` [high] **linked x5** — dichotomize averaged skin-tone score at 0.25 into dark vs light exposure groups
- `71` [medium] **linked x2** — log-transform games played to use as a covariate
- `72-73` [medium] **linked x3** — construct a yellow-cards-per-game rate covariate
- `75-80` [high] **linked x2** — restrict to complete cases with non-missing position, height, and weight for the adjusted analysis
- `130-136` [high] **linked x6** — fit the primary logistic regression of any red card on dark skin tone adjusting for log games, yellow-card rate, position, and league, with standard errors clustered by player
- `147-153` [medium] **linked x4** — convert the skin_dark coefficient into an odds ratio with a Wald 95% CI via the normal approximation
- `168-180` [high] **linked x6** — estimate the adjusted risk difference by g-computation: set every dyad's exposure to all-dark then all-light, predict from the fitted model, and average the predicted probabilities
- `188, 192-196, 199-221` [high] **linked x1** — obtain a cluster bootstrap distribution for the risk difference by resampling players with replacement, discarding replicates with fewer than 1000 rows or a failed fit, over 200 iterations
- `222-227` [medium] **linked x3** — derive the bootstrap CI from the 2.5/97.5 percentiles and a two-sided p-value via a normal approximation using the bootstrap standard error
- `246-252` [high] **linked x3** — fit an unadjusted logistic model of any red card on skin_dark alone as a sensitivity check
- `257-262` [medium] **linked x3** — refit with skin tone as a continuous exposure instead of dichotomized, rescaling the coefficient to a per-0.25-unit odds ratio
- `267-275` [high] **linked x4** — redefine exposure with extreme cutoffs (<=0.125 vs >=0.75) and refit the model on only the extreme-group subsample
- `280-288, 290` [high] **linked x7** — stratify the adjusted model by a fixed set of league countries, fitting one model per league and handling non-convergence
- `295-302` [high] **linked x3** — exclude goalkeepers from the sample and refit the adjusted model
- `307-315` [high] **linked x4** — add referee implicit-bias score (meanIAT) as a covariate, restricted to dyads with non-missing IAT
- `329, 335, 338` [medium] **linked x2** — compare red-card rates and league-country distribution between dyads with vs without skin-tone data to characterize the missingness pattern
