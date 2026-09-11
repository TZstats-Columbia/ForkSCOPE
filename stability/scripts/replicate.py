#!/usr/bin/env python3
"""Set up and drive a replicate build under an isolated study root.

WHY NOT `nocache=True`
----------------------
The obvious way to force fresh model calls is `ask(..., nocache=True)`. It is
the wrong tool here and the reason is not obvious: `nocache` skips the cache
READ but still WRITES the result to the same key. Running it in place would
overwrite the very entries the baseline is made of -- destroying build A while
measuring it, irreversibly, with no error.

So a replicate instead gets its own STUDY_ROOT with an EMPTY cache. Every call
misses and goes to the model, which is exactly what `nocache` was for, and the
baseline cache is not merely left alone but structurally out of reach. The
isolation is a property of the filesystem layout rather than of remembering to
pass a flag.

WHAT IS SHARED AND WHAT IS FRESH
--------------------------------
    shared (read-only)   data/raw          the corpus itself
                         study.json        the study manifest
                         prompts/          hashed into the cache key
    copied in            data/distilled    stage 1 output, when replicating
                                           only the vocabulary (stages 3-6)
    fresh                cache/            empty: every call is a real call
                         data/{vocabulary,analysis,audits,corpus}
                         figures/

Copying `data/distilled` in is what makes a vocabulary replicate a CLEAN one:
the input to stage 3 is byte-identical to build A's, so any difference
downstream is variability in the vocabulary induction and nothing else. A
distillation replicate leaves it out and lets stage 1 run.

PROVENANCE
----------
Writes `manifest.json` recording what the pipeline itself does not: git SHA,
wall-clock start, the model ALIASES used, and -- if the CLI will report it --
the resolved client version. The alias/version gap is a known hazard (see
docs/LIMITATIONS or the paper's reproducibility section); recording what we can
is the partial mitigation available without changing llm.py.

Usage:
    python3 stability/scripts/replicate.py init  --root ../replicates/B --stage vocab
    python3 stability/scripts/replicate.py init  --root ../replicates/B --stage distill \\
                                                 --sample 30
    python3 stability/scripts/replicate.py run   --root ../replicates/B --stage vocab \\
                                                 --corpus ai,human
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent                       # the package root
sys.path.insert(0, str(REPO / "scripts"))
import paths as P                                              # noqa: E402
SEED = 20260822


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw).stdout.strip()


def stratified_runs(n, seed=SEED):
    """Draw n runs spread evenly over persona arms, deterministically.

    Mirrors distill.stratify: arms in fixed order, runs sorted within arm,
    round-robin. Taking the first n of a sorted list would load almost
    everything from whichever arm sorts first, and the arms are the comparison
    the corpus exists to support.
    """
    by = defaultdict(list)
    for d in sorted((REPO / "data" / "distilled").glob("*")):
        rec = d / "record.json"
        if not rec.exists():
            continue
        r = json.loads(rec.read_text(encoding="utf-8"))
        by[r.get("arm") or r.get("corpus")].append(d.name)
    out, arms = [], sorted(by)
    for k in arms:
        by[k].sort()
    i = 0
    while len(out) < n and any(len(by[k]) > i for k in arms):
        for k in arms:
            if len(by[k]) > i and len(out) < n:
                out.append(by[k][i])
        i += 1
    return sorted(out)


def _mdl(role):
    """What this replicate will ACTUALLY ask for, not the alias name.

    This field used to be the hardcoded strings "sonnet" and "opus", with a note
    saying the resolved version was not exposed by the CLI. Both were wrong. The
    pins in FORKSCOPE_MODEL_BULK / FORKSCOPE_MODEL_ADJ change what is requested,
    and llm.py records what answered as model_resolved on every call.

    Recording the alias regardless is how builds A, B and R ended up with 2273
    and 3307 calls that cannot be attributed to any model -- see F21. A
    replicate whose manifest cannot say what read it cannot be compared to the
    build it is a replicate OF, which is the only thing it is for.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_llm", str(REPO / "scripts" / "llm.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m._role(role)


