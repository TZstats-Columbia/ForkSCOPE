# 2025-11-27T03-25-45+0000  (ai)

- code: 169 lines, 55% exon (93 lines in 13 decisions)
- intron: print 58, comment 11, import 4, config 3
- prose: 183 lines, 101 claims (44 action, 57 result)
- links: 43 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 12
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 10
- result_claims_deferred: 57

## Silent decisions — executed, never disclosed

- **24-40** [high] collapse granular playing positions into four broad role categories via a manual mapping

## All decisions

- `12-14` [medium] **linked x2** — load the raw referee-player dyad dataset from a fixed CSV path, fixing the data source and scope for the whole analysis
- `15-17` [high] **linked x1** — average the two raters' skin-tone scores into one continuous skin-tone measure
- `18-20, 153-158` [high] **linked x2** — binarize continuous skin tone into a dark/light indicator using a 0.25 cutoff as the primary choice, then re-test with a 0.50 cutoff as a robustness check
- `21-23` [high] **linked x2** — collapse red card counts into a binary any-red-card outcome
- `24-40` [high] **SILENT** — collapse granular playing positions into four broad role categories via a manual mapping
- `48-50, 53` [high] **linked x3** — drop dyads with missing skin-tone rating or missing broad position from the analysis sample
- `51, 132-141` [high] **linked x1** — exclude goalkeepers from the analysis sample as the primary scope choice, later relaxed in a sensitivity check that re-includes them
- `52, 118-128` [high] **linked x1** — require at least 2 games per dyad for inclusion, later tightened to >=3 games in a sensitivity check
- `59-61` [high] **linked x13** — fit a logistic regression of any red card on the dark-skin indicator adjusting for games played, yellow cards, and broad position as the primary model specification
- `65-67, 71-77` [high] **linked x10** — choose the average marginal effect (dy/dx, evaluated overall, dummy=True) of the dark-skin indicator as the primary effect measure and extract its point estimate, CI, and p-value
- `85-91` [high] **linked x4** — derive an odds ratio as a secondary estimand by exponentiating the logit coefficient and build its 95% CI via a normal (1.96) approximation
- `145-149` [high] **linked x1** — test an alternative adjustment set that additionally controls for league country fixed effects
- `164-169` [low] **linked x3** — declare the bias hypothesis 'supported' by writing out specific percentage/CI/p-value text rather than referencing the computed rd/rd_ci/rd_p variables, framing an exploratory in-sample result as a conclusion
