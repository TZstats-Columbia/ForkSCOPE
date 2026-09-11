# 2025-11-29T18-48-28+0000  (ai)

- code: 324 lines, 36% exon (117 lines in 18 decisions)
- intron: print 149, comment 47, import 7, config 4
- prose: 265 lines, 106 claims (69 action, 37 result)
- links: 51 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 21
- R_only_consistent_negative: 21
- result_claims_deferred: 37

## Silent decisions — executed, never disclosed

- **261** [low] only report a subgroup's model if it has more than 1000 observations

## All decisions

- `33-35` [high] **linked x3** — pull in the raw player-referee dyad table as the full study population
- `37-39` [high] **linked x1** — drop dyads lacking either skin-tone rater score from the working sample
- `42-44` [high] **linked x2** — blend the two raters' scores into one continuous skin-tone measure by simple mean
- `45-47` [high] **linked x2** — collapse red-card counts down to a yes/no indicator per dyad
- `56-58` [high] **linked x2** — squash the games-played exposure variable with a log(1+x) transform
- `59-71` [high] **linked x2** — collapse free-text playing position into four coarse buckets and apply it row-wise
- `114-116` [high] **linked x2** — split the continuous skin-tone score into a dark/light exposure at a 0.25 cutoff
- `121-124` [medium] **linked x2** — compute the crude, unadjusted red-card rate separately for the light and dark groups
- `129-134` [high] **linked x6** — fit a logistic model of any red card on dark_skin adjusting for exposure, position, and league
- `140-151` [high] **linked x7** — convert the model into an average-marginal-effect risk difference and pull out its SE/z/p/CI for dark_skin
- `152-158` [high] **linked x4** — translate the same coefficient into an odds ratio with a Wald 95% interval as a secondary summary
- `200-217` [high] **linked x6** — re-dichotomize skin tone at four different cutoffs and refit the adjusted model at each to check robustness of the effect to the 0.25 choice
- `222-233` [high] **linked x3** — swap the binary exposure for the raw continuous skintone score and refit, extracting its per-unit marginal effect
- `241-249` [high] **linked x3** — restrict to dyads with a non-missing referee implicit-bias score and add that score as an extra covariate in the adjusted model
- `259-260` [high] **linked x4** — iterate the adjusted model separately over each broad position subgroup
- `261` [low] **SILENT** — only report a subgroup's model if it has more than 1000 observations
- `262-267` [high] **linked x1** — fit the dark_skin model within the position subgroup, dropping the position covariate itself, and pull its marginal effect
- `272-280` [high] **linked x1** — restrict to dyads with at least 5 games and refit the adjusted model as a high-exposure robustness check
