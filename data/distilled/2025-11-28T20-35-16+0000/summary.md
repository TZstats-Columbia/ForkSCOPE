# 2025-11-28T20-35-16+0000  (ai)

- code: 374 lines, 32% exon (120 lines in 17 decisions)
- intron: print 143, comment 49, glue 48, import 9, config 5
- prose: 292 lines, 106 claims (49 action, 57 result)
- links: 68 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 8
- result_claims_deferred: 57

## Silent decisions — executed, never disclosed

- **81-84** [medium] choose which outcome, exposure, and covariate columns are carried into the modeling dataset

## All decisions

- `42-43` [high] **linked x1** — load the full soccer referee-dyad dataset from a fixed csv path with no filtering
- `49-50, 53` [high] **linked x1** — exclude player-referee dyads that lack a skin-tone rating from either rater
- `56-58` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skin_tone measure
- `59-63` [high] **linked x5** — binarize skin_tone into a dark_skin exposure using a >0.125 cutoff, chosen to maximize contrast
- `64-66` [high] **linked x4** — collapse the red-card count into a binary any_red_card outcome
- `76-80` [high] **linked x1** — derive player age as days from birthday to a fixed 2013-01-01 reference date
- `81-84` [medium] **SILENT** — choose which outcome, exposure, and covariate columns are carried into the modeling dataset
- `85-88` [high] **linked x4** — restrict the modeling dataset to complete cases by dropping rows with any missing covariate
- `99-105, 107-108` [high] **linked x17** — specify and fit the primary logistic regression of any_red_card on dark_skin adjusting for games, age, position and league country
- `123-126, 220-222, 233-235, 246-248, 261-263` [medium] **linked x8** — exponentiate the skin-tone coefficient (and its CI) to express effects as an odds ratio, across the primary and every sensitivity model
- `141-154` [high] **linked x8** — estimate the adjusted risk difference via g-computation, predicting outcomes under everyone-light vs everyone-dark counterfactuals and averaging the difference
- `164-189` [high] **linked x3** — quantify uncertainty in the risk difference with a 1000-draw parametric bootstrap that resamples the dark_skin coefficient from its normal sampling distribution
- `194-196` [high] **linked x1** — test the risk difference for significance with a two-sided Wald z-test
- `210, 212-219` [high] **linked x2** — re-define the exposure with a stricter 0.25 skin-tone cutoff and refit the adjusted model, to test sensitivity to the threshold choice
- `228, 230-232` [high] **linked x3** — add yellowCards as an extra covariate and refit, to test sensitivity to omitting a play-aggression proxy
- `241, 243-245` [high] **linked x3** — refit using continuous skin_tone instead of the binarized exposure, to test sensitivity to dichotomization
- `254, 256-260` [high] **linked x5** — recompute standard errors clustered by player, to test sensitivity to within-player correlation across dyads
