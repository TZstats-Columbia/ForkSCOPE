# 2025-11-26T20-27-00+0000  (ai)

- code: 428 lines, 25% exon (106 lines in 21 decisions)
- intron: print 214, comment 91, import 7, config 5, glue 5
- prose: 277 lines, 105 claims (74 action, 31 result)
- links: 48 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 27
- R_only_consistent_negative: 18
- result_claims_deferred: 31

## Silent decisions — executed, never disclosed

- **64-66** [high] derive player age as a fixed reference year (2013) minus birth year, with missing birthdays left missing
- **167-169** [high] test the unadjusted group difference in red-card rates with a two-proportion z-test

## Misaligned — code and prose disagree

- code: refit the adjusted model using alternative dark-skin cutoffs (0.375 and 0.5) instead of the primary 0.25 threshold
  - prose: tested multiple skin-tone thresholds (0.25, 0.375, 0.5, 0.625) and cutpoint strategies through exploratory specification search
  - why: claim says thresholds 0.25/0.375/0.5/0.625 were tested; code only refits at 0.375 and 0.5 (plus primary 0.25), never 0.625

## All decisions

- `38` [high] **linked x1** — load the raw player-referee dyad dataset from a fixed CSV path
- `42` [high] **linked x2** — average the two independent raters' skin-tone scores into one consensus skinTone measure
- `45-46` [medium] **linked x2** — restrict to dyads rated by both raters and compute their correlation as a reliability diagnostic
- `58-59` [high] **linked x3** — drop dyads that lack a skin-tone rating (no player photo available)
- `64-66` [high] **SILENT** — derive player age as a fixed reference year (2013) minus birth year, with missing birthdays left missing
- `70-76` [high] **linked x5** — further exclude dyads missing position, height, or weight from the analysis sample
- `92` [high] **linked x2** — collapse red-card counts into a binary outcome for whether any red card occurred in the dyad
- `100` [high] **linked x3** — dichotomize the continuous skin-tone score into a binary dark-skin exposure at a 0.25 cutoff
- `118-122` [high] **linked x4** — z-score standardize the continuous covariates before modeling
- `127-130` [high] **linked x3** — one-hot encode player position, dropping Goalkeeper as the reference category
- `135-136` [high] **linked x2** — one-hot encode league country, dropping the first (England) as reference category
- `150-160` [high] **linked x1** — split the sample by exposure group and compute the crude (unadjusted) red-card rate difference between groups
- `167-169` [high] **SILENT** — test the unadjusted group difference in red-card rates with a two-proportion z-test
- `183-186, 336` [high] **linked x1** — define the covariate adjustment set (position, league, standardized age/height/weight/games) and the outcome~exposure+covariates model formula; reused as-is when refitting on the games-restricted sensitivity subset
- `198` [high] **linked x3** — fit the adjustment model as a logistic regression via maximum likelihood
- `219-224, 226-227, 230` [high] **linked x4** — estimate the adjusted risk difference as an average marginal effect by predicting outcomes under all-dark and all-light counterfactuals and averaging the difference
- `239-250` [medium] **linked x4** — approximate the marginal effect's standard error via the delta method (coefficient scaled by mean fitted p(1-p)) and derive a Wald CI and z-test from it
- `272-274` [high] **linked x2** — report the exponentiated model coefficient and its exponentiated confidence interval as an adjusted odds ratio
- `297-305, 307-311` [high] **linked x4** — refit the adjusted model using alternative dark-skin cutoffs (0.375 and 0.5) instead of the primary 0.25 threshold
- `320-327` [high] **linked x1** — refit the model treating skin tone as a continuous predictor instead of dichotomizing it, and scale the reported effect to a 0.1-unit increment
- `335, 337-346` [high] **linked x1** — restrict the sample to dyads with at least two games as a robustness check on exposure reliability, and recompute the OR and AME on that subset
