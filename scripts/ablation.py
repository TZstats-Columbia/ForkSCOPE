#!/usr/bin/env python3
"""Validation gate 5.4 — code ablation. Can decisions be recovered from prose?

The plan set this gate because it decides whether the corpora can be pooled:

    hide the script for 30% of the runs that have one, re-derive from prose;
    >= 0.85 land in the same option, else split the analysis.

It matters more now than when it was written. v2 decision extraction is
code-anchored, so the pooled run carried only 19 of 31 human teams -- the 11
prose-only teams contributed 1,123 prose spans and zero decisions. That is the
"12-team rump" the plan explicitly forbade, wearing the other shoe. Until this
gate runs, no AI-vs-human claim is safe.

THE ABLATION IS ALREADY BUILT, WHICH IS WHY THIS IS CHEAP
---------------------------------------------------------
No re-extraction is needed and none is done here. Prompt 02 segments the
write-up **having never seen the script**, and its claims carry polarity: a
claim with polarity `did` or `did_not` is a decision stated in prose. So each
run already has two independent accounts of itself:

    code channel   code_spans.json,  kind == "decision"
    prose channel  prose_spans.json, kind == "claim", polarity in (did, did_not)

The prose channel is blind to the code by construction, not by an ablation
procedure I applied afterwards. That is a stronger design than hiding files and
re-running, because there is no risk of leakage through a cache.

WHAT IS MEASURED
----------------
  recall     of the decisions the code channel found, how many does prose find?
  agreement  of the decisions both found, how many are the SAME option?
  conflict   how many are the same question with a DIFFERENT answer? This is
             the number that would invalidate pooling, and it is not the same
             as low recall: prose being silent is a coverage problem, prose
             contradicting the code is a validity problem.
  vaguer     same choice, too underspecified to pin the option. Not a
             disagreement -- a loss of resolution, which bears on the
             granularity at which prose-only runs could be pooled.

THE MATCHER IS BLINDED AND CALIBRATED
-------------------------------------
The judge is not told which list is code and which is prose, and the order is
randomised per run, so it cannot anchor on the code as ground truth.

More important, `--null` re-runs the matcher on **mismatched pairs** -- run i's
code against run j's prose. Every match it makes there is false by
construction. Without that number the within-run agreement rate is
uninterpretable: a lenient judge that matches anything would also score well.

Usage:
    python3 scripts/ablation.py sample  --frac 0.30
    python3 scripts/ablation.py match                # LLM, cached
    python3 scripts/ablation.py match --null         # calibration
    python3 scripts/ablation.py report
"""
import argparse
import json
import random
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
RUNS = P.DISTILLED
OUT = P.ANALYSIS
ABL = P.ABLATION

SEED = 20260822
GATE = 0.85
WORKERS = 8
MATCH_SCHEMA = {"type": "object",
                "required": ["pairs", "unmatched_1", "unmatched_2"]}


def spans(path, key="spans"):
    if not path.exists():
        return []
    j = json.loads(path.read_text(encoding="utf-8"))
    return j[key] if isinstance(j, dict) and key in j else (j or [])


def channels(run):
    """(code decisions, prose decisions) for one run, as [{id, text, targets}]."""
    d = RUNS / run
    code = [{"id": str(s.get("id")),
             "text": s.get("operation") or "",
             "targets": s.get("targets") or []}
            for s in spans(d / "code_spans.json")
            if s.get("kind") == "decision" and s.get("operation")]
    prose = [{"id": str(s.get("id")),
              "text": s.get("assertion") or "",
              "targets": s.get("targets") or []}
             for s in spans(d / "prose_spans.json")
             if s.get("kind") == "claim"
             and s.get("polarity") in ("did", "did_not")
             and s.get("assertion")]
    return code, prose


# A stratum smaller than this is taken whole rather than sampled. 40 is
# above soccer's 19 code-bearing human teams and far below its 204 AI runs,
# so it reproduces that study exactly while generalising the intent.
SMALL_STRATUM = 40


def whole_stratum(items, frac):
    """How the sample line describes what happened to one stratum."""
    return (f"  (all: stratum under {SMALL_STRATUM})"
            if len(items) < SMALL_STRATUM else f"  ({frac:.0%})")


