# team-05  (human)

- code: 108 lines, 53% exon (57 lines in 13 decisions)
- intron: glue 29, plot 13, import 4, print 3, comment 2
- prose: 524 lines, 52 claims (31 action, 21 result)
- links: 49 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 12
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 1
- R_only_consistent_negative: 2
- result_claims_deferred: 21

## Silent decisions — executed, never disclosed

- **7** [high] load the crowdstorming dataset from a CSV file as the analysis input

## All decisions

- `7` [high] **SILENT** — load the crowdstorming dataset from a CSV file as the analysis input
- `11-12` [low] **linked x1** — concatenate playerShort and refNum into a single player-referee pair identifier
- `14-15` [high] **linked x1** — average the two raters' skin-tone scores per player into one continuous rating, ignoring missing rater values
- `17-33` [high] **linked x4** — expand each player-referee aggregate row into one row per game played, and recode red cards received as a binary per-game outcome, turning count totals into bernoulli trials for a later binomial model
- `35-36` [high] **linked x3** — drop rows with a missing average skin-tone rating or missing meanIAT, restricting the sample to complete cases
- `38-39` [high] **linked x2** — rescale the average skin-tone rating from its 1-5 scale onto a 0-1 scale
- `41-42` [high] **linked x3** — restrict to games where at least one red card was shown, defining the comparison group for the observed-frequency plot
- `44-46, 48-49, 51` [high] **linked x1** — truncate skin-tone ratings to integer bins and run a chi-square goodness-of-fit test comparing the rating distribution among red-carded games against the overall expected distribution
- `67, 69-70, 72-73, 75-76, 78-79` [high] **linked x19** — fit a sequence of mixed-effects logistic regression models with progressively richer random-effects structure (intercepts only, then add the fixed skin-tone effect, then a random slope by referee, then a random slope by referee country) to model red cards from skin-tone rating, treating gm3 as the preferred specification
- `81-82, 84-85, 87` [high] **linked x2** — compute each referee country's mean implicit-bias score (meanIAT) and pair it with that country's estimated random slope of the skin-tone effect from gm3, to inspect a country-level association
- `92-93` [high] **linked x5** — add a cross-level interaction between individual skin-tone rating and country-mean implicit bias to the preferred random-effects model
- `96-97, 99-100, 102` [medium] **linked x2** — repeat the country-level aggregation and random-slope extraction for a second country-level measure labeled meanExp (the code re-aggregates data.games.nona$meanIAT and relabels it, rather than referencing a distinct explicit-bias column), pairing it with gm3's random slopes
- `106-107` [high] **linked x6** — add a cross-level interaction between individual skin-tone rating and the country-level meanExp measure to the preferred random-effects model
