#!/usr/bin/env python3
"""Split options that merged distant decisions from one run. No model calls.

WHAT IS BEING REPAIRED
----------------------
An option holding two decisions from the SAME run, written far apart in the
script, is a claim that the analyst did one thing twice. Reading those cases
showed the claim is usually false: a skin-tone effect moderated by IAT score at
line 27 and by referee experience at line 31 are two moderators; "drop
unclassified dyads" at line 45 and "restrict to extreme skin tones and refit"
at line 236 are sample formation and a sensitivity analysis 190 lines apart.
76 of 96 such groups span more than five lines.

That is an over-merge at the option level -- the error this project calls
invisible in the output and unrecoverable. Repairing it is a SPLIT, which is
the sanctioned direction: over-merge is unrecoverable, under-merge is visible
and fixable.

THE RULE
--------
Within an option, order each run's members by source line. The first is the
PRIMARY use; later ones separated by more than `--span` lines move to
`<option> #2`, `#3`, ... This is deterministic, needs no model call, and maps
directly onto the carve-out the induction prompt already states: "dichotomise
at 0.25, then refit at 0.50" is one analyst reporting a sensitivity analysis,
not one analyst taking two options at one slot.

Runs contributing a single decision are untouched, so an option with no
same-run repeats is returned exactly as it was.

WHAT THIS DOES NOT DO
---------------------
It does not decide whether the split is *correct* -- only that the merge was
unsupported. A genuine repeat (the same policy applied to two variables, e.g.
treating "NA" as missing for height and for rater scores) will also be split,
and that is a known over-correction. The asymmetry rule prefers it: a wrong
split is visible in the output and a human can merge it back; a wrong merge is
neither.

It also does not touch forks. The larger exclusivity problem -- 86% of runs
hold two options at one fork, dominated by the skin-tone exposure fork at 158
of 223 runs -- is a fork-level question and needs adjudication, not a rule.

WARNING ON MEASURING AFTER REPAIR
---------------------------------
Applying one deterministic transformation to two builds can raise their
agreement for a trivial reason: both receive the same systematic change. The
rule here reads only each build's own membership and line numbers, never the
other build, so it is not circular -- but any agreement measured after repair
must be reported with that caveat, and against the pre-repair number.

Usage:
    python3 stability/scripts/repair_option_splits.py --vocab V.json
        --out-tag <tag> [--span 5] [--report out.csv]
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--vocab", required=True)
    ap.add_argument("--out", required=True, help="path for the repaired file")
    ap.add_argument("--span", type=int, default=5,
                    help="line distance above which a same-run repeat is "
                         "treated as a separate use")
    ap.add_argument("--report")
    x = ap.parse_args()

    d = json.loads(Path(x.vocab).read_text(encoding="utf-8"))
    dec = d["decisions"]

    new_options, rows = [], []
    n_split = n_new = 0
    for o in d["options"]:
        ms = [m for m in o.get("members", ()) if 0 <= m < len(dec)]
        by_run = defaultdict(list)
        for m in ms:
            by_run[dec[m]["run"]].append(m)

        # occurrence index per member: 0 for each run's first use, then 1, 2...
        # but only when the gap exceeds `span`; a close repeat stays index 0
        # because it is far more likely one operation the segmenter split.
        idx_of = {}
        split_here = False
        for r, mm in by_run.items():
            mm.sort(key=lambda m: dec[m].get("line", 0))
            k, last = 0, None
            for m in mm:
                ln = dec[m].get("line", 0)
                if last is not None and (ln - last) > x.span:
                    k += 1
                    split_here = True
                idx_of[m] = k
                last = ln

        groups = defaultdict(list)
        for m in ms:
            groups[idx_of[m]].append(m)

        if not split_here or len(groups) == 1:
            new_options.append(o)
            continue

        n_split += 1
        for k in sorted(groups):
            mem = sorted(groups[k])
            no = dict(o)
            no["members"] = mem
            no["n"] = len(mem)
            no["runs"] = sorted({dec[m]["run"] for m in mem})
            if k > 0:
                no["option"] = f"{o['option']} #{k + 1}"
                no.setdefault("option_raw", [o["option"]])
                no["split_from"] = o["option"]
                no["split_rule"] = f"same-run repeat >{x.span} lines apart"
                n_new += 1
            new_options.append(no)
            rows.append({"fork": o["fork"][:80],
                         "option": no["option"][:80],
                         "occurrence": k + 1, "members": len(mem),
                         "runs": len(no["runs"])})

    before, after = len(d["options"]), len(new_options)
    d["options"] = new_options
    d["option_split_repair"] = {
        "source": Path(x.vocab).name, "span": x.span,
        "options_before": before, "options_after": after,
        "options_split": n_split, "options_created": n_new,
    }
    try:
        from vocab import sync_counts
        sync_counts(d)
    except Exception:                                           # noqa: BLE001
        d["n_options"] = after
        d["n_forks"] = len({o["fork"] for o in new_options})

    Path(x.out).parent.mkdir(parents=True, exist_ok=True)
    Path(x.out).write_text(json.dumps(d, ensure_ascii=False, indent=1),
                           encoding="utf-8")

    print(f"OPTION-SPLIT REPAIR  {Path(x.vocab).name}")
    print(f"  span threshold        {x.span} lines")
    print(f"  options split         {n_split}")
    print(f"  new options created   {n_new}")
    print(f"  options {before} -> {after}")
    print(f"  forks unchanged at    {d['n_forks']}")
    print(f"-> {x.out}")

    if x.report and rows:
        Path(x.report).parent.mkdir(parents=True, exist_ok=True)
        with open(x.report, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"   {x.report}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()
