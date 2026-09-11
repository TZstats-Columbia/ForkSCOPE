#!/usr/bin/env python3
"""Lock a layer once a human has settled it, and notice when it comes unstuck.

WHY A LOCK IS A HASH AND NOT A NOTE
-----------------------------------
Charting has checkpoints a person has to clear: distillation is good enough to
build on, the vocabulary is good enough to report from. We ran both informally
-- "determine if distillation needs a rerun or we can lock it in and focus on
the garden work" -- and nothing in the tree recorded either answer.

A note recording that answer would not have helped, because the failure it must
prevent is silent. Re-run distillation after settling it, and every charting
number is now built on an extraction nobody reviewed. Nothing errors. The
figures render. So a lock stores a CONTENT HASH of the layer it settles, and
goes stale by itself when the layer moves.

WHAT A LOCK IS NOT
------------------
Not a gate that blocks a build. Nothing here refuses to run; `verify` reports
and returns a non-zero exit for a caller that wants to care. Blocking would
make the honest response to a stale lock -- re-open the question -- more
expensive than the dishonest one, which is to avoid re-running the thing that
would break it.

Not a quality claim either. A lock records that a person looked at the evidence
and decided; it says nothing about whether they were right. The evidence is
stored with it so the decision can be revisited on its merits.

Usage:
    python3 scripts/settle.py status
    python3 scripts/settle.py lock distill --decision "..." [--evidence f.json]
    python3 scripts/settle.py verify           # exit 1 if any lock is stale
    python3 scripts/settle.py unlock chart --why "..."
"""
import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                  # noqa: E402

LOCKS = P.ROOT / "locks"

# What each layer IS, for hashing. Deliberately the artifacts a downstream
# stage reads -- not everything a stage wrote. Hashing incidental outputs would
# make a lock go stale on a re-render that changed nothing anyone consumes.
LAYERS = {
    "distill": {
        "what": "per-run decision records and their spans",
        "globs": ["data/distilled/*/record.json",
                  "data/distilled/*/code_spans.json",
                  "data/distilled/*/prose_spans.json"],
    },
    "chart": {
        "what": "the headline vocabulary",
        "globs": [None],          # resolved from final_tag at run time
    },
}


def layer_files(layer):
    if layer == "chart":
        p = P.VOCAB / f"bottom_up_{P.FINAL_TAG}.json"
        return [p] if p.exists() else []
    out = []
    for g in LAYERS[layer]["globs"]:
        out += sorted(P.ROOT.glob(g))
    return sorted(out)


def digest(layer):
    """sha256 over (relative path, file digest) pairs, sorted.

    Paths are included so that deleting a run changes the hash. A digest over
    concatenated contents alone would not notice a removal that happened to
    leave the remaining bytes identical.
    """
    files = layer_files(layer)
    h = hashlib.sha256()
    for f in files:
        rel = f.relative_to(P.ROOT).as_posix()
        h.update(rel.encode())
        h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest(), len(files)


def lock_path(layer):
    return LOCKS / f"{layer}.lock.json"


def read_lock(layer):
    p = lock_path(layer)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                              # noqa: BLE001
        return None


def state(layer):
    lk = read_lock(layer)
    cur, n = digest(layer)
    if not n:
        return "absent", lk, cur, n
    if not lk:
        return "unlocked", lk, cur, n
    return ("locked" if lk.get("content_sha256") == cur else "STALE",
            lk, cur, n)


def cmd_status(a):
    print(f"study {P.STUDY_NAME}   tag {P.FINAL_TAG}\n")
    any_stale = False
    for layer in LAYERS:
        st, lk, cur, n = state(layer)
        any_stale |= st == "STALE"
        print(f"  {layer:<9} {st:<9} {n:>4} files   {LAYERS[layer]['what']}")
        if lk:
            print(f"            settled {lk.get('locked_at', '?')}"
                  f" — {str(lk.get('decision', ''))[:60]}")
        if st == "STALE":
            print(f"            locked  {lk['content_sha256'][:16]}")
            print(f"            now     {cur[:16]}")
            print(f"            the layer moved since it was settled; the "
                  f"question is re-open")
    if any_stale:
        print("\n  A stale lock is not an error. It means work downstream of "
              "it\n  is resting on something nobody has reviewed in its "
              "current form.")


