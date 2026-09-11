# 2025-11-22T00-56-43+0000  (ai)

- code: 375 lines, 35% exon (130 lines in 17 decisions)
- intron: print 120, plot 69, comment 45, import 7, glue 2, config 2
- prose: 287 lines, 87 claims (44 action, 43 result)
- links: 49 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 5
- result_claims_deferred: 43

## All decisions

- `23-25` [high] **linked x1** — load the full soccer player-referee dyad dataset from a local CSV as the raw analysis base
- `26-28` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `29-31` [high] **linked x2** — drop dyads lacking a skin-tone rating before analysis
- `32-34` [high] **linked x2** — dichotomize continuous skin tone into a darkSkin indicator using a 0.5 cutoff
- `35-37` [high] **linked x3** — collapse red card counts into a binary any-red-card outcome per dyad
- `38-40` [high] **linked x2** — log-transform games played, with a 0.5 offset, for use as a modeling covariate
- `41-44` [high] **linked x3** — drop dyads missing height, weight, position, leagueCountry, or meanIAT to form the modeling sample
- `69-72, 76-78` [high] **linked x1** — restrict to dyads both raters scored and quantify agreement via Pearson/Spearman correlation plus exact-match and within-0.25 agreement rates
- `87-91` [high] **linked x1** — compute the crude (unadjusted) red-card rate difference and odds ratio between dark- and light-skin groups
- `106-116` [high] **linked x10** — specify the adjusted logistic regression of any red card on darkSkin controlling for games, position, league country, height, weight, and referee implicit-bias score, fit with player-clustered standard errors
- `138-168` [high] **linked x6** — derive the adjusted risk difference as the average marginal effect between all-dark and all-light counterfactual predictions, with its delta-method standard error, 95% CI, and p-value
- `186-193` [high] **linked x5** — exponentiate the darkSkin coefficient and its confidence interval to report an adjusted odds ratio as a secondary effect measure
- `208-218` [high] **linked x2** — restrict to extreme skin-tone groups (below 0.25 vs above 0.5, dropping the middle) and refit the adjusted model with this alternate dichotomization
- `225-232` [high] **linked x3** — refit the adjusted model using continuous skinTone in place of the binary exposure
- `238-246` [high] **linked x2** — refit the adjusted model omitting the position covariate
- `250-257` [high] **linked x2** — refit a minimally-adjusted model controlling only for log_games
- `364-373` [high] **linked x3** — characterize the results as SUPPORTING the referee-bias hypothesis and enumerate selected evidentiary bullet points rather than a more measured causal-inference framing
