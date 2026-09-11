# 2025-11-22T14-39-37+0000  (ai)

- code: 325 lines, 43% exon (141 lines in 19 decisions)
- intron: print 100, comment 56, glue 15, import 9, config 4
- prose: 321 lines, 114 claims (35 action, 79 result)
- links: 54 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 6
- result_claims_deferred: 79

## Silent decisions — executed, never disclosed

- **101-105** [medium] test the unadjusted association with a chi-square contingency test

## Misaligned — code and prose disagree

- code: classify players into light/dark skin groups using cutoffs (<=0.25 light, >=0.75 dark), discard the excluded middle range, and encode the result as a binary darkSkin indicator
  - prose: the middle skin-tone category (0.375-0.625) was excluded from the primary analysis for clearer comparison
  - why: code excludes the middle range (0.25, 0.75); claim states the excluded middle category is 0.375-0.625

## All decisions

- `36-37` [high] **linked x1** — load the raw player-referee dyad dataset from a specific CSV path with latin1 encoding
- `42-43` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `44-49` [low] **linked x2** — assess and report inter-rater agreement (correlation and exact-match rate) between the two skin-tone raters
- `54-55` [high] **linked x1** — drop rows without a valid skinTone rating before building the analysis dataset
- `56-69` [high] **linked x4** — classify players into light/dark skin groups using cutoffs (<=0.25 light, >=0.75 dark), discard the excluded middle range, and encode the result as a binary darkSkin indicator
- `70` [high] **linked x1** — binarize the outcome as whether any red card occurred, rather than using the red-card count
- `92-100` [medium] **linked x2** — compute and report the unadjusted (crude) risk difference between dark- and light-skin groups
- `101-105` [medium] **SILENT** — test the unadjusted association with a chi-square contingency test
- `111-116, 223-227` [high] **linked x4** — restrict the sample to complete cases on height, position, and weight
- `122-124, 228-229` [medium] **linked x2** — encode player position and league country as categorical (dummy-coded) covariates
- `134-139` [high] **linked x6** — fit the primary model as an OLS linear probability model of any-red-card on dark skin plus the covariate set, with player-clustered standard errors
- `146-152` [medium] **linked x8** — designate the LPM coefficient as the primary estimand and report it as a risk difference with a 95% CI and two-sided p-value against alpha=0.05
- `162-169` [high] **linked x1** — fit a secondary logistic regression (same covariates, player-clustered SEs) to obtain an odds ratio
- `176-180` [medium] **linked x2** — report the secondary estimand as an exponentiated odds ratio with a 95% CI
- `202-212` [medium] **linked x2** — justify player-level SE clustering by computing the intraclass correlation and cluster-size distribution of dyads per player
- `222, 230-240` [high] **linked x6** — sensitivity check refitting with continuous skinTone as the exposure instead of the binary light/dark group
- `241-247` [high] **linked x3** — sensitivity check adding a darkSkin by league interaction term to test effect heterogeneity across leagues
- `259-268, 272-276` [high] **linked x2** — sensitivity check modeling red-card counts with a Poisson regression using log(games) as an exposure offset
- `307-319` [medium] **linked x6** — characterize the overall conclusion by judging the effect as small in magnitude, barely significant, heterogeneous across leagues, and hedging on generalizability
