# 2025-11-21T03-02-44+0000  (ai)

- code: 209 lines, 50% exon (104 lines in 19 decisions)
- intron: print 87, comment 9, import 8, config 1
- prose: 166 lines, 72 claims (34 action, 38 result)
- links: 52 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 5
- result_claims_deferred: 38

## Silent decisions — executed, never disclosed

- **93-100** [low] assemble the model design matrix with an intercept term and cast dummy columns to numeric, and fix the outcome vector

## All decisions

- `22-24` [high] **linked x1** — pick which raw file and rows constitute the working dataset
- `26-28` [high] **linked x2** — drop dyads lacking both skin-tone rater scores from the working set
- `30-32` [high] **linked x1** — combine the two raters' scores into a single continuous skin-tone measure by averaging
- `33-34, 36` [medium] **linked x1** — assess how much the two raters agree using a Pearson correlation as a data-quality check
- `38-41` [high] **linked x4** — collapse the continuous skin-tone average into a dark/light binary using a 0.5 midpoint split
- `42-44` [high] **linked x2** — define the outcome as having received one or more red cards, collapsing counts to a binary
- `45-49` [high] **linked x1** — derive player age by anchoring birthdate to a chosen mid-season reference date
- `50-58` [high] **linked x4** — restrict the analysis population to complete cases across height, weight, age, position, and league country
- `74-75` [medium] **linked x1** — compute the crude (unadjusted) red-card rate separately for each skin-tone group as a comparator to the adjusted estimate
- `85-88` [high] **linked x2** — one-hot encode position and league country as dummy variables, dropping the reference category
- `89-91` [high] **linked x4** — select which variables enter the regression as adjustment covariates alongside skin tone
- `92` [medium] **linked x2** — log-transform games played to include as an exposure/playing-time adjustment
- `93-100` [low] **SILENT** — assemble the model design matrix with an intercept term and cast dummy columns to numeric, and fix the outcome vector
- `111-114` [high] **linked x5** — fit a logistic regression of red card on skin tone and covariates, with standard errors clustered by player
- `119-131` [high] **linked x6** — estimate the adjusted risk difference by setting skin tone to dark/light for everyone, predicting, and averaging predictions (marginal standardization / g-computation)
- `137-158` [high] **linked x1** — derive the standard error of the risk difference via the delta method using a numerically estimated gradient of the g-computation function
- `159-164` [high] **linked x3** — build a 95% confidence interval and two-sided p-value for the risk difference using a normal approximation with a 1.96 multiplier
- `175-177` [high] **linked x4** — report the skin-tone effect as an adjusted odds ratio by exponentiating the model coefficient and its confidence interval
- `200-204` [low] **linked x8** — characterize the overall finding as inconclusive/hypothesis-not-supported based on the p-values relative to an implied 0.05 threshold
