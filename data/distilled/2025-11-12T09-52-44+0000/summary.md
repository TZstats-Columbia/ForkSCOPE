# 2025-11-12T09-52-44+0000  (ai)

- code: 395 lines, 43% exon (170 lines in 23 decisions)
- intron: print 175, comment 42, import 5, config 3
- prose: 276 lines, 79 claims (37 action, 42 result)
- links: 48 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 12
- result_claims_deferred: 42

## Silent decisions — executed, never disclosed

- **53-70, 310** [high] bucket free-text position strings into Goalkeeper/Defender/Midfielder/Forward/Unknown via keyword matching
- **313-314** [medium] drop remaining dyads missing height or weight before fitting the continuous-exposure model

## All decisions

- `23-25` [high] **linked x2** — load the raw player-referee dyad dataset from a local CSV
- `33-35` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `36-41` [medium] **linked x1** — assess inter-rater agreement (correlation and exact-match rate) using only dyads where both raters supplied a rating
- `42-46` [high] **linked x4** — restrict to dyads with extreme skin-tone ratings (<=0.25 or >=0.75) and dichotomize into a darkSkin exposure indicator
- `47-48, 309` [high] **linked x2** — define the outcome as receipt of any red card in the dyad, binarizing the red-card count
- `53-70, 310` [high] **SILENT** — bucket free-text position strings into Goalkeeper/Defender/Midfielder/Forward/Unknown via keyword matching
- `71-74, 311-312` [high] **linked x2** — one-hot encode position category and league country, dropping the first level as reference
- `75-83` [high] **linked x3** — select the analysis variable set and listwise-delete any dyad missing a value among them
- `97-100` [low] **linked x1** — compute the raw red-card rate within each skin-tone group as an unadjusted baseline comparison
- `116-121` [low] **linked x1** — cross-tabulate position category by skin-tone group, normalized within group, as a confounding diagnostic
- `133-138` [high] **linked x4** — specify the covariate set for the primary adjusted logistic model
- `139-145` [high] **linked x5** — fit the primary model with standard errors clustered by player instead of treating dyads as independent
- `169-171` [medium] **linked x3** — exponentiate the darkSkin coefficient and its CI to report an adjusted odds ratio as a secondary estimand
- `188-201` [high] **linked x5** — estimate the adjusted risk difference via g-computation: set darkSkin to 1 and to 0 for every row, predict, average, and difference
- `207-234` [high] **linked x2** — propagate the logistic coefficient's CI endpoints through the g-computation transform via the delta method to get a CI for the risk difference
- `251-254` [high] **linked x2** — fit a minimally-adjusted sensitivity model controlling only for games played
- `261-267` [high] **linked x2** — refit excluding yellowCards and goals to check whether behavior covariates possibly on the causal pathway drive the result
- `275-291` [high] **linked x1** — collapse dyad-level rows to one row per player, summing count variables and taking the first value for time-invariant ones
- `292-299` [high] **linked x3** — fit a Poisson model of total red cards on darkSkin at the player level with log(games) as an exposure term
- `308` [high] **linked x1** — for the continuous-exposure sensitivity check, keep all dyads with any non-missing skin-tone rating instead of only the extremes
- `313-314` [medium] **SILENT** — drop remaining dyads missing height or weight before fitting the continuous-exposure model
- `315-322` [high] **linked x2** — refit the adjusted logistic model treating skin tone as a continuous exposure instead of a dichotomized one
- `348` [low] **linked x1** — compute the percentage of dyads missing a skin-tone rating to characterize potential selection bias
