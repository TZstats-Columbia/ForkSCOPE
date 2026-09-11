#!/usr/bin/env python3
"""Agreement at each layer, measured over that layer's own items. No model calls.

THE CONFOUND THIS FIXES
-----------------------
The vocabulary is two stacked clusterings:

    decisions  --(prompt 19, "same action?")-->  options
    options    --(prompt 22, foreclosure)     -->  decision points

Every fork number reported so far was computed over DECISION INSTANCES. That
conflates the two steps: if two builds split an option differently, the
instances in it land in different forks *even when both builds made exactly the
same fork judgement about that option*. Instance-level fork ARI therefore
inherits all of the option-level noise and reports it as fork instability.

To measure what fork induction actually does, the items must be the things it
actually clusters -- options, not decisions.

HOW OPTIONS BECOME A COMMON ITEM SET
------------------------------------
Options are different objects in the two builds, so there is no shared index to
cluster over. But options agree very well across builds (95% intact-or-split,
median per-run ARI 1.0), which is exactly the condition that makes a matching
trustworthy: match A's options to B's by instance overlap, keep the confident
pairs, and treat each matched pair as ONE item. Then ask whether those items
were grouped into the same forks.

The matching threshold is reported alongside the result, and so is the share of
options that could not be matched -- because a fork score computed on a
confidently-matched subset says nothing about the options it dropped.

WEIGHTING
---------
Both weightings are reported and they answer different questions:

  by option    each option counts once. "Did fork induction make the same
               judgements?" This is the estimator for the induction step.
  by instance  each option counts by how many decisions it holds. "Does the
               corpus split the same way?" This is what downstream statistics
               actually feel, since they aggregate over runs.

A large gap between them means the disagreement is concentrated in options of
unusual size -- worth knowing either way.

Usage:
    python3 stability/scripts/layer_agreement.py --a A.json --b B.json
        [--tau 0.5] [--json out.json]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import partition as P                                          # noqa: E402


def load(path):
    """(option_id -> members), (option_id -> fork), instance count."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    keys = [(r["run"], r.get("line", -1), (r.get("text") or "")[:60])
            for r in dec]
    opts, fork = {}, {}
    for i, o in enumerate(d["options"]):
        ms = {keys[m] for m in o.get("members", ()) if 0 <= m < len(keys)}
        if not ms:
            continue
        opts[i] = ms
        fork[i] = o["fork"]
    return opts, fork


