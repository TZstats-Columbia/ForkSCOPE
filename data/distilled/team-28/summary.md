# team-28  (human)

- code: 75 lines, 65% exon (49 lines in 16 decisions)
- intron: glue 18, comment 3, print 3, import 2
- prose: 269 lines, 73 claims (34 action, 39 result)
- links: 29 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 13
- C_only_silent_decision: 3
- R_only_unbacked_action_claim: 18
- R_only_consistent_negative: 2
- result_claims_deferred: 39

## Silent decisions — executed, never disclosed

- **20** [high] define the non-red-card game count as games minus redCards, to use as the binomial 'failure' count
- **50, 62, 74** [medium] exponentiate fixed-effect estimates to report them as odds ratios instead of log-odds
- **54-59** [high] fit a binomial mixed model testing the interaction between standardized skintone and standardized playing experience, with an enlarged optimizer iteration limit to reach convergence

## All decisions

- `2` [high] **linked x1** — load the referee/player match dataset from CSV as the analysis sample
- `4-5` [high] **linked x1** — average the two raters' skin-tone ratings into a single continuous skintone score
- `8-12` [high] **linked x1** — collapse the detailed playing-position labels into three broader groups (Back/Front/Middle) and store as a factor
- `14` [high] **linked x1** — drop players lacking a photo/skintone rating from the sample
- `15` [high] **linked x1** — drop rows lacking referee implicit-bias (IAT) scores from the sample
- `16` [high] **linked x1** — drop players lacking position information from the sample
- `17-18` [high] **linked x1** — exclude referees who encountered only one player, based on a computed frequency table of appearances
- `20` [high] **SILENT** — define the non-red-card game count as games minus redCards, to use as the binomial 'failure' count
- `24-26` [medium] **linked x2** — build a player-level table and chi-square test whether skintone is associated with position or league, to check confounding before choosing covariates
- `31-35` [high] **linked x13** — fit a binomial mixed-effects logistic model of red-card counts on skintone, position, and league, with crossed random intercepts for referee and player
- `37-41` [high] **linked x1** — fit an alternative Poisson mixed-effects model of red-card counts with an offset for games played, instead of the binomial specification
- `44-47` [high] **linked x2** — compare the Poisson and binomial models via an AIC table to judge which model family fits better
- `50, 62, 74` [medium] **SILENT** — exponentiate fixed-effect estimates to report them as odds ratios instead of log-odds
- `51, 63, 75` [medium] **linked x1** — compute confidence intervals for the exponentiated coefficients using the Wald approximation rather than profile or bootstrap methods
- `54-59` [high] **SILENT** — fit a binomial mixed model testing the interaction between standardized skintone and standardized playing experience, with an enlarged optimizer iteration limit to reach convergence
- `66-71` [high] **linked x3** — fit a binomial mixed model testing the interaction between standardized skintone and standardized referee-country implicit bias (IAT), with an enlarged optimizer iteration limit to reach convergence
