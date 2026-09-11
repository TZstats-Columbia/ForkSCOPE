#!/usr/bin/env python3
"""V1-V7: falsification exhibits for the vocabulary itself. No model calls.

This is the check that exists because a reported statistic once said 2.7% of
within-fork option pairs were near-duplicates, and a person reading the option
lists side by side found in minutes that two whole forks were the same
question. The statistic was not wrong so much as blind, and it was offered as
reassurance -- the worst possible use of a weak measure.

So this audit inverts that. It computes weak signals deliberately and uses
them for one purpose only: to ORDER a queue of things a human should look at,
worst first. Nothing here concludes that the vocabulary is sound. Several
checks cannot conclude that even in principle, and say so.

  V1  options within one fork are distinct actions        (lexical ranking)
  V2  options within one fork are mutually exclusive      (structural, real)
  V3  distinct forks ask distinct questions               (lexical ranking)
  V4  an option records one action, not several           (structural smell)
  V5  forks whose option count needs a human              (no verdict)
  V6  an option records one use, not a primary and a refit (structural, real)
  V7  an option label names one choice, not a list         (lexical prior)

V2 and V6 are the ones whose evidence is conclusive, and both in one direction
only. Options at one fork are alternatives, so two of them in the SAME run is a
defect and not a matter of taste (V2); and two decisions written 200 lines
apart are not one operation, however similar their wording (V6). The rest rank;
they do not decide.

Usage:
    python3 scripts/audit_vocab.py
    python3 scripts/audit_vocab.py --corpus ai+human.merged --show 30
"""
import argparse
import re
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402
from exhibit import Report                                       # noqa: E402
from trace import Tracer, h_fork, h_option                       # noqa: E402

STOP = set("""a an the of to in on for by with and or at as is are be into from
that this these those it its use used using which what how do does done than
then when where each per via over under between within not no if""".split())

# thresholds are for ordering and for counting how big the queue is; no
# verdict rests on the value of a similarity alone
SIM_WITHIN = 0.55
SIM_FORK = 0.60
CLAUSE = re.compile(r"\b(?:and|then|while|after|before)\b|[,;]|\bwith\b")


def words(s):
    return {w for w in re.findall(r"[a-z0-9.]+", s.lower()) if w not in STOP}


def grams(s, n=3):
    t = re.sub(r"\s+", " ", s.lower().strip())
    return {t[i:i + n] for i in range(max(0, len(t) - n + 1))}


def jac(a, b):
    return len(a & b) / len(a | b) if a or b else 0.0


