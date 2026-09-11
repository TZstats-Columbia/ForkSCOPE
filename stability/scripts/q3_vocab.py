#!/usr/bin/env python3
"""Q3 -- vocabulary stability at the option and fork levels. No model calls.

Wraps `partition.py` to report both levels together, and -- this is the part
that matters -- decides and states what KIND of comparison it just ran.

REPLICATE VS SCOPE CHANGE
-------------------------
Two vocabulary builds can differ for two unrelated reasons:

  REPLICATE     same corpora, same code, model called again. Every difference
                is run-to-run variability. This is stability.
  SCOPE CHANGE  different corpora pooled. Differences confound variability with
                the effect of adding or removing a corpus. This is NOT
                stability, however similar the numbers look.

The distinction is invisible in the output files -- both are just
`bottom_up_<tag>.json` -- and conflating them is the specific error this whole
folder exists to avoid. So the corpora lists are read from the vocabulary
headers and compared, and the verdict is written into the result rather than
left to whoever reads it.

WHY BOTH LEVELS
---------------
Options and forks can move independently, and the pipeline treats them
asymmetrically: options merge on "same action", forks on "same purpose"
(foreclosure). A build can be stable at the option level and unstable at the
fork level, which would say the concrete choices are recovered reliably but
their grouping into rival slots is not -- a very different finding from the
reverse, and one that points at prompt 22 rather than prompt 19.

Usage:
    python3 stability/scripts/q3_vocab.py --a <vocabA.json> --b <vocabB.json>
                                          [--json out.json]
"""
import argparse
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import partition as P                                          # noqa: E402


def header(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"corpora": sorted(d.get("corpora", [])),
            "n_runs": d.get("n_runs"), "n_decisions": d.get("n_decisions"),
            "n_options": d.get("n_options"), "n_forks": d.get("n_forks")}


def classify(ha, hb):
    """What kind of comparison is this, and is the stability reading valid?"""
    if ha["corpora"] != hb["corpora"]:
        return ("scope_change",
                f"corpora differ ({'+'.join(ha['corpora'])} vs "
                f"{'+'.join(hb['corpora'])}); differences confound run-to-run "
                f"variability with the effect of corpus scope. NOT a stability "
                f"measurement.")
    if ha["n_decisions"] != hb["n_decisions"]:
        return ("input_change",
                f"same corpora but different decision counts "
                f"({ha['n_decisions']} vs {hb['n_decisions']}); distillation "
                f"differs, so this is not a clean vocabulary replicate.")
    return ("replicate",
            "same corpora and same distilled input; differences are "
            "run-to-run variability in the vocabulary induction.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--json")
    x = ap.parse_args()

    ha, hb = header(x.a), header(x.b)
    kind, why = classify(ha, hb)

    res = {"comparison_type": kind, "interpretation": why,
           "header_a": ha, "header_b": hb, "levels": {}}
    for level in ("option", "fork"):
        res["levels"][level] = P.compare(x.a, x.b, level)

    banner = {"replicate": "REPLICATE  (valid stability measurement)",
              "scope_change": "SCOPE CHANGE  (NOT a stability measurement)",
              "input_change": "INPUT CHANGE  (not a clean replicate)"}[kind]
    print(f"Q3  VOCABULARY STABILITY -- {banner}")
    print(f"    {why}\n")
    print(f"    {'':<22}{'A':>14}{'B':>14}")
    for f in ("corpora", "n_runs", "n_decisions", "n_options", "n_forks"):
        a = "+".join(ha[f]) if f == "corpora" else ha[f]
        b = "+".join(hb[f]) if f == "corpora" else hb[f]
        print(f"    {f:<22}{str(a):>14}{str(b):>14}")

    for level, r in res["levels"].items():
        print(f"\n    --- {level.upper()} level "
              f"({r['shared']} shared instances) ---")
        for k in ("ari", "vi_bits", "vi_normalised", "bcubed_precision",
                  "bcubed_recall", "bcubed_f1", "direction",
                  "clusters_a", "clusters_b", "stable_clusters",
                  "split_clusters", "split_instances",
                  "merge_clusters", "merge_instances"):
            print(f"    {k:<22} {r[k]}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n    wrote {x.json}")


if __name__ == "__main__":
    main()
