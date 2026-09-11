# team-17  (human)

- code: 38 lines, 53% exon (20 lines in 9 decisions)
- intron: glue 16, comment 2
- prose: 303 lines, 81 claims (45 action, 36 result)
- links: 29 (6 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 9
- C_only_silent_decision: 0
- R_only_unbacked_action_claim: 23
- R_only_consistent_negative: 10
- result_claims_deferred: 36

## Misaligned — code and prose disagree

- code: model the count of cards given out as a binomial draw out of games played, linked to the predictor via a probit function
  - prose: for each player-referee dyad the logit of red-card probability was modeled as cards[i] ~ dbin(p[i],games[i]), logit(p[i]) as a function of seven predictors
  - why: claim states logit(p[i]); code links the binomial mean via a probit function
- code: model the count of cards given out as a binomial draw out of games played, linked to the predictor via a probit function
  - prose: the initial analysis used a probit regression, but the final analysis switched to logistic regression so the effect could be reported as an odds ratio
  - why: claim says the final analysis switched to logistic regression; the code uses a probit link and contains no logit switch
- code: model the count of cards given out as a binomial draw out of games played, linked to the predictor via a probit function
  - prose: the link function was changed from probit (initial approach) to logit (final approach) in order to summarize the effect as an odds ratio
  - why: claim says the link was changed from probit to logit; the code uses a probit link
- code: model the count of cards given out as a binomial draw out of games played, linked to the predictor via a probit function
  - prose: the study used Bayesian logistic regression to model a player's red-card record as a function of seven predictors, addressing the skin-tone-bias question
  - why: claim calls the model logistic regression; the code uses a probit link
- code: treat each player's rating as a latent categorical class drawn from probabilities theta, with each category probability given an independent Uniform(0,1) prior rather than a joint simplex prior
  - prose: the two raters' skin tone scores were z-transformed and then averaged into a single predictor
  - why: claim says the two raters' scores were z-transformed and averaged into a single predictor; the code treats the rating as a latent categorical class drawn from theta with per-category Uniform(0,1) priors, not an average
- code: treat each player's rating as a latent categorical class drawn from probabilities theta, with each category probability given an independent Uniform(0,1) prior rather than a joint simplex prior
  - prose: the logistic regression modeled red-card probability as a function of seven predictors: player aggression, referee strictness, IAT score, explicit bias score, player skin tone (average of two raters' z-scores), IAT×skin-tone interaction, and explicit-bias×skin-tone interaction
  - why: claim describes skin tone as the average of two raters' z-scores; the code models the rating as a latent categorical class with per-category Uniform priors rather than an average

## All decisions

- `4, 5` [high] **linked x4** — model the count of cards given out as a binomial draw out of games played, linked to the predictor via a probit function
- `6, 20, 36` [high] **linked x3** — give each referee an additive random intercept centered at zero (not estimated) with an estimated precision, so referees are treated as unbiased on average unlike players
- `7, 29` [high] **linked x4** — add a main-effect slope for referee IAT score with a N(0,1) prior on its coefficient
- `8, 30` [high] **linked x4** — add a main-effect slope for referee explicit bias score with a N(0,1) prior on its coefficient
- `9, 31` [high] **linked x3** — add a main-effect slope for the player's skin-tone rating value with a N(0,1) prior on its coefficient
- `10, 32` [high] **linked x3** — add an interaction term between skin-tone rating and IAT score with a N(0,1) prior on its coefficient
- `11, 33` [high] **linked x3** — add an interaction term between skin-tone rating and explicit bias score with a N(0,1) prior on its coefficient
- `15, 28, 35` [high] **linked x3** — give each player an additive random intercept drawn from a normal distribution whose mean (mu0) and precision (precPlayer) are themselves estimated with weakly informative hyperpriors
- `16, 24` [high] **linked x2** — treat each player's rating as a latent categorical class drawn from probabilities theta, with each category probability given an independent Uniform(0,1) prior rather than a joint simplex prior
