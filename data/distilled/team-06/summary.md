# team-06  (human)

- code: 224 lines, 62% exon (139 lines in 26 decisions)
- intron: glue 63, dead 11, comment 8, config 3
- prose: 483 lines, 53 claims (34 action, 19 result)
- links: 29 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 10
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 6
- result_claims_deferred: 19

## Silent decisions — executed, never disclosed

- **9-10** [high] load the raw crowdstorming CSV as the full working dataset
- **11** [high] parse the birthday string into a date using day-month-year format
- **12** [high] derive player age as 2012 minus birth year
- **13-16** [high] force-convert height, weight, meanIAT, and meanExp from string to numeric, coercing unparseable values to missing
- **17-24** [medium] encode player, position, referee number, league-country, and referee-country string fields into numeric ID variables for later grouping/fixed-effects use
- **47-50** [high] drop observations with missing values on any player-characteristic control variable
- **60, 115-116, 170-171** [high] set referee (refID) as the panel unit for fixed-effects/clustered models
- **69** [high] fit a referee fixed-effects model of red cards with clustered SEs
- **188-201** [medium] select and format rater1/highExp interaction coefficients for the Exp results table
- **202-214** [medium] select and format rater2/highExp interaction coefficients for the Exp results table

## All decisions

- `6` [high] **linked x7** — pick refCountryID as the variable on which standard errors are clustered in every regression model
- `9-10` [high] **SILENT** — load the raw crowdstorming CSV as the full working dataset
- `11` [high] **SILENT** — parse the birthday string into a date using day-month-year format
- `12` [high] **SILENT** — derive player age as 2012 minus birth year
- `13-16` [high] **SILENT** — force-convert height, weight, meanIAT, and meanExp from string to numeric, coercing unparseable values to missing
- `17-24` [medium] **SILENT** — encode player, position, referee number, league-country, and referee-country string fields into numeric ID variables for later grouping/fixed-effects use
- `25-26` [high] **linked x1** — restrict the sample to rows with non-missing rater1/rater2 ratings and games==1
- `33-36` [high] **linked x1** — dichotomize implicit-bias score (meanIAT) into a high/low indicator split at the sample mean
- `37-40` [high] **linked x1** — dichotomize explicit-bias score (meanExp) into a high/low indicator split at the sample mean
- `41-42` [high] **linked x1** — expand position, rater x highIAT, rater x highExp, and club into indicator/interaction dummy variables for the design matrix
- `45-46` [high] **linked x1** — choose age, height, and weight as the player-characteristic control variables
- `47-50` [high] **SILENT** — drop observations with missing values on any player-characteristic control variable
- `51-55` [high] **linked x1** — define four alternative right-hand-side specifications (rater dummies with/without player controls, club fixed effects) for the main models
- `60, 115-116, 170-171` [high] **SILENT** — set referee (refID) as the panel unit for fixed-effects/clustered models
- `63` [high] **linked x4** — fit an OLS/linear-probability model of red cards on the chosen specification with clustered SEs
- `69` [high] **SILENT** — fit a referee fixed-effects model of red cards with clustered SEs
- `78-91` [medium] **linked x1** — select rater1-block OLS/FE coefficients and formatting to report in the main LaTeX results table
- `92-104` [medium] **linked x1** — select rater2-block OLS/FE coefficients and formatting to report in the main LaTeX results table
- `107-111` [high] **linked x2** — define right-hand-side specifications adding the rater x highIAT interaction terms for the implicit-bias-moderation models
- `119` [high] **linked x2** — fit the rater x highIAT interaction model of red cards with clustered SEs
- `133-146` [medium] **linked x1** — select and format rater1/highIAT interaction coefficients for the IAT results table
- `147-159` [medium] **linked x1** — select and format rater2/highIAT interaction coefficients for the IAT results table
- `163-166` [high] **linked x2** — define right-hand-side specifications adding the rater x highExp interaction terms for the explicit-bias-moderation models
- `174` [high] **linked x2** — fit the rater x highExp interaction model of red cards with clustered SEs
- `188-201` [medium] **SILENT** — select and format rater1/highExp interaction coefficients for the Exp results table
- `202-214` [medium] **SILENT** — select and format rater2/highExp interaction coefficients for the Exp results table
