# 2025-11-28T21-46-20+0000  (ai)

- code: 393 lines, 49% exon (194 lines in 20 decisions)
- intron: print 134, comment 52, config 6, import 5, glue 2
- prose: 248 lines, 91 claims (57 action, 34 result)
- links: 63 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 8
- result_claims_deferred: 34

## Silent decisions — executed, never disclosed

- **82-97** [high] collapse the many specific playing positions into three broad categories
- **136-138** [medium] compute the crude (unadjusted) red-card rate difference between dark- and light-skin groups

## All decisions

- `31-32` [high] **linked x3** — read the full raw player-referee dyad dataset from a local CSV as the analysis population
- `43-45` [high] **linked x1** — drop dyads where either skin-tone rater score is missing
- `49-51` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `52-55` [high] **linked x2** — exclude goalkeepers from the analysis sample
- `59-62` [high] **linked x2** — require at least 3 games in a dyad to keep it in the sample
- `74-76` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `77-81` [high] **linked x5** — dichotomize the continuous skin-tone score into dark vs light at a 0.25 cutoff
- `82-97` [high] **SILENT** — collapse the many specific playing positions into three broad categories
- `102-104` [high] **linked x1** — drop observations lacking a position category or referee bias measures
- `105-108` [high] **linked x2** — fill missing height and weight with the sample median rather than dropping those rows
- `136-138` [medium] **SILENT** — compute the crude (unadjusted) red-card rate difference between dark- and light-skin groups
- `152-158` [high] **linked x14** — choose the covariate adjustment set and fit a logistic regression of the red-card outcome on skin tone
- `170-177` [medium] **linked x4** — exponentiate the log-odds coefficient into an odds ratio with CI as the reported effect scale
- `194-206` [high] **linked x9** — use marginal standardization (predict under darkSkin set to 1 and 0 for everyone, average the difference) to define the primary risk-difference estimand
- `217-252` [high] **linked x4** — quantify uncertainty in the risk difference via a parametric bootstrap over the model's coefficient covariance, then derive a CI and p-value by percentile and z-statistic methods
- `268, 270-281` [high] **linked x2** — test a more extreme skin-tone contrast (>=0.375 vs <0.125), dropping the middle band, as a robustness check on the exposure threshold
- `286, 288-308` [high] **linked x2** — rebuild the sample including goalkeepers as their own position category to test sensitivity to the goalkeeper exclusion
- `314, 316-336` [high] **linked x2** — rebuild the sample with a lower minimum-games cutoff (>=2 instead of >=3) to test sensitivity to that threshold
- `341, 343-354` [high] **linked x2** — refit the model using continuous skinTone instead of the dichotomized darkSkin variable, scaling the reported effect per 0.25 units
- `378-387` [high] **linked x5** — assert a fixed interpretive conclusion ('SUPPORTED', 'statistically significant and robust') describing the finding rather than deriving that language conditionally from the estimated effect and its significance
