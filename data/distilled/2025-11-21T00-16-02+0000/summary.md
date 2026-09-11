# 2025-11-21T00-16-02+0000  (ai)

- code: 314 lines, 33% exon (103 lines in 14 decisions)
- intron: print 103, comment 47, plot 40, glue 10, import 8, config 3
- prose: 247 lines, 100 claims (60 action, 40 result)
- links: 57 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 17
- result_claims_deferred: 40

## Misaligned — code and prose disagree

- code: define the secondary effect measure as the conditional odds ratio obtained by exponentiating the darkSkin coefficient and its Wald CI, rather than a marginal/standardized OR
  - prose: secondary estimand (odds ratio) confidence interval was obtained via profile likelihood from the logistic regression model
  - why: claim states the OR CI was obtained via profile likelihood; code exponentiates the darkSkin coefficient's Wald confidence interval

## All decisions

- `28` [high] **linked x2** — pick the input dataset and file path that defines the full analysis population
- `34-36` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `37-41` [high] **linked x4** — dichotomize continuous skin tone into dark vs light using a 0.5 cutoff, keeping missing skin tone as NaN
- `42-44` [high] **linked x3** — collapse red-card counts into a binary any-red-card outcome
- `49-50` [high] **linked x1** — restrict the analysis population to dyads that have non-missing skin-tone data
- `53-56` [high] **linked x3** — drop dyads with any missing outcome/covariate values, i.e. use complete-case analysis rather than imputation
- `76-83` [medium] **linked x1** — compute the crude (unadjusted) red-card-rate difference between dark- and light-skin groups as a comparison baseline
- `98-107` [high] **linked x11** — choose which covariates enter the model (games, height, weight, position, league country), one-hot encode categoricals with a dropped reference level, and add an intercept
- `108-110, 116, 118-119` [high] **linked x3** — correct standard errors for within-player dependence by clustering on player rather than assuming independent dyads
- `117` [high] **linked x2** — specify the outcome model as a logistic (binomial-family) GLM rather than another functional form
- `131-148` [high] **linked x10** — estimate the adjusted risk difference by g-computation: score every dyad under forced dark-skin and forced light-skin values, average predicted probabilities, and scale the difference to percentage points
- `159-189` [high] **linked x9** — quantify uncertainty for the risk difference via a parametric bootstrap over the fitted coefficient distribution (1000 draws), taking the 2.5/97.5 percentile CI, the draw SD as SE, and a two-sided proportion-based p-value
- `203-210` [high] **linked x6** — define the secondary effect measure as the conditional odds ratio obtained by exponentiating the darkSkin coefficient and its Wald CI, rather than a marginal/standardized OR
- `226, 246, 306` [medium] **linked x1** — adopt a 0.05 two-sided significance threshold to characterize and report whether the risk-difference estimate counts as statistically significant
