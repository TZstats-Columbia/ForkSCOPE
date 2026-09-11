# 2025-11-21T01-57-03+0000  (ai)

- code: 323 lines, 24% exon (76 lines in 16 decisions)
- intron: print 129, comment 47, plot 41, glue 20, import 8, config 2
- prose: 323 lines, 144 claims (51 action, 93 result)
- links: 81 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 11
- result_claims_deferred: 93

## Silent decisions — executed, never disclosed

- **30-31** [high] load the raw dyad-level dataset from a fixed CSV path as the analysis population
- **60-63** [high] parse birthday strings and derive player age relative to a fixed mid-season reference date (2012.5)

## All decisions

- `30-31` [high] **SILENT** — load the raw dyad-level dataset from a fixed CSV path as the analysis population
- `34-35` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skintone measure
- `39-47` [high] **linked x2** — cut continuous skintone into three ordinal bands (light/medium/dark) at fixed thresholds 0.25 and 0.5
- `48-50` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `55-57` [high] **linked x4** — drop the ambiguous medium skin-tone group and keep only light vs dark dyads, recoding as a dark_skin indicator
- `60-63` [high] **SILENT** — parse birthday strings and derive player age relative to a fixed mid-season reference date (2012.5)
- `64-65` [high] **linked x2** — restrict the modeling sample to rows with non-missing position and age, dropping the rest
- `86-95` [high] **linked x4** — compute unadjusted red card rates for each skin-tone group and their crude risk difference
- `101-106` [high] **linked x1** — test the crude association between dark_skin and any_red_card with a chi-square test of independence
- `109-115` [high] **linked x4** — check covariate balance between skin-tone groups via two-sample t-tests on games, yellowCards, age
- `126-127, 130` [high] **linked x14** — estimate the adjusted risk difference with an OLS linear probability model using HC3 heteroskedasticity-robust standard errors
- `128-129` [high] **linked x12** — choose the adjustment set of covariates (games, yellowCards, position, leagueCountry, age) alongside dark_skin
- `167-169` [high] **linked x14** — fit a logistic regression on the same specification to obtain an adjusted odds ratio
- `194-199` [high] **linked x5** — recompute standard errors clustered by player to account for within-player correlation across dyads
- `220, 224-226` [medium] **linked x11** — explore whether the dark_skin effect varies by league via group-wise rates and a dark_skin×leagueCountry interaction model
- `304-313` [high] **linked x5** — classify the hypothesis as supported/not supported based on whether the adjusted risk-difference CI excludes zero, and in which direction
