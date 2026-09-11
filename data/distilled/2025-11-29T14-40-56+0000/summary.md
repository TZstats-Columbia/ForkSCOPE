# 2025-11-29T14-40-56+0000  (ai)

- code: 379 lines, 40% exon (150 lines in 17 decisions)
- intron: print 172, comment 47, config 6, import 4
- prose: 257 lines, 78 claims (45 action, 33 result)
- links: 63 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 5
- result_claims_deferred: 33

## All decisions

- `32-33` [high] **linked x1** — pull the raw player-referee dyad table from a single fixed CSV path with no row scoping applied yet
- `36-37` [high] **linked x3** — drop every dyad that lacks a skin-tone rating from either coder, deciding non-response is excluded rather than imputed
- `40-42` [high] **linked x1** — collapse the two raters' scores into a single continuous skin-tone measure by simple averaging
- `43-44` [high] **linked x1** — define the outcome as any red card at all rather than counting multiple cards or using yellow cards
- `53-69` [high] **linked x1** — collapse the detailed on-field position labels into four coarse role buckets, dropping goalkeeper-adjacent nuance
- `70-74` [high] **linked x5** — pick a specific cut point (0.125) to turn the continuous skin-tone score into a dark/light binary, chosen explicitly to maximize apparent evidence
- `87-92` [high] **linked x4** — restrict the analysis sample to rows with non-missing position, height and weight, discarding the rest as a complete-case set
- `96-101` [medium] **linked x2** — z-score the continuous covariates before modeling instead of leaving them in raw units
- `108, 114, 118-119` [medium] **linked x2** — split the sample into dark/light subgroups by the chosen threshold and report a raw, unadjusted risk difference between them
- `130-134` [high] **linked x13** — fit the primary model as a logistic regression of any red card on the dichotomized exposure plus a specific adjustment set (position, league, games, yellow cards, height, weight)
- `160-169` [high] **linked x6** — compute the primary effect as an adjusted risk difference via marginal standardization (predict outcomes under everyone-dark vs everyone-light and difference the means) rather than reading the raw model coefficient
- `174, 177-204` [high] **linked x6** — get uncertainty on the risk difference via a 1000-draw parametric bootstrap over the model's coefficient covariance, and derive a two-sided p-value from the fraction of draws crossing zero
- `223-230` [high] **linked x5** — report a secondary effect measure by exponentiating the model's exposure coefficient and its CI into an odds ratio
- `246, 250-271` [high] **linked x5** — re-run the whole modeling pipeline at two alternative dichotomization cut points (0.10, 0.25) as a sensitivity check on the threshold choice
- `277, 281-298` [high] **linked x2** — swap the dichotomized exposure for the raw continuous (standardized) skin-tone score as an alternative model specification
- `303, 307-312` [high] **linked x1** — add referee-country implicit-bias score as an extra covariate in a sensitivity model, choosing to adjust for it rather than treat it as a mediator or ignore it
- `361, 373` [high] **linked x5** — declare the hypothesis 'supported' using a specific gate: two-sided p-value below 0.05 combined with a positive-signed risk difference
