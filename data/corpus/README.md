# corpus/ — the flat view

Four TSVs and a summary. This is the extraction layer from
[`../distilled/`](../distilled/) flattened into tables you can open in a
spreadsheet or `awk`. Nothing here is clustered — for the garden, see
[`../vocabulary/`](../vocabulary/).

All five are written by `distill.py index`.

| file | one row per | columns |
|---|---|---|
| `coverage.tsv` | run | `run_id`, `corpus`, `arm`, `code_lines`, `exon_share`, `decisions`, `claims`, `links`, `silent`, `misaligned` |
| `by_arm.tsv` | persona arm | `arm`, `runs`, `decisions`, `silent`, `silent_per_decision`, `misaligned`, `misaligned_per_run` |
| `silent_decisions.tsv` | silent decision | `run_id`, `arm`, `lines`, `confidence`, `operation` |
| `misalignments.tsv` | misalignment | `run_id`, `arm`, `note`, `code_operation`, `prose_claim` |
| `index.md` | — | generated summary of the distillation run |

`exon_share` is the fraction of script lines that carry an analytic decision;
the rest are typed introns (imports, printing, comments). A low share is not a
defect — most of a script is plumbing.

`misalignments.tsv` is the most directly readable evidence in the repository:
each row is a place where a script and its write-up disagree about what was
done — a 0.75 versus 0.625 cutpoint, logit versus probit, one-sided versus
two-sided *p*.

```bash
# decisions per run, by arm
awk -F'\t' 'NR>1{n[$3]++; d[$3]+=$6} END{for(a in n) printf "%-28s %3d runs  %5.1f decisions\n", a, n[a], d[a]/n[a]}' coverage.tsv

# every disagreement between code and prose
column -t -s$'\t' misalignments.tsv | less -S
```

Silent decisions and misalignments are the *residue of an alignment* rather
than something searched for directly. Corpus-wide rollups with categories live
in `../analysis/silent.json` and `../analysis/misaligned.json`.
