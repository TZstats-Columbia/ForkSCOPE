#!/usr/bin/env python3
"""Q2 -- stability of the code/prose alignment judge (gate 5.4). No model calls.

This is the ONE place in the pipeline where two genuine replicates already
exist. Prompt 16 (`align_channels`) was called twice on an identical 80-run
sample with identical inputs -- same 1,363 code decisions, same 3,329 prose
spans -- five days apart. Nothing about the corpus, the code, or the prompt
changed between them, so every difference is run-to-run variability in the
model's judgement.

WHAT IS COMPARED
----------------
Each run of the judge emits, per code decision it could match, a partner prose
span and a verdict in {same_option, same_fork_different_option, vaguer}. Two
independent things can therefore move, and they mean different things:

  PARTNER   which prose span the decision was matched to. A change here is a
            matching difference -- the judge found a different sentence.
  VERDICT   how the pair was scored. A change here is a severity difference --
            the same pair judged more or less strictly.

Reporting one agreement number would fuse them. A judge that always picks the
same partner but grades it differently is a calibration problem; a judge that
picks different partners is a retrieval problem, and they have different fixes.

THE DENOMINATOR MATTERS
-----------------------
Agreement among decisions matched by BOTH runs flatters the result, because it
conditions on the easy cases. The honest denominator is the union: every code
decision either run managed to match. Both are reported, and the union figure
is the headline.

Output includes a stratified sample of disagreements for human adjudication,
because whether these are edge cases is a question about content that no
summary statistic answers.

Usage:
    python3 stability/scripts/q2_ablation.py --a <matchesA.json> --b <matchesB.json>
        [--json out.json] [--sample-csv out.csv] [--sample-n 40]
"""
import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

SEED = 20260822


