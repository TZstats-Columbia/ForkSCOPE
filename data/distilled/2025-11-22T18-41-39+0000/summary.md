# 2025-11-22T18-41-39+0000  (ai)

- code: 371 lines, 42% exon (154 lines in 22 decisions)
- intron: print 82, plot 69, comment 38, glue 19, import 8, config 1
- prose: 225 lines, 130 claims (33 action, 97 result)
- links: 58 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 7
- result_claims_deferred: 97

## Silent decisions — executed, never disclosed

- **260-273** [medium] assemble a single comparison table juxtaposing N, risk difference, CI, p-value and OR across the unadjusted, primary and position models
- **297-306** [low] compute the unadjusted red-card rate for each of the three skin-tone categories on the full ratings sample for display

## All decisions

- `24-26` [high] **linked x1** — load the raw dyad-level dataset from a fixed CSV path
- `33, 35` [high] **linked x2** — average the two raters' scores into a single skin_tone measure
- `34` [high] **linked x2** — drop dyads missing either rater's skin-tone score before any skin-tone analysis
- `36-38` [low] **linked x2** — quantify rater agreement as the Pearson correlation between the two raters
- `42-48` [high] **linked x1** — bucket continuous skin_tone into light/medium/dark using cut points at 0.25 and 0.75
- `52-54, 59` [high] **linked x6** — narrow the analysis to a light-vs-dark contrast by dropping medium and encoding a binary dark_skin exposure
- `57-58, 281-283` [high] **linked x1** — define any_red_card as an indicator for receiving one or more red cards
- `60, 238` [medium] **linked x2** — transform games played with log(games+1) for use as a model covariate
- `61-63, 237` [high] **linked x1** — drop players missing height or weight before modeling
- `78-84` [high] **linked x3** — split the sample into light/dark groups and compute the raw difference in red-card rates
- `89-93` [medium] **linked x1** — test independence of red-card receipt and skin-tone group with a chi-square test
- `95-98` [high] **linked x1** — express the unadjusted light-vs-dark contrast as an odds ratio
- `108-115` [high] **linked x7** — fit a logistic model of any_red_card on dark_skin adjusting for log_games, yellowCards and league, clustering standard errors by player
- `129-133, 190-192, 251` [high] **linked x4** — convert a logistic coefficient (and its CI) to an odds ratio via exponentiation for reporting
- `139-149, 197-206` [high] **linked x5** — estimate the adjusted risk difference by predicting outcomes under counterfactual all-light and all-dark exposure and averaging the difference
- `150-159, 207-209, 212-213, 321-322` [medium] **linked x5** — approximate the risk-difference estimate's standard error via the delta method and derive a 95% CI and p-value from a normal approximation
- `175-176` [high] **linked x2** — restrict the sensitivity sample to rows with non-missing position
- `178-184` [high] **linked x3** — add player position as an additional covariate to the adjusted model as a robustness check
- `222-223, 225-232` [medium] **linked x5** — recompute the unadjusted risk difference separately within each league, skipping leagues with no dark-skin observations
- `233-234, 236, 239-244` [high] **linked x4** — refit the adjusted model treating skin_tone as a continuous exposure instead of the binary contrast
- `260-273` [medium] **SILENT** — assemble a single comparison table juxtaposing N, risk difference, CI, p-value and OR across the unadjusted, primary and position models
- `297-306` [low] **SILENT** — compute the unadjusted red-card rate for each of the three skin-tone categories on the full ratings sample for display
