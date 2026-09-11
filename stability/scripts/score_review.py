#!/usr/bin/env python3
"""Score a returned human benchmark packet. No model calls.

Answers the question every number in `stability/` has been waiting on: is the
pipeline's self-agreement good or bad? A rate of 0.70 means nothing until it
sits beside the rate two humans achieve on the same items.

WHAT IS COMPARED, AND WHY IT IS FAIR
------------------------------------
Each pair carries two model verdicts already: build A either grouped the items
or did not, and so did build B. That binary is the same one the rater answered.
So model-model agreement and human-human agreement are computed on identical
items, with identical response options, and can be placed in one column.

Human-human agreement is reported as mean PAIRWISE agreement across raters, not
as a majority-vs-individual rate. Majority agreement flatters: with three
raters the majority is right by construction and the number drifts upward with
rater count, which would make the human side look better simply for having more
people. Pairwise is what the two builds give us, so pairwise is what the humans
must give too.

THE READING, REGISTERED IN ADVANCE
----------------------------------
  human agreement on unstable pairs LOW    -> the pipeline is uncertain where
                                              the question is genuinely hard
  human agreement on unstable pairs HIGH   -> the instability is model noise

The script prints the comparison and refuses to choose between those readings
for you; it reports the numbers that decide it.

DISAGREED IS NOT THE SAME AS UNJUDGEABLE
----------------------------------------
The label on the sheet reads `unsure`, but the raters agreed what it means and
it is not uncertainty:

  UNJUDGEABLE -- the item does not say what the two lines DO, so there is no
  judgement to attempt.

That is a property of the item, and it is a different thing from two readers
understanding the item and reaching opposite conclusions:

  split        raters judged it and disagreed  -> the QUESTION is ambiguous
  unjudgeable  there was nothing to judge      -> the LABELS do not say

The two are never added together, and only `split` enters the difficulty score.

The clearest example is a pair of bare covariate lists -- "position only"
against "games, height, weight, age, yellowCards, goals, position, league".
Neither has a verb, and neither says which step of the analysis it belongs to,
so a reader cannot tell whether they are two rival adjustment sets at one fork
or the covariate sets of two different models. Every one of the twelve such
items in this packet came from two forks: "which covariates make up the model's
adjustment set?" and "Which control variables and functional forms enter the
regression model?"

So `unjudgeable` is not noise and not a rater failing. It measures how many
option labels name a set of variables without naming an operation, and it
points at the same two forks the part 3 audit asked to be re-merged.

AGREEMENT IS REPORTED TWICE, AND THE SECOND IS THE FAIR ONE
-----------------------------------------------------------
The model was never offered `unsure`; it must answer same or different. Scoring
a human `unsure` as a disagreement therefore penalises the human for an option
the model did not have. Both are printed: strict agreement over all answers,
and agreement over the rater-pairs where BOTH committed. The committed rate is
the one that belongs beside model-model.

ITEM DIFFICULTY
---------------
The stratum comparison above is coarse: it asks whether humans are worse on the
unstable third than on the stable two thirds. The item-level test is sharper.
Each pair gets scores from the raters alone -- split, unjudgeable, and
confidence -- computed WITHOUT looking at the model. Then we ask whether each
ranks the pairs the two builds disagreed about above the pairs they agreed on
(AUC, with a permutation null).

An AUC near 0.5 means human difficulty and model instability are unrelated: the
model is failing on items people find easy, which is a prompt problem. An AUC
well above 0.5 means the model breaks down exactly where the task is hard,
which is a task property and bounds what any pipeline can achieve. Which of the
three scores carries the AUC says which repair to attempt: `split` points at
the task, `unjudgeable` points at the distillation prompt.

The strata were SAMPLED on model agreement by construction (13/13/13 and
20/20/20), so the base rate here is an artifact of sampling. The AUC is a
ranking statistic and is unaffected by that; the raw prevalence is not
interpretable and is not reported as one.

CONFIDENCE IS NOT COMPARABLE ACROSS RATERS
------------------------------------------
The scale is 1-5, 1 low and 5 high. Raters use it differently -- one may never
go below 4. Raw means would then measure who is bold, not which item is hard.
Confidence is z-scored WITHIN rater before it is averaged, and the per-rater
usage is printed so the compression is visible rather than buried.

PART 3 IS A WORKSHEET, NOT A TEST
---------------------------------
Part 3 has no model-model counterpart -- it asks a human to audit a whole fork
-- and the first run showed it is not really a measurement at all. Scored as
one it looks poor: three raters agree on the verdict about half the time and
one of them flagged nothing. Read as a worksheet it is the most productive page
in the packet, because the free text said something the labels could not:

    "Transformation of games should be its own fork."
    "One fork about how to transform variables and another on what to include."
    "Or reorganize with the skin tone fork above."

Those are instructions. `over-merged` only says something is wrong; a re-merge
axis says what to do, and it can be handed back to the pipeline. So part 3 is
reported as a QUEUE OF PROPOSALS -- what was flagged, by whom, and what they
said to do about it -- with the agreement figures kept but demoted to context.

Low agreement here is not automatically a defect. Raters who flag different
forks may be proposing the SAME re-merge from different ends, and the script
looks for that: forks that different raters connect to each other are gathered
into one proposal rather than counted as two disagreements.

A rater who flags nothing is reported by name, because a page of `correct` is a
fact about how the sheet was used and not a clean bill of health.

GOLD CHECKS, AND WHEN THE GOLD IS WRONG
---------------------------------------
Gold pairs exist to catch a rater who is not reading. They only do that if the
answer really is obvious. Two guards keep a gold failure from meaning the wrong
thing:

  `unsure` is never a gold failure. The packet's own rules license it, and
  under the raters' definition it says the text is insufficient -- which is an
  observation about the item, not a wrong answer to it.

  A gold item that MOST raters answer against is a failed ITEM. Independent
  readers converging on the other answer is evidence about the pair, not about
  the readers. Such an item is reported, excluded, and the raters are judged on
  what remains.

This matters because `gold_same` pairs are drawn from two decisions the
PIPELINE assigned to one option. If the pair is not also obviously the same by
its wording, the check asks whether the rater agrees with the pipeline -- which
is the thing under test. Scoring dissent as disengagement would let a hard item
disqualify the humans and quietly flatter the model.

Usage:
    python3 stability/scripts/score_review.py --packet reviews/human-benchmark
        [--json out.json]
"""
import argparse
import csv
import json
import math
import random
from collections import defaultdict
from itertools import combinations
from pathlib import Path

