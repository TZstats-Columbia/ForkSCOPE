# vocab_exhibits

Weak signals used to order a review queue, never to conclude.

Corpus `ai+human.merged.forkmerged.merged.induced.r3.osplit`.

Exhibits are ordered **worst-first** — the cases closest to
breaking each claim, never a representative sample. Handles
resolve with `python3 scripts/trace.py resolve <handle>`.

| check | verdict | claim |
|---|---|---|
| V1 | **REVIEW** | options within one fork are distinct actions |
| V2 | **REVIEW** | every fork is a slot where a run picks exactly one option |
| V3 | **REVIEW** | distinct forks ask distinct questions |
| V4 | **REVIEW** | an option records one action, not several |
| V6 | **REVIEW** | an option records one use, not a primary and a refit |
| V7 | **REVIEW** | an option's label names one choice, not a list |
| V5 | **INFO** | forks where nearly every run invented its own option |

## V1 — options within one fork are distinct actions

**REVIEW** — 561 pairs to read; the metric cannot clear the rest

*Compared against:* no null -- a ranking for human attention, not a test

*Cannot see:* two descriptions of one action that share no words. The rater-averaging fork was invisible to exactly this measure

> **Entangled.** This check uses `label_similarity`, `option_lists`, which the pipeline also used to build what is being checked (candidate screen for every merge pass; what the grouping passes were shown when they decided). Its agreement is not independent evidence.

| measure | value |
|---|---|
| within_fork_pairs | 5611 |
| above | 561 |
| threshold | 0.55 |

### within-fork option pairs most likely to be one action

Showing the worst **20 of 561**.

> Lexical similarity cannot see two descriptions of one action that share no words. A short queue here is NOT evidence the fork is clean.

**1. `fork:bfb93694`**

- *similarity*: 1.0
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: games, yellowCards, height, position, league
- *option_b*: position, league, yellowCards, height (no games)
- *fork*: which covariates make up the model's adjustment set?
- *trace_a*: opt:a16e70c4
- *trace_b*: opt:5d252d11

**2. `fork:bfb93694`**

- *similarity*: 1.0
- *runs_a*: 29
- *runs_b*: 1
- *option_a*: log(games) + position + league
- *option_b*: log(games), position (no league)
- *fork*: which covariates make up the model's adjustment set?
- *trace_a*: opt:3a92bad8
- *trace_b*: opt:df150cb5

**3. `fork:bfb93694`**

- *similarity*: 1.0
- *runs_a*: 1
- *runs_b*: 2
- *option_a*: position, league, yellowCards (no games)
- *option_b*: games, yellowCards, position (no league)
- *fork*: which covariates make up the model's adjustment set?
- *trace_a*: opt:c7db2974
- *trace_b*: opt:aed071c9

**4. `fork:bfb93694`**

- *similarity*: 1.0
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: league, position, age, height, weight, yellowCards, goals (no games)
- *option_b*: games, height, weight, age, yellowCards, goals, position, league
- *fork*: which covariates make up the model's adjustment set?
- *trace_a*: opt:bb3e14b4
- *trace_b*: opt:5d0df0f6

**5. `fork:bfb93694`**

- *similarity*: 1.0
- *runs_a*: 2
- *runs_b*: 1
- *option_a*: games, position, league, yellowCards, meanIAT, meanExp, height, weight, age
- *option_b*: games, yellowCards, age, height, weight, league, meanIAT, meanExp (no position)
- *fork*: which covariates make up the model's adjustment set?
- *trace_a*: opt:bf37dbf9
- *trace_b*: opt:ee6e4478

**6. `fork:f1d58d6a`**

- *similarity*: 1.0
- *runs_a*: 5
- *runs_b*: 2
- *option_a*: games + age + position + league + height + weight
- *option_b*: no games, no age; position + league + height + weight
- *fork*: Which control variables and functional forms enter the regression model?
- *trace_a*: opt:22eef353
- *trace_b*: opt:dbd756b5

**7. `fork:f1d58d6a`**

- *similarity*: 1.0
- *runs_a*: 5
- *runs_b*: 3
- *option_a*: games + age + position + league + height + weight
- *option_b*: no games; position + league + age + height + weight
- *fork*: Which control variables and functional forms enter the regression model?
- *trace_a*: opt:22eef353
- *trace_b*: opt:e5b46add

**8. `fork:f1d58d6a`**

- *similarity*: 1.0
- *runs_a*: 2
- *runs_b*: 3
- *option_a*: no games, no age; position + league + height + weight
- *option_b*: no games; position + league + age + height + weight
- *fork*: Which control variables and functional forms enter the regression model?
- *trace_a*: opt:dbd756b5
- *trace_b*: opt:e5b46add

**9. `fork:1bfc73f3`**

- *similarity*: 0.974
- *runs_a*: 4
- *runs_b*: 1
- *option_a*: predict at a single fixed reference profile (means/modal categories), then difference
- *option_b*: predict at a single fixed reference profile (means/modal categories), then difference #2
- *fork*: When forming adjusted counterfactual predictions, are covariates averaged over the observed sample or fixed at a single reference profile?
- *trace_a*: opt:eca007f9
- *trace_b*: opt:31da5e54

**10. `fork:45323461`**

- *similarity*: 0.973
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: nonparametric bootstrap, 200 resamples
- *option_b*: nonparametric bootstrap, 2000 resamples
- *fork*: how is uncertainty in the estimates quantified?
- *trace_a*: opt:1860a0af
- *trace_b*: opt:63c96b7f

**11. `fork:1bfc73f3`**

