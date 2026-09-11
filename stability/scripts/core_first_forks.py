#!/usr/bin/env python3
"""Would forming forks from stable options first improve stability? No model calls.

THE PROPOSAL
------------
Current: every option, however rare, participates in fork induction on equal
footing. Proposed instead:

  1  restrict to STABLE options -- those taken by more than a threshold share
     of runs
  2  form forks from those, by the current method
  3  attach the remaining rare options to a fork by semantics

The motivation is measured rather than aesthetic. Fork assignment for rare
options does not reproduce: by-option ARI is 0.31 at >= 1 instance against 0.69
at >= 5, and 64% of options are singletons. Under the current design those
coin-flip assignments are made independently in each build and each one is an
opportunity to disagree.

WHY THIS SHOULD HELP, MECHANICALLY
----------------------------------
Stage 3 replaces an independent per-build judgement with a DETERMINISTIC
function of that build's own stable core. Two builds then disagree about a rare
option only if their cores disagree -- and the core is the part that reproduces.
The noise is not removed so much as made to inherit from something stable.

HOW IT IS EVALUATED WITHOUT RUNNING THE PIPELINE
------------------------------------------------
The proposal is simulated on the two existing builds. Core options keep the
fork the build already gave them; non-core options are reassigned to the fork
of their nearest core option. Agreement is then recomputed and compared with
the same builds unmodified.

Stage 3 here uses LSA cosine over option labels as the semantic attach step,
because no embedding model is available. That is weaker than the LLM the real
implementation would use, so the measured improvement is a LOWER BOUND on the
proposal -- with one caveat below.

THE CONFOUND, STATED
--------------------
Applying one deterministic rule to both builds can raise their agreement for a
trivial reason: both receive the same systematic transformation. The rule here
reads only each build's own options and its own core, never the other build, so
it is not circular. But the improvement must be read against what a rule that
IGNORES semantics achieves -- so a null is included that attaches each rare
option to a RANDOM core fork, size-matched. If the semantic attach barely beats
that, the gain is coming from the restriction, not the semantics.

Usage:
    python3 stability/scripts/core_first_forks.py --a A.json --b B.json
        [--core-share 0.05] [--json out]
"""
import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from layer_agreement import load as load_opts, match_options    # noqa: E402

SEED = 20260822


