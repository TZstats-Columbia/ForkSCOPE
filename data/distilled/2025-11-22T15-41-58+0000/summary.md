# 2025-11-22T15-41-58+0000  (ai)

- code: 277 lines, 39% exon (107 lines in 19 decisions)
- intron: print 115, comment 48, import 5, config 2
- prose: 192 lines, 95 claims (37 action, 58 result)
- links: 53 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 5
- R_only_consistent_negative: 8
- result_claims_deferred: 58

## Silent decisions — executed, never disclosed

- **89-92** [high] recode missing position and league-country values as an explicit 'Unknown' category instead of dropping them
- **183-187** [medium] derive player age by subtracting the parsed birth year from a hardcoded reference year (2012)
- **225-231** [medium] break down the unadjusted dark-vs-light red-card rate gap separately within each of the four leagues

## All decisions

- `28-29` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path as the entire analysis input
- `34-36` [high] **linked x1** — average the two raters' scores into a single continuous skin-tone measure
- `37-40` [low] **linked x1** — restrict to dyads rated by both raters and quantify their agreement via Pearson correlation and exact-match rate
- `53-54` [high] **linked x1** — drop dyads lacking any skin-tone rating from the working sample
- `57-63` [high] **linked x5** — dichotomize skin tone at 0.5/0.25 cutoffs into dark vs. light categories and discard the medium band entirely
- `69-70` [high] **linked x1** — collapse red-card counts into a binary any-red-card outcome
- `86-88` [high] **linked x3** — log-transform total games played to use as an exposure control
- `89-92` [high] **SILENT** — recode missing position and league-country values as an explicit 'Unknown' category instead of dropping them
- `93-95, 192-196` [high] **linked x2** — z-score the continuous covariates (yellow cards, age, height, weight) before they enter the regression
- `96-98, 117-118, 200-201, 235-236` [high] **linked x3** — cluster standard errors by player to account for repeated observations per player across all three fitted models
- `114-116, 119-122` [high] **linked x6** — fit a logistic regression of any-red-card on skin-tone category adjusting for games, position, league, and yellow cards
- `135-146` [high] **linked x9** — convert the isDark coefficient into an average-marginal-effect risk difference on the percentage-point scale, with its SE/CI/p-value
- `164-167` [high] **linked x5** — re-express the isDark coefficient as an odds ratio via exponentiation, with its CI and p-value
- `183-187` [medium] **SILENT** — derive player age by subtracting the parsed birth year from a hardcoded reference year (2012)
- `188-189` [high] **linked x1** — restrict the sensitivity sample to complete cases on age, height, and weight rather than imputing missing values
- `197-199, 202-211` [high] **linked x2** — refit the risk-difference model adding age, height, and weight controls and recompute the marginal-effect risk difference for comparison
- `225-231` [medium] **SILENT** — break down the unadjusted dark-vs-light red-card rate gap separately within each of the four leagues
- `232-234, 237-240` [high] **linked x8** — add an isDark-by-league interaction term to test whether the skin-tone effect varies across leagues
- `254-255, 260-261, 264-265` [high] **linked x3** — declare the hypothesis supported only when the risk difference is significant at p<0.05 and its CI lower bound is above zero
