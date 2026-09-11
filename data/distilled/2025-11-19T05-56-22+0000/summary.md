# 2025-11-19T05-56-22+0000  (ai)

- code: 362 lines, 40% exon (146 lines in 16 decisions)
- intron: print 105, plot 51, comment 44, import 12, config 3, glue 1
- prose: 272 lines, 97 claims (48 action, 49 result)
- links: 69 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 10
- result_claims_deferred: 49

## Silent decisions — executed, never disclosed

- **34-35** [high] load the raw player-referee dyad dataset from a specific CSV path
- **319-328** [low] map p-values to significance-star annotations using conventional alpha thresholds (0.001/0.01/0.05)

## All decisions

- `34-35` [high] **SILENT** — load the raw player-referee dyad dataset from a specific CSV path
- `38-40` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `41-42, 44-45` [medium] **linked x1** — restrict to dyads with both ratings present and quantify inter-rater agreement via Pearson and Spearman correlation
- `50-57` [high] **linked x5** — dichotomize continuous skin tone into light (<=0.25) vs dark (>=0.75) groups, dropping the middle range
- `58-60` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `61-63` [high] **linked x7** — drop dyads lacking a defined light/dark category to form the analysis sample
- `73-92` [high] **linked x1** — bucket free-text position strings into a fixed set of position categories via keyword matching
- `93-95` [high] **linked x2** — log-transform games played for use as a covariate
- `104-106` [high] **linked x6** — choose which variables (outcome, exposure, id, covariates) are carried into the modeling dataset
- `107-108` [high] **linked x1** — drop rows with any missing covariate via listwise deletion
- `123-134` [high] **linked x4** — test the unadjusted association between skin tone and red cards via chi-square, odds ratio, and risk difference
- `148-157` [high] **linked x15** — specify and fit a logistic regression of any-red-card on skin tone adjusted for log games, position, and league, with player-clustered standard errors
- `178-189` [high] **linked x13** — compute the adjusted risk difference as an average marginal effect by predicting outcomes under counterfactual light vs dark skin tone for every observation
- `195-233, 235-239, 240-242` [high] **linked x8** — construct a confidence interval and p-value for the AME via player-level cluster bootstrap with 200 resamples, refitting the model each time
- `258-261` [high] **linked x3** — exponentiate the logistic coefficient to report an adjusted odds ratio as a secondary effect measure
- `319-328` [low] **SILENT** — map p-values to significance-star annotations using conventional alpha thresholds (0.001/0.01/0.05)
