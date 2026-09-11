# 2025-11-21T03-48-39+0000  (ai)

- code: 356 lines, 44% exon (156 lines in 18 decisions)
- intron: print 86, comment 62, plot 36, import 10, config 4, glue 2
- prose: 351 lines, 88 claims (32 action, 56 result)
- links: 64 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 6
- R_only_consistent_negative: 5
- result_claims_deferred: 56

## All decisions

- `34-36` [high] **linked x1** — load the raw player-referee dyad CSV as the analysis source
- `38-40` [high] **linked x1** — average the two raters' scores into one continuous skin-tone measure
- `41-43` [high] **linked x1** — drop dyads that have no skin tone rating
- `45-47` [high] **linked x2** — collapse the red card count into a binary any-red-card outcome
- `48-52, 241-245` [high] **linked x7** — restrict the sample to skin-tone extremes with a cutoff (primary 0.25/0.75, sensitivity variant 0.375/0.625) and derive the binary darkSkin group label
- `54-56, 246` [high] **linked x1** — drop dyads with unrecorded playing position
- `58-75, 247` [medium] **linked x1** — collapse free-text position strings into five categories via keyword matching
- `90-91, 93-94` [medium] **linked x1** — quantify agreement between the two skin-tone raters using Pearson and Spearman correlation
- `104-107` [high] **linked x2** — compute the crude, unadjusted red-card rate difference between dark and light skin groups
- `113-118` [low] **linked x3** — pick games played and yellow cards as the covariates to display for a balance check across skin-tone groups
- `125-127` [high] **linked x8** — specify the adjustment set for the outcome model
- `128-134, 252-257` [high] **linked x7** — fit a logistic regression for the red-card outcome with standard errors clustered by player
- `138-142, 258-260` [high] **linked x7** — re-express the darkSkin coefficient as an odds ratio with a confidence interval and p-value for reporting
- `152-167` [high] **linked x8** — standardize risks by predicting outcomes under all-dark and all-light counterfactual scenarios and differencing the averaged predicted probabilities
- `178-217` [high] **linked x5** — obtain the risk-difference confidence interval and p-value by simulating 10,000 coefficient draws from the model's asymptotic normal distribution instead of a delta-method or resampling approach
- `228-230` [medium] **linked x1** — assess model discrimination via in-sample AUC
- `270-278` [high] **linked x5** — stratify the unadjusted rate comparison by league to look for heterogeneity
- `301-305` [high] **linked x3** — declare the hypothesis 'SUPPORTED' in the printed conclusion unconditionally, without stating or applying a significance threshold
