# 2025-11-29T15-01-09+0000  (ai)

- code: 399 lines, 39% exon (157 lines in 16 decisions)
- intron: print 128, comment 48, plot 34, glue 19, import 8, config 5
- prose: 244 lines, 76 claims (41 action, 35 result)
- links: 55 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 11
- result_claims_deferred: 35

## Silent decisions — executed, never disclosed

- **201-209** [medium] additionally compute an average marginal effect from the logit model by predicting outcomes with dark forced to 1 vs 0 and averaging the difference
- **289-293** [low] hardcode the threshold-sweep effect sizes and confidence intervals as literal numbers for the plot instead of pulling them from the fitted model results computed above
- **310-313** [medium] bin continuous skinTone into six display categories for the unadjusted red-card-rate plot

## All decisions

- `37-39` [high] **linked x2** — load the full raw player-referee dyad dataset from soccer.csv, fixing the starting sample scope
- `41-45` [high] **linked x3** — average the two independent raters' skin-tone codings into one continuous skinTone score
- `46-48` [high] **linked x3** — collapse the red-card count into a binary any-red-card outcome
- `61-64` [high] **linked x4** — drop dyads with no skin-tone rating (missing player photo) from the analysis set
- `83-118, 127-129, 260` [high] **linked x9** — sweep five candidate skin-tone thresholds, compare dark/light red-card rates and chi-square significance at each, pick the threshold with the largest effect size as the primary dark/light definition, and apply that chosen threshold each time a 'dark' exposure variable is built
- `130-133` [high] **linked x4** — drop dyads missing height or weight so every adjusted model shares one common sample
- `149-158` [high] **linked x3** — choose the covariate adjustment set (position, league country, games, yellow cards, height, weight, goals) used to control confounding
- `159-161, 166` [high] **linked x5** — fit the primary association as an OLS linear-probability model with HC3 heteroskedasticity-robust standard errors, yielding a risk-difference estimate
- `180-182, 186` [high] **linked x4** — fit a logistic regression as the secondary model to obtain an odds-ratio estimate
- `201-209` [medium] **SILENT** — additionally compute an average marginal effect from the logit model by predicting outcomes with dark forced to 1 vs 0 and averaging the difference
- `220-239` [high] **linked x4** — re-run the full adjusted analysis using an alternate skin-tone threshold (>0.25) in place of the primary threshold, as a robustness check
- `240-256` [high] **linked x7** — re-run the analysis treating skinTone as a continuous predictor instead of dichotomizing into dark/light
- `257-259, 261-277` [high] **linked x3** — restrict to dyads with non-missing referee implicit/explicit bias measures and add those measures as extra adjustment covariates, as a robustness check
- `289-293` [low] **SILENT** — hardcode the threshold-sweep effect sizes and confidence intervals as literal numbers for the plot instead of pulling them from the fitted model results computed above
- `310-313` [medium] **SILENT** — bin continuous skinTone into six display categories for the unadjusted red-card-rate plot
- `370-372, 385, 390` [high] **linked x4** — set the criteria for declaring the hypothesis SUPPORTED/NOT SUPPORTED and for describing the risk-difference CI's relation to zero, based on whether the CI excludes zero and whether p-values fall below 0.05
