# 2025-11-20T06-03-23+0000  (ai)

- code: 479 lines, 43% exon (206 lines in 21 decisions)
- intron: print 199, comment 56, import 10, config 6, glue 2
- prose: 314 lines, 161 claims (55 action, 106 result)
- links: 70 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 8
- result_claims_deferred: 106

## Silent decisions — executed, never disclosed

- **399-403, 411, 418-419** [medium] assess whether missingness in skin-tone photos is related to the outcome, via group comparison of red-card rates and a chi-square test

## All decisions

- `41-42` [high] **linked x2** — load the full soccer player-referee dyad dataset from a fixed CSV path
- `47-48, 336` [high] **linked x2** — keep only rows with a valid skin-tone rating before including them in an analysis
- `52-54` [high] **linked x1** — average the two raters' scores into one continuous skin-tone score per dyad
- `55-59, 123-125, 372-373` [high] **linked x5** — cut the continuous skin-tone score into Light/Medium/Dark bins at 0.25 and 0.75 and collapse that into a binary dark-skin flag
- `72-84, 104-106, 323, 338, 375` [high] **linked x1** — collapse detailed position labels into four broad role buckets (Goalkeeper/Defender/Midfielder/Forward/Other)
- `85-100` [high] **linked x2** — aggregate dyad-level rows to one row per player, taking the first value for fixed attributes and summing counts across the season
- `101-103, 404` [high] **linked x3** — define the outcome as binary: whether a player received at least one red card
- `121-122, 374` [high] **linked x4** — drop the Medium skin-tone group and restrict the comparison to Light vs Dark only
- `126-128, 322, 337, 377` [medium] **linked x1** — log-transform total games played, used either as a covariate or as a model offset for playing-time exposure
- `129-132, 324, 339, 376` [high] **linked x3** — drop players/dyads missing any adjustment covariate (complete-case analysis)
- `149-151` [low] **linked x3** — compute the crude (unadjusted) risk difference between dark- and light-skinned groups as a comparison point
- `172-174, 236-238, 328, 360-361` [high] **linked x3** — specify and (re)fit a logistic regression of the red-card outcome on dark_skin adjusting for position, league, and log games (league dropped when stratifying by league)
- `179-182` [high] **linked x5** — extract the exponentiated logistic coefficient and treat it as a secondary effect measure (adjusted odds ratio)
- `200-211` [high] **linked x9** — estimate the adjusted risk difference via g-formula: predict every player's outcome under both counterfactual exposure levels and difference the averages
- `223-235, 239-261` [high] **linked x5** — quantify uncertainty in the adjusted risk difference via nonparametric bootstrap (2000 resamples, percentile CI, drop failed/NaN fits, two-sided p-value from the smaller tail proportion doubled)
- `276-304` [high] **linked x2** — cross-check the bootstrap uncertainty with a delta-method standard error, using a manually reimplemented prediction function and a numerical finite-difference gradient
- `320-321, 329-330` [high] **linked x4** — redefine the exposure contrast to only the most extreme skin-tone scores (0.0 vs 1.0) instead of the 0.25/0.75 bins, as a sensitivity check
- `340-344` [high] **linked x4** — model skin tone as a continuous predictor instead of a binarized exposure, as a sensitivity check
- `351-359, 362-368` [high] **linked x6** — refit the adjusted model separately within each league as a sensitivity check, only when both exposure groups have at least 10 players
- `381-387` [high] **linked x5** — switch to dyad-level unit of analysis with a Poisson GLM of red-card counts, using log(games) as an offset rather than a covariate, as a sensitivity check
- `399-403, 411, 418-419` [medium] **SILENT** — assess whether missingness in skin-tone photos is related to the outcome, via group comparison of red-card rates and a chi-square test
