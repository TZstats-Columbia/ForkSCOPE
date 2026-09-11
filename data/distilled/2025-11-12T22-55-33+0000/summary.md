# 2025-11-12T22-55-33+0000  (ai)

- code: 300 lines, 39% exon (117 lines in 18 decisions)
- intron: print 62, comment 52, plot 49, import 11, glue 7, config 2
- prose: 235 lines, 66 claims (34 action, 32 result)
- links: 40 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 4
- R_only_consistent_negative: 6
- result_claims_deferred: 32

## Silent decisions — executed, never disclosed

- **29-31** [high] average two independent raters' skin-tone scores into a single continuous skin_tone_avg measure
- **237-238** [medium] bin continuous skin tone into quarter-range categories for a bar-chart summary of red card rate

## Misaligned — code and prose disagree

- code: collapse raw position labels into six broader positional categories (Defender, Defensive Midfielder, Attacking Midfielder/Winger, Forward, Goalkeeper, Other)
  - prose: included player position as a 5-level categorical covariate (Defender[reference], Defensive Midfielder, Attacking Midfielder/Winger, Forward, Goalkeeper)
  - why: code collapses positions into six categories including 'Other'; claim describes a 5-level position covariate omitting the 'Other' category

## All decisions

- `19-20` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path as the full analysis scope
- `29-31` [high] **SILENT** — average two independent raters' skin-tone scores into a single continuous skin_tone_avg measure
- `32-33` [high] **linked x1** — drop dyads missing either rater's skin-tone rating, defining the base analytic sample
- `41-43` [high] **linked x2** — collapse red card count into a binary any-red-card outcome
- `44-46` [high] **linked x3** — binarize continuous skin tone at the midpoint 0.5 into dark vs light skin categories
- `56-63, 270-276` [high] **linked x1** — compute the unadjusted risk difference and odds ratio for red cards between dark- and light-skin groups (and later its normal-approximation SE/CI for plotting), without covariate adjustment
- `69-86` [high] **linked x1** — collapse raw position labels into six broader positional categories (Defender, Defensive Midfielder, Attacking Midfielder/Winger, Forward, Goalkeeper, Other)
- `87-91` [high] **linked x3** — restrict to complete cases on position, height, weight, and referee implicit-bias score, defining the modeling sample
- `98-99` [high] **linked x1** — log-transform games played to reduce skew before use as a covariate
- `102-105` [high] **linked x3** — z-score standardize height, weight, and referee IAT score for use as model covariates
- `117-119` [high] **linked x4** — specify the adjusted logistic model's covariate set: skin tone exposure plus games played, position category, league country, height, weight, and referee bias score
- `120-124` [high] **linked x5** — fit a logistic regression for the outcome with standard errors clustered by player
- `139-147` [high] **linked x5** — approximate the average marginal effect (risk difference) from the logistic coefficient via the delta method at the mean predicted probability, and build its 95% Wald CI
- `160-163` [high] **linked x3** — convert the adjusted log-odds coefficient to an odds ratio and compute its 95% CI by exponentiating coefficient ± 1.96 SE
- `182-189` [medium] **linked x1** — check multicollinearity among model covariates by computing variance inflation factors
- `201-227` [high] **linked x4** — refit the adjusted logistic model across alternative skin-tone cutoffs (0.375, 0.5, 0.625) to test robustness of the dark-skin effect
- `237-238` [medium] **SILENT** — bin continuous skin tone into quarter-range categories for a bar-chart summary of red card rate
- `258-259` [medium] **linked x1** — bin number of games played per dyad into categories for a bar chart of red-card rate by games played
