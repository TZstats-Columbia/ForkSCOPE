# team-18  (human)

- code: 280 lines, 52% exon (145 lines in 20 decisions)
- intron: comment 53, glue 36, plot 22, print 14, import 5, dead 3, config 2
- prose: 99 lines, 35 claims (25 action, 10 result)
- links: 24 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 9
- C_only_silent_decision: 11
- R_only_unbacked_action_claim: 9
- R_only_consistent_negative: 2
- result_claims_deferred: 10

## Silent decisions — executed, never disclosed

- **6** [high] load the raw crowdstorming CSV as the analysis dataset, fixed to a specific file path
- **15-16, 18** [high] collapse the now-agreeing rater1/rater2 codes into a single SkinCol variable
- **26** [medium] pull a four-digit birth year out of the birthday string by character position
- **29** [medium] narrow the working dataset down to a fixed list of columns to carry forward
- **36-44, 47** [high] collapse match-level rows into one row per player, summing cards/games/goals/results and computing a red-cards-per-match rate
- **49** [high] fill missing player heights with the sample mean height
- **52-56, 57** [high] collapse match-level rows into one row per referee, summing cards/games and computing a red-cards-per-match rate
- **60-64, 65** [high] collapse match-level rows into one row per referee country, summing cards/games and computing a red-cards-per-match rate
- **88-96** [high] choose which player-level fields feed the Q1 hierarchical model (matches, red cards, skin tone, league, group sizes)
- **104-105, 244-245** [medium] seed the MCMC intercept with the logit of the overall empirical red-card rate to speed convergence
- **177-178** [low] flag (without acting on) an alternative skin-tone coding, SkinCol3, that could have been used instead of SkinCol

## Misaligned — code and prose disagree

- code: keep only rows where both raters logged a skin-tone rating and the two ratings match exactly
  - prose: for cases where raters disagreed, the average of their skin tone ratings was used
  - why: claim states rater disagreements were resolved by averaging the two ratings; code instead drops every row where the two ratings differ

## All decisions

- `6` [high] **SILENT** — load the raw crowdstorming CSV as the analysis dataset, fixed to a specific file path
- `13` [high] **linked x2** — keep only rows where both raters logged a skin-tone rating and the two ratings match exactly
- `15-16, 18` [high] **SILENT** — collapse the now-agreeing rater1/rater2 codes into a single SkinCol variable
- `21` [high] **linked x2** — drop players whose referee-country IAT or explicit-bias scores are missing
- `26` [medium] **SILENT** — pull a four-digit birth year out of the birthday string by character position
- `29` [medium] **SILENT** — narrow the working dataset down to a fixed list of columns to carry forward
- `36-44, 47` [high] **SILENT** — collapse match-level rows into one row per player, summing cards/games/goals/results and computing a red-cards-per-match rate
- `49` [high] **SILENT** — fill missing player heights with the sample mean height
- `52-56, 57` [high] **SILENT** — collapse match-level rows into one row per referee, summing cards/games and computing a red-cards-per-match rate
- `60-64, 65` [high] **SILENT** — collapse match-level rows into one row per referee country, summing cards/games and computing a red-cards-per-match rate
- `88-96` [high] **SILENT** — choose which player-level fields feed the Q1 hierarchical model (matches, red cards, skin tone, league, group sizes)
- `104-105, 244-245` [medium] **SILENT** — seed the MCMC intercept with the logit of the overall empirical red-card rate to speed convergence
- `107-130` [high] **linked x4** — specify the Q1 logistic hierarchical model structure: binomial red cards per player with player-style and skin-tone random effects and their hyperpriors
- `134-135, 249, 251` [medium] **linked x3** — fix the MCMC run's chain count, adaptation length, iterations, thinning interval, and which parameters get monitored
- `148, 164, 275, 279` [medium] **linked x3** — summarize posterior uncertainty as a 95% equal-tailed credible interval (2.5%/97.5% quantiles)
- `163, 274, 278` [medium] **linked x3** — exponentiate the logit-scale posterior effects to report them as odds ratios, rounded to 2 decimals
- `167` [medium] **linked x4** — compute the posterior probability that the darkest skin-tone category's effect exceeds the lightest category's
- `177-178` [low] **SILENT** — flag (without acting on) an alternative skin-tone coding, SkinCol3, that could have been used instead of SkinCol
- `179-195` [high] **linked x1** — choose Q2 model inputs, including converting each country's IAT/Explicit standard errors and sample sizes into precision weights
- `196-241` [high] **linked x2** — specify the Q2 model structure linking referee-level red-card rates to referee style plus skin-tone-specific slopes on country implicit/explicit bias scores
