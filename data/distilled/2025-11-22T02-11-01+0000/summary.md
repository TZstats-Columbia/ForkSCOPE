# 2025-11-22T02-11-01+0000  (ai)

- code: 432 lines, 34% exon (149 lines in 18 decisions)
- intron: print 97, plot 86, glue 73, comment 11, import 11, config 5
- prose: 254 lines, 78 claims (37 action, 41 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 6
- result_claims_deferred: 41

## All decisions

- `36-37` [high] **linked x3** — load the raw dyad-level dataset from a fixed path as the entire source and scope of the analysis, with no upfront filtering
- `42-43` [high] **linked x2** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `45-48` [medium] **linked x2** — restrict to dyads with both ratings present and quantify inter-rater reliability via correlation and exact-agreement rate
- `52-53` [high] **linked x1** — collapse red card counts into a binary any-red-card outcome indicator
- `55-57` [high] **linked x1** — derive player age by subtracting birth year from a fixed reference year (2012), coercing unparseable birthdays to missing
- `59-61, 67-68` [high] **linked x4** — define dark/light exposure using extreme skin-tone rating thresholds (>=0.875 / <=0.125) and drop all players whose rating falls between them from the analytic sample
- `71-72` [high] **linked x4** — drop dyads with missing position, height, weight, or age from the analytic sample
- `95-101` [medium] **linked x2** — compute crude (unadjusted) red-card rates and counts by exposure group for comparison against the adjusted estimate
- `108-113` [medium] **linked x2** — check covariate balance across exposure groups for a chosen set of variables (games, age, height, weight) by comparing group means
- `123-125` [high] **linked x4** — choose the adjustment set and functional form for the outcome model: darkSkin plus games, position, leagueCountry, age, height, weight, meanIAT, meanExp
- `127-136` [high] **linked x6** — fit the adjustment model as a GEE with a binomial family and exchangeable within-player correlation structure, clustering by playerShort
- `162-174` [high] **linked x4** — estimate the adjusted risk difference via g-computation: predict outcomes under counterfactual all-dark and all-light exposure and contrast the averaged predictions
- `184-190, 199-219` [high] **linked x2** — quantify uncertainty in the g-computation risk difference via a parametric bootstrap: redraw GEE coefficients from their asymptotic multivariate normal distribution (5000 draws) and recompute the counterfactual contrast each draw
- `221-226` [high] **linked x2** — summarize the bootstrap distribution as a 2.5/97.5 percentile 95% CI and derive a two-sided z-based p-value using the bootstrap standard error
- `243-253` [high] **linked x5** — report the darkSkin coefficient as a secondary estimand on the odds-ratio scale by exponentiating the coefficient and its Wald CI from the model
- `268-272, 277-286` [high] **linked x4** — repeat the primary GEE analysis after redefining exposure as strictly extreme skin-tone ratings (0 vs 1) instead of the <=0.125/>=0.875 bands, as a sensitivity check
- `287-293` [medium] **linked x2** — compute the sensitivity-analysis odds ratio and its 95% CI using a manual Wald approximation (coefficient +/- 1.96*SE) rather than the model's built-in confidence interval used for the primary OR
- `305-327` [high] **linked x3** — declare the hypothesis supported or not based on whether the primary p-value crosses the 0.05 significance threshold, and phrase the narrative conclusion text accordingly
