# 2025-11-29T04-37-04+0000  (ai)

- code: 282 lines, 41% exon (117 lines in 13 decisions)
- intron: print 118, comment 38, import 5, config 4
- prose: 285 lines, 94 claims (51 action, 43 result)
- links: 49 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 16
- R_only_consistent_negative: 15
- result_claims_deferred: 43

## Misaligned — code and prose disagree

- code: collapse the red card count into a binary any-red-card outcome
  - prose: no transformations were applied; variables used as measured in the original data
  - why: claim states no transformations were applied, but code collapses the red card count into a binary any_red_card indicator
- code: define the exposure by splitting skin tone into extreme dark (>=0.75) vs light (<0.25) groups and discarding players in the intermediate range
  - prose: no transformations were applied; variables used as measured in the original data
  - why: claim states no transformations were applied, but code dichotomizes skin tone into skin_dark at >=0.75 vs <0.25

## All decisions

- `34` [high] **linked x2** — read the raw player-referee dyad dataset from CSV as the analysis input
- `36-38` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone_avg measure
- `39-41` [high] **linked x1** — restrict to complete cases by dropping rows with missing rater1/rater2 skin-tone ratings
- `43-45` [high] **linked x2** — collapse the red card count into a binary any-red-card outcome
- `55-62` [high] **linked x5** — define the exposure by splitting skin tone into extreme dark (>=0.75) vs light (<0.25) groups and discarding players in the intermediate range
- `63-67` [high] **linked x4** — assemble the final analytic sample by selecting the outcome, exposure, and covariate columns and dropping rows with any remaining missing covariate
- `108-113` [high] **linked x3** — specify and fit the primary model as logistic regression of any_red_card on skin_dark adjusting for games, yellowCards and position
- `122-131` [high] **linked x3** — convert the logistic coefficient for skin_dark into an odds ratio with a confidence interval, to be reported as the secondary effect measure
- `137-146` [high] **linked x11** — compute the average marginal effect (risk difference) for skin_dark via dydx margins and treat it as the primary effect measure
- `192-203` [high] **linked x3** — declare the hypothesis 'supported' using a significance threshold of p<0.05 combined with a risk-difference confidence interval that excludes zero
- `212-241` [high] **linked x8** — re-run the exposure/outcome model under two alternative extreme-threshold cutoffs as a robustness check, only reporting a cutoff's result if its resulting sample exceeds 1000 rows
- `242-255` [high] **linked x5** — refit the model using continuous skinTone_avg in place of the binarized exposure, on the full complete-case sample
- `256-267` [high] **linked x1** — add leagueCountry as an additional adjustment covariate to the primary model as a further robustness check