def match_options(oa, ob, tau):
    """Greedy one-to-one option matching on Jaccard of instance sets."""
    cand = []
    # Index by instance so only genuinely overlapping pairs are scored.
    where = defaultdict(list)
    for j, B in ob.items():
        for k in B:
            where[k].append(j)
    for i, A in oa.items():
        seen = defaultdict(int)
        for k in A:
            for j in where.get(k, ()):
                seen[j] += 1
        for j, inter in seen.items():
            s = inter / len(A | ob[j])
            if s >= tau:
                cand.append((-s, i, j))
    cand.sort()
    ua, ub, pairs = set(), set(), []
    for negs, i, j in cand:
        if i in ua or j in ub:
            continue
        ua.add(i)
        ub.add(j)
        pairs.append((i, j, -negs))
    return pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--tau", type=float, default=0.5,
                    help="Jaccard floor for treating two options as one item")
    ap.add_argument("--json")
    x = ap.parse_args()

    oa, fa = load(x.a)
    ob, fb = load(x.b)

    # ---- layer 1: options as a clustering of decision instances -------------
    la, _ = P.labeling(x.a, "option")
    lb, _ = P.labeling(x.b, "option")
    ikeys = sorted(set(la) & set(lb))
    opt_ari = P.adjusted_rand(la, lb, ikeys)
    _, _, opt_f1 = P.bcubed(la, lb, ikeys)

    # ---- layer 2: forks as a clustering of OPTIONS --------------------------
    pairs = match_options(oa, ob, x.tau)
    items = list(range(len(pairs)))
    ga = {n: fa[i] for n, (i, j, s) in enumerate(pairs)}
    gb = {n: fb[j] for n, (i, j, s) in enumerate(pairs)}
    fork_ari_opt = P.adjusted_rand(ga, gb, items)
    _, _, fork_f1_opt = P.bcubed(ga, gb, items)

    # instance-weighted: repeat each matched option by its size
    w_items, wa, wb = [], {}, {}
    for n, (i, j, s) in enumerate(pairs):
        for c in range(len(oa[i])):
            t = (n, c)
            w_items.append(t)
            wa[t] = fa[i]
            wb[t] = fb[j]
    fork_ari_inst = P.adjusted_rand(wa, wb, w_items)

    # ---- the confounded number, for comparison ------------------------------
    lfa, _ = P.labeling(x.a, "fork")
    lfb, _ = P.labeling(x.b, "fork")
    fk = sorted(set(lfa) & set(lfb))
    fork_ari_raw = P.adjusted_rand(lfa, lfb, fk)

    res = {
        "build_a": x.a, "build_b": x.b, "comparison_type": "replicate",
        "tau": x.tau,
        "layer1_options_over_decisions": {
            "items": len(ikeys), "ari": round(opt_ari, 4),
            "bcubed_f1": round(opt_f1, 4),
            "clusters_a": len(oa), "clusters_b": len(ob),
        },
        "option_matching": {
            "matched": len(pairs),
            "of_a": round(len(pairs) / len(oa), 4),
            "of_b": round(len(pairs) / len(ob), 4),
            "unmatched_a": len(oa) - len(pairs),
            "unmatched_b": len(ob) - len(pairs),
        },
        "layer2_forks_over_options": {
            "items": len(pairs),
            "ari_by_option": round(fork_ari_opt, 4),
            "bcubed_f1_by_option": round(fork_f1_opt, 4),
            "ari_by_instance": round(fork_ari_inst, 4),
            "forks_a": len({fa[i] for i, _, _ in pairs}),
            "forks_b": len({fb[j] for _, j, _ in pairs}),
        },
        "forks_over_decisions_confounded": round(fork_ari_raw, 4),
    }

    l1, om, l2 = (res["layer1_options_over_decisions"],
                  res["option_matching"], res["layer2_forks_over_options"])
    print("LAYERED AGREEMENT -- each step measured over its own items\n")
    print(f"  LAYER 1  options as a clustering of DECISIONS")
    print(f"    items                      {l1['items']}")
    print(f"    ARI                        {l1['ari']}")
    print(f"    B-cubed F1                 {l1['bcubed_f1']}")
    print(f"    clusters                   {l1['clusters_a']} vs "
          f"{l1['clusters_b']}\n")
    print(f"  OPTION MATCHING  (Jaccard >= {x.tau})")
    print(f"    matched                    {om['matched']}  "
          f"({om['of_a']:.1%} of A, {om['of_b']:.1%} of B)")
    print(f"    unmatched                  {om['unmatched_a']} A / "
          f"{om['unmatched_b']} B\n")
    print(f"  LAYER 2  forks as a clustering of OPTIONS")
    print(f"    items                      {l2['items']}")
    print(f"    ARI  by option             {l2['ari_by_option']}"
          f"   <- the fork-induction estimator")
    print(f"    ARI  by instance           {l2['ari_by_instance']}")
    print(f"    B-cubed F1 by option       {l2['bcubed_f1_by_option']}")
    print(f"    forks spanned              {l2['forks_a']} vs {l2['forks_b']}\n")
    print(f"  for comparison, forks over DECISIONS (confounded with layer 1): "
          f"{res['forks_over_decisions_confounded']}")
    print(f"    -> that number charges fork induction for option-level "
          f"disagreement\n       it did not cause")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")


if __name__ == "__main__":
    main()
