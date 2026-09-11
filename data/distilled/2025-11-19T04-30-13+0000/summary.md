# 2025-11-19T04-30-13+0000  (ai)

- code: 380 lines, 20% exon (76 lines in 18 decisions)
- intron: print 114, comment 82, plot 66, glue 21, import 13, other 5, config 3
- prose: 283 lines, 135 claims (37 action, 98 result)
- links: 73 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 16
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 1
- result_claims_deferred: 98

## Silent decisions — executed, never disclosed

- **110-111** [medium] summarizes the unadjusted contrast as both a risk difference and a relative risk
- **297-301** [medium] approximates confidence intervals for the plotted unadjusted rates using a normal (1.96 x SE) approximation

## Misaligned — code and prose disagree

- code: recodes missing player position as its own 'Unknown' category instead of dropping those rows
  - prose: a complete-case analysis was used for all other models, since missing data in other variables was minimal
  - why: claim states complete-case handling for other variables, but code recodes missing position into an 'Unknown' category rather than dropping those rows

## All decisions

- `35` [high] **linked x3** — reads the referee-dyads CSV in as the entire dataset the analysis will draw from
- `49` [high] **linked x1** — averages the two raters' scores into a single continuous skin-tone measure
- `58-59, 288` [high] **linked x6** — cuts continuous skin tone at 0.5 into a binary dark-vs-light exposure, preserving missingness; the same 0.5 cutoff is redrawn on the distribution plot
- `62` [high] **linked x2** — collapses any positive red-card count into a binary outcome
- `73` [high] **linked x4** — drops dyads lacking a skin-tone rating from the analysis sample
- `82` [high] **linked x2** — recodes missing player position as its own 'Unknown' category instead of dropping those rows
- `85` [high] **linked x4** — log-transforms games played to use as an exposure-time covariate
- `96-100` [medium] **linked x1** — splits the sample into light- vs dark-skin groups and computes each group's raw red-card rate
- `110-111` [medium] **SILENT** — summarizes the unadjusted contrast as both a risk difference and a relative risk
- `125-129, 161-165` [high] **linked x5** — chooses the covariate set entering both the primary and secondary regressions: skin-tone exposure plus games played, position, and league country, dummy-coded with an intercept
- `132-135` [high] **linked x15** — fits the primary effect as a linear probability model with standard errors clustered by player
- `168-172` [high] **linked x11** — fits a logistic regression as a secondary specification for the same effect, again clustering by player
- `200-213` [high] **linked x4** — redefines exposure as an extreme-groups contrast (skin tone <0.25 vs >=0.75), drops the middle players, and refits the adjusted linear probability model
- `223-234` [high] **linked x5** — re-specifies exposure as continuous skin tone in the same adjusted model and rescales the fitted slope to a per-0.25-unit effect
- `240-243` [high] **linked x7** — recomputes the primary model's standard errors clustering by referee instead of by player
- `259-261` [medium] **linked x2** — translates the adjusted risk difference into a relative-increase percentage and a number-needed-to-expose
- `269-271` [medium] **linked x1** — computes Cohen's h as an additional standardized effect-size metric
- `297-301` [medium] **SILENT** — approximates confidence intervals for the plotted unadjusted rates using a normal (1.96 x SE) approximation