def load(path):
    """[(option_label, fork, set(runs), members)] indexed as in the file."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    dec = d["decisions"]
    out = {}
    for i, o in enumerate(d["options"]):
        ms = [m for m in o.get("members", ()) if 0 <= m < len(dec)]
        if ms:
            out[i] = {"label": o["option"], "fork": o["fork"],
                      "runs": {dec[m]["run"] for m in ms}, "members": ms}
    n_runs = len({r["run"] for r in dec})
    return out, n_runs


def embed(labels):
    X = TfidfVectorizer(stop_words="english", sublinear_tf=True,
                        ngram_range=(1, 2)).fit_transform(labels)
    k = min(128, X.shape[1] - 1, len(labels) - 1)
    Z = TruncatedSVD(n_components=k, random_state=0).fit_transform(X)
    return Z / (np.linalg.norm(Z, axis=1, keepdims=True) + 1e-12)


def reassign(opts, n_runs, share, mode, rng):
    """Fork label per option under the core-first scheme.

    Core options keep what the build gave them. Non-core options are attached
    to the fork of their nearest core option (`mode='semantic'`) or to a core
    fork drawn at random with probability proportional to core size
    (`mode='random'`, the null).
    """
    idx = sorted(opts)
    core = [i for i in idx if len(opts[i]["runs"]) > share * n_runs]
    rest = [i for i in idx if i not in set(core)]
    if not core:
        return {i: opts[i]["fork"] for i in idx}, 0, len(idx)

    out = {i: opts[i]["fork"] for i in core}
    if mode == "semantic":
        Z = embed([opts[i]["label"] for i in idx])
        pos = {i: k for k, i in enumerate(idx)}
        C = np.stack([Z[pos[i]] for i in core])
        for i in rest:
            sims = C @ Z[pos[i]]
            out[i] = opts[core[int(np.argmax(sims))]]["fork"]
    else:
        w = np.array([len(opts[i]["runs"]) for i in core], dtype=float)
        w /= w.sum()
        for i in rest:
            out[i] = opts[core[rng.choice(len(core), p=w)]]["fork"]
    return out, len(core), len(rest)


def agree(fa, fb, pairs):
    a = [fa[i] for i, j, _ in pairs]
    b = [fb[j] for i, j, _ in pairs]
    return (round(float(adjusted_rand_score(a, b)), 4),
            round(float(adjusted_mutual_info_score(a, b)), 4),
            len({*a}), len({*b}))


def geometry(opts, forkmap, runs_all):
    """Run x run Jaccard distance over the forks each run touches."""
    per = defaultdict(set)
    for i, o in opts.items():
        for r in o["runs"]:
            per[r].add(forkmap[i])
    runs = sorted(runs_all)
    sets = [per.get(r, set()) for r in runs]
    n = len(runs)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            u = len(sets[i] | sets[j])
            D[i, j] = D[j, i] = 1.0 - (len(sets[i] & sets[j]) / u if u else 0.0)
    return D


def mantel(A, B):
    iu = np.triu_indices_from(A, k=1)
    a, b = A[iu], B[iu]
    if a.std() < 1e-12 or b.std() < 1e-12:
        return float("nan")
    return round(float(np.corrcoef(a, b)[0, 1]), 4)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--core-share", type=float, default=0.05)
    ap.add_argument("--json")
    x = ap.parse_args()

    oa, na = load(x.a)
    ob, nb = load(x.b)
    ma, _ = load_opts(x.a)
    mb, _ = load_opts(x.b)
    pairs = match_options(ma, mb, 0.5)
    runs = sorted({r for o in oa.values() for r in o["runs"]} &
                  {r for o in ob.values() for r in o["runs"]})
    print(f"  {len(oa)} / {len(ob)} options, {len(pairs)} matched, "
          f"{len(runs)} shared runs\n")

    rng = np.random.default_rng(SEED)
    res = {"build_a": x.a, "build_b": x.b, "core_share": x.core_share,
           "matched_options": len(pairs), "schemes": {}}

    base_a = {i: oa[i]["fork"] for i in oa}
    base_b = {i: ob[i]["fork"] for i in ob}

    schemes = [("current", None), ("core-first (semantic)", "semantic"),
               ("core-first (random null)", "random")]
    print(f"  {'scheme':<26}{'ARI':>8}{'AMI':>8}{'forks A':>9}{'forks B':>9}"
          f"{'geometry':>10}")
    for name, mode in schemes:
        if mode is None:
            fa, fb = base_a, base_b
            ca = cb = None
        else:
            fa, ca, ra_ = reassign(oa, na, x.core_share, mode, rng)
            fb, cb, rb_ = reassign(ob, nb, x.core_share, mode, rng)
        ari, ami, nfa, nfb = agree(fa, fb, pairs)
        g = mantel(geometry(oa, fa, runs), geometry(ob, fb, runs))
        res["schemes"][name] = {"ari": ari, "ami": ami, "forks_a": nfa,
                                "forks_b": nfb, "geometry_mantel": g,
                                "core_a": ca, "core_b": cb}
        print(f"  {name:<26}{ari:>8}{ami:>8}{nfa:>9}{nfb:>9}{g:>10}")

    c = res["schemes"]["core-first (semantic)"]
    print(f"\n  core options: {c['core_a']} of {len(oa)} in A, "
          f"{c['core_b']} of {len(ob)} in B "
          f"(> {x.core_share:.0%} of runs)")

    if x.json:
        Path(x.json).parent.mkdir(parents=True, exist_ok=True)
        Path(x.json).write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(f"\n  wrote {x.json}")


if __name__ == "__main__":
    main()
