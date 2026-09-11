#!/usr/bin/env python3
"""S1-S2 of the v2 pipeline: artifacts -> segmented spans -> links -> a record.

Reads only what data/raw/inputs.json marks RAW. Derived artifacts -- upstream's
decisions_mapped.json and sonnet_llmj.txt, and v1's own records -- are refused
by construction, because feeding one to the parser would launder its taxonomy
into our vocabulary and silently destroy the free-discovery claim.

What it does per run:

  S1  segment the code   -> exons (decisions) + typed introns
      segment the prose  -> claim units + typed non-claims
      Both partitions are *enforced*: the union of line ranges must be exactly
      1..n with no gaps. A violation is fed back to the model as a specific
      correction and retried, because coverage arithmetic is meaningless if the
      partition leaks.

  S2  link exons to claims, with an agreement verdict.

  Then the presence grid is computed *here*, in code, from the links and from
  what was left unlinked. The model does alignment; the bookkeeping is not its
  job. Asking it to classify would let it reason toward a tidy distribution
  instead of leaving an honest residue.

Presence is reported on the C/R basis only -- code and prose. Traces exist for
207 AI runs and no human teams, so a three-channel measure of silence is not
comparable across corpora (see DISTILL_V2_PLAN.md S2).

Usage:
    python3 scripts/distill.py run <run_id>
    python3 scripts/distill.py all [--workers N] [--limit N] [--corpus ai|human]
    python3 scripts/distill.py index
"""
import argparse
import collections
import glob
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402
from llm import ask, LLMError                                  # noqa: E402

REPO = P.ROOT
V2 = P.ROOT
RUNS = P.DISTILLED
CORPUS = P.CORPUS
# Corpora are third-party and large, so they are fetched rather than vendored.
# Where each one lives, what it contains and which artifacts count is declared
# in study.json:corpora and read by discover(). See data/raw/MANIFEST.md.

SEG_SCHEMA = {"type": "object", "required": ["n_lines", "spans"]}
LINK_SCHEMA = {"type": "object", "required": ["links"]}


# ---------- artifact resolution, constrained by the manifest ----------------
def manifest():
    return json.loads((P.RAW / "inputs.json").read_text(encoding="utf-8"))


