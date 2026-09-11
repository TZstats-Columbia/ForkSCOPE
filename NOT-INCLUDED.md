# What is not in this repository

Everything downstream of the two source corpora is committed. Four things are
not, and each is named here so that its absence is a stated decision rather
than a gap.

## The two source corpora

Neither is ours to redistribute. [`data/raw/MANIFEST.md`](data/raw/MANIFEST.md)
records exactly what was consumed and where to get it, and
[`data/raw/CHECKSUMS.txt`](data/raw/CHECKSUMS.txt) records a SHA-256 for each
of the 697 artifacts the pipeline reads, so `fetch_corpus.py verify` can confirm
that a fetched copy is the one the results rest on.

| corpus | source | how |
|---|---|---|
| agentic, 207 runs | `amazon-science/agentic-forking-path`, pinned at `d489f03` | `python3 scripts/fetch_corpus.py fetch --dest ../corpus` |
| soccer dataset | OSF node `c9mkx` | fetched with the above |
| human, 31 teams | Silberzahn et al. 2018, *Many analysts, one data set*, the team directories on OSF | acquired by the reader under the original study's terms |

Only stage 1 (distillation) reads them. Every later stage runs from
`data/distilled/` and the cache.

## The replicate builds

The stability measurements of the paper's section 6 compare the committed build
against builds made under separate study roots with empty caches: a
distillation replicate (`B-distill`), a vocabulary replicate (`B-vocab`), and
ten fork-formation replicates over frozen options (`A1`–`A5`, `B1`–`B5`). Those
roots, with their vocabularies and their own model-response caches, are not
included. What is included is what the paper reads from:

- [`replicates/`](replicates/) — the manifest of each fork-formation replicate
  and, in `results/`, the variance decomposition (`fork_variance.json`);
- [`stability/data/`](stability/data/) — every cross-build comparison, each
  recording which build it compared against;
- [`stability/results/human_benchmark.json`](stability/results/human_benchmark.json)
  — the scored human benchmark.

`stability/scripts/fork_variance.py` recomputes the decomposition from a
replicate root, and `stability/scripts/replicate.py` builds one.

## The pilot build over the agentic corpus alone

The supplement's pinned-model cross-check (§S7) comes from a separate pilot
build over the agentic corpus alone, exploring an agent-driven review workflow
that is out of scope for the paper. That build is not included; its figures are
reported in the supplement as recorded.

## The corpus authors' codebook, and the comparison against it

The agentic corpus ships with `decisions_mapped.json`, the corpus authors' own
extraction of each run's decisions against their fixed 21-slot schema. ForkSCOPE
never reads it as input: the exclusion is enforced in
[`data/raw/inputs.json`](data/raw/inputs.json), the study manifest names only
the script and the report as artifacts, and no cached model call saw it. It was
used only as a comparison target once the induced vocabulary existed.

Two comparisons were made (supplement §S11).

- **The structural comparison** is included:
  [`stability/data/aws_compare.json`](stability/data/aws_compare.json), computed
  by `stability/scripts/aws_compare.py` against a fetched copy of the corpus.
  It reads no labels, only which runs each slot and each fork partition.
- **The node-for-node adjudication** is not included. Its inputs are reshaped
  copies of the corpus authors' file, which belong with the corpus rather than
  here, and its outputs are derived from them. The supplement reports its
  figures as recorded and marks them accordingly.
