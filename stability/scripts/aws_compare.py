#!/usr/bin/env python3
"""Compare the induced vocabulary against the AWS fixed schema. No model calls.

READ THIS FIRST: THIS FILE IS NEVER AN INPUT
--------------------------------------------
`decisions_mapped.json` is the corpus authors' own extraction against a fixed
21-slot codebook. The pipeline never reads it -- doing so would import the
taxonomy this project exists to avoid, and `data/raw/inputs.json` enforces the
exclusion mechanically. It is read HERE, after the vocabulary exists, purely as
an independent comparison set. Nothing in this script feeds anything upstream.

THE CLAIM BEING TESTED
----------------------
If a vocabulary induced from the corpus, with no sight of their codebook,
independently recovers their slots, that is direct evidence the induction finds
real structure rather than artifacts of its own phrasing. Rediscovery is the
validation; the residue in both directions is diagnostic.

WHY THE COMPARISON IS STRUCTURAL, NOT LEXICAL
---------------------------------------------
Matching "skin_tone_operationalization" to "how is the skin-tone rating entered
as the exposure" by wording would be a weak test and would inherit every
problem lexical matching has caused elsewhere in this folder.

Both vocabularies instead PARTITION THE SAME RUNS. Their slot assigns each run
a `choice_made`; our fork assigns each run an option. Two decision points are
the same question to the extent those two partitions of the runs agree --
measured by adjusted Rand and normalised mutual information, exactly as builds
are compared to each other. No labels are read, so a slot and a fork that share
no vocabulary can still be matched.

WHAT THE RESIDUE MEANS, IN EACH DIRECTION
-----------------------------------------
  their slot, no fork of ours   either our induction missed a decision the
                                corpus contains, or their slot is a
                                distinction the corpus does not actually make.
                                Only tracing separates those.
  our fork, no slot of theirs   a decision a fixed schema could not hold. Their
                                own `unmapped_decisions` -- 1,120 items, 5.4
                                per run -- is the authors' record of the same
                                gap, and is the natural place to look for
                                confirmation.

Usage:
    python3 stability/scripts/aws_compare.py --vocab V.json --afp <corpus>/afp
        [--min-runs 10] [--json out] [--csv out]
"""
import argparse
import csv
import glob
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score

MODEL_DIR = "bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0"


def load_aws(afp):
    """{slot: {run: choice}} plus the unmapped list, from their extraction."""
    pat = os.path.join(afp, "experiment_data", "workspaces", "*", MODEL_DIR,
                       "sample_soccer", "*", "decisions_mapped.json")
    per = defaultdict(dict)
    unmapped = []
    runs = set()
    for f in glob.glob(pat):
        run = os.path.basename(os.path.dirname(f))
        runs.add(run)
        d = json.load(open(f, encoding="utf-8"))
        for cat, sl in (d.get("mapped_decisions") or {}).items():
            if not isinstance(sl, dict):
                continue
            for s, v in sl.items():
                if isinstance(v, dict) and v.get("choice_made"):
                    per[f"{cat}.{s}"][run] = str(v["choice_made"]).strip()
        for u in (d.get("unmapped_decisions") or []):
            txt = (u.get("description") or u.get("decision") or str(u)
                   if isinstance(u, dict) else str(u))
            unmapped.append({"run": run, "text": str(txt)})
    return dict(per), unmapped, runs


