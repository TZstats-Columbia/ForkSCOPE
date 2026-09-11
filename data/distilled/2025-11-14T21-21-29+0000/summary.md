# 2025-11-14T21-21-29+0000  (ai)

- code: 366 lines, 38% exon (138 lines in 15 decisions)
- intron: print 127, comment 50, plot 41, import 7, config 2, glue 1
- prose: 209 lines, 84 claims (52 action, 32 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 14
- result_claims_deferred: 32

## All decisions

- `30-31` [medium] **linked x3** — choose the input dataset and its scope: the full set of player-referee dyads from the 2012-2013 soccer CSV
- `37-40` [high] **linked x3** — average the two independent raters' skin-tone scores into a single continuous skinTone measure
- `41-43` [high] **linked x1** — drop dyads that lack a skin-tone rating from the analysis population
- `45-47` [high] **linked x1** — collapse red-card counts into a binary any-red-card outcome per dyad
- `57-68` [high] **linked x8** — bin continuous skin tone into light/dark exposure groups at 0.25/0.5 cutpoints, dropping the intermediate band, and encode the result as a binary indicator
- `74-77` [medium] **linked x1** — compute the crude (unadjusted) red-card rate difference between skin tone groups as a comparison point before adjustment
- `92-111` [high] **linked x1** — collapse detailed position strings into five broad position categories via keyword-matching rules
- `116-117` [high] **linked x1** — exclude dyads whose position could not be categorized
- `118-121` [high] **linked x2** — one-hot encode position and league-country categoricals with a reference level dropped
- `122-124` [high] **linked x1** — drop dyads missing the referee-country implicit bias score
- `139-154` [high] **linked x7** — choose the adjustment set / design matrix for the regression: exposure, game count, position dummies, league dummies, and implicit-bias score, with an added intercept
- `155-162` [high] **linked x5** — fit a logistic regression model for any-red-card with standard errors clustered by player
- `176-188` [high] **linked x6** — derive the primary effect estimate as a marginal risk difference from counterfactual all-light vs all-dark predicted probabilities
- `194-196, 198-230` [high] **linked x7** — quantify uncertainty on the risk difference via a parametric bootstrap that redraws coefficients from their asymptotic covariance, then derive a percentile CI and a simulation-based two-sided p-value
- `248-255` [high] **linked x6** — report the secondary effect estimate as an odds ratio by exponentiating the dark_skin coefficient and its confidence interval
