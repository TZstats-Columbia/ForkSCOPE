# 2025-11-26T17-46-30+0000  (ai)

- code: 271 lines, 42% exon (114 lines in 15 decisions)
- intron: print 92, comment 47, glue 7, import 6, config 5
- prose: 262 lines, 99 claims (52 action, 47 result)
- links: 55 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 9
- result_claims_deferred: 47

## All decisions

- `34` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path
- `44-45` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `48, 56` [high] **linked x2** — drop dyads with no skin-tone rating available
- `49-50, 53-55, 58, 206-208, 213` [high] **linked x4** — require at least 3 games in a dyad to keep it in the sample, later re-testing the cutoff at 4 games
- `51-52, 57, 198-200, 205` [high] **linked x3** — exclude goalkeepers from the analysis sample, later re-testing with goalkeepers included
- `71-75, 201, 209, 214-215, 217-218` [high] **linked x7** — binarize skin tone into dark/light exposure at a 0.25 cutoff, later re-testing a 0.375 cutoff
- `76-78, 202, 210` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome
- `81-83, 203, 211` [medium] **linked x1** — group specific field positions into a single defensive-position indicator covariate
- `84, 204, 212, 219-222` [high] **linked x4** — add a squared games term to allow a curved games effect, later re-testing a linear-only games specification
- `85-88` [medium] **linked x1** — fill missing height/weight values with the sample median instead of dropping those rows
- `129-137, 180-187` [high] **linked x8** — fit dyad outcome with logistic regression on dark+games+games_sq+pos_defensive, clustering standard errors by player
- `138-147, 188-194, 223-227` [high] **linked x9** — report the average marginal effect (risk difference) with its own SE/CI/p-value as the primary effect size, rather than the raw logit coefficient
- `156` [medium] **linked x1** — bucket the p-value into significance stars at 0.001/0.01/0.05 cutoffs for display
- `157-160` [medium] **linked x3** — additionally compute and report an odds ratio from the logit coefficient as a secondary effect measure
- `253-268` [low] **linked x7** — characterize the overall result as supporting the hypothesis and describe the sensitivity checks as robust, including a fixed baseline-risk comparison not tied to a computed variable
