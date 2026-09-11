# 2025-11-20T20-25-41+0000  (ai)

- code: 352 lines, 36% exon (125 lines in 14 decisions)
- intron: print 146, comment 38, glue 24, import 11, other 6, config 2
- prose: 190 lines, 81 claims (37 action, 44 result)
- links: 59 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 1
- R_only_consistent_negative: 9
- result_claims_deferred: 44

## Misaligned — code and prose disagree

- code: specifies and fits a logistic regression of red cards on dark-skin exposure adjusting for games, position, league country, height and weight, with standard errors clustered by player
  - prose: referee country and league country were controlled for instead of referee fixed effects
  - why: claim states referee country was controlled for, but the model's covariates include only league country, not referee country

## All decisions

- `33-34` [high] **linked x2** — loads the raw player-referee dyad dataset from the soccer CSV file as the full analysis population
- `37-38` [high] **linked x1** — averages the two raters' skin-tone scores into a single continuous skinTone measure
- `45-47, 245` [high] **linked x2** — defines any red card issued (redCards > 0) as the binary outcome, collapsing counts of multiple cards into a single flag
- `48-53, 59-61` [high] **linked x3** — splits the continuous skin-tone score at the 0.5 midpoint into light/dark bins and encodes a binary darkSkin exposure indicator
- `54-55` [high] **linked x1** — excludes dyads with no skin-tone rating from the analysis sample
- `62-63` [high] **linked x2** — restricts the sample to complete cases with non-missing height, weight, and position
- `87-88` [medium] **linked x1** — computes and reports the raw, unadjusted difference in red-card rate between dark- and light-skin groups
- `108-112, 144` [high] **linked x12** — specifies and fits a logistic regression of red cards on dark-skin exposure adjusting for games, position, league country, height and weight, with standard errors clustered by player
- `118, 121-135` [high] **linked x9** — estimates the adjusted risk difference via marginal standardization/g-computation, setting darkSkin to 1 and then 0 for the whole sample and averaging predicted probabilities
- `140, 143, 145-173` [high] **linked x9** — derives the standard error, 95% confidence interval and p-value for the risk difference using the delta method with a normal-approximation z-test
- `192-202` [high] **linked x5** — exponentiates the darkSkin logistic coefficient and its Wald confidence interval to report an adjusted odds ratio
- `224-232` [high] **linked x1** — refits the outcome model with darkSkin as the sole predictor, dropping all covariate adjustment, as an unadjusted sensitivity check
- `239-244, 246-247, 252-260` [high] **linked x3** — redefines exposure using extreme cutoffs (<=0.25 light, >=0.75 dark), drops the middle group, and refits the adjusted model on that narrower subsample
- `267-278` [high] **linked x8** — reruns the adjusted model separately within each league country, dropping the now-constant leagueCountry term, to check consistency across countries
