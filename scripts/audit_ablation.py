#!/usr/bin/env python3
"""Audit for gate 5.4, the code ablation. Deterministic; reads the match files.

The ablation produces one number the pooling decision rests on -- the fraction
of decisions that land in the same option when re-derived from prose. Six ways
that number can be wrong, each checkable:

  E1  BLINDING. The matcher must not know which list came from code. Verify the
      presentation order was actually randomised and that roughly half the runs
      were flipped, so the judge cannot have anchored on a fixed channel.
  E2  LENIENCY. Compare against the mismatched-run null. If pairing run i's
      code with run j's prose yields a similar match rate, the judge matches on
      topic rather than on decision and the headline is meaningless. This is
      the single most important check here.
  E3  LENGTH CONFOUND. A run with a long report has more prose decisions and
      more chances to match. If recall tracks prose length, the gate is partly
      measuring verbosity.
  E4  CORPUS SPLIT. The gate exists to license pooling AI with human. A pooled
      pass rate hides a failure confined to one corpus, which is precisely the
      case that matters.
  E5  RUN-LEVEL SPREAD. A mean of 0.85 built from runs at 1.0 and 0.4 is a
      different world from every run near 0.85. Report the distribution and how
      many runs individually clear the gate.
  E6  DEGENERATE MATCHING. A judge that pairs almost everything, or almost
      nothing, produces an uninformative rate. Check the match rate sits away
      from both ceilings and that no single run dominates the pairs.

Usage:
    python3 scripts/audit_ablation.py
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
ABL = P.ABLATION
OUT = P.ANALYSIS
GATE = 0.85


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    out = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            out[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(a, b):
    if len(a) < 3:
        return 0.0
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    den = (sum((x - ma) ** 2 for x in ra) * sum((x - mb) ** 2 for x in rb)) ** .5
    return num / den if den else 0.0


def per_run(r):
    v = Counter(p["verdict"] for p in r["pairs"])
    m = sum(v.values())
    return {"run": r["run"], "n_code": r["n_code"], "n_prose": r["n_prose"],
            "matched": m, "same": v["same_option"], "vague": v["vaguer"],
            "conflict": v["same_fork_different_option"],
            "recall": m / r["n_code"] if r["n_code"] else 0,
            "agree": v["same_option"] / m if m else 0,
            "flipped": r.get("flipped", False)}


def main():
    mp = ABL / "matches.json"
    if not mp.exists():
        sys.exit("run `ablation.py match` first")
    main_res = json.loads(mp.read_text(encoding="utf-8"))["results"]
    np_ = ABL / "matches_null.json"
    null_res = json.loads(np_.read_text(encoding="utf-8"))["results"] \
        if np_.exists() else []
    sample = {x["run"]: x for x in
              json.loads((ABL / "sample.json").read_text(encoding="utf-8"))["runs"]}
    rows = [per_run(r) for r in main_res]
    res = {}

    n_code = sum(r["n_code"] for r in rows)
    matched = sum(r["matched"] for r in rows)
    same = sum(r["same"] for r in rows)
    recall = matched / n_code if n_code else 0
    agree = same / matched if matched else 0

    print(f"ABLATION AUDIT — gate 5.4")
    print(f"{len(rows)} runs, {n_code} code decisions, {matched} matched\n")

    # ---- E1 blinding -------------------------------------------------------
    fl = sum(1 for r in rows if r["flipped"])
    frac = fl / len(rows)
    v = "PASS" if 0.35 <= frac <= 0.65 else "REVIEW"
    print(f"E1  BLINDING                                                {v}")
    print(f"    runs with channel order flipped   {fl}/{len(rows)} "
          f"({frac:.0%})")
    fa = [r["agree"] for r in rows if r["flipped"]]
    fb = [r["agree"] for r in rows if not r["flipped"]]
    if fa and fb:
        print(f"    agreement when flipped            "
              f"{sum(fa)/len(fa):.3f}")
        print(f"    agreement when not flipped        "
              f"{sum(fb)/len(fb):.3f}")
        print(f"    -> a large gap would mean the judge favours whichever "
              f"list\n       is presented first, not the decisions in it")
    res["E1"] = {"verdict": v, "flipped_frac": round(frac, 3)}

    # ---- E2 leniency null --------------------------------------------------
    if null_res:
        nrows = [per_run(r) for r in null_res]
        nn = sum(r["n_code"] for r in nrows)
        nm = sum(r["matched"] for r in nrows)
        nrec = nm / nn if nn else 0
        nsame = sum(r["same"] for r in nrows) / nm if nm else 0
        ratio = recall / nrec if nrec else float("inf")
        v = "PASS" if nrec < 0.25 * recall else "REVIEW"
        print(f"\nE2  LENIENCY  (run i's code vs run j's prose)               {v}")
        print(f"    within-run match rate             {recall:.3f}")
        print(f"    mismatched-run match rate         {nrec:.3f}")
        print(f"    ratio                             {ratio:.1f}x")
        print(f"    'same option' among spurious      {nsame:.3f}")
        print(f"    -> every match in the null is false by construction; the")
        print(f"       within-run rate is only meaningful above it")
        res["E2"] = {"verdict": v, "within": round(recall, 4),
                     "null": round(nrec, 4), "ratio": round(ratio, 2)}
    else:
        print(f"\nE2  LENIENCY                                                "
              f"NOT RUN")
        print(f"    `ablation.py match --null` has not been run. Without it "
              f"the\n    agreement rate has no calibration.")
        res["E2"] = {"verdict": "NOT RUN"}

    # ---- E3 length confound ------------------------------------------------
    rho_p = spearman([r["n_prose"] for r in rows], [r["recall"] for r in rows])
    rho_c = spearman([r["n_code"] for r in rows], [r["recall"] for r in rows])
    v = "PASS" if abs(rho_p) < 0.5 else "REVIEW"
    print(f"\nE3  LENGTH CONFOUND                                         {v}")
    print(f"    Spearman(prose decisions, recall) {rho_p:+.3f}")
    print(f"    Spearman(code decisions, recall)  {rho_c:+.3f}")
    res["E3"] = {"verdict": v, "rho_prose": round(rho_p, 3),
                 "rho_code": round(rho_c, 3)}

    # ---- E4 corpus split ---------------------------------------------------
    print(f"\nE4  CORPUS SPLIT  (the gate exists to license pooling)")
    print(f"    {'corpus':<8}{'runs':>6}{'recall':>9}{'agree':>8}"
          f"{'vague':>8}{'conflict':>10}{'gate':>7}")
    worst = 1.0
    by = {}
    # The corpora present in the sample, not two names. sorted() keeps
    # the report order deterministic across studies.
    for corp in sorted({v.get("corpus") for v in sample.values()
                        if v.get("corpus")}):
        sub = [r for r in rows if sample.get(r["run"], {}).get("corpus") == corp]
        if not sub:
            continue
        c_code = sum(r["n_code"] for r in sub)
        c_m = sum(r["matched"] for r in sub)
        c_s = sum(r["same"] for r in sub)
        c_v = sum(r["vague"] for r in sub)
        c_x = sum(r["conflict"] for r in sub)
        a = c_s / c_m if c_m else 0
        worst = min(worst, a)
        by[corp] = {"runs": len(sub), "recall": round(c_m / max(1, c_code), 4),
                    "agree": round(a, 4),
                    "vague": round(c_v / max(1, c_m), 4),
                    "conflict": round(c_x / max(1, c_m), 4)}
        print(f"    {corp:<8}{len(sub):>6}{c_m/max(1,c_code):>9.3f}"
              f"{a:>8.3f}{c_v/max(1,c_m):>8.3f}{c_x/max(1,c_m):>10.3f}"
              f"{'PASS' if a >= GATE else 'FAIL':>7}")
    v = "PASS" if worst >= GATE else "REVIEW"
    print(f"    -> pooling is licensed only if BOTH clear the gate; a pooled")
    print(f"       average that passes while one corpus fails is the case "
          f"this\n       check exists to catch")
    res["E4"] = {"verdict": v, "by_corpus": by}

    # ---- E5 run-level spread ------------------------------------------------
    ag = sorted(r["agree"] for r in rows if r["matched"] >= 3)
    if ag:
        q = lambda p: ag[min(len(ag) - 1, int(len(ag) * p))]     # noqa: E731
        clear = sum(1 for x in ag if x >= GATE)
        v = "PASS" if clear / len(ag) >= 0.6 else "REVIEW"
        print(f"\nE5  RUN-LEVEL SPREAD  (runs with >= 3 matches)              {v}")
        print(f"    runs                              {len(ag)}")
        print(f"    min / q25 / median / q75 / max    "
              f"{ag[0]:.2f} / {q(.25):.2f} / {q(.5):.2f} / {q(.75):.2f} / "
              f"{ag[-1]:.2f}")
        print(f"    runs individually clearing {GATE}    {clear}/{len(ag)} "
              f"({clear/len(ag):.0%})")
        res["E5"] = {"verdict": v, "median": q(.5), "min": ag[0],
                     "clearing": clear, "n": len(ag)}

    # ---- E6 degenerate matching --------------------------------------------
    share = max(r["matched"] for r in rows) / matched if matched else 0
    ceil_hi = sum(1 for r in rows if r["recall"] >= 0.98)
    ceil_lo = sum(1 for r in rows if r["recall"] <= 0.02)
    v = "PASS" if 0.05 < recall < 0.95 and share < 0.15 else "REVIEW"
    print(f"\nE6  DEGENERATE MATCHING                                     {v}")
    print(f"    overall match rate                {recall:.3f}")
    print(f"    runs matching ~everything         {ceil_hi}")
    print(f"    runs matching ~nothing            {ceil_lo}")
    print(f"    largest single run's share        {share:.1%}")
    res["E6"] = {"verdict": v, "recall": round(recall, 4),
                 "ceiling_runs": ceil_hi, "floor_runs": ceil_lo}

    fails = [k for k, x in res.items() if isinstance(x, dict)
             and x.get("verdict") in ("REVIEW", "NOT RUN")]
    print("\n" + "=" * 68)
    print("ALL CHECKS PASS" if not fails else "NEEDS REVIEW: " + ", ".join(fails))
    print(f"headline: recall {recall:.3f}, agreement {agree:.3f} "
          f"(gate {GATE}) -> {'PASS' if agree >= GATE else 'FAIL'}")
    p = P.AUDITS / "ablation_audit.json"
    p.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {p}")


if __name__ == "__main__":
    main()