- *similarity*: 0.973
- *runs_a*: 135
- *runs_b*: 4
- *option_a*: marginal standardization / g-computation: average counterfactual predictions over the observed sample, then difference
- *option_b*: marginal standardization / g-computation: average counterfactual predictions over the observed sample, then difference #2
- *fork*: When forming adjusted counterfactual predictions, are covariates averaged over the observed sample or fixed at a single reference profile?
- *trace_a*: opt:9aef08e2
- *trace_b*: opt:aa41c6a6

**12. `fork:5e8875c3`**

- *similarity*: 0.971
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: fit redCards regression with interactions, varying the focal predictor #2
- *option_b*: fit redCards regression with interactions, varying the focal predictor #3
- *fork*: are interaction terms included in the model?
- *trace_a*: opt:548f869e
- *trace_b*: opt:f8c8e2c7

**13. `fork:1aebd46a`**

- *similarity*: 0.968
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: logistic, continuous skin tone, full adjustment, default SEs #2
- *option_b*: logistic, continuous skin tone, full adjustment, default SEs #3
- *fork*: which regression model, estimator, and SE scheme specifies the primary confound-adjusted skin-tone effect on red cards?
- *trace_a*: opt:8fef9816
- *trace_b*: opt:1f39b5f5

**14. `fork:b1fc4f73`**

- *similarity*: 0.968
- *runs_a*: 98
- *runs_b*: 16
- *option_a*: cluster-robust SEs, varying clustering dimension (unspecified / player / referee / two-way player+referee / referee-country)
- *option_b*: cluster-robust SEs, varying clustering dimension (unspecified / player / referee / two-way player+referee / referee-country) #2
- *fork*: how are the regression model's standard errors estimated?
- *trace_a*: opt:121963dd
- *trace_b*: opt:4cbd50ba

**15. `fork:6579c06a`**

- *similarity*: 0.968
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: format the rater×bias interaction coefficients for the results table #2
- *option_b*: format the rater×bias interaction coefficients for the results table #3
- *fork*: how are the interaction coefficients presented in the results table?
- *trace_a*: opt:748337f8
- *trace_b*: opt:f1f6fd16

**16. `fork:6579c06a`**

- *similarity*: 0.968
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: format the rater×bias interaction coefficients for the results table #2
- *option_b*: format the rater×bias interaction coefficients for the results table #4
- *fork*: how are the interaction coefficients presented in the results table?
- *trace_a*: opt:748337f8
- *trace_b*: opt:95428a95

**17. `fork:6579c06a`**

- *similarity*: 0.968
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: format the rater×bias interaction coefficients for the results table #3
- *option_b*: format the rater×bias interaction coefficients for the results table #4
- *fork*: how are the interaction coefficients presented in the results table?
- *trace_a*: opt:f1f6fd16
- *trace_b*: opt:95428a95

**18. `fork:1aebd46a`**

- *similarity*: 0.966
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: categorical rater1 exposure through referee fixed effects #2
- *option_b*: categorical rater1 exposure through referee fixed effects #3
- *fork*: which regression model, estimator, and SE scheme specifies the primary confound-adjusted skin-tone effect on red cards?
- *trace_a*: opt:b7265e20
- *trace_b*: opt:7119bbe8

**19. `fork:e9676146`**

- *similarity*: 0.962
- *runs_a*: 24
- *runs_b*: 2
- *option_a*: dyad/observation-level nonparametric bootstrap, refit logistic, percentile CI
- *option_b*: dyad/observation-level nonparametric bootstrap, refit logistic, percentile CI #2
- *fork*: what bootstrap resampling scheme is used to compute the confidence interval?
- *trace_a*: opt:d7b6b8a7
- *trace_b*: opt:28910e9d

**20. `fork:8f3d6c78`**

- *similarity*: 0.958
- *runs_a*: 1
- *runs_b*: 1
- *option_a*: pair a country-level mean bias score with gm3's random skin-tone slope
- *option_b*: pair a country-level mean bias score with gm3's random skin-tone slope #2
- *fork*: Is the skin-tone slope allowed to vary and be linked to a country-level bias score?
- *trace_a*: opt:13db408d
- *trace_b*: opt:18afe4b9

## V2 — every fork is a slot where a run picks exactly one option

**REVIEW** — 43 of 317 forks have runs that took two options; the single-choice model does not hold for all of them

*Compared against:* structural, and conclusive about the pattern -- a run cannot take two alternatives at one slot. What it cannot settle is WHY, and the three causes below are indistinguishable by shape

*Cannot see:* which of the three causes produced any given row, and any fork the grouping already split BECAUSE its options co-occurred -- those cannot appear here by construction

> **Entangled.** This check uses `co_occurrence`, which the pipeline also used to build what is being checked (cannot-link constraint in merge_forks and induce_forks — two options chosen by one run is treated as evidence their forks differ). Its agreement is not independent evidence.

| measure | value |
|---|---|
| violating_pairs | 386 |
| forks_affected | 43 |
| forks_total | 317 |
| pairs_sharing_one_run | 296 |

### forks whose runs took more than one option

Showing the worst **20 of 43**.

> Three causes produce this identically, and only reading the fork separates them. (a) The fork is genuinely MULTI-SELECT -- reporting both an odds ratio and a risk difference is one analyst doing two legitimate things, not a clustering error, and the single-choice model is simply wrong for that slot. (b) A ROBUSTNESS REFIT -- one run dichotomising at 0.25 and again at 0.50; expected, and the reason most rows here share exactly one run. (c) A CLUSTERING ARTIFACT -- a fork with more co-choices than runs is not a slot at all. Sort by `rate`: high rate on few runs is (c), low rate on many runs is (b), high rate on many runs is (a).