# Confidence is 1-5, 1 low and 5 high, as the raters agreed before rating. An
# earlier draft of the packet asked for words; those are mapped onto the same
# scale so an old sheet still reads. Anything else is dropped, not guessed at.
CONF_WORDS = {"high": 5.0, "medium": 3.0, "med": 3.0, "low": 1.0}

# Part 3 verdicts, as written by hand. The packet asked for hyphens; sheets came
# back without them. A sheet saying both errors are present is kept as its own
# label rather than collapsed, because "this fork is wrong in two ways" is a
# stronger statement than either half.
AUDIT_VERDICTS = {
    "correct": "correct",
    "over-merged": "over-merged",
    "overmerged": "over-merged",
    "over merged": "over-merged",
    "split": "over-merged",
    "under-merged": "under-merged",
    "undermerged": "under-merged",
    "under merged": "under-merged",
    "absorb": "under-merged",
    "move": "move",
    "over-merged and under-merged": "both",
    "overmerged and undermerged": "both",
    "both": "both",
    "unsure": "unsure",
}
FLAGS = ("over-merged", "under-merged", "both", "move")


def _rows(p):
    """Data rows of a hand-edited CSV: comments and blank lines removed.

    The blank spacer line the templates put before the header is not a comment
    and does not start with '#'. Taking rows[0] without dropping it makes the
    header an empty list, every column lookup fail, and the sheet read as
    unreturned -- which is exactly what happened the first time this ran.
    """
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8-sig") as fh:
        return [r for r in csv.reader(fh)
                if r and any(c.strip() for c in r)
                and not r[0].lstrip().startswith("#")]


def _find(d, stem):
    """The sheet for one part, whatever the rater renamed it to.

    Sheets come back as `1_option_pairs_<rater>.csv`, `1_option_pairs.csv`, and so
    on. Blank templates parked in a subdirectory are not matched, because glob
    does not descend.
    """
    hits = sorted(d.glob(stem + "*.csv"))
    return hits[0] if hits else None


def read_sheet(p):
    """{pair_id: {verdict, confidence, note}} for a part 1 or part 2 sheet."""
    rows = _rows(p) if p else []
    if not rows:
        return {}
    hdr = rows[0]
    try:
        i_id, i_v = hdr.index("pair_id"), hdr.index("verdict")
    except ValueError:
        return {}
    i_c = hdr.index("confidence") if "confidence" in hdr else None
    i_n = hdr.index("note") if "note" in hdr else None
    out = {}
    for r in rows[1:]:
        if len(r) <= i_v or not r[i_id].strip():
            continue
        v = r[i_v].strip().lower()
        if not v:
            continue
        c = None
        if i_c is not None and len(r) > i_c:
            raw = r[i_c].strip().lower()
            if raw in CONF_WORDS:
                c = CONF_WORDS[raw]
            else:
                try:
                    c = float(raw)
                except ValueError:
                    c = None
        out[r[i_id].strip()] = {
            "verdict": v, "conf": c,
            "note": (r[i_n].strip() if i_n is not None and len(r) > i_n else "")}
    return out


def read_audit(p):
    """{fork_text: {verdict, note, runs, coverage, n_options, eff_options}}."""
    rows = _rows(p) if p else []
    if not rows:
        return {}
    hdr = rows[0]
    if "fork" not in hdr or "verdict" not in hdr:
        return {}
    ix = {k: hdr.index(k) for k in hdr}
    out = {}
    for r in rows[1:]:
        if len(r) <= ix["verdict"] or not r[ix["fork"]].strip():
            continue
        raw = r[ix["verdict"]].strip().lower()
        if not raw:
            continue

        def num(k):
            try:
                return float(r[ix[k]])
            except (KeyError, IndexError, ValueError):
                return None
        out[r[ix["fork"]].strip()] = {
            "verdict": AUDIT_VERDICTS.get(raw, raw), "raw": raw,
            "note": (r[ix["note"]].strip()
                     if "note" in ix and len(r) > ix["note"] else ""),
            # `remerge` is the column added after the first run; older sheets
            # carry the instruction in `note`, so both are read and joined.
            "remerge": (r[ix["remerge"]].strip()
                        if "remerge" in ix and len(r) > ix["remerge"] else ""),
            "runs": num("runs"), "coverage": num("coverage"),
            "n_options": num("n_options"), "eff_options": num("eff_options"),
            "modal_share": num("modal_share")}
    return out


def pairwise(labels):
    """(agreeing rater-pairs, total rater-pairs) for one item."""
    ok = tot = 0
    for a, b in combinations(labels, 2):
        tot += 1
        ok += (a == b)
    return ok, tot


def pairwise_committed(labels):
    """Agreement over rater-pairs where BOTH committed.

    `unsure` here means the description does not carry enough to decide, and
    the model was never offered that answer. Counting it as a disagreement
    scores the human against an option the model did not have.
    """
    ok = tot = 0
    for a, b in combinations(labels, 2):
        if a == "unsure" or b == "unsure":
            continue
        tot += 1
        ok += (a == b)
    return ok, tot


def binom_p(k, n, p=0.5):
    """Exact two-sided binomial p, by summing outcomes no more likely than k."""
    if not n:
        return None

    def pmf(i):
        return math.comb(n, i) * p ** i * (1 - p) ** (n - i)
    obs = pmf(k)
    return min(1.0, sum(pmf(i) for i in range(n + 1) if pmf(i) <= obs + 1e-12))


def zscores(vals):
    """Within-rater z-scores; a rater with no spread contributes zeros."""
    xs = [v for v in vals.values() if v is not None]
    if len(xs) < 2:
        return {k: 0.0 for k in vals}
    m = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))
    if sd == 0:
        return {k: 0.0 for k in vals}
    return {k: (None if v is None else (v - m) / sd) for k, v in vals.items()}


def auc(scores, labels):
    """Rank AUC of `scores` against binary `labels`, ties counted as half."""
    pos = [s for s, y in zip(scores, labels) if y]
    neg = [s for s, y in zip(scores, labels) if not y]
    if not pos or not neg:
        return None
    tot = 0.0
    for p in pos:
        for n in neg:
            tot += 1.0 if p > n else (0.5 if p == n else 0.0)
    return tot / (len(pos) * len(neg))


