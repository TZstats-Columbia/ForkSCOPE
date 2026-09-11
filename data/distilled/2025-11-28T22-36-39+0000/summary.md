# 2025-11-28T22-36-39+0000  (ai)

- code: 357 lines, 48% exon (173 lines in 19 decisions)
- intron: print 109, comment 62, import 8, config 5
- prose: 250 lines, 85 claims (55 action, 30 result)
- links: 59 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 13
- result_claims_deferred: 30

## Silent decisions — executed, never disclosed

- **275-314** [medium] assemble a comparison table choosing which model estimates (unadjusted, primary Poisson, logistic, and the three sensitivity specs) and which columns (estimate, CI bounds, p-value) to report side by side

## All decisions

- `34` [high] **linked x1** — load the raw player-referee dyad dataset from a fixed CSV path as the analysis's data source
- `38` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `41` [high] **linked x1** — collapse red card count into a binary any-red-card indicator
- `44` [high] **linked x1** — exclude dyads with missing skin tone rating from the working dataset
- `47-50` [high] **linked x5** — binarize the continuous skin-tone score into a dark/light exposure using a 0.25 cutpoint, chosen post hoc via exploratory analysis
- `51-54` [high] **linked x4** — restrict the analytic sample to dyads with complete data on height, weight, position, and both bias covariates (listwise deletion)
- `68-74` [medium] **linked x1** — compute per-group tallies (red cards, games, dyads, any-red-card count) used to derive rates and percentages by skin-tone group
- `90-95` [high] **linked x10** — specify and fit the primary Poisson model of red cards on darkSkin adjusting for height, weight, league, position, and both bias measures, with log(games) as an offset
- `99-107` [medium] **linked x3** — pull the darkSkin coefficient, SE, and p-value from the primary model and exponentiate them into a rate ratio with a 95% CI
- `121-137` [high] **linked x8** — estimate the adjusted risk difference via marginal standardization: predict P(any red card) under all-dark and all-light counterfactual scenarios from the primary model and average the difference
- `149-178` [high] **linked x5** — quantify uncertainty for the adjusted risk difference via a 5000-draw parametric bootstrap that samples model coefficients from their asymptotic multivariate normal distribution and recomputes the risk difference each draw, then takes the 2.5/97.5 percentiles
- `193-201` [high] **linked x7** — specify and fit a secondary logistic model of any-red-card on darkSkin with the same covariate set, reporting an odds ratio with CI and p-value
- `215-220` [high] **linked x1** — re-derive the dark-skin exposure at an alternate 0.5 cutpoint and refit the Poisson model as a sensitivity check
- `227-232` [high] **linked x1** — refit the Poisson model dropping the implicit/explicit bias covariates from the adjustment set
- `239-244` [high] **linked x1** — refit the Poisson model using the continuous skinTone score in place of the binarized darkSkin exposure
- `260-274` [high] **linked x2** — compute a crude (unadjusted) rate ratio and its CI directly from raw group-level red card and game counts using a log-rate-ratio normal approximation
- `275-314` [medium] **SILENT** — assemble a comparison table choosing which model estimates (unadjusted, primary Poisson, logistic, and the three sensitivity specs) and which columns (estimate, CI bounds, p-value) to report side by side
- `315-319` [high] **linked x2** — test the crude group association with a chi-square test on the 2x2 red-card contingency table to fill in the unadjusted p-value
- `348-352` [medium] **linked x4** — declare the hypothesis 'supported' in the printed conclusion based on the adjusted results, asserted as fixed text rather than derived from a stated significance rule