**1. `fork:753a1bff`**

- *co_choices*: 409
- *pairs*: 187
- *runs*: 211
- *options*: 71
- *rate*: 1.938
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?

**2. `fork:1aebd46a`**

- *co_choices*: 54
- *pairs*: 53
- *runs*: 93
- *options*: 39
- *rate*: 0.581
- *fork*: which regression model, estimator, and SE scheme specifies the primary confound-adjusted skin-tone effect on red cards?

**3. `fork:bfb93694`**

- *co_choices*: 45
- *pairs*: 35
- *runs*: 127
- *options*: 52
- *rate*: 0.354
- *fork*: which covariates make up the model's adjustment set?

**4. `fork:f68bb1ba`**

- *co_choices*: 34
- *pairs*: 8
- *runs*: 111
- *options*: 9
- *rate*: 0.306
- *fork*: how are the confidence interval and p-value for the exposure effect computed?

**5. `fork:8d07b365`**

- *co_choices*: 25
- *pairs*: 6
- *runs*: 175
- *options*: 6
- *rate*: 0.143
- *fork*: which effect-size measure is used to express the exposure's effect on red cards?

**6. `fork:b1fc4f73`**

- *co_choices*: 23
- *pairs*: 5
- *runs*: 108
- *options*: 7
- *rate*: 0.213
- *fork*: how are the regression model's standard errors estimated?

**7. `fork:441e6c5d`**

- *co_choices*: 15
- *pairs*: 15
- *runs*: 2
- *options*: 7
- *rate*: 7.5
- *fork*: how is the continuous skin-tone rating discretized into categories for analysis?

**8. `fork:4c1b4953`**

- *co_choices*: 10
- *pairs*: 2
- *runs*: 203
- *options*: 3
- *rate*: 0.049
- *fork*: How is the red-card outcome operationalised and modelled — a binary indicator, a raw count, or a count with an exposure offset?

**9. `fork:9c0ec519`**

- *co_choices*: 10
- *pairs*: 7
- *runs*: 214
- *options*: 6
- *rate*: 0.047
- *fork*: how are the two raters combined into a single skin-tone exposure measure?

**10. `fork:e9676146`**

- *co_choices*: 7
- *pairs*: 3
- *runs*: 44
- *options*: 5
- *rate*: 0.159
- *fork*: what bootstrap resampling scheme is used to compute the confidence interval?

**11. `fork:553ece13`**

- *co_choices*: 6
- *pairs*: 4
- *runs*: 30
- *options*: 5
- *rate*: 0.2
- *fork*: what minimum number of shared games per dyad is required for inclusion?

**12. `fork:a39a9523`**

- *co_choices*: 6
- *pairs*: 6
- *runs*: 1
- *options*: 4
- *rate*: 6.0
- *fork*: which moderation model specification is estimated?

**13. `fork:6579c06a`**

- *co_choices*: 6
- *pairs*: 6
- *runs*: 1
- *options*: 4
- *rate*: 6.0
- *fork*: how are the interaction coefficients presented in the results table?

**14. `fork:c62e464b`**

- *co_choices*: 5
- *pairs*: 5
- *runs*: 119
- *options*: 17
- *rate*: 0.042
- *fork*: what rule determines whether the effect is declared statistically supported?

**15. `fork:d3dbe4e1`**

- *co_choices*: 5
- *pairs*: 4
- *runs*: 111
- *options*: 10
- *rate*: 0.045
- *fork*: how are records with missing covariates handled — complete-case, impute, or recode as explicit category?

**16. `fork:f3162f72`**

- *co_choices*: 5
- *pairs*: 4
- *runs*: 82
- *options*: 9
- *rate*: 0.061
- *fork*: how is the crude, unadjusted association estimated and tested?

**17. `fork:1bfc73f3`**

- *co_choices*: 5
- *pairs*: 2
- *runs*: 137
- *options*: 4
- *rate*: 0.036
- *fork*: When forming adjusted counterfactual predictions, are covariates averaged over the observed sample or fixed at a single reference profile?

**18. `fork:db670d07`**

- *co_choices*: 5
- *pairs*: 5
- *runs*: 41
- *options*: 16
- *rate*: 0.122
- *fork*: which regression model and outcome family estimates the exposure–red-card association?

**19. `fork:f13c05e7`**

- *co_choices*: 4
- *pairs*: 1
- *runs*: 26
- *options*: 3
- *rate*: 0.154
- *fork*: are goalkeepers included in or excluded from the analysis sample?

**20. `fork:2a6f87c0`**

- *co_choices*: 3
- *pairs*: 2
- *runs*: 9
- *options*: 4
- *rate*: 0.333
- *fork*: how is moderation of the referee-bias effect by player skin tone assessed?

### the individual option pairs

Showing the worst **20 of 386**.

> Read these before acting on the fork-level table above.

**1. `fork:753a1bff`**

- *shared_runs*: 34
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: single-cutoff dichotomize at 0.5
- *runs*: 2025-11-12T09-30-16+0000, 2025-11-12T12-24-45+0000, 2025-11-12T13-06-46+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:650c1f36

**2. `fork:753a1bff`**

- *shared_runs*: 29
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: drop-middle dichotomize 0.25/0.75
- *runs*: 2025-11-12T09-52-44+0000, 2025-11-12T13-06-46+0000, 2025-11-12T17-10-55+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:4770a012

**3. `fork:753a1bff`**

