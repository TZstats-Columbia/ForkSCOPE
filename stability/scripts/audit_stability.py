#!/usr/bin/env python3
"""S1-S6 -- stability checks, and the over/under-merge signal. No model calls.

Every other audit family in this project asks whether ONE build is internally
sound. This one asks whether the build would come back the same, which no
single-build check can see. It is the audit companion for the stability
measurement, and it follows the same rule as the rest: a check that cannot fail
is not evidence, so each one names the failure it rules out.

THE MERGE SIGNAL
----------------
The motivating idea is that an unstable merge is a suspect merge. If build A
puts two decisions in one option and build B does not, the pipeline has
answered "are these the same action?" both ways -- which is exactly the
evidence a human review round wants, and it is free once two builds exist.

The response follows the project's existing asymmetry: over-merge is invisible
and unrecoverable, under-merge is visible and fixable. So an unstable pair
defaults to UNMERGED and is routed to review, rather than resolved by majority.
Majority vote would silently keep 2-of-3 merges, which is precisely the
over-merge the rule exists to avoid.

CALIBRATION, NOT THRESHOLD-FITTING
----------------------------------
Thresholds below are set from the first replicate and stated as such. They are
not tuned until checks pass -- that would manufacture the result, and the
project's own auditing guidance names it as the failure to avoid. Where no
replicate has been run yet, the check reports NOT RUN rather than inventing a
verdict.

Usage:
    python3 stability/scripts/audit_stability.py --dir stability/data [--json out]
"""
import argparse
import json
from pathlib import Path

# Set from the first pooled replicate.
# Raising one of these to make a check pass is threshold-fitting; change the
# build instead, or report the failure.
T = {
    "option_ari": 0.85,      # below this, option clustering is not reproducible
    "fork_ari": 0.75,        # forks are harder: purpose is a weaker constraint
    "bcubed_f1": 0.80,
    # Distillation, decision layer. The threshold encodes a DECISION -- may a
    # later stage reuse cached distillation without that reuse being an
    # unexamined assumption? -- not the observed value. Set once, at the level
    # where the answer would change, and not moved to make a check pass.
    "decision_lenient_f1": 0.70,
    "judge_union": 0.75,     # ablation judge, honest denominator
    "traffic_rho": 0.85,     # highways: do busy routes stay busy
    # Residues (silent decisions, misalignments). Same rule, different claim:
    # above this they may be quoted as point estimates; below it they must
    # carry uncertainty, because a second build would have found a materially
    # different set.
    "residue_f1": 0.70,
}


