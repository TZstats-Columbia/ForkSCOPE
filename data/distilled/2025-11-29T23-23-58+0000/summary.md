# 2025-11-29T23-23-58+0000  (ai)

- code: 391 lines, 42% exon (165 lines in 19 decisions)
- intron: print 166, comment 48, import 7, config 5
- prose: 282 lines, 114 claims (60 action, 54 result)
- links: 81 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 6
- result_claims_deferred: 54

## Silent decisions — executed, never disclosed

- **36-37** [high] pick the raw input file and scope of dyads to load
- **69-86** [high] collapse detailed field positions into four coarse position groups, bucketing unmapped values as Unknown
- **178** [medium] convert the two-sided p-value into a one-sided p-value by halving it, assuming a directional hypothesis RD>0

## All decisions

- `36-37` [high] **SILENT** — pick the raw input file and scope of dyads to load
- `42-44` [high] **linked x2** — collapse the two independent raters into a single skin-tone score by averaging
- `45-47` [high] **linked x1** — collapse red-card count into a binary any-red-card outcome
- `48-53` [high] **linked x1** — drop dyads lacking a skin-tone rating (no player photo) and tally how many were dropped
- `69-86` [high] **SILENT** — collapse detailed field positions into four coarse position groups, bucketing unmapped values as Unknown
- `90-97` [high] **linked x6** — define the primary dark/light exposure contrast by cutting skin tone at the top quartile vs bottom ~10%, leaving the middle range unclassified
- `103-106` [medium] **linked x4** — restrict to dyads with complete exposure and categorical covariate data
- `107-114` [medium] **linked x1** — z-score yellow cards and height for numerical stability in the model
- `115-117` [medium] **linked x3** — drop remaining rows missing the standardized covariates
- `125-127` [medium] **linked x2** — compute the unadjusted red-card rate for each exposure group as a descriptive baseline
- `150` [high] **linked x8** — choose the covariate/adjustment set for the primary model
- `157-171` [high] **linked x25** — fit a binomial GLM with identity link (risk-difference scale) weighted by games played, using HC1 robust SEs, and pull out the dark_primary coefficient/SE/CI/z/p
- `178` [medium] **SILENT** — convert the two-sided p-value into a one-sided p-value by halving it, assuming a directional hypothesis RD>0
- `194-205` [high] **linked x4** — refit the same specification with a logit link to report the effect as an odds ratio and pull out its coefficient/CI/p
- `225, 230-240` [high] **linked x6** — re-estimate the primary model with standard errors clustered by player instead of HC1, to test robustness to within-player correlation
- `248, 252-272` [high] **linked x2** — rebuild the analysis sample keeping the full continuous skin-tone range (no dark/light dichotomization) and refit the risk-difference model on it
- `278, 282-290` [high] **linked x3** — refit the primary model dropping the games frequency weights, to test robustness to the weighting choice
- `296, 299-329` [high] **linked x8** — sweep three alternative dark/light skin-tone cutoffs and refit the model at each to test robustness of the primary threshold choice
- `368, 370` [low] **linked x5** — declare the hypothesis outcome as SUPPORTED based on the estimated effects
