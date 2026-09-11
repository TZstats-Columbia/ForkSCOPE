# 2025-11-22T18-52-50+0000  (ai)

- code: 287 lines, 29% exon (84 lines in 16 decisions)
- intron: print 107, comment 61, glue 20, import 11, config 4
- prose: 217 lines, 104 claims (28 action, 76 result)
- links: 39 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 4
- result_claims_deferred: 76

## All decisions

- `33` [medium] **linked x2** — pull the entire raw dyad-level dataset from a fixed local file path with no scope restriction at load time
- `37` [high] **linked x1** — collapse two independent raters' skin-tone codings into a single score by simple averaging
- `40` [high] **linked x1** — drop every dyad lacking a skin-tone score before any modeling happens
- `44-48` [high] **linked x2** — throw away the middle of the skin-tone distribution and keep only the two tails, then label the dark tail as the exposed group
- `52, 152, 169` [high] **linked x1** — require a non-missing playing position before a dyad counts toward any of the three analyses that use it, rather than imputing
- `53, 153, 170` [high] **linked x1** — collapse red-card counts into a yes/no indicator instead of modeling counts, re-derived identically for the continuous and median-split checks
- `68` [high] **linked x5** — pick position, league country and games played as the confounders to condition on for the exposure-outcome relationship
- `69-73, 155-158, 173-176, 189-192, 206-209` [high] **linked x3** — estimate every risk-difference-style specification with a linear probability model whose standard errors are clustered on the player rather than treated as independent
- `88-92, 138-142, 216, 247-253, 267-273, 277, 279` [high] **linked x5** — declare an effect 'real' by a bundle of ad hoc rules: p<0.05 on the primary estimand, p<0.05 plus OR-CI excluding 1 on the secondary estimand, p<0.05 per robustness model, and a fallback 'suggestive' label when the primary p is only <0.10 but two robustness checks clear 0.05, plus a separate CI-excludes-zero check
- `95-97` [medium] **linked x4** — additionally frame the effect as a relative percentage increase over the light-skin baseline rate, not just an absolute risk difference
- `113-120` [high] **linked x1** — re-fit the same exposure-outcome relationship as a GEE logistic model with a binomial family and exchangeable within-player correlation structure instead of the linear probability model
- `129-131` [medium] **linked x3** — exponentiate the logistic coefficient and its interval to report on the odds-ratio scale rather than the log-odds scale
- `154` [high] **linked x3** — swap the dichotomized exposure for raw continuous skin tone in a sensitivity model
- `171-172` [high] **linked x3** — redefine the exposure with a single 0.25 cutoff over the full non-missing sample instead of dropping the middle range, despite calling it a 'median' split
- `187-188` [high] **linked x2** — restrict to dyads with a measured implicit-bias score and add that score as an extra covariate in a sensitivity model
- `204-205` [high] **linked x2** — swap in yellow cards as a falsification/specificity outcome in place of red cards
