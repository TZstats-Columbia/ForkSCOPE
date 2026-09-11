# 2025-11-19T19-09-24+0000  (ai)

- code: 392 lines, 39% exon (152 lines in 15 decisions)
- intron: print 112, plot 61, comment 47, import 12, config 4, glue 4
- prose: 302 lines, 141 claims (53 action, 88 result)
- links: 66 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 13
- result_claims_deferred: 88

## Silent decisions — executed, never disclosed

- **36** [high] point the whole analysis at one specific CSV file as the raw player-referee dyad data
- **82-92** [medium] report the raw, unadjusted difference in red-card rate between the two skin-tone groups before any modeling

## All decisions

- `36` [high] **SILENT** — point the whole analysis at one specific CSV file as the raw player-referee dyad data
- `39-41` [high] **linked x2** — collapse the two skin-tone raters into a single continuous score by simple averaging
- `42-48` [low] **linked x2** — quantify rater agreement with a Pearson correlation and an exact-match percentage between the two raters
- `49-54, 58-61, 62-64, 113` [high] **linked x5** — split continuous skin tone into Light/Dark buckets at the 0.25 / 0.75 cutoffs, discard the unclassified middle band from the analytic sample, and encode the surviving group as a 0/1 darkSkin exposure
- `55-57` [high] **linked x2** — reduce the red-card count in each dyad to a yes/no indicator of any red card
- `82-92` [medium] **SILENT** — report the raw, unadjusted difference in red-card rate between the two skin-tone groups before any modeling
- `99-100, 136-137` [high] **linked x7** — settle on which covariates enter the regression (position, league, games, height, weight) plus the player/referee IDs kept for clustering and reporting
- `101` [high] **linked x3** — drop any dyad missing a covariate instead of imputing it, i.e. complete-case analysis
- `125-127, 134-135, 138-143` [high] **linked x8** — fit the outcome with a logistic regression estimated by MLE, using standard errors clustered on player to account for repeated dyads per player
- `149-161` [high] **linked x6** — translate the fitted model into an average marginal effect and treat that percentage-point risk difference as the headline result
- `172-176, 203-207, 369-377` [high] **linked x5** — use a two-sided p<0.05 cutoff to call a result significant, and build the final verdict (supported / not supported / inconclusive) off that cutoff plus whether the CI crosses zero
- `185-196` [high] **linked x4** — re-express the same fitted coefficient as an odds ratio and present it as a second effect measure alongside the risk difference
- `216-229` [high] **linked x5** — re-run the adjusted model after dropping Center Backs, the position with the most red cards, to check whether they drive the result
- `230-252` [high] **linked x13** — refit the model separately inside each league, only when a league clears 500 dyads and 20 red cards, dropping the now-constant league covariate within each fit
- `253-268` [high] **linked x4** — add a darkSkin-by-league interaction to test for effect modification and pick which three interaction terms (each league vs. England) to report
