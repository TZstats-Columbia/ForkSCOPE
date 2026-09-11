# 2025-11-27T04-07-54+0000  (ai)

- code: 301 lines, 34% exon (102 lines in 13 decisions)
- intron: print 126, comment 45, glue 17, import 6, config 5
- prose: 329 lines, 110 claims (71 action, 39 result)
- links: 52 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 21
- R_only_consistent_negative: 15
- result_claims_deferred: 39

## Misaligned — code and prose disagree

- code: compute the adjusted risk difference via predictive margins (predict at darkSkin=1 vs 0 and average the gap), with a delta-method SE and normal-approximation CI/p-value
  - prose: computes the average marginal effect approximately as the darkSkin coefficient times p̄(1-p̄), where p̄ is the mean predicted probability
  - why: decision computes the risk difference via predictive margins (predict at darkSkin=1 vs 0 and average the gap), while the claim describes it as the coefficient times p̄(1−p̄) approximation, a different estimator

## All decisions

- `33-34` [medium] **linked x1** — choose the raw player-referee dyad file as the data source and analysis scope
- `45-47` [high] **linked x2** — drop dyads where either rater's skin-tone score is missing
- `52-53` [high] **linked x1** — average the two independent raters into a single continuous skin-tone measure
- `56-59, 77-78` [high] **linked x7** — remove goalkeeper dyads from the analytic sample
- `60-76` [high] **linked x1** — bucket free-text position strings into Defender/Midfielder/Forward/Goalkeeper/Unknown via keyword matching
- `90-91` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `95-98` [high] **linked x8** — dichotomize the continuous skin-tone score into light/dark groups at a 0.25 cutoff chosen to maximize the effect
- `103-104` [high] **linked x2** — log-transform the games-played exposure variable
- `107-114` [high] **linked x3** — encode position and league as reference-category dummy covariates
- `163-164, 167-171` [high] **linked x7** — fit a binomial GLM of any-red-card on skin tone plus position/league/exposure covariates with HC1 robust standard errors
- `176-181, 238-241` [high] **linked x6** — turn the dark-skin coefficient into a two-sided Wald test and an exponentiated odds ratio with a normal-approximation CI
- `190-216` [high] **linked x7** — compute the adjusted risk difference via predictive margins (predict at darkSkin=1 vs 0 and average the gap), with a delta-method SE and normal-approximation CI/p-value
- `262-273` [high] **linked x5** — declare the hypothesis SUPPORTED only if the risk-difference p-value is below 0.05 and the effect is in the hypothesized positive direction, and report accordingly
