# templates/ — starting a second study

The pipeline is the instrument and it is shared. A study is a corpus plus the
data derived from it, and it declares itself in one file.

```bash
mkdir -p studies/my-study/data/raw
cp templates/study.json  studies/my-study/study.json
cp templates/policy.json studies/my-study/policy.json
$EDITOR studies/my-study/study.json
export FORKSCOPE_STUDY=my-study
python3 scripts/paths.py            # prints what it resolved
```

`scripts/` and `prompts/` stay where they are. That is not a convenience — the
claim a second study supports is that **the instrument was unchanged**, and a
per-study copy of the pipeline would forfeit it.

## The three files, and the one that does the work

| file | what it declares |
|---|---|
| `study.json` | what the corpus **is** — where runs live, what artifacts they hold, and the `context` block that carries your domain to the model |
| `policy.json` | how charting **works** — the method decisions, each marked *decided*, *defaulted* or *unknown* |
| `INTAKE.md` | what was **asked**, what was answered, and what was not known at the time |

**`study.json:context` is the mechanism that makes the instrument shared.** Your
glossary, your conventions that are not decisions, and the choices a
non-specialist would skim past all reach the model as *data appended to a fixed
prompt*. Prompt text is never edited per study, which is why `prompt_hash` is
identical across studies and the shared-instrument claim is checkable rather
than asserted. A study that omits `context` still runs, and extracts worse,
silently — so fill it in even when it feels obvious.

`/intake` writes all three by interview and is the better route: it asks in an
order that surfaces what you do not know yet, and it records the difference
between a value you chose and one you accepted without comment.

## Getting the corpus

`scripts/fetch_corpus.py` fetches **this** study's corpora and is the only
script that is study-specific. A second study writes its own, against the
contract in [`fetch_corpus.md`](fetch_corpus.md): a directory the `glob`
matches, artifacts that are present and non-empty, a checksum manifest, and a
`MANIFEST.md` recording what was consumed.

## You do not empty the soccer study

The obvious way to start over — delete `data/`, blank `figures/`, clear
`reviews/` — is the wrong one, and the package is built so you never have to.
`FORKSCOPE_STUDY` redirects everything study-scoped to a new root, and the
soccer study stays where it is as the worked example. That example is most of
what the package is *for*: it is the only place to see what a filled `study.json`,
a real review round, and a finished report actually look like.

Emptying also has no safe stopping point. Half-cleared state is
indistinguishable from a build that failed midway, and the failure is silent —
a stale `figures/circle.html` beside new data renders without error and shows
the previous study's garden.

**Study-scoped**, and created for you by `paths.py:ensure_dirs()`:

    data/  figures/  cache/  reviews/  replicates/  report/

**Code-scoped**, shared by every study, never copied:

    scripts/  prompts/  stability/scripts/  templates/  docs/

The seam runs *through* `stability/`: the replicate machinery is instrument, the
replicates it produces are material. They lived in one directory until the
soccer replicates made the distinction concrete.

## What to fill in

| field | |
|---|---|
| `study` | short name, used in output |
| `question` | what every analyst in the corpus was asked. It is the thing that makes forks comparable *within* a study and not across one |
| `corpora` | one entry per source of runs. `glob` matches **one run**, relative to the corpus root; `artifacts` names the code and prose file inside it |
| `final_tag` | leave as `CHANGE-ME` until the repair chain has run — you cannot know it in advance |
| `outcomes` | omit the block if there is no outcome side. Better absent than pointing at a file that does not exist |

## `final_tag` comes last

The tag records lineage — `ai+human.merged.forkmerged.merged.induced.r3` reads as
pooled, options collapsed, forks merged, options collapsed again, forks
re-induced. Which stages a study needs depends on what its clustering does, and
that is not knowable before running it. Build, read `compare_vocab.py`, then
write the tag you settled on.

A study whose `study.json` is missing is an error rather than a fallback: it
would otherwise inherit another study's tag and report numbers that look fine.

## Two gardens, not one pooled garden

Different dataset, different question, so the forks are not comparable and the
vocabularies must not be pooled. `ai` and `human` are corpora *within* the
soccer study, answering the same question about the same data; a second study
is a different axis.

What compares across studies is the **shape** — is the space a fan there too,
is disagreement concentrated in operationalisation, do choices predict the
answer — and the fact that the same instrument produced both.

## What a new study needs beyond the manifest

- **Raw material** reachable at the `env` path, one directory per run.
- **An outcome side, or none.** Soccer's `outcomes.json` was assembled outside
  the pipeline and has no generator; 52 of its 207 records have no provenance
  (`scripts/check_outcomes.py`). If your study needs outcomes, write the
  extractor as a pipeline stage the first time rather than assembling per run.
- **Nothing else.** No new prompts, no new scripts. If a study needs either,
  that is a finding about the instrument, and it should be recorded as one.
