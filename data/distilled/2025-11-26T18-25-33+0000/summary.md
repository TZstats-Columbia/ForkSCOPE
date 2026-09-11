# 2025-11-26T18-25-33+0000  (ai)

- code: 297 lines, 32% exon (95 lines in 22 decisions)
- intron: comment 97, print 90, glue 7, import 6, config 2
- prose: 271 lines, 109 claims (50 action, 59 result)
- links: 64 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 22
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 4
- result_claims_deferred: 59

## Misaligned — code and prose disagree

- code: sweep additional binary exposure cutpoints (0.25 and 0.5) and refit the model at each to probe threshold sensitivity
  - prose: thresholds at 0.125, 0.25, 0.375, 0.5, 0.625, and 0.75 were tested for the skin tone cutoff
  - why: claim says thresholds 0.125/0.25/0.375/0.5/0.625/0.75 were tested; code only sweeps binary cutpoints 0.25/0.5/0.75

## All decisions

- `25` [high] **linked x2** — load the entire soccer.csv dyad-level file as the analysis population with no scoping/filter at read time
- `29` [high] **linked x1** — combine the two independent rater scores into a single skin-tone measure by simple averaging
- `32` [high] **linked x2** — drop dyads lacking both skin-tone ratings rather than imputing them
- `36` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome rather than modeling counts
- `43` [high] **linked x3** — log-transform games played to use as the exposure/offset-like control
- `46-47` [high] **linked x2** — z-standardize height and weight before entering them as covariates
- `50-64` [high] **linked x1** — collapse free-text playing position into five coarse groups (Forward/Defender/Midfielder/Goalkeeper/Other/Missing) via keyword matching
- `70-74` [high] **linked x6** — bin the continuous skin-tone average into three ordered categories (Light/Medium/Dark) at 0.25/0.75 cutpoints to serve as the primary exposure
- `81-84` [high] **linked x5** — restrict the analytic sample to dyads with complete data on the chosen covariate set (listwise deletion)
- `101-103` [high] **linked x12** — choose the adjustment set / covariates entered into the primary outcome model
- `106` [high] **linked x1** — pick logistic regression as the model family for the binary red-card outcome
- `107-108` [high] **linked x2** — cluster standard errors by referee rather than assuming independent errors
- `124-126, 129-131, 134` [high] **linked x6** — estimate the risk difference by standardization: set exposure to Light for everyone and predict, then to Dark for everyone and predict, and difference the two average predicted probabilities
- `146-150, 159-160, 162, 165-168, 171-174, 175-178` [high] **linked x1** — build a 500-draw parametric bootstrap by sampling coefficients from the fitted model's asymptotic multivariate-normal distribution and recomputing the standardized risk difference on each draw
- `179-180` [high] **linked x2** — form the 95% CI as the 2.5/97.5 percentiles of the bootstrap risk-difference distribution
- `186` [high] **linked x2** — compute a two-sided bootstrap p-value as twice the smaller proportion of draws on either side of zero
- `196-198` [high] **linked x4** — report an adjusted odds ratio (Dark vs Light) with CI as a secondary effect-size estimand, exponentiating the model coefficient
- `214-218` [high] **linked x1** — re-specify exposure as a single binary cut at 0.75 and refit the same model to check sensitivity to the categorization scheme
- `223-227` [high] **linked x1** — re-specify exposure as a continuous skin-tone score (per 0.1 unit) instead of categorical, and refit
- `231, 233-238` [high] **linked x3** — sweep additional binary exposure cutpoints (0.25 and 0.5) and refit the model at each to probe threshold sensitivity
- `243-246` [high] **linked x3** — restrict to dyads with at least 2 games and refit the primary model to test sensitivity to low-exposure dyads
- `252-255` [high] **linked x2** — drop goalkeepers from the sample and refit the primary model to test sensitivity to position mix
