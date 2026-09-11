# team-13  (human)

- code: 153 lines, 48% exon (73 lines in 20 decisions)
- intron: print 37, comment 22, other 9, plot 6, glue 4, import 2
- prose: 194 lines, 55 claims (35 action, 20 result)
- links: 25 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 12
- C_only_silent_decision: 8
- R_only_unbacked_action_claim: 17
- R_only_consistent_negative: 3
- result_claims_deferred: 20

## Silent decisions — executed, never disclosed

- **10-11** [high] pull in the raw CrowdStorming CSV as the entire analysis dataset
- **65, 67-70** [high] replace model-based standard errors with heteroskedasticity-robust (sandwich) errors and rebuild the coefficient/CI table from them
- **85-87** [high] summarize each country's implicit/explicit bias measures by averaging across referees within that country
- **88-90** [medium] join the country-level red-card counts with the country-level bias measures into one analysis table, relabeling the merged count columns
- **105-107, 108-109** [high] inspect the extreme-rate countries and drop referee country 133 as an outlier from the country-level analysis
- **112, 115-117** [high] treat non-finite (NaN/Inf) ratio values, produced by zero-rate denominators, as missing rather than as real values
- **130-133** [high] recompute this model's standard errors with a sandwich/robust estimator and rebuild the estimate table
- **139-142** [high] apply the same sandwich/robust standard-error correction to the explicit-bias poisson model's estimates

## Misaligned — code and prose disagree

- code: regress the dark/light red-card ratio on country implicit-bias score, weighting observations by the inverse of that same score
  - prose: abandoned the relative-risk ratio approach because many probabilities were zero, leaving too few data points, and instead decided to model red card counts as a Poisson distribution as in Hypothesis 1
  - why: claim says the relative-risk ratio approach was abandoned, but code still regresses ratio.p.darktolight on implicit bias (decision 40)
- code: regress the same ratio on country explicit-bias score instead, weighting by the inverse of its standard error
  - prose: abandoned the relative-risk ratio approach because many probabilities were zero, leaving too few data points, and instead decided to model red card counts as a Poisson distribution as in Hypothesis 1
  - why: claim says the relative-risk ratio approach was abandoned, but code still regresses ratio.p.darktolight on explicit bias (decision 42)

## All decisions

- `10-11` [high] **SILENT** — pull in the raw CrowdStorming CSV as the entire analysis dataset
- `25-26` [high] **linked x2** — quantify agreement between the two continuous rater scores with Cronbach's alpha
- `27-31` [high] **linked x1** — cut each rater's continuous score into light/dark categories at the midpoint value of 3, dropping the exact-3 cases as missing, then check the two raters' categorical agreement with kappa
- `32-34` [high] **linked x1** — collapse the two raters' scores into one continuous skin-tone rating by averaging
- `41-43, 45-46` [high] **linked x2** — split the averaged skin-tone score into a binary light/dark grouping variable at 3, excluding the neutral midpoint, for use as the main predictor
- `54-61` [high] **linked x6** — model red cards as poisson counts predicted by skin color and position, using log(games) as an exposure offset, on the reasoning that red cards are rare events roughly consistent with mean≈variance and that exposure/position need to be accounted for
- `65, 67-70` [high] **SILENT** — replace model-based standard errors with heteroskedasticity-robust (sandwich) errors and rebuild the coefficient/CI table from them
- `78-82` [high] **linked x1** — collapse player-level rows up to one row per referee country by summing games and red cards separately within each skin-color group, then reshape those sums to wide form
- `85-87` [high] **SILENT** — summarize each country's implicit/explicit bias measures by averaging across referees within that country
- `88-90` [medium] **SILENT** — join the country-level red-card counts with the country-level bias measures into one analysis table, relabeling the merged count columns
- `91-96` [medium] **linked x1** — define per-country dark-skin and light-skin red-card rate variables directly from the summed counts (and surface the corresponding games totals) as the basis for a relative rate
- `97-100` [high] **linked x1** — form a relative-risk-style ratio of dark-skin to light-skin rates, flagging that zero light-skin rates will produce divide-by-zero cases
- `105-107, 108-109` [high] **SILENT** — inspect the extreme-rate countries and drop referee country 133 as an outlier from the country-level analysis
- `112, 115-117` [high] **SILENT** — treat non-finite (NaN/Inf) ratio values, produced by zero-rate denominators, as missing rather than as real values
- `118` [high] **linked x1** — regress the dark/light red-card ratio on country implicit-bias score, weighting observations by the inverse of that same score
- `122` [high] **linked x1** — regress the same ratio on country explicit-bias score instead, weighting by the inverse of its standard error
- `127-128` [high] **linked x4** — switch to a poisson model of dark-skin red-card counts predicted by country implicit bias and the light-skin rate, offset by dark-skin games played
- `130-133` [high] **SILENT** — recompute this model's standard errors with a sandwich/robust estimator and rebuild the estimate table
- `137` [high] **linked x4** — fit the parallel poisson model using explicit bias in place of implicit bias, again offset by dark-skin games played
- `139-142` [high] **SILENT** — apply the same sandwich/robust standard-error correction to the explicit-bias poisson model's estimates
