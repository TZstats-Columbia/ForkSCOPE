#!/usr/bin/env python3
"""Does the lexical candidate screen leak fork merges? No model calls.

THE QUESTION
------------
`merge_forks.py` only adjudicates fork pairs that `audit_lineage.neighbours()`
scores above 0.55:

    score = 1.6*label_jaccard + 1.0*option_vocab_jaccard + 0.9*exclusivity

Everything below that is never seen by a model, so a merge the screen misses
cannot be made at all. The screen's RECALL therefore bounds the whole pass, and
it has never been measured.

WHY THE OBVIOUS EXPERIMENT DOES NOT WORK
----------------------------------------
Comparing against the pairs `21_fork_identity` judged "same" is circular: those
pairs were selected BY the screen, so its recall on them is 100% by
construction. That is the same selection trap this project keeps hitting, and
it has to be designed around rather than noticed afterwards.

GROUND TRUTH FROM THE SECOND BUILD
----------------------------------
Build B is an independent run of the same pipeline. Where two of A's forks have
their members land in ONE of B's forks, B has judged them one question --
independently of A's screen, which never influenced B.

That gives a positive set the screen cannot have manufactured. It is not
perfect ground truth: B could be over-merging. But B's judgement is exactly as
authoritative as A's, and a pair the screen never even *considered* is a
recall failure regardless of who is right about it.

WHAT IS COMPARED
----------------
  lexical    the production screen, reimplemented from audit_lineage
  lsa        TF-IDF over label + option vocabulary, reduced by SVD, cosine

LSA is a distributional embedding, not a neural one -- no embedding model or
API key is available here. It is therefore a LOWER BOUND on what a modern
sentence embedding would achieve: if LSA already beats the lexical screen, a
real embedding does at least as well.

Both are compared at MATCHED BUDGET -- the same number of candidate pairs --
because a screen can always buy recall by lowering its threshold, and the
question is whether it ranks better, not whether it is more permissive.

Usage:
    python3 stability/scripts/screen_recall.py --a A.json --b B.json
        [--min-containment 0.5] [--json out]
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

STOP = set("""a an the of to in on for by with and or at as is are be into from
that this these those it its use used using which what how do does done than
then when where each per via over under between within not no if""".split())


def toks(s):
    return {w for w in re.findall(r"[a-z0-9.]+", s.lower()) if w not in STOP}


def jac(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0


def fork_table(path):
    """{fork: {"runs": set, "members": set, "opts": [labels]}}."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    keys = [(r["run"], r.get("line", -1), (r.get("text") or "")[:60])
            for r in dec]
    per = defaultdict(lambda: {"runs": set(), "members": set(), "opts": []})
    for o in d["options"]:
        ms = [m for m in o.get("members", ()) if 0 <= m < len(keys)]
        if not ms:
            continue
        f = per[o["fork"]]
        f["runs"].update(dec[m]["run"] for m in ms)
        f["members"].update(keys[m] for m in ms)
        f["opts"].append(o["option"])
    return dict(per)


def lexical_scores(fa, pairs):
    """The production screen, reimplemented. Same weights, same terms."""
    fs = list(fa)
    tk = {f: toks(f) for f in fs}
    ov = {f: set().union(*[toks(o) for o in fa[f]["opts"]]) if fa[f]["opts"]
          else set() for f in fs}
    all_runs = set().union(*[fa[f]["runs"] for f in fs])
    out = {}
    for a, b in pairs:
        ra, rb = fa[a]["runs"], fa[b]["runs"]
        co = len(ra & rb)
        exp = len(ra) * len(rb) / max(1, len(all_runs))
        excl = 1.0 if (co == 0 and exp >= 4) else 0.0
        out[(a, b)] = (1.6 * jac(tk[a], tk[b]) + 1.0 * jac(ov[a], ov[b])
                       + 0.9 * excl)
    return out


