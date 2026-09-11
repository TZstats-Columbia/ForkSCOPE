# audits/ — verdicts, and the evidence for them

Analyses ship with audits, and the audits have overturned reported results more
than once. They are pipeline stages, not optional extras.

**Start with [`vocab_exhibits.md`](vocab_exhibits.md).** It is written for a
person: a review queue ordered worst-first, with the actual items in it.

## The check sets

Each file is written by the script of the same name (`audit_ai.json` by
`audit_clusters.py`).

Every check now runs on the headline vocabulary. `<FINAL>` below is
`ai+human.merged.forkmerged.merged.induced.r3`.

| file | made by | set | verdict on `<FINAL>` |
|---|---|---|---|
| `audit_<FINAL>.json` | `audit_clusters.py` | A1–A9 | clustering properties — pass |
| `iteration_audit_<FINAL>.json` | `audit_iteration.py` | I1–I6 | **all pass** |
| `garden_audit_<FINAL>.json` | `audit_garden.py` | G1–G6 | **G1, G4 REVIEW** |
| `shapley_audit_<FINAL>.json` | `audit_shapley.py` | H1–H6 | **H1 REVIEW** |
| `ablation.json`, `ablation_audit.json` | `ablation.py`, `audit_ablation.py` | E1–E6 | **E2 REVIEW** |
| `granularity_audit_<FINAL>.json` | `audit_granularity.py` | | redundancy **0.990** on `.r3` |
| `lineage_audit_<FINAL>.json` | `audit_lineage.py` | | **2 of 13 fork pairs are one question** on `.r3` |
| `vocab_exhibits.json` / `.md` | `audit_vocab.py` | V1–V5 | see below |

`garden_audit_ai.json` and `garden_audit_ai+human.json` are kept beside the
current one: G1 passed on both earlier vocabularies and reviews on this one,
which is only visible if all three are here.

Verdicts are `PASS`, `REVIEW`, or `INFO`. **`REVIEW` does not mean "broken."**
Several are left failing deliberately and two of them *are* the finding —
the Validation section of [`../../report/REPORT.md`](../../report/REPORT.md) says which, and why.

```bash
python3 -c "import json;d=json.load(open('data/audits/garden_audit_ai+human.json'));\
print({k:v['verdict'] for k,v in d.items() if isinstance(v,dict) and 'verdict' in v})"
```

## The evidence contract

Newer checks (V1–V5) write through `scripts/exhibit.py` and emit four things
rather than one:

| | |
|---|---|
| `verdict` | PASS / REVIEW / INFO |
| `measurement` + `against` | what was computed, and the null it faced — or an explicit statement that there was none |
| `exhibits` | the actual items, **worst-first** |
| handles | `fork:`, `opt:`, `dec:<run>@<line>` — resolvable directly |

Two rules are enforced in code, not left to discipline:

- **Exhibits are worst-first.** `exhibit()` requires a `worst` key function, so
  a representative sample cannot be attached. A check earning trust shows the
  cases closest to breaking it, not its best ones.
- **A `REVIEW` with no exhibits raises.** A check that fails and cannot show
  what failed is not reviewable.

This exists because a statistic once reported that 2.7% of within-fork option
pairs were near-duplicates. It was reassuring and structurally blind — token
overlap cannot see that *"compute the mean of the two rater columns"* and
*"average the two raters' scores"* are one action. A person reading the two
option lists side by side found it in minutes. The summary hid the error; the
artifact showing raw items revealed it.

Hence: **a weak signal is a legitimate sort key for human attention and is
never evidence of absence.** Checks that rank that way say so in the exhibit's
note and do not claim PASS on its strength.

The older G/H/I/E audits predate the contract and emit verdicts plus
statistics. Retrofitting them is open work.

## Walking from an exhibit to the source

Every exhibit row carries a handle:

```bash
python3 ../../scripts/trace.py resolve fork:8d07b365
python3 ../../scripts/trace.py resolve opt:53c963cf
python3 ../../scripts/trace.py resolve dec:team-10@8
```

Four rungs resolve offline — fork, option, decision, run + line. The literal
source lines need a mounted corpus, since the scripts are third-party and not
vendored:

```bash
export FORKSCOPE_RAW_AI=/path/to/agentic-forking-path
python3 ../../scripts/trace.py option "average rater1 and rater2" --source
```

## What the current run says

| | |
|---|---|
| V1 | 561 of 5,611 within-fork option pairs queued for reading |
| V2 | 43 of 317 forks contain runs that took **two** options, across 386 pairs |
| V3 | 24 of 50,086 fork pairs may be one question |
| V4 | 116 of 777 options bundle separable actions |
| V5 | 0 forks flagged where nearly every run invented its own option |
| V6 | 2 of 22 option groups span distant script regions |
| V7 | 36 of 777 options carry a disjunctive label |

V2 is the only one whose evidence is conclusive about the *pattern* — a run
cannot take two alternatives at one slot. It cannot settle **why**, and three
causes share the shape: genuinely multi-select forks, robustness refits, and
clustering artifacts. Sort by `rate` in the exhibit; the note explains how each
looks. V1, V3, V4 rank and do not decide.

The queues are ranked but **unread**. They are listed as open in the report
rather than reported as clean.

## What the adjudicating audits say

These three call a model rather than compute, and on the headline vocabulary
they agree: the repair chain improved the vocabulary and did not finish it.

**Do not read these at face value.** Two of the three partly measure the
repair chain's own cannot-link constraint, so a high number is expected rather
than alarming. The report's section on the repair chain works it through; the
short version:

| | |
|---|---|
| **lineage** | 27 of 30 pairs judged "one question" — but **17 of them co-occur**, meaning the repair refused to merge them on structural evidence the identity test cannot see. The real finding is the other **10, which were never adjudicated at all** |
| **G1** | screens 21 of 43 label-similar fork pairs and excludes 22 on co-occurrence — the same constraint, so not independent evidence. Narrower live concern: for the 43 multi-select forks of V2, co-occurrence does not imply distinctness |
| **granularity** | redundancy 0.990 on `.r3`. **This one is not circular**: it never uses co-occurrence |

The ten missed pairs trace to an ordering gap — `merge_forks` runs at repair
step 2 and `induce_forks` at step 4, so nothing merges forks after induction.
That is a pipeline fix, not an adjudication.
