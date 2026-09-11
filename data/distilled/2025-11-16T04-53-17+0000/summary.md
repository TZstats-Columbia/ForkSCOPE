# 2025-11-16T04-53-17+0000  (ai)

- code: 253 lines, 55% exon (138 lines in 18 decisions)
- intron: print 98, import 9, comment 6, config 2
- prose: 201 lines, 122 claims (50 action, 72 result)
- links: 61 (1 misaligned)

## Presence (code / prose basis)

- CR_executed_and_disclosed: 17
- C_only_silent_decision: 1
- R_only_unbacked_action_claim: 7
- R_only_consistent_negative: 14
- result_claims_deferred: 72

## Silent decisions — executed, never disclosed

- **18-19** [high] load the raw soccer referee-player dyad dataset from a fixed path

## Misaligned — code and prose disagree

- code: fit the primary logistic regression of any-red-card on dark skin, log games, position group, and league, with standard errors clustered by player
  - prose: no survey weights or fixed effects were used
  - why: claim states no fixed effects were used, but the primary model includes leagueCountry as categorical fixed effects (decision 37 itself calls it the 'league fixed effect')

## All decisions

- `18-19` [high] **SILENT** — load the raw soccer referee-player dyad dataset from a fixed path
- `25-26` [high] **linked x1** — average the two raters' skin-tone scores into a single continuous skinTone measure
- `27-29` [high] **linked x1** — collapse red card counts into a binary any-red-card outcome
- `30-32` [high] **linked x7** — binarize skin tone at the 0.5 midpoint into a dark/light skin exposure group
- `38-42` [medium] **linked x2** — restrict to dyads with both raters present and quantify rater agreement with Pearson and Spearman correlations
- `47-48` [high] **linked x1** — drop dyads that lack a skin tone score before modeling
- `49-52` [high] **linked x5** — further drop dyads missing position, height, or weight to form the complete-case modeling sample
- `53-54` [high] **linked x2** — log-transform the games-played count for use as a model covariate
- `55-71` [high] **linked x2** — collapse the detailed position labels into four coarse position groups (Goalkeeper/Defender/Midfielder/Forward)
- `81-85` [high] **linked x7** — fit the primary logistic regression of any-red-card on dark skin, log games, position group, and league, with standard errors clustered by player
- `89-94, 158-162` [high] **linked x8** — derive the secondary odds-ratio estimand and its Wald p-value/CI from the primary model's dark-skin coefficient and SE using a normal approximation
- `100-108` [high] **linked x6** — compute the adjusted risk difference via marginal standardization/g-computation: predict outcomes under counterfactual all-dark vs all-light exposure and average the difference
- `112-120, 122-148` [high] **linked x7** — estimate uncertainty for the adjusted risk difference by refitting the model on 1000 player-clustered bootstrap resamples and taking the empirical percentile CI and a normal-approximation p-value
- `187-193` [high] **linked x1** — run a sensitivity model using continuous skin tone in place of the binary dark-skin indicator
- `198-204` [high] **linked x1** — run a sensitivity model adding height and weight to the covariate/adjustment set
- `209-216` [high] **linked x1** — run a sensitivity analysis restricting to dyads with at least 5 games together
- `221, 223-230` [high] **linked x5** — run a sensitivity analysis stratifying the model separately by league country, dropping the league fixed effect from each stratum's formula
- `237-242` [high] **linked x4** — declare the hypothesis supported or not based on a p<0.05 and CI-excludes-zero threshold rule