def load(d, name):
    p = Path(d) / name
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def verdict(ok):
    return "PASS" if ok else "REVIEW"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dir", default="stability/data")
    ap.add_argument("--json")
    x = ap.parse_args()
    d = Path(x.dir)
    res, notrun = {}, []

    print("STABILITY AUDIT  (S1-S6)\n")

    # ---- S1 distillation ---------------------------------------------------
    q1 = load(d, "q1_distill.json")
    if q1 and q1.get("decisions"):
        dd = q1["decisions"]
        lf, cf = dd["lenient"]["f1"], dd["core"]["f1"]
        vf = dd["verbatim"]["f1"]
        ok = lf >= T["decision_lenient_f1"]
        res["S1"] = {"verdict": verdict(ok), "runs": q1["runs_compared"],
                     "verbatim_f1": vf, "lenient_f1": lf, "core_f1": cf,
                     "jitter_share": dd["jitter_share"],
                     "median_boundary_jitter_lines":
                         dd["median_boundary_jitter_lines"],
                     "prose_group_ari": q1.get("prose_group_ari_mean")}
        print(f"S1  DISTILLATION, DECISION LAYER                       {verdict(ok)}")
        print(f"    runs compared                 {q1['runs_compared']}")
        print(f"    verbatim F1                   {vf}   (identical line sets)")
        print(f"    lenient  F1                   {lf}   (floor "
              f"{T['decision_lenient_f1']}) <- the decision rule")
        print(f"    core     F1                   {cf}   (upper bound)")
        print(f"    jitter share / median lines   {dd['jitter_share']} / "
              f"{dd['median_boundary_jitter_lines']}")
        print(f"    prose channel ARI             {q1.get('prose_group_ari_mean')}")
        print(f"    -> the verbatim/lenient gap is the measurement: a strict")
        print(f"       score charges a one-line boundary shift almost as")
        print(f"       heavily as a missed decision\n")
    else:
        res["S1"] = {"verdict": "NOT RUN"}
        notrun.append("S1")
        print("S1  DISTILLATION, DECISION LAYER                       NOT RUN")
        print("    needs a distillation replicate (replicate.py --stage distill)\n")

    # ---- S2/S3 vocabulary --------------------------------------------------
    # Pick the replicate comparison of the FINAL vocabulary, not whichever
    # sorts first. Both the base and the repaired comparison are legitimate
    # replicates, but the base one describes a vocabulary no result is ever
    # reported from -- auditing it would understate reproducibility by the
    # entire contribution of the repair chain. Prefer the deepest tag; fall
    # back to any replicate so the check still runs before repair exists.
    q3 = None
    cands = []
    for f in sorted(d.glob("q3_*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        if c.get("comparison_type") != "replicate":
            continue
        # tag depth = number of repair passes applied
        depth = str(c.get("header_a", {}).get("n_forks", "")) and \
            c["levels"]["option"]["build_a"].count(".")
        cands.append((depth, f.name, c))
    if cands:
        cands.sort(key=lambda t: (t[0], t[1]))
        q3 = cands[-1][2]
        if len(cands) > 1:
            print(f"    [auditing {cands[-1][1]}; "
                  f"{len(cands) - 1} earlier-stage replicate(s) present]\n")
    if q3:
        o, k = q3["levels"]["option"], q3["levels"]["fork"]
        for tag, lvl, key, label in (("S2", o, "option_ari", "OPTION"),
                                     ("S3", k, "fork_ari", "FORK")):
            ok = lvl["ari"] >= T[key] and lvl["bcubed_f1"] >= T["bcubed_f1"]
            res[tag] = {"verdict": verdict(ok), "ari": lvl["ari"],
                        "bcubed_f1": lvl["bcubed_f1"],
                        "direction": lvl["direction"]}
            print(f"{tag}  {label}-LEVEL REPRODUCIBILITY"
                  f"{'':<{max(0, 30 - len(label))}}{verdict(ok)}")
            print(f"    ARI                           {lvl['ari']}  "
                  f"(floor {T[key]})")
            print(f"    B-cubed F1                    {lvl['bcubed_f1']}  "
                  f"(floor {T['bcubed_f1']})")
            print(f"    direction                     {lvl['direction']}")
            print(f"    stable / split / merged       {lvl['stable_clusters']} / "
                  f"{lvl['split_clusters']} / {lvl['merge_clusters']}\n")
    else:
        for tag, label in (("S2", "OPTION"), ("S3", "FORK")):
            res[tag] = {"verdict": "NOT RUN"}
            notrun.append(tag)
            print(f"{tag}  {label}-LEVEL REPRODUCIBILITY"
                  f"{'':<{max(0, 30 - len(label))}}NOT RUN")
        print("    no q3_*.json with comparison_type == 'replicate'.")
        print("    A scope comparison is present but does NOT substitute: it")
        print("    confounds run-to-run variability with corpus scope.\n")

    # ---- S4 unstable merges ------------------------------------------------
    if q3:
        o = q3["levels"]["option"]
        unstable = o["split_clusters"] + o["merge_clusters"]
        rate = unstable / max(1, o["clusters_a"])
        ok = rate <= 0.20
        res["S4"] = {"verdict": verdict(ok), "unstable_clusters": unstable,
                     "unstable_rate": round(rate, 4),
                     "action": "unstable pairs default to UNMERGED; route to review"}
        print(f"S4  UNSTABLE MERGES                                    {verdict(ok)}")
        print(f"    clusters that moved           {unstable} / {o['clusters_a']}"
              f"  ({rate:.1%})")
        print(f"    -> an option the pipeline groups one way and then another is")
        print(f"       a disputed merge. Default to UNMERGED and route to a")
        print(f"       review round; majority vote would silently keep 2-of-3")
        print(f"       merges, which is the over-merge the rule exists to avoid\n")
    else:
        res["S4"] = {"verdict": "NOT RUN"}
        notrun.append("S4")
        print("S4  UNSTABLE MERGES                                    NOT RUN\n")

    # ---- S5 judge stability ------------------------------------------------
    q2 = load(d, "q2_ablation.json")
    if q2:
        v = q2["stability_over_union"]
        ok = v >= T["judge_union"]
        drift = {k: val for k, val in q2["verdict_transitions"].items()}
        res["S5"] = {"verdict": verdict(ok), "stability_over_union": v,
                     "agreement_given_both": q2["agreement_given_both"],
                     "transitions": drift}
        print(f"S5  ALIGNMENT-JUDGE STABILITY                          {verdict(ok)}")
        print(f"    stability over union          {v}  (floor {T['judge_union']})")
        print(f"    agreement given both matched  {q2['agreement_given_both']}")
        print(f"    inputs identical              {q2.get('identical_code_inputs')}")
        for kk, vv in list(drift.items())[:4]:
            print(f"      {vv:>4}  {kk}")
        print(f"    -> asymmetric transitions indicate a severity shift in the")
        print(f"       judge, not symmetric noise\n")
    else:
        res["S5"] = {"verdict": "NOT RUN"}
        notrun.append("S5")
        print("S5  ALIGNMENT-JUDGE STABILITY                          NOT RUN\n")

    # ---- S6 provenance -----------------------------------------------------
    q4 = None
    for f in sorted(d.glob("q4_*.json")):
        q4 = json.loads(f.read_text(encoding="utf-8"))
    missing = []
    for f in sorted(d.glob("*.json")):
        # The audit's own report is a verdict sheet, not a comparison result;
        # scanning it would flag this check for failing to satisfy itself.
        if f.name.startswith("audit_"):
            continue
        c = json.loads(f.read_text(encoding="utf-8"))
        if isinstance(c, dict) and not any(
                k in c for k in ("corpus_a", "header_a", "build_a", "runs_compared")):
            missing.append(f.name)
    ok = not missing
    res["S6"] = {"verdict": verdict(ok), "results_without_provenance": missing}
    print(f"S6  RESULT PROVENANCE                                  {verdict(ok)}")
    print(f"    results lacking a build/corpus tag   {len(missing)}")
    if missing:
        print(f"      {', '.join(missing)}")
    print(f"    -> a stability number with no record of WHICH builds it")
    print(f"       compares is not interpretable; figures carry no tag at all")
    print(f"       (see the figure-provenance hazard)\n")

    if q4:
        print(f"    [context] highway traffic Spearman {q4.get('traffic_spearman')}"
              f" over {q4.get('edges_overlapping')} overlapping dyads")
        print(f"              persona enrichments reproduced "
              f"{q4.get('enriched_reproduced')}/{q4.get('enriched_a')}\n")

    # ---- S7 residue stability ----------------------------------------------
    sem = load(d, "q1c_semantic.json")
    q1b = load(d, "q1b_residue.json")
    if sem:
        f = sem["f1"]
        ok = f >= T["residue_f1"]
        res["S7"] = {"verdict": verdict(ok), "semantic_f1": f,
                     "n_a": sem["n_a"], "n_b": sem["n_b"],
                     "matched": sem["matched_semantic"],
                     "structural_f1": (q1b or {}).get("silent_decisions", {})
                                                  .get("f1_core"),
                     "flipped_fraction": sem.get("flipped_fraction"),
                     "action": ("quote residue counts with uncertainty, not as "
                                "point estimates")}
        print(f"S7  RESIDUE STABILITY  (silent decisions)              {verdict(ok)}")
        print(f"    semantically adjudicated F1   {f}  (floor "
              f"{T['residue_f1']})")
        print(f"    structural (core) F1          "
              f"{res['S7']['structural_f1']}")
        print(f"    silent decisions              {sem['n_a']} in A, "
              f"{sem['n_b']} in B, {sem['matched_semantic']} same")
        print(f"    blinding: flipped fraction    {sem.get('flipped_fraction')}"
              f"  (0.35-0.65 acceptable)")
        print(f"    -> semantic adjudication does NOT rescue the structural")
        print(f"       figure. The two builds flag DIFFERENT operations as")
        print(f"       unmentioned; this is not boundary jitter.\n")
    else:
        res["S7"] = {"verdict": "NOT RUN"}
        notrun.append("S7")
        print("S7  RESIDUE STABILITY                                  NOT RUN\n")

    bad = [k for k, v in res.items() if v.get("verdict") == "REVIEW"]
    print("=" * 68)
    if notrun:
        print(f"NOT RUN: {', '.join(notrun)} -- the measurement is incomplete.")
    if bad:
        print(f"REVIEW:  {', '.join(bad)}")
    if not bad and not notrun:
        print("all stability checks pass")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\nwrote {x.json}")


if __name__ == "__main__":
    main()
