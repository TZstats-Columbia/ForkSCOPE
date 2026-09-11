# 2025-11-20T22-39-34+0000  (ai)

- code: 382 lines, 21% exon (80 lines in 21 decisions)
- intron: print 135, comment 76, plot 58, import 10, other 10, glue 10, config 3
- prose: 311 lines, 111 claims (56 action, 55 result)
- links: 85 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 4
- result_claims_deferred: 55

## Silent decisions — executed, never disclosed

- **270-273** [low] compute a normal-approximation (Wald) 95% CI as mean plus/minus 1.96 times SEM for the descriptive red-card rate chart

## All decisions

- `34` [medium] **linked x1** — load the full raw referee/player dyad dataset from one fixed CSV file as the entire analysis universe
- `49` [high] **linked x1** — average the two raters' skin-tone scores into one continuous skinTone measure
- `52` [medium] **linked x1** — drop dyads where either rater's skin-tone score is missing
- `61-66` [high] **linked x4** — cut continuous skin tone into light/medium/dark categories using cutoffs at 0.325 and 0.675
- `75` [high] **linked x3** — collapse red card count into a binary any-red-card outcome (count > 0)
- `90-92` [high] **linked x4** — keep only light and dark skin-tone dyads (drop medium) and encode exposure as a 0/1 darkSkin indicator
- `94-100` [high] **linked x4** — restrict to complete cases on height, weight, position and meanIAT, dropping any dyad missing one of these
- `116-118` [medium] **linked x3** — compute unadjusted mean red-card rate separately for light- and dark-skin groups as the baseline comparison
- `125-127` [low] **linked x1** — pick a specific subset of variables (games, yellowCards, goals, height, weight) to summarize by skin-tone group
- `140-142` [high] **linked x2** — one-hot encode position and league country, dropping the first level as reference category
- `143-148` [high] **linked x16** — assemble the covariate/adjustment set used in the primary regression model
- `154-157` [high] **linked x1** — fit an unadjusted linear probability model with standard errors clustered by player
- `166-168` [high] **linked x6** — fit the covariate-adjusted linear probability model with standard errors clustered by player
- `177-178` [high] **linked x13** — refit the adjusted linear probability model with HC3 heteroskedasticity-robust SEs and mark this as the preferred specification
- `195-198` [high] **linked x1** — fit an unadjusted logistic regression and report the effect on the odds-ratio scale
- `204-210` [high] **linked x9** — fit a fully covariate-adjusted logistic regression via formula and report the effect as an odds ratio
- `216` [medium] **linked x6** — compute the average marginal effect of dark skin at the overall sample composition as an alternate risk-difference estimate
- `237-243` [high] **linked x1** — build a separate sensitivity sample that keeps all skin-tone categories (including medium) and restricts only on covariate completeness
- `244-251` [high] **linked x4** — re-specify exposure as continuous skin tone rather than a binary category in an adjusted logistic model, reporting the OR per unit increase
- `270-273` [low] **SILENT** — compute a normal-approximation (Wald) 95% CI as mean plus/minus 1.96 times SEM for the descriptive red-card rate chart
- `374-378` [low] **linked x4** — frame the effect as a relative percentage increase (adjusted risk difference divided by the unadjusted light-skin rate) and declare the hypothesis supported
