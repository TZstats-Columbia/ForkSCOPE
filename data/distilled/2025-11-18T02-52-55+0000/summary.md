# 2025-11-18T02-52-55+0000  (ai)

- code: 309 lines, 41% exon (127 lines in 16 decisions)
- intron: print 85, comment 43, plot 43, import 7, config 3, glue 1
- prose: 369 lines, 133 claims (57 action, 76 result)
- links: 46 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 18
- R_only_consistent_negative: 12
- result_claims_deferred: 76

## All decisions

- `29-31` [high] **linked x2** — read the soccer dyad dataset from a fixed local CSV path, fixing the data source and full sample scope
- `33-35` [high] **linked x1** — drop dyads where either rater's skin-tone score is missing before any further processing
- `37-39` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skin_tone measure per dyad
- `40-42` [high] **linked x2** — collapse the red-card count into a binary indicator for whether the player ever received a red card
- `43-52` [high] **linked x3** — split skin_tone into light (<=0.25) and dark (>=0.5) groups with fixed cutoffs and discard the ambiguous middle range entirely
- `54-58` [high] **linked x2** — further restrict the sample to dyads with non-missing height, weight, and position
- `60-64` [high] **linked x2** — z-score height and weight and log-transform games played for use as model covariates
- `82-85, 275-276` [medium] **linked x1** — tabulate the raw, unadjusted red-card rate separately for the light and dark skin-tone groups
- `95-97` [high] **linked x6** — choose the regression formula/adjustment set: skin tone plus games played, position, league country, height, and weight
- `98-104` [high] **linked x8** — fit that formula as a logistic regression with standard errors clustered by player instead of treating dyads as independent
- `118-134` [high] **linked x3** — estimate the adjusted risk difference by g-computation: predict every player's red-card probability under all-dark and all-light counterfactuals and difference the averages
- `147-148, 150-179` [high] **linked x2** — quantify uncertainty in the risk difference via a parametric bootstrap: draw 2000 coefficient vectors from the model's asymptotic multivariate normal and recompute the counterfactual risk difference for each draw
- `180-184` [high] **linked x3** — build the 95% confidence interval for the risk difference from the 2.5th/97.5th percentiles of the bootstrap draws
- `185-188` [high] **linked x1** — derive a two-sided p-value for the risk difference by treating point-estimate over bootstrap-SE as a standard normal z-statistic
- `203-207` [high] **linked x5** — report a secondary adjusted odds ratio for dark vs light skin using the model's own Wald-based confidence interval and p-value rather than the bootstrap approach used for the risk difference
- `234-249` [high] **linked x4** — declare the hypothesis unsupported against a 0.05 significance threshold, narrating the result with specific numeric values written directly into the text rather than pulled from the computed variables