- *shared_runs*: 21
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: single-cutoff dichotomize at 0.25
- *runs*: 2025-11-16T09-53-00+0000, 2025-11-16T11-59-47+0000, 2025-11-16T17-04-39+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:f464e581

**4. `fork:753a1bff`**

- *shared_runs*: 18
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: single-cutoff dichotomize at 0.5
- *option_b*: drop-middle dichotomize 0.25/0.75
- *runs*: 2025-11-12T12-54-24+0000, 2025-11-12T13-06-46+0000, 2025-11-12T17-10-55+0000
- *trace_a*: opt:650c1f36
- *trace_b*: opt:4770a012

**5. `fork:8d07b365`**

- *shared_runs*: 16
- *fork*: which effect-size measure is used to express the exposure's effect on red cards?
- *option_a*: report only an odds ratio
- *option_b*: report a risk difference plus an odds ratio
- *runs*: 2025-11-12T11-24-34+0000, 2025-11-12T12-54-24+0000, 2025-11-12T17-30-15+0000
- *trace_a*: opt:6c3d5475
- *trace_b*: opt:5d50266f

**6. `fork:b1fc4f73`**

- *shared_runs*: 16
- *fork*: how are the regression model's standard errors estimated?
- *option_a*: cluster-robust SEs, varying clustering dimension (unspecified / player / referee / two-way player+referee / referee-country)
- *option_b*: cluster-robust SEs, varying clustering dimension (unspecified / player / referee / two-way player+referee / referee-country) #2
- *runs*: 2025-11-12T18-56-42+0000, 2025-11-12T22-11-51+0000, 2025-11-17T14-46-19+0000
- *trace_a*: opt:121963dd
- *trace_b*: opt:4cbd50ba

**7. `fork:753a1bff`**

- *shared_runs*: 12
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: search single cutoff maximizing effect size
- *runs*: 2025-11-14T22-05-46+0000, 2025-11-16T09-53-00+0000, 2025-11-17T01-20-10+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:ad997da0

**8. `fork:753a1bff`**

- *shared_runs*: 11
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: single-cutoff dichotomize, unspecified cutoff, full sample
- *option_b*: enter continuous, raw (per-unit, full range)
- *runs*: 2025-11-12T21-15-40+0000, 2025-11-15T17-13-29+0000, 2025-11-19T07-38-28+0000
- *trace_a*: opt:198a3387
- *trace_b*: opt:65961bfc

**9. `fork:4c1b4953`**

- *shared_runs*: 9
- *fork*: How is the red-card outcome operationalised and modelled — a binary indicator, a raw count, or a count with an exposure offset?
- *option_a*: Poisson regression on raw counts with log(games) exposure offset
- *option_b*: binarize into a binary any-red indicator (logistic/binary model)
- *runs*: 2025-11-12T09-52-44+0000, 2025-11-20T02-49-33+0000, 2025-11-20T04-21-39+0000
- *trace_a*: opt:0b8aaec0
- *trace_b*: opt:0d79aab2

**10. `fork:753a1bff`**

- *shared_runs*: 7
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: trichotomize at 0.25/0.75
- *runs*: 2025-11-15T23-57-58+0000, 2025-11-19T07-38-28+0000, 2025-11-22T11-14-05+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:f8afefc8

**11. `fork:753a1bff`**

- *shared_runs*: 7
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: single-cutoff dichotomize at 0.75
- *runs*: 2025-11-20T21-05-32+0000, 2025-11-22T14-03-14+0000, 2025-11-26T18-25-33+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:a2ee7e09

**12. `fork:f68bb1ba`**

- *shared_runs*: 7
- *fork*: how are the confidence interval and p-value for the exposure effect computed?
- *option_a*: percentile bootstrap CI (resampling unspecified)
- *option_b*: bootstrap p-value from tail proportion of draws crossing zero, resampling scheme unspecified
- *runs*: 2025-11-12T10-05-42+0000, 2025-11-15T02-22-25+0000, 2025-11-15T23-57-58+0000
- *trace_a*: opt:aa99d7aa
- *trace_b*: opt:2feb434b

**13. `fork:f68bb1ba`**

- *shared_runs*: 7
- *fork*: how are the confidence interval and p-value for the exposure effect computed?
- *option_a*: model-based Wald CI/p from the GLM coefficient SE
- *option_b*: analytic delta-method SE via g-computation gradient, Wald CI/p
- *runs*: 2025-11-12T21-15-40+0000, 2025-11-15T20-23-37+0000, 2025-11-17T21-31-42+0000
- *trace_a*: opt:36c94204
- *trace_b*: opt:9e0209a5

**14. `fork:753a1bff`**

- *shared_runs*: 6
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: extreme groups at endpoints 0 vs 1
- *option_b*: enter continuous, raw (per-unit, full range)
- *runs*: 2025-11-16T07-53-05+0000, 2025-11-16T17-04-39+0000, 2025-11-17T14-46-19+0000
- *trace_a*: opt:113e482e
- *trace_b*: opt:65961bfc

**15. `fork:753a1bff`**

- *shared_runs*: 6
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: drop-middle dichotomize 0.25/0.5
- *runs*: 2025-11-15T15-38-19+0000, 2025-11-17T05-02-45+0000, 2025-11-19T22-14-21+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:094c5d0a

**16. `fork:753a1bff`**

- *shared_runs*: 6
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: enter continuous, raw (per-unit, full range)
- *option_b*: drop-middle dichotomize 0.375/0.625
- *runs*: 2025-11-12T11-24-34+0000, 2025-11-20T22-17-42+0000, 2025-11-20T22-39-34+0000
- *trace_a*: opt:65961bfc
- *trace_b*: opt:8cc4c381

