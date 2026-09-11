# Acquiring a corpus for a second study

`scripts/fetch_corpus.py` fetches **this** study's corpora and nothing else. It
pins a repository, a commit, a sparse-checkout scope and an OSF node, and those
are provenance for the soccer study rather than configuration.

A second study writes its own fetcher. That is a normal amount of work, not a
gap in the design: acquiring a corpus is not a general operation. One corpus is
a pinned git repo with LFS, another an OSF archive, a third an institutional
download behind a login, a fourth a directory a colleague hands you on a drive.
No parameterisation covers those honestly.

What *is* general is the **contract** the result has to satisfy. Meet it however
you like — a script, a Makefile, a shell one-liner, or by hand.

---

## The contract

### 1 · A directory the glob matches

`study.json` names, per corpus, a `glob` matching **one run directory** relative
to the corpus root, and the `artifacts` inside it:

```json
"corpora": {
  "mystudy": {
    "env": "FORKSCOPE_RAW_MYSTUDY",
    "default": "data/raw/mystudy",
    "glob": "runs/*",
    "artifacts": {"code": "analysis.py", "prose": "report.md"}
  }
}
```

So the fetcher must produce:

```
<corpus root>/
  runs/
    run-001/  analysis.py  report.md
    run-002/  analysis.py  report.md
    ...
```

**Put the corpus outside the repository.** It is third-party material and
usually not yours to redistribute. `--dest ../corpus` is the convention here,
and the path reaches the pipeline through the `env` variable above.

### 2 · Artifacts that are present and non-empty

`distill.py` counts a run only when its artifacts exist and carry content. Two
failure modes look identical to a naive check and neither raises:

- **An unfetched Git-LFS pointer** is valid UTF-8, about 130 bytes, and reads as
  a file. It becomes a run with no analysis in it.
- **A truncated download** is a shorter file, not an error.

This is why the prose channel has a size floor rather than an existence check.
If your corpus has an analogous trap, guard it in the fetcher, not downstream.

### 3 · A checksum manifest

Naming a source and a commit says where the bytes came from. It does not say the
bytes you have are the bytes you read. Upstream gets re-tagged; partial pulls
look complete.

```bash
python3 scripts/fetch_corpus.py checksum --dest ../corpus   # writes CHECKSUMS.txt
python3 scripts/fetch_corpus.py verify   --dest ../corpus   # re-checks it
```

`checksum` and `verify` are the two subcommands that are **not** soccer-specific
— they walk whatever is on disk. Reuse them even if you replace `fetch`
entirely. A manifest turns "we used this corpus" into a claim someone else can
falsify, which is the whole point.

### 4 · A `MANIFEST.md` beside it

Record what was consumed and where to get it: source, version or commit, access
date, licence or terms, and anything you had to do by hand. Someone reproducing
your study three years from now has this file and nothing else.

---

## What not to automate

Some material should not be fetched by a script even when it technically could
be. In this study the human corpus is participant documents from a
human-subjects study; obtaining it is a decision a person takes against the
original study's terms.

`fetch_corpus.py` therefore tells you what is expected, checks what is present,
and verifies what you supply — but will not download it, and no flag changes
that. **Refusing to automate that step is the design, not an omission.** If your
corpus has a comparable boundary, put it in the same place.

---

## Checking your work

```bash
export FORKSCOPE_RAW_MYSTUDY=$(pwd)/../corpus/mystudy
FORKSCOPE_STUDY=my-study python3 scripts/paths.py          # what did it resolve?
FORKSCOPE_STUDY=my-study python3 scripts/distill.py all --limit 2
```

Two runs, not the corpus. If the glob matches nothing or an artifact is absent,
`distill.py` now **exits non-zero** and names the glob, the environment variable
and what to check — for the price of two model calls instead of two hundred.

An earlier version printed `0 run(s)` and exited 0, which meant a misconfigured
study looked like a clean build and the first sign of trouble was a plausible
number much further downstream. If you write your own fetcher, preserve that
property: **zero runs is never a success.**
