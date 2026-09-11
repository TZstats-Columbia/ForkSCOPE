# 2025-11-19T07-38-28+0000  (ai)

- code: 412 lines, 29% exon (118 lines in 20 decisions)
- intron: print 128, comment 92, plot 61, import 10, config 2, glue 1
- prose: 232 lines, 88 claims (54 action, 34 result)
- links: 62 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 5
- result_claims_deferred: 34

## Silent decisions — executed, never disclosed

- **277-278** [high] restrict this sensitivity sample to dyads with non-missing referee bias scores
- **324-325, 330** [low] compute the plotted error bars from a normal-approximation SE of the raw proportions times 1.96
- **340** [low] limit the position breakdown plot to the 10 most frequent positions

## Misaligned — code and prose disagree

- code: take the 2.5/97.5 percentiles of the bootstrap draws as the CI and derive a p-value from a normal approximation to the bootstrap SE
  - prose: p-values were computed via two-sided Wald tests using cluster-robust standard errors
  - why: claim says p-values came from two-sided Wald tests, but the primary risk-difference p-value is derived from a normal approximation to the bootstrap SE

## All decisions

- `35-36` [high] **linked x2** — read the raw player-referee dyad CSV as the dataset and unit of analysis
- `42` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `47` [high] **linked x4** — collapse red card counts into a yes/no indicator of any red card in the dyad
- `52-55` [high] **linked x3** — cut continuous skin tone into light/medium/dark bins at fixed thresholds
- `69, 73, 236` [high] **linked x5** — keep only light and dark dyads and code dark skin as the binary exposure
- `76` [high] **linked x1** — drop dyads missing position, height, or weight before modeling
- `82-84, 238-240, 279-280` [medium] **linked x2** — z-score the continuous covariates before entering them in the model
- `106-111, 243-244, 263-264, 281-284` [high] **linked x9** — pick position, league, height, weight and games played as the covariates to adjust for
- `116-120, 245-247, 265-267, 286-288` [high] **linked x7** — fit a logistic regression with standard errors clustered by player
- `133-143` [high] **linked x4** — use g-computation, predicting outcomes under everyone-light and everyone-dark, to get a marginal risk difference
- `158-163, 168-171, 173, 176-189` [high] **linked x1** — resample players with replacement 1000 times and refit the model to build a bootstrap distribution, silently dropping non-converging draws
- `193-197` [high] **linked x3** — take the 2.5/97.5 percentiles of the bootstrap draws as the CI and derive a p-value from a normal approximation to the bootstrap SE
- `214-221` [high] **linked x7** — convert the logistic coefficient to an odds ratio with a Wald-type exponentiated CI
- `234-235, 237, 241-242` [high] **linked x5** — rerun the model on the full sample including medium skin tone, adding a separate medium-tone dummy
- `258-260, 261-262` [high] **linked x1** — rerun the model treating skin tone as a standardized continuous exposure instead of a category
- `277-278` [high] **SILENT** — restrict this sensitivity sample to dyads with non-missing referee bias scores
- `285` [high] **linked x2** — add the referee's implicit and explicit bias scores as extra covariates
- `324-325, 330` [low] **SILENT** — compute the plotted error bars from a normal-approximation SE of the raw proportions times 1.96
- `340` [low] **SILENT** — limit the position breakdown plot to the 10 most frequent positions
- `403-406` [medium] **linked x4** — declare the hypothesis unsupported using an uncorrected 0.05 significance threshold on the bootstrap p-value, without adjusting for the multiple analyses run
