# 2025-11-27T01-53-05+0000  (ai)

- code: 289 lines, 42% exon (120 lines in 15 decisions)
- intron: print 100, comment 49, other 10, import 5, config 5
- prose: 296 lines, 99 claims (53 action, 46 result)
- links: 89 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 8
- result_claims_deferred: 46

## All decisions

- `32` [high] **linked x4** — pick which raw file becomes the analytic dataset and its initial scope
- `35-36` [high] **linked x7** — drop dyads missing either rater's score, treating complete-case dyads as the analysis population
- `45-47` [high] **linked x1** — combine the two raters' scores into one continuous skin-tone measure by simple averaging
- `52-56` [high] **linked x15** — collapse continuous skin tone into a binary light/dark split at a >0.125 cutpoint, explicitly chosen after searching for the split that maximizes the effect
- `70-72` [high] **linked x2** — reduce the red-card count to a yes/no indicator of any red card in the dyad
- `78-80` [high] **linked x2** — log-transform games played to serve as the exposure-time adjustment covariate
- `89-95` [medium] **linked x2** — report a raw, unadjusted red-card-rate gap between the two skin-tone groups as a descriptive baseline
- `107-110` [high] **linked x9** — choose logistic regression of any-red-card on dark skin plus log games as the primary model family and adjustment set
- `117, 184-187` [high] **linked x7** — translate the model's log-odds coefficient into an odds ratio with a Wald-based CI, framed as the secondary estimand
- `124, 127-135` [high] **linked x8** — standardize the fitted model by predicting outcomes under dark=1 and dark=0 for every dyad and averaging the gap, naming this the primary estimand
- `144-168, 173-175` [high] **linked x9** — get uncertainty on the risk difference by resampling dyads 2000 times, refitting each time, taking the empirical percentile interval, and back out a two-sided p-value from the bootstrap spread
- `197, 199-206` [high] **linked x6** — redo the light/dark split at a looser >0.25 line and refit, checking whether the result survives a different cutpoint
- `211, 213-220` [high] **linked x6** — throw league country into the model as an extra adjustment factor
- `224-240, 242-249` [high] **linked x9** — invent a coarse position taxonomy from free-text position strings and stack it with league country as additional covariates
- `282-287` [high] **linked x2** — assert the hypothesis is 'strongly supported' on the basis of the adjusted risk difference and its CI excluding zero