def _read(p):
    # newline="" is load-bearing: text mode rewrites a lone \r to \n, and
    # splitlines() additionally breaks on \f, which pdftotext emits at page
    # boundaries in the human reports. Either would shift every line number in
    # the file and silently corrupt the spans.
    with open(p, encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read().split("\n")


def stratify(runs, n):
    """Draw n runs spread evenly over the persona arms.

    Taking the first n of a sorted list would load almost everything from
    whichever arm sorts first, and the arms are the comparison this corpus
    exists to support. Deterministic: arms in a fixed order, runs within an arm
    in sorted order, round-robin until n. No RNG, so the sample is the same on
    every machine and every re-run.
    """
    by = {}
    for r in runs:
        by.setdefault(r[3], []).append(r)
    for k in by:
        by[k].sort(key=lambda r: r[0])
    picked, arms = [], sorted(by)
    i = 0
    while len(picked) < n and any(by[a] for a in arms):
        a = arms[i % len(arms)]
        if by[a]:
            picked.append(by[a].pop(0))
        i += 1
    return picked


def _artifact_paths(d, spec, floor):
    """Resolve one role's filename(s) inside run directory `d`.

    A string is one candidate; a list is several, and the LARGEST present wins
    with the runner-up carried as `<role>_secondary`. That is not a nicety --
    two prose channels written at two time points are both evidence, and the
    pipeline reads the fuller one first while keeping the other for the second
    pass.

    `floor` is a size in bytes. It exists because "the file is there" and "the
    file has content" are different claims: an unfetched Git-LFS pointer is
    valid UTF-8 at ~130 bytes, and a stub report is not a write-up.
    """
    names = [spec] if isinstance(spec, str) else list(spec)
    found = [(f.stat().st_size, str(f)) for f in (Path(d) / n for n in names)
             if f.exists() and f.stat().st_size >= floor]
    found.sort(reverse=True)
    return [pth for _, pth in found]


def discover(corpus=None):
    """[(run_id, corpus, {role: path}, arm)] for every run with usable material.

    Driven entirely by `study.json:corpora`, so a second study is a manifest
    change rather than a code change. Per corpus it reads:

        glob           matches ONE run directory, relative to the corpus root
        artifacts      {role: filename} or {role: [candidates]}
        required       roles a run must have; default every role in artifacts
        min_bytes      {role: floor}; default 1, i.e. merely non-empty
        arm_from_path  regex with one group, read off the run's path
        arm            a constant arm, when the corpus has only one

    The run id is the basename of the matched directory. Corpora are visited in
    sorted order and runs within a corpus in sorted path order, so the result
    is deterministic on every machine.
    """
    out = []
    for name in P.corpora():
        if corpus not in (None, name):
            continue
        c = P.STUDY["corpora"][name]
        arts_spec = c.get("artifacts") or {}
        required = c.get("required") or list(arts_spec)
        floors = c.get("min_bytes") or {}
        arm_re = c.get("arm_from_path")

        for d in sorted(glob.glob(P.corpus_glob(name))):
            if not os.path.isdir(d):
                continue
            arts = {}
            for role, spec in arts_spec.items():
                hits = _artifact_paths(d, spec, floors.get(role, 1))
                if hits:
                    arts[role] = hits[0]
                    if len(hits) > 1:
                        arts[f"{role}_secondary"] = hits[1]
            if any(r not in arts for r in required):
                continue
            if arm_re:
                m = re.search(arm_re, d.replace("\\", "/"))
                arm = m.group(1) if m else "unknown"
            else:
                arm = c.get("arm", name)
            out.append((os.path.basename(d.rstrip("/")), name, arts, arm))
    return out


# ---------- the partition invariant ----------------------------------------
def partition_error(obj, n, exclusive=True):
    """Return a specific complaint, or None if the cover is acceptable.

    Both artifact kinds must be *exhaustive* -- every line assigned -- because
    that is what turns "the parser didn't look here" into a disputable claim.

    Only code must also be *exclusive*. The exon model says a line of code
    belongs to one decision; prose does not work that way. A single sentence
    routinely asserts two separable things ("we averaged the raters and dropped
    unrated players"), and demanding an exclusive partition of prose fights the
    data rather than measuring it -- it cost three retries a run before this was
    relaxed. Overlapping claims are the norm and are allowed; overlapping exons
    are a modelling error and are not.
    """
    seen, overlaps = {}, []
    for s in obj.get("spans", []):
        if not isinstance(s, dict):
            return f"a span is {type(s).__name__}, not an object"
        sid = s.get("id")
        # The model occasionally returns nested lists here. Coerce to hashable
        # scalars rather than letting set() raise: a malformed field is bad
        # output to be corrected on retry, not a crash that kills the run.
        raw_shares = s.get("shares_lines_with") or []
        if not isinstance(raw_shares, (list, tuple)):
            raw_shares = [raw_shares]
        shares = {x for x in raw_shares if isinstance(x, (str, int, float))}
        for rng in s.get("lines", []):
            if not (isinstance(rng, list) and len(rng) == 2):
                return f"span {sid} has a malformed range {rng!r}"
            a, b = rng
            # Endpoints occasionally come back as nested lists or strings.
            # Compare only after confirming they are integers: a TypeError here
            # aborts the whole run, whereas a returned complaint is just another
            # correction the model can act on.
            if not (isinstance(a, int) and isinstance(b, int)):
                return (f"span {sid} range [{a!r},{b!r}] must be two integers, "
                        f"not {type(a).__name__}/{type(b).__name__}")
            if not (1 <= a <= b <= n):
                return f"span {sid} range [{a},{b}] is outside 1..{n}"
            for L in range(a, b + 1):
                prev = seen.get(L)
                # a declared share is not an overlap: check the *other* span's
                # id against this one's list, not the span against itself
                if prev is not None and prev not in shares:
                    overlaps.append((L, prev, sid))
                seen[L] = sid
    missing = [L for L in range(1, n + 1) if L not in seen]
    if missing:
        head = ", ".join(map(str, missing[:12]))
        return (f"{len(missing)} line(s) unassigned: {head}"
                f"{' ...' if len(missing) > 12 else ''}. Every line 1..{n} must "
                f"appear in at least one span.")
    if exclusive and overlaps:
        head = "; ".join(f"line {L} in spans {a} and {b}" for L, a, b in overlaps[:8])
        return (f"{len(overlaps)} overlapping line(s): {head}. Each line of code "
                f"belongs to one decision; declare a genuine dual-purpose line in "
                f"shares_lines_with.")
    return None


def _checked(n, exclusive=True):
    def check(obj):
        err = partition_error(obj, n, exclusive)
        if err:
            raise ValueError(err)
    return check


# A note conceding agreement under a `misaligned` verdict is self-contradiction,
# and it is cheap to catch mechanically rather than hoping the prompt holds. An
# independent typology pass found 6 of 85 misalignments were of this kind (7%),
# which is a measurement error in a headline number. Matched on whole words so
# "consistent" fires but "inconsistent" does not.
_CONCEDES = re.compile(
    r"(?<!in)\bconsistent\b|\baligned?\b|\bmatch(?:es|ing)?\b|\bthe same\b"
    r"|\bno (?:material )?(?:difference|discrepancy|disagreement)\b"
    r"|\bagree(?:s|ment)?\b", re.I)


def link_error(obj):
    """Reject a link set that contradicts itself. Returns a complaint or None."""
    for l in obj.get("links", []):
        if not isinstance(l, dict):
            return f"a link is {type(l).__name__}, not an object"
        if l.get("agreement") not in ("aligned", "misaligned"):
            return (f"link {l.get('decision_id')}->{l.get('claim_id')} has "
                    f"agreement {l.get('agreement')!r}; must be "
                    f"'aligned' or 'misaligned'")
        note = l.get("note") or ""
        if l["agreement"] == "misaligned":
            if not note.strip():
                return (f"link {l.get('decision_id')}->{l.get('claim_id')} is "
                        f"misaligned with an empty note; state the specific "
                        f"discrepancy or mark it aligned")
            m = _CONCEDES.search(note)
            if m:
                return (f"link {l.get('decision_id')}->{l.get('claim_id')} is "
                        f"marked misaligned but its note concedes agreement "
                        f"({m.group(0)!r}): {note[:120]!r}. If the two agree, "
                        f"the verdict is 'aligned' or there is no link.")
    return None


def _link_check(obj):
    err = link_error(obj)
    if err:
        raise ValueError(err)


def coverage(obj, n, kind_key):
    ex = sum(b - a + 1 for s in obj["spans"] if s["kind"] == kind_key
             for a, b in s["lines"])
    intr = {}
    for s in obj["spans"]:
        if s["kind"] == kind_key:
            continue
        k = s.get("subtype", "other")
        intr[k] = intr.get(k, 0) + sum(b - a + 1 for a, b in s["lines"])
    return {"n_lines": n, "functional_lines": ex,
            "functional_share": round(ex / n, 4) if n else 0.0,
            "by_type": dict(sorted(intr.items(), key=lambda x: -x[1]))}


# ---------- one run ---------------------------------------------------------
def numbered(lines):
    return "\n".join(f"{i+1}\t{l}" for i, l in enumerate(lines))


def do_run(rid, corpus, arts, force=False, arm=None):
    outdir = RUNS / rid
    outdir.mkdir(parents=True, exist_ok=True)
    rec_path = outdir / "record.json"
    if rec_path.exists() and not force:
        return json.loads(rec_path.read_text(encoding="utf-8"))

    # The two segmentations are independent -- only the link step needs both --
    # so they run concurrently. The global cap in llm.py keeps this from
    # multiplying against the outer per-run pool.
    def seg_prose():
        # Symmetric with seg_code below, and it was not. The pipeline was built
        # for the human corpus, where prose is always present and 12 of 31 runs
        # have no script -- so code was guarded and prose was not. This corpus
        # is the mirror case: every run has a script and three have no usable
        # write-up. Owner decision A3 requires those to COUNT AS RUNS, and
        # study.json sets required:["code"] accordingly, but this line dropped
        # them with KeyError: 'prose' after the code segmentation was paid for.
        if not arts.get("prose"):
            return None, None
        lines = _read(arts["prose"])
        return lines, ask("02_segment_prose",
                          {"path": os.path.basename(arts["prose"]),
                           "n_lines": len(lines), "text": numbered(lines)},
                          schema=SEG_SCHEMA, check=_checked(len(lines), exclusive=False),
                          run_id=rid)

    def seg_code():
        if not arts.get("code"):
            return None, None
        lines = _read(arts["code"])
        return lines, ask("01_segment_code",
                          {"path": os.path.basename(arts["code"]),
                           "n_lines": len(lines), "code": numbered(lines)},
                          schema=SEG_SCHEMA, check=_checked(len(lines)), run_id=rid)

    with ThreadPoolExecutor(max_workers=2) as ex:
        fp, fc = ex.submit(seg_prose), ex.submit(seg_code)
        _, ps = fp.result()
        _, cs = fc.result()

    if ps:
        (outdir / "prose_spans.json").write_text(
            json.dumps(ps, ensure_ascii=False, indent=1), encoding="utf-8")
    if cs:
        (outdir / "code_spans.json").write_text(
            json.dumps(cs, ensure_ascii=False, indent=1), encoding="utf-8")
    return link_and_record(rid, corpus, arm, arts, ps, cs, outdir)


def link_and_record(rid, corpus, arm, arts, ps, cs, outdir):
    """Align the two segmentations, then derive the record from the residue.

    Split out of do_run so relink.py can rebuild the links and everything
    derived from them without re-segmenting. The presence grid, the silent
    decisions and the misalignments all fall out of what fails to align, so
    there must be exactly one implementation of it -- two would drift, and the
    drift would be invisible in the numbers.
    """
    rec_path = outdir / "record.json"
    claims = [s for s in ps["spans"] if s["kind"] == "claim"] if ps else []
    decisions = [s for s in cs["spans"] if s["kind"] == "decision"] if cs else []

    links = []
    if decisions and claims:
        lk = ask("03_link",
                 {"decisions": [{"id": s["id"], "operation": s["operation"],
                                 "targets": s.get("targets", [])} for s in decisions],
                  "claims": [{"id": s["id"], "assertion": s["assertion"],
                              "polarity": s.get("polarity"),
                              "targets": s.get("targets", [])} for s in claims]},
                 schema=LINK_SCHEMA, model="opus", check=_link_check, run_id=rid)
        links = lk["links"]
        (outdir / "links.json").write_text(
            json.dumps(lk, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- presence grid, computed here rather than asked for ----
    linked_d = {l["decision_id"] for l in links}
    linked_c = {l["claim_id"] for l in links}
    # 'found' claims assert a RESULT, not an action; they were never going to
    # link to a decision that performs an operation. Counting them as unbacked
    # would be a category error. They are held for a separate results pass.
    action_claims = [c for c in claims if c.get("polarity") != "found"]
    result_claims = [c for c in claims if c.get("polarity") == "found"]
    negatives = [c for c in action_claims
                 if c.get("polarity") in ("did_not", "would_have")
                 and c["id"] not in linked_c]

    rec = {
        "run_id": rid, "corpus": corpus, "arm": arm or corpus,
        "artifacts": {k: os.path.basename(v) for k, v in arts.items()},
        "coverage": {
            "code": coverage(cs, cs["n_lines"], "decision") if cs else None,
            "prose": coverage(ps, ps["n_lines"], "claim") if ps else None,
        },
        "counts": {
            "decisions": len(decisions), "claims": len(claims),
            "action_claims": len(action_claims), "result_claims": len(result_claims),
            "links": len(links),
            "misaligned": sum(1 for l in links if l.get("agreement") == "misaligned"),
        },
        "prose_absent": not ps,
        "presence": {
            "CR_executed_and_disclosed": len(linked_d),
            # UNASSESSABLE, not silent. A silent decision is one the analyst
            # performed and did not disclose; that is a property of the pair.
            # With no write-up there is nothing to have disclosed it in, so
            # counting these as silent would inflate the headline figure with
            # runs that could never have contributed to it. This keeps the
            # silent count on A3's denominator of 204 by construction.
            "C_only_silent_decision": 0 if not ps else len(decisions) - len(linked_d),
            "C_unassessable_no_prose": len(decisions) if not ps else 0,
            "R_only_unbacked_action_claim":
                len([c for c in action_claims if c["id"] not in linked_c])
                - len(negatives),
            "R_only_consistent_negative": len(negatives),
            "result_claims_deferred": len(result_claims),
        },
        "silent_decisions": [] if not ps else [
            {"id": s["id"], "lines": s["lines"], "confidence": s.get("confidence"),
             "operation": s["operation"], "targets": s.get("targets", [])}
            for s in decisions if s["id"] not in linked_d],
        "misalignments": [
            {"decision": next(d["operation"] for d in decisions
                              if d["id"] == l["decision_id"]),
             "claim": next(c["assertion"] for c in claims
                           if c["id"] == l["claim_id"]),
             "note": l.get("note", "")}
            for l in links if l.get("agreement") == "misaligned"],
    }
    rec_path.write_text(json.dumps(rec, ensure_ascii=False, indent=1),
                        encoding="utf-8")
    (outdir / "summary.md").write_text(summary_md(rec, decisions, links, claims),
                                       encoding="utf-8")
    return rec


def summary_md(rec, decisions, links, claims):
    byd = {}
    for l in links:
        byd.setdefault(l["decision_id"], []).append(l)
    cl = {c["id"]: c for c in claims}
    L = [f"# {rec['run_id']}  ({rec['corpus']})", ""]
    cov = rec["coverage"]
    if cov["code"]:
        L += [f"- code: {cov['code']['n_lines']} lines, "
              f"{cov['code']['functional_share']:.0%} exon "
              f"({cov['code']['functional_lines']} lines in {rec['counts']['decisions']} decisions)",
              f"- intron: " + ", ".join(f"{k} {v}"
                                        for k, v in cov["code"]["by_type"].items())]
    if cov["prose"]:
        L += [f"- prose: {cov['prose']['n_lines']} lines, {rec['counts']['claims']} claims "
              f"({rec['counts']['action_claims']} action, {rec['counts']['result_claims']} result)"]
    else:
        L += ["- prose: NONE -- no usable write-up (A3: counts as a run; its "
              "decisions are unassessable, not silent)"]
    L += [
          f"- links: {rec['counts']['links']} ({rec['counts']['misaligned']} misaligned)",
          "", "## Presence (code / prose basis)", ""]
    for k, v in rec["presence"].items():
        L.append(f"- {k}: {v}")
    if rec["silent_decisions"]:
        L += ["", "## Silent decisions — executed, never disclosed", ""]
        for s in rec["silent_decisions"]:
            rng = ", ".join(f"{a}-{b}" if a != b else str(a) for a, b in s["lines"])
            L.append(f"- **{rng}** [{s['confidence']}] {s['operation']}")
    if rec["misalignments"]:
        L += ["", "## Misaligned — code and prose disagree", ""]
        for m in rec["misalignments"]:
            L += [f"- code: {m['decision']}", f"  - prose: {m['claim']}",
                  f"  - why: {m['note']}"]
    if decisions:
        L += ["", "## All decisions", ""]
        for s in sorted(decisions, key=lambda x: x["lines"][0][0]):
            rng = ", ".join(f"{a}-{b}" if a != b else str(a) for a, b in s["lines"])
            tag = "SILENT" if s["id"] not in byd else f"linked x{len(byd[s['id']])}"
            L.append(f"- `{rng}` [{s.get('confidence','?')}] **{tag}** — "
                     f"{s['operation']}")
    return "\n".join(L) + "\n"


# ---------- corpus roll-up --------------------------------------------------
def index():
    CORPUS.mkdir(parents=True, exist_ok=True)
    recs = [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(RUNS.glob("*/record.json"))]
    if not recs:
        print("no runs distilled yet")
        return
    # Records written before `arm` existed have none. Recover it from the corpus
    # layout rather than re-running them: the arm is a property of where the run
    # lives, so it is always derivable and never worth a model call to restore.
    known = {rid: a for rid, _c, _arts, a in discover()}
    for r in recs:
        if not r.get("arm") or r["arm"] == r["corpus"]:
            r["arm"] = known.get(r["run_id"], r.get("arm") or r["corpus"])
    cov = ["run_id\tcorpus\tarm\tcode_lines\texon_share\tdecisions\tclaims\tlinks"
           "\tsilent\tmisaligned"]
    sil = ["run_id\tarm\tlines\tconfidence\toperation"]
    mis = ["run_id\tarm\tnote\tcode_operation\tprose_claim"]
    for r in recs:
        c = r["coverage"]["code"]
        arm = r.get("arm", r["corpus"])
        cov.append("\t".join(map(str, [
            r["run_id"], r["corpus"], arm, c["n_lines"] if c else "",
            f"{c['functional_share']:.3f}" if c else "",
            r["counts"]["decisions"], r["counts"]["claims"], r["counts"]["links"],
            r["presence"]["C_only_silent_decision"], r["counts"]["misaligned"]])))
        for s in r["silent_decisions"]:
            rng = ",".join(f"{a}-{b}" for a, b in s["lines"])
            sil.append(f"{r['run_id']}\t{arm}\t{rng}\t{s['confidence']}"
                       f"\t{s['operation']}")
        for m in r["misalignments"]:
            mis.append(f"{r['run_id']}\t{arm}\t{m['note']}"
                       f"\t{m['decision']}\t{m['claim']}")
    (CORPUS / "coverage.tsv").write_text("\n".join(cov) + "\n", encoding="utf-8")
    (CORPUS / "silent_decisions.tsv").write_text("\n".join(sil) + "\n", encoding="utf-8")
    (CORPUS / "misalignments.tsv").write_text("\n".join(mis) + "\n", encoding="utf-8")

    # Per-arm breakdown: the reason the sample is stratified at all. Rates are
    # per decision, not per run, so an arm that writes longer scripts does not
    # look more secretive purely for having more decisions to be silent about.
    arms = collections.defaultdict(lambda: collections.Counter())
    for r in recs:
        a = arms[r.get("arm", r["corpus"])]
        a["runs"] += 1
        a["decisions"] += r["counts"]["decisions"]
        a["silent"] += r["presence"]["C_only_silent_decision"]
        a["misaligned"] += r["counts"]["misaligned"]
        a["claims"] += r["counts"]["claims"]
    arm_rows = ["arm\truns\tdecisions\tsilent\tsilent_per_decision"
                "\tmisaligned\tmisaligned_per_run"]
    for k in sorted(arms):
        a = arms[k]
        arm_rows.append(
            f"{k}\t{a['runs']}\t{a['decisions']}\t{a['silent']}"
            f"\t{a['silent']/a['decisions']:.3f}" if a["decisions"] else
            f"{k}\t{a['runs']}\t0\t0\t")
        arm_rows[-1] += f"\t{a['misaligned']}\t{a['misaligned']/a['runs']:.2f}"
    (CORPUS / "by_arm.tsv").write_text("\n".join(arm_rows) + "\n", encoding="utf-8")

    nd = sum(r["counts"]["decisions"] for r in recs)
    ns = sum(r["presence"]["C_only_silent_decision"] for r in recs)
    nm = sum(r["counts"]["misaligned"] for r in recs)
    shares = [r["coverage"]["code"]["functional_share"] for r in recs
              if r["coverage"]["code"]]
    md = [f"# v2 distillation — {len(recs)} runs", "",
          f"- decisions: {nd} (median {nd/len(recs):.1f} per run)",
          f"- silent decisions: {ns} ({ns/nd:.1%} of decisions)" if nd else "",
          f"- misalignments: {nm}",
          f"- exon share of code: median {sorted(shares)[len(shares)//2]:.1%}"
          if shares else "",
          "", "Files: `coverage.tsv`, `silent_decisions.tsv`, "
          "`misalignments.tsv`; per-run detail in `../distilled/<run_id>/summary.md`."]
    (CORPUS / "index.md").write_text("\n".join(x for x in md if x) + "\n",
                                     encoding="utf-8")
    print(f"{len(recs)} runs | {nd} decisions | {ns} silent | {nm} misaligned")
    print(f"-> {CORPUS}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "all", "index"])
    ap.add_argument("run_id", nargs="?")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--corpus", choices=P.corpora(),
                    help="restrict to one corpus; default all of them")
    ap.add_argument("--stratify", type=int,
                    help="draw N runs spread evenly over persona arms")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if a.cmd == "index":
        return index()

    runs = discover(a.corpus)

    # Zero runs is never a success. It used to print "0 run(s)" and exit 0,
    # which is the silent-wrong class: a new study looks like it distilled
    # cleanly, every downstream stage runs on nothing, and the first sign of
    # trouble is a plausible number much later. Fail here, and say what to
    # check -- an unset corpus root and a glob that matches nothing are the two
    # causes, and they need different fixes.
    if not runs:
        where = []
        for nm in P.corpora():
            if a.corpus not in (None, nm):
                continue
            c = P.STUDY["corpora"][nm]
            env = c.get("env")
            val = os.environ.get(env) if env else None
            arts = c.get("artifacts") or {}
            where.append(
                f"  {nm}\n"
                f"      glob      {P.corpus_glob(nm)}\n"
                f"      artifacts {', '.join(f'{k}={v}' for k, v in arts.items()) or '(none declared)'}\n"
                f"      required  {', '.join(c.get('required') or list(arts)) or '(none)'}\n"
                f"      {env or 'env'}={val or '(unset, using default)'}")

        sys.exit(
            "no runs found — nothing was distilled.\n\n"
            + "\n".join(where) + "\n\n"
            "A run counts only when its artifacts are present and non-empty.\n"
            "Check, in this order:\n"
            "  1. the corpus is fetched:  python3 scripts/fetch_corpus.py status\n"
            "  2. the checksums verify:   python3 scripts/fetch_corpus.py verify\n"
            "     an unfetched Git-LFS pointer is valid UTF-8 and ~130 bytes,\n"
            "     so it passes existence checks and carries no analysis\n"
            "  3. study.json:corpora[*].glob matches ONE run directory,\n"
            "     relative to the corpus root, and names the right artifacts\n"
            "  4. FORKSCOPE_STUDY is UNSET for the packaged study — setting it\n"
            "     to the study you are already in resolves to studies/<name>/,\n"
            "     which does not exist")

    if a.cmd == "run":
        runs = [r for r in runs if r[0] == a.run_id]
        if not runs:
            sys.exit(f"no such run: {a.run_id}")
    if a.stratify:
        runs = stratify(runs, a.stratify)
    elif a.limit:
        runs = runs[:a.limit]
    byarm = collections.Counter(r[3] for r in runs)
    print(f"{len(runs)} run(s), {a.workers} worker(s)")
    print(f"  arms: {dict(sorted(byarm.items()))}", flush=True)

    done = fail = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(do_run, rid, c, arts, a.force, _arm): rid
                for rid, c, arts, _arm in runs}
        for f in as_completed(futs):
            rid = futs[f]
            try:
                r = f.result()
                done += 1
                print(f"  ok   {rid}  {r['counts']['decisions']:>3} decisions, "
                      f"{r['presence']['C_only_silent_decision']:>2} silent, "
                      f"{r['counts']['misaligned']} misaligned", flush=True)
            except Exception as e:
                fail += 1
                print(f"  FAIL {rid}  {type(e).__name__}: {str(e)[:120]}", flush=True)
    print(f"\n{done} ok, {fail} failed")
    index()


if __name__ == "__main__":
    main()
