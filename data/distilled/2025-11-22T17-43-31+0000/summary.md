# 2025-11-22T17-43-31+0000  (ai)

- code: 372 lines, 38% exon (142 lines in 20 decisions)
- intron: print 129, comment 51, glue 36, import 10, config 4
- prose: 300 lines, 118 claims (47 action, 71 result)
- links: 69 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 8
- result_claims_deferred: 71

## All decisions

- `31-32` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV file/season, setting the scope of the whole analysis
- `45-47, 49` [medium] **linked x2** — restrict to dyads rated by both graders and quantify inter-rater agreement with a Pearson correlation
- `51-53` [high] **linked x1** — average the two raters' scores into one continuous skin-tone measure
- `54-60` [high] **linked x2** — bucket the continuous skin-tone score into light/medium/dark groups using fixed cutoffs at 0.25 and 0.75
- `72-75` [high] **linked x3** — drop the medium skin-tone group and encode the remaining light/dark split as a binary exposure indicator
- `76-78, 291` [high] **linked x1** — define the outcome as receiving any red card, dichotomizing the red card count
- `79-81, 292` [high] **linked x1** — log-transform games played for use as a playing-time control variable
- `82-84` [high] **linked x2** — drop dyads missing position, height, weight, or league, restricting the primary analytic sample to covariate-complete cases
- `101-106, 122-125` [high] **linked x2** — compute the unadjusted (crude) risk difference between dark- and light-skinned groups as a baseline comparison
- `135-137` [high] **linked x7** — specify the adjustment set for the primary model as log games, position, league, height, and weight
- `138-142` [high] **linked x8** — fit the specification as a logistic regression with standard errors clustered by player to account for repeated dyads
- `157-172` [high] **linked x7** — estimate the adjusted risk difference by standardization: predict outcomes with everyone set to light skin and to dark skin, then average the difference
- `186-188, 226-258` [high] **linked x6** — quantify uncertainty in the adjusted risk difference via a parametric bootstrap: draw parameter vectors from the model's asymptotic sampling distribution, recompute the standardized risk difference for each draw, and summarize with percentile CI and a two-sided tail-proportion p-value
- `271-275` [high] **linked x5** — report the exponentiated coefficient (adjusted odds ratio) and its Wald confidence interval as a secondary effect measure
- `288-290, 293` [high] **linked x2** — build an alternate sample that keeps medium skin tones and uses the continuous skin-tone score instead of the light/dark split, filtering missing position/height/weight but not league here
- `296-302` [high] **linked x3** — refit the adjusted logistic model with continuous skin tone in place of the binary exposure, again clustering SEs by player, as a sensitivity check
- `316-322, 325-328` [high] **linked x5** — add a dark_skin × league interaction term to test whether the effect varies by league, then derive each league's simple-effect odds ratio by summing the main-effect and interaction coefficients
- `329-332` [high] **linked x1** — test whether the interaction model fits significantly better than the main-effects model via a likelihood-ratio chi-square test fixed at 3 degrees of freedom
- `358` [low] **linked x1** — report the count of excluded dyads by subtracting the analysis N from a hardcoded original sample size (146028) rather than a value computed from the loaded data
- `361-369` [high] **linked x8** — apply a 0.05 significance threshold to the bootstrap p-value and narrate whether the referee-bias hypothesis is judged supported or not
