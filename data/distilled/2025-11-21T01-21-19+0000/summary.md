# 2025-11-21T01-21-19+0000  (ai)

- code: 408 lines, 25% exon (100 lines in 18 decisions)
- intron: print 156, plot 70, comment 54, glue 15, import 10, config 3
- prose: 230 lines, 113 claims (57 action, 56 result)
- links: 80 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 10
- result_claims_deferred: 56

## Silent decisions — executed, never disclosed

- **108-112** [high] compute the unadjusted (crude) risk difference in red-card rate between dark- and light-skinned players
- **307-311** [low] compute descriptive red-card rates per skin-tone category with normal-approximation 95% confidence intervals for the chart's error bars

## Misaligned — code and prose disagree

- code: binarize the outcome as any red card (redCards>0) received within a dyad
  - prose: the outcome definition includes both direct red cards and second yellows (yellowReds)
  - why: claim says the outcome includes second yellows (yellowReds); code binarizes only on redCards>0, which excludes the yellowReds column

## All decisions

- `32-34` [high] **linked x6** — load the raw player-referee dyad dataset from CSV as the analysis input
- `41-43` [high] **linked x1** — average rater1 and rater2 into a single continuous skinTone score
- `44-47` [medium] **linked x1** — assess inter-rater agreement by Pearson-correlating rater1 and rater2 on complete-pair cases
- `49-51` [high] **linked x2** — binarize the outcome as any red card (redCards>0) received within a dyad
- `52-65, 334-335` [high] **linked x2** — categorize continuous skinTone into Light/Medium/Dark using cutoffs at 0.125 and 0.625, cutoffs later re-marked on the ratings histogram
- `70-72` [high] **linked x2** — drop dyads with a missing skinTone value before analysis
- `74-78` [high] **linked x5** — restrict to complete cases across the outcome and all adjustment covariates
- `81-84` [high] **linked x7** — drop the Medium skin-tone category and code a binary darkSkin exposure contrasting Dark vs Light
- `108-112` [high] **SILENT** — compute the unadjusted (crude) risk difference in red-card rate between dark- and light-skinned players
- `123-126` [high] **linked x13** — choose the adjustment covariate set (games, position, leagueCountry, height, weight, meanIAT, meanExp) for the primary model
- `127-129` [high] **linked x9** — fit a logistic-regression model with conventional (non-clustered) standard errors as the base model
- `156-159, 192-195` [high] **linked x2** — report effects as average marginal effects on the risk-difference scale rather than only log-odds, computed for both the standard and clustered models
- `174-180` [high] **linked x16** — refit the model with standard errors clustered by player and designate this the primary inference
- `206-210` [high] **linked x5** — convert the clustered log-odds coefficient into an odds ratio as a secondary estimand
- `226-233` [high] **linked x3** — run a sensitivity analysis using the continuous skinTone score as exposure instead of the binary Dark/Light contrast
- `239-247` [high] **linked x2** — run a sensitivity analysis clustering standard errors by referee instead of by player
- `307-311` [low] **SILENT** — compute descriptive red-card rates per skin-tone category with normal-approximation 95% confidence intervals for the chart's error bars
- `390-394` [high] **linked x4** — classify the hypothesis as supported or not based on whether the clustered p-value is below 0.05
