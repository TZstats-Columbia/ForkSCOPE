# 2025-11-29T16-49-58+0000  (ai)

- code: 406 lines, 45% exon (182 lines in 22 decisions)
- intron: print 101, plot 59, comment 45, import 9, config 5, glue 5
- prose: 277 lines, 100 claims (60 action, 40 result)
- links: 65 (4 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 23
- R_only_consistent_negative: 5
- result_claims_deferred: 40

## Silent decisions — executed, never disclosed

- **38-39** [high] choose the input dataset and its file path as the analysis source
- **70-73** [high] derive player age from birthday using a fixed 2012 reference season

## Misaligned — code and prose disagree

- code: standardize height, weight, and age to z-scores before modeling
  - prose: continuous covariates (number of games, number of yellow cards, player height, weight, age) were included in the model, standardized
  - why: claim states games and yellow cards were standardized; code standardizes only height, weight, and age, leaving games and yellowCards on their raw scale in the model
- code: bootstrap the risk difference with 500 resamples-with-replacement, refitting the primary model each iteration and silently discarding non-converging fits
  - prose: bootstrap convergence was achieved in 500 of 500 iterations
  - why: claim reports 500 of 500 iterations converged, but the code silently discards non-converging fits, so retained iterations may be fewer than 500 and full convergence is not guaranteed
- code: re-run the primary model at alternative skin-tone cutpoints (0.30, 0.35, 0.375) as a robustness check
  - prose: seven skin tone cutpoints were tested: 0.25, 0.30, 0.35, 0.375, 0.40, 0.45, 0.50
  - why: claim states seven cutpoints (incl. 0.40, 0.45, 0.50) were tested; code only re-runs at 0.25, 0.30, 0.35, and 0.375
- code: drop yellowCards from the adjustment set and rerun the model as a robustness check
  - prose: multiple covariate set combinations were tested (with/without yellow cards, with/without physical characteristics, with/without league/position)
  - why: claim states with/without physical characteristics and with/without league/position were also tested; code only drops yellowCards as a covariate-set variation

## All decisions

- `38-39` [high] **SILENT** — choose the input dataset and its file path as the analysis source
- `42-44` [high] **linked x3** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `45-47` [high] **linked x3** — collapse the red-card count into a binary any-red-card outcome
- `48-49` [high] **linked x2** — drop dyads lacking skin-tone ratings from the analytic sample
- `52-59` [high] **linked x6** — further exclude dyads missing IAT bias score or height from the analytic sample
- `70-73` [high] **SILENT** — derive player age from birthday using a fixed 2012 reference season
- `74-76` [high] **linked x1** — impute missing position with an explicit 'Unknown' category rather than dropping rows
- `77-81` [high] **linked x1** — impute missing weight using the median weight within each position group
- `82-87` [high] **linked x3** — standardize height, weight, and age to z-scores before modeling
- `96-100, 290-291` [high] **linked x5** — binarize skin tone at a 0.25 cutpoint to define the dark/light exposure group, and mark this cutpoint on the results plot
- `114-127` [high] **linked x6** — specify and fit the primary logistic regression model, choosing outcome, predictor, adjustment covariates, and fitting settings
- `128-134` [medium] **linked x4** — extract the darkSkin coefficient's SE, z-statistic, two-sided p-value, and Wald confidence interval from the fitted model's default output
- `135-139` [medium] **linked x6** — exponentiate the log-odds coefficient and its interval to report an odds ratio
- `150-154` [high] **linked x6** — compute the adjusted risk difference via marginal standardization, averaging predicted probabilities under darkSkin=1 vs darkSkin=0
- `165-187, 190-192` [high] **linked x5** — bootstrap the risk difference with 500 resamples-with-replacement, refitting the primary model each iteration and silently discarding non-converging fits
- `193-198` [medium] **linked x2** — summarize the bootstrap distribution with mean, SD, and a 2.5/97.5 percentile interval
- `212-229` [high] **linked x2** — re-run the primary model at alternative skin-tone cutpoints (0.30, 0.35, 0.375) as a robustness check
- `230-244` [high] **linked x3** — re-specify skin tone as a continuous predictor instead of binarized, rerun the model
- `245-259` [high] **linked x2** — drop yellowCards from the adjustment set and rerun the model as a robustness check
- `260-271` [high] **linked x2** — exclude dyads with only a single game and rerun the primary model on the remaining subset
- `328-342` [medium] **linked x1** — bin number of games into categories and compute the darkSkin effect within each bin for a subgroup exploration
- `387` [high] **linked x2** — declare the hypothesis supported using a joint rule of two-sided p<0.05 and a bootstrap CI lower bound above zero