**17. `fork:753a1bff`**

- *shared_runs*: 6
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: search single cutoff maximizing effect size
- *option_b*: single-cutoff dichotomize at 0.25
- *runs*: 2025-11-16T09-53-00+0000, 2025-11-27T00-12-07+0000, 2025-11-27T01-53-05+0000
- *trace_a*: opt:ad997da0
- *trace_b*: opt:f464e581

**18. `fork:f68bb1ba`**

- *shared_runs*: 6
- *fork*: how are the confidence interval and p-value for the exposure effect computed?
- *option_a*: parametric bootstrap from full coefficient MVN/covariance, percentile-quantile inference (percentile CI and crossing-zero p are duals of the same draws)
- *option_b*: bootstrap p-value from tail proportion of draws crossing zero, resampling scheme unspecified
- *runs*: 2025-11-15T18-59-03+0000, 2025-11-16T07-53-05+0000, 2025-11-21T00-55-35+0000
- *trace_a*: opt:1078a805
- *trace_b*: opt:2feb434b

**19. `fork:753a1bff`**

- *shared_runs*: 5
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: single-cutoff dichotomize, unspecified cutoff, full sample
- *option_b*: drop-middle dichotomize 0.25/0.75
- *runs*: 2025-11-15T17-13-29+0000, 2025-11-17T20-22-41+0000, 2025-11-20T06-03-23+0000
- *trace_a*: opt:198a3387
- *trace_b*: opt:4770a012

**20. `fork:753a1bff`**

- *shared_runs*: 5
- *fork*: how is the skin-tone rating entered as the exposure — continuous or split/binned at which cutpoints?
- *option_a*: drop-middle dichotomize 0.125/0.75
- *option_b*: enter continuous, raw (per-unit, full range)
- *runs*: 2025-11-16T11-59-47+0000, 2025-11-17T05-02-45+0000, 2025-11-19T22-14-21+0000
- *trace_a*: opt:9bfc6e8a
- *trace_b*: opt:65961bfc

## V3 — distinct forks ask distinct questions

**REVIEW** — 24 fork pairs to read

*Compared against:* no null -- a ranking for human attention, not a test

*Cannot see:* two forks asking one question in unrelated words, and -- since the merge passes already united the label-similar pairs that do NOT co-occur -- this queue is enriched for pairs the pipeline refused on structural grounds

> **Entangled.** This check uses `label_similarity`, `option_lists`, which the pipeline also used to build what is being checked (candidate screen for every merge pass; what the grouping passes were shown when they decided). Its agreement is not independent evidence.

| measure | value |
|---|---|
| fork_pairs | 50086 |
| above | 24 |
| threshold | 0.6 |

### fork pairs most likely to be one question

Showing the worst **20 of 24**.

> Merging two forks that are genuinely one is safe; merging two that are not destroys a distinction invisibly. Read both option lists before acting on any row here.

**1. `#1`**

- *similarity*: 0.853
- *runs_a*: 33
- *runs_b*: 2
- *fork_a*: how is agreement between the two skin-tone raters quantified?
- *fork_b*: how is inter-rater agreement between the two skin-tone raters quantified?
- *trace_a*: fork:4e20f1b5
- *trace_b*: fork:8c4f167e

**2. `#2`**

- *similarity*: 0.849
- *runs_a*: 2
- *runs_b*: 1
- *fork_a*: Is an explicit-bias (country-mean Exp) cross-level interaction added to the preferred model?
- *fork_b*: Is an implicit-bias (country-mean IAT) cross-level interaction added to the preferred model?
- *trace_a*: fork:f8cddcf1
- *trace_b*: fork:9da021ab

**3. `#3`**

- *similarity*: 0.841
- *runs_a*: 1
- *runs_b*: 209
- *fork_a*: which version of the dataset is loaded?
- *fork_b*: which version of the source dataset is loaded?
- *trace_a*: fork:da4bffaa
- *trace_b*: fork:e21a9784

**4. `#4`**

- *similarity*: 0.808
- *runs_a*: 2
- *runs_b*: 4
- *fork_a*: how is the continuous skin-tone rating discretized into categories for analysis?
- *fork_b*: how is the continuous skin-tone rating discretized into categories?
- *trace_a*: fork:441e6c5d
- *trace_b*: fork:0cc97d1e

**5. `#5`**

- *similarity*: 0.802
- *runs_a*: 1
- *runs_b*: 1
- *fork_a*: How is the referee explicit-bias column's string 'NA' parsed to numeric?
- *fork_b*: How is the referee implicit-bias (IAT) column's string 'NA' parsed to numeric?
- *trace_a*: fork:30f2d973
- *trace_b*: fork:4dc70b2a

**6. `#6`**

- *similarity*: 0.8
- *runs_a*: 1
- *runs_b*: 2
- *fork_a*: Are goalkeepers included in the analysis sample?
- *fork_b*: Are goalkeepers included in the analytic sample?
- *trace_a*: fork:ba0485e1
- *trace_b*: fork:6c9ad8d3

**7. `#7`**

- *similarity*: 0.8
- *runs_a*: 1
- *runs_b*: 1
- *fork_a*: which version / sheet of the dataset is loaded?
- *fork_b*: which version of the dataset is loaded?
- *trace_a*: fork:c7405ac7
- *trace_b*: fork:da4bffaa

**8. `#8`**

