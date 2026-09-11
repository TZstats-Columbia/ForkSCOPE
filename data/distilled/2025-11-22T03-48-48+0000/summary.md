# 2025-11-22T03-48-48+0000  (ai)

- code: 409 lines, 35% exon (144 lines in 18 decisions)
- intron: print 161, comment 49, plot 38, import 10, config 4, glue 3
- prose: 272 lines, 133 claims (43 action, 90 result)
- links: 84 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 2
- result_claims_deferred: 90

## All decisions

- `36-38` [high] **linked x3** — read the player-referee dyad csv as the raw input dataset
- `40-42` [high] **linked x2** — average the two raters' scores into one continuous skin-tone measure
- `43-46` [medium] **linked x2** — assess rater agreement via Pearson correlation and exact-match rate on dyads both raters scored
- `49-51` [high] **linked x1** — drop dyads with no averaged skin-tone value
- `53-63` [high] **linked x6** — collapse the continuous skin-tone scale into Light (<=0.25) vs Dark (>=0.75) groups, discarding the middle range
- `64-66, 285` [high] **linked x2** — flag a dyad as having any red card whenever the red-card count exceeds zero
- `75-77, 280` [high] **linked x3** — restrict the analysis sample to dyads with non-missing height, weight and position
- `79-83, 281-282` [high] **linked x2** — z-score standardize height and weight for use as covariates
- `84, 283` [medium] **linked x3** — log-transform games played to form the games covariate
- `85-95, 284` [high] **linked x1** — collapse detailed position labels into four coarse groups (Goalkeeper/Defender/Midfielder/Forward)
- `121-127` [low] **linked x1** — choose which covariates (games, yellow cards, height, weight) to compare descriptively across skin-tone groups
- `136-143` [high] **linked x21** — specify and fit the primary logistic model of any_red_card on dark_skin adjusting for games, position group, league country, height and weight, with Goalkeeper/England as reference levels
- `177-191` [high] **linked x10** — estimate the primary effect by g-computation: predict each dyad's probability under a forced dark-skin value and a forced light-skin value and difference the averaged predictions
- `197-198, 200-241` [medium] **linked x6** — obtain uncertainty for the g-computation risk difference via a parametric bootstrap: simulate the model's coefficient vector 5000 times from a multivariate normal, recompute the risk difference each draw, then take percentiles/SD and a z-test from the simulated distribution
- `251, 269, 390` [medium] **linked x3** — set significance star tiers (p<0.05/0.01/0.001) and require p<0.05 with a positive risk difference to label the hypothesis supported
- `260-263` [high] **linked x10** — report the exposure effect on the odds-ratio scale by exponentiating the dark_skin coefficient and its CI
- `278-279, 286-292` [high] **linked x7** — as a sensitivity check, refit the same adjustment set with skinTone entered as a continuous exposure on the full, non-binarized sample
- `328` [low] **linked x1** — cap the red-card-rate bar chart's y-axis at a fixed 0-2% range
