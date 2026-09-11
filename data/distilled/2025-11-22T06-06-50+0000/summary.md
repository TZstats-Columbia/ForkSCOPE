# 2025-11-22T06-06-50+0000  (ai)

- code: 338 lines, 33% exon (113 lines in 22 decisions)
- intron: comment 108, print 106, import 9, config 2
- prose: 260 lines, 106 claims (39 action, 67 result)
- links: 51 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 4
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 3
- result_claims_deferred: 67

## Silent decisions — executed, never disclosed

- **74-77** [high] pick which columns (exposure, position, league, height, weight, player and ref IDs) travel forward into the modeling frame
- **261-262** [high] only report a threshold's sensitivity result if both groups have more than 100 dyads
- **298-301** [medium] check multicollinearity via VIF on darkSkin, log_games, height_std and weight_std, leaving the categorical position/league dummies out of the check
- **306** [low] generate in-sample predicted probabilities from the adjusted model to compare against the observed rate

## All decisions

- `32` [high] **linked x1** — load the full player-referee dyad CSV as the starting dataset with no row filtering or sampling
- `42` [high] **linked x1** — average rater1 and rater2 into a single continuous skinTone score
- `45, 47` [medium] **linked x1** — limit the reliability check to dyads with non-missing scores from both raters and quantify agreement with a Pearson correlation
- `54-56` [high] **linked x2** — cut the continuous skinTone score into light/medium/dark bands at fixed cutoffs of 0.375 and 0.625
- `62` [high] **linked x1** — reduce the red-card count to a binary any-red-card outcome
- `71` [high] **linked x3** — drop the medium-skin-tone band and keep only light vs dark dyads for the main comparison
- `74-77` [high] **SILENT** — pick which columns (exposure, position, league, height, weight, player and ref IDs) travel forward into the modeling frame
- `80, 226, 257` [high] **linked x4** — delete any row with a missing value in the modeling columns rather than imputing
- `97` [high] **linked x1** — turn the light/dark category into a 0/1 darkSkin exposure variable
- `100, 227, 263` [high] **linked x1** — log-transform games (+0.5 offset) to use as the exposure control
- `103-104, 228-229, 264-265` [high] **linked x2** — z-score height and weight before entering them as covariates
- `113-115, 122-126` [high] **linked x2** — report a crude, covariate-free comparison — raw red-card rates by group plus a bivariate logistic fit — as the unadjusted baseline
- `140-142, 156-158` [high] **linked x10** — fit the main covariate-adjusted logistic model (darkSkin plus exposure, position, league, height, weight) and pull out the adjusted odds ratio
- `172-173, 176-180` [high] **linked x7** — report the average marginal effect (a risk-difference-scale estimate) as the headline number rather than stopping at the odds ratio
- `198-203` [high] **linked x2** — add an OLS linear probability model as a functional-form robustness check on the same specification
- `210-217` [high] **linked x5** — recompute standard errors clustered by player to account for repeated dyads from the same player
- `224-225, 230-232, 236-239` [high] **linked x4** — swap the binary dark/light treatment for the raw continuous skinTone score and refit the adjusted model
- `249-256, 258-260, 266-284` [high] **linked x3** — sweep three alternative dark-skin cutoffs (0.375, 0.5, 0.625) and refit the adjusted model under each to check sensitivity to the binarization threshold
- `261-262` [high] **SILENT** — only report a threshold's sensitivity result if both groups have more than 100 dyads
- `298-301` [medium] **SILENT** — check multicollinearity via VIF on darkSkin, log_games, height_std and weight_std, leaving the categorical position/league dummies out of the check
- `306` [low] **SILENT** — generate in-sample predicted probabilities from the adjusted model to compare against the observed rate
- `330-335` [high] **linked x1** — declare the hypothesis supported only if the risk-difference p-value is below 0.05 and the CI lower bound is above zero
