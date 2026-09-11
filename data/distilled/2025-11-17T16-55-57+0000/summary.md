# 2025-11-17T16-55-57+0000  (ai)

- code: 298 lines, 40% exon (118 lines in 16 decisions)
- intron: print 124, comment 42, import 10, config 4
- prose: 278 lines, 74 claims (31 action, 43 result)
- links: 36 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 1
- result_claims_deferred: 43

## Silent decisions — executed, never disclosed

- **83-85, 227** [high] code dark-skinned players as 1 and light-skinned as 0, making light the reference category

## Misaligned — code and prose disagree

- code: bucket continuous skin tone into light/medium/dark categories using fixed cutoffs (<=0.25 light, >=0.75 dark, else medium)
  - prose: defines Medium as an average rating between 0.375 and 0.625
  - why: code defines medium as everything not light/dark (0.25<x<0.75); claim defines medium as 0.375 to 0.625

## All decisions

- `33-35` [high] **linked x1** — load the raw player-referee dyad dataset from a fixed CSV path with no filtering at read time
- `38-40` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `41-56` [high] **linked x3** — bucket continuous skin tone into light/medium/dark categories using fixed cutoffs (<=0.25 light, >=0.75 dark, else medium)
- `57-59` [high] **linked x1** — collapse the red-card count into a binary indicator for whether any red card occurred in the dyad
- `77-79` [high] **linked x1** — drop rows lacking a skin-tone rating before any further analysis
- `80-82` [high] **linked x2** — narrow the primary comparison to only light- and dark-toned players, dropping medium-toned players
- `83-85, 227` [high] **SILENT** — code dark-skinned players as 1 and light-skinned as 0, making light the reference category
- `90-106, 232` [high] **linked x1** — collapse detailed playing positions into five broader groups (Defender/Midfielder/Forward/Goalkeeper/Other)
- `107-109, 229-231` [high] **linked x1** — drop dyads with missing position data (complete-case restriction)
- `146-149, 233-234` [high] **linked x1** — standardize games and yellow-card counts to z-scores before using them as covariates
- `150-152, 235-236` [high] **linked x5** — choose the regression's adjustment set — position group, league country, standardized games and yellow cards — alongside the treatment indicator
- `156-162, 237-242` [high] **linked x3** — fit a logistic regression for anyRedCard with standard errors clustered by player instead of assuming independent observations
- `174-184, 247-250` [high] **linked x5** — summarize the treatment effect on the risk-difference scale via average marginal effects (dy/dx at overall means) rather than only reporting log-odds
- `199-209` [high] **linked x3** — additionally report the effect as an odds ratio by exponentiating the logistic coefficient and its confidence interval
- `224-226, 228` [high] **linked x3** — run a sensitivity model that keeps medium-toned players as their own dummy category instead of excluding them
- `289-293` [high] **linked x5** — declare the finding 'not supported' because the 95% CI crosses zero and the p-value exceeds a 0.05 significance threshold
