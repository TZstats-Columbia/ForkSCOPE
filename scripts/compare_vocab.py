#!/usr/bin/env python3
"""Before/after across successive vocabularies. No model calls, fully derived.

Four repair passes have run over the v2 clustering, each fixing something the
last audit exposed:

    ai+human                          as originally clustered
    .merged                           paraphrase options collapsed within a fork
    .merged.forkmerged                duplicate decision points merged
    .merged.forkmerged.merged         options re-merged, now that duplicate
                                      forks are united and their options can
                                      finally be compared to each other
    ....induced                       decision points re-derived from option
                                      PURPOSE rather than emitted as a
                                      by-product of option merging

Every one moves the numbers the project reports, so a claim is only meaningful
against a named vocabulary. This prints the same statistics for each, side by
side, and flags where a conclusion flips.

The comparison is deliberately narrow: concentration statistics and coverage,
the two things option and fork granularity actually determine. Outcome-linked
results (Shapley, novelty dose-response) are not here -- they need re-running in
full rather than recomputing from the vocabulary, and mixing the two would
imply a precision this does not have.

Usage:
    python3 scripts/compare_vocab.py ai+human ai+human.merged ...
"""
import json
import re
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
OUT = P.ANALYSIS
MIN_RUNS = 10          # matches stability.py: below this, concentration is noise


def stats(tag):
    p = P.VOCAB / f"bottom_up_{tag}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    base = tag.split(".")[0]
    gm = json.loads((OUT / f"garden_{base}.json").read_text(encoding="utf-8"))
    dec = d["decisions"]
    cmap = {}
    for h, ms in gm.get("sibling_groups", {}).items():
        for m in ms:
            cmap[m] = h
    forks = defaultdict(lambda: defaultdict(set))
    for o in d["options"]:
        # once forks have been re-induced the sibling map is already folded in
        node = o["fork"] if ("fork_raw" in o or "fork_induction" in d) \
            else cmap.get(o["fork"], o["fork"])
        for i in o.get("members", []):
            if i < len(dec):
                forks[node][o["option"]].add(dec[i]["run"])
    rows = {}
    for f, om in forks.items():
        runs = set().union(*om.values())
        c = sorted((len(v) for v in om.values()), reverse=True)
        t = sum(c)
        rows[f] = {"runs": len(runs), "opts": len(om),
                   "modal": c[0] / len(runs), "singles": sum(1 for x in c if x == 1),
                   "eff": 1 / sum((x / t) ** 2 for x in c)}
    meas = [f for f in rows if rows[f]["runs"] >= MIN_RUNS]
    allruns = {r for f in forks for o in forks[f] for r in forks[f][o]}
    return {"tag": tag, "forks": len(forks),
            "options": sum(len(v) for v in forks.values()),
            "decisions": len(dec), "runs": len(allruns),
            "measurable": len(meas),
            "med_opts": st.median(rows[f]["opts"] for f in meas) if meas else 0,
            "med_modal": st.median(rows[f]["modal"] for f in meas) if meas else 0,
            "med_eff": st.median(rows[f]["eff"] for f in meas) if meas else 0,
            "singles": sum(rows[f]["singles"] for f in meas),
            "conventions": sum(1 for f in meas if rows[f]["modal"] >= 0.80),
            "contested": sum(1 for f in meas if rows[f]["eff"] >= 3),
            "universal": sum(1 for f in rows
                             if rows[f]["runs"] >= 0.60 * len(allruns)),
            "rows": rows}


SHORT = {"merged": "+opt-merge", "forkmerged": "+fork-merge",
         "induced": "+induced", "excl": "+exclusivity"}


