# 2025-11-16T18-27-13+0000  (ai)

- code: 266 lines, 45% exon (121 lines in 18 decisions)
- intron: print 100, comment 28, import 6, config 5, glue 3, other 3
- prose: 335 lines, 75 claims (41 action, 34 result)
- links: 56 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 10
- result_claims_deferred: 34

## Misaligned — code and prose disagree

- code: refit the primary-style model across a range of alternative skin-tone cutoffs (0.125-0.75) to test sensitivity of the risk difference to the threshold choice
  - prose: an exhaustive search over thresholds from 0.125 to 0.875 was conducted and 0.25 was selected as the primary dichotomization threshold
  - why: claim states threshold search extended to 0.875; code refits over cutoffs only up to 0.75

## All decisions

- `28-29` [high] **linked x2** — load the raw soccer referee-player dyad dataset from a fixed CSV path as the full analytic universe
- `34-36` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skin_tone_avg measure
- `37-38` [high] **linked x2** — drop dyads with missing average skin-tone score from the analytic sample
- `41-45` [medium] **linked x1** — restrict to dyads with both ratings present and compute Pearson/Spearman correlation and exact agreement between the two raters as an inter-rater reliability check
- `53-55` [high] **linked x4** — collapse the red-card count into a binary any-red-card outcome
- `56-60` [high] **linked x4** — dichotomize skin tone into dark vs light using a 0.25 cutoff chosen from exploratory analysis
- `61-64` [high] **linked x1** — log-transform games played to reduce skew before using it as a covariate
- `65-68` [high] **linked x2** — impute missing height and weight with the sample median
- `69-86` [high] **linked x1** — collapse free-text position labels into five coarse position categories via keyword matching, defaulting unmatched or missing values to Unknown
- `123-130` [high] **linked x7** — specify and fit the primary logistic regression of any_red_card on dark_skin adjusted for log_games, position, league country, yellow cards, height and weight
- `131-133` [high] **linked x5** — choose average marginal effects (overall) as the estimator used to turn the logit fit into a risk-difference scale
- `134-140` [medium] **linked x4** — pull the dark_skin effect, its SE, p-value and CI out of the marginal-effects object via a hardcoded array index position
- `156-160` [high] **linked x6** — exponentiate the dark_skin logit coefficient and its CI to report an adjusted odds ratio as a secondary estimand
- `196-208` [high] **linked x3** — refit the primary-style model across a range of alternative skin-tone cutoffs (0.125-0.75) to test sensitivity of the risk difference to the threshold choice
- `209-215` [high] **linked x3** — refit with a minimal covariate set (exposure only) to test sensitivity of the effect to the adjustment set
- `219-226` [high] **linked x2** — re-specify skin tone as a continuous predictor instead of the binary indicator and fit via OLS with HC1 robust standard errors
- `230-235` [high] **linked x1** — drop dyads with only one game played and refit the primary model to check sensitivity to low-exposure dyads
- `245-262` [high] **linked x7** — declare the hypothesis supported using a two-sided p<0.05 threshold on the primary marginal effect combined with a positive-direction check, and phrase the reported conclusion accordingly
