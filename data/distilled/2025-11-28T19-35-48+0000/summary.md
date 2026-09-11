# 2025-11-28T19-35-48+0000  (ai)

- code: 382 lines, 27% exon (104 lines in 15 decisions)
- intron: print 129, glue 77, comment 62, import 8, config 2
- prose: 279 lines, 105 claims (61 action, 44 result)
- links: 64 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 14
- result_claims_deferred: 44

## Misaligned — code and prose disagree

- code: collapse red card count into a binary any-red-card outcome
  - prose: no other data transformations were applied beyond the skin tone averaging and age calculation
  - why: claim denies any transformations beyond averaging and age, but code collapses redCards into a binary anyRedCard outcome
- code: fill missing height, weight, and age with the sample median rather than dropping or modeling them
  - prose: no other data transformations were applied beyond the skin tone averaging and age calculation
  - why: claim denies transformations beyond averaging and age, but code median-imputes height, weight, and age

## All decisions

- `40` [high] **linked x3** — load the raw soccer referee/red-card dataset from CSV as the entire analysis input
- `53` [high] **linked x2** — drop player-referee dyads that are missing either rater's skin-tone score
- `60` [high] **linked x2** — average the two raters' scores into one composite skin-tone measure
- `65` [high] **linked x4** — collapse red card count into a binary any-red-card outcome
- `70-72` [high] **linked x1** — parse birthdate format and pick a fixed end-of-season reference date to compute player age in years
- `74-76` [high] **linked x4** — fill missing height, weight, and age with the sample median rather than dropping or modeling them
- `92-98, 102-107, 144, 156-160, 242-245` [high] **linked x16** — search across candidate light/dark skin-tone cutoff pairs, keep only dyads at the extremes for each pair, and pick the cutoff whose estimated effect is largest to serve as the primary (and later a 'robustness') comparison
- `110-117, 179-186, 211-215, 246-253, 265-266, 283-284, 301-307, 320-321` [high] **linked x6** — define the standard adjustment set (position, league, games, imputed age/height/weight) used to control every red-card regression
- `125-126, 193-194, 256-257, 274-275, 292-293, 329-330` [high] **linked x8** — fit the dark-skin/red-card relationship as an OLS linear probability model with standard errors clustered by player
- `220-221` [high] **linked x3** — refit the primary comparison as a logistic regression and report the odds ratio as a secondary estimand
- `268-271` [high] **linked x3** — treat skin tone as a continuous exposure instead of the dichotomized dark/light indicator
- `286-289` [high] **linked x2** — refit the primary comparison with a reduced covariate set that drops age, height, and weight
- `310` [high] **linked x5** — swap player-clustered standard errors for HC3 heteroskedasticity-robust standard errors (no clustering)
- `318, 323-326` [high] **linked x4** — restrict to dyads with a non-missing referee implicit-bias score and add referee IAT/explicit-bias measures to the adjustment set
- `371` [high] **linked x1** — declare the hypothesis 'supported' only if the primary effect is significant at .05 and its CI excludes zero
