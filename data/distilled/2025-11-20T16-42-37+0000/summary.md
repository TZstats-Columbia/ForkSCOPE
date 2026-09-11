# 2025-11-20T16-42-37+0000  (ai)

- code: 355 lines, 54% exon (191 lines in 18 decisions)
- intron: print 103, comment 49, import 7, config 5
- prose: 201 lines, 83 claims (40 action, 43 result)
- links: 59 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 6
- result_claims_deferred: 43

## Misaligned — code and prose disagree

- code: drop dyads missing either rater's skin-tone score
  - prose: dyads missing skin tone ratings from both raters were excluded as unclassifiable
  - why: code drops dyads missing either rater's score; claim says only dyads missing ratings from both raters were excluded

## All decisions

- `28` [high] **linked x1** — load the raw player-referee dyad dataset from the soccer CSV file
- `31-35` [medium] **linked x2** — check inter-rater agreement between the two skin-tone raters via Spearman correlation on complete pairs
- `40, 45, 309` [high] **linked x3** — keep only player-referee dyads with at least 2 games together
- `41-42, 46` [high] **linked x2** — drop dyads missing either rater's skin-tone score
- `47-49` [high] **linked x1** — average the two raters' scores into a single skin-tone value per player
- `50-55` [high] **linked x1** — cut the averaged skin-tone score into light (≤0.125) and dark (≥0.750) groups
- `56-58` [high] **linked x1** — collapse the red card count into a yes/no indicator for any red card
- `59-62` [high] **linked x2** — keep only the light and dark extreme groups for the comparison sample, dropping intermediate tones
- `77-91, 94, 314` [medium] **linked x2** — bucket free-text position strings into five broad role categories by keyword matching
- `95-98, 315-317` [high] **linked x2** — fill missing height/weight with the sample median and missing IAT/experience with the sample mean
- `99-103, 318-319` [medium] **linked x3** — derive per-game yellow-card and goal rates and a log-transformed games-played exposure term
- `114-119` [high] **linked x7** — specify and fit the adjusted logistic regression of any red card on dark skin plus exposure, physical, behavioral, bias, position and league covariates
- `129-190, 326, 346` [high] **linked x7** — derive the average marginal effect (risk difference) for dark skin with delta-method standard errors and a 95% normal-approximation CI
- `196-202` [high] **linked x2** — convert the dark-skin log-odds coefficient into an odds ratio with a Wald 95% CI
- `251-253` [medium] **linked x3** — scale the risk difference against the light-skin baseline rate to get a relative percentage increase
- `270-284` [high] **linked x6** — declare the hypothesis supported only if the risk-difference p-value is below 0.05 and the CI lower bound exceeds zero, and phrase the conclusion accordingly
- `302-308, 310-313, 320-325, 327-332` [high] **linked x6** — refit the adjusted model under three alternative light/dark threshold definitions to check sensitivity of the effect estimate
- `336-345, 347-350` [high] **linked x8** — refit the model across five nested covariate sets, from unadjusted to fully adjusted, to see how the estimate moves
