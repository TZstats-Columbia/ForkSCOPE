#!/usr/bin/env python3
"""Build the human review packet: two benchmarks and one audit. No model calls.

WHAT THIS IS FOR
----------------
Every number in `stability/` is a model self-agreement rate, and a self-agreement
rate has no interpretation on its own. 0.70 is poor against humans who agree at
0.95 and at ceiling against humans who agree at 0.70. This packet supplies the
missing denominator.

For the comparison to be valid the humans must do the SAME TASK the model did,
on the SAME ITEMS. That constraint drives every design choice below, and it is
why the packet is pairwise rather than holistic: the model never made a
holistic judgement, so there is nothing holistic to compare it against.

THE THREE PARTS, AND WHY THE ORDER IS FIXED
-------------------------------------------
  1  option pairs   "same action?"          benchmarks prompt 19
  2  fork pairs     "same decision point?"  benchmarks prompts 21/22
  3  fork audit     over/under-merged?      improves the vocabulary

Parts 1 and 2 must be completed BEFORE part 3, and the pair rows deliberately
do not name their parent fork. Seeing a whole fork first would anchor the pair
judgements with context the model never had, which would leave the audit intact
but destroy the benchmark. Order is the only thing protecting that, so the
packet ships as separate files with the instruction stated in each.

WHAT MODEL-MODEL AGREEMENT MEANS HERE
-------------------------------------
For any pair of items, build A either put them together or did not, and so did
build B. That binary is exactly the co-membership ARI is computed from, so the
model's answer to every question in this packet already exists and needs no new
calls. The rater's answer is the same binary. They are directly comparable.

STRATA
------
  stable_same    both builds grouped them
  stable_diff    neither did
  unstable       the builds disagree      <- the stratum the packet exists for
  gold           obviously same / obviously different, to catch disengagement

Strata and model verdicts live in a KEY file the rater never opens. Rows are
shuffled. Without that the model's answer anchors the human's.

THE HYPOTHESIS, REGISTERED BEFORE ANY RATING
--------------------------------------------
  If humans also split on the unstable pairs, model instability is tracking
  genuine ambiguity -- the pipeline is uncertain where the question is hard,
  which is the good outcome.

  If humans agree confidently on pairs the builds disagree about, the
  instability is model noise rather than ambiguity. That is the worse outcome
  and it points at the prompt.

Both are publishable. Writing it here means the reading cannot be chosen after
the fact.

Usage:
    python3 stability/scripts/review_sheet.py --a A.json --b B.json
        --out reviews/human-benchmark [--n-option 40] [--n-fork 60]
        [--n-audit 30] [--raters 3]
"""
import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import vocab                                                   # noqa: E402
import partition as P                                          # noqa: E402
from layer_agreement import load as load_opts, match_options    # noqa: E402

SEED = 20260822