def lsa_scores(fa, pairs, dims=128):
    """TF-IDF over label + option vocabulary, SVD-reduced, cosine."""
    fs = list(fa)
    docs = [f + " . " + " . ".join(fa[f]["opts"]) for f in fs]
    X = TfidfVectorizer(stop_words="english", sublinear_tf=True,
                        ngram_range=(1, 2), min_df=1).fit_transform(docs)
    k = min(dims, X.shape[1] - 1, len(fs) - 1)
    Z = TruncatedSVD(n_components=k, random_state=0).fit_transform(X)
    Z /= (np.linalg.norm(Z, axis=1, keepdims=True) + 1e-12)
    idx = {f: i for i, f in enumerate(fs)}
    return {(a, b): float(Z[idx[a]] @ Z[idx[b]]) for a, b in pairs}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--min-containment", type=float, default=0.5)
    ap.add_argument("--min-runs", type=int, default=4,
                    help="the production screen skips forks below this")
    ap.add_argument("--json")
    x = ap.parse_args()

    fa, fb = fork_table(x.a), fork_table(x.b)

    # ---- ground truth: A-fork pairs that B puts in one fork ----------------
    dom = {}
    for f, s in fa.items():
        best, bc = None, 0.0
        for g, t in fb.items():
            inter = len(s["members"] & t["members"])
            if inter:
                c = inter / len(s["members"])
                if c > bc:
                    best, bc = g, c
        dom[f] = (best, bc)

    by_b = defaultdict(list)
    for f, (g, c) in dom.items():
        if g and c >= x.min_containment:
            by_b[g].append(f)

    # the production screen never looks at forks under min_runs, so a pair it
    # structurally cannot see is excluded from the denominator rather than
    # counted as a miss it had no chance at
    eligible = {f for f, s in fa.items() if len(s["runs"]) >= x.min_runs}
    truth = set()
    for g, members in by_b.items():
        members = [f for f in members if f in eligible]
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                truth.add(tuple(sorted((members[i], members[j]))))

    fa_e = {f: fa[f] for f in eligible}
    allp = [tuple(sorted((a, b)))
            for i, a in enumerate(sorted(fa_e))
            for b in sorted(fa_e)[i + 1:]]
    allp = sorted(set(allp))

    lex = lexical_scores(fa_e, allp)
    lsa = lsa_scores(fa_e, allp)

    n_prod = sum(1 for p in allp if lex[p] > 0.55)     # production budget

    def recall_at(scores, budget):
        top = set(sorted(allp, key=lambda p: -scores[p])[:budget])
        hit = len(truth & top)
        return hit, round(hit / len(truth), 4) if truth else None

    res = {"build_a": x.a, "build_b": x.b,
           "forks_a": len(fa), "eligible_forks": len(eligible),
           "candidate_pairs_total": len(allp),
           "ground_truth_pairs": len(truth),
           "production_budget": n_prod,
           "production_threshold": 0.55}

    print("SCREEN RECALL  (ground truth = A-fork pairs that build B merges)\n")
    print(f"  forks in A                    {len(fa)}")
    print(f"  eligible (>= {x.min_runs} runs)          {len(eligible)}")
    print(f"  all pairs among eligible      {len(allp)}")
    print(f"  ground-truth 'same' pairs     {len(truth)}")
    print(f"  production screen budget      {n_prod} pairs "
          f"(score > 0.55)\n")

    hit_l, rec_l = recall_at(lex, n_prod)
    hit_e, rec_e = recall_at(lsa, n_prod)
    res["recall_at_production_budget"] = {
        "lexical": {"hits": hit_l, "recall": rec_l},
        "lsa": {"hits": hit_e, "recall": rec_e}}
    print(f"  AT THE PRODUCTION BUDGET ({n_prod} pairs)")
    print(f"    lexical screen   {hit_l}/{len(truth)}  recall {rec_l}")
    print(f"    LSA embedding    {hit_e}/{len(truth)}  recall {rec_e}\n")

    print(f"  RECALL AT OTHER BUDGETS")
    print(f"    {'budget':>8}{'lexical':>10}{'LSA':>10}")
    curve = {}
    for b in (100, 250, 500, 1000, 2000):
        if b > len(allp):
            continue
        _, rl = recall_at(lex, b)
        _, re_ = recall_at(lsa, b)
        curve[b] = {"lexical": rl, "lsa": re_}
        print(f"    {b:>8}{rl:>10}{re_:>10}")
    res["recall_curve"] = curve

    missed = sorted(truth - set(sorted(allp, key=lambda p: -lex[p])[:n_prod]),
                    key=lambda p: -lsa[p])
    res["missed_by_lexical"] = [
        {"lex": round(lex[p], 3), "lsa": round(lsa[p], 3),
         "fork_a": p[0][:80], "fork_b": p[1][:80]} for p in missed[:12]]
    if missed:
        print(f"\n  pairs the lexical screen never considered "
              f"({len(missed)} of {len(truth)}), ranked by LSA:")
        for r in res["missed_by_lexical"][:6]:
            print(f"    lex {r['lex']:<6} lsa {r['lsa']:<6}")
            print(f"      A: {r['fork_a'][:72]}")
            print(f"      B: {r['fork_b'][:72]}")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")


if __name__ == "__main__":
    main()
