# 2025-11-22T16-29-06+0000  (ai)

- code: 341 lines, 16% exon (53 lines in 21 decisions)
- intron: print 102, comment 76, plot 73, glue 28, import 8, config 1
- prose: 225 lines, 82 claims (40 action, 42 result)
- links: 47 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 10
- R_only_consistent_negative: 8
- result_claims_deferred: 42

## Silent decisions — executed, never disclosed

- **31** [high] average the two raters' skin-tone scores into a single continuous measure
- **64** [medium] encode dark skin tone as the treatment indicator (1=dark, 0=light)
- **285-286** [medium] bin games-played into discrete ranges for the descriptive plot

## All decisions

- `22` [high] **linked x1** — load the raw referee-dyad dataset from CSV, fixing the full analysis scope
- `31` [high] **SILENT** — average the two raters' skin-tone scores into a single continuous measure
- `34` [low] **linked x2** — restrict the inter-rater reliability check to complete-case dyads with both ratings present
- `41-45` [high] **linked x1** — bin the averaged skin-tone score into light/medium/dark categories using 0.25 and 0.75 cutoffs
- `47, 151` [high] **linked x3** — collapse red card counts into a binary any-red-card outcome
- `61` [high] **linked x4** — drop the medium skin-tone group, restricting the primary comparison to light vs dark only
- `64` [medium] **SILENT** — encode dark skin tone as the treatment indicator (1=dark, 0=light)
- `67, 152` [high] **linked x1** — exclude dyads with missing player position as a required confounder
- `70, 153` [high] **linked x1** — log-transform games played before entering it as a covariate
- `98-99` [high] **linked x1** — fit an unadjusted linear probability model with standard errors clustered by player
- `107` [high] **linked x7** — choose the covariate adjustment set for the main model (position, league country, log games, yellow cards)
- `108-109` [high] **linked x9** — fit the primary adjusted linear probability model with player-clustered standard errors
- `127-129` [high] **linked x1** — refit the adjusted association as a logistic regression instead of a linear probability model
- `130-133` [medium] **linked x3** — exponentiate the logistic coefficient and its CI to report an odds ratio instead of a log-odds coefficient
- `148` [medium] **linked x1** — build an alternative analysis sample spanning the full skin-tone range instead of only light/dark, for sensitivity checks
- `149-150, 154-157` [high] **linked x2** — recode exposure via a median split on skin tone and refit the adjusted model on this alternative exposure
- `164-166` [high] **linked x3** — treat skin tone as a continuous linear predictor instead of a categorical exposure
- `173-174` [high] **linked x2** — recompute standard errors clustering by referee instead of by player
- `181-183` [high] **linked x2** — drop goalkeepers and refit the adjusted model on the remaining positions
- `197-204` [medium] **linked x3** — compute a minimum detectable effect via a normal-approximation power formula at 80% power and alpha=0.05
- `285-286` [medium] **SILENT** — bin games-played into discrete ranges for the descriptive plot
