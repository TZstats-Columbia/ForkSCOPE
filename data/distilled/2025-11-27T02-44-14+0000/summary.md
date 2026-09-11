# 2025-11-27T02-44-14+0000  (ai)

- code: 177 lines, 35% exon (62 lines in 14 decisions)
- intron: print 55, comment 47, glue 5, import 4, config 4
- prose: 209 lines, 87 claims (47 action, 40 result)
- links: 48 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 20
- R_only_consistent_negative: 4
- result_claims_deferred: 40

## All decisions

- `16-17` [high] **linked x1** — load the analysis input from a fixed CSV path, fixing the data source and scope
- `24-25` [high] **linked x2** — average the two independent raters' scores into a single continuous skin-tone measure
- `27-28` [high] **linked x1** — collapse the red card count into a binary any-red-card indicator using a >0 rule
- `30-31` [high] **linked x3** — drop dyads lacking a skin tone rating from the analytic sample rather than imputing or otherwise handling them
- `43-44` [high] **linked x7** — dichotomize the continuous skin-tone score into dark/light exposure groups at a 0.25 cutoff
- `53-65, 66-67` [high] **linked x3** — regroup free-text position labels into four coarse role categories via keyword matching, with a residual Unknown bucket
- `69-71` [high] **linked x4** — fill missing height and weight values with the sample mean rather than dropping or modeling them
- `77-78` [high] **linked x4** — pick the covariate adjustment set and functional form, including a log(games+1) transform for exposure time
- `83-84` [high] **linked x3** — fit the specified formula with a logistic regression estimator rather than an alternative link/family, with fixed convergence settings
- `92-95` [high] **linked x4** — back-transform the logit coefficient into an odds ratio and build a Wald-style 95% interval using a 1.96 normal multiplier
- `110-114, 115-117, 118-119` [high] **linked x4** — define the primary estimand as an average-marginal-effect risk difference by scoring the whole sample under counterfactual all-dark and all-light exposure and contrasting predictions
- `122-124, 126-128` [high] **linked x4** — approximate the risk difference's standard error and CI via a delta-method derivative scaling of the coefficient SE, with a 1.96 normal multiplier
- `160-163` [high] **linked x4** — additionally report a crude, unadjusted rate difference between exposure groups alongside the adjusted estimate
- `170-175` [high] **linked x4** — classify the finding as supported vs not supported using a p<0.05 and positive-direction rule
