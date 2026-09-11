# 2025-11-29T08-21-37+0000  (ai)

- code: 217 lines, 60% exon (131 lines in 21 decisions)
- intron: print 50, comment 23, import 8, config 5
- prose: 309 lines, 119 claims (68 action, 51 result)
- links: 59 (3 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 26
- R_only_consistent_negative: 13
- result_claims_deferred: 51

## Silent decisions — executed, never disclosed

- **38-41** [medium] derive player age relative to a fixed reference year (2013) from birthdate

## Misaligned — code and prose disagree

- code: refit the primary logistic model substituting alternative dark-skin cutpoints (0.375, 0.5) as a robustness check
  - prose: alternative cutpoints of 0.375, 0.5, and 0.625 were explored
  - why: claim states cutpoint 0.625 was explored; code computes only cutpoints 0.25/0.375/0.5
- code: refit the primary logistic model substituting alternative dark-skin cutpoints (0.375, 0.5) as a robustness check
  - prose: skin tone cutpoints 0.25/0.375/0.5/0.625 were explored and 0.25 was chosen as it maximizes power and is substantively defensible
  - why: claim lists 0.625 among explored cutpoints; code computes only 0.25/0.375/0.5
- code: restrict the sample to dyads with at least 2 games as a robustness check
  - prose: all-dyads, >=2 games, and >=3 games sample restrictions were explored and all dyads was chosen to maximize power
  - why: claim states a >=3 games restriction was explored; code only restricts to >=2 games

## All decisions

- `20-21` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path as the analysis scope
- `23-25` [high] **linked x1** — average the two raters' skin-tone scores into one continuous skinTone measure
- `26-28` [high] **linked x1** — drop dyads with no skin tone rating from the working frame
- `30-32` [high] **linked x4** — collapse red card counts into a binary any-red-card outcome
- `33-37` [high] **linked x4** — dichotomize continuous skin tone into dark/light indicators at three candidate cutpoints, designating 0.25 as primary
- `38-41` [medium] **SILENT** — derive player age relative to a fixed reference year (2013) from birthdate
- `42-45` [high] **linked x2** — z-score standardize height, weight, age, and the two implicit/explicit bias measures for modeling
- `46-54` [high] **linked x4** — restrict the analytic sample to complete cases on position, physical, and bias covariates
- `65-67` [high] **linked x2** — one-hot encode position and league, dropping the first level as reference
- `68-77` [high] **linked x5** — choose and assemble the covariate adjustment set (skin-tone indicator, standardized physical/behavioral/bias covariates, position and league dummies, intercept) for the regression
- `78-84` [high] **linked x3** — fit a logistic regression of any-red-card on the covariate set with standard errors clustered by referee
- `90-94` [medium] **linked x5** — pull out the dark-skin coefficient, clustered SE, two-sided p-value, and 95% CI as the reported effect
- `100-103` [high] **linked x4** — convert the log-odds coefficient and its CI into an odds ratio for reporting
- `111-116, 117-120, 121-123` [high] **linked x5** — compute an adjusted risk difference via marginal standardization: set the dark indicator to 1/0 for all dyads, predict probabilities under each counterfactual, and contrast their means
- `124-127, 128-131, 132-135` [high] **linked x3** — approximate the risk difference's uncertainty with a delta-method SE, build a Wald 95% CI, and derive a two-sided z-test p-value
- `157, 159-172` [high] **linked x4** — refit the primary logistic model substituting alternative dark-skin cutpoints (0.375, 0.5) as a robustness check
- `174-175, 177-178` [high] **linked x2** — restrict the sample to dyads with at least 2 games as a robustness check
- `179-184` [high] **linked x1** — refit the clustered logistic model on the games-restricted subsample
- `188-189` [medium] **linked x1** — label the switch to a Poisson count-outcome specification with exposure offset
- `194-195, 196-202` [high] **linked x3** — model red-card counts with a Poisson GLM using log(games) as an exposure offset and dropping games as a direct covariate, with SEs clustered by referee
- `210-217` [high] **linked x3** — frame the final conclusion as the adjusted risk difference and two-sided p-value (α=0.05) supporting the hypothesis that referees give more red cards to dark-skinned players, citing consistency across sensitivity analyses
