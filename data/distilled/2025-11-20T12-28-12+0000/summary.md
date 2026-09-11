# 2025-11-20T12-28-12+0000  (ai)

- code: 425 lines, 54% exon (229 lines in 19 decisions)
- intron: print 134, comment 46, import 6, config 5, glue 5
- prose: 219 lines, 86 claims (39 action, 47 result)
- links: 64 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 2
- R_only_consistent_negative: 9
- result_claims_deferred: 47

## Misaligned — code and prose disagree

- code: bootstrap the risk-difference estimate by resampling dyads with replacement and refitting the model 2000 times
  - prose: computed confidence intervals via parametric bootstrap with 2,000 iterations and seed=42
  - why: claim calls it a parametric bootstrap; code resamples dyads with replacement (nonparametric case bootstrap)

## All decisions

- `32-33` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path as the entire analysis universe
- `36-37` [high] **linked x2** — average the two independent raters' scores into a single continuous skin-tone measure
- `39-41` [low] **linked x1** — restrict to dyads with both raters' scores present when reporting the inter-rater correlation diagnostic
- `51-52` [high] **linked x1** — drop dyads with no skin-tone rating at all (no photo available)
- `56-59` [high] **linked x4** — drop dyads with fewer than 3 shared games as unstable rate estimates
- `64` [high] **linked x3** — define the binary outcome as having received any red card at all
- `65, 320` [high] **linked x5** — dichotomize the continuous skin-tone score at 0.25 to define the dark-skin exposure group
- `66, 321` [medium] **linked x2** — add a squared games term to let the games effect be nonlinear in the model
- `68-73, 314-318` [high] **linked x2** — restrict the analytic sample to complete cases on height, weight, and meanIAT
- `105-111` [medium] **linked x6** — compute the raw, unadjusted red-card-rate difference between dark- and light-skin groups
- `121-127` [high] **linked x6** — specify and fit the primary logistic model of any red card on dark_skin adjusted for games, games_sq, height, and weight
- `144-167` [high] **linked x5** — estimate the adjusted risk difference by standardization: predict outcome probability with dark_skin forced to 1 and to 0 for every dyad and average the difference
- `173, 175-217` [high] **linked x1** — bootstrap the risk-difference estimate by resampling dyads with replacement and refitting the model 2000 times
- `218-226` [high] **linked x4** — derive standard error and a percentile 95% CI from the bootstrap draws, and compute a normal-approximation two-sided p-value
- `242-244` [high] **linked x3** — express the exposure effect as an adjusted odds ratio by exponentiating the dark_skin coefficient and its CI bounds
- `261, 267-304` [high] **linked x6** — re-fit the model and re-derive risk difference/OR under alternative dark-skin thresholds (0.25, 0.375, 0.5)
- `306, 312-313, 319, 322-354` [high] **linked x5** — re-fit the model and re-derive risk difference/OR under alternative minimum-games-together thresholds (2, 3, 4, 5)
- `356, 362-384` [high] **linked x3** — compare the adjusted effect from a reduced games-only model against the full covariate-adjusted model
- `415-420` [medium] **linked x3** — interpret the estimate/CI/p-value against a conventional significance cutoff and declare the hypothesis SUPPORTED