def cmd_lock(a):
    layer = a.layer
    st, lk, cur, n = state(layer)
    if st == "absent":
        sys.exit(f"nothing to settle: no files for layer {layer!r}")
    if st == "locked" and not a.force:
        print(f"  {layer} is already settled and unchanged since "
              f"{lk.get('locked_at')}")
        return
    if not a.decision:
        sys.exit("--decision is required: what did the human decide, and why")

    ev = {}
    for f in a.evidence or []:
        p = Path(f)
        if p.exists():
            try:
                ev[p.name] = json.loads(p.read_text(encoding="utf-8"))
            except Exception:                                      # noqa: BLE001
                ev[p.name] = "unparsed"
        else:
            print(f"  warning: evidence file not found: {f}")

    LOCKS.mkdir(parents=True, exist_ok=True)
    rec = {
        "layer": layer,
        "what": LAYERS[layer]["what"],
        "locked_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "content_sha256": cur,
        "n_files": n,
        "study": P.STUDY_NAME,
        "final_tag": P.FINAL_TAG if layer == "chart" else None,
        "decision": a.decision,
        "settled_by": a.by or "unrecorded",
        "git_sha": subprocess.run(["git", "rev-parse", "HEAD"],
                                  capture_output=True, text=True,
                                  cwd=str(P.CODE_ROOT)).stdout.strip() or None,
        "evidence": ev,
        "note": ("A lock records that a person reviewed the evidence and "
                 "decided. It is not a claim that the decision was right."),
    }
    lock_path(layer).write_text(json.dumps(rec, indent=1, ensure_ascii=False),
                                encoding="utf-8")
    print(f"  {layer} settled — {n} files, {cur[:16]}")
    print(f"  wrote {lock_path(layer)}")
    if not ev:
        print("  NOTE: no evidence attached. A lock with no evidence cannot be "
              "revisited on its merits.")


def cmd_unlock(a):
    p = lock_path(a.layer)
    if not p.exists():
        sys.exit(f"{a.layer} is not locked")
    if not a.why:
        sys.exit("--why is required: re-opening a settled question is a "
                 "decision too")
    old = read_lock(a.layer) or {}
    hist = LOCKS / f"{a.layer}.unlocked.jsonl"
    with open(hist, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"unlocked_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                             "why": a.why, "was": old}, ensure_ascii=False)
                 + "\n")
    p.unlink()
    print(f"  {a.layer} re-opened; the previous lock is kept in {hist.name}")


def cmd_verify(a):
    bad = []
    for layer in LAYERS:
        st, lk, cur, n = state(layer)
        mark = {"locked": "ok", "STALE": "STALE", "unlocked": "unlocked",
                "absent": "absent"}[st]
        print(f"  {layer:<9} {mark}")
        if st == "STALE":
            bad.append(layer)
    if bad:
        print(f"\n  stale: {', '.join(bad)} — settled, then changed")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("verify")
    p = sub.add_parser("lock")
    p.add_argument("layer", choices=sorted(LAYERS))
    p.add_argument("--decision", required=False)
    p.add_argument("--by")
    p.add_argument("--evidence", action="append")
    p.add_argument("--force", action="store_true")
    u = sub.add_parser("unlock")
    u.add_argument("layer", choices=sorted(LAYERS))
    u.add_argument("--why")
    a = ap.parse_args()
    {"status": cmd_status, "lock": cmd_lock, "unlock": cmd_unlock,
     "verify": cmd_verify}[a.cmd](a)


if __name__ == "__main__":
    main()
