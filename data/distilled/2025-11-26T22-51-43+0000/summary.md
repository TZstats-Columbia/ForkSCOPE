# 2025-11-26T22-51-43+0000  (ai)

- code: 246 lines, 37% exon (91 lines in 16 decisions)
- intron: print 93, comment 39, glue 11, import 6, config 6
- prose: 265 lines, 106 claims (69 action, 37 result)
- links: 44 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 19
- R_only_consistent_negative: 20
- result_claims_deferred: 37

## All decisions

- `28-29` [high] **linked x2** — load the raw player-referee dyad dataset from a specific fixed file, fixing the source and season/league scope of the whole analysis
- `30-32` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `33-34` [high] **linked x1** — drop dyads that have no skin-tone rating at all
- `41-58` [high] **linked x1** — collapse free-text position strings into five coarse position buckets via keyword rules, then apply it to every player
- `59-63` [high] **linked x1** — fill missing referee implicit-bias scores with the mean score for that referee's country rather than dropping them
- `68-69` [high] **linked x3** — restrict the modeling dataset to dyads with complete height, weight, and filled IAT values
- `72-75` [high] **linked x2** — z-score standardize height, weight, and filled IAT before entering them as covariates
- `76-77` [high] **linked x2** — log-transform games played to represent exposure time in the model
- `78-80` [high] **linked x4** — define the binary outcome as having received at least one red card or yellow-red card
- `81-83` [high] **linked x4** — exclude goalkeepers from the analytic sample on the grounds that their game dynamics differ
- `99-105` [high] **linked x7** — specify and fit a logistic regression of the serious-card outcome on continuous skin tone, adjusting for exposure time, size, position, league, yellow cards and referee bias
- `117-131` [high] **linked x4** — fix skin tone at two reference values (0.125 and 0.75, described as ~30th/90th percentiles), predict outcome probability at each, and take the difference as the adjusted risk difference
- `137-143, 147, 149-150` [medium] **linked x4** — approximate the standard error, 95% CI and two-sided p-value of the risk difference with a delta-method-style expansion off the model's coefficient SE, rather than e.g. bootstrapping
- `161-162, 168-172` [high] **linked x2** — dichotomize skin tone at a 0.25 cutoff into a dark/light exposure and refit the logistic regression on that binary exposure with the same covariate set as the primary model
- `176-177` [medium] **linked x2** — exponentiate the binary-exposure coefficient and its CI to report the effect as an odds ratio rather than a log-odds
- `227-232` [high] **linked x3** — declare the hypothesis 'supported' only if the risk-difference p-value is below 0.05, the estimate is positive, and the CI lower bound exceeds zero