def eligible():
    """Runs with both channels non-empty."""
    out = []
    for d in sorted(RUNS.iterdir()):
        if not d.is_dir():
            continue
        c, p = channels(d.name)
        if c and p:
            # The record says which corpus it came from. This used to be
            # inferred from a "team-" filename prefix, which is a fact about
            # one study's directory names rather than about the corpus.
            try:
                corp = json.loads((d / "record.json").read_text(
                    encoding="utf-8")).get("corpus", d.name)
            except Exception:                                  # noqa: BLE001
                corp = d.name
            out.append({"run": d.name, "corpus": corp,
                        "n_code": len(c), "n_prose": len(p)})
    return out


# --------------------------------------------------------------------------
def do_sample(frac):
    el = eligible()
    rng = random.Random(SEED)
    by = defaultdict(list)
    for e in el:
        by[e["corpus"]].append(e)
    picked = []
    for corp, items in sorted(by.items()):
        items.sort(key=lambda x: x["run"])
        if len(items) < SMALL_STRATUM:
            # Take the whole stratum. A fraction of a small corpus cannot carry
            # a pooling decision: soccer's 19 code-bearing human teams are the
            # reason this gate exists, and sampling 30% of them would leave 6.
            # Expressed as a size rule rather than a corpus name, so a second
            # study gets the same protection without naming its corpora here.
            picked += items
        else:
            k = max(1, round(len(items) * frac))
            picked += rng.sample(items, k)
    picked.sort(key=lambda x: (x["corpus"], x["run"]))
    ABL.mkdir(parents=True, exist_ok=True)
    p = ABL / "sample.json"
    p.write_text(json.dumps({"seed": SEED, "frac": frac,
                             "n_eligible": len(el), "runs": picked},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"CODE ABLATION — sample")
    print(f"  eligible runs (both channels)  {len(el)}")
    for corp in sorted(by):
        got = sum(1 for x in picked if x["corpus"] == corp)
        print(f"    {corp:<8} {got} of {len(by[corp])}"
              f"{whole_stratum(by[corp], frac)}")
    print(f"  sampled                        {len(picked)}")
    print(f"  code decisions in sample       {sum(x['n_code'] for x in picked)}")
    print(f"  prose decisions in sample      {sum(x['n_prose'] for x in picked)}")
    print(f"-> {p}")


# --------------------------------------------------------------------------
def align_one(run, code, prose, rng, tag):
    """One matcher call, blinded: lists are shuffled and channel-anonymous."""
    from llm import ask
    flip = rng.random() < 0.5          # which channel is presented as list 1
    A, B = (prose, code) if flip else (code, prose)
    a = [{"id": x["id"], "decision": x["text"], "concerns": x["targets"][:6]}
         for x in A]
    b = [{"id": x["id"], "decision": x["text"], "concerns": x["targets"][:6]}
         for x in B]
    rng.shuffle(a)
    rng.shuffle(b)
    ids_a, ids_b = {x["id"] for x in a}, {x["id"] for x in b}

    def check(o):
        pa = [p.get("id_1") for p in o.get("pairs", [])]
        pb = [p.get("id_2") for p in o.get("pairs", [])]
        ua, ub = o.get("unmatched_1", []), o.get("unmatched_2", [])
        miss_a = ids_a - set(pa) - set(ua)
        miss_b = ids_b - set(pb) - set(ub)
        if miss_a or miss_b:
            raise ValueError(
                f"unaccounted ids — list1 {sorted(miss_a)[:6]}, "
                f"list2 {sorted(miss_b)[:6]}. Every id appears exactly once.")
        dup = [i for i, c in Counter(pa + list(ua)).items() if c > 1] + \
              [i for i, c in Counter(pb + list(ub)).items() if c > 1]
        if dup:
            raise ValueError(f"ids used more than once: {dup[:6]}")
        ok = {"same_option", "same_fork_different_option", "vaguer"}
        bad = sorted({str(p.get("verdict")) for p in o["pairs"]
                      if p.get("verdict") not in ok})
        if bad:
            raise ValueError(f"verdict must be one of {sorted(ok)}; got {bad}")

    out = ask("16_align_channels", {"list_1": a, "list_2": b},
              schema=MATCH_SCHEMA, model="opus", run_id=f"ablate_{tag}",
              check=check)
    # normalise back to (code, prose) regardless of presentation order
    pairs = []
    for p in out["pairs"]:
        c_id, p_id = (p["id_2"], p["id_1"]) if flip else (p["id_1"], p["id_2"])
        pairs.append({"code_id": c_id, "prose_id": p_id,
                      "verdict": p["verdict"], "why": p.get("why", "")})
    un_code = out["unmatched_2"] if flip else out["unmatched_1"]
    un_prose = out["unmatched_1"] if flip else out["unmatched_2"]
    return {"run": run, "flipped": flip, "pairs": pairs,
            "unmatched_code": un_code, "unmatched_prose": un_prose,
            "n_code": len(code), "n_prose": len(prose)}


def do_match(null=False):
    sp = ABL / "sample.json"
    if not sp.exists():
        sys.exit("run `ablation.py sample` first")
    runs = json.loads(sp.read_text(encoding="utf-8"))["runs"]
    rng = random.Random(SEED + (1 if null else 0))

    jobs = []
    if null:
        # pair run i's code with run j's prose, j != i, same corpus so the
        # comparison is fair. Any match here is false by construction.
        by = defaultdict(list)
        for r in runs:
            by[r["corpus"]].append(r["run"])
        for corp, rs in sorted(by.items()):
            if len(rs) < 2:
                continue
            shifted = rs[1:] + rs[:1]
            for a, b in zip(rs, shifted):
                jobs.append((f"{a}|{b}", a, b))
    else:
        jobs = [(r["run"], r["run"], r["run"]) for r in runs]

    print(f"matching {len(jobs)} run pairs "
          f"({'NULL — mismatched runs' if null else 'within-run'}), "
          f"{WORKERS} workers")
    results, fails = [], []

    def work(job):
        label, ra, rb = job
        code, _ = channels(ra)
        _, prose = channels(rb)
        seed_rng = random.Random(hash(label) & 0xffffffff)
        try:
            r = align_one(label, code, prose, seed_rng,
                          "null" if null else "main")
            return r
        except Exception as e:                                  # noqa: BLE001
            return {"run": label, "error": f"{type(e).__name__}: {e}"[:200]}

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, r in enumerate(ex.map(work, jobs), 1):
            if "error" in r:
                fails.append(r)
                print(f"  FAIL {r['run']}: {r['error'][:90]}", flush=True)
            else:
                results.append(r)
            if i % 10 == 0:
                print(f"  {i}/{len(jobs)}", flush=True)

    p = ABL / ("matches_null.json" if null else "matches.json")
    p.write_text(json.dumps({"null": null, "n": len(results),
                             "failures": fails, "results": results},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(results)} ok, {len(fails)} failed\n-> {p}")


# --------------------------------------------------------------------------
def tally(res):
    v = Counter()
    n_code = n_prose = 0
    for r in res:
        n_code += r["n_code"]
        n_prose += r["n_prose"]
        for p in r["pairs"]:
            v[p["verdict"]] += 1
    matched = sum(v.values())
    return v, matched, n_code, n_prose


def do_report():
    mp = ABL / "matches.json"
    if not mp.exists():
        sys.exit("run `ablation.py match` first")
    main = json.loads(mp.read_text(encoding="utf-8"))["results"]
    npath = ABL / "matches_null.json"
    null = json.loads(npath.read_text(encoding="utf-8"))["results"] \
        if npath.exists() else []

    sample = {r["run"]: r for r in
              json.loads((ABL / "sample.json").read_text(encoding="utf-8"))["runs"]}

    print("CODE ABLATION — gate 5.4\n")
    v, matched, n_code, n_prose = tally(main)
    recall = matched / n_code if n_code else 0
    same = v["same_option"]
    conflict = v["same_fork_different_option"]
    vague = v["vaguer"]
    agree = same / matched if matched else 0
    agree_lenient = (same + vague) / matched if matched else 0

    print(f"  runs                              {len(main)}")
    print(f"  code decisions                    {n_code}")
    print(f"  prose decisions                   {n_prose}")
    print(f"  matched pairs                     {matched}")
    print(f"\n  RECALL   code decisions prose also found   "
          f"{recall:.3f}  ({matched}/{n_code})")
    print(f"  AGREEMENT of matched pairs:")
    print(f"    same option                     {same:>5}  {same/max(1,matched):.3f}")
    print(f"    vaguer (same choice, coarser)   {vague:>5}  {vague/max(1,matched):.3f}")
    print(f"    DIFFERENT option (conflict)     {conflict:>5}  "
          f"{conflict/max(1,matched):.3f}")
    print(f"\n  gate 5.4 asks >= {GATE} land in the same option")
    print(f"    strict  (same_option only)      {agree:.3f}   "
          f"{'PASS' if agree >= GATE else 'FAIL'}")
    print(f"    lenient (same + vaguer)         {agree_lenient:.3f}   "
          f"{'PASS' if agree_lenient >= GATE else 'FAIL'}")

    # ---- null calibration -------------------------------------------------
    if null:
        nv, nmatched, nn_code, _ = tally(null)
        nrecall = nmatched / nn_code if nn_code else 0
        print(f"\n  NULL CALIBRATION  (run i's code vs run j's prose; every "
              f"match is false)")
        print(f"    runs paired                     {len(null)}")
        print(f"    spurious match rate             {nrecall:.3f}  "
              f"(vs {recall:.3f} within-run)")
        print(f"    ratio within/null               "
              f"{recall/nrecall if nrecall else float('inf'):.1f}x")
        print(f"    of those spurious matches, "
              f"'same option'  {nv['same_option']/max(1,nmatched):.3f}")
        if nrecall > 0.25 * recall:
            print(f"    !! the matcher pairs unrelated runs at a comparable "
                  f"rate;\n       the within-run figures above are not "
                  f"trustworthy")
    else:
        print(f"\n  NULL CALIBRATION  not run — `ablation.py match --null`")

    # ---- by corpus ---------------------------------------------------------
    print(f"\n  BY CORPUS  (the gate exists to license pooling, so the split "
          f"matters more\n  than the pooled number)")
    print(f"    {'corpus':<8}{'runs':>6}{'code':>7}{'recall':>9}"
          f"{'same':>8}{'vague':>8}{'conflict':>10}")
    # The corpora present in the sample, not two names. sorted() keeps
    # the report order deterministic across studies.
    for corp in sorted({v.get("corpus") for v in sample.values()
                        if v.get("corpus")}):
        sub = [r for r in main if sample.get(r["run"], {}).get("corpus") == corp]
        if not sub:
            continue
        cv, cm, cc, _ = tally(sub)
        print(f"    {corp:<8}{len(sub):>6}{cc:>7}"
              f"{cm/max(1,cc):>9.3f}"
              f"{cv['same_option']/max(1,cm):>8.3f}"
              f"{cv['vaguer']/max(1,cm):>8.3f}"
              f"{cv['same_fork_different_option']/max(1,cm):>10.3f}")

    # ---- what prose misses, and what only prose has ------------------------
    miss = sum(len(r["unmatched_code"]) for r in main)
    extra = sum(len(r["unmatched_prose"]) for r in main)
    print(f"\n  ASYMMETRY")
    print(f"    code decisions prose never mentions   {miss} "
          f"({miss/max(1,n_code):.1%} of code)")
    print(f"    prose decisions with no code          {extra} "
          f"({extra/max(1,n_prose):.1%} of prose)")
    print(f"    the second number is the silent-decision mirror: things "
          f"claimed\n    in the write-up that the script does not do")

    print(f"\n  CONFLICTS  (same question, different answer — the validity "
          f"problem)")
    shown = 0
    for r in main:
        for p in r["pairs"]:
            if p["verdict"] == "same_fork_different_option" and shown < 10:
                print(f"    {r['run']:<26} {p['why'][:64]}")
                shown += 1

    payload = {"gate": GATE, "runs": len(main),
               "n_code": n_code, "n_prose": n_prose, "matched": matched,
               "recall": round(recall, 4),
               "agreement_strict": round(agree, 4),
               "agreement_lenient": round(agree_lenient, 4),
               "verdicts": dict(v),
               "unmatched_code": miss, "unmatched_prose": extra,
               "null": ({"runs": len(null),
                         "spurious_match_rate": round(nmatched / nn_code, 4)}
                        if null else None)}
    p = P.AUDITS / "ablation.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    print(f"\n-> {p}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "match", "report"])
    ap.add_argument("--frac", type=float, default=0.30)
    ap.add_argument("--null", action="store_true")
    a = ap.parse_args()
    if a.cmd == "sample":
        do_sample(a.frac)
    elif a.cmd == "match":
        do_match(a.null)
    else:
        do_report()
