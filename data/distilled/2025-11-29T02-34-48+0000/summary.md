# 2025-11-29T02-34-48+0000  (ai)

- code: 446 lines, 30% exon (132 lines in 16 decisions)
- intron: print 196, comment 57, plot 46, import 8, config 5, glue 2
- prose: 269 lines, 150 claims (70 action, 80 result)
- links: 79 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 28
- R_only_consistent_negative: 11
- result_claims_deferred: 80

## Misaligned — code and prose disagree

- code: restrict to extreme skin-tone dyads (<=0.25 or >=0.75), dropping the middle band, and binarize the exposure as isDark
  - prose: 17,015 dyads with medium skin tone (0.375-0.625) were excluded
  - why: code excludes the (0.25,0.75) middle band (light 0-0.25, dark 0.75-1.0); claim states the excluded medium range as 0.375-0.625
- code: specify the confirmatory logistic regression and its adjustment set (games, position, league country)
  - prose: the slight differences in games and yellow cards between groups are controlled for in the adjusted analysis
  - why: primary adjustment set is games, position, league; it does not include yellow cards, contrary to the claim that yellow-card differences are controlled in the adjusted analysis

## All decisions

- `35-36` [high] **linked x1** — pick the input dataset and its path as the analysis population
- `39-40` [high] **linked x2** — average the two independent raters' scores into a single continuous skin-tone measure
- `50-52` [high] **linked x6** — drop dyads with missing skin-tone data before any modeling
- `55-72` [medium] **linked x1** — collapse free-text playing positions into five coarse categories via keyword matching, then apply the mapping
- `73-75` [high] **linked x2** — define the binary outcome as whether any red card occurred in the dyad
- `84-93` [high] **linked x11** — restrict to extreme skin-tone dyads (<=0.25 or >=0.75), dropping the middle band, and binarize the exposure as isDark
- `108-112` [low] **linked x4** — compute crude (unadjusted) red-card rates by group as a descriptive baseline comparison
- `122-129` [low] **linked x5** — choose which covariates (games, cards, height, weight) to tabulate by exposure group for sample characterization
- `140-147` [high] **linked x9** — specify the confirmatory logistic regression and its adjustment set (games, position, league country)
- `161-170` [high] **linked x7** — extract the average marginal effect of isDark (via a hardcoded parameter index) as the primary risk-difference estimand and build its normal-approximation CI
- `171-173, 361-381` [high] **linked x9** — adopt a two-sided p<0.05 rule and use it, together with the sign of the risk difference, to declare the hypothesis supported or not
- `181-186` [medium] **linked x4** — convert the isDark logit coefficient into an odds ratio with CI as a secondary estimand
- `241, 243-247` [medium] **linked x4** — refit the primary model with standard errors clustered by player as a robustness check
- `253, 255-257` [medium] **linked x5** — re-specify exposure as continuous skin tone over the full (non-restricted) sample as an alternative operationalization
- `263, 265-268` [medium] **linked x4** — swap in a Poisson count model of red cards with games as exposure offset as an alternative model family
- `273, 275-291` [medium] **linked x5** — compare the isDark effect across a ladder of alternative adjustment sets (none, games only, games+position)
