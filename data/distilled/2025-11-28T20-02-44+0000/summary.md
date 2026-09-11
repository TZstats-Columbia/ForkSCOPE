# 2025-11-28T20-02-44+0000  (ai)

- code: 358 lines, 46% exon (165 lines in 19 decisions)
- intron: print 155, comment 25, import 8, config 5
- prose: 246 lines, 98 claims (55 action, 43 result)
- links: 45 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 17
- R_only_consistent_negative: 9
- result_claims_deferred: 43

## Silent decisions — executed, never disclosed

- **27-28** [medium] load the raw player-referee dyad dataset from the CSV file

## All decisions

- `27-28` [medium] **SILENT** — load the raw player-referee dyad dataset from the CSV file
- `32-33` [high] **linked x2** — average the two raters' skin-tone scores into one continuous skinTone measure
- `36-38` [high] **linked x1** — turn red card counts into a binary any-red-card outcome
- `43-45` [high] **linked x1** — drop rows lacking a skin-tone rating
- `48-49` [high] **linked x1** — drop rows lacking height or weight
- `52-69` [high] **linked x1** — bucket free-text position strings into Defender/Midfielder/Forward/Goalkeeper/Other/Unknown via keyword matching
- `70, 72-73` [high] **linked x1** — remove goalkeepers from the analysis sample
- `87-91` [high] **linked x2** — carve out several binary dark/light skin-tone cutoffs (0.5, 0.75, 0.125) for use as alternative exposures
- `92-94` [high] **linked x2** — log-transform games played
- `95-99` [high] **linked x1** — rescale height and weight to mean 0, SD 1 before modeling
- `119-122` [high] **linked x2** — keep only the most extreme light- and dark-skinned dyads for the main contrast, and flag which side of the split each dyad falls on
- `131, 133-137` [high] **linked x10** — fit the main logistic regression of any-red-card on extreme skin tone, adjusting for games, position, height, weight, league
- `141, 143-146, 273-276, 304-307, 336-339` [high] **linked x3** — get standard errors that account for repeated dyads per player by clustering on playerShort
- `147-154, 277-282, 308-313, 340-345` [medium] **linked x1** — turn the coefficient/SE pair into a Wald z-statistic and one-/two-sided p-values via the normal approximation
- `155-162, 283-286, 314-317` [high] **linked x1** — translate the logistic coefficient into an average marginal effect (percentage-point risk difference) using p*(1-p)
- `175-176, 232-254, 293-294, 324-325, 350-351` [high] **linked x10** — call the result supported/marginally supported/not supported off p<0.05, p<0.10, or a CI that excludes zero, and reuse the same cutoffs to grade each robustness check as consistent or not
- `264, 268-272` [high] **linked x2** — rerun the model with skin tone collapsed at the coarser 0.5 cut instead of the extreme split
- `295, 299-303` [high] **linked x2** — rerun the model treating skin tone as a continuous 0-1 predictor instead of binarizing it
- `326, 330-335` [high] **linked x2** — swap to a Poisson model on raw red-card counts with a log-games offset instead of the binary logistic outcome
