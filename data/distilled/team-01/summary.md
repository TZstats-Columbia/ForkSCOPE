# team-01  (human)

- code: 600 lines, 79% exon (474 lines in 21 decisions)
- intron: glue 59, comment 38, dead 15, other 8, config 5, print 1
- prose: 421 lines, 51 claims (19 action, 32 result)
- links: 60 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 4
- R_only_unbacked_action_claim: 3
- R_only_consistent_negative: 1
- result_claims_deferred: 32

## Silent decisions — executed, never disclosed

- **6-7** [high] point the analysis at the pre-cleaned maindata.dta as the full sample to load
- **26-32** [high] treat the literal string 'NA' as missing and convert the rating, anthropometric, and bias variables from string to numeric
- **80-83** [high] define a binary any-card outcome combining reds, second-yellow reds, and yellow cards
- **132-142** [medium] choose age, height, weight, yellow cards, red cards, and any-red as the variables reported in the summary-statistics table

## All decisions

- `6-7` [high] **SILENT** — point the analysis at the pre-cleaned maindata.dta as the full sample to load
- `19-25, 33-37` [high] **linked x1** — split the birthday string into day/month/year and compute player age (plus its square) using a fixed reference year of 2013
- `26-32` [high] **SILENT** — treat the literal string 'NA' as missing and convert the rating, anthropometric, and bias variables from string to numeric
- `38-41` [high] **linked x1** — average the two human raters' skin-tone scores into one continuous rating
- `42-49, 50-63, 64-68` [high] **linked x1** — expand each referee-player dyad into one row per game played and assign the dyad's total observed cards to the first N expanded game-rows rather than modeling at the dyad level
- `75-79` [high] **linked x1** — define a binary any-red-card outcome combining straight reds and second-yellow reds
- `80-83` [high] **SILENT** — define a binary any-card outcome combining reds, second-yellow reds, and yellow cards
- `89-92` [high] **linked x1** — add squared height and weight terms so the card models can fit a nonlinear body-size relationship
- `93-118` [high] **linked x1** — collapse referees to one observation per country (dropping duplicates and countries missing an IAT or EXP score), z-standardize the country-level implicit and explicit bias scores, and merge them back onto the full sample keeping all original rows
- `132-142` [medium] **SILENT** — choose age, height, weight, yellow cards, red cards, and any-red as the variables reported in the summary-statistics table
- `155-169` [high] **linked x6** — model red cards as a linear function of average skin-tone rating, reporting a nested cascade from bivariate up through body-size/age controls, league and position fixed effects, club fixed effects, and referee fixed effects
- `170-197` [high] **linked x6** — re-estimate the red-card/skin-tone relationship as a logit with average marginal effects, using the same nested control cascade up through league, position, and club fixed effects
- `205-222` [high] **linked x3** — re-run the red-card cascade treating the raw 5-point rater1 score as a categorical predictor instead of the averaged continuous rateravg score
- `223-241` [high] **linked x3** — repeat the linear control cascade with any-red-card as the outcome
- `242-269` [high] **linked x4** — repeat the logit control cascade with any-red-card as the outcome
- `277-293` [high] **linked x3** — repeat the categorical (i.rater1) nonlinear cascade with any-red-card as the outcome
- `294-312` [high] **linked x4** — repeat the linear control cascade with yellow cards as the outcome
- `321-345` [high] **linked x5** — repeat the logit control cascade with yellow cards as the outcome
- `353-370` [high] **linked x3** — repeat the categorical (i.rater1) nonlinear cascade with yellow cards as the outcome
- `378-383` [high] **linked x1** — collapse the 5-point rater1 skin-tone scale into a binary dark/light group, splitting ratings 1-2 versus 3-5
- `384-442, 448-508, 518-576` [high] **linked x16** — test whether the implicit/explicit bias-score effect on each card outcome differs between dark- and light-skin-toned players by fitting separate subgroup regressions (with and without player fixed effects) and manually computing a t-test on the coefficient difference, instead of a single interaction model
