# 2025-11-29T22-45-38+0000  (ai)

- code: 369 lines, 42% exon (156 lines in 19 decisions)
- intron: print 144, comment 55, import 7, config 4, glue 3
- prose: 277 lines, 67 claims (39 action, 28 result)
- links: 58 (2 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 15
- C_only_silent_decision: 4
- R_only_unbacked_action_claim: 8
- R_only_consistent_negative: 5
- result_claims_deferred: 28

## Silent decisions — executed, never disclosed

- **57** [medium] collapse the red-card count into a yes/no indicator of ever receiving a red card
- **58** [medium] normalize yellow card counts into a per-game rate
- **112-127** [medium] collapse twelve specific playing positions down to four coarse groups
- **331** [medium] compute the raw, unadjusted difference in red-card rate between the dark and light groups without any covariate control

## Misaligned — code and prose disagree

- code: pick the covariate set (position, league, games, yellow rate, height, weight) and fit a logistic model of any-red-card on the dark-skin indicator
  - prose: covariates included were position, league country, log(games+1), yellow card rate, height (mean-imputed for 46 dyads), and weight (mean-imputed for 753 dyads)
  - why: claim lists log(games+1) as a covariate; decision 35's covariate set uses raw games (log_games created only for the Poisson model, decision 59)
- code: pick the covariate set (position, league, games, yellow rate, height, weight) and fit a logistic model of any-red-card on the dark-skin indicator
  - prose: games was log-transformed to account for a non-linear relationship with red card risk
  - why: claim states games was log-transformed for the model; the main model's covariate set (decision 35) enters raw games, with log transform appearing only in the Poisson offset (decision 59)

## All decisions

- `34-35` [medium] **linked x1** — read the raw player-referee dyad dataset from a fixed CSV path
- `38-39` [high] **linked x2** — average two independent raters' scores into a single continuous skin-tone measure
- `50, 53` [high] **linked x5** — drop dyads that have no skin-tone rating at all
- `57` [medium] **SILENT** — collapse the red-card count into a yes/no indicator of ever receiving a red card
- `58` [medium] **SILENT** — normalize yellow card counts into a per-game rate
- `59-60, 63` [high] **linked x4** — throw out dyads whose yellow-card rate exceeds 1 per game as presumed data errors
- `75-95, 97-99` [high] **linked x6** — sweep six candidate skin-tone cutoffs, test each for a red-card gap, and lock in 0.25 because it gave the strongest (lowest p-value) split
- `112-127` [medium] **SILENT** — collapse twelve specific playing positions down to four coarse groups
- `131, 135-136` [high] **linked x3** — fill missing height and weight with the sample mean
- `146-148, 151` [high] **linked x8** — pick the covariate set (position, league, games, yellow rate, height, weight) and fit a logistic model of any-red-card on the dark-skin indicator
- `156, 158-170` [high] **linked x7** — predict red-card probability for every player under forced-dark and forced-light counterfactuals and difference the averaged predictions
- `176, 178-210` [high] **linked x8** — resample model coefficients from their asymptotic covariance 5,000 times to build a parametric-bootstrap interval and p-value around the risk difference
- `224-226` [high] **linked x4** — exponentiate the dark-skin coefficient and its Wald interval to report an odds ratio
- `239, 241-251` [high] **linked x1** — redo the dichotomization and model at an alternate 0.375 cutoff instead of 0.25
- `256, 258-268` [high] **linked x2** — swap the dichotomized indicator for raw continuous skin tone and compare predictions at the 0/1 extremes
- `273, 275-284` [high] **linked x1** — add referee-country implicit-bias score as an extra covariate in the model
- `289, 291-299` [high] **linked x2** — switch outcome to raw red-card counts with a log(games) offset and a Poisson family instead of logistic
- `331` [medium] **SILENT** — compute the raw, unadjusted difference in red-card rate between the dark and light groups without any covariate control
- `359` [high] **linked x4** — declare the hypothesis 'SUPPORTED' as the headline takeaway
