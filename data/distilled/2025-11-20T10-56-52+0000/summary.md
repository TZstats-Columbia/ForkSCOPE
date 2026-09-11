# 2025-11-20T10-56-52+0000  (ai)

- code: 304 lines, 33% exon (101 lines in 19 decisions)
- intron: comment 100, print 81, import 10, config 4, other 4, glue 4
- prose: 228 lines, 102 claims (51 action, 51 result)
- links: 51 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 6
- result_claims_deferred: 51

## Silent decisions — executed, never disclosed

- **115** [high] drop remaining rows missing the standardized implicit-bias measure
- **230, 238-241, 243-247, 250-251** [high] relax the exposure floor to >=2 games and refit the no-IAT model on this looser sample
- **254, 262-265, 267-271, 274-275** [high] drop the games-played exclusion entirely and refit the no-IAT model on the full non-goalkeeper sample

## All decisions

- `35` [high] **linked x2** — load the raw player-referee dyad dataset from a fixed CSV path as the entire analytic universe
- `48` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `51-55` [medium] **linked x1** — compute Pearson and Spearman inter-rater agreement on pairwise-complete ratings and report it
- `58` [high] **linked x1** — collapse the red-card count into a binary any-red-card outcome
- `67` [high] **linked x1** — drop dyads with no skin-tone rating available
- `74-76` [high] **linked x5** — keep only the extreme skin-tone bands (<=0.25 or >=0.75), discarding the middle range, and dichotomize into a darkSkin exposure indicator
- `82` [high] **linked x1** — exclude goalkeepers from the sample
- `86` [high] **linked x2** — restrict to dyads with at least 3 games together as the exposure floor
- `97-99, 102-103, 231-235, 255-259` [high] **linked x2** — one-hot encode position and league into dummy columns with the first category dropped as reference
- `106, 236, 260` [high] **linked x2** — log-transform games played to use as an exposure adjustment
- `109-112` [high] **linked x2** — z-score standardize referees' mean implicit-association-test score
- `115` [high] **SILENT** — drop remaining rows missing the standardized implicit-bias measure
- `156-157, 160-161` [high] **linked x3** — choose the covariate set (position dummies, league dummies, log games, IAT) and assemble the primary regression formula
- `164-166, 169-173` [high] **linked x11** — fit an OLS linear probability model with referee-clustered standard errors and derive a normal-approximation 95% CI and p-value for the darkSkin effect
- `190-193, 196-197, 200-203` [high] **linked x7** — refit the same covariate set as a logistic regression and exponentiate the darkSkin coefficient and its Wald CI into an odds ratio
- `218-224, 226-227` [high] **linked x2** — refit the primary model with the implicit-bias covariate removed to test sensitivity of the estimate
- `230, 238-241, 243-247, 250-251` [high] **SILENT** — relax the exposure floor to >=2 games and refit the no-IAT model on this looser sample
- `254, 262-265, 267-271, 274-275` [high] **SILENT** — drop the games-played exclusion entirely and refit the no-IAT model on the full non-goalkeeper sample
- `291-299` [high] **linked x8** — declare the hypothesis 'SUPPORTED' by interpreting the sign, significance, and cross-specification consistency of the estimates
