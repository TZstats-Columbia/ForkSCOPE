# 2025-11-20T20-17-27+0000  (ai)

- code: 362 lines, 35% exon (126 lines in 18 decisions)
- intron: print 100, plot 68, comment 39, glue 17, import 11, config 1
- prose: 266 lines, 117 claims (51 action, 66 result)
- links: 61 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 11
- R_only_consistent_negative: 10
- result_claims_deferred: 66

## Silent decisions — executed, never disclosed

- **252-255, 279, 298** [low] approximate standard errors/confidence intervals for the descriptive plot panels using a normal (Wald) approximation on the binomial rates and log-odds ratio

## Misaligned — code and prose disagree

- code: restrict the sample to complete cases on height, weight, and position category, dropping the rest
  - prose: no additional exclusions were made for missing covariates
  - why: decision 14 drops dyads with missing height/weight/position, but claim says no exclusions were made for missing covariates

## All decisions

- `29-31` [high] **linked x3** — read in the raw player-referee dyad dataset from CSV as the analysis population
- `35-37` [high] **linked x1** — average the two independent raters' scores into a single continuous skin_tone measure
- `44-52` [high] **linked x4** — bin the continuous skin_tone score into light (0.00-0.25) vs dark (0.75-1.00) categories, leaving the 0.25-0.75 middle range as missing/excluded
- `53-55` [high] **linked x2** — collapse the red-card count into a binary any-red-card indicator per dyad
- `66-68` [high] **linked x5** — drop dyads with missing or middle-range skin tone, keeping only the two extreme categories for analysis
- `69-86` [high] **linked x1** — collapse free-text position strings into broad role buckets (Goalkeeper/Defender/Midfielder/Forward/Other/Missing) via keyword matching
- `87-93` [high] **linked x2** — restrict the sample to complete cases on height, weight, and position category, dropping the rest
- `112-131` [medium] **linked x4** — compute and report the crude, unadjusted red-card rate difference and odds ratio between dark- and light-skinned players as a pre-adjustment benchmark
- `136-142` [high] **linked x1** — z-standardize the continuous covariates (height, weight, games, goals) before entering them into the regression
- `143-145` [high] **linked x3** — one-hot encode position category and league country, dropping the first level as reference
- `146-160` [high] **linked x7** — choose which covariates make up the adjustment set entering the regression models
- `167-168, 180, 215` [high] **linked x5** — cluster standard errors by player to account for repeated dyads contributed by the same player
- `177-179` [high] **linked x7** — choose a linear probability model (OLS) as the primary specification for estimating the risk difference
- `190-194` [medium] **linked x2** — rescale the risk-difference coefficient and CI from a proportion to percentage points for reporting
- `212-214` [high] **linked x4** — choose a logistic regression as the secondary specification for estimating the odds ratio
- `225-229` [medium] **linked x2** — exponentiate the logit coefficient and CI to report an odds ratio rather than a log-odds scale
- `252-255, 279, 298` [low] **SILENT** — approximate standard errors/confidence intervals for the descriptive plot panels using a normal (Wald) approximation on the binomial rates and log-odds ratio
- `349-357` [high] **linked x8** — apply a two-sided alpha=0.05 significance threshold together with the sign of the CI to decide whether the hypothesis is supported, contradicted, or undetermined
