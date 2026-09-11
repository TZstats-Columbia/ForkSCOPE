#!/usr/bin/env python3
"""Does every script import, and do its paths point inside the package?

Called by `_selfcheck.py`. Prints one line per problem and nothing when clean.

WHY IT EXISTS

`audit_granularity.py` and `audit_lineage.py` shipped in the package,
documented in WORKFLOW, listed in the audits README — and pointing at
`soccer/v2/clusters`, the working tree's layout, which does not exist here.
Both failed the moment they were first run against the package. They had never
been run against it, and nothing checked that they could be.

Documentation cannot catch this: the scripts were documented. A file-presence
check cannot catch it: the files were present. The only thing that catches a
path constant aimed at the wrong tree is resolving it.

Runs in a subprocess because it imports 40-odd modules, and an import error in
one of them should be a reported failure rather than a crash in the checker.
"""
import glob
import importlib
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402

# _selfcheck imports this one; a corpus root legitimately sits outside the
# package and is declared as such in study.json.
SKIP_MODULES = {"_selfcheck", "_importcheck"}
SKIP_ATTRS = {"RAW_AI", "RAW_HUMAN", "ARC"}


def inside(p):
    for root in (P.CODE_ROOT, P.STUDY_ROOT):
        try:
            p.resolve().relative_to(root)
            return True
        except ValueError:
            continue
    return False


def unreachable(p):
    """A path nothing of which exists — not the file, not even its directory.

    `inside()` alone missed the bug this module was written for.
    `soccer/v2/clusters` IS inside the package root; it simply is not there.
    Testing containment and calling that a check was the same mistake as the
    2.7% claim: a measure that cannot see the failure it is used to rule out.

    An output that has not been written yet is normal and its parent exists, so
    requiring the path itself to exist would fire constantly. Requiring the
    *parent* to exist does not: a constant aimed at another tree has no part of
    itself on disk.
    """
    p = p.resolve()
    return not p.exists() and not p.parent.exists()


def main():
    bad = []
    for f in sorted(glob.glob(str(P.SCRIPTS / "*.py"))):
        name = os.path.basename(f)[:-3]
        if name in SKIP_MODULES:
            continue
        try:
            m = importlib.import_module(name)
        except Exception as e:                                  # noqa: BLE001
            bad.append(f"{name}: import failed — {type(e).__name__}: {e}")
            continue
        for k, v in vars(m).items():
            if k.startswith("_") or k in SKIP_ATTRS:
                continue
            if not isinstance(v, pathlib.Path):
                continue
            if not inside(v):
                bad.append(f"{name}.{k} resolves outside the package: {v}")
            elif unreachable(v):
                bad.append(f"{name}.{k} points at nothing on disk: {v}")
    print("\n".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
