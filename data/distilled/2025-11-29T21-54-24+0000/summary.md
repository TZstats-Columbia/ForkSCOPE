# 2025-11-29T21-54-24+0000  (ai)

- code: 291 lines, 52% exon (151 lines in 16 decisions)
- intron: print 88, comment 43, config 5, import 4
- prose: 223 lines, 91 claims (51 action, 40 result)
- links: 60 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 8
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **94-97** [medium] compute the unadjusted (crude) risk difference between skin-tone groups as a baseline contrast

## All decisions

- `23-24` [high] **linked x1** — load the raw player-referee dyad dataset from a specific CSV as the analysis input
- `29-32` [high] **linked x1** — average the two raters' skin-tone codings into a single continuous exposure score
- `33-35` [high] **linked x2** — collapse red-card counts into a binary any-red-card outcome for the dyad
- `36-40` [high] **linked x4** — dichotomize the continuous skin-tone score into dark vs light using a 0.25 cutoff
- `41-44` [high] **linked x1** — compute each player's age at a fixed season-start reference date from birthday
- `45-58` [high] **linked x2** — collapse detailed playing positions into four broader position categories for adjustment
- `69-73` [high] **linked x6** — drop dyads missing skin tone or anthropometric covariates to define the analysis sample
- `88-93` [medium] **linked x2** — tabulate the crude red-card rate separately for the light- and dark-skin groups
- `94-97` [medium] **SILENT** — compute the unadjusted (crude) risk difference between skin-tone groups as a baseline contrast
- `107-115` [high] **linked x11** — specify and fit the primary logistic regression adjustment set (dark_skin adjusted for games and position, deliberately excluding other covariates)
- `122-139` [high] **linked x7** — use marginal standardization (G-computation counterfactual predictions) to convert the logistic model's coefficient into an absolute risk difference
- `140-154` [high] **linked x10** — approximate the standard error, confidence interval, and p-value of the standardized risk difference via a delta-method formula rather than resampling/bootstrapping
- `170-171` [medium] **linked x4** — exponentiate the primary model's coefficient and CI to report an adjusted odds ratio as a secondary estimand
- `187-204` [high] **linked x2** — refit with a minimal covariate set (drop position, keep only games) as a sensitivity check on the adjustment set, re-deriving the standardized risk difference and odds ratio
- `209-227` [high] **linked x3** — refit adding league country as an extra adjustment covariate to test sensitivity to the confounder set, re-deriving the standardized risk difference and odds ratio
- `232-254` [high] **linked x4** — restrict to extreme skin-tone scores and widen the exposure contrast to ≤0.25 vs ≥0.75, excluding the middle group, then re-derive the risk difference and odds ratio
