# 2025-11-16T21-46-30+0000  (ai)

- code: 403 lines, 39% exon (156 lines in 17 decisions)
- intron: print 132, comment 53, plot 48, import 7, config 5, glue 2
- prose: 179 lines, 72 claims (41 action, 31 result)
- links: 45 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 10
- result_claims_deferred: 31

## Silent decisions — executed, never disclosed

- **147-151** [medium] approximate the AME's standard error via a delta-method scaling of the logit coefficient's SE
- **293-309** [medium] compute the red-card rate and a normal-approximation 95% CI separately for every distinct observed skin-tone value

## All decisions

- `35-36` [high] **linked x3** — load the raw player-referee dyad dataset from CSV as the analysis source
- `39-41` [high] **linked x1** — average the two independent raters' skin-tone scores into a single continuous skin_tone value
- `42-44` [high] **linked x1** — collapse any red-card count above zero into a binary any_red outcome flag
- `45-46` [high] **linked x2** — drop dyads that have no skin-tone rating before analysis
- `55-63` [high] **linked x7** — dichotomize skin tone using a >=0.75 vs <0.25 cutoff chosen after trying several thresholds because it discards the middle range and gives the strongest effect
- `76-93, 272` [medium] **linked x1** — bucket free-text position strings into five coarse role categories via keyword matching
- `96-97, 325` [medium] **linked x1** — split the sample into dark and light subsets to compute the raw, unadjusted difference in red-card rates
- `109-117` [high] **linked x7** — fit a logistic regression of any_red on dark_skin adjusting for games, position category and league country
- `132-144` [high] **linked x4** — predict outcome probabilities under counterfactual all-dark and all-light skin assignments and average the gap into an AME
- `147-151` [medium] **SILENT** — approximate the AME's standard error via a delta-method scaling of the logit coefficient's SE
- `163-169, 172-200, 204-207, 214-215` [high] **linked x5** — resample players with replacement 500 times, refit the model on each resample, and derive AME/OR percentile intervals and a two-sided p-value, silently skipping resamples whose fit fails
- `224-227` [medium] **linked x4** — exponentiate the dark_skin coefficient into an odds ratio and bound it with the bootstrap percentile interval
- `238-242` [high] **linked x2** — refit the primary model with player-clustered robust standard errors instead of the default covariance estimator
- `248-252` [medium] **linked x2** — swap the dichotomized exposure for the continuous skin_tone score in the regression
- `258-263` [high] **linked x2** — refit the primary model after dropping goalkeepers from the sample
- `269-271, 273-278` [high] **linked x3** — redefine the exposure at a >=0.5 midpoint split, keeping all dyads including the middle range instead of the extreme-terciles cutoff
- `293-309` [medium] **SILENT** — compute the red-card rate and a normal-approximation 95% CI separately for every distinct observed skin-tone value
