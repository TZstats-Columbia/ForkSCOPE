# 2025-11-29T11-15-38+0000  (ai)

- code: 357 lines, 44% exon (157 lines in 21 decisions)
- intron: print 107, comment 79, import 7, config 4, glue 3
- prose: 277 lines, 112 claims (51 action, 61 result)
- links: 68 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 7
- result_claims_deferred: 61

## Silent decisions — executed, never disclosed

- **33** [medium] pick the soccer.csv dyad-level file as the entire analytic sample

## All decisions

- `33` [medium] **SILENT** — pick the soccer.csv dyad-level file as the entire analytic sample
- `37` [high] **linked x2** — collapse the two independent raters into a single skin-tone score by simple averaging
- `49-61` [high] **linked x4** — roll dyad rows up to one row per player, summing card/game counts and taking the first value for identifying and rating fields
- `66` [high] **linked x1** — dichotomize career red cards into an ever/never outcome
- `69` [high] **linked x7** — drop every player lacking a skin-tone rating from the analytic sample
- `82` [high] **linked x5** — cut the continuous skin-tone score at 0.875 to define an 'extremely dark' exposure group
- `87, 266-278` [high] **linked x3** — use a looser 0.75 darkness cutoff and rerun the model, predicted-probability contrast and odds ratio on it as a sensitivity check
- `90-105` [high] **linked x1** — collapse free-text playing positions into five hand-picked buckets via keyword matching
- `109` [medium] **linked x3** — log(x+1) the yellow-card count instead of leaving it linear, to absorb nonlinearity before it enters the model
- `132` [medium] **linked x3** — read the lower yellow-card rate among dark-skinned players as evidence against an aggressive-play confounding explanation
- `143-146` [high] **linked x8** — fit a logistic regression of any-red-card on the extremely-dark indicator, adjusting for position, league, log-yellow-cards and games played
- `159-172` [high] **linked x6** — standardize the sample under counterfactual all-dark vs all-not-dark exposure and difference the average predicted probabilities to get a risk difference
- `185-212` [high] **linked x1** — define the resampling-with-replacement bootstrap procedure (refit the same model per sample, silently return NaN on non-convergence) and set it to run 1000 iterations
- `214-224` [high] **linked x3** — draw the bootstrap resamples, collect the non-failed risk differences, and take their 2.5/97.5 percentiles as the 95% CI
- `238-239` [high] **linked x4** — exponentiate the primary model's extremelyDark coefficient and its confidence interval to express the effect as an odds ratio
- `252` [high] **linked x2** — pull the Wald p-value for the extremelyDark coefficient out of the primary model as the significance measure
- `254` [high] **linked x2** — call the result significant or not by comparing the p-value to a 0.05 cutoff
- `286-291` [high] **linked x3** — swap in the continuous skin-tone score as the exposure and express its effect as an odds ratio per full-scale unit, as a second sensitivity check
- `298` [high] **linked x3** — further restrict the sample to players with at least 10 games as a quality-control cut for sensitivity analysis 3
- `301-313` [high] **linked x2** — refit the primary model on the games-restricted sample and recompute the standardized risk difference and odds ratio
- `327-352` [high] **linked x5** — narrate the numeric estimates as a large, statistically significant effect and declare the red-card-disparity hypothesis 'SUPPORTED'
