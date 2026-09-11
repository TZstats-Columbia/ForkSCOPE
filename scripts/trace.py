#!/usr/bin/env python3
"""Walk any object in the garden back to the source lines it came from.

Every number this project reports rests on a chain:

    fork  ->  options  ->  decisions  ->  run + line  ->  source

The chain is present in the data and, until now, nothing traversed it. A
reader who doubted a fork had to open four files by hand and join them
mentally. That is the difference between evidence that exists and evidence
that can be reviewed, so this is a tool rather than a document.

It is deliberately a script and not an agent. A trace must return the same
chain every time it is asked, or it cannot be cited.

HOW FAR IT GETS OFFLINE
The package carries structure, not source text: a decision knows its run and
line and the operation it performs, but the original script is third-party and
is not vendored (see data/raw/MANIFEST.md). So four of the five rungs resolve
with no external data, and the fifth -- the literal lines -- resolves only when
a raw corpus is mounted:

    export FORKSCOPE_RAW_AI=/path/to/agentic-forking-path

Without it you still get the operation description the extraction recorded,
which is what most review questions actually need.

HANDLES
Exhibits cite handles so a claim in an audit report can be walked here
directly. Handles are content-derived and stable for a given vocabulary:

    fork:a1b2c3d4          a decision point
    opt:e5f6a7b8           one option at one decision point
    dec:<run>@<line>       one extracted decision (stable across vocabularies,
                           because it is anchored in the source, not a label)
    run:<run_id>           one analysis

USAGE
    python3 scripts/trace.py fork "discretiz"
    python3 scripts/trace.py option "average the two raters"
    python3 scripts/trace.py run 2025-11-29T01-11-34+0000
    python3 scripts/trace.py resolve fork:a1b2c3d4
    python3 scripts/trace.py fork "discretiz" --json --limit 5

A partial string is matched as a substring, case-insensitively. If it is
ambiguous the candidates are listed rather than one being guessed.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402


def _h(*parts):
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:8]


def h_fork(fork):
    return f"fork:{_h(fork)}"


def h_option(fork, option):
    return f"opt:{_h(fork, option)}"


def h_decision(run, line):
    return f"dec:{run}@{line}"


def h_run(run):
    return f"run:{run}"


def raw_labels(o):
    """The original corpus labels folded into an option.

    Normalised on read because the field is written as a bare string by the
    rename step and as a list by the fold step. A consumer that forgets that
    gets `sorted("some label")` -- a list of characters -- and cheerfully
    reports a 27-label merge for an option nobody merged. Producers now write
    a list; this keeps the vocabularies already on disk readable.
    """
    v = o.get("option_raw")
    if not v:
        return []
    return sorted(v) if isinstance(v, list) else [v]


class Tracer:
    """Resolves handles and labels to their evidence chain.

    Loads the vocabulary once; every lookup is in-memory. Import this in an
    audit or an agent rather than shelling out per object.
    """

    def __init__(self, tag=None):
        self.tag = tag or P.FINAL_TAG
        self.vocab = json.loads(
            P.vocab_file(self.tag).read_text(encoding="utf-8"))
        self.decisions = self.vocab["decisions"]
        self.options = self.vocab["options"]
        gf = P.garden_file(self.tag)
        self.garden = (json.loads(gf.read_text(encoding="utf-8"))
                       if gf.exists() else {})
        self.stage = {n["fork"]: n.get("stage")
                      for n in self.garden.get("nodes_detail", [])}
        self._by_fork = {}
        for o in self.options:
            self._by_fork.setdefault(o["fork"], []).append(o)
        self._fh = {h_fork(f): f for f in self._by_fork}
        self._oh = {h_option(o["fork"], o["option"]): o for o in self.options}
        self._spans = {}

    # -- lookup ------------------------------------------------------------

    def forks(self, needle):
        """Forks matching a handle, an exact label, or a substring."""
        if needle in self._fh:
            return [self._fh[needle]]
        if needle in self._by_fork:
            return [needle]
        n = needle.lower()
        return sorted(f for f in self._by_fork if n in f.lower())

    def options_matching(self, needle, fork=None):
        if needle in self._oh:
            return [self._oh[needle]]
        n = needle.lower()
        return [o for o in self.options
                if n in o["option"].lower()
                and (fork is None or fork.lower() in o["fork"].lower())]

    # -- the chain ---------------------------------------------------------

    def fork(self, name, limit=None):
        """A decision point, its options, and where each was seen."""
        if name not in self._by_fork:
            near = self.forks(name[:28])
            raise KeyError(
                f"no fork {name!r} in vocabulary {self.tag!r}. Labels are "
                f"rewritten by each merge stage, so one carried over from "
                f"another vocabulary will not be found here."
                + (f" Did you mean: {near[:3]}" if near else
                   " Search with .forks(<substring>)."))
        opts = sorted(self._by_fork[name], key=lambda o: -o["n"])
        runs = sorted({r for o in opts for r in o.get("runs", [])})
        return {
            "handle": h_fork(name), "fork": name,
            "stage": self.stage.get(name),
            "n_options": len(opts), "n_runs": len(runs),
            "modal_share": round(opts[0]["n"] / max(1, sum(o["n"] for o in opts)), 3),
            "options": [self._option_row(o) for o in opts[:limit]],
            "elided_options": max(0, len(opts) - (limit or len(opts))),
        }

    def _option_row(self, o):
        return {
            "handle": h_option(o["fork"], o["option"]),
            "option": o["option"], "n": o["n"],
            "arms": o.get("arms"), "corpora": o.get("corpora"),
            "n_raw_labels": len(raw_labels(o)),
        }

    def option(self, o, limit=8, source=False):
        """One option, down to the individual decisions that compose it."""
        decs = []
        for i in o.get("members", []):
            if i < len(self.decisions):
                decs.append(self.decision(self.decisions[i], source=source))
        decs.sort(key=lambda d: (d["run"], d["line"]))
        return {
            "handle": h_option(o["fork"], o["option"]),
            "fork": o["fork"], "fork_handle": h_fork(o["fork"]),
            "option": o["option"], "n": o["n"],
            "raw_labels": raw_labels(o),
            "decisions": decs[:limit],
            "elided_decisions": max(0, len(decs) - limit),
        }

    def decision(self, d, source=False):
        """One extracted decision: what it did, where, and optionally the code."""
        run, line = d["run"], d["line"]
        row = {"handle": h_decision(run, line), "run": run, "arm": d.get("arm"),
               "line": line, "text": d.get("text", "")}
        sp = self._span(run, line)
        if sp:
            row["operation"] = sp.get("operation")
            row["targets"] = sp.get("targets")
            row["confidence"] = sp.get("confidence")
            row["lines"] = sp.get("lines")
        if source:
            row["source"] = self.source(run, sp.get("lines") if sp
                                        else [[line, line]])
        return row

    def _span(self, run, line):
        """The code span covering a line, from the run's own segmentation."""
        if run not in self._spans:
            f = P.DISTILLED / run / "code_spans.json"
            try:
                self._spans[run] = json.loads(
                    f.read_text(encoding="utf-8")).get("spans", [])
            except OSError:
                self._spans[run] = []
        for s in self._spans[run]:
            if s.get("kind") != "decision":
                continue
            for a, b in s.get("lines", []):
                if a <= line <= b:
                    return s
        return None

    def run(self, run_id):
        f = P.DISTILLED / run_id / "record.json"
        if not f.exists():
            return {"handle": h_run(run_id), "run": run_id,
                    "error": "no distilled record"}
        rec = json.loads(f.read_text(encoding="utf-8"))
        mine = [(o, self.decisions[i]) for o in self.options
                for i in o.get("members", [])
                if i < len(self.decisions)
                and self.decisions[i]["run"] == run_id]
        mine.sort(key=lambda p: p[1]["line"])
        return {
            "handle": h_run(run_id), "run": run_id,
            "corpus": rec.get("corpus"), "arm": rec.get("arm"),
            "artifacts": rec.get("artifacts"),
            "counts": rec.get("counts"),
            "n_silent": len(rec.get("silent_decisions", []) or []),
            "n_misaligned": len(rec.get("misalignments", []) or []),
            "path": [{"line": d["line"],
                      "fork": o["fork"], "fork_handle": h_fork(o["fork"]),
                      "option": o["option"],
                      "stage": self.stage.get(o["fork"])}
                     for o, d in mine],
        }

    # -- the last rung -----------------------------------------------------

    def source(self, run, ranges):
        """The literal lines, if a raw corpus is mounted. Never invented."""
        p = self._source_file(run)
        if p is None:
            return {"available": False,
                    "why": "raw corpus not mounted; set FORKSCOPE_RAW_AI "
                           "(see data/raw/MANIFEST.md)"}
        try:
            lines = Path(p).read_text(encoding="utf-8",
                                      errors="replace").splitlines()
        except OSError as e:
            return {"available": False, "why": f"{type(e).__name__}: {e}"}
        out = []
        for a, b in ranges or []:
            for n in range(a, min(b, len(lines)) + 1):
                out.append({"line": n, "text": lines[n - 1]})
        return {"available": True, "file": str(p), "lines": out}

    def _source_file(self, run):
        f = P.DISTILLED / run / "record.json"
        if not f.exists():
            return None
        art = json.loads(f.read_text(encoding="utf-8")).get("artifacts", {})
        name = art.get("code")
        if not name:
            return None
        root = os.environ.get("FORKSCOPE_RAW_AI")
        if not root or not Path(root).exists():
            return None
        for pat in (f"**/{run}/**/{name}", f"**/{run}/{name}", f"**/{name}"):
            hits = glob.glob(os.path.join(root, pat), recursive=True)
            if hits:
                return sorted(hits)[0]
        return None

    def resolve(self, handle, **kw):
        """Dispatch any handle to its chain."""
        if handle.startswith("fork:"):
            f = self._fh.get(handle)
            return self.fork(f, **kw) if f else {"error": f"unknown {handle}"}
        if handle.startswith("opt:"):
            o = self._oh.get(handle)
            return self.option(o, **kw) if o else {"error": f"unknown {handle}"}
        if handle.startswith("dec:"):
            m = re.match(r"dec:(.+)@(\d+)$", handle)
            if not m:
                return {"error": f"malformed {handle}"}
            run, line = m.group(1), int(m.group(2))
            for d in self.decisions:
                if d["run"] == run and d["line"] == line:
                    return self.decision(d, **kw)
            return {"error": f"unknown {handle}"}
        if handle.startswith("run:"):
            return self.run(handle[4:])
        return {"error": f"unrecognized handle {handle!r}"}