def init(root, stage, sample, runs_from=None, distilled_from=None,
         from_vocab=None, parent_root=None):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    # THE STUDY'S manifest, not the template at the repo root.
    #
    # REPO is the package root, where study.json is the blank template with
    # "env": "FORKSCOPE_RAW_CORPUS_NAME" and a placeholder glob. Copying that
    # gave the replicate a manifest describing no corpus, and preflight
    # correctly refused on an env var nobody has ever set. It went unnoticed
    # while every study's root WAS the repo root; soccer-C is the first with
    # its own, and this is the third place that assumption was baked in --
    # after _selfcheck's docs/ reads and preflight's hardcoded corpora.
    #
    # A replicate is only meaningful against the build it replicates, so it
    # must carry that build's manifest byte for byte.
    src_study = P.ROOT / "study.json"
    if not src_study.exists():
        sys.exit(f"no study.json at {src_study} -- set FORKSCOPE_STUDY")
    shutil.copy2(src_study, root / "study.json")
    pol = P.ROOT / "policy.json"
    if pol.exists():
        shutil.copy2(pol, root / "policy.json")

    (root / "data").mkdir(exist_ok=True)

    # INPUTS the pipeline reads but does not produce. Each has to be carried
    # into the replicate root or a stage dies on a missing file, and the death
    # arrives mid-run rather than at startup.
    #
    # `outcomes/` is the subtle one: it is the payout side of the multiverse
    # analysis (effect size, CI, verdict per run), was assembled outside this
    # package, and has NO generator here -- see data/outcomes/README.md. It
    # looks like pipeline output because it lives under data/, and it is not.
    if (root / "data" / "raw").exists():
        shutil.rmtree(root / "data" / "raw")
    shutil.copytree(REPO / "data" / "raw", root / "data" / "raw",
                    ignore=shutil.ignore_patterns("afp", "human_corpus"))
    if (REPO / "data" / "outcomes").exists():
        if (root / "data" / "outcomes").exists():
            shutil.rmtree(root / "data" / "outcomes")
        shutil.copytree(REPO / "data" / "outcomes", root / "data" / "outcomes")

    # Create the full output tree using the PIPELINE's own definition of it,
    # not a copy of the list. paths.ensure_dirs() names every directory the
    # stages write to; duplicating that list here would drift the moment a
    # stage gains an output, and the failure mode is silent for 40 minutes --
    # L2/L3 completes, then dies writing its result to a missing directory.
    env = dict(os.environ, FORKSCOPE_STUDY=str(root))
    r = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, sys.argv[1]); "
         "import paths; paths.ensure_dirs(); print('dirs ok')",
         str(REPO / "scripts")],
        env=env, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"could not create output dirs under {root}:\n{r.stderr}")

    picked = []
    dst = root / "data" / "distilled"
    if stage == "forks":
        # A FORK replicate freezes the options layer and re-runs only fork
        # formation. It exists because the three layers do not fail together:
        # distillation and decisions->options reproduce well, options->forks
        # does not, and a whole-vocabulary replicate cannot say how much of the
        # fork disagreement is fork induction's own noise rather than inherited
        # from options that already differed.
        #
        # So the parent's vocabulary is copied in and NOT rebuilt. Only that
        # one file: the downstream tags this run is about to write must not
        # already exist, or `induce_forks` reads a fork layer some earlier build
        # produced and the replicate silently measures nothing.
        # The parent build, which is NOT always this repo. A fork replicate of
        # build B must take B's analysis: `merge_forks` reads
        # garden_<tag>.json, and A's garden describes a different fork layer.
        # Copying the repo's by default would quietly give every B replicate
        # A's sibling structure, and the resulting agreement would be an
        # artifact of the shared input rather than a measurement.
        PR = Path(parent_root).resolve() if parent_root else REPO
        if not (PR / "data").is_dir():
            sys.exit(f"--parent-root has no data/: {PR}")

        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(PR / "data" / "distilled", dst)

        for d in ("analysis", "audits", "corpus"):
            src_d = PR / "data" / d
            if src_d.is_dir():
                dst_d = root / "data" / d
                if dst_d.exists():
                    shutil.rmtree(dst_d)
                shutil.copytree(src_d, dst_d)

        src_v = Path(from_vocab) if from_vocab and Path(from_vocab).exists() \
            else PR / "data" / "vocabulary" / f"bottom_up_{from_vocab}.json"
        if not src_v.exists():
            sys.exit(f"--from-vocab: no such vocabulary: {src_v}")
        vdir = root / "data" / "vocabulary"
        if vdir.exists():
            shutil.rmtree(vdir)
        vdir.mkdir(parents=True)
        shutil.copy2(src_v, vdir / src_v.name)
        picked = []
    elif stage == "vocab":
        # Clean vocabulary replicate: identical stage-1 input.
        if dst.exists():
            shutil.rmtree(dst)
        src = Path(distilled_from) if distilled_from else REPO / "data" / "distilled"
        if runs_from:
            # Restrict to the runs present in another tree. Needed to compare a
            # vocabulary against one built on a DIFFERENT distillation of the
            # same runs: both sides must see the same run set, or corpus size
            # is confounded with run-to-run variability and the comparison
            # measures the wrong thing.
            keep = {p.name for p in Path(runs_from).iterdir()
                    if (p / "record.json").exists()}
            dst.mkdir(parents=True)
            for name in sorted(keep):
                if (src / name / "record.json").exists():
                    shutil.copytree(src / name, dst / name)
            print(f"  restricted to {len(list(dst.iterdir()))} runs "
                  f"present in {runs_from}")
        else:
            shutil.copytree(src, dst)
    else:
        # Distillation replicate: stage 1 must actually run, so the target
        # directory starts empty. do_run() returns any existing record
        # untouched, so a leftover record.json would silently make this a
        # no-op that looks like perfect stability.
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        # Sampling is delegated to `distill.py --stratify`, not done here.
        # distill.stratify() draws over arms recovered from the RAW corpus
        # layout; this module would have to read them from record.json, where
        # 43 runs carry the stale `ai` arm. Stratifying on those would silently
        # treat a bookkeeping artifact as a sixth experimental arm.
        picked = []

    manifest = {
        "root": str(root), "stage": stage,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "git_sha": sh(["git", "rev-parse", "HEAD"], cwd=str(REPO)),
        "git_branch": sh(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                         cwd=str(REPO)),
        "baseline_repo": str(REPO),
        "model_aliases": {"bulk": _mdl("sonnet"), "adjudication": _mdl("opus")},
        "cli_version": sh(["claude", "--version"]) or "unrecorded",
        "note": ("Model ALIASES are recorded; the resolved model version is "
                 "recorded per call in cache/llm_runs as model_resolved; "
                 "check it with scripts/check_model.py. Two builds "
                 "with the same alias may not be the same model."),
        "sample_runs": picked,
        "sample_n": len(picked),
        "sample_n_requested": sample,
        "parent_vocab": from_vocab if stage == "forks" else None,
        "parent_root": (str(Path(parent_root).resolve()) if parent_root
                        else str(REPO)) if stage == "forks" else None,
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=1),
                                        encoding="utf-8")
    print(f"initialised replicate root: {root}")
    print(f"  stage         {stage}")
    # Report the real count, not "empty". Re-initialising after a failed run
    # keeps the cache on purpose -- that is what makes a retry nearly free --
    # and printing "empty" would misrepresent both the isolation and the cost.
    n_cached = len(list((root / "cache" / "llm_cache").glob("*.json")))
    print(f"  cache         {n_cached} entries"
          f"{' (fresh)' if not n_cached else ' (kept; a retry resumes from it)'}")
    n_dist = len(list((root / "data" / "distilled").glob("*/record.json")))
    print(f"  distilled     {f'{n_dist} runs copied in' if stage in ('vocab', 'forks') else f'empty, {len(picked)} runs to build'}")
    if stage == "forks":
        nv = len(list((root / "data" / "vocabulary").glob("bottom_up_*.json")))
        print(f"  options       frozen; {nv} vocabulary carried in")
        print(f"  parent root   {parent_root or REPO}")
    if picked:
        print(f"  sample        {len(picked)} runs, stratified by arm")
    print(f"\n  FORKSCOPE_STUDY={root}")


