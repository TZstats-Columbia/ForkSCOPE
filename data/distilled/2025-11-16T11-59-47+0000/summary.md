# 2025-11-16T11-59-47+0000  (ai)

- code: 591 lines, 38% exon (222 lines in 20 decisions)
- intron: print 229, plot 71, comment 42, glue 14, import 9, config 4
- prose: 283 lines, 110 claims (63 action, 47 result)
- links: 44 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 30
- R_only_consistent_negative: 6
- result_claims_deferred: 47

## Silent decisions — executed, never disclosed

- **34-36** [high] load the raw player-referee dyad dataset from CSV
- **76-92** [high] collapse detailed playing positions into four broad position groups
- **138-139** [low] pick which covariates to compare across skin-tone groups as a balance check

## All decisions

- `34-36` [high] **SILENT** — load the raw player-referee dyad dataset from CSV
- `40-43` [high] **linked x1** — average the two raters' photo scores into one continuous skin_tone variable
- `49-51` [high] **linked x2** — collapse the red card count into a binary any-red-card outcome
- `62-66` [high] **linked x2** — drop dyads that lack a photo-based skin tone rating
- `67-71, 439-440, 466-467` [high] **linked x5** — dichotomize continuous skin tone into dark vs light at a 0.25 cutoff
- `76-92` [high] **SILENT** — collapse detailed playing positions into four broad position groups
- `93-97` [medium] **linked x1** — choose which outcome, exposure and covariate columns are carried into the modeling dataset
- `98-103` [high] **linked x2** — drop dyads with no assignable broad position
- `104-112` [high] **linked x2** — fill missing height and weight with the sample median instead of dropping those rows
- `138-139` [low] **SILENT** — pick which covariates to compare across skin-tone groups as a balance check
- `151-153, 159-161` [high] **linked x10** — specify a logistic regression of any red card on dark_skin adjusted for position, league, games, yellow cards, goals, height and weight
- `179-195` [high] **linked x4** — standardize the fitted model over counterfactual dark_skin values to compute an average marginal risk difference (g-computation)
- `200-204` [high] **linked x2** — approximate the risk difference's standard error via a delta-method scaling of the logit coefficient SE
- `205-208` [high] **linked x1** — build a 95% CI for the risk difference using a normal (±1.96·SE) approximation
- `213-218, 409` [high] **linked x2** — declare statistical significance using a two-sided 0.05 threshold
- `223-227` [medium] **linked x3** — exponentiate the coefficient and CI to report an adjusted odds ratio as a secondary estimand
- `248, 252-264, 268-276` [high] **linked x2** — refit the adjustment model with skin_tone left continuous instead of dichotomized
- `277-278, 282-285, 291-304, 308-321, 325-332` [high] **linked x2** — restrict to the extreme tails of skin tone (<=0.125 vs >=0.75) and refit
- `333-334, 338, 342-355, 359-366` [high] **linked x2** — refit the model excluding goalkeepers
- `367-368, 372, 376-389, 393-400` [high] **linked x1** — refit the model excluding dyads with fewer than two shared games
