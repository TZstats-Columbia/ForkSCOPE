#!/usr/bin/env python3
"""Refresh stale `n_forks` / `n_options` headers in existing vocabularies.

`cluster_up.py` writes those two fields once, at build time. Every repair pass
afterwards rewrites `options` -- relabelling forks, folding option records --
and each computes the new totals for its own console output, but until now none
wrote them back. So every repaired vocabulary reported its BASE fork count
forever: the headline `...induced.r3` file claimed 463 decision points while its
options actually spanned 317.

`vocab.sync_counts` now runs on every repair write, so new builds are correct.
This fixes the files already on disk, which would otherwise need a full rebuild
to correct -- and a rebuild would cost real money to fix a derived field.

Only the two header integers change. Options, forks, members, runs and every
provenance block are untouched, so no analysis output moves: nothing reads
these fields to compute a result. They are read by people, and by anything that
trusts a summary instead of deriving it, which is exactly why a wrong one is
worth fixing rather than tolerating.

Usage:
    python3 scripts/fix_vocab_counts.py --check    # report, change nothing
    python3 scripts/fix_vocab_counts.py --apply
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                              # noqa: E402
from vocab import sync_counts                                 # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    ap.add_argument("--vocab-dir", default=None)
    a = ap.parse_args()

    d = Path(a.vocab_dir) if a.vocab_dir else P.VOCAB
    files = sorted(d.glob("bottom_up_*.json"))
    if not files:
        sys.exit(f"no bottom_up_*.json under {d}")

    stale = []
    for p in files:
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:                                  # noqa: BLE001
            print(f"  SKIP {p.name}: {type(e).__name__}")
            continue
        if "options" not in obj:
            continue
        was = (obj.get("n_forks"), obj.get("n_options"))
        now = (len({o["fork"] for o in obj["options"] if "fork" in o}),
               len(obj["options"]))
        if was != now:
            stale.append((p, was, now, obj))

    print(f"{len(files)} vocabularies under {d}, {len(stale)} with stale "
          f"headers\n")
    if stale:
        print(f"  {'file':<62}{'n_forks':>16}{'n_options':>16}")
        for p, was, now, _ in stale:
            print(f"  {p.name:<62}{f'{was[0]} -> {now[0]}':>16}"
                  f"{f'{was[1]} -> {now[1]}':>16}")

    if a.apply and stale:
        for p, _, _, obj in stale:
            p.write_text(json.dumps(sync_counts(obj), ensure_ascii=False,
                                    indent=1), encoding="utf-8")
        print(f"\nrewrote {len(stale)} files (header integers only)")
    elif a.check and stale:
        print(f"\nrun with --apply to fix")


if __name__ == "__main__":
    main()
