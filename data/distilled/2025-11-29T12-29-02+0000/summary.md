# 2025-11-29T12-29-02+0000  (ai)

- code: 457 lines, 21% exon (96 lines in 16 decisions)
- intron: print 174, comment 91, glue 83, import 9, config 4
- prose: 216 lines, 67 claims (37 action, 30 result)
- links: 51 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 5
- result_claims_deferred: 30

## Silent decisions — executed, never disclosed

- **112** [high] derive a binary dark-skin exposure flag from the categorical skin-tone label

## All decisions

- `43` [high] **linked x1** — load the raw soccer player-referee dyad dataset from CSV as the full analysis universe
- `65` [high] **linked x1** — average the two independent raters' skin-tone scores into a single continuous skinTone measure
- `82-85` [high] **linked x1** — bucket continuous skin tone into light/medium/dark categories using 0.125 and 0.625 cutoffs
- `94, 113` [high] **linked x1** — collapse red card count into a binary any-red-card outcome
- `111` [high] **linked x5** — restrict the analysis sample to only light and dark skin-tone dyads, dropping medium and missing
- `112` [high] **SILENT** — derive a binary dark-skin exposure flag from the categorical skin-tone label
- `143-160, 162` [high] **linked x2** — map free-text player position strings into five coarse buckets (Goalkeeper/Defender/Midfielder/Forward/Other/Missing)
- `176-177` [medium] **linked x1** — one-hot encode position into dummy covariates with Defender chosen as the omitted reference level
- `206-207, 209` [high] **linked x10** — specify and fit the primary logistic GLM of any-red-card on dark_skin adjusting for games and position dummies
- `218-221` [low] **linked x2** — compute a two-sided Wald z-test p-value for the primary exposure coefficient
- `242, 246-247, 250-251, 254-257, 260, 264-266, 269-271, 274-275` [high] **linked x7** — compute the adjusted risk difference via counterfactual marginal standardization (g-computation) with a delta-method standard error and CI
- `297-299` [high] **linked x3** — exponentiate the logit coefficient into an odds ratio with a Wald CI as the secondary estimand
- `321-324, 326-330, 332-335` [high] **linked x5** — re-derive skin categories at an alternative 0.25/0.5 threshold, rebuild the sample, and refit the primary model as a sensitivity check
- `344-347, 349-351, 353-355` [high] **linked x4** — refit using continuous skin tone (dropping only missing values, no categorization) as a linear predictor
- `364-368` [high] **linked x4** — restrict the sample to dyads with at least 3 games and refit the primary model
- `376-377, 379-382, 384-386` [high] **linked x4** — add league-country fixed effects as an additional covariate set on top of the primary model
