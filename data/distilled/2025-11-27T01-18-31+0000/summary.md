# 2025-11-27T01-18-31+0000  (ai)

- code: 375 lines, 28% exon (106 lines in 21 decisions)
- intron: print 154, comment 58, glue 44, import 6, config 5, dead 2
- prose: 211 lines, 107 claims (44 action, 63 result)
- links: 45 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 13
- R_only_consistent_negative: 13
- result_claims_deferred: 63

## Silent decisions — executed, never disclosed

- **256** [high] only report a threshold's result if each exposure group has at least 100 players

## Misaligned — code and prose disagree

- code: keep only rows that actually have a position recorded
  - prose: no other exclusions beyond missing skin-tone data and goalkeepers were applied; all dyads with complete skin-tone data were retained
  - why: code additionally drops rows lacking a recorded position, an exclusion beyond the missing-skin-tone and goalkeeper exclusions the claim says are the only ones applied

## All decisions

- `31-32` [medium] **linked x1** — pick the input CSV of player-referee dyads as the entire analysis universe
- `47-50` [high] **linked x1** — collapse the two human ratings into a single skin-tone score by averaging them
- `51-52, 54` [high] **linked x1** — drop dyads that have no skin-tone rating at all
- `69-82` [high] **linked x4** — roll dyad-level rows up to one row per player, summing career totals for most stats but taking the first value for player attributes
- `88-89` [medium] **linked x1** — flag a player as a case if they ever picked up a red card across their career
- `100-106` [high] **linked x3** — split players into two exposure groups by cutting the skin-tone score at 0.25
- `111-115` [medium] **linked x1** — compute and surface the raw red-card-rate gap between the two skin-tone groups before any adjustment
- `125-140, 275` [high] **linked x1** — collapse the many raw position labels into a handful of role buckets
- `141-144` [high] **linked x3** — drop goalkeepers from the analytic sample
- `145, 273` [medium] **linked x1** — keep only rows that actually have a position recorded
- `149-153, 274` [high] **linked x3** — put games played on a log scale (plus one) to use as a control for exposure/opportunity
- `169-174` [high] **linked x1** — fit a logistic regression of ever-red-card on the dichotomized skin tone, controlling for position group and log games
- `187-188` [high] **linked x8** — summarize the fitted model's exposure effect as an average marginal (risk-difference) effect via dydx with dummy handling
- `199-202` [high] **linked x1** — additionally compute a one-sided p-value on top of the two-sided test, testing the directional hypothesis that the effect is positive
- `226-229` [high] **linked x3** — re-express the same fitted coefficient as an odds ratio with its own CI as a secondary summary of the effect
- `252-255, 257-261` [high] **linked x3** — re-estimate the model at alternative skin-tone cut points (0.125 and 0.375) alongside the primary 0.25 cut to check sensitivity of the result to the threshold
- `256` [high] **SILENT** — only report a threshold's result if each exposure group has at least 100 players
- `276-279` [high] **linked x2** — re-run the model on the full player set including goalkeepers instead of excluding them, to see if the exclusion drives the result
- `291-294` [high] **linked x3** — add league fixed effects to the adjustment set as a further sensitivity check
- `306-309` [high] **linked x2** — swap the dichotomized exposure for the raw continuous skin-tone score in the model as an alternative specification
- `363, 369` [high] **linked x2** — declare the hypothesis 'supported' only when the two-sided p-value is below 0.05 and the effect points in the hypothesized positive direction