- *similarity*: 0.782
- *runs_a*: 1
- *runs_b*: 3
- *fork_a*: how is covariate balance across groups checked?
- *fork_b*: how is covariate balance across skin-tone groups checked?
- *trace_a*: fork:7f478863
- *trace_b*: fork:e151894f

**9. `#9`**

- *similarity*: 0.774
- *runs_a*: 1
- *runs_b*: 3
- *fork_a*: How is covariate balance across skin-tone groups examined?
- *fork_b*: how is covariate balance across skin-tone groups checked?
- *trace_a*: fork:33afb732
- *trace_b*: fork:e151894f

**10. `#10`**

- *similarity*: 0.759
- *runs_a*: 1
- *runs_b*: 26
- *fork_a*: Are goalkeepers included in the analysis sample?
- *fork_b*: are goalkeepers included in or excluded from the analysis sample?
- *trace_a*: fork:ba0485e1
- *trace_b*: fork:f13c05e7

**11. `#11`**

- *similarity*: 0.737
- *runs_a*: 1
- *runs_b*: 1
- *fork_a*: what regression model form is used for the outcome?
- *fork_b*: what regression model is used for the red-card outcome?
- *trace_a*: fork:789e92ad
- *trace_b*: fork:bc348127

**12. `#12`**

- *similarity*: 0.722
- *runs_a*: 1
- *runs_b*: 2
- *fork_a*: how is covariate balance across groups checked?
- *fork_b*: is covariate balance across exposure groups checked?
- *trace_a*: fork:7f478863
- *trace_b*: fork:24177edd

**13. `#13`**

- *similarity*: 0.705
- *runs_a*: 2
- *runs_b*: 1
- *fork_a*: how is the fitted model's calibration / goodness-of-fit assessed?
- *fork_b*: how is the fitted model's calibration assessed?
- *trace_a*: fork:887b364d
- *trace_b*: fork:85849c05

**14. `#14`**

- *similarity*: 0.692
- *runs_a*: 1
- *runs_b*: 209
- *fork_a*: which version / sheet of the dataset is loaded?
- *fork_b*: which version of the source dataset is loaded?
- *trace_a*: fork:c7405ac7
- *trace_b*: fork:e21a9784

**15. `#15`**

- *similarity*: 0.646
- *runs_a*: 37
- *runs_b*: 2
- *fork_a*: How are raw group red-card rates reported descriptively?
- *fork_b*: How are the descriptive per-group red-card rates reported?
- *trace_a*: fork:dec389b8
- *trace_b*: fork:38cb96e2

**16. `#16`**

- *similarity*: 0.642
- *runs_a*: 2
- *runs_b*: 2
- *fork_a*: Are dyads with zero games excluded from the sample?
- *fork_b*: How are dyads with too few shared games excluded from the sample?
- *trace_a*: fork:29f104f9
- *trace_b*: fork:e92e0b5b

**17. `#17`**

- *similarity*: 0.635
- *runs_a*: 3
- *runs_b*: 2
- *fork_a*: how is covariate balance across skin-tone groups checked?
- *fork_b*: is covariate balance across exposure groups checked?
- *trace_a*: fork:e151894f
- *trace_b*: fork:24177edd

**18. `#18`**

- *similarity*: 0.625
- *runs_a*: 1
- *runs_b*: 2
- *fork_a*: Is a descriptive summary table produced?
- *fork_b*: Which variables are reported in the descriptive summary table?
- *trace_a*: fork:a3c9d5d0
- *trace_b*: fork:b2281b1e

**19. `#19`**

- *similarity*: 0.622
- *runs_a*: 1
- *runs_b*: 1
- *fork_a*: what regression model is used for the red-card outcome?
- *fork_b*: which regression model/effect measure is used for the red-card outcome?
- *trace_a*: fork:bc348127
- *trace_b*: fork:d0db1036

**20. `#20`**

- *similarity*: 0.619
- *runs_a*: 2
- *runs_b*: 26
- *fork_a*: Are goalkeepers included in the analytic sample?
- *fork_b*: are goalkeepers included in or excluded from the analysis sample?
- *trace_a*: fork:6c9ad8d3
- *trace_b*: fork:f13c05e7

## V4 — an option records one action, not several

**REVIEW** — 116 options bundle separable actions

*Compared against:* structural smell -- clause counting, which over-fires on options that are genuinely one action described carefully

*Cannot see:* a compound option written as a single clause: 'complete-case analysis' bundles a drop rule and a scope and counts as one

| measure | value |
|---|---|
| options | 777 |
| compound | 116 |

### options describing the most separable actions

Showing the worst **20 of 116**.

> A compound option makes two decisions inseparable: any run choosing it is recorded as having made both, and the second one vanishes from its own fork.

**1. `opt:df7d040a`**

- *clauses*: 9
- *runs*: 5
- *option*: games, height, weight, goals, yellowCards, meanIAT, meanExp, position, league
- *fork*: which covariates make up the model's adjustment set?

**2. `opt:bf37dbf9`**

- *clauses*: 9
- *runs*: 2
- *option*: games, position, league, yellowCards, meanIAT, meanExp, height, weight, age
- *fork*: which covariates make up the model's adjustment set?

**3. `opt:f0a15320`**

- *clauses*: 9
- *runs*: 1
- *option*: games, height, weight, goals, yellowCards, meanIAT, meanExp, position, league #2
- *fork*: which covariates make up the model's adjustment set?

**4. `opt:36ceac72`**

- *clauses*: 8
- *runs*: 3
- *option*: games, age, height, weight, position, league, meanIAT, meanExp
- *fork*: which covariates make up the model's adjustment set?

**5. `opt:d6d4bc4b`**

