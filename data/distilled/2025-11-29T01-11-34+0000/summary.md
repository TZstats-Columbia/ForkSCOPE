# 2025-11-29T01-11-34+0000  (ai)

- code: 301 lines, 43% exon (129 lines in 22 decisions)
- intron: print 100, comment 59, import 8, config 5
- prose: 283 lines, 122 claims (82 action, 40 result)
- links: 83 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 21
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 17
- R_only_consistent_negative: 11
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **88-92** [high] compute the unadjusted red-card rate difference between dark and light groups

## All decisions

- `30-31` [high] **linked x3** — load the raw player-referee dyad dataset from a fixed CSV path
- `37-38` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `39-42` [medium] **linked x1** — restrict to dyads with both ratings present and correlate them to check inter-rater agreement
- `44-46` [high] **linked x1** — collapse red-card count into a binary any-red-card outcome
- `47-49` [high] **linked x4** — exclude dyads that lack a skin-tone rating from the analysis sample
- `53-56` [high] **linked x1** — recode missing player position as its own 'Unknown' category instead of dropping
- `57-60` [high] **linked x2** — fill missing height and weight with the sample median
- `61-65` [high] **linked x1** — derive player age relative to a fixed mid-season reference date
- `66-68` [medium] **linked x1** — derive a yellow-cards-per-game rate variable
- `78-81` [high] **linked x7** — dichotomize skin tone into a 'dark' indicator using a 0.75 cutoff on the 0-1 scale
- `88-92` [high] **SILENT** — compute the unadjusted red-card rate difference between dark and light groups
- `103-105` [high] **linked x15** — choose the covariate adjustment set for the primary model
- `106-108` [high] **linked x7** — fit the primary exposure-outcome association as a Poisson GLM with HC0 robust standard errors
- `122-136` [high] **linked x7** — estimate the adjusted risk difference and risk ratio via marginal standardization over all-dark vs all-light counterfactual predictions
- `150-157, 160-185` [high] **linked x3** — bootstrap the standardized risk difference/ratio with 1000 nonparametric resamples, refitting the Poisson model on each resample and silently skipping fits that fail to converge
- `186-198` [high] **linked x6** — form 95% CIs from bootstrap percentiles and define a two-sided bootstrap p-value from the share of resamples crossing zero
- `216-226` [high] **linked x6** — fit a logistic regression on the same covariate set for a secondary adjusted odds ratio, using a Wald normal-approximation CI
- `242-243` [high] **linked x3** — refit the logistic model with standard errors clustered by referee
- `248-249` [high] **linked x5** — refit the model using continuous skin tone in place of the binary dark indicator
- `254-256` [high] **linked x3** — restrict to only the most extreme skin-tone ratings (0.0 vs 1.0) and refit
- `261-262` [high] **linked x3** — restrict the sample to dyads with at least 2 games and refit
- `293, 297` [high] **linked x3** — declare the hypothesis supported or not based on whether the bootstrap CI for the adjusted risk difference excludes zero
