# 2025-11-29T05-43-38+0000  (ai)

- code: 420 lines, 39% exon (164 lines in 19 decisions)
- intron: print 138, comment 56, plot 47, import 7, config 6, glue 2
- prose: 310 lines, 87 claims (49 action, 38 result)
- links: 47 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 16
- R_only_consistent_negative: 6
- result_claims_deferred: 38

## Silent decisions — executed, never disclosed

- **78-87** [high] derive player age from birthdate using a fixed reference year (2013), mapping parse failures to missing
- **324-329** [low] compute unadjusted red-card rate and standard error by skin-tone group and display error bars using a 1.96 (normal-approximation) multiplier

## Misaligned — code and prose disagree

- code: hand-enter comparison odds ratios from other (unadjusted, +games, +position) specifications as literal values for the forest plot rather than recomputing them here
  - prose: no manual calculations or selective reporting were used; all results are generated directly from the code
  - why: code hand-enters literal odds-ratio values into models_plot for the forest plot rather than computing them, contradicting the claim that no manual calculations were used

## All decisions

- `38-39` [high] **linked x1** — load the raw player-referee dyad dataset from a fixed CSV path as the entire analytic input
- `45-46` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `59-75` [high] **linked x4** — collapse dyad-level rows to one row per player, keeping the first value for static attributes and summing counts across a player's referees
- `78-87` [high] **SILENT** — derive player age from birthdate using a fixed reference year (2013), mapping parse failures to missing
- `88-105` [high] **linked x1** — bucket free-text position strings into four coarse categories via keyword matching, defaulting unmatched values to Other
- `106-108` [high] **linked x2** — define the binary outcome as whether a player ever received any red card, discarding the count
- `119-124` [high] **linked x3** — dichotomize the continuous skin-tone score into dark vs. light using a 0.75 cutoff
- `140-145` [high] **linked x4** — restrict the working sample to players with non-missing skin tone and non-missing position category
- `148-153` [high] **linked x3** — build model covariates: log1p-transform games played, z-standardize age and height, imputing missing standardized height to 0
- `165-168` [high] **linked x3** — specify the primary model as logistic regression of any-red-card on skin-tone dark, adjusting for log games, position, and league
- `171-178` [medium] **linked x5** — summarize the skinDark effect as an exponentiated odds ratio with a Wald confidence interval and a normal-approximation two-sided p-value
- `194-235, 237-239, 299-300` [high] **linked x8** — estimate the adjusted risk difference via g-computation (predicting outcomes under both counterfactual skin-tone values) with a percentile bootstrap confidence interval, using this same procedure for both the full sample and the defender/midfielder subgroup
- `259-264` [high] **linked x1** — restrict to players where the two raters agree within 0.25 points and refit the primary model on this subsample
- `271-273` [high] **linked x3** — refit the primary model using heteroskedasticity-robust (HC3) standard errors instead of model-based ones
- `279-285` [high] **linked x1** — swap the outcome model to a Poisson rate model of red cards with a log-games offset, instead of the binary logistic outcome
- `291-294` [high] **linked x2** — restrict the sample to Defenders and Midfielders only and refit the primary model on this subgroup
- `324-329` [low] **SILENT** — compute unadjusted red-card rate and standard error by skin-tone group and display error bars using a 1.96 (normal-approximation) multiplier
- `341-348` [low] **linked x1** — hand-enter comparison odds ratios from other (unadjusted, +games, +position) specifications as literal values for the forest plot rather than recomputing them here
- `412` [low] **linked x3** — additionally report the relative (percentage) increase in predicted risk between dark- and light-skinned players, beyond the absolute difference
