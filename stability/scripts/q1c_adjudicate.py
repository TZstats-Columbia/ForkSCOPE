#!/usr/bin/env python3
"""Q1c -- semantic agreement of silent decisions across two builds. MODEL CALLS.

Q1b matched silent decisions structurally (line overlap) and lexically (token
overlap) and got F1 0.50 and 0.31. Neither is the number we want. Line overlap
cannot see that "average the two raters" and "combine both ratings into one
score" are the same operation; token overlap cannot either. Both are floors.

This asks a model, per run, to align the two lists -- the same move the ablation
gate makes for code-vs-prose, applied to build-vs-build.

WHY THE WHOLE LIST, NOT JUST THE UNMATCHED PAIRS
------------------------------------------------
Adjudicating only what the structural pass failed to match would inherit that
pass's decisions about everything else, and those decisions are exactly what is
in question. Giving the model both complete lists yields a clean semantic F1
that stands on its own, subsumes the unmatched cases, and costs almost nothing:
the lists average about two entries per run.

BLINDING
--------
Which build is presented as list 1 is randomised per run, and the lists carry no
build label. Without this a judge could systematically favour whichever list is
shown first, and the asymmetry would be indistinguishable from a real difference
between builds. `flipped` is recorded so the effect can be checked afterwards --
the same check E1 makes for the ablation gate.

COST
----
One call per run with a non-empty pair of lists. On this corpus that is ~30
calls on short payloads.

Usage:
    python3 stability/scripts/q1c_adjudicate.py --a <A/data/distilled>
        --b <B/data/distilled> [--json out.json] [--csv out.csv] [--dry-run]
"""
import argparse
import csv
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "scripts"))

SEED = 20260822
PROMPT = "30_silent_identity"
SCHEMA = {
    "type": "object",
    "required": ["pairs", "unmatched_1", "unmatched_2"],
    "properties": {
        "pairs": {"type": "array", "items": {
            "type": "object", "required": ["id_1", "id_2"]}},
        "unmatched_1": {"type": "array"},
        "unmatched_2": {"type": "array"},
    },
}


def silent(d):
    p = Path(d) / "record.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8")).get("silent_decisions", [])


def entry(s):
    return {"id": s["id"], "operation": s.get("operation", ""),
            "lines": s.get("lines"), "concerns": (s.get("targets") or [])[:6]}


