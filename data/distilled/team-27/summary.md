# team-27  (human)

- code: 96 lines, 60% exon (58 lines in 13 decisions)
- intron: print 21, import 8, glue 4, dead 4, comment 1
- prose: 271 lines, 54 claims (25 action, 29 result)
- links: 25 (7 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 10
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 3
- R_only_consistent_negative: 2
- result_claims_deferred: 29

## Silent decisions — executed, never disclosed

- **14-18** [medium] pull the raw rows into memory as a list of dicts via csv.DictReader rather than reading straight into a pandas dataframe
- **38-39** [high] reload the same source csv into a dataframe with pandas.read_csv for the main analysis, separate from the earlier DictReader pass
- **40-41** [high] narrow the working dataframe down to a fixed list of columns, discarding everything else in the source file

## Misaligned — code and prose disagree

- code: drop rows missing either rater score and construct a single 'rating' exposure variable as the sum of rater1 and rater2 (the comment calls it an average, but no division happens)
  - prose: the two ratings 'rater1' and 'rater2' were averaged into a single variable 'rating'
  - why: claim says rater1 and rater2 were averaged; code sums them with no division
- code: drop rows missing either rater score and construct a single 'rating' exposure variable as the sum of rater1 and rater2 (the comment calls it an average, but no division happens)
  - prose: as with the initial approach, the mean of 'rater1' and 'rater2' was taken to create the variable 'rating'
  - why: claim says the mean of rater1 and rater2 was taken; code adds them without dividing
- code: specify the Question 1 formula: redCards regressed on rating with pairwise interactions against games, goals, yellowCards, meanIAT, and meanExp
  - prose: goals, position, yellow cards, league of player, and country-of-origin bias measures (meanIAT, meanExp) were included in the model
  - why: claim lists position and league among model variables; the code's model includes neither
- code: specify the Question 1 formula: redCards regressed on rating with pairwise interactions against games, goals, yellowCards, meanIAT, and meanExp
  - prose: a Poisson regression was again performed, including the initial-approach variables plus a new variable for player position
  - why: claim adds a player position variable to the model; the code's formula contains no position term
- code: specify the Question 1 formula: redCards regressed on rating with pairwise interactions against games, goals, yellowCards, meanIAT, and meanExp
  - prose: a variable for the league of the player was included in the model
  - why: claim says league was included in the model; the code's formula has no league term
- code: specify the Question 2a formula: redCards regressed on meanIAT with interactions against rating, games, goals, yellowCards, and meanExp
  - prose: the separate regressions previously used to answer questions 2a and 2b were dropped
  - why: claim says the separate question 2a regression was dropped; code still fits it as a distinct model on df_2a
- code: specify the Question 2b formula: redCards regressed on meanExp with interactions against rating, games, goals, yellowCards, and meanIAT
  - prose: the separate regressions previously used to answer questions 2a and 2b were dropped
  - why: claim says the separate question 2b regression was dropped; code still fits it as a distinct model on df_2b

## All decisions

- `14-18` [medium] **SILENT** — pull the raw rows into memory as a list of dicts via csv.DictReader rather than reading straight into a pandas dataframe
- `19-34` [medium] **linked x2** — restrict the IRR check to rows where neither rater score is missing, test the two rating distributions for normality (D'Agostino-Pearson test plus histograms), and on that basis use Spearman's rank correlation instead of Pearson to summarize inter-rater agreement
- `38-39` [high] **SILENT** — reload the same source csv into a dataframe with pandas.read_csv for the main analysis, separate from the earlier DictReader pass
- `40-41` [high] **SILENT** — narrow the working dataframe down to a fixed list of columns, discarding everything else in the source file
- `42-45` [high] **linked x4** — drop rows missing either rater score and construct a single 'rating' exposure variable as the sum of rater1 and rater2 (the comment calls it an average, but no division happens)
- `47-49` [high] **linked x1** — rescale meanIAT and meanExp by a factor of 100 before modeling
- `50-53` [medium] **linked x1** — check redCards' variance against its mean as an informal diagnostic of whether the equidispersion assumption behind a Poisson model is reasonable
- `59-60` [high] **linked x8** — specify the Question 1 formula: redCards regressed on rating with pairwise interactions against games, goals, yellowCards, meanIAT, and meanExp
- `61-64, 76-79, 92-95` [high] **linked x3** — fit each question's model as a Poisson regression via statsmodels rather than some other count-model family
- `71` [high] **linked x1** — restrict the Question 2a sample to rows with a non-missing meanIAT value
- `73-75` [high] **linked x2** — specify the Question 2a formula: redCards regressed on meanIAT with interactions against rating, games, goals, yellowCards, and meanExp
- `87` [high] **linked x1** — restrict the Question 2b sample to rows with a non-missing meanExp value
- `89-91` [high] **linked x2** — specify the Question 2b formula: redCards regressed on meanExp with interactions against rating, games, goals, yellowCards, and meanIAT
