# 2025-11-15T15-03-11+0000  (ai)

- code: 396 lines, 26% exon (104 lines in 18 decisions)
- intron: print 111, plot 83, comment 79, import 10, config 5, glue 4
- prose: 235 lines, 108 claims (39 action, 69 result)
- links: 62 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 4
- result_claims_deferred: 69

## Silent decisions — executed, never disclosed

- **94-97** [medium] choose which columns enter the modeling dataset, fixing the covariate set available to later models
- **331-339** [medium] choose which covariates to check for balance across skin-tone groups and normalize their means relative to the light-skin group

## All decisions

- `37` [medium] **linked x1** — load the raw soccer dataset from a fixed CSV path as the analysis input
- `41` [high] **linked x1** — average the two raters' ratings into a single continuous skin tone score
- `48-50, 53` [high] **linked x3** — cut the continuous skin tone score into Light/Dark categories at fixed thresholds and collapse to a binary exposure, dropping the medium band
- `56` [high] **linked x1** — define the outcome as whether any red card occurred in the dyad, collapsing counts to a binary
- `59` [high] **linked x3** — restrict the analysis sample to rows with a defined Light/Dark group, dropping medium-skin-tone dyads entirely
- `68-83` [high] **linked x1** — collapse granular player positions into a small set of position categories (Forward/Midfielder/Defender/Goalkeeper/Missing/Other) for use as a covariate
- `94-97` [medium] **SILENT** — choose which columns enter the modeling dataset, fixing the covariate set available to later models
- `100` [high] **linked x3** — handle missing data by complete-case deletion rather than imputation
- `107-109` [high] **linked x3** — one-hot encode categorical covariates with the first level dropped as reference
- `132` [medium] **linked x3** — compute an unadjusted (crude) risk difference between groups as a baseline comparison
- `144-147` [high] **linked x5** — specify the adjustment set of covariates included in the primary regression formula
- `150-154` [high] **linked x5** — fit a logistic regression as the primary model family, using cluster-robust standard errors clustered by player
- `168-178` [high] **linked x9** — choose the average marginal effect (risk-difference scale) as the primary estimand and rescale it to percentage points
- `196-198` [high] **linked x8** — report a secondary estimand by exponentiating the logistic coefficient into an odds ratio
- `218-234` [medium] **linked x5** — stratify the red-card-rate comparison by league as a sensitivity check, with England treated as the implicit reference category via dummy exclusion
- `238-253` [high] **linked x3** — re-specify the exposure as continuous skin tone instead of the binary group and refit an equivalent logistic model as a dose-response sensitivity analysis
- `331-339` [medium] **SILENT** — choose which covariates to check for balance across skin-tone groups and normalize their means relative to the light-skin group
- `386-391` [high] **linked x8** — apply a 0.05 significance threshold to the primary p-value to declare the hypothesis supported or not, and phrase the non-significant case as inconclusive rather than null evidence
