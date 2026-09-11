# 2025-11-17T18-58-32+0000  (ai)

- code: 344 lines, 32% exon (110 lines in 15 decisions)
- intron: print 108, comment 58, plot 48, glue 10, import 8, config 2
- prose: 171 lines, 88 claims (31 action, 57 result)
- links: 35 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 8
- result_claims_deferred: 57

## Silent decisions — executed, never disclosed

- **305** [medium] draw the 0.5 dichotomization cutoff as a reference line on the skin tone histogram
- **314** [low] exclude players with missing position from the by-position red card rate chart

## All decisions

- `29-30` [medium] **linked x1** — choose the source file and scope of the raw dataset to load
- `43-44` [high] **linked x2** — drop dyads lacking both skin-tone ratings from the analysis sample
- `49-51` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `52-54` [high] **linked x4** — dichotomize continuous skin tone into Light/Dark at the 0.5 midpoint
- `64-65` [high] **linked x3** — define the outcome as any red card (redCards > 0) within the dyad
- `85-87` [high] **linked x2** — log-transform number of games to represent exposure
- `88-91` [high] **linked x3** — impute missing height/weight with the median and recode missing position as its own 'Missing' category
- `99-109` [high] **linked x4** — choose the covariate adjustment set and encode position/league as dummy variables (dropping first level) to build the design matrix
- `122-129` [high] **linked x2** — fit a logistic regression model with standard errors clustered by player
- `142-153` [high] **linked x3** — estimate the adjusted risk difference via g-computation: predict outcome under counterfactual all-light and all-dark skin tone and average
- `163-204` [high] **linked x4** — derive the risk difference's standard error via the delta method (numerical gradient through the g-computation) and use it with a normal approximation to build a 95% CI and two-sided p-value
- `219-226` [high] **linked x3** — report a secondary effect measure by exponentiating the model's skin-tone coefficient and its Wald CI into an odds ratio
- `275-282` [high] **linked x3** — translate the p-value and CI sign into a supported/not-supported conclusion using a 0.05 significance threshold
- `305` [medium] **SILENT** — draw the 0.5 dichotomization cutoff as a reference line on the skin tone histogram
- `314` [low] **SILENT** — exclude players with missing position from the by-position red card rate chart
