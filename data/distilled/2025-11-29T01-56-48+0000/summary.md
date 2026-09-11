# 2025-11-29T01-56-48+0000  (ai)

- code: 275 lines, 53% exon (145 lines in 18 decisions)
- intron: print 92, comment 27, import 6, config 4, glue 1
- prose: 191 lines, 81 claims (42 action, 39 result)
- links: 42 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 9
- result_claims_deferred: 39

## Silent decisions — executed, never disclosed

- **71-76** [medium] carve out the specific set of columns that will constitute the modeling dataset

## All decisions

- `29-30` [high] **linked x2** — read the raw player-referee dyad dataset from a fixed CSV path as the analysis's starting scope
- `32-34` [high] **linked x2** — average the two raters' skin-tone codings into a single continuous score
- `36-38` [high] **linked x1** — collapse the red card count into a binary any-red-card outcome
- `39-43` [high] **linked x3** — dichotomize continuous skin tone at a 0.125 cutoff into a binary dark-skin exposure group
- `44-46` [high] **linked x3** — drop dyads with no skin-tone rating (missing photo) from the analysis sample
- `50-66` [high] **linked x2** — bucket free-text playing position into five coarse categories, treating missing position as its own group
- `67-68` [high] **linked x2** — fill missing height and weight with the sample median
- `69-70` [medium] **linked x1** — derive player age as a fixed reference year minus birth year, ignoring month/day and parse failures
- `71-76` [medium] **SILENT** — carve out the specific set of columns that will constitute the modeling dataset
- `87-97` [high] **linked x1** — compare raw red-card rates between light and dark skin groups via a two-proportion normal-approximation z-test and CI
- `120-123` [high] **linked x4** — fit the primary logistic regression of any-red-card on darkSkin adjusting for league, position, age, height, weight, yellow cards and goals
- `124-131` [high] **linked x3** — convert the darkSkin coefficient into an adjusted odds ratio with a Wald-style 95% CI
- `132-136` [high] **linked x3** — standardize the fitted model's predictions at darkSkin=1 vs darkSkin=0 to obtain an adjusted risk-difference estimate
- `143, 145-166` [high] **linked x3** — bootstrap the adjusted risk difference by resampling dyads with replacement and refitting the logistic model 500 times, using the 2.5/97.5 percentiles as the CI
- `190, 192-206` [high] **linked x2** — re-run the adjusted model with a looser dark-skin cutoff (skinTone > 0.25) as a sensitivity check
- `211, 213-227` [high] **linked x2** — re-run the adjusted model with a stricter, inclusive dark-skin cutoff (skinTone >= 0.50) as a sensitivity check
- `232, 234-249` [high] **linked x2** — re-run the adjusted model treating skin tone as continuous rather than dichotomized, as a sensitivity check
- `261-262` [high] **linked x6** — declare the hypothesis 'supported' using a two-sided p<0.05 threshold combined with a positive coefficient sign
