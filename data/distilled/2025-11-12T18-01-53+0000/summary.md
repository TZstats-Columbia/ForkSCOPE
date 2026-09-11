# 2025-11-12T18-01-53+0000  (ai)

- code: 320 lines, 38% exon (120 lines in 19 decisions)
- intron: print 90, comment 46, plot 32, glue 17, import 11, config 4
- prose: 240 lines, 109 claims (48 action, 61 result)
- links: 80 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 5
- result_claims_deferred: 61

## Silent decisions — executed, never disclosed

- **233-241** [medium] bin continuous skin tone into five display categories with custom edges for the bar chart

## All decisions

- `39-40` [high] **linked x2** — load the raw player-referee dyad CSV as the analysis population
- `46-47` [high] **linked x2** — average the two independent raters' skin-tone scores into one continuous measure
- `48-52` [high] **linked x7** — split the continuous skin-tone score into a dark/light binary at the 0.5 midpoint
- `53-55` [high] **linked x2** — collapse any-red-card counts into a yes/no outcome
- `56-58` [high] **linked x2** — drop dyads that have no skin-tone rating at all
- `61-77` [medium] **linked x2** — bucket free-text playing positions into five coarse groups (goalkeeper/defender/midfielder/forward/other)
- `78-82` [high] **linked x1** — derive player age in 2013 from parsed birthdate
- `83-92` [high] **linked x5** — restrict to dyads with complete data on height, weight, position, age and both referee bias measures
- `96-99` [medium] **linked x2** — mark position and league country as categorical for dummy-coding in the model
- `116-117` [medium] **linked x3** — compare raw mean red-card rate between the dark and light skin-tone groups
- `128-130` [high] **linked x19** — specify the linear probability model's outcome and full covariate/adjustment set
- `131-136` [high] **linked x2** — cluster standard errors by player to account for repeated dyads per player
- `141-142, 207-208, 220-221, 257-262` [high] **linked x3** — build a 95% confidence interval as estimate plus or minus 1.96 standard errors
- `158-172` [high] **linked x6** — fit a logistic GEE model with exchangeable within-player correlation as the secondary specification
- `179-181` [high] **linked x6** — exponentiate the log-odds coefficient and its interval to report an odds ratio
- `197-203` [high] **linked x3** — rerun the primary model with an alternative dark/light cutoff of 0.375 instead of 0.5
- `211-216` [high] **linked x6** — rerun the primary model treating skin tone as continuous rather than binarized
- `233-241` [medium] **SILENT** — bin continuous skin tone into five display categories with custom edges for the bar chart
- `310-315` [high] **linked x7** — define the bias hypothesis as 'supported' only if p<0.05 and the confidence interval excludes zero from below
