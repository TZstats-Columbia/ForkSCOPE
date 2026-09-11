# team-24  (human)

- code: 138 lines, 65% exon (90 lines in 14 decisions)
- intron: glue 38, comment 7, import 2, dead 1
- prose: 113 lines, 46 claims (40 action, 6 result)
- links: 40 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 2
- result_claims_deferred: 6

## Silent decisions — executed, never disclosed

- **6** [high] pick the raw crowdstorming CSV as the data source, read in as-is with UTF-8 encoding

## Misaligned — code and prose disagree

- code: derive a per-player career goals total from the player list and merge it back in as a new column
  - prose: a variable for each player's average number of goals per game was computed
  - why: claim says average goals per game; code derives a career goals total and never divides by games
- code: mean-center the implicit and explicit bias scores using the average over non-excluded referee-countries (the corresponding sd is computed but not applied)
  - prose: height, weight, meanIAT, and meanExp variables were standardized
  - why: claim says meanIAT/meanExp were standardized; code only mean-centers them and does not divide by the sd

## All decisions

- `6` [high] **SILENT** — pick the raw crowdstorming CSV as the data source, read in as-is with UTF-8 encoding
- `23-29, 130, 136` [high] **linked x2** — flag referee-countries whose implicit/explicit bias survey has too few respondents (SE above sd/5, or missing) and drop them when building the bias-interaction models
- `33-34` [high] **linked x1** — combine the two raters' scores into a single skin-tone rating by averaging them
- `36-52` [high] **linked x3** — expand each player-referee row into one row per game refereed, and allocate that dyad's total red/yellow-red cards to the first N games rather than a specific game
- `58-68` [medium] **linked x2** — derive a per-player career goals total from the player list and merge it back in as a new column
- `70-78` [high] **linked x1** — collapse left/right variants of winger, fullback and midfielder into a single side-agnostic position category
- `87-94` [medium] **linked x4** — compute player age as of the script's run date from birthdate and z-standardize it at creation; also z-standardize height, weight and goals in the modeling frame
- `95-100` [high] **linked x2** — mean-center the implicit and explicit bias scores using the average over non-excluded referee-countries (the corresponding sd is computed but not applied)
- `101-104` [high] **linked x3** — standardize the rating variable using the mean and sd of each player's first-listed rater-average rating
- `109-110, 112-113, 115-116, 118` [high] **linked x3** — backward-eliminate predictors from the full mixed model via drop1, dropping goals then age across successive models
- `111, 114, 117` [high] **linked x1** — restrict the exploratory model fits to complete cases only, via listwise deletion of any row with an NA
- `122-126` [high] **linked x8** — fit the primary model of rating's effect on red cards on the full (unfiltered) sample, then report the effect as a percentage-point change with a Wald confidence interval
- `128-129, 131-132` [high] **linked x5** — add an implicit-bias (meanIAT) by rating interaction, fit only on countries with adequate implicit-bias data, and report the interaction as a percentage-point change with Wald CI
- `134-135, 137-138` [high] **linked x5** — add an explicit-bias (meanExp) by rating interaction, fit only on countries with adequate explicit-bias data, and report the interaction as a percentage-point change with Wald CI
