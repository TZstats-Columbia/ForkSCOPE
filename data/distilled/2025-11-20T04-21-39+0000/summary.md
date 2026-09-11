# 2025-11-20T04-21-39+0000  (ai)

- code: 494 lines, 46% exon (227 lines in 22 decisions)
- intron: print 117, plot 86, comment 49, import 8, config 5, glue 2
- prose: 256 lines, 114 claims (39 action, 75 result)
- links: 78 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 19
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 7
- result_claims_deferred: 75

## Silent decisions — executed, never disclosed

- **52-54, 90** [high] collapse red-card counts into a binary any-red-card outcome
- **59-74, 87-88, 317** [high] bucket free-text playing positions into five coarse groups (Goalkeeper/Defender/Midfielder/Forward/Other) and apply that mapping at both player and dyad level
- **374-378** [medium] bin the continuous skin-tone score into eighths to plot red-card rate by category

## Misaligned — code and prose disagree

- code: hardcode two of the four forest-plot estimates ('Unadjusted RR' and 'Adjusted RR (player-level)') as literal numbers rather than values computed anywhere in this script
  - prose: all analyses are fully reproducible from the provided Python script, which generates all reported estimates/CIs/p-values, the sensitivity analyses, and diagnostic plots
  - why: claim says the script generates all reported estimates, but code hardcodes 'Unadjusted RR' and 'Adjusted RR (player-level)' as literals rather than computing them

## All decisions

- `33-34` [medium] **linked x1** — load the full player-referee dyad dataset from soccer.csv with no upfront filtering
- `42-44` [high] **linked x3** — drop dyads that are missing either skin-tone rater score
- `45` [high] **linked x2** — average the two raters' scores into one continuous skin-tone measure
- `52-54, 90` [high] **SILENT** — collapse red-card counts into a binary any-red-card outcome
- `59-74, 87-88, 317` [high] **SILENT** — bucket free-text playing positions into five coarse groups (Goalkeeper/Defender/Midfielder/Forward/Other) and apply that mapping at both player and dyad level
- `75-86` [high] **linked x1** — collapse dyad rows to one row per player, picking sum/first/max per column
- `89, 316` [high] **linked x6** — split the continuous skin-tone score into a dark/light exposure at the 0.5 midpoint
- `94-101, 318-324` [high] **linked x3** — keep only rows with non-missing height, weight, and a known position category
- `114-116, 127, 139, 379, 397` [medium] **linked x1** — express red-card counts as a rate per 1000 games for reporting and plotting
- `118-126, 128-129, 132-133, 135-138` [medium] **linked x3** — pick which counts and rates to tabulate when describing red cards by skin-tone group and by position
- `149-159` [high] **linked x7** — fit the primary adjusted model: Poisson regression of red cards on dark_skin plus position/league/height/weight with a log(games) offset
- `163-178` [high] **linked x7** — derive the adjusted risk difference by g-computation: score every player as if dark-skinned vs light-skinned at a one-game exposure and average the predictions
- `186, 188-222, 223-224` [high] **linked x3** — quantify uncertainty by resampling players with replacement 2000 times and refitting the whole risk-difference pipeline, silently skipping iterations where the fit errors out
- `225-229` [high] **linked x4** — build the 95% interval from the 2.5/97.5 percentiles of the bootstrap draws and define a two-sided p-value from the share of draws crossing zero
- `252-257` [high] **linked x5** — fit a secondary logistic model of any_red_card on dark_skin with the same covariate set as the main model
- `261-264` [medium] **linked x6** — exponentiate the logit coefficient and its Wald interval to report an odds ratio
- `280-281, 283-295` [high] **linked x6** — re-run the Poisson model swapping in alternative skin-tone cutoffs (0.25, 0.375, 0.5) instead of only the primary threshold
- `297-298, 300-308` [high] **linked x9** — re-run the model with skin_tone left as a continuous exposure instead of dichotomized
- `311-312, 314-315, 325-334` [high] **linked x8** — re-run the model at the dyad level instead of one row per player, and cluster standard errors by player
- `374-378` [medium] **SILENT** — bin the continuous skin-tone score into eighths to plot red-card rate by category
- `409-414` [medium] **linked x1** — hardcode two of the four forest-plot estimates ('Unadjusted RR' and 'Adjusted RR (player-level)') as literal numbers rather than values computed anywhere in this script
- `463-466, 472-475, 484-489` [high] **linked x2** — declare significance and hypothesis support using a 0.05 p-value cutoff
