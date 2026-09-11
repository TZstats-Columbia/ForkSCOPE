# 2025-11-22T12-02-23+0000  (ai)

- code: 288 lines, 36% exon (103 lines in 15 decisions)
- intron: print 133, comment 39, import 9, config 4
- prose: 169 lines, 80 claims (38 action, 42 result)
- links: 44 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 7
- result_claims_deferred: 42

## Silent decisions — executed, never disclosed

- **96-98** [high] recode the three-level skin_group into a binary dark-skin exposure indicator with light skin as reference

## All decisions

- `34-35` [high] **linked x1** — load the fixed soccer referee dataset from a hardcoded CSV path as the entire analysis universe
- `38-39` [high] **linked x2** — average the two independent raters' skin-tone ratings into one continuous score per dyad
- `50-54, 59-61, 267` [high] **linked x5** — classify dyads into Light (<=0.25) / Dark (>=0.75) / Excluded skin-tone groups, drop the excluded middle range to build the analysis sample, and re-derive the same cutoff later to count how many were excluded
- `72-77` [medium] **linked x1** — compute each player's age against a single fixed reference date, parsed from a specific birthday string format
- `78-82, 85-87` [high] **linked x4** — require non-missing values across the chosen set of covariates/fields and drop any dyad failing that complete-case check
- `93-95` [high] **linked x2** — binarize the red-card count into a yes/no 'any red card in the dyad' outcome
- `96-98` [high] **SILENT** — recode the three-level skin_group into a binary dark-skin exposure indicator with light skin as reference
- `110-111, 126` [medium] **linked x3** — compute the crude, unadjusted risk difference between dark- and light-skin groups as a comparison point before adjustment
- `137-138` [high] **linked x9** — choose the covariate adjustment set and functional form for the outcome model
- `139-144` [high] **linked x3** — estimate the model's standard errors with cluster-robust variance clustered on player instead of assuming independent dyads
- `156-173, 195-204` [high] **linked x4** — estimate the adjusted risk difference via marginal standardization/g-computation: score every unit under all-dark and all-light counterfactual exposure and difference the averaged predicted probabilities, both for the point estimate and inside each bootstrap resample
- `179, 181-194, 205-210` [high] **linked x4** — build the bootstrap sampling distribution for the risk difference: resample dyads with replacement 1000 times, refit the model per resample with relaxed convergence settings, silently discard resamples where the fit fails, and take the 2.5/97.5 percentiles as the 95% CI
- `215-216` [medium] **linked x1** — report the Wald p-value for the dark_skin coefficient straight from the primary GLM fit as the significance test
- `227-228` [high] **linked x1** — derive the adjusted odds ratio and its 95% CI by exponentiating the model's coefficient and Wald confidence interval
- `272-273, 276-277, 280-281` [high] **linked x4** — classify the overall finding as supported/not supported/contradictory based on whether the bootstrap CI for the risk difference excludes zero and which direction it points
