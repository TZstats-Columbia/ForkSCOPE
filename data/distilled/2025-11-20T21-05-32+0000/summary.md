# 2025-11-20T21-05-32+0000  (ai)

- code: 314 lines, 42% exon (132 lines in 16 decisions)
- intron: print 119, comment 44, import 11, glue 7, config 1
- prose: 236 lines, 103 claims (45 action, 58 result)
- links: 64 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 12
- R_only_consistent_negative: 2
- result_claims_deferred: 58

## All decisions

- `28-29` [high] **linked x4** — read the raw player-referee dyad csv as the analysis input, fixing the data source and starting scope
- `41-42` [high] **linked x2** — drop dyads lacking both rater1 and rater2 skin-tone scores before any tone-based analysis
- `45, 47-51` [medium] **linked x1** — quantify agreement between the two skin-tone raters via Pearson and Spearman correlation and report it as a diagnostic
- `52-54` [high] **linked x1** — average the two raters' scores into a single continuous skin_tone_avg measure
- `55-62, 87-89` [high] **linked x4** — cut the continuous skin-tone score into light/medium/dark bands at 0.25 and 0.75 cutoffs, then collapse that to a dark-vs-not binary indicator
- `63-65` [high] **linked x2** — collapse the red-card count into a binary any-red-card indicator per dyad
- `66-70` [high] **linked x4** — restrict the primary analysis sample to light vs dark, dropping medium-toned dyads as a contrast choice
- `79-81` [high] **linked x3** — drop dyads with missing player position because it is required as a covariate
- `83-86` [high] **linked x3** — fill missing height and weight with the sample median rather than dropping those rows
- `121-145, 170-175` [high] **linked x20** — fit a linear-probability (OLS) model of any_red_card on skin_dark across five nested covariate tiers with SEs clustered by player, then treat the fully-adjusted model as the primary estimate
- `203-212` [medium] **linked x2** — manually one-hot encode position and leagueCountry (dropping the first level) to build the logistic-regression design matrix
- `213-218` [high] **linked x2** — fit a binomial GLM (logistic regression) as the secondary model, again clustering SEs by player
- `226-229` [medium] **linked x3** — exponentiate the logistic coefficient and its CI to express the effect on an odds-ratio scale instead of log-odds
- `246-249` [high] **linked x2** — re-run the adjusted model treating skin tone as a continuous exposure instead of the binary dark/light split, as a robustness check
- `256-259` [high] **linked x3** — re-run the primary model clustering standard errors by referee instead of by player
- `274-307` [medium] **linked x8** — adopt a two-sided alpha=0.05 threshold with a CI-includes-zero rule to declare the red-card/skin-tone hypothesis 'not supported', and frame the covariate list as adequate adjustment
