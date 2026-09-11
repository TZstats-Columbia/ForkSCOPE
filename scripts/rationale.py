#!/usr/bin/env python3
"""Cluster forks by what they rest on, not by what they are about.

Every fork in this corpus concerns skin tone, red cards and referees, so any
clustering that keys on subject matter returns one cluster. The interesting
grouping is by *reasoning*: which decisions are hard for the same reason, and
therefore share an assumption an analyst could get wrong in the same way.

That is not a field the corpus has, so it is elicited and then clustered:

  tag      prompt 17, per fork -> assumption, tradeoff, and 2-5 free tags
           naming the KIND of consideration in play. The prompt spends most of
           its length on the failure mode -- tagging with the study's nouns --
           because that is the way this step dies.
  merge    prompt 18 consolidates the free tags into families, bottom-up, in
           the same shape as the L2/L3 option merge, and with the same bias:
           under-merge is visible and recoverable, over-merge collapses a
           distinction and is not.
  cluster  fork x family binary matrix -> Jaccard distance -> average-linkage
           hierarchical clustering (scipy). k is chosen by silhouette over a
           range rather than fixed.

WHY JACCARD AND AVERAGE LINKAGE
-------------------------------
The matrix is sparse binary presence/absence over a few dozen families, which
is what Jaccard is for -- it ignores joint absences, and with 40+ families most
pairs share almost nothing but zeros, so Euclidean or correlation distance
would call every fork similar. Average linkage because it makes no assumption
about cluster shape and does not chain the way single linkage does on sparse
data. Ward is unavailable here: it requires Euclidean geometry, which a Jaccard
matrix does not provide.

Clustering on the LLM's tags rather than on the fork text is deliberate. TF-IDF
over the questions would cluster on shared nouns, which is exactly the trap the
tagging prompt exists to avoid, and would reproduce the subject-matter grouping
that makes the whole exercise pointless.

Usage:
    python3 scripts/rationale.py tag     --corpus ai      # LLM, cached
    python3 scripts/rationale.py merge   --corpus ai      # LLM, cached
    python3 scripts/rationale.py cluster --corpus ai
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist, squareform

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
OUT = P.ANALYSIS

BATCH = 40
MERGE_BATCH = 90
K_RANGE = range(4, 13)
MIN_FAMILY = 3        # a family on fewer forks than this is dropped as a coordinate
SEED = 20260822
RAT_SCHEMA = {"type": "object", "required": ["forks"]}
FAM_SCHEMA = {"type": "object", "required": ["families"]}


def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", (t or "").lower()).strip()


def load_forks(tag):
    gm = json.loads((OUT / f"garden_{tag}.json").read_text(encoding="utf-8"))
    return [x["fork"] for x in gm["nodes_detail"]], gm


# --------------------------------------------------------------------------
def do_tag(tag):
    from llm import ask
    forks, _ = load_forks(tag)
    print(f"eliciting assumption / tradeoff / tags for {len(forks)} forks")
    got = {}
    for k in range(0, len(forks), BATCH):
        chunk = forks[k:k + BATCH]
        want = set(range(k, k + len(chunk)))

        def check(o, want=want):
            ids = [x.get("id") for x in o.get("forks", [])]
            miss = want - set(ids)
            if miss:
                raise ValueError(f"{len(miss)} ids missing: {sorted(miss)[:8]}")
            thin = [x.get("id") for x in o["forks"]
                    if len(x.get("tags") or []) < 2]
            if thin:
                raise ValueError(f"ids {thin[:6]} have fewer than 2 tags; "
                                 f"every fork needs 2-5")
            for x in o["forks"]:
                if not (x.get("assumption") or "").strip():
                    raise ValueError(f"id {x.get('id')} has an empty assumption")

        out = ask("17_fork_rationale",
                  {"forks": [{"id": k + j, "question": f}
                             for j, f in enumerate(chunk)]},
                  schema=RAT_SCHEMA, model="opus", run_id="rationale",
                  check=check)
        for x in out["forks"]:
            i = x.get("id")
            if isinstance(i, int) and 0 <= i < len(forks):
                got[forks[i]] = {"assumption": x.get("assumption", ""),
                                 "tradeoff": x.get("tradeoff", ""),
                                 "tags": [norm(t) for t in x.get("tags", [])
                                          if norm(t)]}
        print(f"  {min(k + BATCH, len(forks))}/{len(forks)}", flush=True)
    p = OUT / f"rationale_{tag}.json"
    p.write_text(json.dumps(got, ensure_ascii=False, indent=1), encoding="utf-8")
    c = Counter(t for v in got.values() for t in v["tags"])
    print(f"\n{len(c)} distinct tags over {sum(c.values())} assignments")
    print("most common:")
    for t, n in c.most_common(15):
        print(f"  {n:>4}  {t}")
    print(f"-> {p}")


def do_merge(tag):
    from llm import ask
    rp = OUT / f"rationale_{tag}.json"
    if not rp.exists():
        sys.exit(f"run `rationale.py tag --corpus {tag}` first")
    rat = json.loads(rp.read_text(encoding="utf-8"))
    cnt = Counter(t for v in rat.values() for t in v["tags"])
    tags = [t for t, _ in cnt.most_common()]
    print(f"consolidating {len(tags)} tags")
    fams = []
    for k in range(0, len(tags), MERGE_BATCH):
        chunk = tags[k:k + MERGE_BATCH]

        def check(o, chunk=chunk):
            seen = [m for f in o.get("families", []) for m in f.get("members", [])]
            miss = set(chunk) - set(norm(x) for x in seen)
            if miss:
                raise ValueError(f"{len(miss)} tags unplaced: "
                                 f"{sorted(miss)[:8]}")
            dup = [t for t, c in Counter(norm(x) for x in seen).items() if c > 1]
            if dup:
                raise ValueError(f"tags in more than one family: {dup[:6]}")

        out = ask("18_merge_tags",
                  {"tags": [{"tag": t, "n_forks": cnt[t]} for t in chunk]},
                  schema=FAM_SCHEMA, model="opus", run_id="rationale_merge",
                  check=check)
        fams += out["families"]
        print(f"  {min(k + MERGE_BATCH, len(tags))}/{len(tags)}", flush=True)

    # a tag can only be in one family; first writer wins, later duplicates drop
    fam_of, families = {}, {}
    for f in fams:
        nm = norm(f.get("name")) or "unnamed"
        for m in f.get("members", []):
            m = norm(m)
            if m and m not in fam_of:
                fam_of[m] = nm
                families.setdefault(nm, []).append(m)
    for t in cnt:
        fam_of.setdefault(t, t)
        families.setdefault(t, [t])
    p = OUT / f"rationale_families_{tag}.json"
    p.write_text(json.dumps({"family_of": fam_of, "families": families},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    fc = Counter(fam_of[t] for v in rat.values() for t in v["tags"])
    print(f"\n{len(tags)} tags -> {len(families)} families")
    print("largest:")
    for f, n in fc.most_common(15):
        print(f"  {n:>4} forks  {f}   [{', '.join(families[f][:4])}]")
    print(f"-> {p}")


# --------------------------------------------------------------------------
def do_cluster(tag):
    rp = OUT / f"rationale_{tag}.json"
    fp = OUT / f"rationale_families_{tag}.json"
    if not (rp.exists() and fp.exists()):
        sys.exit(f"run `tag` then `merge` for corpus {tag} first")
    rat = json.loads(rp.read_text(encoding="utf-8"))
    fam_of = json.loads(fp.read_text(encoding="utf-8"))["family_of"]
    gm = json.loads((OUT / f"garden_{tag}.json").read_text(encoding="utf-8"))
    stage = {x["fork"]: x.get("stage") for x in gm["nodes_detail"]}

    prof = {f: {fam_of.get(t, t) for t in v["tags"]} for f, v in rat.items()}
    fc = Counter(x for s in prof.values() for x in s)
    cols = sorted(f for f, n in fc.items() if n >= MIN_FAMILY)
    forks = sorted(f for f in prof if prof[f] & set(cols))
    M = np.array([[1 if c in prof[f] else 0 for c in cols] for f in forks],
                 dtype=float)

    print(f"RATIONALE CLUSTERS - {tag}")
    print(f"{len(forks)} forks with at least one family on >= {MIN_FAMILY} "
          f"forks, over {len(cols)} coordinates\n")

    D = pdist(M, metric="jaccard")
    Z = linkage(D, method="average")
    sq = squareform(D)

    def silhouette(lab):
        s = []
        for i in range(len(lab)):
            same = [j for j in range(len(lab)) if j != i and lab[j] == lab[i]]
            if not same:
                continue
            a = np.mean([sq[i, j] for j in same])
            b = min(np.mean([sq[i, j] for j in range(len(lab))
                             if lab[j] == o])
                    for o in set(lab) if o != lab[i])
            s.append((b - a) / max(a, b) if max(a, b) else 0.0)
        return float(np.mean(s)) if s else 0.0

    print(f"  {'k':>3}{'silhouette':>12}{'largest':>9}{'singletons':>12}")
    best, best_s = None, -2
    for k in K_RANGE:
        lab = fcluster(Z, k, criterion="maxclust")
        sc = silhouette(lab)
        sz = Counter(lab)
        print(f"  {k:>3}{sc:>12.3f}{max(sz.values()):>9}"
              f"{sum(1 for v in sz.values() if v == 1):>12}")
        if sc > best_s:
            best, best_s = k, sc
    lab = fcluster(Z, best, criterion="maxclust")
    print(f"\n  chosen k = {best} (silhouette {best_s:.3f})\n")

    groups = defaultdict(list)
    for f, c in zip(forks, lab):
        groups[int(c)].append(f)
    # name each cluster by the family most over-represented in it
    base = {c: fc[c] / len(forks) for c in cols}
    out = []
    for c in sorted(groups, key=lambda c: -len(groups[c])):
        mem = groups[c]
        inside = Counter(x for f in mem for x in prof[f])
        lift = sorted(((inside[x] / len(mem)) / base[x], x) for x in cols
                      if inside[x] >= max(2, 0.3 * len(mem)))
        name = lift[-1][1] if lift else "mixed"
        top = [x for _, x in lift[::-1][:4]]
        stg = Counter(stage.get(f) for f in mem).most_common(1)[0]
        out.append({"cluster": c, "name": name, "n": len(mem),
                    "families": top, "dominant_stage": stg[0],
                    "stage_share": round(stg[1] / len(mem), 2),
                    "forks": mem})
        print(f"  [{c}] {name}   {len(mem)} forks   "
              f"{stg[0]} {stg[1]/len(mem):.0%}")
        print(f"      {' · '.join(top)}")
        for f in mem[:3]:
            print(f"      - {f[:70]}")

    p = OUT / f"rationale_clusters_{tag}.json"
    p.write_text(json.dumps({"k": best, "silhouette": round(best_s, 4),
                             "coordinates": cols, "clusters": out,
                             "assignment": {f: int(c)
                                            for f, c in zip(forks, lab)}},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["tag", "merge", "cluster"])
    ap.add_argument("--corpus", default=P.FINAL_TAG)
    a = ap.parse_args()
    t = "+".join(c.strip() for c in a.corpus.split(","))
    {"tag": do_tag, "merge": do_merge, "cluster": do_cluster}[a.cmd](t)
