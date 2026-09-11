# 2025-11-29T00-13-53+0000  (ai)

- code: 357 lines, 47% exon (169 lines in 18 decisions)
- intron: print 126, comment 52, import 6, config 4
- prose: 223 lines, 102 claims (70 action, 32 result)
- links: 81 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 10
- result_claims_deferred: 32

## All decisions

- `31` [high] **linked x2** — choose the input dataset and file path to load as the analysis source
- `33-35` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `36-38` [high] **linked x3** — collapse the red-card count into a binary any-red-card indicator
- `39-41` [high] **linked x2** — drop dyads that lack a skin-tone rating
- `49-54` [high] **linked x7** — restrict the sample to dyads with at least 3 games together
- `56-65` [high] **linked x12** — define dark_skin exposure from the two extreme skin-tone bands and drop everyone in the middle range
- `73-75` [medium] **linked x2** — log-transform games played to use as an exposure covariate
- `76-79` [medium] **linked x2** — derive player age from birthdate relative to a fixed reference year (2012)
- `80-97` [medium] **linked x2** — bucket the many raw position labels into six broader position categories
- `98-100` [high] **linked x4** — drop remaining rows missing age, height, or weight
- `116-118` [medium] **linked x1** — compute unadjusted red-card rate per skin-tone group by simple grouped mean
- `132-137` [high] **linked x7** — specify and fit the adjusted logistic model, choosing which covariates enter the adjustment set
- `142-147, 217-219` [high] **linked x8** — pull the dark_skin coefficient and its CI from the fit and exponentiate it into an odds ratio
- `157-166` [high] **linked x4** — compute the adjusted risk difference by predicting outcomes under an all-dark vs all-light counterfactual and differencing the averages
- `173-202` [high] **linked x7** — bootstrap the risk difference (500 resamples, refit each time) and take a percentile interval plus a proportion-based two-sided p-value
- `233-254` [high] **linked x7** — re-run the whole pipeline under alternative minimum-games cutoffs (2 and 5) to check sensitivity of the odds ratio
- `255-277` [high] **linked x5** — swap the extreme-group exposure definition for a single sweeping cutoff (0.5, then 0.625) and refit to see if the odds ratio holds up
- `278-289` [high] **linked x4** — add yellow-card count to the adjustment set and refit to see if the effect survives controlling for player aggressiveness