def adjudicate(run, sa, sb, rng, dry=False):
    """One blinded alignment call. Returns (matched, n_a, n_b, flipped, rows)."""
    flip = rng.random() < 0.5
    A, B = (sb, sa) if flip else (sa, sb)
    a = [entry(s) for s in A]
    b = [entry(s) for s in B]
    rng.shuffle(a)
    rng.shuffle(b)
    ids_a = {x["id"] for x in a}
    ids_b = {x["id"] for x in b}

    def check(o):
        """Every id used exactly once -- the invariant the schema cannot state.

        Without it the model can silently drop entries, which would look like
        disagreement rather than like an unanswered question.
        """
        pa = [p.get("id_1") for p in o.get("pairs", [])]
        pb = [p.get("id_2") for p in o.get("pairs", [])]
        ua = list(o.get("unmatched_1", []))
        ub = list(o.get("unmatched_2", []))
        miss_a, miss_b = ids_a - set(pa) - set(ua), ids_b - set(pb) - set(ub)
        if miss_a or miss_b:
            raise ValueError(
                f"unaccounted ids -- list1 {sorted(miss_a)[:6]}, "
                f"list2 {sorted(miss_b)[:6]}. Every id appears exactly once.")
        dup = ([i for i, c in Counter(pa + ua).items() if c > 1] +
               [i for i, c in Counter(pb + ub).items() if c > 1])
        if dup:
            raise ValueError(f"ids used more than once: {dup[:6]}")

    if dry:
        return 0, len(sa), len(sb), flip, []

    from llm import ask
    out = ask(PROMPT, {"list_1": a, "list_2": b}, schema=SCHEMA,
              model="opus", run_id="stability_silent", check=check)

    by_a = {s["id"]: s for s in A}
    by_b = {s["id"]: s for s in B}
    rows = []
    for p in out.get("pairs", []):
        x, y = by_a.get(p["id_1"]), by_b.get(p["id_2"])
        # Undo the blinding for the audit trail, so a row always names the
        # build an entry came from rather than the position it was shown in.
        ra, rb = (y, x) if flip else (x, y)
        rows.append({"run": run, "verdict": "same",
                     "a_operation": (ra or {}).get("operation", ""),
                     "b_operation": (rb or {}).get("operation", ""),
                     "why": p.get("why", "")})
    for i in out.get("unmatched_1", []):
        s = by_a.get(i, {})
        rows.append({"run": run,
                     "verdict": "only_in_B" if flip else "only_in_A",
                     "a_operation": "" if flip else s.get("operation", ""),
                     "b_operation": s.get("operation", "") if flip else "",
                     "why": ""})
    for i in out.get("unmatched_2", []):
        s = by_b.get(i, {})
        rows.append({"run": run,
                     "verdict": "only_in_A" if flip else "only_in_B",
                     "a_operation": s.get("operation", "") if flip else "",
                     "b_operation": "" if flip else s.get("operation", ""),
                     "why": ""})
    return len(out.get("pairs", [])), len(sa), len(sb), flip, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--json")
    ap.add_argument("--csv")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be called, spend nothing")
    x = ap.parse_args()

    da, db = Path(x.a), Path(x.b)
    shared = sorted({p.name for p in da.iterdir() if p.is_dir()} &
                    {p.name for p in db.iterdir() if p.is_dir()})
    rng = random.Random(SEED)

    tot_m = tot_a = tot_b = 0
    calls = flips = 0
    rows, per_run = [], []
    for name in shared:
        sa, sb = silent(da / name), silent(db / name)
        if sa is None or sb is None:
            continue
        if not sa and not sb:
            continue
        if not sa or not sb:
            # Nothing to align: one side is empty, so every entry on the other
            # is unmatched by construction and a call would only confirm it.
            tot_a += len(sa)
            tot_b += len(sb)
            per_run.append({"run": name, "n_a": len(sa), "n_b": len(sb),
                            "matched": 0, "called": False})
            continue
        m, na, nb, flip, r = adjudicate(name, sa, sb, rng, x.dry_run)
        calls += 1
        flips += int(flip)
        tot_m += m
        tot_a += na
        tot_b += nb
        rows.extend(r)
        per_run.append({"run": name, "n_a": na, "n_b": nb, "matched": m,
                        "called": True, "flipped": flip})
        if not x.dry_run:
            print(f"    {name}  {na} vs {nb} -> {m} same")

    p = tot_m / tot_b if tot_b else 0.0
    r_ = tot_m / tot_a if tot_a else 0.0
    f1 = 2 * p * r_ / (p + r_) if (p + r_) else 0.0
    res = {
        "build_a": str(da), "build_b": str(db),
        "comparison_type": "replicate",
        "runs_with_silent": len(per_run), "model_calls": calls,
        "flipped_fraction": round(flips / calls, 3) if calls else None,
        "n_a": tot_a, "n_b": tot_b, "matched_semantic": tot_m,
        "precision": round(p, 4), "recall": round(r_, 4), "f1": round(f1, 4),
        "per_run": per_run,
    }

    if x.dry_run:
        print(f"DRY RUN -- {calls} calls would be made over "
              f"{len(per_run)} runs ({tot_a} vs {tot_b} silent decisions)")
        return

    print(f"\nQ1c  SILENT DECISIONS, SEMANTIC AGREEMENT")
    print(f"    model calls          {calls}  "
          f"(blinded; flipped {res['flipped_fraction']})")
    print(f"    silent decisions     {tot_a} in A, {tot_b} in B")
    print(f"    same operation       {tot_m}")
    print(f"    precision / recall   {res['precision']} / {res['recall']}")
    print(f"    F1                   {res['f1']}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"    wrote {x.json}")
    if x.csv and rows:
        Path(x.csv).parent.mkdir(parents=True, exist_ok=True)
        with open(x.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"    wrote {x.csv}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
