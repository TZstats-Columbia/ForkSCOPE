# `stability/` — does the pipeline return the same answer twice?

Every other audit family in this repo asks whether **one** build is internally
sound. This one asks whether the build would **come back the same** — which no
single-build check can see, because a build has no way of knowing what it would
have said on a different day.

## The distinction this folder exists to enforce

Two vocabulary builds can differ for two unrelated reasons, and the output
files look identical either way:

| | what differs | what it measures |
|---|---|---|
| **replicate** | model called again, same corpora, same distilled input | run-to-run variability — **this is stability** |
| **scope change** | different corpora pooled | the effect of adding/removing a corpus — **not stability** |

Conflating them is the specific error this folder guards against. Every script
reads the corpora from the vocabulary headers, classifies the comparison, and
writes the verdict into its output. `audit_stability.py` **refuses** to let a
scope comparison stand in for a replicate — `S2`/`S3` report `NOT RUN` rather
than quoting a number that looks like stability and isn't.

## Running it

There is no Python on the Windows host. Use the dev container:

```bash
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "<path to your checkout>:/work" -w /work/forkscope \
  distill-dev:latest python stability/scripts/<script>.py ...
```

`MSYS_NO_PATHCONV=1` is required — Git Bash otherwise rewrites `/work` into a
Windows path and Docker rejects it.

## Scripts

| script | question | needs |
|---|---|---|
| `partition.py` | metric library: ARI, VI, B-cubed, merge/split events | — |
| `q1_distill.py` | Q1 does distillation reproduce, per run | a distill replicate |
| `q2_ablation.py` | Q2 does the alignment judge reproduce | **already have two** |
| `q3_vocab.py` | Q3 do options and forks reproduce | a vocab replicate |
| `q4_circle.py` | Q4 do the highways and persona enrichments reproduce | a vocab replicate |
| `audit_stability.py` | S1–S6 verdicts, and the merge signal | whatever exists |
| `replicate.py` | build a replicate under an isolated study root | — |

### Why partition metrics rather than semantic matching

Both builds partition the **same decision instances** — verified: the 3,665 AI
instances are identical across builds, keyed on `(run, line, text-prefix)`. So
agreement is exact arithmetic on two labelings of one item set, with no model
calls and no matching heuristic.

Matching option labels by string or embedding similarity would import exactly
the failure the pipeline rejects for clustering: ~95% of option labels are
unique, so a lexical match rate measures phrasing, not agreement. Semantic
adjudication is reserved for *classifying* the disagreements (merge / split /
genuine), never for producing the headline number.

Three metrics, because they fail differently — **ARI** (chance-corrected pair
agreement), **VI** (a true metric, so it obeys the triangle inequality once
there are three builds), and **B-cubed** (per-instance, so it reveals *which
direction* the vocabulary moved).

## Replicating without destroying the baseline

`nocache=True` skips the cache **read** but still **writes** to the same key —
running it in place would overwrite build A while measuring it, irreversibly and
silently. So `replicate.py` gives each replicate its own `FORKSCOPE_STUDY` root
with an **empty cache**. Every call misses and goes to the model; the baseline
is out of reach by filesystem layout rather than by remembering a flag.

```bash
python3 stability/scripts/replicate.py init --root ../replicates/B --stage vocab
python3 stability/scripts/replicate.py run  --root ../replicates/B --stage vocab \
                                            --corpus ai,human
```

A `vocab` replicate copies `data/distilled` in, so stage 3's input is
byte-identical to build A's and any difference downstream is vocabulary
variability alone. A `distill` replicate leaves it empty — `do_run()` returns an
existing record untouched, so a leftover `record.json` would make the whole run
a silent no-op that looks like perfect stability.

## The merge signal

An **unstable merge is a suspect merge**. If build A puts two decisions in one
option and build B does not, the pipeline has answered "same action?" both ways
— which is the evidence a review round wants, free once two builds exist.

The response follows the project's existing asymmetry (over-merge is invisible
and unrecoverable; under-merge is visible and fixable): an unstable pair
defaults to **unmerged** and routes to review. Majority vote would silently keep
2-of-3 merges, which is the over-merge the rule exists to prevent.

## Status

See `METHODS.md` for the paper-ready write-up.

- **Q2 measured** on a genuine replicate. `S5` PASS.
- **Q1, Q3, Q4 not yet measured** — no replicate exists at matching scope. The
  pooled-vs-ai-only comparison in `data/q3_*.json` and `data/q4_*.json` is a
  **scope** comparison, retained as a calibration of the machinery and clearly
  labelled as not stability.
