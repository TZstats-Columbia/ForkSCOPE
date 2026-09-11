# team-09  (human)

- code: 5 lines, 80% exon (4 lines in 4 decisions)
- intron: comment 4
- prose: 249 lines, 63 claims (34 action, 29 result)
- links: 6 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 2
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 24
- R_only_consistent_negative: 5
- result_claims_deferred: 29

## Silent decisions — executed, never disclosed

- **5** [medium] select which prepared data subset to fit the model on
- **5** [low] pick a specific numerical optimizer for model convergence rather than the package default

## All decisions

- `5` [high] **linked x2** — fit a mixed-effects logistic regression (glmer, binomial link) rather than a non-mixed or different-link model
- `5` [high] **linked x4** — choose the fixed-effect covariate set and random-intercept structure (position, leagueCountry, skintone as fixed effects; player and referee as random intercepts)
- `5` [medium] **SILENT** — select which prepared data subset to fit the model on
- `5` [low] **SILENT** — pick a specific numerical optimizer for model convergence rather than the package default
