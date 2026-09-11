# 2025-11-22T11-04-38+0000  (ai)

- code: 385 lines, 25% exon (97 lines in 25 decisions)
- intron: print 118, comment 62, glue 52, plot 35, import 10, other 7, config 4
- prose: 257 lines, 115 claims (47 action, 68 result)
- links: 67 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 5
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 7
- result_claims_deferred: 68

## Silent decisions — executed, never disclosed

- **99** [medium] recode missing position values into an explicit 'Unknown' category rather than leaving them null
- **130-131** [high] recode the light/dark exposure category into a 0/1 numeric indicator for regression
- **149, 247-248** [medium] report interval estimates at the 95% confidence level throughout
- **205-207** [high] discard a bootstrap replicate as degenerate if it has fewer than 1000 dyads or fewer than 10 red-card events
- **289, 335** [high] only report/plot a league's stratified effect if it has more than 100 dyads and more than 5 red-card events

## All decisions

- `37-38` [high] **linked x4** — load the raw referee-player dyad dataset from a fixed path, fixing the full universe of records available to the analysis
- `51-52` [high] **linked x1** — collapse the two independent skin-tone ratings into a single averaged score
- `58` [medium] **linked x3** — define rater 'agreement within one category' as a difference no greater than 0.25
- `65-71` [high] **linked x4** — bucket the continuous skin-tone score into light/medium/dark using cut points at 0.375 and 0.625
- `84-85` [high] **linked x1** — collapse red-card count into a binary any-red-card outcome
- `87-90, 95-96` [high] **linked x3** — define the exposure as a light-vs-dark binary contrast, treating medium-toned dyads as neither category and dropping them from the binary-exposure subsample
- `92-93` [high] **linked x3** — restrict the analysis sample to dyads that have any skin-tone rating at all
- `98, 100` [high] **linked x2** — exclude dyads with missing position data from the final modeling dataset, treating position as a required confounder
- `99` [medium] **SILENT** — recode missing position values into an explicit 'Unknown' category rather than leaving them null
- `130-131` [high] **SILENT** — recode the light/dark exposure category into a 0/1 numeric indicator for regression
- `132` [high] **linked x3** — log-transform games played after flooring at 1 game, as a confounder control
- `134-135` [high] **linked x6** — specify the primary model's covariate adjustment set as position, league country, and log games alongside the exposure
- `140-143` [high] **linked x11** — fit the exposure-outcome association as a binomial (logistic) GLM with standard errors clustered by player instead of treating dyads as independent
- `149, 247-248` [medium] **SILENT** — report interval estimates at the 95% confidence level throughout
- `166-181, 215-228` [high] **linked x6** — estimate the adjusted risk difference via marginal standardization: predict outcomes for the whole sample under counterfactual all-dark and all-light exposure and difference the averaged predicted probabilities, rather than reading it off the model coefficient directly
- `197-203` [high] **linked x2** — resample players (not individual dyads) with replacement, preserving within-player correlation in the bootstrap
- `205-207` [high] **SILENT** — discard a bootstrap replicate as degenerate if it has fewer than 1000 dyads or fewer than 10 red-card events
- `233` [medium] **linked x2** — set the number of bootstrap replicates to 1000
- `252` [high] **linked x1** — derive a two-sided empirical p-value from the bootstrap distribution as twice the smaller tail proportion on either side of zero
- `270-273` [high] **linked x4** — re-run the association test with skin tone treated as continuous instead of the light/dark binary, as a sensitivity check
- `278-282` [high] **linked x4** — add log(yellow cards + 1) as an extra adjustment covariate in a sensitivity model
- `287-288, 333-334` [medium] **linked x2** — limit the league-specific subgroup analysis to England, Germany, France, and Spain
- `289, 335` [high] **SILENT** — only report/plot a league's stratified effect if it has more than 100 dyads and more than 5 red-card events
- `290, 336` [high] **linked x4** — drop league country from the covariate set in within-league models since stratification already holds league fixed
- `345` [medium] **linked x1** — highlight a league's bar in a different color when its within-league p-value is below 0.05
