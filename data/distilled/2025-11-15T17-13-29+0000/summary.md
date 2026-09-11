# 2025-11-15T17-13-29+0000  (ai)

- code: 417 lines, 36% exon (149 lines in 19 decisions)
- intron: print 105, comment 90, plot 50, glue 11, import 9, other 3
- prose: 257 lines, 64 claims (25 action, 39 result)
- links: 37 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 5
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 5
- result_claims_deferred: 39

## Silent decisions — executed, never disclosed

- **31** [high] load the raw soccer referee dataset from a fixed CSV path with no filtering at read time
- **53** [high] binarize skin category into a dark-skin indicator used as the exposure
- **56-71** [high] collapse free-text position strings into a small set of position buckets via keyword matching, with an Unknown catch-all
- **85-89** [high] choose the fixed set of variables (outcome, exposure, covariates, IDs) that will be carried into modeling
- **401-402** [medium] drop skin-tone values supported by fewer than 100 dyads before plotting the rate-by-skin-tone curve

## All decisions

- `31` [high] **SILENT** — load the raw soccer referee dataset from a fixed CSV path with no filtering at read time
- `36` [high] **linked x1** — average the two independent raters' scores into one continuous skin-tone score
- `45-47, 393-394, 405-407` [high] **linked x2** — split continuous skin tone into Light/Dark categories using 0.25/0.75 cutoffs, discarding the middle band; same cutoffs later drawn as reference lines/shaded regions in the plots
- `50` [high] **linked x1** — binarize the outcome as whether any red card occurred in the dyad
- `53` [high] **SILENT** — binarize skin category into a dark-skin indicator used as the exposure
- `56-71` [high] **SILENT** — collapse free-text position strings into a small set of position buckets via keyword matching, with an Unknown catch-all
- `82` [high] **linked x1** — restrict the working dataset to dyads that received a definite (non-medium) skin category
- `85-89` [high] **SILENT** — choose the fixed set of variables (outcome, exposure, covariates, IDs) that will be carried into modeling
- `92` [high] **linked x1** — apply complete-case analysis, dropping any dyad with a missing covariate
- `111-113` [medium] **linked x1** — contrast raw red-card rates between light- and dark-skin groups as an unadjusted descriptive estimate
- `138-141, 360-361` [high] **linked x6** — specify the primary model's functional form, covariate set, and reference levels for position/league; later reused to generate adjusted predicted rates for the figure
- `145-148` [high] **linked x5** — fit the logistic model with player-clustered robust standard errors using a specific optimizer/iteration cap
- `164-166` [high] **linked x4** — exponentiate the exposure coefficient (and its CI) to report an adjusted odds ratio as a secondary estimand
- `179-230, 233, 235-238` [high] **linked x5** — define and apply an average-marginal-effect delta-method routine to obtain the primary risk-difference estimate and its SE/CI/p-value, then rescale to percentage points
- `249-250` [medium] **linked x2** — re-express the risk difference as a percentage increase relative to the light-skin baseline rate
- `264-267, 269-273, 275-276` [high] **linked x1** — refit the model dropping the referee-bias covariates as a sensitivity check on confounder set
- `282-285, 287-290, 292-296, 298-299` [high] **linked x4** — rebuild the analysis sample and refit using continuous skinTone in place of the dichotomized category, as a dose-response check
- `316, 322, 332-340` [high] **linked x3** — classify the hypothesis as supported / marginally supported / not supported using chosen p-value (0.05, 0.10) and CI-margin (-0.05) cutoffs
- `401-402` [medium] **SILENT** — drop skin-tone values supported by fewer than 100 dyads before plotting the rate-by-skin-tone curve
