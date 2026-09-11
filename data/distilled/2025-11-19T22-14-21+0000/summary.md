# 2025-11-19T22-14-21+0000  (ai)

- code: 401 lines, 39% exon (157 lines in 16 decisions)
- intron: print 125, plot 53, comment 51, import 10, config 4, glue 1
- prose: 211 lines, 94 claims (49 action, 45 result)
- links: 64 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 13
- result_claims_deferred: 45

## Silent decisions — executed, never disclosed

- **326-331** [low] hard-code the unadjusted odds ratio and its confidence interval as literal numbers in the forest-plot summary table rather than computing them from the data already in scope

## All decisions

- `37-39` [high] **linked x1** — load the raw player-referee dyad dataset from a fixed csv path
- `41-43` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `44-46, 48-49` [medium] **linked x2** — assess inter-rater agreement between the two raters using Pearson and Spearman correlation on complete-case ratings
- `54-56` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome per dyad
- `57-65` [high] **linked x6** — dichotomize skin tone into light/dark exposure groups at 0.25/0.5 cutoffs and drop the excluded middle range
- `79-82` [high] **linked x8** — restrict the analytic sample to complete cases on outcome, exposure, and the chosen covariate set
- `99-103, 109-115` [high] **linked x1** — estimate the unadjusted risk difference between groups and test it with a normal-approximation two-proportion z-test
- `136-139, 251-253, 267-269` [high] **linked x10** — fit a logistic regression of anyRedCard on the exposure adjusted for games, position, leagueCountry, yellowCards, and goals
- `142-147, 254-257, 270-273` [high] **linked x6** — define the reported effect as the exponentiated logistic coefficient (odds ratio) together with a Wald-based confidence interval
- `162-175` [high] **linked x8** — derive the primary risk-difference estimate by marginal standardization: predict outcomes for the whole sample set uniformly to dark and to light, then average the difference
- `185-220, 224-226` [high] **linked x5** — obtain the risk-difference confidence interval and p-value via a 500-draw parametric bootstrap sampling model parameters from their asymptotic covariance matrix
- `236-237, 239-248` [high] **linked x1** — re-derive the exposure using more extreme skin-tone cutoffs (0.125/0.75) as a sensitivity check on the threshold choice
- `261-262, 264-266` [high] **linked x3** — re-specify the exposure as continuous skin tone instead of the binary light/dark category, as a sensitivity check
- `326-331` [low] **SILENT** — hard-code the unadjusted odds ratio and its confidence interval as literal numbers in the forest-plot summary table rather than computing them from the data already in scope
- `372-374` [medium] **linked x4** — compute alternate effect-size framings (baseline rate, absolute percentage-point difference, relative percent increase) for the narrative interpretation
- `384-398` [high] **linked x5** — classify the hypothesis as supported, not supported, or inconclusive using p<0.05 combined with a strictly positive CI lower bound as the significance rule
