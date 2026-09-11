# team-12  (human)

- code: 11 lines, 18% exon (2 lines in 2 decisions)
- intron: glue 5, print 2, comment 1, import 1
- prose: 166 lines, 42 claims (22 action, 20 result)
- links: 22 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 2
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 2
- result_claims_deferred: 20

## Misaligned — code and prose disagree

- code: fit a zero-inflated count model of red cards on skin tone and a main-effects covariate set (no interactions)
  - prose: a mixed-effects model was used to test whether darker player skin tone had a systematic impact on likelihood of penalization
  - why: claim says a mixed-effects model was used to test skin tone on penalization; the code fits a zero-inflated count model, a different estimator

## All decisions

- `5` [high] **linked x14** — fit a zero-inflated count model of red cards on skin tone and a main-effects covariate set (no interactions)
- `8` [high] **linked x8** — refit the zero-inflated model replacing darkSkin's main effect with its interactions against meanIAT and meanExp
