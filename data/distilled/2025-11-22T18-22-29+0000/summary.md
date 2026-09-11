# 2025-11-22T18-22-29+0000  (ai)

- code: 278 lines, 41% exon (114 lines in 15 decisions)
- intron: print 106, comment 39, import 7, glue 7, config 5
- prose: 244 lines, 104 claims (50 action, 54 result)
- links: 60 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 14
- result_claims_deferred: 54

## Misaligned — code and prose disagree

- code: quantify uncertainty in the risk difference with a 1000-iteration dyad-level nonparametric bootstrap, refitting the model each draw, discarding non-converging iterations, and deriving a percentile CI and a doubled one-sided-tail p-value
  - prose: confidence intervals were computed via a parametric bootstrap with 1,000 replications using dyad-level resampling
  - why: claim labels the resampling a parametric bootstrap; code performs a nonparametric dyad-level bootstrap

## All decisions

- `33-34` [high] **linked x5** — load the raw player-referee dyad dataset from CSV as the analytic universe
- `37-39` [high] **linked x2** — average the two independent raters' skin-tone scores into one continuous skin-tone measure
- `40-43` [medium] **linked x2** — assess rater agreement via Pearson correlation restricted to dyads where both raters scored
- `45-47` [high] **linked x4** — exclude dyads with no skin-tone score from the analysis dataset
- `50-52` [high] **linked x2** — collapse red-card count into a binary any-red-card outcome per dyad
- `53-55` [high] **linked x4** — dichotomize the averaged skin-tone score into dark vs light groups using a 0.5 cutoff
- `60-62` [high] **linked x4** — further restrict the modeling sample to dyads with non-missing player position
- `78-83` [high] **linked x9** — specify the primary model as logistic regression of any-red-card on dichotomized skin tone adjusting for games, position, and league country, with SEs clustered by player
- `97-108` [high] **linked x5** — estimate the adjusted risk difference via average marginal effects, comparing predictions under all-dark vs all-light counterfactual skin tone
- `120-123, 125-148, 153-159` [high] **linked x5** — quantify uncertainty in the risk difference with a 1000-iteration dyad-level nonparametric bootstrap, refitting the model each draw, discarding non-converging iterations, and deriving a percentile CI and a doubled one-sided-tail p-value
- `174-176` [medium] **linked x3** — convert the primary model's coefficient and CI into an odds ratio to report as a secondary effect measure
- `191, 193-198` [high] **linked x3** — refit the model using the continuous skin-tone score instead of the dichotomized indicator as a sensitivity check
- `202, 204-209` [high] **linked x2** — add yellow-card count as a covariate to test whether adjusting for playing style attenuates the skin-tone effect
- `212-213, 215-222` [high] **linked x3** — rebuild the dark/light indicator separately from each individual rater's score and refit the model per rater to test sensitivity to using the averaged rating
- `261-273` [high] **linked x7** — interpret the evidence as supporting the hypothesis while weighing statistical significance against small absolute effect size and listing caveats (missingness, heterogeneity, attenuation with yellow cards)
