# 2025-11-29T20-04-37+0000  (ai)

- code: 335 lines, 41% exon (136 lines in 15 decisions)
- intron: print 126, comment 38, glue 23, import 7, config 5
- prose: 256 lines, 90 claims (52 action, 38 result)
- links: 61 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 14
- result_claims_deferred: 38

## Silent decisions — executed, never disclosed

- **284-304** [medium] assemble the results_summary table, filling the alternative-cutpoint rows with hard-coded OR/CI/p-value literals rather than referencing the values computed in the cutpoint loop

## All decisions

- `33-34` [high] **linked x1** — load the raw player-referee dyad dataset from CSV as the analysis population
- `37-39` [high] **linked x3** — drop any player-referee dyad missing either rater's skin-tone score before analysis
- `43-46` [high] **linked x3** — average the two raters' skin-tone scores into a single continuous skin_tone measure
- `47-49` [high] **linked x5** — collapse the red-card count into a binary any-red-card outcome (redCards > 0)
- `50-54` [high] **linked x9** — dichotomize skin_tone at 0.125 — a cutpoint the comment says was chosen via specification search to maximize effect size — to define the primary dark_skin exposure
- `75-77, 84-87` [high] **linked x1** — compute the crude red-card-rate difference and fit a logistic regression of any_red_card on dark_skin alone, with no covariates, as an unadjusted estimate
- `109-111` [high] **linked x5** — specify and fit the primary logistic regression of any_red_card on dark_skin adjusting for games and 12-category player position
- `126-127` [high] **linked x6** — exponentiate the primary model's dark_skin coefficient and CI to express the adjusted association as an odds ratio
- `147-163` [high] **linked x5** — standardize via g-computation: predict each dyad's red-card probability under counterfactual dark_skin=0 vs dark_skin=1 from the primary model and average the individual differences to get the population-average adjusted risk difference
- `166, 168-181` [high] **linked x6** — quantify uncertainty for the adjusted risk difference via a 10,000-draw parametric bootstrap that resamples model coefficients from their asymptotic multivariate-normal distribution, then take 2.5/97.5 percentiles and a two-sided p-value
- `198-201` [high] **linked x1** — add league country as an additional covariate to the adjusted model as a robustness check
- `208-209, 210-216` [high] **linked x4** — re-fit the adjusted model at alternative skin-tone cutpoints (0.25, 0.375, 0.5) to test sensitivity of the primary exposure threshold
- `224-227` [high] **linked x3** — re-fit the adjusted model using continuous skin_tone instead of dichotomized dark_skin, to check sensitivity to dichotomization
- `239-275` [medium] **linked x9** — interpret the risk-difference and odds-ratio estimates and declare the hypothesis SUPPORTED, framing p<0.001 and a CI excluding zero as strong evidence
- `284-304` [medium] **SILENT** — assemble the results_summary table, filling the alternative-cutpoint rows with hard-coded OR/CI/p-value literals rather than referencing the values computed in the cutpoint loop
