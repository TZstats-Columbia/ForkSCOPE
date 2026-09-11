# 2025-11-29T08-18-50+0000  (ai)

- code: 343 lines, 52% exon (180 lines in 14 decisions)
- intron: print 108, comment 42, import 8, config 5
- prose: 251 lines, 115 claims (57 action, 58 result)
- links: 83 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 14
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 14
- R_only_consistent_negative: 10
- result_claims_deferred: 58

## All decisions

- `32-33` [high] **linked x2** — pull in the raw player-referee dyad records from a fixed CSV path, setting the scope of the whole analysis
- `37-39` [high] **linked x6** — drop any dyad missing either rater's skin-tone score before analysis
- `43-46` [high] **linked x2** — collapse the two raters into a single continuous skin-tone score by averaging
- `47-49` [high] **linked x2** — collapse the red-card count into a yes/no indicator of receiving any red card in the dyad
- `63-69` [high] **linked x8** — pick 0.25 as the cutpoint that splits skin tone into dark vs light, chosen explicitly because it maximizes the unadjusted effect
- `86-104` [medium] **linked x1** — bucket free-text position strings into a handful of position categories via keyword matching, with a residual Unknown/Other bucket
- `105-108` [high] **linked x3** — log-transform games played to address right skew before entering it as a covariate
- `125-135` [high] **linked x15** — specify the primary model: logistic regression of red card on dark_skin adjusted for games, position and league, with standard errors clustered by player
- `138-189, 229-230, 260-262` [medium] **linked x13** — define the causal contrast as an average marginal-effect risk difference, with its SE from a delta-method approximation and a Wald-based CI/p-value, then apply it to each fitted model
- `204-206` [medium] **linked x6** — additionally express the primary effect as an exponentiated odds ratio with its CI, alongside the risk difference
- `220, 223-228` [high] **linked x7** — as a robustness check, drop goalkeepers entirely and refit the same adjusted model on the remaining field players
- `249-251, 254-259` [high] **linked x6** — as a second robustness check, restrict to the most extreme skin-tone contrast (score 0 vs score >=0.5), recode a new binary exposure, and refit the model on that subgroup
- `278-315` [low] **linked x7** — assemble a side-by-side comparison table of the primary and two sensitivity specifications, choosing which statistics (N, RD, CI, p, OR) to juxtapose
- `327-339` [high] **linked x5** — declare the hypothesis supported or not based on a p<0.05 threshold combined with the sign of the risk difference
