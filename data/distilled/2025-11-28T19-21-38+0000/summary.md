# 2025-11-28T19-21-38+0000  (ai)

- code: 364 lines, 37% exon (133 lines in 17 decisions)
- intron: print 172, comment 48, import 6, config 5
- prose: 328 lines, 141 claims (75 action, 66 result)
- links: 63 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 23
- R_only_consistent_negative: 19
- result_claims_deferred: 66

## Silent decisions — executed, never disclosed

- **266-269** [medium] pick specific skin-tone reference values (0.75 vs 0.125) to translate the continuous slope into an implied rate ratio

## All decisions

- `32-33` [high] **linked x1** — choose the raw CSV file as the full data source and scope of the analysis
- `38-40` [high] **linked x4** — drop dyads that are missing either rater's skin-tone score
- `44-45` [high] **linked x1** — drop dyads with zero recorded games as an integrity check
- `56-57` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `64-65` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `72-78, 88-90` [high] **linked x16** — bin continuous skin tone into Light/Medium/Dark via fixed cutoffs (0.125, 0.5), then restrict the comparison sample to Light vs Dark only and code it as a binary darkSkin indicator
- `97-112` [high] **linked x2** — collapse detailed player positions into four coarse role categories, defaulting unmapped values to Unknown
- `132-134, 139-144` [high] **linked x8** — specify the primary model as a Poisson GLM of red cards on darkSkin adjusting for position and league, with a log(games) exposure offset
- `160-184` [high] **linked x9** — derive an average marginal risk-difference estimand: predict counterfactual red-card rates at darkSkin=0/1, convert Poisson rates to per-dyad probabilities of at least one card via 1-exp(-rate*games), and average the difference across dyads
- `185-192` [medium] **linked x4** — approximate the risk difference's SE via the delta method scaled from the model coefficient's SE, then build a 95% CI using a normal-approximation multiplier of 1.96
- `193-196` [high] **linked x3** — report both the model's two-sided p-value and a one-sided p-value obtained by halving it
- `218-219` [high] **linked x4** — express the darkSkin coefficient and its interval as an exponentiated rate ratio
- `238, 241-249` [high] **linked x2** — refit the red-card model on the same sample without covariates to test sensitivity to adjustment, and re-derive its rate ratio and CI
- `252-253, 256-263` [high] **linked x3** — refit on the full unrestricted sample using continuous skinTone as a linear predictor instead of the binary light/dark contrast
- `266-269` [medium] **SILENT** — pick specific skin-tone reference values (0.75 vs 0.125) to translate the continuous slope into an implied rate ratio
- `271-272, 275-287` [high] **linked x1** — redefine the dark/light contrast with an alternative cutoff (>=0.375 vs <=0.125), excluding the middle band, and refit the adjusted model plus rate ratio on that alternative sample
- `350-358` [high] **linked x2** — declare the hypothesis supported only when the two-sided p-value is below 0.05 and the estimated effect is in the positive (dark > light) direction