def sim(a, b):
    """Max of token and character-trigram Jaccard.

    Two weak measures rather than one: tokens catch shared vocabulary,
    trigrams survive morphology ("rater"/"raters", "average"/"averaging").
    Both are blind to two descriptions of one action sharing no words, which
    is precisely the failure that motivated this file -- hence ranking only.
    """
    return max(jac(words(a), words(b)), jac(grams(a), grams(b)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=None)
    ap.add_argument("--show", type=int, default=20)
    a = ap.parse_args()

    t = Tracer(a.corpus)
    tag = t.tag
    by_fork = t._by_fork
    opts = t.options
    print(f"VOCABULARY EXHIBITS - {tag}")
    print(f"{len(by_fork)} forks, {len(opts)} options\n")

    r = Report("vocab_exhibits",
               "Weak signals used to order a review queue, never to conclude.",
               corpus=tag)

    # ---- V1 within-fork option pairs --------------------------------------
    rows, n_pairs = [], 0
    for f, os_ in by_fork.items():
        for x, y in combinations(os_, 2):
            n_pairs += 1
            s = sim(x["option"], y["option"])
            if s >= SIM_WITHIN:
                rows.append({
                    "handle": h_fork(f), "similarity": round(s, 3),
                    "fork": f, "runs_a": x["n"], "runs_b": y["n"],
                    "option_a": x["option"], "option_b": y["option"],
                    "trace_a": h_option(f, x["option"]),
                    "trace_b": h_option(f, y["option"])})
    c = r.check("V1", "options within one fork are distinct actions")
    c.measured(within_fork_pairs=n_pairs, above=len(rows),
               threshold=SIM_WITHIN)
    c.against("no null -- a ranking for human attention, not a test")
    c.uses("label_similarity", "option_lists")
    c.blind_to("two descriptions of one action that share no words. The "
               "rater-averaging fork was invisible to exactly this measure")
    c.exhibit("within-fork option pairs most likely to be one action",
              rows, worst=lambda x: x["similarity"], show=a.show,
              columns=["similarity", "runs_a", "runs_b", "option_a",
                       "option_b", "fork", "trace_a", "trace_b"],
              note="Lexical similarity cannot see two descriptions of one "
                   "action that share no words. A short queue here is NOT "
                   "evidence the fork is clean.")
    c.verdict("REVIEW" if rows else "INFO",
              f"{len(rows)} pairs to read; the metric cannot clear the rest"
              if rows else "no pair passed the ranking threshold, which "
                           "settles nothing -- see the note")
    print(f"V1  {len(rows):>4} within-fork pairs queued of {n_pairs}")

    # ---- V2 exclusivity ----------------------------------------------------
    viol = []
    for f, os_ in by_fork.items():
        for x, y in combinations(os_, 2):
            both = set(x.get("runs") or []) & set(y.get("runs") or [])
            if both:
                viol.append({
                    "handle": h_fork(f), "shared_runs": len(both),
                    "fork": f, "option_a": x["option"], "option_b": y["option"],
                    "runs": ", ".join(sorted(both)[:3]),
                    "trace_a": h_option(f, x["option"]),
                    "trace_b": h_option(f, y["option"])})
    per_fork = {}
    for v in viol:
        d = per_fork.setdefault(v["fork"], {"co": 0, "pairs": 0})
        d["co"] += v["shared_runs"]
        d["pairs"] += 1
    fork_rows = []
    for f, d in per_fork.items():
        runs = len({r for o in by_fork[f] for r in (o.get("runs") or [])})
        fork_rows.append({
            "handle": h_fork(f), "co_choices": d["co"], "pairs": d["pairs"],
            "runs": runs, "options": len(by_fork[f]),
            "rate": round(d["co"] / max(1, runs), 3), "fork": f})

    c = r.check("V2", "every fork is a slot where a run picks exactly one "
                      "option")
    c.measured(violating_pairs=len(viol), forks_affected=len(per_fork),
               forks_total=len(by_fork),
               pairs_sharing_one_run=sum(1 for v in viol
                                         if v["shared_runs"] == 1))
    c.against("structural, and conclusive about the pattern -- a run cannot "
              "take two alternatives at one slot. What it cannot settle is "
              "WHY, and the three causes below are indistinguishable by shape")
    c.uses("co_occurrence")
    c.blind_to("which of the three causes produced any given row, and any "
               "fork the grouping already split BECAUSE its options "
               "co-occurred -- those cannot appear here by construction")
    c.exhibit("forks whose runs took more than one option", fork_rows,
              worst=lambda x: x["co_choices"], show=a.show,
              columns=["co_choices", "pairs", "runs", "options", "rate",
                       "fork", "handle"],
              note="Three causes produce this identically, and only reading "
                   "the fork separates them. (a) The fork is genuinely "
                   "MULTI-SELECT -- reporting both an odds ratio and a risk "
                   "difference is one analyst doing two legitimate things, "
                   "not a clustering error, and the single-choice model is "
                   "simply wrong for that slot. (b) A ROBUSTNESS REFIT -- one "
                   "run dichotomising at 0.25 and again at 0.50; expected, "
                   "and the reason most rows here share exactly one run. "
                   "(c) A CLUSTERING ARTIFACT -- a fork with more co-choices "
                   "than runs is not a slot at all. Sort by `rate`: high rate "
                   "on few runs is (c), low rate on many runs is (b), high "
                   "rate on many runs is (a).")
    c.exhibit("the individual option pairs", viol,
              worst=lambda x: x["shared_runs"], show=a.show,
              columns=["shared_runs", "fork", "option_a", "option_b",
                       "runs", "trace_a", "trace_b"],
              note="Read these before acting on the fork-level table above.")
    c.verdict("REVIEW" if viol else "PASS",
              f"{len(per_fork)} of {len(by_fork)} forks have runs that took "
              f"two options; the single-choice model does not hold for all "
              f"of them" if viol else
              "no option pair at any fork was chosen twice by one run")
    print(f"V2  {len(viol):>4} co-choice pairs across {len(per_fork)} forks")

    # ---- V3 fork pairs -----------------------------------------------------
    sig = {f: (grams(f), {w for o in os_ for w in words(o["option"])})
           for f, os_ in by_fork.items()}
    fp = []
    for x, y in combinations(sorted(by_fork), 2):
        s = max(jac(sig[x][0], sig[y][0]), jac(sig[x][1], sig[y][1]))
        if s >= SIM_FORK:
            fp.append({"similarity": round(s, 3),
                       "runs_a": len({r for o in by_fork[x]
                                      for r in (o.get("runs") or [])}),
                       "runs_b": len({r for o in by_fork[y]
                                      for r in (o.get("runs") or [])}),
                       "fork_a": x, "fork_b": y,
                       "trace_a": h_fork(x), "trace_b": h_fork(y)})
    c = r.check("V3", "distinct forks ask distinct questions")
    c.measured(fork_pairs=len(by_fork) * (len(by_fork) - 1) // 2,
               above=len(fp), threshold=SIM_FORK)
    c.against("no null -- a ranking for human attention, not a test")
    c.uses("label_similarity", "option_lists")
    c.blind_to("two forks asking one question in unrelated words, and -- "
               "since the merge passes already united the label-similar pairs "
               "that do NOT co-occur -- this queue is enriched for pairs the "
               "pipeline refused on structural grounds")
    c.exhibit("fork pairs most likely to be one question", fp,
              worst=lambda x: x["similarity"], show=a.show,
              columns=["similarity", "runs_a", "runs_b", "fork_a", "fork_b",
                       "trace_a", "trace_b"],
              note="Merging two forks that are genuinely one is safe; merging "
                   "two that are not destroys a distinction invisibly. Read "
                   "both option lists before acting on any row here.")
    c.verdict("REVIEW" if fp else "INFO",
              f"{len(fp)} fork pairs to read" if fp else
              "no fork pair passed the ranking threshold")
    print(f"V3  {len(fp):>4} fork pairs queued")

    # ---- V4 compound options ------------------------------------------------
    comp = []
    for o in opts:
        n = len(CLAUSE.findall(o["option"]))
        if n >= 2:
            comp.append({"handle": h_option(o["fork"], o["option"]),
                         "clauses": n + 1, "runs": o["n"],
                         "option": o["option"], "fork": o["fork"]})
    c = r.check("V4", "an option records one action, not several")
    c.measured(options=len(opts), compound=len(comp))
    c.against("structural smell -- clause counting, which over-fires on "
              "options that are genuinely one action described carefully")
    c.blind_to("a compound option written as a single clause: "
               "'complete-case analysis' bundles a drop rule and a scope and "
               "counts as one")
    c.exhibit("options describing the most separable actions", comp,
              worst=lambda x: (x["clauses"], x["runs"]), show=a.show,
              columns=["clauses", "runs", "option", "fork", "handle"],
              note="A compound option makes two decisions inseparable: any "
                   "run choosing it is recorded as having made both, and the "
                   "second one vanishes from its own fork.")
    c.verdict("REVIEW" if comp else "PASS",
              f"{len(comp)} options bundle separable actions" if comp else
              "no option matched the compound pattern")
    print(f"V4  {len(comp):>4} compound options")

    # ---- V6 same-run repeats -------------------------------------------------
    # An option holding two decisions from ONE run, written far apart, claims
    # the analyst did one thing twice. Within a run there is no vocabulary
    # drift to explain a difference away, so the claim is directly checkable by
    # reading both texts -- and reading them showed it is usually false. A
    # skin-tone effect moderated by IAT score at line 27 and by referee
    # experience at line 31 are two moderators; "drop unclassified dyads" at
    # line 45 and "restrict to extreme tones and refit" at line 236 are sample
    # formation and a sensitivity analysis 190 lines apart.
    #
    # Line span is the discriminator, and it is why this is not simply V4 by
    # another route: adjacent lines are one operation the SEGMENTER split, and
    # are not a vocabulary defect at all.
    SPAN = 5
    dec = t.decisions
    rep, n_close = [], 0
    for o in opts:
        by_run = {}
        for m in o.get("members", ()):
            if 0 <= m < len(dec):
                by_run.setdefault(dec[m]["run"], []).append(m)
        for run, ms in by_run.items():
            if len(ms) < 2:
                continue
            lines = sorted(dec[m].get("line", 0) for m in ms)
            span = lines[-1] - lines[0]
            if span <= SPAN:
                n_close += 1
                continue
            rep.append({"handle": h_option(o["fork"], o["option"]),
                        "span": span, "n": len(ms), "run": run,
                        "lines": "/".join(str(x) for x in lines[:4]),
                        "option": o["option"], "fork": o["fork"]})
    c = r.check("V6", "an option records one use, not a primary and a refit")
    c.measured(groups=len(rep) + n_close, distant=len(rep), adjacent=n_close,
               span_threshold=SPAN)
    c.against("structural, and conclusive in one direction only -- two "
              "decisions written 200 lines apart are not one operation, but "
              "two written 3 lines apart may well be")
    c.blind_to("a primary and a refit that happen to sit close together, and "
               "a repeat across DIFFERENT runs, which is what an option is "
               "for and is not a defect")
    c.exhibit("options merging distant decisions from one run", rep,
              worst=lambda x: (x["span"], x["n"]), show=a.show,
              columns=["span", "n", "lines", "run", "option", "fork",
                       "handle"],
              note="Splitting these is the sanctioned direction: over-merge "
                   "is invisible in the output and unrecoverable, under-merge "
                   "is visible and a human can undo it. "
                   "stability/scripts/repair_option_splits.py applies the "
                   "split; it does not decide whether the split is right.")
    c.verdict("REVIEW" if rep else "PASS",
              f"{len(rep)} options merge a run's distant decisions"
              if rep else "no option merges distant same-run decisions")
    print(f"V6  {len(rep):>4} same-run merges over {SPAN} lines "
          f"({n_close} adjacent, not flagged)")

    # ---- V7 disjunctive labels -----------------------------------------------
    # An option whose NAME contains a disjunction is admitting it spans
    # distinct choices: "cluster-robust SEs, varying clustering dimension
    # (unspecified / player / referee / two-way)" is four options wearing one
    # label. Purely lexical and free, and measured at 8.3x enrichment for V6
    # groups -- which makes it a cheap prior on where over-merge lives, on a
    # single build with no replicate needed.
    DISJ = re.compile(r"\s/\s|\bor\b|\([^)]*/[^)]*\)")
    v6_opts = {x["option"] for x in rep}
    disj = []
    for o in opts:
        if DISJ.search(o["option"]):
            disj.append({"handle": h_option(o["fork"], o["option"]),
                         "runs": o["n"], "also_v6": o["option"] in v6_opts,
                         "option": o["option"], "fork": o["fork"]})
    both = sum(1 for x in disj if x["also_v6"])
    c = r.check("V7", "an option's label names one choice, not a list")
    c.measured(options=len(opts), disjunctive=len(disj), also_flagged_by_v6=both)
    c.against("lexical only -- it reads the label, never the members, so a "
              "genuinely single action described with an 'or' will fire")
    c.blind_to("an over-merged option with a clean label, which is the "
               "majority: V7 finds the ones that announce themselves")
    c.exhibit("options whose label lists alternatives", disj,
              worst=lambda x: (x["also_v6"], x["runs"]), show=a.show,
              columns=["runs", "also_v6", "option", "fork", "handle"],
              note="Enriched 8.3x for same-run merges on this corpus, so a "
                   "disjunctive label is a usable prior on over-merge even "
                   "before any member is read.")
    c.verdict("REVIEW" if disj else "PASS",
              f"{len(disj)} options carry a disjunctive label, {both} of them "
              f"also flagged by V6" if disj else "no disjunctive labels")
    print(f"V7  {len(disj):>4} disjunctive labels ({both} also V6)")

    # ---- V5 option counts ---------------------------------------------------
    wide = []
    for f, os_ in by_fork.items():
        runs = len({r for o in os_ for r in (o.get("runs") or [])})
        if runs >= 8 and len(os_) / runs >= 0.7:
            wide.append({"handle": h_fork(f), "options": len(os_),
                         "runs": runs, "ratio": round(len(os_) / runs, 2),
                         "fork": f, "stage": t.stage.get(f)})
    c = r.check("V5", "forks where nearly every run invented its own option")
    c.measured(flagged=len(wide), min_runs=8, min_ratio=0.7)
    c.against("no null -- these are simultaneously the most interesting and "
              "the least trustworthy forks, and only reading them separates "
              "the two")
    c.blind_to("an under-merged fork whose run count is low enough to fall "
               "under the >=8 floor, and any fork whose options are "
               "duplicated without inflating the per-run ratio")
    c.exhibit("forks with the most options per run", wide,
              worst=lambda x: (x["ratio"], x["runs"]), show=a.show,
              columns=["ratio", "options", "runs", "stage", "fork", "handle"],
              note="A fork with 22 options over 22 runs is either the most "
                   "contested object in the corpus or a clustering failure. "
                   "The shape is identical; only the content distinguishes "
                   "them.")
    c.verdict("INFO", f"{len(wide)} forks need a human read; no verdict is "
                      f"available from the shape alone")
    print(f"V5  {len(wide):>4} wide forks flagged")

    r.write()
    return 0


if __name__ == "__main__":
    sys.exit(main())
