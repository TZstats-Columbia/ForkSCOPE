# 2025-11-21T00-55-35+0000  (ai)

- code: 411 lines, 43% exon (177 lines in 18 decisions)
- intron: print 132, plot 47, comment 45, import 6, config 4
- prose: 226 lines, 106 claims (58 action, 48 result)
- links: 69 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 14
- result_claims_deferred: 48

## Silent decisions — executed, never disclosed

- **32-34** [high] load the raw player-referee dyad dataset from CSV as the analysis population

## All decisions

- `32-34` [high] **SILENT** — load the raw player-referee dyad dataset from CSV as the analysis population
- `36-38` [high] **linked x2** — average the two independent raters' skin-tone ratings into one continuous skinTone score
- `39-41` [high] **linked x3** — collapse any nonzero red card count into a binary outcome indicator
- `42-44` [high] **linked x2** — drop dyads that lack a skin-tone rating from the analysis sample
- `46-48` [high] **linked x5** — dichotomize continuous skin tone into dark/light exposure groups at a 0.5 cutoff
- `49-55` [high] **linked x2** — exclude dyads missing position, height, or weight covariate data from the modeling sample
- `57-72` [high] **linked x2** — collapse detailed field positions into four coarse categories (Defender, Midfielder, Forward, Goalkeeper)
- `87-91` [high] **linked x1** — compute the raw (unadjusted) red-card rate gap between dark- and light-skin groups
- `105-107` [high] **linked x7** — specify the outcome model's covariate adjustment set and functional form (games, position category, league country, height, weight)
- `108-109, 111-115` [high] **linked x4** — fit the adjustment model as logistic regression with standard errors clustered by player
- `119-124` [high] **linked x3** — convert the model's darkSkin coefficient and CI into an odds ratio effect measure
- `140-141, 143-160` [high] **linked x9** — estimate the adjusted risk difference by G-computation: set darkSkin to 1 and 0 for the whole sample, predict outcome probabilities under each, and difference the averages
- `174-175, 177-180, 181-184, 200-202, 203-204, 207-217, 218-223` [high] **linked x10** — build a confidence interval for the risk difference by drawing model coefficients from a multivariate-normal sampling distribution and recomputing the G-computation risk difference for each draw
- `185-189, 190-195, 196-199` [medium] **linked x1** — restrict the per-simulation risk-difference recomputation to a 10,000-row subsample instead of the full dataset for tractability
- `224-226` [medium] **linked x1** — derive a two-sided p-value from the simulated risk-difference distribution as twice the smaller tail proportion on either side of zero
- `244-245, 247-248, 249-255, 256-259` [high] **linked x2** — rerun the adjusted model on a sensitivity subsample restricted to extreme skin tones, redefining exposure at 0.25/0.75 cutoffs
- `263-264, 266-271, 272-275` [high] **linked x6** — rerun the adjusted model treating skin tone as a continuous linear predictor instead of a binary exposure
- `386-406` [medium] **linked x9** — declare the hypothesis 'not supported' by comparing the primary risk-difference p-value and CI against a 0.05 significance threshold, while separately narrating the significant continuous-exposure sensitivity result