def preflight(root, stage, env):
    """Check every input before spending anything. Fail fast, list everything.

    Written after three runs died 40 minutes in on a missing file, each time on
    a different one. The stages discover their inputs lazily, so a gap surfaces
    only when the stage that needs it runs -- and by then the wall-clock and
    the model calls before it are already spent. Checking up front costs
    milliseconds and reports ALL gaps at once rather than the first.
    """
    problems = []
    if not (root / "study.json").exists():
        problems.append("study.json missing from the replicate root")

    # WHAT THE STAGE NEEDS, NOT WHAT THE FIRST STUDY HAPPENED TO HAVE.
    #
    # These three were unconditional and encoded build A's shape. soccer-C is
    # the first study with a different one, and preflight blocked a distill
    # replicate on outcomes.json (owner decision D3: the extractor does not
    # exist yet, deliberately), on data/raw/inputs.json, and on
    # FORKSCOPE_RAW_HUMAN (owner decision D6: this study is AI-only, there is no
    # human corpus to point at).
    #
    # The distill stage demonstrably needs none of them: run C extracted 207 of
    # 207 runs with no inputs.json and no human corpus. A preflight that
    # refuses a stage over inputs that stage never reads trains people to skip
    # the preflight, which is worse than not having one.
    # NEITHER FILE BLOCKS ANY STAGE. Both used to, and my first correction of
    # that was still wrong: I scoped them to ("vocab", "forks") by guessing,
    # and the forks stage then refused for want of files it never opens.
    #
    # What the chains actually read:
    #   forks   -> induce_forks + merge_forks. Neither touches outcomes.
    #   distill -> distill.py, which is the only reader of inputs.json, and
    #              which extracted 207 of 207 runs for soccer-C without it.
    #   outcomes-consuming scripts (novelty, novelty_curve, shapley_v2,
    #              iteration, audit_shapley) now all skip loudly when the file
    #              is absent, so even a stage that runs them degrades rather
    #              than dies.
    #
    # Reported as notes, because their absence changes what a replicate can
    # answer and the operator should know -- but a preflight that refuses a
    # stage over inputs that stage never reads trains people to skip the
    # preflight, which is worse than not having one.
    notes = []
    if not (root / "data" / "outcomes" / "outcomes.json").exists():
        notes.append("no outcomes.json -- outcome-linked analyses will skip")
    if not (root / "data" / "raw" / "inputs.json").exists():
        notes.append("no data/raw/inputs.json -- only distill.py reads it")
    for d in ("vocabulary", "analysis", "audits", "corpus"):
        if not (root / "data" / d).is_dir():
            problems.append(f"data/{d}/ missing -- run init to create the "
                            f"output tree")
    n_dist = len(list((root / "data" / "distilled").glob("*/record.json"))) \
        if (root / "data" / "distilled").is_dir() else 0
    if stage in ("vocab", "forks") and n_dist == 0:
        problems.append("data/distilled is empty; a vocab replicate needs the "
                        "baseline's stage-1 output copied in")
    if stage == "forks":
        # Exactly one vocabulary, and it must be the parent. More than one
        # means a previous run's fork layer is still here, and `induce_forks`
        # would read it instead of re-deriving -- a replicate that measures
        # nothing and reports perfect agreement.
        vs = sorted((root / "data" / "vocabulary").glob("bottom_up_*.json")) \
            if (root / "data" / "vocabulary").is_dir() else []
        if len(vs) != 1:
            problems.append(
                f"data/vocabulary holds {len(vs)} vocabularies; a fork "
                f"replicate must start from exactly one (the frozen options). "
                f"Re-run init.")
        if not (root / "data" / "analysis").is_dir():
            problems.append("data/analysis missing -- merge_forks reads "
                            "garden_<tag>.json")
    # Which corpora this STUDY declares, and the env var each one names --
    # rather than the two build A had. A study that declares one corpus must
    # not be blocked on the other's variable.
    try:
        sj = json.loads((root / "study.json").read_text(encoding="utf-8"))
        wanted = [c["env"] for c in sj.get("corpora", {}).values() if c.get("env")]
    except Exception:
        wanted = ["FORKSCOPE_RAW_AI"]
    for n in notes:
        print(f"  note: {n}")
    for var in wanted:
        p = env.get(var)
        if not p:
            problems.append(f"{var} unset -- arm recovery falls back to the "
                            f"corpus name and silently produces a phantom arm")
        elif not Path(p).is_dir():
            problems.append(f"{var}={p} is not a directory")
    if problems:
        print("PREFLIGHT FAILED -- nothing spent:\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"  preflight ok  ({n_dist} distilled runs, outcomes present, "
          f"raw corpora reachable)")


def run(root, stage, corpus, workers):
    root = Path(root).resolve()
    if not (root / "manifest.json").exists():
        sys.exit(f"no manifest at {root}; run `init` first")
    man = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    env = dict(os.environ, FORKSCOPE_STUDY=str(root))
    preflight(root, stage, env)
    S = REPO / "scripts"

    if stage == "distill":
        n = man.get("sample_n_requested", 30)
        print(f"distilling a stratified sample of {n} runs into {root}")
        for c in [x.strip() for x in corpus.split(",") if x.strip()]:
            cmd = [sys.executable, "-u", str(S / "distill.py"), "all",
                   "--corpus", c, "--workers", str(workers),
                   "--stratify", str(n)]
            print("  " + " ".join(cmd))
            rc = subprocess.run(cmd, cwd=str(REPO), env=env).returncode
            if rc:
                sys.exit(f"distill failed for corpus {c} (exit {rc})")
        built = sorted(p.name for p in (root / "data" / "distilled").iterdir()
                       if (p / "record.json").exists())
        man["sample_runs"] = built
        man["sample_n"] = len(built)
    elif stage == "forks":
        man["fork_chain"] = _run_forks(root, man, env, S)
    else:
        # TWO PASSES, and the order is forced by the workflow rather than
        # chosen. `build_all --repair` skips the garden stages (6g/6h) because
        # a repaired vocabulary must not have its sibling merge applied twice
        # -- but the repair chain's first step reads garden_<base>.json. So the
        # garden has to exist before the repair pass, and only the non-repair
        # pass builds it.
        #
        # Pass 1 stops after `analyse`: that covers the garden and the stage
        # assignment the repair chain needs, and skips the viewers, which are
        # rebuilt by pass 2 anyway.
        passes = [
            ("base (builds garden + stage labels)",
             ["--skip-distill", "--stop-after", "analyse"]),
            ("repair chain", ["--skip-distill", "--repair"]),
        ]
        rc = 0
        for label, extra in passes:
            argv = ([sys.executable, "-u", str(S / "build_all.py"),
                     "--corpus", corpus, "--workers", str(workers)] + extra)
            print(f"\n=== pass: {label} ===")
            print("  " + " ".join(argv))
            rc = subprocess.run(argv, cwd=str(REPO), env=env).returncode
            if rc:
                break
        if rc:
            # Do not exit before writing the manifest: the cache is populated
            # and its spend must be recorded even on a failed run, or the money
            # spent looks free and the next attempt looks cheaper than it was.
            _finish(root, man)
            sys.exit(f"build_all failed (exit {rc}); cache and manifest kept, "
                     f"so a retry resumes from the cache")

    _finish(root, man)


MAX_FORK_ROUNDS = 4
CONVERGED_AT = 0.02


def _forks_in(root, tag):
    p = root / "data" / "vocabulary" / f"bottom_up_{tag}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    return len({o["fork"] for o in d["options"]})


def _run_forks(root, man, env, S):
    """Re-derive the fork layer over a frozen options layer.

    THE CHAIN, AND WHY IT IS NOT build_all's
    ----------------------------------------
    `build_all --repair` alternates option merging and fork merging, because on
    a fresh build both layers are wrong together. Here the options are fixed by
    construction, so every `merge_options` pass is dropped:

        induce_forks   once   re-derive fork labels from option purpose
        merge_forks    xN     collapse duplicate decision points, to a fixpoint

    That ordering is build_all's own (6-4 then 6-5.i) with the option passes
    removed, not a new design. Dropping them is what makes this replicate
    ISOLATE fork formation -- and it is also what makes it a modified pipeline,
    which any result from it has to say out loud. It answers "given identical
    options, how much do forks vary?" and not "how much does the pipeline vary".

    Cost is roughly a third of a full vocabulary replicate: on build B the two
    surviving stages were $13.83 + $21.81 against $109.60 for the whole repair
    loop, because the dropped `merge_options` pass is the expensive one (655
    opus calls for option granularity).
    """
    tag = man["parent_vocab"]
    if tag and tag.endswith(".json"):
        tag = Path(tag).name[len("bottom_up_"):-len(".json")]
    base = tag
    chain = [{"stage": "parent", "tag": tag, "forks": _forks_in(root, tag)}]
    print(f"\nfork replicate over frozen options: {tag}")
    print(f"  parent has {chain[0]['forks']} decision points\n")

    def step(label, script, argv_tag, out_tag=None):
        for mode in ("run", "apply"):
            argv = [sys.executable, "-u", str(S / script), mode,
                    "--corpus", argv_tag]
            if mode == "apply" and out_tag:
                argv += ["--out-tag", out_tag]
            print(f"  {label} [{mode}]")
            rc = subprocess.run(argv, cwd=str(REPO), env=env).returncode
            if rc:
                _finish(root, man)
                sys.exit(f"{script} {mode} failed (exit {rc}); cache kept")

    step("induce forks", "induce_forks.py", tag)
    tag = tag + ".induced"
    chain.append({"stage": "induce", "tag": tag,
                  "forks": _forks_in(root, tag)})
    print(f"    -> {chain[-1]['forks']} decision points\n")

    for i in range(1, MAX_FORK_ROUNDS + 1):
        before = _forks_in(root, tag)
        out = f"{base}.f{i}"
        step(f"merge forks round {i}", "merge_forks.py", tag, out)
        tag = out
        after = _forks_in(root, tag)
        moved = (before - after) / max(1, before)
        chain.append({"stage": f"merge_forks.{i}", "tag": tag,
                      "forks": after, "moved": round(moved, 4)})
        print(f"    round {i}: {before} -> {after} ({moved:.1%})\n")
        if moved <= CONVERGED_AT:
            break
    else:
        print(f"  NOTE: still merging after {MAX_FORK_ROUNDS} rounds; "
              f"report where this stopped rather than calling it converged.\n")

    argv = [sys.executable, "-u", str(S / "finalize_vocab.py"),
            "--corpus", tag]
    print("  finalize vocabulary")
    if subprocess.run(argv, cwd=str(REPO), env=env).returncode:
        _finish(root, man)
        sys.exit("finalize_vocab failed; cache kept")

    man["final_tag"] = tag
    return chain


def _finish(root, man):
    """Record what the run cost and produced. Called on success AND failure."""
    man["completed"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    man["cache_entries"] = len(list((root / "cache" / "llm_cache").glob("*.json")))
    spend = 0.0
    for f in (root / "cache" / "llm_cache").glob("*.json"):
        try:
            spend += float(json.loads(f.read_text(encoding="utf-8"))
                           .get("cost_usd") or 0)
        except Exception:
            pass
    man["spend_usd"] = round(spend, 2)
    man["vocabulary_files"] = len(
        list((root / "data" / "vocabulary").glob("*.json")))
    (root / "manifest.json").write_text(json.dumps(man, indent=1),
                                        encoding="utf-8")
    print(f"\n  {man['cache_entries']} cache entries, "
          f"${man['spend_usd']:.2f}, "
          f"{man['vocabulary_files']} vocabulary files")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "run"):
        p = sub.add_parser(name)
        p.add_argument("--root", required=True)
        p.add_argument("--stage", choices=["vocab", "distill", "forks"],
                       default="vocab")
        p.add_argument("--from-vocab", dest="from_vocab",
                       help="stage=forks: the vocabulary whose OPTIONS are "
                            "frozen; a tag or a path")
        p.add_argument("--sample", type=int, default=30)
        p.add_argument("--corpus", default="ai,human")
        p.add_argument("--workers", type=int, default=8)
        p.add_argument("--runs-from", dest="runs_from",
                       help="restrict to runs present in this distilled tree")
        p.add_argument("--parent-root", dest="parent_root",
                       help="stage=forks: build whose distilled/analysis are "
                            "copied in (default: this repo)")
        p.add_argument("--distilled-from", dest="distilled_from",
                       help="copy stage-1 output from here instead of the "
                            "baseline")
    a = ap.parse_args()
    if a.cmd == "init":
        if a.stage == "forks" and not a.from_vocab:
            sys.exit("--stage forks needs --from-vocab (the frozen options)")
        init(a.root, a.stage, a.sample, a.runs_from, a.distilled_from,
             a.from_vocab, a.parent_root)
    else:
        run(a.root, a.stage, a.corpus, a.workers)


if __name__ == "__main__":
    main()
