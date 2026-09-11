# 2025-11-29T13-19-54+0000  (ai)

- code: 362 lines, 37% exon (135 lines in 15 decisions)
- intron: print 146, glue 61, comment 10, import 6, config 4
- prose: 203 lines, 106 claims (54 action, 52 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 22
- R_only_consistent_negative: 8
- result_claims_deferred: 52

## All decisions

- `30` [medium] **linked x1** — load the player-referee dyad dataset from the fixed source csv
- `41-44` [high] **linked x5** — drop dyads where either skin-tone rater score is missing
- `47-50` [high] **linked x3** — average the two raters' scores into a single continuous skin-tone measure
- `51-54` [high] **linked x6** — dichotomize skin tone into dark vs light using a 0.25 cutoff
- `55-57` [high] **linked x3** — collapse red-card counts into a binary any-red-card outcome
- `58-63` [high] **linked x4** — drop goalkeeper dyads from the analysis sample
- `107-111, 114-117` [high] **linked x8** — fit a logistic regression of any red card on the dark-skin exposure, adjusting for position, league country, and games played
- `124-127` [high] **linked x5** — exponentiate the exposure coefficient and its CI to report an odds ratio
- `149-152, 159-177` [high] **linked x4** — standardize predictions at the mean games value and modal position/league, then difference the dark- vs light-skin predicted probabilities to obtain a risk difference in percentage points
- `192-199, 201-235` [high] **linked x5** — obtain a CI for the risk difference by simulating parameter draws from the model's asymptotic multivariate normal distribution and recomputing the risk difference for each draw
- `248, 250-254` [medium] **linked x1** — refit the primary model on the full sample including goalkeepers to test sensitivity to that exclusion
- `265, 267-271` [high] **linked x1** — refit using a 0.5 cutoff for dark skin instead of 0.25 to test sensitivity to the threshold
- `282, 284-287` [high] **linked x1** — refit using continuous skin tone as the exposure instead of the binarized version
- `298, 300-303` [high] **linked x3** — refit the primary model with HC3 heteroskedasticity-robust standard errors instead of MLE-based SEs
- `344, 346-356` [low] **linked x3** — declare the hypothesis 'supported' based on the observed effect direction and statistical significance
