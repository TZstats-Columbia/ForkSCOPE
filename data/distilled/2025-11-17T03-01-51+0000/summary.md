# 2025-11-17T03-01-51+0000  (ai)

- code: 402 lines, 51% exon (206 lines in 22 decisions)
- intron: print 143, comment 43, import 5, config 5
- prose: 259 lines, 140 claims (67 action, 73 result)
- links: 72 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 20
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 25
- R_only_consistent_negative: 12
- result_claims_deferred: 73

## Silent decisions — executed, never disclosed

- **73-80** [high] restrict the working dataset to a fixed set of variables carried into all downstream models
- **222-225** [medium] derive a two-sided p-value via a normal-approximation z-test built from the bootstrap standard error rather than from the bootstrap distribution's own tails

## All decisions

- `29-31` [high] **linked x1** — load the raw soccer dataset from CSV as the analysis population
- `34-36` [high] **linked x1** — average the two raters' skin-tone ratings into a single continuous skin_tone score
- `37-38` [high] **linked x2** — drop rows lacking a skin-tone rating from the analysis population
- `45-61` [high] **linked x1** — collapse detailed playing positions into four broad position groups via a manual mapping
- `62-66` [high] **linked x2** — fill missing position group with each player's own modal position, defaulting to Midfielder when no mode exists
- `67-72` [high] **linked x1** — fill missing height and weight with the median within each player's position group
- `73-80` [high] **SILENT** — restrict the working dataset to a fixed set of variables carried into all downstream models
- `82` [high] **linked x1** — define the binary outcome as having received at least one red card
- `83` [high] **linked x2** — dichotomize continuous skin tone into a dark/light exposure using a 0.25 cutoff
- `84-85` [high] **linked x2** — log-transform games-played (+1) to use as a covariate
- `86-89` [high] **linked x1** — fill missing implicit- and explicit-bias scores with their sample means
- `129-134` [high] **linked x19** — specify the primary model as logistic regression of red card on dark_skin adjusted for position, league and log games
- `138-143` [high] **linked x6** — report the exposure effect on the odds-ratio scale by exponentiating the coefficient, framed as a secondary estimand
- `159-171` [high] **linked x7** — define the primary estimand as the standardized risk difference from counterfactual predictions setting everyone's exposure to light vs. dark
- `184-186, 188-210, 213-214, 216-221` [high] **linked x6** — bootstrap the risk-difference estimate over 200 resamples, refitting the adjusted model each time and silently discarding resamples where the fit fails to converge, then summarizing as an SE and a percentile 95% CI
- `222-225` [medium] **SILENT** — derive a two-sided p-value via a normal-approximation z-test built from the bootstrap standard error rather than from the bootstrap distribution's own tails
- `257-264` [high] **linked x2** — fit an alternative model treating skin tone as continuous instead of dichotomized, reporting the raw coefficient rather than an odds ratio
- `269-277` [high] **linked x2** — quantify the continuous-exposure effect as the predicted risk difference for a ±0.5 SD contrast in skin tone
- `284, 288-309` [high] **linked x8** — re-run the adjusted-model / odds-ratio / risk-difference pipeline across four alternative dark-skin cutoffs to probe sensitivity to the threshold choice
- `315, 319-340, 342` [high] **linked x4** — re-run the adjusted analysis separately within each position group, excluding subgroups smaller than 100 dyads and dropping position from the adjustment set
- `348, 352-370, 372` [high] **linked x1** — re-run the adjusted analysis separately within each of four leagues, dropping league from the adjustment set
- `383, 384, 390, 391, 394, 395` [high] **linked x3** — declare the hypothesis supported only when the odds-ratio p-value is below 0.05 and the risk difference is positive, otherwise inconclusive or contradictory