def chain(final=None):
    """The stages that produced the headline vocabulary, read off disk.

    Each repair pass extends the tag by one suffix, so the lineage is exactly
    the set of tags that are prefixes of the final one. Deriving it beats
    listing it: the chain now loops to a fixpoint, so its length is not known
    in advance, and a hardcoded list silently stops showing the later rounds.
    """
    final = final or P.FINAL_TAG
    have = {f.name[len("bottom_up_"):-len(".json")]
            for f in P.VOCAB.glob("bottom_up_*.json")}

    # Fixpoint rounds are `<base>.rN`, and `.r1` is not a prefix of `.r2`, so
    # the prefix walk alone would skip every round but the last.
    m = re.match(r"^(.*)\.r(\d+)$", final)
    base, rounds = (m.group(1), int(m.group(2))) if m else (final, 0)

    parts = base.split(".")
    out = [".".join(parts[:i]) for i in range(1, len(parts) + 1)]
    out += [f"{base}.r{n}" for n in range(1, rounds + 1)]
    return [t for t in out if t in have]


def label(tag, i):
    """`+opt-merge`, `-2` for a repeat, `round N` for a fixpoint round."""
    if "." not in tag:
        return "original"
    suf = tag.split(".")[-1]
    m = re.match(r"^r(\d+)$", suf)
    if m:
        return f"round {m.group(1)}"
    n = sum(1 for x in tag.split(".")[1:] if x == suf)
    return SHORT.get(suf, "+" + suf) + ("" if n < 2 else f"-{n}")


def main():
    tags = sys.argv[1:] or chain()
    S = [s for s in (stats(t) for t in tags) if s]
    if not S:
        sys.exit("no vocabularies found")

    names = [label(s["tag"], i) for i, s in enumerate(S)]

    print("VOCABULARY COMPARISON")
    print(f"{len(S)} vocabularies, {S[0]['decisions']} decisions, "
          f"{S[0]['runs']} runs (both invariant by construction)\n")
    rowspec = [
        ("decision points", "forks", "{:.0f}"),
        ("options", "options", "{:.0f}"),
        ("measurable forks (>=10 runs)", "measurable", "{:.0f}"),
        ("universal forks (>=60% runs)", "universal", "{:.0f}"),
        ("", None, ""),
        ("median options per fork", "med_opts", "{:.1f}"),
        ("median modal share", "med_modal", "{:.2f}"),
        ("median effective options", "med_eff", "{:.1f}"),
        ("singleton options", "singles", "{:.0f}"),
        ("", None, ""),
        ("conventions (modal >= 0.80)", "conventions", "{:.0f}"),
        ("contested (eff >= 3)", "contested", "{:.0f}"),
    ]
    w = max(13, max(len(n) for n in names) + 2)
    print(f"{'':<30}" + "".join(f"{n:>{w}}" for n in names))
    for lab, key, fmt in rowspec:
        if key is None:
            print()
            continue
        print(f"{lab:<30}" + "".join(fmt.format(s[key]).rjust(w) for s in S))

    # what flipped
    first, last = S[0], S[-1]
    print(f"\nWHAT FLIPPED  ({label(first['tag'], 0)} -> "
          f"{label(last['tag'], -1)})")
    common = set(first["rows"]) & set(last["rows"])
    both = [f for f in common
            if first["rows"][f]["runs"] >= MIN_RUNS
            and last["rows"][f]["runs"] >= MIN_RUNS]
    became_conv = [f for f in both if first["rows"][f]["modal"] < 0.8
                   <= last["rows"][f]["modal"]]
    print(f"  forks present and measurable in both      {len(both)}")
    print(f"  went from contested to convention         {len(became_conv)}")
    for f in sorted(became_conv,
                    key=lambda f: last["rows"][f]["modal"] -
                    first["rows"][f]["modal"], reverse=True)[:8]:
        a, b = first["rows"][f], last["rows"][f]
        print(f"    modal {a['modal']:.2f}->{b['modal']:.2f}  "
              f"eff {a['eff']:>4.1f}->{b['eff']:>4.1f}   {f[:46]}")
    print(f"\n  NOTE  forks not present in both are omitted from the flip "
          f"count: a\n  merged or re-induced fork has a new label and is a new "
          f"object, so it\n  cannot be compared to either parent.")


if __name__ == "__main__":
    main()
