# 2025-11-22T01-21-47+0000  (ai)

- code: 380 lines, 26% exon (99 lines in 18 decisions)
- intron: print 136, glue 64, plot 61, import 10, comment 9, config 1
- prose: 214 lines, 113 claims (59 action, 54 result)
- links: 62 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 15
- result_claims_deferred: 54

## Silent decisions — executed, never disclosed

- **62-78, 196** [high] collapse free-text position strings into four broad role buckets (Goalkeeper/Defender/Midfielder/Forward) plus Unknown

## All decisions

- `26-27` [high] **linked x2** — load the full raw player-referee dyad dataset from CSV with no filtering
- `33-35` [high] **linked x1** — average the two raters' skin-tone ratings into a single continuous skinTone score
- `36-38` [high] **linked x1** — collapse the red card count into a binary any-red-card outcome
- `39-42` [medium] **linked x4** — restrict to dyads with both ratings present and compute inter-rater correlation as a reliability check
- `49-52` [high] **linked x6** — keep only dyads with skin tone <=0.25 or >=0.75 and flag the high end as darkSkin, discarding the middle of the scale
- `62-78, 196` [high] **SILENT** — collapse free-text position strings into four broad role buckets (Goalkeeper/Defender/Midfielder/Forward) plus Unknown
- `84-85` [high] **linked x5** — drop dyads missing any regression covariate, defining the analytic sample
- `86-88, 197` [high] **linked x3** — log-transform games played for use as an exposure-adjustment covariate
- `89-91, 198-200` [high] **linked x3** — z-score standardize yellowCards, meanIAT and meanExp before entering them as covariates
- `108-110, 112-114` [medium] **linked x2** — compute unadjusted red-card rates and their difference between the light- and dark-skin groups
- `124-132` [high] **linked x9** — specify and fit the primary logistic regression of any red card on darkSkin, adjusting for games, yellow cards, position, league and referee bias measures, with Goalkeeper/Germany as reference categories
- `144-148` [high] **linked x7** — derive the primary estimand as the average marginal effect (risk difference) of darkSkin from the fitted model
- `170-175` [high] **linked x4** — exponentiate the darkSkin coefficient and its confidence interval to report an adjusted odds ratio as a secondary estimand
- `194-195` [high] **linked x3** — rebuild the analysis sample using continuous skin tone across all players instead of the light/dark extremes, as a sensitivity check
- `201-209` [high] **linked x2** — refit the logistic model with continuous skinTone in place of the binary darkSkin indicator
- `219-224` [high] **linked x4** — refit with a minimal covariate set (darkSkin + log_games only) to test robustness of the estimate
- `225-232` [high] **linked x3** — refit with a medium covariate set (adding position and league, omitting yellow cards and bias measures) to test robustness
- `250-251` [medium] **linked x3** — translate the adjusted risk difference into a relative-increase percentage and a number-needed-to-harm figure