def load_ours(path):
    """{fork: {run: option}}. A run choosing twice at one fork keeps its modal
    choice -- the alternative is dropping the run, which would silently narrow
    the comparison to the forks that behave."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    per = defaultdict(lambda: defaultdict(Counter))
    for o in d["options"]:
        for m in o.get("members", ()):
            if 0 <= m < len(dec):
                per[o["fork"]][dec[m]["run"]][o["option"]] += 1
    return {f: {r: c.most_common(1)[0][0] for r, c in rr.items()}
            for f, rr in per.items()}


def ari(a, b, keys):
    return float(adjusted_rand_score([a[k] for k in keys], [b[k] for k in keys]))


def ami(a, b, keys):
    """Adjusted mutual information -- chance-corrected.

    Raw NMI is severely biased upward when the number of categories is large
    relative to the sample. With 13 shared runs and 12 distinct choices on one
    side, nearly every run lands in its own cell and NMI approaches 1 for any
    pair whatsoever. That is not a subtlety here: it produced a 0.73 "match"
    between the transformation slot and a fork about how the conclusion is
    worded, with an ARI of -0.02 on the same pair. AMI subtracts the expected
    MI under a permutation model and removes it.
    """
    return float(adjusted_mutual_info_score([a[k] for k in keys],
                                            [b[k] for k in keys]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vocab", required=True)
    ap.add_argument("--afp", required=True)
    ap.add_argument("--min-runs", type=int, default=30,
                    help="a slot or fork needs this many shared runs to be "
                         "comparable at all")
    ap.add_argument("--match", type=float, default=0.30,
                    help="AMI above which a slot counts as recovered")
    ap.add_argument("--json")
    ap.add_argument("--csv")
    x = ap.parse_args()

    aws, unmapped, aws_runs = load_aws(x.afp)
    ours = load_ours(x.vocab)
    # their extraction covers the AI corpus only
    ai_runs = aws_runs

    # a slot filled in one run is not a schema entry; it is an artifact
    slots = {s: v for s, v in aws.items() if len(v) >= x.min_runs}
    forks = {f: {r: o for r, o in v.items() if r in ai_runs}
             for f, v in ours.items()}
    forks = {f: v for f, v in forks.items() if len(v) >= x.min_runs}

    # A slot whose choice is the same in every run partitions nothing, and
    # neither does a fork whose runs all took one option. Two such partitions
    # score ARI = 1.0 against each other -- vacuously, since both are the
    # trivial one-cluster partition -- which is how the first version of this
    # comparison "recovered" five slots by matching them all to one unrelated
    # fork. NMI reports 0.0 for the same pair and is therefore the primary
    # statistic here; ARI is kept because it is comparable to the build-vs-build
    # numbers elsewhere, but it is not what decides a match.
    degenerate_slots = [s for s, v in slots.items()
                        if len(set(v.values())) < 2]
    slots = {s: v for s, v in slots.items() if len(set(v.values())) >= 2}
    forks = {f: v for f, v in forks.items() if len(set(v.values())) >= 2}

    rows, best_for_slot = [], {}
    for s, sv in slots.items():
        best = None
        for f, fv in forks.items():
            keys = sorted(set(sv) & set(fv))
            if len(keys) < x.min_runs:
                continue
            # both sides must still vary ON THE SHARED RUNS, not just overall
            if len({sv[k] for k in keys}) < 2 or len({fv[k] for k in keys}) < 2:
                continue
            a = ari(sv, fv, keys)
            m = ami(sv, fv, keys)
            if best is None or m > best["ami"]:
                best = {"slot": s, "fork": f, "ari": round(a, 4),
                        "ami": round(m, 4), "shared_runs": len(keys),
                        "their_choices": len({sv[k] for k in keys}),
                        "our_options": len({fv[k] for k in keys})}
        if best:
            rows.append(best)
            best_for_slot[s] = best

    matched = [r for r in rows if r["ami"] >= x.match]
    claimed_forks = {r["fork"] for r in matched}
    ours_unmatched = [f for f in forks if f not in claimed_forks]

    res = {
        "vocab": x.vocab, "note": "comparison only; never an input",
        "aws_runs": len(ai_runs),
        "aws_slots_declared": len(aws),
        "aws_slots_real": len(slots),
        "our_forks_comparable": len(forks),
        "match_threshold_ami": x.match,
        "degenerate_slots_excluded": degenerate_slots,
        "slots_recovered": len(matched),
        "recovery_rate": round(len(matched) / len(slots), 4) if slots else None,
        "our_forks_unmatched": len(ours_unmatched),
        "aws_unmapped_decisions": len(unmapped),
        "per_slot": sorted(rows, key=lambda r: -r["ami"]),
    }

    print(f"INDUCED VOCABULARY vs THE AWS FIXED SCHEMA\n")
    print(f"  their runs                      {len(ai_runs)}")
    print(f"  their slots declared            {len(aws)}")
    print(f"  their slots actually used       {len(slots)}  "
          f"(filled in >= {x.min_runs} runs)")
    print(f"  our forks comparable            {len(forks)}  "
          f"(reached by >= {x.min_runs} of their runs)\n")
    print(f"  REDISCOVERY: {len(matched)} of {len(slots)} slots recovered "
          f"at ARI >= {x.match}\n")
    print(f"    {'ARI':>6}{"AMI":>7}{'runs':>6}{'their':>7}{'ours':>6}  "
          f"slot  ->  our fork")
    for r in res["per_slot"]:
        mark = "OK" if r["ami"] >= x.match else "  "
        print(f"    {r['ari']:>6}{r["ami"]:>7}{r['shared_runs']:>6}"
              f"{r['their_choices']:>7}{r['our_options']:>6} {mark} "
              f"{r['slot']}")
        print(f"    {'':>32}    -> {r['fork'][:74]}")
    print(f"\n  RESIDUE")
    print(f"    our forks with no slot        {len(ours_unmatched)} of "
          f"{len(forks)}")
    print(f"    their unmapped_decisions      {len(unmapped)} "
          f"({len(unmapped)/max(len(ai_runs),1):.1f} per run)")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        res["our_forks_unmatched_list"] = ours_unmatched
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")
    if x.csv and rows:
        Path(x.csv).parent.mkdir(parents=True, exist_ok=True)
        with open(x.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(res["per_slot"])
        print(f"  wrote {x.csv}")


if __name__ == "__main__":
    main()