# -- rendering -------------------------------------------------------------

def _wrap(s, width, indent):
    out, line = [], ""
    for w in str(s).split():
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    out.append(line)
    return f"\n{' ' * indent}".join(out)


def show_fork(t, name, limit, source):
    d = t.fork(name, limit=limit)
    print(f"{d['handle']}  [{d['stage']}]")
    print(f"  {_wrap(d['fork'], 72, 2)}")
    print(f"  {d['n_runs']} runs · {d['n_options']} options · "
          f"modal share {d['modal_share']}")
    print()
    for o in d["options"]:
        raw = (f"  ({o['n_raw_labels']} raw labels merged)"
               if o["n_raw_labels"] > 1 else "")
        print(f"  {o['n']:>3} runs  {o['handle']}{raw}")
        print(f"           {_wrap(o['option'], 62, 11)}")
    if d["elided_options"]:
        print(f"\n  ... {d['elided_options']} further options not shown "
              f"(--limit)")
    if source or limit:
        first = t._by_fork[name][0]
        print(f"\n  deepest rung for {h_option(name, first['option'])}:")
        oo = t.option(first, limit=3, source=source)
        for dd in oo["decisions"]:
            print(f"    {dd['handle']}")
            print(f"      {_wrap(dd.get('operation') or dd['text'], 66, 6)}")
            src = dd.get("source") or {}
            if src.get("available"):
                for ln in src["lines"][:6]:
                    print(f"      {ln['line']:>4} | {ln['text'][:66]}")
            elif source:
                print(f"      source: {src.get('why')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("kind", choices=["fork", "option", "run", "decision",
                                     "resolve"])
    ap.add_argument("needle", nargs="+")
    ap.add_argument("--corpus", default=None)
    ap.add_argument("--fork", default=None, help="narrow an option lookup")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--source", action="store_true",
                    help="include literal source lines (needs a raw corpus)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t = Tracer(a.corpus)
    needle = " ".join(a.needle)

    if a.kind == "resolve":
        out = t.resolve(needle, **({"source": a.source}
                                   if needle.startswith(("opt:", "dec:"))
                                   else {}))
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 1 if "error" in out else 0

    if a.kind == "run":
        out = t.run(needle)
        if a.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        print(f"{out['handle']}  {out.get('corpus')} / {out.get('arm')}")
        print(f"  artifacts {out.get('artifacts')}")
        print(f"  {len(out.get('path', []))} decisions on the vocabulary · "
              f"{out.get('n_silent')} silent · "
              f"{out.get('n_misaligned')} misaligned\n")
        for s in out.get("path", []):
            print(f"  line {s['line']:>4}  [{(s['stage'] or '?')[:14]:<14}] "
                  f"{s['option'][:52]}")
        return 0

    if a.kind == "decision":
        if len(a.needle) < 2:
            sys.exit("usage: trace.py decision <run> <line>")
        return 0 if not print(json.dumps(
            t.resolve(f"dec:{a.needle[0]}@{a.needle[1]}", source=a.source),
            indent=2, ensure_ascii=False)) else 0

    if a.kind == "fork":
        hits = t.forks(needle)
        if not hits:
            sys.exit(f"no fork matches {needle!r}")
        if len(hits) > 1:
            print(f"{len(hits)} forks match {needle!r} — narrow it:\n")
            for f in hits[:20]:
                print(f"  {h_fork(f)}  {f[:66]}")
            return 2
        if a.json:
            print(json.dumps(t.fork(hits[0], limit=a.limit), indent=2,
                             ensure_ascii=False))
            return 0
        show_fork(t, hits[0], a.limit, a.source)
        return 0

    hits = t.options_matching(needle, a.fork)
    if not hits:
        sys.exit(f"no option matches {needle!r}")
    if len(hits) > 1:
        print(f"{len(hits)} options match {needle!r} — narrow it:\n")
        for o in hits[:20]:
            print(f"  {h_option(o['fork'], o['option'])}  {o['n']:>3} runs  "
                  f"{o['option'][:56]}")
        return 2
    out = t.option(hits[0], limit=a.limit, source=a.source)
    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    print(f"{out['handle']}   {out['n']} runs")
    print(f"  option  {_wrap(out['option'], 68, 10)}")
    print(f"  fork    {_wrap(out['fork'], 68, 10)}  {out['fork_handle']}")
    if len(out["raw_labels"]) > 1:
        print(f"\n  merged from {len(out['raw_labels'])} raw labels:")
        for r in out["raw_labels"][:10]:
            print(f"    - {_wrap(r, 64, 6)}")
    print()
    for d in out["decisions"]:
        print(f"  {d['handle']}  [{d.get('arm')}]")
        print(f"    {_wrap(d.get('operation') or d['text'], 66, 4)}")
        src = d.get("source") or {}
        if src.get("available"):
            for ln in src["lines"][:8]:
                print(f"    {ln['line']:>4} | {ln['text'][:64]}")
        elif a.source:
            print(f"    source: {src.get('why')}")
    if out["elided_decisions"]:
        print(f"\n  ... {out['elided_decisions']} further decisions "
              f"(--limit)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
