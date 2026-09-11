#!/usr/bin/env python3
"""Verify outcomes.json against the per-run fragments it was assembled from.

WHY THIS IS A CHECKER AND NOT A BUILDER

`outcomes.json` is the payout side of the Shapley analysis -- what each run
concluded. Five scripts read it and, until this file existed, nothing in the
package wrote it or could confirm it. It was assembled per run, outside the
pipeline, and that is a gap worth stating rather than papering over.

The per-run fragments are now vendored in `data/outcomes/fragments/`, one JSON
per run. They cover **155 of the 207 records**. So they are real provenance for
three quarters of the file and no provenance at all for the rest, and a script
that rebuilt `outcomes.json` from them would silently delete 52 runs. Hence a
checker: it verifies what can be verified and reports precisely what cannot.

WHAT IT CHECKS

  every fragment agrees, field by field, with its record
  every fragment corresponds to a record that exists
  which records have no fragment behind them

Usage:
    python3 scripts/check_outcomes.py
    python3 scripts/check_outcomes.py --json
"""
import argparse
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402

FIELDS = ("primary_estimand_type", "primary_estimate", "or_scale_estimate",
          "ci_low", "ci_high", "conclusion", "notes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    # Unlike the analyses, this script is ABOUT outcomes, so an absence is its
    # answer rather than a reason to skip quietly. It still must not traceback:
    # /audit runs it as one of the free checks, and a crash there reads as a
    # broken check rather than as an absent input.
    if not P.OUTCOMES.exists():
        print(f"no outcomes at {P.OUTCOMES}")
        print("  This study has no outcome side yet. For soccer-C that is "
              "owner decision D3: the extractor must be written, and the "
              "hand-assembled set it replaces was rejected because 52 of 207 "
              "records had no provenance.")
        print("  Nothing to check. This is a MISSING INPUT, not a failed check.")
        return 0

    out = json.loads(P.OUTCOMES.read_text(encoding="utf-8"))
    rec = {o["repo_id"]: o for o in out}
    frag_dir = P.OUTCOMES.parent / "fragments"
    frags = {}
    for f in glob.glob(str(frag_dir / "*.json")):
        try:
            frags[os.path.basename(f)[:-5]] = json.loads(
                Path(f).read_text(encoding="utf-8"))
        except ValueError as e:
            print(f"  unreadable fragment {os.path.basename(f)}: {e}")

    orphan = sorted(set(frags) - set(rec))
    unbacked = sorted(set(rec) - set(frags))
    mismatch = []
    for rid, fr in frags.items():
        if rid not in rec:
            continue
        bad = [k for k in FIELDS if rec[rid].get(k) != fr.get(k)]
        if bad:
            mismatch.append({"run": rid, "fields": bad})

    res = {"records": len(rec), "fragments": len(frags),
           "verified": len(frags) - len(orphan) - len(mismatch),
           "no_fragment": len(unbacked), "orphan_fragments": len(orphan),
           "mismatched": mismatch,
           "no_fragment_runs": unbacked}
    if a.json:
        print(json.dumps(res, indent=2))
        return 1 if mismatch or orphan else 0

    print(f"OUTCOMES PROVENANCE")
    print(f"  records in outcomes.json     : {res['records']}")
    print(f"  per-run fragments on disk    : {res['fragments']}")
    print(f"  records verified against one : {res['verified']} "
          f"({res['verified']/max(1,res['records']):.0%})")
    print(f"  records with no fragment     : {res['no_fragment']}")
    print(f"  fragments with no record     : {res['orphan_fragments']}")
    if mismatch:
        print(f"\n  MISMATCHES ({len(mismatch)}):")
        for m in mismatch[:10]:
            print(f"    {m['run']}  differs on {', '.join(m['fields'])}")
    if unbacked:
        print(f"\n  no fragment behind these {len(unbacked)} records "
              f"(first 8):")
        for r in unbacked[:8]:
            print(f"    {r}")
        print(f"\n  These are not wrong -- they are unverifiable from what the")
        print(f"  package carries. Treated as a known gap, not a failure.")
    print(f"\n  verdict: "
          f"{'FAIL - fragments disagree with the file' if mismatch else 'PASS'}")
    return 1 if mismatch or orphan else 0


if __name__ == "__main__":
    sys.exit(main())
