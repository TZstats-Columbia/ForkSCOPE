# 2025-11-22T12-56-26+0000  (ai)

- code: 391 lines, 46% exon (181 lines in 20 decisions)
- intron: print 117, comment 56, plot 22, import 11, config 4
- prose: 262 lines, 108 claims (36 action, 72 result)
- links: 82 (0 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 18
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 1
- R_only_consistent_negative: 8
- result_claims_deferred: 72

## Silent decisions — executed, never disclosed

- **123-125** [high] specify the primary model's functional form as additive main effects of dark_skin, position, league and standardized controls with no interaction terms
- **334-339** [medium] populate the forest plot with manually typed odds-ratio and CI values per league (rather than the values just computed in the per-league loop above) and color-code leagues whose CI lower bound exceeds 1

## All decisions

- `28-29` [high] **linked x5** — load the raw soccer referee-player dataset from a fixed path as the entire analysis universe
- `36-38` [high] **linked x1** — average the two independent raters' skin-tone scores into a single continuous skin_tone_avg score per player
- `46-52` [high] **linked x2** — cut the continuous skin tone average into light/medium/dark categories using a 0.5 threshold split
- `56-59` [high] **linked x6** — drop players with medium or missing skin-tone rating and recode the remaining light/dark categories into a 0/1 dark_skin indicator
- `60, 237` [high] **linked x2** — collapse the red-card count into a binary any_red_card indicator (received at least one red card) rather than analyzing counts
- `74, 76-79, 81-84` [medium] **linked x2** — compute the crude (unadjusted) red-card rate difference and relative risk between dark- and light-skin players as a baseline comparison
- `93-98` [high] **linked x9** — choose which player/referee/match covariates enter the model (position, league, games, yellow cards, goals, height, weight, meanIAT, player and referee identifiers)
- `101-102, 239` [high] **linked x5** — restrict modeling data to complete cases by dropping any row with a missing covariate
- `106-113, 240-248` [high] **linked x1** — z-score standardize the continuous covariates before entering them into the model
- `123-125` [high] **SILENT** — specify the primary model's functional form as additive main effects of dark_skin, position, league and standardized controls with no interaction terms
- `126-132` [high] **linked x4** — fit a logistic regression and correct standard errors for clustering by player rather than treating dyads as independent
- `136-140` [medium] **linked x5** — pull out and headline only the dark_skin coefficient, SE, p-value and CI from the fitted model, leaving other covariates' effects unreported
- `157-169` [high] **linked x7** — estimate the adjusted risk difference via marginal standardization/g-computation: predict outcomes setting everyone to dark_skin then to light-skin and difference the average predictions
- `181-209` [high] **linked x2** — derive the risk difference's SE, CI and p-value via a parametric simulation that draws model parameters from their asymptotic multivariate normal distribution rather than an analytic/delta-method formula
- `223, 225-230` [high] **linked x5** — run a sensitivity model excluding player-referee dyads with only a single game together
- `234, 236, 238, 249-251, 252-257` [high] **linked x5** — run a sensitivity model replacing the binary dark_skin category with the original continuous standardized skin-tone score
- `269-271, 272-277, 278-282` [high] **linked x3** — test whether the dark_skin effect differs by league by adding a dark_skin×league interaction and comparing via a likelihood-ratio test
- `287-288, 290-291, 292-294, 295-300, 301-304, 305-314` [high] **linked x13** — refit the model separately within each of the four leagues and report per-league odds ratios and adjusted risk differences as a subgroup/heterogeneity analysis
- `334-339` [medium] **SILENT** — populate the forest plot with manually typed odds-ratio and CI values per league (rather than the values just computed in the per-league loop above) and color-code leagues whose CI lower bound exceeds 1
- `382-386` [medium] **linked x5** — frame the overall conclusion around cross-league heterogeneity (highlighting Germany's significant effect and France/Spain's null/protective effects) rather than the non-significant pooled estimate alone