def load_pairs(path):
    """{(run, code_id): (prose_id, verdict, why)} plus per-run totals."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    pairs, totals = {}, {}
    for r in d["results"]:
        run = r["run"]
        totals[run] = {"n_code": r.get("n_code", 0),
                       "n_prose": r.get("n_prose", 0),
                       "flipped": r.get("flipped")}
        for p in r.get("pairs", ()):
            pairs[(run, str(p["code_id"]))] = (
                str(p["prose_id"]), p["verdict"], p.get("why", ""))
    return pairs, totals, d


def compare(pa, pb):
    ka, kb = set(pa), set(pb)
    both, only_a, only_b = ka & kb, ka - kb, kb - ka
    union = ka | kb

    same_all = same_partner_diff_verdict = 0
    diff_partner_same_verdict = diff_both = 0
    transitions = Counter()
    disagreements = []

    for k in sorted(both):
        prose_a, v_a, why_a = pa[k]
        prose_b, v_b, why_b = pb[k]
        p_same, v_same = prose_a == prose_b, v_a == v_b
        if p_same and v_same:
            same_all += 1
            continue
        if p_same:
            same_partner_diff_verdict += 1
            kind = "verdict_only"
        elif v_same:
            diff_partner_same_verdict += 1
            kind = "partner_only"
        else:
            diff_both += 1
            kind = "partner_and_verdict"
        if not v_same:
            transitions[f"{v_a} -> {v_b}"] += 1
        disagreements.append({
            "run": k[0], "code_id": k[1], "kind": kind,
            "prose_a": prose_a, "verdict_a": v_a, "why_a": why_a,
            "prose_b": prose_b, "verdict_b": v_b, "why_b": why_b})

    for k in sorted(only_a):
        prose_a, v_a, why_a = pa[k]
        disagreements.append({
            "run": k[0], "code_id": k[1], "kind": "matched_only_in_A",
            "prose_a": prose_a, "verdict_a": v_a, "why_a": why_a,
            "prose_b": "", "verdict_b": "", "why_b": ""})
    for k in sorted(only_b):
        prose_b, v_b, why_b = pb[k]
        disagreements.append({
            "run": k[0], "code_id": k[1], "kind": "matched_only_in_B",
            "prose_a": "", "verdict_a": "", "why_a": "",
            "prose_b": prose_b, "verdict_b": v_b, "why_b": why_b})

    res = {
        "matched_a": len(ka), "matched_b": len(kb),
        "matched_both": len(both), "matched_union": len(union),
        "only_a": len(only_a), "only_b": len(only_b),
        "identical": same_all,
        "same_partner_diff_verdict": same_partner_diff_verdict,
        "diff_partner_same_verdict": diff_partner_same_verdict,
        "diff_partner_and_verdict": diff_both,
        # Conditioned on both -- flattering, reported for comparability.
        "agreement_given_both": round(same_all / len(both), 4) if both else 0,
        # The honest one: of everything either run matched, how much is stable.
        "stability_over_union": round(same_all / len(union), 4) if union else 0,
        "verdict_transitions": dict(transitions.most_common()),
    }
    return res, disagreements


def verdict_mix(pairs):
    return dict(Counter(v for _, v, _ in pairs.values()).most_common())


def stratified_sample(disagreements, n, seed=SEED):
    """Even draw across disagreement kinds, so the rare ones are represented.

    A uniform draw would return mostly whichever kind is most common and tell a
    reviewer nothing about the others. Kinds are the stratum because they are
    what a reviewer adjudicates differently.
    """
    rng = random.Random(seed)
    by = defaultdict(list)
    for d in disagreements:
        by[d["kind"]].append(d)
    kinds = sorted(by)
    per = max(1, n // max(1, len(kinds)))
    out = []
    for k in kinds:
        rows = sorted(by[k], key=lambda r: (r["run"], r["code_id"]))
        out.extend(rows if len(rows) <= per else rng.sample(rows, per))
    return sorted(out, key=lambda r: (r["kind"], r["run"], r["code_id"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True, help="build A matches.json")
    ap.add_argument("--b", required=True, help="build B matches.json")
    ap.add_argument("--json")
    ap.add_argument("--sample-csv")
    ap.add_argument("--sample-n", type=int, default=40)
    x = ap.parse_args()

    pa, ta, da = load_pairs(x.a)
    pb, tb, db = load_pairs(x.b)

    runs_a, runs_b = set(ta), set(tb)
    if runs_a != runs_b:
        print(f"  WARNING: run samples differ "
              f"({len(runs_a - runs_b)} only in A, {len(runs_b - runs_a)} only in B)")
        print("  These builds are not replicates of one another; "
              "differences below confound sample and judgement.\n")
    code_a = sum(v["n_code"] for v in ta.values())
    code_b = sum(v["n_code"] for v in tb.values())

    res, dis = compare(pa, pb)
    # Provenance first: a stability number with no record of which builds it
    # compares is not interpretable. Check S6 enforces this.
    res["build_a"], res["build_b"] = x.a, x.b
    res["comparison_type"] = ("replicate" if code_a == code_b and runs_a == runs_b
                              else "input_change")
    res["runs"] = len(runs_a)
    res["identical_run_sample"] = runs_a == runs_b
    res["n_code_a"], res["n_code_b"] = code_a, code_b
    res["identical_code_inputs"] = code_a == code_b
    res["verdict_mix_a"] = verdict_mix(pa)
    res["verdict_mix_b"] = verdict_mix(pb)

    print(f"Q2  ABLATION JUDGE STABILITY")
    print(f"    runs {len(runs_a)}, code decisions "
          f"{code_a} vs {code_b}"
          f"{'  (identical inputs)' if code_a == code_b else '  (DIFFERENT)'}\n")
    order = ["matched_a", "matched_b", "matched_both", "matched_union",
             "only_a", "only_b", "identical", "same_partner_diff_verdict",
             "diff_partner_same_verdict", "diff_partner_and_verdict",
             "agreement_given_both", "stability_over_union"]
    for k in order:
        print(f"    {k:<28} {res[k]}")
    print("\n    verdict transitions (A -> B):")
    for k, v in res["verdict_transitions"].items():
        print(f"      {v:>4}  {k}")
    print("\n    verdict mix:")
    for name, mix in (("A", res["verdict_mix_a"]), ("B", res["verdict_mix_b"])):
        print(f"      {name}: {mix}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n    wrote {x.json}")
    if x.sample_csv:
        rows = stratified_sample(dis, x.sample_n)
        Path(x.sample_csv).parent.mkdir(parents=True, exist_ok=True)
        with open(x.sample_csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]) + ["reviewer_verdict",
                                                              "reviewer_note"])
            w.writeheader()
            for r in rows:
                w.writerow({**r, "reviewer_verdict": "", "reviewer_note": ""})
        print(f"    wrote {x.sample_csv}  ({len(rows)} rows, "
              f"{len(dis)} disagreements total)")


if __name__ == "__main__":
    main()
