# 2025-11-26T21-41-50+0000  (ai)

- code: 222 lines, 37% exon (83 lines in 13 decisions)
- intron: print 87, comment 37, import 8, config 5, glue 2
- prose: 232 lines, 98 claims (45 action, 53 result)
- links: 32 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 15
- result_claims_deferred: 53

## All decisions

- `25-26` [high] **linked x3** — read the full soccer referee-player dyad dataset from CSV as the starting analysis sample
- `39-40` [high] **linked x1** — drop dyads that are missing a skin-tone rating from either rater
- `43-44` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `45-47` [high] **linked x1** — drop goalkeepers from the sample on the grounds of minimal field contact
- `49-51` [high] **linked x1** — restrict to dyads with at least 3 games together as a minimum-exposure cutoff
- `63-64` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `65-69` [high] **linked x4** — dichotomize the continuous skin-tone average at 0.25 to define the dark-skin exposure group
- `70-73` [high] **linked x2** — z-score the games count before using it as a model covariate
- `83-90` [medium] **linked x1** — compute and report the unadjusted red-card rate separately for the light- and dark-skin groups
- `100-104` [high] **linked x5** — fit a logistic regression of any-red-card on dark-skin status, adjusting only for standardized games
- `120-156, 158` [high] **linked x6** — derive the covariate-adjusted risk difference by predicting outcome probabilities under both skin-tone levels for every dyad, averaging the contrast, and computing a delta-method SE with a normal-approximation 95% CI and two-sided p-value
- `176-181` [high] **linked x4** — exponentiate the dark-skin coefficient and its Wald interval to report an adjusted odds ratio as a secondary estimand
- `203-205` [medium] **linked x2** — express the adjusted risk difference as a percentage of the raw (unadjusted) light-skin baseline rate
