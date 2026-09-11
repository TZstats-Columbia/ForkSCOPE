# 2025-11-20T01-31-19+0000  (ai)

- code: 287 lines, 32% exon (92 lines in 15 decisions)
- intron: print 100, comment 82, import 8, config 4, glue 1
- prose: 207 lines, 96 claims (33 action, 63 result)
- links: 47 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 7
- result_claims_deferred: 63

## Silent decisions — executed, never disclosed

- **106** [medium] report the crude, unadjusted red-card rate split by skin-tone group before any covariate adjustment

## All decisions

- `38` [high] **linked x3** — pick the source file and population of dyads to load as the analysis universe
- `42` [high] **linked x1** — collapse the two independent rater scores into a single continuous skin-tone measure by averaging them
- `45` [high] **linked x1** — throw out dyads lacking any rater-assigned skin tone rather than imputing them
- `50` [high] **linked x2** — collapse dyad-level red card counts into a binary any-red-card outcome rather than modeling counts
- `53` [high] **linked x2** — cut the continuous skin-tone average into a binary dark/light exposure at the 0.5 midpoint
- `56` [high] **linked x1** — put games played on a log scale before using it as a covariate
- `59-69` [high] **linked x1** — derive player age by anchoring birthdate to the 2012-08-01 season start rather than e.g. season midpoint or data date, with parse failures set to missing
- `72-74, 132-134` [high] **linked x11** — settle on the adjustment covariate set (games, position, league, cards, referee bias measures, height/weight/age) and restrict the sample to dyads complete on all of them, then carry that same set into the regression specification
- `97-99` [medium] **linked x1** — characterize rater agreement using correlation, exact match, and a within-0.25 tolerance band rather than e.g. a formal kappa statistic
- `106` [medium] **SILENT** — report the crude, unadjusted red-card rate split by skin-tone group before any covariate adjustment
- `139-143` [high] **linked x3** — fit the exposure-outcome relationship as a logistic regression and treat within-player observations as correlated by clustering standard errors on player rather than assuming independence
- `155-162` [high] **linked x6** — summarize the exposure effect on the odds scale by exponentiating the fitted coefficient and its confidence bounds
- `178-182, 185-186, 189-191` [high] **linked x7** — obtain the adjusted risk difference by g-computation/standardization: set every dyad's exposure to light then dark, predict from the fitted model each time, and average the predicted probabilities to get the primary effect estimate, rather than reading the difference off a single coefficient
- `200-240` [high] **linked x4** — quantify uncertainty on the risk difference via a 2000-draw parametric bootstrap that samples coefficients from their asymptotic multivariate normal distribution, recomputes the standardized risk difference for each draw, and takes percentile bounds and a simulation-based two-sided p-value, instead of e.g. a delta-method or nonparametric bootstrap
- `276` [high] **linked x4** — declare the hypothesis supported only if both the p-value clears the 0.05 significance threshold and the bootstrap interval excludes zero on the harmful side
