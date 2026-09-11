# 2025-11-19T11-29-03+0000  (ai)

- code: 218 lines, 52% exon (113 lines in 17 decisions)
- intron: print 63, comment 31, import 9, config 2
- prose: 281 lines, 100 claims (43 action, 57 result)
- links: 58 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 8
- result_claims_deferred: 57

## Silent decisions — executed, never disclosed

- **43-49** [medium] pick which columns carry into the modeling dataset (outcome, exposure, covariates, cluster id)
- **149-153** [high] redefine exposure using extreme skin-tone cutoffs (>=0.75 vs <=0.25) and exclude the ambiguous middle group
- **154-162** [high] refit the adjusted logistic model on the extreme-only subsample using the extreme exposure coding

## All decisions

- `23-24` [high] **linked x1** — choose the raw input file and load the full soccer dataset as the analysis starting point
- `27-29` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `30-32` [high] **linked x3** — split the continuous skin-tone score into a binary dark/light exposure at the 0.5 midpoint
- `33-35` [high] **linked x2** — collapse the red-card count into a binary any-red-card outcome
- `36-38` [high] **linked x2** — recode missing position values as an explicit 'Unknown' category instead of dropping them
- `43-49` [medium] **SILENT** — pick which columns carry into the modeling dataset (outcome, exposure, covariates, cluster id)
- `50-52` [high] **linked x4** — restrict to complete cases by dropping rows missing skin tone, height, or weight
- `72-76` [medium] **linked x3** — compute the crude (unadjusted) red-card rate difference between dark- and light-skinned groups
- `90-100` [high] **linked x11** — fit a covariate-adjusted logistic regression of any red card on the binary dark-skin exposure with referee-clustered standard errors
- `101-105` [high] **linked x10** — extract the average marginal effect of dark skin as the primary risk-difference estimate
- `113-117` [high] **linked x5** — convert the model's dark-skin coefficient to an odds ratio as a secondary effect measure
- `131-140` [high] **linked x2** — refit the adjusted logistic model using continuous skin tone instead of the binary exposure, as a sensitivity check
- `141-143` [medium] **linked x6** — extract the average marginal effect of continuous skin tone from the sensitivity model
- `149-153` [high] **SILENT** — redefine exposure using extreme skin-tone cutoffs (>=0.75 vs <=0.25) and exclude the ambiguous middle group
- `154-162` [high] **SILENT** — refit the adjusted logistic model on the extreme-only subsample using the extreme exposure coding
- `163-165` [medium] **linked x5** — extract the average marginal effect of the extreme dark-skin exposure from the sensitivity model
- `180-212` [low] **linked x2** — assemble a side-by-side comparison table of effect estimates, CIs, and p-values across the primary and sensitivity specifications
