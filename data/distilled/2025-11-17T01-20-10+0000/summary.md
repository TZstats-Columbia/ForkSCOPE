# 2025-11-17T01-20-10+0000  (ai)

- code: 440 lines, 42% exon (183 lines in 30 decisions)
- intron: print 151, comment 40, plot 40, glue 13, import 8, config 5
- prose: 176 lines, 116 claims (69 action, 47 result)
- links: 101 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 23
- C_only_silent_decision: 7
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 8
- result_claims_deferred: 47

## Silent decisions — executed, never disclosed

- **227** [high] announce a sensitivity sweep over alternative skin-tone cutoffs
- **252** [high] announce swapping the dichotomized exposure for the raw continuous skin-tone score
- **273** [high] announce adding league-country fixed effects to the adjustment set
- **294** [high] announce dropping yellow-card count from the adjustment set
- **315** [high] announce a minimally-adjusted specification
- **364** [low] populate the forest plot's robustness-check row values with hand-typed literal numbers instead of referencing the actually-computed rd/rd_cont/rd_league/rd_noyellow/rd_min variables from section 5
- **372-373** [low] substitute a single hand-picked approximate CI half-width for every forest-plot row instead of the CI actually computed for each specification

## Misaligned — code and prose disagree

- code: refit the same adjusted logistic model with the dark-skin cutoff swapped to 0.125, 0.375 and 0.5 in turn, recomputing the risk difference and odds ratio for each
  - prose: the specification search explored multiple cutoffs (0.125, 0.25, 0.375, 0.5, 0.625)
  - why: claim lists a 0.625 cutoff among those explored, but the code only refits at 0.125, 0.375, and 0.5 besides the 0.25 primary
- code: dichotomize the continuous skin-tone score into a binary dark-skin exposure at a 0.25 cut point that the code itself notes was chosen because it was most supportive during a specification search
  - prose: 0.25 was chosen as a conceptually defensible, substantive threshold
  - why: the code comment on decision 16 states 0.25 was chosen because it was most supportive during a specification search, contradicting the claim that it was chosen as a conceptually defensible substantive threshold

## All decisions

- `35` [high] **linked x2** — pick the CSV file and treat every row in it as the starting dyad-level dataset
- `39-40` [high] **linked x2** — collapse the two independent rater scores into a single continuous skin-tone score by averaging
- `43-44` [high] **linked x7** — drop every dyad lacking a photo-derived skin tone score from the analysis population
- `54-56, 356-357` [high] **linked x11** — dichotomize the continuous skin-tone score into a binary dark-skin exposure at a 0.25 cut point that the code itself notes was chosen because it was most supportive during a specification search
- `60-61` [high] **linked x3** — define the binary outcome as whether a dyad had any red card at all, ignoring counts above one
- `64-68` [high] **linked x2** — compute player age against a fixed mid-season anchor date rather than per-match or per-season dates
- `69-78, 84` [medium] **linked x1** — collapse detailed playing positions into four coarse buckets via a hand-built lookup table
- `79-83` [high] **linked x7** — fill missing height and weight with the sample median and missing position with an explicit 'Unknown' category rather than dropping those rows
- `138-141, 146` [high] **linked x11** — specify and fit a logistic regression of any-red-card on dark-skin exposure adjusting for games, position category, age, height, weight and yellow cards
- `154-158` [high] **linked x2** — build a counterfactual dataset where every dyad is forced to dark-skin status and predict from the fitted model
- `159-163` [high] **linked x2** — build the mirror counterfactual dataset forcing every dyad to light-skin status and predict from the fitted model
- `164-166` [high] **linked x7** — define the primary effect estimate as the mean difference in predicted probabilities between the two counterfactual worlds (g-computation risk difference)
- `171` [medium] **linked x2** — choose a simulation-based delta method (rather than an analytic or bootstrap approach) to get uncertainty on the risk difference
- `174-199` [high] **linked x6** — draw 5,000 coefficient vectors from the model's asymptotic sampling distribution, recompute the counterfactual risk difference under each draw, and take the 2.5/97.5 percentiles and SD as the CI and SE
- `200-203` [medium] **linked x4** — form a z-statistic and two-sided p-value for the risk difference using the simulated standard error
- `209-213` [high] **linked x6** — report an adjusted odds ratio and its Wald CI, exponentiating the darkSkin coefficient, as a secondary effect measure alongside the risk difference
- `227` [high] **SILENT** — announce a sensitivity sweep over alternative skin-tone cutoffs
- `229-247` [high] **linked x7** — refit the same adjusted logistic model with the dark-skin cutoff swapped to 0.125, 0.375 and 0.5 in turn, recomputing the risk difference and odds ratio for each
- `252` [high] **SILENT** — announce swapping the dichotomized exposure for the raw continuous skin-tone score
- `254-268` [high] **linked x3** — refit the adjusted model using continuous skin tone as the exposure and compute the same risk difference / OR contrasting skinTone=1 vs 0
- `273` [high] **SILENT** — announce adding league-country fixed effects to the adjustment set
- `275-289` [high] **linked x4** — refit the primary model with league country added as a categorical control and recompute the risk difference / OR
- `294` [high] **SILENT** — announce dropping yellow-card count from the adjustment set
- `296-310` [high] **linked x4** — refit the model without yellow cards as a covariate and recompute the risk difference / OR
- `315` [high] **SILENT** — announce a minimally-adjusted specification
- `317-329` [high] **linked x1** — fit a bare-bones model of any-red-card on dark skin and games only, dropping every other covariate, and recompute the risk difference / OR
- `364` [low] **SILENT** — populate the forest plot's robustness-check row values with hand-typed literal numbers instead of referencing the actually-computed rd/rd_cont/rd_league/rd_noyellow/rd_min variables from section 5
- `372-373` [low] **SILENT** — substitute a single hand-picked approximate CI half-width for every forest-plot row instead of the CI actually computed for each specification
- `419, 430-431` [low] **linked x2** — state specific exclusion count and baseline red-card rate figures in the written summary that are typed as literals rather than sourced from the variables computed earlier (len(df)-len(df_analysis) at line 46, pred_light.mean() at line 168)
- `425-429, 433-435` [medium] **linked x5** — characterize the result as 'SUPPORTED' and frame it as robust across specifications, an interpretive labeling choice layered on top of the computed statistics
