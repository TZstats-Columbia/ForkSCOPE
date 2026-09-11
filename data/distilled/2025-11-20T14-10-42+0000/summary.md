# 2025-11-20T14-10-42+0000  (ai)

- code: 232 lines, 25% exon (57 lines in 13 decisions)
- intron: print 90, comment 75, import 6, config 4
- prose: 172 lines, 78 claims (43 action, 35 result)
- links: 34 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 8
- result_claims_deferred: 35

## All decisions

- `29` [medium] **linked x3** — load the raw player-referee dyad dataset from a fixed CSV path
- `33` [high] **linked x2** — drop dyads lacking a skin-tone rating from either rater before analysis
- `44` [high] **linked x2** — average the two raters' skin-tone scores into one continuous measure
- `49` [high] **linked x3** — dichotomize the averaged skin-tone score into dark vs. light skin using a 0.25 cutoff
- `52` [high] **linked x2** — collapse the red-card count into a binary indicator for any red card in the dyad
- `55-70` [high] **linked x2** — collapse detailed playing positions into four broader groups, bucketing unmapped positions as Other
- `73-75, 108` [high] **linked x4** — represent games played with a flexible 4-df natural cubic spline instead of a linear term
- `94-97` [medium] **linked x2** — compute and report the raw (unadjusted) red-card-rate gap between dark- and light-skin players
- `109, 112` [high] **linked x3** — specify the primary model as a logistic regression of any red card on dark skin, the games spline, league, and position group
- `128-129, 132-137` [high] **linked x4** — use the average marginal effect of dark_skin (evaluated overall) as the primary risk-difference estimand
- `155-158` [high] **linked x3** — report the exponentiated dark_skin coefficient as an adjusted odds ratio secondary estimand
- `174, 177-178, 181-190` [high] **linked x2** — refit the model replacing the games spline with log(games) as a robustness check and recompute the risk difference and odds ratio
- `226` [high] **linked x2** — declare the hypothesis 'supported' only if the risk-difference p-value is below 0.05 and the CI lower bound exceeds zero
