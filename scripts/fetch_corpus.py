#!/usr/bin/env python3
"""Acquire the two source corpora, and verify they are the ones we used.

The corpora are third-party and are NOT redistributed with this repository:
the AI corpus is published by its authors under their own terms, and the human
corpus is participant-supplied material from a human-subjects study, where
republishing is a consent and licensing decision for the original authors
rather than a default of this pipeline. So this script fetches them from source
instead of shipping them.

WHY A CHECKSUM MANIFEST AND NOT JUST A URL
------------------------------------------
Naming a source and a commit says where the bytes came from. It does not say
that the bytes you have are the bytes we read. Upstream can be re-tagged, a
Git-LFS pull can silently leave pointer files in place of content (it did here
once), and a partial download looks exactly like a complete one to every stage
downstream. `checksum` records SHA-256 for every artifact the pipeline actually
reads; `verify` re-checks them. That turns "we used the corpus" into a claim
someone else can falsify.

WHAT IS AUTOMATED AND WHAT IS NOT
---------------------------------
  ai      fully automated. Pinned commit, sparse checkout scoped to the
          sonnet-4-5 sample_soccer workspaces, LFS pulled for that scope only.
  soccer  fully automated. The dataset CSV from the OSF project.
  human   NOT automated, deliberately. The 31 teams' scripts, surveys and
          reports are participant documents; obtaining them is a decision a
          person makes against the original study's terms, not something a
          script should do silently on their behalf. This script tells you what
          is expected, checks what is present, and verifies what you supply.

Refusing to automate that last step is the point, not a gap.

THIS FETCHER IS STUDY-SPECIFIC AND THE ONLY SCRIPT THAT IS
----------------------------------------------------------
Everything else in `scripts/` reads its corpus location from `study.json`, so a
second study reuses the instrument unchanged. This file does not: the repository
URL, the pinned commit, the sparse-checkout scope and the OSF node below are
constants for THIS study's corpora and cannot be parameterised into something
general, because acquiring a corpus is not a general operation. One corpus is a
pinned git repo with LFS, another is an OSF archive, a third will be an
institutional download behind a login.

So a second study does not configure this script — it **writes its own**, and
that is a normal amount of work rather than a defect in the design. What the
replacement must produce is a contract, not an implementation:
`templates/fetch_corpus.md` states it. In short, a directory whose layout
matches the `glob` and `artifacts` in your `study.json`, plus a checksum
manifest, so that `distill.py` finds runs and someone else can falsify that they
have the same bytes.

Do not edit the constants below to point at a different corpus. They are the
provenance record for the soccer study, and `data/raw/MANIFEST.md` cites them.

Usage:
    python3 scripts/fetch_corpus.py status                    # what's present
    python3 scripts/fetch_corpus.py fetch  --dest ../corpus   # get ai + soccer
    python3 scripts/fetch_corpus.py checksum --dest ../corpus # write manifest
    python3 scripts/fetch_corpus.py verify --dest ../corpus   # check manifest
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

# ---- pinned upstream sources ------------------------------------------------
# The commit is the provenance claim. Changing it means the corpus changed, and
# every cached model response keyed on the old content is no longer describing
# the same material.
AFP_REPO = "https://github.com/amazon-science/agentic-forking-path.git"
AFP_COMMIT = "d489f03b143fcaa9befb8cc443594ff63ec61eaa"
AFP_MODEL_DIR = "bedrock_us.anthropic.claude-sonnet-4-5-20250929-v1_0"
AFP_SCOPE = f"experiment_data/workspaces/*/{AFP_MODEL_DIR}/sample_soccer/*"

# OSF project for Silberzahn et al., "Many analysts, one data set".
OSF_NODE = "c9mkx"
OSF_API = f"https://api.osf.io/v2/nodes/{OSF_NODE}/files/osfstorage/"
# Name inside the OSF archive, and the name it is stored under locally. The
# rename is not cosmetic: `soccer_raw.csv` sits beside a derived `soccer.csv`,
# and conflating the two would feed a cleaned file to a stage that documents
# itself as reading the raw one.
SOCCER_CSV = "CrowdstormingDataJuly1st.csv"
SOCCER_LOCAL = "soccer_raw.csv"

MANIFEST = REPO / "data" / "raw" / "CHECKSUMS.txt"

# Artifacts the pipeline actually reads. Checksumming everything else would
# make the manifest churn on files no result depends on.
AI_ARTIFACTS = ("final_analysis.py", "mirrored_report.txt", "transcript.json")
HUMAN_ARTIFACTS = ("script.txt", "survey.txt", "report.txt")


def sh(cmd, cwd=None, check=True):
    print("    $ " + " ".join(cmd))
    r = subprocess.run(cmd, cwd=cwd, text=True)
    if check and r.returncode:
        sys.exit(f"failed: {' '.join(cmd)}")
    return r.returncode


def sha256(path, buf=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


# ---- fetch ------------------------------------------------------------------
def fetch_ai(dest):
    """Sparse, pinned, LFS-scoped clone of the AI corpus.

    Full clone is ~4,196 experiment runs across every model; we read 207. A
    sparse checkout scoped to the sonnet-4-5 sample_soccer paths is the
    difference between a few hundred MB and many GB, and it makes the scope of
    what we read explicit rather than implicit in a glob applied later.
    """
    root = Path(dest) / "afp"
    if (root / ".git").exists():
        print(f"  afp: already present at {root}")
    else:
        root.parent.mkdir(parents=True, exist_ok=True)
        sh(["git", "clone", "--filter=blob:none", "--no-checkout",
            AFP_REPO, str(root)])
        sh(["git", "sparse-checkout", "init", "--cone"], cwd=str(root))
        sh(["git", "sparse-checkout", "set", "experiment_data/workspaces"],
           cwd=str(root))
    sh(["git", "checkout", AFP_COMMIT], cwd=str(root))

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root),
                          capture_output=True, text=True).stdout.strip()
    if head != AFP_COMMIT:
        sys.exit(f"  afp: HEAD is {head}, expected {AFP_COMMIT}")
    print(f"  afp: at pinned commit {AFP_COMMIT[:12]}")

    # LFS content, scoped. Without this the *.txt/*.json artifacts are pointer
    # files: present, small, parseable as text, and completely wrong. This
    # exact failure occurred on the first build.
    sh(["git", "lfs", "pull", "--include", AFP_SCOPE], cwd=str(root),
       check=False)
    check_lfs_pointers(root)


def check_lfs_pointers(root):
    """A pointer file is ~130 bytes starting with a known header.

    Worth checking explicitly: an unfetched pointer is valid UTF-8 and does not
    raise anywhere in the pipeline. It simply makes a run look like it produced
    a 130-byte report, which the prose filter then silently drops.
    """
    bad = []
    for p in root.glob(f"experiment_data/workspaces/*/{AFP_MODEL_DIR}"
                       f"/sample_soccer/*/*"):
        if p.is_file() and p.stat().st_size < 200:
            try:
                if p.open("rb").read(40).startswith(b"version https://git-lfs"):
                    bad.append(p)
            except OSError:
                pass
    if bad:
        print(f"  WARNING: {len(bad)} unfetched Git-LFS pointer files remain.")
        print(f"           These parse as text and will silently corrupt "
              f"stage 1.")
        print(f"           Re-run: git lfs pull --include '{AFP_SCOPE}'")
    else:
        print("  afp: no unfetched LFS pointers")


def fetch_soccer(dest):
    """The shared dataset every analysis was given."""
    import urllib.request
    out = Path(dest) / "osf"
    out.mkdir(parents=True, exist_ok=True)
    zp = out / "crowd.zip"
    if not zp.exists():
        url = f"https://osf.io/{OSF_NODE}/files/osfstorage/"
        print(f"  soccer: crowd.zip not present.")
        print(f"          Download {SOCCER_CSV} from {url}")
        print(f"          and place the archive at {zp}")
        return
    with zipfile.ZipFile(zp) as z:
        names = [n for n in z.namelist() if n.endswith(SOCCER_CSV)
                 and not n.startswith("__MACOSX")]
        if not names:
            sys.exit(f"  soccer: {SOCCER_CSV} not found inside {zp}")
        tgt = Path(dest) / "data" / "soccer"
        tgt.mkdir(parents=True, exist_ok=True)
        if not (tgt / SOCCER_LOCAL).exists():
            with z.open(names[0]) as src, open(tgt / SOCCER_LOCAL, "wb") as dst:
                dst.write(src.read())
        print(f"  soccer: {SOCCER_LOCAL} at {tgt}")


def human_status(dest):
    """Report, do not fetch. See the module docstring for why."""
    root = Path(dest) / "human_corpus"
    teams = sorted(root.glob("team-*")) if root.exists() else []
    with_script = [t for t in teams if (t / "script.txt").exists()
                   and (t / "script.txt").stat().st_size]
    print(f"  human: {len(teams)} team directories, "
          f"{len(with_script)} with a non-empty script.txt")
    if not teams:
        print(f"         Expected at {root}/team-NN/"
              f"{{script.txt,survey.txt,report.txt}}")
        print(f"         Source: OSF node {OSF_NODE} (Silberzahn et al.).")
        print(f"         NOT fetched automatically: these are participant "
              f"documents from a")
        print(f"         human-subjects study. Obtaining them is a decision "
              f"against the")
        print(f"         original study's terms, not a step a script should "
              f"take for you.")
    elif len(with_script) != 19:
        print(f"         NOTE: the published analysis rests on 19 teams with "
              f"scripts; you have {len(with_script)}.")
    return len(teams), len(with_script)


# ---- checksum / verify ------------------------------------------------------
def iter_artifacts(dest):
    dest = Path(dest)
    ai_glob = (f"afp/experiment_data/workspaces/*/{AFP_MODEL_DIR}"
               f"/sample_soccer/*")
    for d in sorted(dest.glob(ai_glob)):
        for name in AI_ARTIFACTS:
            p = d / name
            if p.exists():
                yield p.relative_to(dest), p
    for d in sorted((dest / "human_corpus").glob("team-*")):
        for name in HUMAN_ARTIFACTS:
            p = d / name
            if p.exists():
                yield p.relative_to(dest), p
    p = dest / "data" / "soccer" / SOCCER_LOCAL
    if p.exists():
        yield p.relative_to(dest), p


def do_checksum(dest):
    rows = []
    for rel, p in iter_artifacts(dest):
        rows.append((sha256(p), p.stat().st_size, rel.as_posix()))
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"# SHA-256 of every raw artifact the pipeline reads.\n")
        fh.write(f"# afp pinned at {AFP_COMMIT}\n")
        fh.write(f"# osf node {OSF_NODE}\n")
        fh.write(f"# {len(rows)} artifacts\n")
        fh.write(f"# regenerate: python3 scripts/fetch_corpus.py checksum "
                 f"--dest <corpus>\n")
        for h, sz, rel in rows:
            fh.write(f"{h}  {sz:>10}  {rel}\n")
    print(f"  wrote {MANIFEST} ({len(rows)} artifacts)")


def do_verify(dest):
    if not MANIFEST.exists():
        sys.exit(f"no manifest at {MANIFEST}; run `checksum` first")
    expect = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        h, sz, rel = line.split(None, 2)
        expect[rel] = (h, int(sz))
    dest = Path(dest)
    missing, bad, ok = [], [], 0
    for rel, (h, sz) in expect.items():
        p = dest / rel
        if not p.exists():
            missing.append(rel)
        elif sha256(p) != h:
            bad.append(rel)
        else:
            ok += 1
    extra = [rel.as_posix() for rel, _ in iter_artifacts(dest)
             if rel.as_posix() not in expect]
    print(f"  verified {ok}/{len(expect)} artifacts")
    for label, rows in (("MISSING", missing), ("CHANGED", bad),
                        ("UNTRACKED", extra)):
        if rows:
            print(f"  {label}: {len(rows)}")
            for r in rows[:5]:
                print(f"    {r}")
            if len(rows) > 5:
                print(f"    ... and {len(rows) - 5} more")
    return not (missing or bad)


def do_status(dest):
    dest = Path(dest)
    print(f"corpus root: {dest}"
          f"{'' if dest.exists() else '   (does not exist)'}")
    afp = dest / "afp"
    if (afp / ".git").exists():
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(afp),
                              capture_output=True, text=True).stdout.strip()
        mark = "pinned" if head == AFP_COMMIT else f"NOT PINNED (want {AFP_COMMIT[:12]})"
        runs = len(list(afp.glob(f"experiment_data/workspaces/*/{AFP_MODEL_DIR}"
                                 f"/sample_soccer/*")))
        print(f"  ai:     {runs} runs, HEAD {head[:12]} [{mark}]")
    else:
        print(f"  ai:     not present at {afp}")
    human_status(dest)
    csv = dest / "data" / "soccer" / SOCCER_LOCAL
    print(f"  soccer: {'present' if csv.exists() else 'not present'}")
    print(f"\n  manifest: {'present' if MANIFEST.exists() else 'not written'}")
    print(f"\n  to use:  export FORKSCOPE_RAW_AI={dest}/afp")
    print(f"           export FORKSCOPE_RAW_HUMAN={dest}/human_corpus")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["status", "fetch", "checksum", "verify"])
    ap.add_argument("--dest", default=os.environ.get("FORKSCOPE_CORPUS",
                                                     str(REPO.parent.parent / "corpus")),
                    help="corpus root, OUTSIDE this repository")
    a = ap.parse_args()
    dest = Path(a.dest).resolve()

    if a.cmd == "status":
        do_status(dest)
    elif a.cmd == "fetch":
        print(f"fetching into {dest}")
        fetch_ai(dest)
        fetch_soccer(dest)
        human_status(dest)
        print("\n  then: python3 scripts/fetch_corpus.py verify --dest "
              f"{dest}")
    elif a.cmd == "checksum":
        do_checksum(dest)
    else:
        sys.exit(0 if do_verify(dest) else 1)


if __name__ == "__main__":
    main()
