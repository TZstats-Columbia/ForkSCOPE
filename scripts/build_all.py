#!/usr/bin/env python3
"""The whole v2 workflow, end to end, for any corpus.

    python3 scripts/build_all.py --corpus ai
    python3 scripts/build_all.py --corpus human
    python3 scripts/build_all.py --corpus ai,human      # the pooled analysis

Stages, in order:

    1  distill    artifacts -> exons/introns -> links -> per-run record
    2  index      per-run records -> corpus tables
    3  l1         decisions -> local groups, per corpus, no cap
    4  build      L2 + L3 over the union -> options -> forks
    5  audit      A1-A9 over the clustering, then R1-R4 splits
    6  repair     option/fork vocabulary repair (--repair), then analyse:
               stability, novelty, dose-response, iteration, garden, shapley
    7  viewer     self-contained HTML
    8  gate       validation gate 5.4, code ablation (--gate)

Stages 5 and 6 exist so that no reported number comes from a command someone
typed once. Each analysis script has an audit companion that runs beside it and
prints named checks; a stage that fails its audit stops the workflow.

Every stage is idempotent. Model calls are cached on
sha256(prompt + payload + schema), so re-running an unchanged stage costs
nothing and returns byte-identical output; the cache, not the model, is what
makes this reproducible (the CLI exposes no temperature or seed).

Two rules the workflow enforces rather than leaves to memory:

**L1 runs per corpus, L2/L3 run over the union.** L1 batching depends on sorting
the whole item set, so adding 31 human teams to a pooled sort would reshuffle
every batch and invalidate all 67 cached AI calls. Splitting the phase keeps
local work stable and is the right shape anyway: L1 is local grouping, L2 is
global merging.

**Cluster pooled for any AI-vs-human claim.** Clustering the corpora separately
gives two incomparable vocabularies -- exactly the v1 failure, where the human
side came out ten times finer-grained per record than the AI side and no
comparison between them meant anything.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
S = P.SCRIPTS


MAX_REPAIR_ROUNDS = 3
# A round that moves at most this share of decision points is treated as
# converged. Equality would be the natural test and is the wrong one: merge_forks
# adjudicates every pair above a fixed score, and relabelling shifts scores, so
# each round surfaces a few fresh candidates from the tail. Observed on this
# corpus: 375 -> 329 -> 321 -> 317, merging 46, then 8, then 4. That asymptotes
# without reaching zero, and a loop demanding a strict fixpoint would run to the
# cap on every corpus while implying something it never achieved.
CONVERGED_AT = 0.02


def forks_in(tag):
    """Decision-point count of a vocabulary, for the fixpoint test."""
    import paths as _P
    f = _P.vocab_file(tag)
    if not f.exists():
        return -1
    return len({o["fork"] for o in
                json.loads(f.read_text(encoding="utf-8"))["options"]})


def run(label, argv, allow_fail=False):
    print(f"\n{'='*70}\n{label}\n{'='*70}", flush=True)
    t0 = time.time()
    r = subprocess.run([sys.executable, "-u"] + argv, cwd=str(REPO))
    dt = time.time() - t0
    ok = r.returncode == 0
    print(f"[{label}] {'ok' if ok else 'FAILED'} in {dt/60:.1f} min", flush=True)
    if not ok and not allow_fail:
        sys.exit(f"stage failed: {label}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=P.FINAL_TAG,
                    help="comma-separated: ai, human, or both")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--skip-distill", action="store_true",
                    help="records already exist; start from clustering")
    ap.add_argument("--repair", action="store_true",
                    help="run the vocabulary repair chain (stage 6-1..6-5)")
    ap.add_argument("--gate", action="store_true",
                    help="also run validation gate 5.4 (code ablation)")
    ap.add_argument("--stop-after", choices=["distill", "index", "l1", "build",
                                             "audit", "repair", "analyse", "viewer"])
    a = ap.parse_args()
    corpora = [c.strip() for c in a.corpus.split(",") if c.strip()]
    tag = "+".join(corpora)
    print(f"v2 workflow — corpus: {tag}")

    if not a.skip_distill:
        for c in corpora:
            run(f"1. distill [{c}]",
                [str(S / "distill.py"), "all", "--corpus", c,
                 "--workers", str(a.workers)])
        if a.stop_after == "distill":
            return

    run("2. index", [str(S / "distill.py"), "index"])
    if a.stop_after == "index":
        return

    for c in corpora:
        run(f"3. l1 [{c}]", [str(S / "cluster_up.py"), "l1", "--corpus", c])
    if a.stop_after == "l1":
        return

    run("4. build (L2+L3)",
        [str(S / "cluster_up.py"), "build", "--corpus", ",".join(corpora)])
    if a.stop_after == "build":
        return

    ctag = ",".join(corpora)
    jt = "+".join(corpora)
    OUTC = P.ANALYSIS
    run("5a. audit clusters (A1-A9)",
        [str(S / "audit_clusters.py"), "--corpus", ctag])
    run("5b. repair clusters (R1-R4)",
        [str(S / "repair_clusters.py"), "--corpus", ctag])
    if a.stop_after == "audit":
        return

    # ---- vocabulary repair -------------------------------------------------
    # L2/L3 leave two errors the A/R checks cannot see, both found by reading
    # the garden rather than the metrics. Each pass writes a NEW tag rather
    # than overwriting, so every number ever reported stays reproducible from
    # the vocabulary that produced it, and the filename records the lineage.
    #
    # Order is not arbitrary and cost real errors to establish:
    #   options first   -- collapse paraphrase within a fork
    #   forks second    -- merge duplicate decision points
    #   options AGAIN   -- duplicate forks hid duplicate options from each
    #                      other; this pass found 146 more that were never
    #                      comparable until their forks were united
    #   induce last     -- re-derive decision points from option PURPOSE.
    #                      prompt 13 emitted a fork label per option group in
    #                      isolation and never compared them, so forks were a
    #                      by-product of option merging rather than a
    #                      clustering step. This is that missing step.
    #
    #   then ITERATE     -- induce_forks re-derives fork labels, and any
    #                      duplicate it creates is invisible to merge_forks,
    #                      which already ran. That ordering gap left 46 forks
    #                      unmerged on the first build: a post-induction pass
    #                      adjudicated 147 pairs and judged 103 of them one
    #                      question. Rather than bolt on one more stage and
    #                      leave the same gap behind it, the merge passes now
    #                      repeat until one changes nothing.
    SUFFIX = {"merge_options.py": ".merged", "merge_forks.py": ".forkmerged",
              "induce_forks.py": ".induced"}

    def pass_(label, script, out=None):
        nonlocal jt
        run(f"{label} [run]", [str(S / script), "run", "--corpus", jt])
        args = [str(S / script), "apply", "--corpus", jt]
        if out:
            args += ["--out-tag", out]
        run(f"{label} [apply]", args)
        jt = out or (jt + SUFFIX[script])
        return forks_in(jt)

    if a.repair:
        # BOOTSTRAP THE GARDEN THE FIRST PASS READS.
        #
        # 6-1 merge_options calls audit_granularity.tables(tag), which reads
        # data/analysis/garden_<tag>.json. The only thing that writes that file
        # is finalize_vocab, and in this chain finalize_vocab runs at 6-6 --
        # AFTER the passes that need it. The dependency is circular on a first
        # build and invisible on every later one, because a garden left by a
        # previous build satisfies it.
        #
        # soccer-C is the first study built from nothing, and it died here with
        # FileNotFoundError: garden_ai.json immediately after the repair
        # clusters stage had written the vocabulary. Finalising the pre-repair
        # vocabulary once is not a workaround: coverage, position and stage are
        # exactly what merge_options needs to judge granularity, and computing
        # them on the vocabulary it is about to merge is the correct input.
        if not (P.ANALYSIS / f"garden_{jt}.json").exists():
            run("6-0 finalize pre-repair vocabulary (bootstrap)",
                [str(S / "finalize_vocab.py"), "--corpus", jt])

        for label, script in (
                ("6-1 options: collapse paraphrase", "merge_options.py"),
                ("6-2 forks: merge duplicates", "merge_forks.py"),
                ("6-3 options: re-merge across united forks",
                 "merge_options.py"),
                ("6-4 forks: re-induce from purpose", "induce_forks.py")):
            pass_(label, script)

        # Fixpoint. Capped because a pass that keeps finding merges is a
        # symptom to investigate, not a loop to run harder.
        #
        # Rounds are named `.rN` rather than by appending one suffix per pass.
        # Appending grew the tag to 77 characters that did not say which round
        # was which; `<base>.r2` says it in three. The full lineage stays
        # recoverable inside each file.
        base = jt
        for i in range(1, MAX_REPAIR_ROUNDS + 1):
            before = forks_in(jt)
            pass_(f"6-5.{i} forks: merge post-induction duplicates",
                  "merge_forks.py", f"{base}.r{i}f")
            after = pass_(f"6-5.{i} options: re-merge across united forks",
                          "merge_options.py", f"{base}.r{i}")
            moved = (before - after) / max(1, before)
            print(f"\n  round {i}: {before} -> {after} decision points "
                  f"({moved:.1%})")
            if moved <= CONVERGED_AT:
                print(f"  converged (a round moved <= {CONVERGED_AT:.0%})\n")
                break
        else:
            print(f"\n  NOTE: still merging after {MAX_REPAIR_ROUNDS} rounds. "
                  f"Report where you stopped and how much the last round "
                  f"moved; do not describe the vocabulary as converged.\n")

        run("6-6 finalize vocabulary (coverage, position, stages)",
            [str(S / "finalize_vocab.py"), "--corpus", jt])
        ctag = jt
        print(f"\nrepaired vocabulary: {jt}\n")
        if a.stop_after == "repair":
            return

    # Each pair is production-then-audit. The audit is not optional decoration:
    # iteration in particular reports a headline (97% of runs loop back) that is
    # meaningless without its permutation null, so the two ship together.
    run("6a. stability", [str(S / "stability.py"), "--corpus", ctag,
                          "--json", str(OUTC / f"stability_{jt}.json")])
    run("6b. novelty", [str(S / "novelty.py"), "--corpus", ctag,
                        "--json", str(OUTC / f"novelty_{jt}.json")])
    run("6c. novelty dose-response",
        [str(S / "novelty_curve.py"), "--corpus", ctag,
         "--json", str(OUTC / f"novelty_curve_{jt}.json")])
    # 6d and 6g/6h are skipped after a repair: finalize_vocab has already
    # written fork_stage_ and garden_ for the repaired vocabulary, and running
    # them again would overwrite that map with one built on a sibling merge
    # that is already folded into the labels -- applying the same merge twice.
    if not a.repair:
        run("6d. stage assignment (LLM, cached)",
            [str(S / "iteration.py"), "stages", "--corpus", ctag])
    run("6e. stage iteration", [str(S / "iteration.py"), "run",
                                "--corpus", ctag])
    run("6f. audit iteration (I1-I6)",
        [str(S / "audit_iteration.py"), "--corpus", ctag])
    if not a.repair:
        # garden must follow iteration: its node merge is vetoed by gate/rival
        # verdicts and its gate direction uses the stage labels from 6d.
        run("6g. garden siblings (LLM, cached)",
            [str(S / "garden.py"), "siblings", "--corpus", ctag])
        run("6h. garden map", [str(S / "garden.py"), "map", "--corpus", ctag])
        run("6i. audit garden (G1-G6)",
            [str(S / "audit_garden.py"), "--corpus", ctag])
    run("6j. shapley", [str(S / "shapley_v2.py"), "--corpus", ctag])
    run("6k. audit shapley (H1-H6)",
        [str(S / "audit_shapley.py"), "--corpus", ctag])
    if a.stop_after == "analyse":
        return

    run("7c. fork atlas", [str(S / "fork_atlas.py"), "--corpus", ctag])
    run("7d. fork graph", [str(S / "fork_graph.py"), "--corpus", ctag])
    run("7f. circle + persona routes",
        [str(S / "circle.py"), "--corpus", ctag])

    # Gate 5.4 runs once over the whole corpus, not per --corpus, because it
    # asks whether prose-only runs can be admitted at all. Its sample is drawn
    # from every run with both channels, so re-running it per corpus would
    # re-answer the same question with less data. Off by default: it is a
    # validation gate, not a product of the corpus being built.
    if a.gate:
        run("8a. ablation sample", [str(S / "ablation.py"), "sample"])
        run("8b. ablation match (LLM, cached)",
            [str(S / "ablation.py"), "match"])
        run("8c. ablation null", [str(S / "ablation.py"), "match", "--null"])
        run("8d. ablation report", [str(S / "ablation.py"), "report"])
        run("8e. audit ablation (E1-E6)", [str(S / "audit_ablation.py")])

    print(f"\nworkflow complete for {tag}")


if __name__ == "__main__":
    main()
