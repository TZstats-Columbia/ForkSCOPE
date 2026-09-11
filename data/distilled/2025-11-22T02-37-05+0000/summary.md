# 2025-11-22T02-37-05+0000  (ai)

- code: 447 lines, 35% exon (157 lines in 19 decisions)
- intron: print 123, plot 106, comment 42, import 9, config 6, glue 4
- prose: 290 lines, 142 claims (57 action, 85 result)
- links: 97 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 6
- result_claims_deferred: 85

## All decisions

- `34-35` [high] **linked x2** — read the raw player-referee dyad CSV as the analysis input, fixing the data source and initial scope
- `39-40` [high] **linked x3** — average the two independent raters' skin-tone scores into one continuous rating
- `41-48` [high] **linked x5** — threshold continuous skin tone into a light/dark binary, dropping the middle band as missing rather than assigning it either group
- `49-51` [high] **linked x3** — collapse the red card count into a binary any-red-card outcome
- `52-69` [high] **linked x2** — collapse free-text position strings into five coarse categories via keyword matching
- `70-72` [high] **linked x3** — restrict the sample to dyads with a defined binary skin tone, dropping the excluded middle band from the working dataset
- `74-80` [high] **linked x6** — further restrict to complete cases on position, height, weight, and referee implicit-bias score
- `96-101` [low] **linked x4** — choose which variables (red-card sum/count/mean, games, yellow cards) to summarize by skin-tone group for the descriptive table and how to label the rows
- `103-107` [high] **linked x4** — compute the raw, unadjusted risk difference in red-card rate between dark- and light-skin-tone groups
- `121-133` [high] **linked x11** — specify the covariate/adjustment set for the primary model: skin tone plus games, position, league, height, weight, yellow cards, and referee implicit bias
- `134-136` [high] **linked x6** — choose logistic regression as the functional form linking the adjustment set to the red-card outcome
- `140-157` [high] **linked x19** — estimate the adjusted risk difference by g-computation/marginal standardization: predict outcomes for every dyad under counterfactual light vs. dark assignment and average the difference
- `165-168` [medium] **linked x7** — report the exponentiated skin-tone coefficient and its confidence interval as an adjusted odds ratio
- `181` [medium] **linked x2** — choose the number of parametric bootstrap draws (10,000) used for inference
- `183-198, 201-218` [high] **linked x10** — derive uncertainty for the adjusted risk difference via parametric bootstrap: draw parameter vectors from the model's asymptotic multivariate normal distribution, recompute the standardized risk difference under each draw, and take the 2.5/97.5 percentiles as a 95% CI
- `219-221` [high] **linked x4** — derive a two-sided p-value from the proportion of bootstrap draws falling on each side of zero
- `246-257` [high] **linked x1** — fit a minimally-adjusted sensitivity model (skin tone plus games only) and recompute the standardized risk difference under it
- `265-278` [high] **linked x1** — fit a sensitivity model dropping referee implicit bias (meanIAT) from the covariate set and recompute the standardized risk difference under it
- `320` [low] **linked x4** — additionally express the adjusted risk difference as a relative percent increase in red-card probability
