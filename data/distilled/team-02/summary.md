# team-02  (human)

- code: 204 lines, 40% exon (81 lines in 23 decisions)
- intron: comment 87, glue 20, dead 13, config 2, print 1
- prose: 116 lines, 57 claims (23 action, 34 result)
- links: 25 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 11
- C_only_silent_decision: 12
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 6
- result_claims_deferred: 34

## Silent decisions — executed, never disclosed

- **17** [high] load the already-cleaned Stata dataset instead of re-importing and re-saving the raw crowdstorming CSV
- **27-28** [high] treat the string "NA" as missing and convert height to a numeric variable
- **31-32** [high] treat the string "NA" as missing and convert weight to a numeric variable
- **35-36** [high] treat "NA" as missing for position and expand position into a full set of dummy indicators
- **45-48** [high] treat "NA" as missing and convert both raters' skin-tone scores to numeric
- **58-61** [high] dichotomize every skin-tone measure at a cutoff greater than 3 to create dark/light indicator versions
- **74, 77** [high] regress the raw, non-binarized red-card count on a skin-tone measure with no covariates, as an alternate outcome specification
- **166** [high] add the referee-pool's mean implicit-bias (IAT) score as a covariate alongside the core adjustment set
- **188** [high] add the referee-pool's mean explicit-bias (feeling thermometer) score as a covariate alongside the core adjustment set
- **116-121** [high] collapse the panel from player-game rows to one row per player by summing season totals and dropping duplicates, changing the unit of analysis
- **154-155** [high] treat "NA" as missing and convert the mean implicit-bias (IAT) score to numeric
- **158-159** [high] treat "NA" as missing and convert the mean explicit-bias score to numeric

## All decisions

- `17` [high] **SILENT** — load the already-cleaned Stata dataset instead of re-importing and re-saving the raw crowdstorming CSV
- `27-28` [high] **SILENT** — treat the string "NA" as missing and convert height to a numeric variable
- `31-32` [high] **SILENT** — treat the string "NA" as missing and convert weight to a numeric variable
- `35-36` [high] **SILENT** — treat "NA" as missing for position and expand position into a full set of dummy indicators
- `39-42` [high] **linked x1** — derive four league-country dummy indicators from the leaguecountry string, leaving Spain unused later as the implicit reference category
- `45-48` [high] **SILENT** — treat "NA" as missing and convert both raters' skin-tone scores to numeric
- `50` [high] **linked x2** — average the two raters' scores into a single continuous skin-tone measure
- `51-52` [high] **linked x2** — take the lower of the two raters' scores as an alternative skin-tone measure
- `54-55` [high] **linked x2** — take the higher of the two raters' scores as an alternative skin-tone measure
- `58-61` [high] **SILENT** — dichotomize every skin-tone measure at a cutoff greater than 3 to create dark/light indicator versions
- `64-65, 124-126` [high] **linked x1** — collapse the red-card count into a binary any-red-card indicator, first at the game-observation level and again with an adjusted threshold once data are summed to one row per player
- `74, 77` [high] **SILENT** — regress the raw, non-binarized red-card count on a skin-tone measure with no covariates, as an alternate outcome specification
- `83, 90, 132` [high] **linked x3** — estimate the skin-tone/red-card relationship with no covariates at all (bivariate model)
- `84, 91, 133, 165` [high] **linked x4** — adjust the model for player physical traits, position (positionbin2-12, omitting the first category), and country fixed effects (France/Germany/England, Spain as reference)
- `85, 92, 134` [high] **linked x3** — extend the core-adjusted model with season performance totals as additional controls
- `102, 103, 107, 108, 139, 140, 144, 145, 171, 172, 180, 181, 193, 194, 202, 203` [high] **linked x5** — re-estimate the corresponding specification using logit instead of a linear probability model, reporting odds ratios (and dropping player clustering once data are player-level)
- `116-121` [high] **SILENT** — collapse the panel from player-game rows to one row per player by summing season totals and dropping duplicates, changing the unit of analysis
- `154-155` [high] **SILENT** — treat "NA" as missing and convert the mean implicit-bias (IAT) score to numeric
- `158-159` [high] **SILENT** — treat "NA" as missing and convert the mean explicit-bias score to numeric
- `164, 167, 168, 175, 176, 177` [high] **linked x1** — construct and include a skin-tone times implicit-bias interaction term to test moderation, first using continuous then binarized skin tone
- `166` [high] **SILENT** — add the referee-pool's mean implicit-bias (IAT) score as a covariate alongside the core adjustment set
- `186, 189, 190, 197, 198, 199` [high] **linked x1** — construct and include a skin-tone times explicit-bias interaction term to test moderation, first using continuous then binarized skin tone
- `188` [high] **SILENT** — add the referee-pool's mean explicit-bias (feeling thermometer) score as a covariate alongside the core adjustment set
