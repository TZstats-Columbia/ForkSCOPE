# 2025-11-22T11-14-05+0000  (ai)

- code: 418 lines, 29% exon (122 lines in 19 decisions)
- intron: print 175, glue 65, comment 42, import 6, config 4, other 4
- prose: 328 lines, 117 claims (52 action, 65 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 16
- R_only_consistent_negative: 3
- result_claims_deferred: 65

## All decisions

- `29-30` [medium] **linked x2** — read the full player-referee dyad file as the analysis population, with no upfront row filtering
- `34-36` [high] **linked x2** — average the two independent raters' skin-tone scores into a single continuous score
- `41-49` [high] **linked x2** — cut the continuous skin-tone score into three fixed-cutoff ordinal bands (Light ≤0.25, Middle, Dark ≥0.75)
- `53-55` [high] **linked x5** — dichotomize the red card count into a yes/no outcome for the dyad
- `67-69` [high] **linked x4** — drop the Middle skin-tone band and restrict the sample to only Light vs Dark dyads
- `70-72` [medium] **linked x1** — recode the Dark/Light grouping into a 0/1 exposure dummy for modeling
- `73-75, 240, 253, 270` [high] **linked x2** — impute missing player position values into their own 'Missing' category rather than dropping those rows
- `91-95` [medium] **linked x1** — compute the crude (unadjusted) red-card rate difference and rate ratio between dark- and light-skinned players
- `110-114, 121-125` [high] **linked x9** — specify and fit the primary logistic regression of any red card on the dark-skin dummy, adjusting for games, position, and league country, with player-clustered robust standard errors
- `139-154` [high] **linked x5** — derive the adjusted risk difference as an average marginal effect by predicting outcomes under counterfactual all-light and all-dark exposure, rather than reading the risk difference off the raw logit coefficient
- `155-162` [high] **linked x1** — approximate the marginal risk difference's standard error and 95% CI with a delta-method formula and a normal (1.96) critical value
- `178-181` [medium] **linked x2** — exponentiate the logit coefficient and its CI into an odds ratio, reported as a secondary estimand
- `234-235, 237-239, 241-244` [high] **linked x2** — refit the model keeping all three skin-tone bands (only dropping missing skin group) as a sensitivity check on the exclusion of the Middle group
- `249-250, 252, 254-259` [high] **linked x2** — refit using the continuous 0-1 skin-tone score instead of a categorical split, as a sensitivity check on the categorization decision
- `265-266, 268-269, 271-274` [high] **linked x2** — restrict to only the most extreme rater scores (exactly 0.0 vs exactly 1.0) as an extreme-contrast sensitivity check
- `280-281, 283-289` [medium] **linked x4** — compute unadjusted risk differences separately within each league country as a subgroup/heterogeneity check
- `291-292, 294, 295-298` [high] **linked x3** — swap in yellow cards as a falsification/negative-control outcome in place of red cards, using the same adjusted model spec
- `370` [medium] **linked x1** — flag rows as statistically significant using a p<0.05 threshold
- `388-390, 393-394, 398-399` [high] **linked x3** — classify the overall conclusion as supported / not supported / inconclusive using a compound rule of p<0.05 AND the odds-ratio CI lower bound exceeding 1