- *clauses*: 8
- *runs*: 1
- *option*: position, league, games, yellowCards, goals, height, weight, meanIAT
- *fork*: which covariates make up the model's adjustment set?

**6. `opt:ee6e4478`**

- *clauses*: 8
- *runs*: 1
- *option*: games, yellowCards, age, height, weight, league, meanIAT, meanExp (no position)
- *fork*: which covariates make up the model's adjustment set?

**7. `opt:5d0df0f6`**

- *clauses*: 8
- *runs*: 1
- *option*: games, height, weight, age, yellowCards, goals, position, league
- *fork*: which covariates make up the model's adjustment set?

**8. `opt:bb3e14b4`**

- *clauses*: 7
- *runs*: 1
- *option*: league, position, age, height, weight, yellowCards, goals (no games)
- *fork*: which covariates make up the model's adjustment set?

**9. `opt:fd71782c`**

- *clauses*: 7
- *runs*: 1
- *option*: position, league, games, yellowCards, goals, height, weight
- *fork*: which covariates make up the model's adjustment set?

**10. `opt:ca18a462`**

- *clauses*: 7
- *runs*: 1
- *option*: yellowCards, height, weight, position, league, meanIAT, meanExp (no games)
- *fork*: which covariates make up the model's adjustment set?

**11. `opt:d7d82868`**

- *clauses*: 7
- *runs*: 1
- *option*: games, victories, defeats, age, height, weight, goals (no position/league)
- *fork*: which covariates make up the model's adjustment set?

**12. `opt:bab65b61`**

- *clauses*: 7
- *runs*: 1
- *option*: games, position, league, height, weight, yellowCards, meanIAT
- *fork*: which covariates make up the model's adjustment set?

**13. `opt:c5fd9418`**

- *clauses*: 6
- *runs*: 21
- *option*: full standard set: games, position, league, height, weight, player+referee ids
- *fork*: which covariates make up the model's adjustment set?

**14. `opt:8858ca20`**

- *clauses*: 6
- *runs*: 4
- *option*: log(games), position, height, weight, yellowCards, league
- *fork*: which covariates make up the model's adjustment set?

**15. `opt:8a15e53d`**

- *clauses*: 6
- *runs*: 1
- *option*: games, position, age, height, weight, yellowCards (no league)
- *fork*: which covariates make up the model's adjustment set?

**16. `opt:74a5b56f`**

- *clauses*: 6
- *runs*: 1
- *option*: raw games, position, league, yellowCards, height, weight
- *fork*: which covariates make up the model's adjustment set?

**17. `opt:7f8790f2`**

- *clauses*: 6
- *runs*: 1
- *option*: games, yellowCards, position, league, meanIAT, meanExp
- *fork*: which covariates make up the model's adjustment set?

**18. `opt:d72bf99d`**

- *clauses*: 6
- *runs*: 1
- *option*: add dark_skin×league interaction adjusting for log_games, position, height, weight, playerShort; derive per-league ORs
- *fork*: is a skin-tone × league interaction included so the effect can vary by league?

**19. `opt:264edd6c`**

- *clauses*: 5
- *runs*: 4
- *option*: linear games, position, league, height, weight (standardized or raw)
- *fork*: which covariates make up the model's adjustment set?

**20. `opt:ff0ab93e`**

- *clauses*: 5
- *runs*: 2
- *option*: games, yellowCards, position, league, age (no anthropometrics)
- *fork*: which covariates make up the model's adjustment set?

## V6 — an option records one use, not a primary and a refit

**REVIEW** — 2 options merge a run's distant decisions

*Compared against:* structural, and conclusive in one direction only -- two decisions written 200 lines apart are not one operation, but two written 3 lines apart may well be

*Cannot see:* a primary and a refit that happen to sit close together, and a repeat across DIFFERENT runs, which is what an option is for and is not a defect

| measure | value |
|---|---|
| groups | 22 |
| distant | 2 |
| adjacent | 20 |
| span_threshold | 5 |

### options merging distant decisions from one run

All **2**.

> Splitting these is the sanctioned direction: over-merge is invisible in the output and unrecoverable, under-merge is visible and a human can undo it. stability/scripts/repair_option_splits.py applies the split; it does not decide whether the split is right.

**1. `opt:9aef08e2`**

- *span*: 10
- *n*: 3
- *lines*: 154/159/164
- *run*: 2025-11-17T01-20-10+0000
- *option*: marginal standardization / g-computation: average counterfactual predictions over the observed sample, then difference
- *fork*: When forming adjusted counterfactual predictions, are covariates averaged over the observed sample or fixed at a single reference profile?

**2. `opt:1879411f`**

- *span*: 7
- *n*: 3
- *lines*: 110/113/117
- *run*: team-10
- *option*: screen a player-level variable for confounding by testing its association with skin tone
- *fork*: How are potential confounders screened for association with skin tone?

## V7 — an option's label names one choice, not a list

**REVIEW** — 36 options carry a disjunctive label, 1 of them also flagged by V6

*Compared against:* lexical only -- it reads the label, never the members, so a genuinely single action described with an 'or' will fire

*Cannot see:* an over-merged option with a clean label, which is the majority: V7 finds the ones that announce themselves

| measure | value |
|---|---|
| options | 777 |
| disjunctive | 36 |
| also_flagged_by_v6 | 1 |

### options whose label lists alternatives

Showing the worst **20 of 36**.

> Enriched 8.3x for same-run merges on this corpus, so a disjunctive label is a usable prior on over-merge even before any member is read.

**1. `opt:9aef08e2`**

