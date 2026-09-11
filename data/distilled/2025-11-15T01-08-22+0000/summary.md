# 2025-11-15T01-08-22+0000  (ai)

- code: 449 lines, 39% exon (173 lines in 20 decisions)
- intron: print 112, plot 75, comment 64, glue 11, import 10, config 4
- prose: 270 lines, 125 claims (43 action, 82 result)
- links: 78 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 11
- result_claims_deferred: 82

## Silent decisions — executed, never disclosed

- **70-74** [high] compute player age at a fixed end-of-season reference date

## All decisions

- `30` [high] **linked x3** — load the raw player-referee dyad dataset from a fixed CSV path
- `34-36` [high] **linked x1** — average the two raters' skin-tone scores into one continuous measure
- `37-40` [medium] **linked x2** — assess inter-rater reliability by restricting to dyads with both ratings present and correlating them
- `42-44` [high] **linked x2** — binarize the outcome as any red card vs none
- `45-51, 321` [high] **linked x5** — dichotomize continuous skin tone at the 0.5 midpoint into light/dark, and mark that cutoff on the distribution plot
- `52-69` [high] **linked x1** — map free-text position strings into four coarse categories via keyword matching, defaulting unmatched values to Unknown
- `70-74` [high] **SILENT** — compute player age at a fixed end-of-season reference date
- `80-86` [high] **linked x7** — restrict the analysis sample to dyads with non-missing skin tone/height/weight and a known position category
- `93-99` [high] **linked x1** — z-score standardize height, weight, age, and games for use in the regression
- `116-118` [medium] **linked x3** — tabulate unadjusted red-card counts and rates by skin-tone group
- `129-131` [high] **linked x17** — specify the primary model: logistic regression of any_red_card on skin_dark adjusted for position, league, games, height, weight, age
- `143-155` [high] **linked x7** — derive the primary estimand as the model-predicted risk difference between all-dark and all-light counterfactual populations
- `167-206` [high] **linked x7** — quantify uncertainty for the risk difference by simulating 10,000 coefficient draws from the model's asymptotic covariance, recomputing the counterfactual risk difference each draw, then taking a percentile CI and a simulation-based two-sided p-value
- `220-221` [medium] **linked x7** — report the skin_dark effect as an odds ratio by exponentiating the logistic coefficient and its CI
- `235-236, 241-243, 247-256` [high] **linked x1** — run a sensitivity model using continuous skin_tone instead of the dichotomized variable, derive its odds ratio, and compute a risk difference between skin_tone=1.0 and skin_tone=0.0 counterfactuals
- `268-273, 278-280, 281-283, 288-298` [high] **linked x1** — discard the middle skin-tone range and redefine groups as very light (<=0.25) vs very dark (>=0.75), refit the adjusted model on that subsample, and compute its odds ratio and counterfactual risk difference
- `326-327` [low] **linked x2** — bin continuous skin_tone into 10 groups to plot an unadjusted dose-response curve of red-card rate
- `358-359` [medium] **linked x4** — fit an unadjusted model (skin_dark only) as the baseline comparison point for the forest plot
- `360-362` [medium] **linked x2** — fit a partially-adjusted model (position, league, games only) as a second comparison point for the forest plot
- `434-444` [medium] **linked x5** — frame the headline conclusion as 'hypothesis not supported' based on the primary risk-difference result, while narrating the sensitivity analyses as showing small but significant effects
