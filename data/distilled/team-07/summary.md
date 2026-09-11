# team-07  (human)

- code: 18 lines, 78% exon (14 lines in 6 decisions)
- intron: import 2, glue 2
- prose: 311 lines, 57 claims (29 action, 28 result)
- links: 14 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 4
- C_only_silent_decision: 2
- R_only_unbacked_action_claim: 15
- R_only_consistent_negative: 2
- result_claims_deferred: 28

## Silent decisions — executed, never disclosed

- **1** [high] load the full crowdstorming dataset from CSV as the analysis population
- **4-5** [high] recode each rater's skin-tone score to a numeric zero-based scale

## Misaligned — code and prose disagree

- code: restrict the working sample to referee-player rows with at least one red card
  - prose: decided to include all player-referee dyads in the analysis following the feedback round
  - why: code restricts the working sample to referee-player rows with at least one red card, while the claim states the final analysis included all player-referee dyads

## All decisions

- `1` [high] **SILENT** — load the full crowdstorming dataset from CSV as the analysis population
- `3` [high] **linked x1** — drop rows where either rater's skin-tone rating is missing
- `4-5` [high] **SILENT** — recode each rater's skin-tone score to a numeric zero-based scale
- `6` [high] **linked x2** — restrict the working sample to referee-player rows with at least one red card
- `8-13` [high] **linked x6** — fit a Bayesian Dirichlet-process profile regression with a binomial outcome model of red cards over games played, treating the rater scores as discrete covariates, on the red-card subset, with fixed MCMC settings (sweeps, burn-in, seed)
- `14-16` [high] **linked x5** — derive dissimilarities between fitted profiles, cluster them into an optimal partition, then compute and plot each cluster's relative risk profile