def auc_perm_p(scores, labels, reps=20000, seed=7):
    """Two-sided permutation p for AUC != 0.5, shuffling the labels."""
    obs = auc(scores, labels)
    if obs is None:
        return None, None
    rng = random.Random(seed)
    ys, hit = list(labels), 0
    for _ in range(reps):
        rng.shuffle(ys)
        if abs(auc(scores, ys) - 0.5) >= abs(obs - 0.5) - 1e-12:
            hit += 1
    return obs, (hit + 1) / (reps + 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", required=True)
    ap.add_argument("--json")
    ap.add_argument("--perm", type=int, default=20000,
                    help="permutation reps for the difficulty AUC null")
    x = ap.parse_args()
    root = Path(x.packet)
    key = json.loads((root / "KEY-do-not-open.json").read_text(encoding="utf-8"))

    meta = {}
    for part, rows in (("option", key["part1_option_pairs"]),
                       ("fork", key["part2_fork_pairs"])):
        for r in rows:
            meta[r["pair_id"]] = {"part": part, "stratum": r["stratum"],
                                  "model_a": r["model_a"],
                                  "model_b": r["model_b"],
                                  "a_text": r.get("a_text", ""),
                                  "b_text": r.get("b_text", "")}
    audit_strata = key.get("part3_audit_strata", {})

    sheets, audits = {}, {}
    raters = sorted(d for d in root.glob("rater-*") if d.is_dir())
    for d in raters:
        s = {}
        s.update(read_sheet(_find(d, "1_option_pairs")))
        s.update(read_sheet(_find(d, "2_fork_pairs")))
        sheets[d.name] = s
        audits[d.name] = read_audit(_find(d, "3_fork_audit"))

    returned = {k: v for k, v in sheets.items() if v}
    if len(returned) < 2:
        print(f"{len(returned)} sheet(s) returned of {len(raters)}. "
              f"Human-human agreement needs at least two.")
        for k, v in sheets.items():
            print(f"  {k}: {len(v)} rated")
        return

    # ---- gold checks -------------------------------------------------------
    gold_ids = sorted(p for p, m in meta.items() if m["stratum"].startswith("gold"))

    # Step 1: retire gold items the raters converged against. A majority of
    # independent readers answering the other way is evidence about the item.
    bad_gold = {}
    for pid in gold_ids:
        want = "same" if meta[pid]["stratum"] == "gold_same" else "different"
        vs = [returned[r][pid]["verdict"] for r in returned if pid in returned[r]]
        committed = [v for v in vs if v != "unsure"]
        if committed and sum(1 for v in committed if v != want) * 2 >= len(committed):
            bad_gold[pid] = vs
    live_gold = [p for p in gold_ids if p not in bad_gold]

    # Step 2: judge each rater on the gold that survived. `unsure` abstains.
    failed = {}
    for r, s in returned.items():
        bad = []
        for pid in live_gold:
            if pid not in s:
                continue
            want = "same" if meta[pid]["stratum"] == "gold_same" else "different"
            v = s[pid]["verdict"]
            if v != "unsure" and v != want:
                bad.append(pid)
        if bad:
            failed[r] = bad
    good = {k: v for k, v in returned.items() if k not in failed}
    res_gold = {"items": len(gold_ids), "retired": sorted(bad_gold),
                "live": live_gold}

    print(f"HUMAN BENCHMARK  ({len(returned)} sheets returned of "
          f"{len(raters)})\n")
    for r in sorted(returned):
        n_opt = sum(1 for p in returned[r] if meta.get(p, {}).get("part") == "option")
        n_frk = sum(1 for p in returned[r] if meta.get(p, {}).get("part") == "fork")
        print(f"  {r:<10}part1 {n_opt:>3}   part2 {n_frk:>3}   "
              f"part3 {len(audits.get(r, {})):>3}")
    print()
    if bad_gold:
        print("  GOLD ITEMS RETIRED -- the raters converged against the key,")
        print("  so the item is not obvious and cannot test engagement:")
        for pid, vs in sorted(bad_gold.items()):
            want = "same" if meta[pid]["stratum"] == "gold_same" else "different"
            print(f"    {pid}  key says {want}, raters said {'/'.join(vs)}")
            print(f"        A: {meta[pid]['a_text'][:88]}")
            print(f"        B: {meta[pid]['b_text'][:88]}")
        print(f"    {len(live_gold)} of {len(gold_ids)} gold pairs still live\n")
    if failed:
        print("  GOLD CHECK FAILED -- excluded from the headline:")
        for r, bad in failed.items():
            print(f"    {r}: missed {len(bad)} gold pair(s) {bad[:4]}")
        print()
    else:
        print(f"  gold check passed by every returned sheet "
              f"({len(live_gold)} live pairs)\n")
    if len(good) < 2:
        print("  fewer than two sheets pass the gold check; nothing to report")
        return

    res = {"raters_returned": len(returned), "raters_scored": len(good),
           "gold_failures": {k: v for k, v in failed.items()},
           "gold": res_gold,
           "hypothesis": key.get("hypothesis"), "strata": {}}

    # ---- how each rater used the confidence scale ---------------------------
    print("  CONFIDENCE USE  (1-5; word scales mapped high/medium/low = 5/3/1)")
    print(f"    {'rater':<10}{'n':>5}{'mean':>7}{'sd':>7}{'min':>5}{'max':>5}"
          f"{'unsure':>8}")
    res["confidence_use"] = {}
    for r in sorted(good):
        cs = [a["conf"] for a in good[r].values() if a["conf"] is not None]
        un = sum(1 for a in good[r].values() if a["verdict"] == "unsure")
        if cs:
            m = sum(cs) / len(cs)
            sd = math.sqrt(sum((c - m) ** 2 for c in cs) / max(1, len(cs) - 1))
            print(f"    {r:<10}{len(cs):>5}{m:>7.2f}{sd:>7.2f}"
                  f"{min(cs):>5.0f}{max(cs):>5.0f}"
                  f"{un / len(good[r]):>8.2f}")
            res["confidence_use"][r] = {
                "n": len(cs), "mean": round(m, 3), "sd": round(sd, 3),
                "min": min(cs), "max": max(cs),
                "unsure_rate": round(un / len(good[r]), 4)}
    print()

    # ---- the three-way table, per part -------------------------------------
    # Three agreements on identical items:
    #   rater x rater   two people
    #   rater x build A one person against the pipeline
    #   A x B           two pipeline runs
    #
    # The third is 1.00 or 0.00 by construction, because the strata were
    # DEFINED by whether A and B matched. It is printed to make that visible,
    # not as a measurement. The comparison that carries meaning is the first
    # two: if a rater agrees with build A about as often as with another
    # rater, the pipeline is performing like a person on that stratum.
    # WEIGHTING. Two averages are possible and they differ by up to 0.09 here.
    #
    #   PER-ITEM  score each item, then average the item scores.
    #   POOLED    sum all matching judgement-pairs over all judgement-pairs.
    #
    # Pooled lets an item all three raters could judge carry three times the
    # weight of one only two could. Whether an item is judgeable is not random
    # -- it tracks a kind of item, the bare covariate lists -- so pooling
    # quietly up-weights one part of the sample. Items were the sampling unit,
    # so PER-ITEM is the estimator that matches the design and is reported
    # first. Pooled is printed beside it so the choice is visible and can be
    # checked rather than taken on trust.
    print("  BY PART -- three agreements on identical items")
    print("  Per-item averages (pooled in brackets). `A x B` is 1.00/0.00 BY")
    print("  CONSTRUCTION -- the strata are defined by it -- so compare")
    print("  `rater x A` against `rater x rater`, not against `A x B`.")
    res["by_part"] = {}
    for part, title in (("option", "PART 1 -- same action?"),
                        ("fork", "PART 2 -- same decision point?")):
        print(f"\n    {title}")
        print(f"      {'stratum':<13}{'items':>6}{'unjudg':>8}"
              f"{'rater x rater':>22}{'rater x A':>20}{'A x B':>7}")
        for st in ("stable_same", "stable_diff", "unstable"):
            pids = [p for p, m in meta.items()
                    if m["part"] == part and m["stratum"] == st]
            rr_ok = rr_n = ra_ok = ra_n = uj = tot = 0
            rr_i, ra_i = [], []
            for p in pids:
                vs = [good[r][p]["verdict"] for r in good if p in good[r]]
                tot += len(vs)
                uj += sum(1 for v in vs if v == "unsure")
                com = [v for v in vs if v in ("same", "different")]
                o, n = pairwise(com)
                rr_ok += o
                rr_n += n
                if n:
                    rr_i.append(o / n)
                a_says = "same" if meta[p]["model_a"] else "different"
                hit = sum(1 for v in com if v == a_says)
                ra_n += len(com)
                ra_ok += hit
                if com:
                    ra_i.append(hit / len(com))
            if not (rr_n and ra_n):
                continue
            ab = 1.0 if st != "unstable" else 0.0
            rr_pi, ra_pi = sum(rr_i) / len(rr_i), sum(ra_i) / len(ra_i)
            print(f"      {st:<13}{len(pids):>6}{uj / tot:>8.3f}"
                  f"{rr_pi:>15.3f} [{rr_ok / rr_n:.3f}]"
                  f"{ra_pi:>13.3f} [{ra_ok / ra_n:.3f}]{ab:>7.2f}")
            res["by_part"][f"{part}:{st}"] = {
                "items": len(pids), "unjudgeable": round(uj / tot, 4),
                "rater_x_rater": round(rr_pi, 4),
                "rater_x_rater_pooled": round(rr_ok / rr_n, 4),
                "rater_x_rater_items": len(rr_i),
                "rater_x_buildA": round(ra_pi, 4),
                "rater_x_buildA_pooled": round(ra_ok / ra_n, 4),
                "rater_x_buildA_items": len(ra_i),
                "buildA_x_buildB": ab}
    print()

    # ---- who agrees with whom ----------------------------------------------
    # A mean over rater-pairs hides an outlier. If one rater is carrying the
    # disagreement, the headline is about that rater and not about the task.
    print("  BY RATER PAIR  (parts 1-2, committed answers only)")
    res["rater_pairs"] = {}
    for a, b in combinations(sorted(good), 2):
        shared = [p for p in good[a] if p in good[b]
                  and not meta.get(p, {}).get("stratum", "").startswith("gold")]
        ok = n = 0
        for p in shared:
            o, t = pairwise_committed([good[a][p]["verdict"],
                                       good[b][p]["verdict"]])
            ok += o
            n += t
        if n:
            print(f"    {a} x {b}   {ok / n:.3f}   ({n} committed of "
                  f"{len(shared)})")
            res["rater_pairs"][f"{a}|{b}"] = {"agreement": round(ok / n, 4),
                                              "committed": n,
                                              "shared": len(shared)}
    print()

    # ---- agreement per stratum ---------------------------------------------
    print("  AGREEMENT.  `committed` drops rater-pairs where either said")
    print("  unsure -- the model had no such option, so that is the column")
    print("  that belongs beside model-model.")
    print(f"  {'part':<7}{'stratum':<14}{'pairs':>6}{'strict':>9}"
          f"{'committed':>11}{'model':>9}{'unsure':>9}")
    for part in ("option", "fork"):
        for st in ("stable_same", "stable_diff", "unstable"):
            pids = [p for p, m in meta.items()
                    if m["part"] == part and m["stratum"] == st]
            hh, hn, ch, cn, un, tot = 0, 0, 0, 0, 0, 0
            for p in pids:
                ans = [good[r][p]["verdict"] for r in good if p in good[r]]
                if len(ans) < 2:
                    continue
                tot += 1
                un += sum(1 for a in ans if a == "unsure")
                ok, n = pairwise(ans)
                hh += ok
                hn += n
                ok2, n2 = pairwise_committed(ans)
                ch += ok2
                cn += n2
            if not tot:
                continue
            mm = sum(1 for p in pids
                     if meta[p]["model_a"] == meta[p]["model_b"]) / len(pids)
            row = {"pairs_rated": tot,
                   "human_human": round(hh / hn, 4) if hn else None,
                   "human_human_committed": round(ch / cn, 4) if cn else None,
                   "committed_pairs": cn,
                   "model_model": round(mm, 4),
                   "unsure_rate": round(un / (tot * len(good)), 4)}
            res["strata"][f"{part}:{st}"] = row
            cc = ("     --" if row["human_human_committed"] is None
                  else format(row["human_human_committed"], ">11.4f"))
            print(f"  {part:<7}{st:<14}{tot:>6}{row['human_human']:>9.4f}"
                  f"{cc}{row['model_model']:>9.4f}{row['unsure_rate']:>9.4f}")

    # ---- the registered comparison -----------------------------------------
    # The gap MUST be read on the committed basis. On the strict basis an
    # `unjudgeable` answer counts as a disagreement, and unjudgeable items are
    # not spread evenly -- they concentrate in the `unstable` stratum (0.128
    # against 0.051 and 0.026 in part 1). Counting them as disagreement
    # therefore penalises exactly the stratum under test and manufactures a
    # gap. The first reading of this packet reported +0.295 and +0.152 that
    # way; on the committed basis they are +0.141 and -0.009.
    print()
    print("  THE REGISTERED COMPARISON")
    print("  Per-item, committed basis. The strict basis is shown for")
    print("  comparison only: it counts `unjudgeable` as disagreement, and")
    print("  those items cluster in the disputed stratum, so it inflates the")
    print("  gap it is meant to measure.")
    for part in ("option", "fork"):
        rows = {st: res["by_part"].get(f"{part}:{st}")
                for st in ("stable_same", "stable_diff", "unstable")}
        if not all(rows.values()):
            continue
        ns = rows["stable_same"]["items"] + rows["stable_diff"]["items"]
        stable = (rows["stable_same"]["rater_x_rater"]
                  * rows["stable_same"]["items"]
                  + rows["stable_diff"]["rater_x_rater"]
                  * rows["stable_diff"]["items"]) / ns
        u = rows["unstable"]["rater_x_rater"]
        gap = stable - u
        res.setdefault("verdict", {})[part] = {
            "human_on_stable": round(stable, 4), "human_on_unstable": round(u, 4),
            "gap": round(gap, 4), "basis": "per-item, committed"}
        print(f"\n    {part.upper()} LEVEL")
        print(f"      raters agree on pairs the runs agree on    {stable:.3f}")
        print(f"      raters agree on pairs the runs DISPUTE     {u:.3f}")
        print(f"      gap                                        {gap:+.3f}")
        if gap > 0.15:
            print(f"      -> raters also find the disputed pairs hard, so that")
            print(f"         instability tracks genuine ambiguity")
        elif gap < 0.05:
            print(f"      -> raters agree on the disputed pairs as readily as")
            print(f"         on any other, so that instability is not tracking")
            print(f"         how hard the question is")
        else:
            print(f"      -> intermediate; neither registered reading is")
            print(f"         clearly supported")
    print()

    # ---- the pool-weighted rate, and what it is not ------------------------
    # Strata were sampled 13/13/13 and 20/20/20, which is not how they occur.
    # Reweighting by the pool the packet drew from recovers the rate over that
    # pool -- for BOTH sides, on the same items, so the two are comparable.
    #
    # It is NOT an ARI. ARI is chance-corrected and this is raw pair agreement,
    # so the two must not be set side by side. Nor is the pool the natural
    # population: `review_sheet` restricts option pairs to within one fork of
    # build A, restricts fork pairs to those at least one build co-forked, and
    # then INJECTS lexically-similar hard negatives into fork `stable_diff`.
    # Part of that stratum is therefore synthetic, and its weight is an
    # artifact of how many negatives were injected. The weights are printed so
    # that is visible rather than buried in a single number.
    pools = key.get("pool_sizes") or {}
    restricted = key.get("pool_restricted") or {}
    injected = key.get("pool_injected_negatives") or {}
    if pools:
        print("  POOL-WEIGHTED  (strata reweighted to the pool the packet drew")
        print("  from; raw pair agreement, NOT an ARI, and not chance-corrected)")
        res["pool_weighted"] = {}
        for part in ("option", "fork"):
            pl = pools.get(part) or {}
            tot = sum(pl.values())
            if not tot:
                continue
            hw = mw = wsum = 0.0
            parts = []
            for st, npool in sorted(pl.items()):
                row = res["strata"].get(f"{part}:{st}")
                if not row or row["human_human_committed"] is None:
                    continue
                w = npool / tot
                hw += w * row["human_human_committed"]
                mw += w * row["model_model"]
                wsum += w
                parts.append(f"{st} {w:.3f}")
            if not wsum:
                continue
            hw, mw = hw / wsum, mw / wsum

            # Is this pool restricted to pairs at least one build grouped? An
            # older KEY does not say, so fall back to the signature of one:
            # a `stable_diff` cell too small to be a real population of
            # separated pairs.
            share_diff = pl.get("stable_diff", 0) / tot
            is_restricted = restricted.get(
                part, share_diff < 0.05 and pl.get("unstable", 0) > tot / 2)
            entry = {"human": round(hw, 4),
                     "weights": {st: round(n / tot, 4) for st, n in pl.items()},
                     "restricted": bool(is_restricted)}

            if is_restricted:
                a = pl.get("stable_same", 0)
                bc = pl.get("unstable", 0)
                jac = a / (a + bc) if (a + bc) else float("nan")
                print(f"    {part.upper():<8} human {hw:.3f}   "
                      f"model NOT COMPARABLE -- see below")
                print(f"             weights: {', '.join(parts)}")
                print(f"      This pool keeps only pairs at least one build")
                print(f"      grouped, and its stable_diff cell "
                      f"({pl.get('stable_diff', 0)}"
                      + (f", {injected[part]} injected" if part in injected
                         else "") + f") is not a real")
                print(f"      population of separated pairs. A model rate over")
                print(f"      it is Jaccard on co-membership, "
                      f"a/(a+b+c) = {jac:.3f},")
                print(f"      and {pl.get('unstable', 0) / tot:.0%} of the "
                      f"weight sits in a stratum whose")
                print(f"      model agreement is 0 BY DEFINITION. The pool was")
                print(f"      selected on the model's disagreements and on")
                print(f"      nobody else's, so printing it opposite the human")
                print(f"      rate would be selection on the outcome for one")
                print(f"      side. Use the per-stratum rows and the AUC.")
                entry.update({"model": None, "jaccard_co_membership":
                              round(jac, 4),
                              "why_no_model_rate":
                              "pool restricted to pairs at least one build "
                              "grouped, with synthetic negatives; a model rate "
                              "over it restates the pool's construction"})
            else:
                print(f"    {part.upper():<8} human {hw:.3f}   model {mw:.3f}"
                      f"   gap {mw - hw:+.3f}")
                print(f"             weights: {', '.join(parts)}")
                entry.update({"model": round(mw, 4), "gap": round(mw - hw, 4)})
            res["pool_weighted"][part] = entry
        print()

    # ---- validity: does the human majority agree with the builds? ----------
    # Everything above measures RELIABILITY -- whether two doers agree with
    # themselves. Reliability is blind to a bias both builds share: two runs
    # that make the same mistake agree perfectly. The humans are a third,
    # independent party, so they are the only thing here that can detect one.
    #
    # This section is not affected by how the strata were sized. It asks, for
    # each stratum separately, whether the human majority endorses what the
    # builds did -- and on the disputed pairs, which way humans lean. That
    # direction is the actionable part: a pipeline that errs toward `same` is
    # over-grouping and needs a stricter prompt, one that errs toward
    # `different` is fragmenting and needs a looser one.
    print("  VALIDITY  (do the humans endorse BUILD A, per stratum?)")
    print("  Reliability cannot see a bias both builds share. This can.")
    print("  Every item a rater saw is build A's text -- A's decisions, A's")
    print("  option labels, A's forks. Build B never appears on a sheet; it")
    print("  only defines the strata. So these are endorsements of A, sorted")
    print("  by whether B happened to concur.")
    print(f"  {'part':<7}{'stratum':<14}{'n':>4}{'A said':>10}"
          f"{'humans say same':>17}{'endorse':>9}{'binom p':>10}")
    res["validity"] = {}
    for part in ("option", "fork"):
        for st in ("stable_same", "stable_diff", "unstable"):
            pids = [p for p, m in meta.items()
                    if m["part"] == part and m["stratum"] == st]
            n_same = n_dec = 0
            for p in pids:
                vs = [good[r][p]["verdict"] for r in good if p in good[r]]
                vs = [v for v in vs if v in ("same", "different")]
                if not vs:
                    continue
                s, d = vs.count("same"), vs.count("different")
                if s == d:
                    continue          # a tied panel endorses nothing
                n_dec += 1
                n_same += (s > d)
            if not n_dec:
                continue
            share_same = n_same / n_dec
            if st == "stable_same":
                built, endorse = "same", share_same
            elif st == "stable_diff":
                built, endorse = "different", 1 - share_same
            else:
                built, endorse = "split", None
            # On stable_* the null is "humans endorse at chance". On unstable
            # there is nothing to endorse, so the test is whether the lean
            # differs from an even split -- which way induction errs.
            pv = binom_p(n_same, n_dec)
            print(f"  {part:<7}{st:<14}{n_dec:>4}{built:>10}"
                  f"{share_same:>17.3f}"
                  f"{'      --' if endorse is None else format(endorse, '>9.3f')}"
                  f"{pv:>10.4f}")
            res["validity"][f"{part}:{st}"] = {
                "n_decided": n_dec, "a_said": built,
                "human_majority_same": round(share_same, 4),
                "endorsement": None if endorse is None else round(endorse, 4),
                "binom_p_vs_even": round(pv, 5)}
    print()
    # The pairs where the human majority contradicts BOTH builds. These are the
    # only places in the packet where a mistake the two runs SHARE becomes
    # visible: agreement between runs cannot reveal it, by definition.
    #
    # Raters applied the foreclosure test strictly -- "same" only where taking
    # one option really does rule out the other. That makes a majority "same"
    # against two builds that separated the pair a strong signal, and a
    # majority "different" against two builds that grouped it a weak one.
    contra = []
    for pid, m in meta.items():
        if m["stratum"].startswith("gold") or m["model_a"] != m["model_b"]:
            continue
        vs = [good[r][pid]["verdict"] for r in good if pid in good[r]]
        vs = [v for v in vs if v in ("same", "different")]
        if not vs:
            continue
        s, d = vs.count("same"), vs.count("different")
        if s == d:
            continue
        human = "same" if s > d else "different"
        built = "same" if m["model_a"] else "different"
        if human != built:
            contra.append((pid, m, human, built, vs))
    print(f"    {len(contra)} pairs where the human majority contradicts BOTH "
          f"builds --")
    print("    the only place a shared pipeline error can show up:")
    for pid, m, human, built, vs in sorted(
            contra, key=lambda c: (c[3] != "different", c[0])):
        flag = ("  <- both builds separated these; humans call them rivals"
                if built == "different" else "")
        print(f"      {pid} [{m['stratum']:<12}] builds {built}, "
              f"humans {human} ({'/'.join(vs)}){flag}")
        print(f"          A: {m['a_text'][:82]}")
        print(f"          B: {m['b_text'][:82]}")
    res["contradicts_both_builds"] = [
        {"pair_id": p, "stratum": m["stratum"], "builds": b, "humans": h,
         "verdicts": v, "a_text": m["a_text"], "b_text": m["b_text"]}
        for p, m, h, b, v in contra]
    print()
    print("    `humans say same` is the share of panels whose majority called")
    print("    the pair one thing. On stable_same the builds said same, so a")
    print("    LOW value there is the builds over-grouping in a way no")
    print("    self-agreement number can reveal. On unstable there is no")
    print("    endorsement to compute -- the builds split -- but the lean says")
    print("    which way induction errs when it errs.")
    print()

    # ---- item difficulty ---------------------------------------------------
    # Built from the raters only. The model's verdicts are used to TEST it, and
    # never to build it.
    zconf = {r: zscores({p: a["conf"] for p, a in good[r].items()})
             for r in good}
    items = {}
    for pid, m in meta.items():
        if m["stratum"].startswith("gold"):
            continue
        ans = [(r, good[r][pid]) for r in good if pid in good[r]]
        if len(ans) < 2:
            continue
        labels = [a["verdict"] for _, a in ans]
        ok, tot = pairwise_committed(labels)
        zs = [zconf[r][pid] for r, _ in ans if zconf[r].get(pid) is not None]
        items[pid] = {
            "part": m["part"], "stratum": m["stratum"],
            # `split` counts only rater-pairs that BOTH committed, so it is
            # ambiguity of the question and not shortage of information. An
            # item nobody committed on has no split to measure.
            "split": None if not tot else round(1 - ok / tot, 4),
            "committed_pairs": tot,
            "unjudgeable": round(
                sum(1 for a in labels if a == "unsure") / len(labels), 4),
            "z_conf": round(sum(zs) / len(zs), 4) if zs else 0.0,
            "labels": labels,
            "model_disagree": int(m["model_a"] != m["model_b"]),
            "a_text": m["a_text"], "b_text": m["b_text"]}
    # Difficulty is `split` and confidence ONLY. `unjudgeable` is
    # deliberately excluded.
    #
    # The raters reported that when they answered `unsure` they were not
    # saying the item was hard -- they were saying the packet had not told
    # them what the two lines DO, so there was no judgement to attempt. The
    # clearest case is a pair of bare covariate lists: "position only" against
    # "games, height, weight, age, yellowCards, goals, position, league". With
    # no verb and no indication of which step each belongs to, a reader cannot
    # tell whether these are two adjustment sets rivalling each other at one
    # fork or the covariate sets of two different models.
    #
    # Adding that to a difficulty score would measure the packet, not the
    # item. It is reported on its own instead, under LABELS THAT CANNOT BE
    # JUDGED, where it belongs -- as evidence about the option labels.
    for it in items.values():
        it["difficulty"] = round((it["split"] or 0.0) - it["z_conf"] / 4, 4)

    print("  ITEM DIFFICULTY  (from raters only; the model is not used to "
          "build it)")
    print("    split = raters committed and disagreed (the question is hard)")
    print("    under = raters said unsure (the text cannot settle it)")
    print()
    print(f"    {'part':<8}{'items':>6}{'split':>8}{'under':>8}"
          f"{'  AUC of':>10}{'split':>8}{'under':>8}{'conf':>8}"
          f"{'  combined':>11}{'perm p':>9}{'  judgeable only':>18}{'perm p':>9}")
    res["difficulty"] = {}
    for part in ("option", "fork", "both"):
        sel = [it for it in items.values()
               if part == "both" or it["part"] == part]
        if len(sel) < 4:
            continue
        y = [it["model_disagree"] for it in sel]
        # An item where fewer than two raters committed has NO measurable
        # split. Scoring it 0.0 would rank it as the easiest item in the set,
        # which is the opposite of what it is, so it is dropped from every
        # split-based AUC rather than defaulted.
        hs = [it for it in sel if it["split"] is not None]
        ys = [it["model_disagree"] for it in hs]
        a_sp = auc([it["split"] for it in hs], ys)
        a_un = auc([it["unjudgeable"] for it in sel], y)
        # Low confidence should mean hard, so the sign is flipped.
        a_cf = auc([-it["z_conf"] for it in sel], y)
        a, p = auc_perm_p([it["difficulty"] for it in hs], ys, reps=x.perm)
        # The same test on items every rater could actually judge. This is the
        # one to quote: an item nobody could attempt contributes a difficulty
        # score that reflects the packet rather than the question.
        cl = [it for it in hs if it["unjudgeable"] == 0]
        a_cl, p_cl = ((None, None) if len(cl) < 4 else
                      auc_perm_p([it["difficulty"] for it in cl],
                                 [it["model_disagree"] for it in cl],
                                 reps=x.perm))
        sp = [i["split"] for i in sel if i["split"] is not None]
        row = {"items": len(sel),
               "mean_split": round(sum(sp) / len(sp), 4) if sp else None,
               "mean_unjudgeable": round(
                   sum(i["unjudgeable"] for i in sel) / len(sel), 4),
               "auc_split": None if a_sp is None else round(a_sp, 4),
               "auc_unjudgeable": None if a_un is None else round(a_un, 4),
               "auc_low_confidence": None if a_cf is None else round(a_cf, 4),
               "auc_combined": None if a is None else round(a, 4),
               "perm_p": None if p is None else round(p, 5)}
        res["difficulty"][part] = row

        def f(v, w=8):
            return "      --" if v is None else format(v, f">{w}.3f")
        row["items_judgeable"] = len(cl)
        row["auc_judgeable_only"] = None if a_cl is None else round(a_cl, 4)
        row["perm_p_judgeable_only"] = None if p_cl is None else round(p_cl, 5)
        print(f"    {part:<8}{row['items']:>6}{f(row['mean_split'])}"
              f"{f(row['mean_unjudgeable'])}{'':>10}"
              f"{f(a_sp)}{f(a_un)}{f(a_cf)}{f(a, 11)}"
              f"{'       --' if p is None else format(p, '>9.4f')}"
              f"{f(a_cl, 18)}"
              f"{'       --' if p_cl is None else format(p_cl, '>9.4f')}")
    print()
    print("    AUC = P(a pair the builds disputed scores harder than one they")
    print("    agreed on). 0.5 is no relation. Strata were sampled on model")
    print("    agreement, so the base rate is by construction; the ranking is")
    print("    not. The column carrying the signal says where the repair is:")
    print("    `split` points at the task, `under` at the distilled text.")
    print()

    # Where the humans themselves broke down, regardless of the model.
    hardest = sorted(items.items(), key=lambda kv: -kv[1]["difficulty"])[:8]
    print("  HARDEST ITEMS BY HUMAN DISAGREEMENT")
    for pid, it in hardest:
        print(f"    {pid}  {it['part']:<7}{it['stratum']:<13}"
              f"d={it['difficulty']:.2f}  {'/'.join(it['labels'])}")
        print(f"        A: {it['a_text'][:88]}")
        print(f"        B: {it['b_text'][:88]}")
    print()
    res["hardest_items"] = [
        {"pair_id": p, **{k: v for k, v in it.items()
                          if k not in ("a_text", "b_text")}}
        for p, it in hardest]

    # A pair every rater is unsure about is a finding, per the packet's rules:
    # the distilled text does not carry enough for anyone to decide.
    allunsure = sorted(p for p, it in items.items()
                       if it["unjudgeable"] >= 1.0 - 1e-9)
    if allunsure:
        print("  NO RATER COULD DECIDE FROM THE TEXT  (unanimous `unsure`)")
        for p in allunsure:
            print(f"    {p}  {items[p]['part']:<7}{items[p]['stratum']}")
            print(f"        A: {items[p]['a_text'][:88]}")
            print(f"        B: {items[p]['b_text'][:88]}")
        print()
    res["unanimous_unsure"] = allunsure

    # ---- part 3: the re-merge queue ----------------------------------------
    have = {r: a for r, a in audits.items() if a and r in good}
    if len(have) >= 2:
        forks = sorted(set.intersection(*(set(a) for a in have.values())))
        first = sorted(have)[0]
        res["audit"] = {"raters": sorted(have), "forks": len(forks)}
        print(f"  PART 3 -- RE-MERGE QUEUE  ({len(have)} raters, "
              f"{len(forks)} forks in common)\n")

        # The queue: every fork someone proposed changing, with what they said.
        queue = []
        for f in forks:
            entries = []
            for r in sorted(have):
                a = have[r][f]
                instr = " / ".join(t for t in (a.get("remerge"), a["note"]) if t)
                if a["verdict"] in FLAGS or instr:
                    entries.append({"rater": r, "verdict": a["verdict"],
                                    "instruction": instr})
            if entries:
                src = have[first][f]
                queue.append({
                    "fork": f, "entries": entries,
                    "n_flagged": sum(1 for e in entries
                                     if e["verdict"] in FLAGS),
                    "n_instructed": sum(1 for e in entries if e["instruction"]),
                    "stratum": audit_strata.get(f),
                    "runs": src["runs"], "coverage": src["coverage"],
                    "n_options": src["n_options"],
                    "eff_options": src["eff_options"]})
        queue.sort(key=lambda q: (-q["n_instructed"], -q["n_flagged"],
                                  -(q["runs"] or 0)))
        res["audit"]["queue"] = queue

        actionable = [q for q in queue if q["n_instructed"]]
        print(f"    {len(queue)} of {len(forks)} forks drew a proposal; "
              f"{len(actionable)} carry an instruction that can be acted on.\n")
        for q in queue:
            cov = "" if q["coverage"] is None else f"cov {q['coverage']:.2f}  "
            eff = "" if q["eff_options"] is None else f"eff {q['eff_options']:.2f}"
            print(f"    {q['fork'][:92]}")
            print(f"      {cov}{eff}   {q['stratum'] or ''}")
            for e in q["entries"]:
                line = f"      {e['rater']}  {e['verdict']}"
                if e["instruction"]:
                    line += f"  -- {e['instruction']}"
                print(line)
            print()

        # An axis proposed at more than one fork is a claim about the
        # vocabulary, not about any single fork. Surfacing it is the point:
        # several separate "under-merged" rows saying the same thing are one
        # instruction, and reading them as several disagreements loses it.
        print("    RECURRING AXES  (an instruction repeated across forks is a")
        print("    claim about the vocabulary, not about one fork)")
        STOP = {"the", "and", "for", "with", "into", "this", "that", "from",
                "should", "could", "can", "one", "its", "own", "above", "but",
                "rest", "see", "here", "how", "what", "which", "them", "these",
                "another", "other", "than", "then", "about", "each", "all",
                "more", "some", "was", "are", "not", "has", "have", "will",
                "improved", "interesting", "showing", "pattern", "reorganize",
                "organized", "separated"}
        seen = defaultdict(set)
        for q in actionable:
            for e in q["entries"]:
                for w in set("".join(c if c.isalnum() else " "
                                     for c in e["instruction"].lower()).split()):
                    if len(w) > 2 and w not in STOP:
                        seen[w].add(q["fork"])
        rec = sorted(((w, fs) for w, fs in seen.items() if len(fs) >= 2),
                     key=lambda kv: -len(kv[1]))
        for w, fs in rec[:10]:
            print(f"      '{w}' appears in proposals at {len(fs)} forks")
        res["audit"]["recurring_terms"] = {w: sorted(fs) for w, fs in rec}
        print()

        # ---- kept as context, not as the headline --------------------------
        print("    AGREEMENT  (context only -- this sheet is a worksheet, and")
        print("    two raters proposing different halves of one re-merge are")
        print("    not in conflict)")
        print(f"      {'rater':<10}{'correct':>9}{'flagged':>9}"
              f"{'unsure':>8}{'instructions':>14}")
        for r in sorted(have):
            vs = [have[r][f]["verdict"] for f in forks]
            ins = sum(1 for f in forks
                      if have[r][f].get("remerge") or have[r][f]["note"])
            print(f"      {r:<10}{vs.count('correct'):>9}"
                  f"{sum(1 for v in vs if v in FLAGS):>9}"
                  f"{vs.count('unsure'):>8}{ins:>14}")
            res["audit"].setdefault("per_rater", {})[r] = {
                "correct": vs.count("correct"),
                "flagged": sum(1 for v in vs if v in FLAGS),
                "unsure": vs.count("unsure"), "instructions": ins}
        silent = [r for r in sorted(have)
                  if not any(have[r][f]["verdict"] in FLAGS for f in forks)]
        if silent:
            print(f"      {', '.join(silent)} proposed no change on any fork;")
            print(f"      read that as a use of the sheet, not a clean bill "
                  f"of health")

        strict_ok = strict_n = coarse_ok = coarse_n = 0
        for f in forks:
            vs = [have[r][f]["verdict"] for r in sorted(have)]
            o, n = pairwise(vs)
            strict_ok += o
            strict_n += n
            o2, n2 = pairwise([v in FLAGS for v in vs])
            coarse_ok += o2
            coarse_n += n2
        # Part 3's counterpart to the three-way table. Build B is not involved
        # -- the audit shows build A's forks only -- so there is no A x B
        # column here, and "rater x A" is the share of judgements calling a
        # fork correct.
        endorse = sum(1 for f in forks for r in have
                      if have[r][f]["verdict"] == "correct")
        uj3 = sum(1 for f in forks for r in have
                  if have[r][f]["verdict"] == "unsure")
        njud = len(forks) * len(have)
        print(f"      rater endorses build A's fork            "
              f"{endorse / njud:.3f}  ({endorse} of {njud})")
        print(f"      unjudgeable                              {uj3 / njud:.3f}")
        print(f"      verdict agreement, exact                 "
              f"{strict_ok / strict_n:.3f}")
        print(f"      verdict agreement, flagged or not        "
              f"{coarse_ok / coarse_n:.3f}")
        res["audit"]["endorse_rate"] = round(endorse / njud, 4)
        res["audit"]["unjudgeable_rate"] = round(uj3 / njud, 4)
        res["audit"].update({
            "agreement_strict": round(strict_ok / strict_n, 4),
            "agreement_flag_or_not": round(coarse_ok / coarse_n, 4),
            "silent_raters": silent})

        # Does a flag track fork size, or the question? If it only tracks size,
        # "over-merged" is a proxy for option count and not a judgement.
        flagged = {f for f in forks
                   if any(have[r][f]["verdict"] in FLAGS for r in have)}
        for field in ("eff_options", "n_options", "coverage"):
            sc = [have[first][f][field] for f in forks
                  if have[first][f][field] is not None]
            yy = [1 if f in flagged else 0 for f in forks
                  if have[first][f][field] is not None]
            a = auc(sc, yy)
            if a is not None:
                print(f"      AUC, {field:<12} predicts a flag      {a:.3f}")
                res["audit"][f"auc_{field}"] = round(a, 4)
        for st in ("targeted", "random"):
            sel = [f for f in forks if audit_strata.get(f) == st]
            if sel:
                fr = sum(1 for f in sel if f in flagged) / len(sel)
                print(f"      flag rate, {st:<9} forks            "
                      f"{fr:.2f}  (n={len(sel)})")
                res["audit"][f"flag_rate_{st}"] = round(fr, 4)
        print()

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        res["items"] = {p: {k: v for k, v in it.items()
                            if k not in ("a_text", "b_text")}
                        for p, it in items.items()}
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"  wrote {x.json}")


if __name__ == "__main__":
    main()