- *runs*: 135
- *also_v6*: True
- *option*: marginal standardization / g-computation: average counterfactual predictions over the observed sample, then difference
- *fork*: When forming adjusted counterfactual predictions, are covariates averaged over the observed sample or fixed at a single reference profile?

**2. `opt:0d79aab2`**

- *runs*: 198
- *also_v6*: False
- *option*: binarize into a binary any-red indicator (logistic/binary model)
- *fork*: How is the red-card outcome operationalised and modelled — a binary indicator, a raw count, or a count with an exposure offset?

**3. `opt:121963dd`**

- *runs*: 98
- *also_v6*: False
- *option*: cluster-robust SEs, varying clustering dimension (unspecified / player / referee / two-way player+referee / referee-country)
- *fork*: how are the regression model's standard errors estimated?

**4. `opt:f6283bfc`**

- *runs*: 84
- *also_v6*: False
- *option*: complete-case / listwise deletion
- *fork*: how are records with missing covariates handled — complete-case, impute, or recode as explicit category?

**5. `opt:415a6b71`**

- *runs*: 58
- *also_v6*: False
- *option*: crude risk difference, point estimate only (no test or CI)
- *fork*: how is the crude, unadjusted association estimated and tested?

**6. `opt:20700931`**

- *runs*: 38
- *also_v6*: False
- *option*: z-score a varying subset of continuous covariates (umbrella/aggregate)
- *fork*: how are continuous predictors transformed and z-scored/standardized before modeling?

**7. `opt:1b89b45d`**

- *runs*: 29
- *also_v6*: False
- *option*: collapse into 4 categories (GK/Def/Mid/Fwd), no residual
- *fork*: how many categories, and by what mapping, is player position collapsed into?

**8. `opt:0dd15c26`**

- *runs*: 25
- *also_v6*: False
- *option*: report the average marginal effect / risk difference (RD) as primary
- *fork*: which model effect is reported as primary, and on what scale (risk difference/AME vs odds ratio)?

**9. `opt:4afd03ed`**

- *runs*: 17
- *also_v6*: False
- *option*: overall median-impute continuous covariates (height/weight, ±age)
- *fork*: how are records with missing covariates handled — complete-case, impute, or recode as explicit category?

**10. `opt:4cbd50ba`**

- *runs*: 16
- *also_v6*: False
- *option*: cluster-robust SEs, varying clustering dimension (unspecified / player / referee / two-way player+referee / referee-country) #2
- *fork*: how are the regression model's standard errors estimated?

**11. `opt:d6182cd7`**

- *runs*: 7
- *also_v6*: False
- *option*: declare hypothesis supported (significant/robust)
- *fork*: what overall conclusion is drawn about the hypothesis?

**12. `opt:eca007f9`**

- *runs*: 4
- *also_v6*: False
- *option*: predict at a single fixed reference profile (means/modal categories), then difference
- *fork*: When forming adjusted counterfactual predictions, are covariates averaged over the observed sample or fixed at a single reference profile?

**13. `opt:aa41c6a6`**

- *runs*: 4
- *also_v6*: False
- *option*: marginal standardization / g-computation: average counterfactual predictions over the observed sample, then difference #2
- *fork*: When forming adjusted counterfactual predictions, are covariates averaged over the observed sample or fixed at a single reference profile?

**14. `opt:264edd6c`**

- *runs*: 4
- *also_v6*: False
- *option*: linear games, position, league, height, weight (standardized or raw)
- *fork*: which covariates make up the model's adjustment set?

**15. `opt:2ebc47b9`**

- *runs*: 4
- *also_v6*: False
- *option*: collapse into 6 categories, underspecified (Winger or Other+Unknown)
- *fork*: how many categories, and by what mapping, is player position collapsed into?

**16. `opt:af7679c1`**

- *runs*: 4
- *also_v6*: False
- *option*: collapse into 6 categories (four core + separate Other/Unknown)
- *fork*: how many categories, and by what mapping, is player position collapsed into?

**17. `opt:5f8bec8d`**

- *runs*: 3
- *also_v6*: False
- *option*: compute VIF on all covariates, no threshold or subset specified
- *fork*: is multicollinearity among covariates diagnosed?

**18. `opt:1a1419d7`**

- *runs*: 3
- *also_v6*: False
- *option*: conventional non-robust / model-based SEs
- *fork*: how are the regression model's standard errors estimated?

**19. `opt:063af9ce`**

- *runs*: 2
- *also_v6*: False
- *option*: compute Cohen's h effect size and bucket it into fixed categories (e.g. negligible/small/medium)
- *fork*: How is the effect-size magnitude reported and categorized?

**20. `opt:367bf811`**

- *runs*: 2
- *also_v6*: False
- *option*: report the model coefficient's Wald test (z-statistic / p-value on the log-odds scale) for the exposure term
- *fork*: How is the exposure term's statistical significance test reported?

## V5 — forks where nearly every run invented its own option

**INFO** — 0 forks need a human read; no verdict is available from the shape alone

*Compared against:* no null -- these are simultaneously the most interesting and the least trustworthy forks, and only reading them separates the two

*Cannot see:* an under-merged fork whose run count is low enough to fall under the >=8 floor, and any fork whose options are duplicated without inflating the per-run ratio

| measure | value |
|---|---|
| flagged | 0 |
| min_runs | 8 |
| min_ratio | 0.7 |

### forks with the most options per run

All **0**.

> A fork with 22 options over 22 runs is either the most contested object in the corpus or a clustering failure. The shape is identical; only the content distinguishes them.

*(none)*

