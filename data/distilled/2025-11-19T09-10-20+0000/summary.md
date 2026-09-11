# 2025-11-19T09-10-20+0000  (ai)

- code: 339 lines, 38% exon (128 lines in 15 decisions)
- intron: print 115, plot 42, comment 36, import 8, glue 6, config 4
- prose: 296 lines, 125 claims (48 action, 77 result)
- links: 81 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 7
- result_claims_deferred: 77

## All decisions

- `29-31` [medium] **linked x4** — read the player-referee dyad CSV as the raw dataset for the whole analysis
- `33-35` [high] **linked x1** — average rater1 and rater2 into a single continuous skinTone score
- `41-44` [high] **linked x5** — threshold skinTone at 0.5 to create a binary darkSkin indicator, leaving missing skinTone as NaN
- `45-47` [high] **linked x1** — reduce redCards to a binary anyRedCard flag instead of using the count
- `48-50` [high] **linked x1** — log-transform games to build the log_games covariate
- `51-67` [high] **linked x3** — bucket the free-text position field into Goalkeeper/Defender/Midfielder/Forward/Other/Missing categories
- `68-71` [high] **linked x6** — drop dyads with missing darkSkin or missing referee meanIAT to form the analysis sample
- `96-98` [medium] **linked x5** — compute the raw (unadjusted) gap in red-card rate between dark- and light-skin groups as a percentage-point difference
- `108-110, 114-120` [high] **linked x14** — define and fit the adjustment set for the outcome model — logit of anyRedCard on darkSkin, log_games, league, position category and referee meanIAT, with standard errors clustered by player
- `130-133` [high] **linked x6** — exponentiate the darkSkin coefficient and its CI to report an odds ratio
- `149-163` [high] **linked x11** — standardize over the sample by scoring every dyad twice (forcing darkSkin to 1, then to 0) and differencing the average predicted probabilities to get the adjusted risk difference
- `176-209, 213-216, 219` [high] **linked x5** — cluster-bootstrap the risk difference by resampling players with replacement, refitting an unclustered logit and recomputing the risk difference on each of 500 resamples, silently dropping resamples where the fit fails to converge
- `225-228` [high] **linked x8** — take the 2.5/97.5 percentiles of the bootstrap distribution as the 95% CI for the risk difference
- `229-232` [medium] **linked x6** — convert the point estimate and bootstrap SD into a z-statistic and read off a normal-theory two-sided p-value instead of using the bootstrap distribution's own percentiles
- `323-334` [high] **linked x5** — declare the hypothesis supported, not supported, or inconclusive depending on whether the bootstrap CI for the risk difference excludes zero
