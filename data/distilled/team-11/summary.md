# team-11  (human)

- code: 58 lines, 40% exon (23 lines in 16 decisions)
- intron: glue 30, plot 2, comment 1, config 1, print 1
- prose: 731 lines, 126 claims (71 action, 55 result)
- links: 81 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 25
- R_only_consistent_negative: 14
- result_claims_deferred: 55

## Silent decisions — executed, never disclosed

- **12** [low] set p-value thresholds for stepwise variable entry/removal, though the model actually uses forced entry so this criteria may be inert
- **24** [high] flag and plot cases whose standardized residual exceeds 3 SD as outliers
- **41, 58** [medium] request a Hosmer-Lemeshow goodness-of-fit test and 95% confidence intervals for the odds ratios in both logistic models

## All decisions

- `4, 16` [high] **linked x8** — declare an OLS multiple regression predicting total red cards received
- `8` [high] **linked x6** — exclude cases with any missing values listwise rather than pairwise or with imputation
- `10` [medium] **linked x3** — choose which coefficient, model-fit, collinearity (tolerance/VIF), and R²-change statistics get computed and reported
- `12` [low] **SILENT** — set p-value thresholds for stepwise variable entry/removal, though the model actually uses forced entry so this criteria may be inert
- `18` [high] **linked x9** — enter the player/position control variables together as the first predictor block
- `20` [high] **linked x12** — add average skin-tone rating as a second block to test its incremental effect over the controls
- `22` [medium] **linked x1** — request Durbin-Watson autocorrelation statistic plus residual histogram/normal-probability plots to check regression assumptions
- `24` [high] **SILENT** — flag and plot cases whose standardized residual exceeds 3 SD as outliers
- `27, 44` [high] **linked x14** — switch model family to binary logistic regression predicting a dichotomized red-card indicator instead of the continuous count
- `29, 46` [high] **linked x4** — enter the same covariate set, including mean skin-tone rating, as the first block in both logistic models
- `31` [high] **linked x3** — add mean implicit-association (IAT) bias score as a second block
- `33` [high] **linked x9** — add an IAT interaction term as a third block to test moderation
- `35, 37, 52, 54` [high] **linked x1** — use indicator (dummy) contrast coding instead of the default coding scheme for the categorical position variables amid and cback, consistently across both logistic models
- `41, 58` [medium] **SILENT** — request a Hosmer-Lemeshow goodness-of-fit test and 95% confidence intervals for the odds ratios in both logistic models
- `48` [high] **linked x3** — add mean explicit-bias score as a second block
- `50` [high] **linked x8** — add an explicit-bias interaction term as a third block to test moderation