# ---------- shared loading ---------------------------------------------------
def decisions(path):
    """[(key, run, line, text)] in file order, plus option/fork label maps."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    keys = [(r["run"], r.get("line", -1), (r.get("text") or "")[:60])
            for r in dec]
    text = {keys[i]: (dec[i].get("text") or "") for i in range(len(dec))}
    opt, fork = {}, {}
    for o in d["options"]:
        for m in o.get("members", ()):
            if 0 <= m < len(keys):
                opt[keys[m]] = o["option"]
                fork[keys[m]] = o["fork"]
    return text, opt, fork


def stratum(a_same, b_same):
    if a_same and b_same:
        return "stable_same"
    if not a_same and not b_same:
        return "stable_diff"
    return "unstable"


def draw(pool, n, rng):
    return rng.sample(pool, n) if len(pool) > n else list(pool)


# ---------- part 1: option pairs ---------------------------------------------
def option_pairs(ta, oa, fa, ob, n, rng):
    """Pairs of decisions WITHIN one fork of build A.

    Within-fork is not a convenience -- it is prompt 19's actual universe. The
    model only ever compares options inside a single fork, so a cross-fork pair
    would be a question it was never asked, and a random corpus pair is
    trivially 'different' and wastes a rater.
    """
    by_fork = defaultdict(list)
    for k, f in fa.items():
        by_fork[f].append(k)

    buckets = defaultdict(list)
    for f, ks in by_fork.items():
        if len(ks) < 2:
            continue
        ks = sorted(ks)
        # Cap per fork so one huge fork cannot dominate the sample.
        for i in range(len(ks)):
            for j in range(i + 1, min(i + 12, len(ks))):
                x, y = ks[i], ks[j]
                if x not in ob or y not in ob:
                    continue
                s = stratum(oa[x] == oa[y], ob[x] == ob[y])
                buckets[s].append((x, y))

    per = max(1, n // 3)
    rows = []
    for s in ("stable_same", "stable_diff", "unstable"):
        for x, y in draw(buckets[s], per, rng):
            rows.append({"a_text": ta[x], "b_text": ta[y], "stratum": s,
                         "model_a": oa[x] == oa[y], "model_b": ob[x] == ob[y]})
    return rows, {k: len(v) for k, v in buckets.items()}


# ---------- part 2: fork pairs -----------------------------------------------
def fork_pairs(pa, fa_of, fb_of, oa_lbl, n, rng):
    """Pairs of cross-build MATCHED options, asked at the fork level.

    Using matched options as the item makes this exactly the layer-2 clustering
    measured at ARI 0.307 -- same items, same question, so the human rate drops
    straight into the same table.

    The universe is restricted to pairs at least one build co-forked, plus hard
    negatives from forks that are adjacent in the same DSLC stage. Sampling all
    pairs would be ~99.9% trivially-different and unusable.
    """
    buckets = defaultdict(list)
    m = len(pa)
    for i in range(m):
        ia, ib = pa[i][0], pa[i][1]
        for j in range(i + 1, m):
            ja, jb = pa[j][0], pa[j][1]
            a_same = fa_of[ia] == fa_of[ja]
            b_same = fb_of[ib] == fb_of[jb]
            if not (a_same or b_same):
                continue           # hard negatives handled separately
            buckets[stratum(a_same, b_same)].append((i, j, a_same, b_same))

    # Hard negatives: neither build co-forked them, but they share a stage-like
    # neighbourhood -- sampled from options whose forks differ yet whose labels
    # overlap lexically, which is where a human might plausibly hesitate.
    neg = []
    for i in range(min(m, 300)):
        for j in range(i + 1, min(m, 300)):
            ia, ib, ja, jb = pa[i][0], pa[i][1], pa[j][0], pa[j][1]
            if fa_of[ia] == fa_of[ja] or fb_of[ib] == fb_of[jb]:
                continue
            wa = set(fa_of[ia].lower().split()) - {"the", "a", "is", "are"}
            wb = set(fa_of[ja].lower().split()) - {"the", "a", "is", "are"}
            if wa and wb and len(wa & wb) / len(wa | wb) > 0.25:
                neg.append((i, j, False, False))
    buckets["stable_diff"].extend(neg)

    per = max(1, n // 3)
    rows = []
    for s in ("stable_same", "stable_diff", "unstable"):
        for i, j, a_same, b_same in draw(buckets[s], per, rng):
            rows.append({
                "a_text": oa_lbl[pa[i][0]], "b_text": oa_lbl[pa[j][0]],
                "stratum": s, "model_a": a_same, "model_b": b_same})
    # The injected count is returned because a reader of the KEY cannot
    # otherwise tell that this pool's `stable_diff` cell is synthetic.
    return rows, {k: len(v) for k, v in buckets.items()}, len(neg)


GOLD_SAME_JACCARD = 0.6   # wording overlap required of an "obviously same" pair


def _toks(s):
    return {w for w in "".join(c if c.isalnum() else " "
                              for c in s.lower()).split() if len(w) > 2}


def _jac(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


def gold(ta, oa, rng, n=4, min_jac=GOLD_SAME_JACCARD):
    """Obvious pairs, to detect a rater who is not reading.

    A gold pair must be obvious FROM THE TEXT the rater sees. Being assigned to
    one option by the pipeline is not that: it is the very judgement under test,
    so a rater who reads a hard pair carefully and disagrees would be scored as
    disengaged and their whole sheet thrown away. That is backwards -- it lets a
    hard item disqualify the humans and quietly flatter the model.

    The first version of this function drew `gold_same` from co-assigned
    decisions and only *claimed* in its docstring that they shared most of their
    wording. Nothing checked it. One such pair shipped -- a generic "choose the
    covariate/adjustment set" against a specific named covariate list -- and two
    of three raters called it different, one of them at confidence 1. It was
    retired at scoring time. The overlap is now enforced, not asserted.

    `gold_diff` pairs come from different forks, which is a weaker requirement:
    two lines from unrelated forks are obviously different however they are
    worded, and the failure mode above does not apply.
    """
    by_opt = defaultdict(list)
    for k, o in oa.items():
        by_opt[o].append(k)
    tk = {k: _toks(t) for k, t in ta.items()}

    # Candidates ranked by wording overlap: the most obviously-same first.
    cand = []
    for ks in by_opt.values():
        for i, x in enumerate(sorted(ks)):
            for y in sorted(ks)[i + 1:]:
                j = _jac(tk[x], tk[y])
                if j >= min_jac:
                    cand.append((j, x, y))
    cand.sort(key=lambda c: -c[0])

    rows, used = [], set()
    for j, x, y in cand:
        if len(rows) >= n // 2:
            break
        if oa[x] in used:
            continue
        used.add(oa[x])
        rows.append({"a_text": ta[x], "b_text": ta[y], "stratum": "gold_same",
                     "model_a": True, "model_b": True, "gold_jaccard": round(j, 3)})
    if len(rows) < n // 2:
        print(f"  WARNING: only {len(rows)} gold_same pairs clear Jaccard "
              f"{min_jac}; asked for {n // 2}. Lower --gold-jaccard or accept "
              f"a weaker engagement check -- do NOT fall back to co-assignment.")

    keys = sorted(ta)
    guard = 0
    while len(rows) < n and guard < 10000:
        guard += 1
        x, y = rng.sample(keys, 2)
        if oa.get(x) != oa.get(y):
            rows.append({"a_text": ta[x], "b_text": ta[y],
                         "stratum": "gold_diff",
                         "model_a": False, "model_b": False,
                         "gold_jaccard": round(_jac(tk[x], tk[y]), 3)})
    return rows


# ---------- part 3: fork audit -----------------------------------------------
def audit_rows(path, n, rng):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    per = defaultdict(lambda: {"opts": defaultdict(set)})
    for o in d["options"]:
        for m in o.get("members", ()):
            if 0 <= m < len(dec):
                per[o["fork"]]["opts"][o["option"]].add(dec[m]["run"])
    n_runs = len({r["run"] for r in dec})
    ST = vocab.fork_stats(d, n_runs)

    rows = []
    for f, v in per.items():
        runs = set().union(*v["opts"].values()) if v["opts"] else set()
        if len(runs) < 10:
            continue
        # one vote per analysis; see vocab.fork_stats
        s_ = ST.get(f, {})
        rows.append({
            "fork": f, "runs": s_.get("reach", len(runs)),
            "coverage": s_.get("coverage", round(len(runs) / n_runs, 3)),
            "n_options": s_.get("options", len(v["opts"])),
            "modal_share": s_.get("modal_share", 0),
            "eff_options": s_.get("eff_reached", 0),
            "eff_all": s_.get("eff_all", 0),
            "options": " | ".join(
                f"{o} [{len(s)}]" for o, s in
                sorted(v["opts"].items(), key=lambda t: -len(t[1]))[:14]),
        })
    rows.sort(key=lambda r: -r["coverage"])
    # Half the sheet worst-first (most options relative to runs -- the
    # over-merge smell), half at random so the targeted rows have a base rate
    # to be read against. Without the random half we only ever see what a
    # ranking pushed forward.
    targeted = sorted(rows, key=lambda r: -r["n_options"])[: n // 2]
    rest = [r for r in rows if r not in targeted]
    sample = targeted + draw(rest, n - len(targeted), rng)
    for r in sample:
        r["stratum"] = "targeted" if r in targeted else "random"
    rng.shuffle(sample)
    return sample


def write_pairs(path, rows, question, guidance):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([f"# {question}"])
        for g in guidance:
            w.writerow([f"# {g}"])
        w.writerow([])
        w.writerow(["pair_id", "item_a", "item_b", "verdict",
                    "confidence", "note"])
        for r in rows:
            w.writerow([r["pair_id"], r["a_text"], r["b_text"], "", "", ""])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-option", type=int, default=40)
    ap.add_argument("--n-fork", type=int, default=60)
    ap.add_argument("--n-audit", type=int, default=30)
    ap.add_argument("--raters", type=int, default=3)
    x = ap.parse_args()

    rng = random.Random(SEED)
    out = Path(x.out)
    out.mkdir(parents=True, exist_ok=True)

    ta, oa, fa = decisions(x.a)
    tb, ob, fb = decisions(x.b)

    p1, b1 = option_pairs(ta, oa, fa, ob, x.n_option, rng)
    p1 += gold(ta, oa, rng, 4)

    ma, fa_lbl = load_opts(x.a)
    mb, fb_lbl = load_opts(x.b)
    pairs = match_options(ma, mb, 0.5)
    lbl = {i: o for i, o in enumerate(
        json.loads(Path(x.a).read_text(encoding="utf-8"))["options"])}
    oa_lbl = {i: lbl[i]["option"] for i in lbl}
    p2, b2, n_neg2 = fork_pairs(pairs, fa_lbl, fb_lbl, oa_lbl, x.n_fork, rng)

    for i, r in enumerate(p1):
        r["pair_id"] = f"O{i+1:03d}"
    for i, r in enumerate(p2):
        r["pair_id"] = f"F{i+1:03d}"
    rng.shuffle(p1)
    rng.shuffle(p2)

    a3 = audit_rows(x.a, x.n_audit, rng)

    for rid in range(1, x.raters + 1):
        d = out / f"rater-{rid}"
        d.mkdir(exist_ok=True)
        r2 = random.Random(SEED + rid)
        s1, s2 = list(p1), list(p2)
        r2.shuffle(s1)
        r2.shuffle(s2)
        write_pairs(d / "1_option_pairs.csv", s1,
                    "PART 1 of 3 - same ACTION?",
                    ["Do these two lines describe the SAME OPERATION ON DATA,",
                     "however differently worded?",
                     "verdict: same | different | unsure",
                     "unsure = the text does not carry enough to decide.",
                     "  It is a real answer about the ITEM, not a hedge.",
                     "confidence: 1-5, 1 low and 5 high.",
                     "Complete this file and PART 2 before opening PART 3."])
        write_pairs(d / "2_fork_pairs.csv", s2,
                    "PART 2 of 3 - same DECISION POINT?",
                    ["Are these two choices alternatives at the SAME slot?",
                     "TEST: could one analyst, in one script, do BOTH?",
                     "  yes -> different decision points",
                     "  taking one rules out the other -> SAME decision point",
                     "A robustness refit at another setting is NOT the same.",
                     "verdict: same | different | unsure",
                     "unsure = the text does not carry enough to decide.",
                     "  It is a real answer about the ITEM, not a hedge.",
                     "confidence: 1-5, 1 low and 5 high.",
                     "Complete PART 1 and this file before opening PART 3."])
        # Part 3 is a WORKSHEET, not a test. The first run of this packet was
        # scored for inter-rater agreement on over/under-merged and that was
        # the wrong reading: the raters' free text -- "transformation of games
        # should be its own fork", "one fork about what to include and another
        # about how to transform" -- was worth more than the labels, because it
        # said HOW to re-merge and the label only said THAT something was off.
        # So the label is now a proposed ACTION, and `remerge` is the column
        # the pipeline actually consumes. A blank `remerge` beside a `split`
        # or `move` verdict is an incomplete row, not a filed one.
        with open(d / "3_fork_audit.csv", "w", newline="",
                  encoding="utf-8") as fh:
            w = csv.writer(fh)
            for g in (
                "PART 3 of 3 - how should this fork be RE-MERGED?",
                "Not a test. This sheet is how you hand the pipeline an"
                " instruction it can act on.",
                "",
                "verdict: correct | split | absorb | move | unsure",
                "  correct  one question, and its options are alternatives"
                " at it",
                "  split    two or more questions have been fused -- say"
                " along WHICH AXIS",
                "  absorb   part of a question that also lives in another"
                " fork -- name that fork",
                "  move     some options belong elsewhere -- name which,"
                " and where",
                "  unsure   the row does not carry enough to judge",
                "",
                "remerge: the instruction itself, in your words. This is the"
                " column that",
                "  gets acted on. Examples:",
                "    split by axis: which variables enter | how each is"
                " transformed",
                "    absorb into: how is the skin-tone rating entered as the"
                " exposure?",
                "    move: the games-played options -> their own fork",
                "",
                "An axis you find yourself writing twice is worth saying once,"
                " loudly:",
                "a repeated re-merge instruction is a finding about the"
                " vocabulary,",
                "not about the fork in front of you.",
            ):
                w.writerow([f"# {g}" if g else "#"])
            w.writerow([])
            w.writerow(["fork", "runs", "coverage", "n_options", "modal_share",
                        "eff_options", "options", "verdict", "remerge", "note"])
            for r in a3:
                w.writerow([r.get(k, "") for k in
                            ("fork", "runs", "coverage", "n_options",
                             "modal_share", "eff_options", "options")]
                           + ["", "", ""])

    key = {
        "seed": SEED, "build_a": x.a, "build_b": x.b,
        "hypothesis": (
            "If humans also split on the unstable pairs, model instability "
            "tracks genuine ambiguity. If humans agree confidently where the "
            "builds disagree, it is model noise. Registered before rating."),
        "part1_option_pairs": p1,
        "part2_fork_pairs": p2,
        "part3_audit_strata": {r["fork"]: r["stratum"] for r in a3},
        "pool_sizes": {"option": b1, "fork": b2},
        # The two pools are NOT built the same way, and reweighting to them
        # therefore does not mean the same thing.
        #
        # The option pool is every within-fork pair of build A. Its
        # `stable_diff` cell is real: pairs both builds separated. Reweighting
        # to it gives an honest agreement rate over that universe.
        #
        # The fork pool keeps only pairs at least one build co-forked, then
        # INJECTS lexically-similar hard negatives. Its `stable_diff` cell is
        # entirely synthetic and the true negatives -- the overwhelming
        # majority -- are gone. A "model agreement rate" over that pool is
        # a positive-agreement statistic (Jaccard on co-membership) diluted by
        # however many negatives happened to be injected, and it is dominated
        # by a stratum whose model agreement is 0 BY DEFINITION. It must not
        # be printed opposite the human rate as though the two were measuring
        # the same thing: the pool was selected on the model's disagreements
        # and on nobody else's.
        "pool_restricted": {"option": False, "fork": True},
        "pool_injected_negatives": {"option": 0, "fork": n_neg2},
    }
    (out / "KEY-do-not-open.json").write_text(
        json.dumps(key, indent=1, ensure_ascii=False), encoding="utf-8")

    def tally(rows):
        c = defaultdict(int)
        for r in rows:
            c[r["stratum"]] += 1
        return dict(sorted(c.items()))

    print(f"packet -> {out}\n")
    print(f"  part 1  option pairs   {len(p1):>3}   {tally(p1)}")
    print(f"  part 2  fork pairs     {len(p2):>3}   {tally(p2)}")
    print(f"  part 3  fork audit     {len(a3):>3}   {tally(a3)}")
    print(f"  raters                 {x.raters}  (same items, "
          f"independently shuffled)")
    print(f"\n  candidate pools: option {b1}")
    print(f"                   fork   {b2}")
    print(f"\n  KEY-do-not-open.json holds strata, model verdicts and the "
          f"registered hypothesis.")


if __name__ == "__main__":
    main()
