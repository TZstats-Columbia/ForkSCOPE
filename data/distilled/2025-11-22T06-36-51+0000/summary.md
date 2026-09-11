# 2025-11-22T06-36-51+0000  (ai)

- code: 367 lines, 17% exon (64 lines in 13 decisions)
- intron: print 188, plot 62, comment 39, import 8, config 3, glue 3
- prose: 306 lines, 134 claims (51 action, 83 result)
- links: 28 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 20
- R_only_consistent_negative: 9
- result_claims_deferred: 83

## All decisions

- `30-31` [high] **linked x1** — pull the full soccer player-referee dyad table from disk as the analysis universe
- `34-35` [high] **linked x1** — drop dyads that lack a skin-tone rating from either rater before any further analysis
- `38-41` [high] **linked x2** — collapse the two raters' scores into one skin-tone value by averaging them
- `45-47` [high] **linked x2** — collapse red-card counts into a binary any-red-card outcome
- `48-50` [high] **linked x3** — dichotomize the continuous skin-tone score into dark vs light groups at the 0.5 midpoint
- `51-57` [high] **linked x2** — restrict the modeling sample to complete cases by dropping dyads missing position, height, or weight
- `106-113` [high] **linked x10** — specify the primary outcome model as a linear probability model of any-red-card on dark-skin exposure adjusted for games, position, league country, height, and weight, fit with heteroscedasticity-robust (HC3) standard errors
- `132, 159, 346` [medium] **linked x1** — apply a fixed 0.05 p-value cutoff to label an estimate as statistically significant
- `142-149` [high] **linked x1** — refit the same darkSkin/covariate specification as a logistic regression to report an odds ratio instead of a risk difference
- `170-178` [high] **linked x1** — restrict to players rated at the extreme ends of the skin-tone scale and redefine exposure as top vs bottom extreme category, refitting the adjusted LPM to check robustness of the 0.5 cutpoint
- `189-194` [high] **linked x1** — re-run the adjusted model treating skin tone as a continuous exposure instead of a dichotomized one
- `204-209` [high] **linked x1** — add a darkSkin-by-games interaction term to test whether the exposure effect changes with number of games played
- `358, 360-361` [high] **linked x2** — state the overall conclusion as a fixed 'SUPPORTED' verdict rather than a statement conditioned on the significance results computed above
