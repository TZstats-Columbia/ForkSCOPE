# 2025-11-20T18-12-31+0000  (ai)

- code: 391 lines, 49% exon (190 lines in 21 decisions)
- intron: print 125, comment 65, import 6, config 4, glue 1
- prose: 242 lines, 92 claims (51 action, 41 result)
- links: 55 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 7
- result_claims_deferred: 41

## Silent decisions — executed, never disclosed

- **32-33** [high] load the raw player-referee dyad dataset from a fixed CSV path
- **59-61** [high] exclude dyads with zero recorded games (no exposure)
- **148-149** [medium] compute the raw, unadjusted risk difference between dark- and light-skin groups

## All decisions

- `32-33` [high] **SILENT** — load the raw player-referee dyad dataset from a fixed CSV path
- `40-41` [high] **linked x1** — drop dyads that are missing a skin-tone rating from either rater
- `44-45` [high] **linked x1** — average the two raters' ratings into one continuous skin-tone score
- `46-49` [high] **linked x5** — dichotomize the continuous skin-tone score into a binary dark/light indicator at a 0.25 cutoff
- `59-61` [high] **SILENT** — exclude dyads with zero recorded games (no exposure)
- `63-66` [high] **linked x1** — exclude dyads with a missing player position
- `68-74` [high] **linked x1** — exclude dyads with missing height or weight
- `76-82` [high] **linked x2** — exclude dyads whose height or weight falls outside a plausible physiological range (160-210cm, 50-110kg)
- `84-90` [high] **linked x1** — exclude dyads missing referee implicit-bias measures
- `99-115` [high] **linked x1** — z-score standardize the continuous covariates height, weight, meanIAT and meanExp
- `116-119` [medium] **linked x2** — encode the outcome as red-card and no-red-card trial counts for a binomial model
- `148-149` [medium] **SILENT** — compute the raw, unadjusted risk difference between dark- and light-skin groups
- `160-166` [high] **linked x8** — fit a binomial GLM with logit link regressing red-card outcome on dark_skin, log(games) and categorical position
- `179-194, 250-258` [high] **linked x6** — estimate the adjusted risk difference by averaging model-predicted probabilities under counterfactual dark_skin=0 vs dark_skin=1 for every observation
- `199-213, 259-270` [medium] **linked x7** — approximate the risk difference's uncertainty via a delta-method-scaled coefficient SE, then build a normal-approximation 95% CI and two-sided p-value
- `226-229, 275-279` [high] **linked x3** — report the effect as an adjusted odds ratio by exponentiating the model coefficient, with a Wald-based CI
- `243-249` [high] **linked x5** — expand the adjustment set into a robustness model adding league, height, weight and referee bias measures
- `291-316` [high] **linked x3** — re-run the dichotomization and modeling under alternative skin-tone cutpoints (0.375, 0.5) as a robustness/sensitivity check
- `325-334, 338-348` [high] **linked x2** — re-specify the exposure as the continuous skin-tone score instead of the dichotomized indicator, and estimate the risk difference across the full 0-to-1 range
- `381` [low] **linked x3** — report the total number excluded using a hardcoded assumed original sample size (146028) rather than the size of the originally loaded dataset
- `383-388` [low] **linked x3** — declare the hypothesis 'supported' and characterize the effect as statistically significant and robust across specifications
