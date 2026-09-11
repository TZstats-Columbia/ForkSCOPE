#!/usr/bin/env python3
"""The review round-trip: questions the pipeline cannot answer for itself.

WHY THIS IS A FILE AND NOT A CONVERSATION

Several judgements in this pipeline are genuinely a person's to make. Whether
two forks are one question, whether an option bundles two decisions, whether a
fork is multi-select or mis-clustered -- the shape is identical in each case and
only reading settles it.

Asking those in chat loses them. The answer is given once, applied once, and
three weeks later nobody can say who decided what or why, so the same question
gets asked again and may be answered differently. A round is therefore an
artifact:

    reviews/round-NN.md      questions with their evidence; the human answers here
    reviews/round-NN.json    the same, machine-readable, plus what was applied

The .md is the one a person edits. `read` parses their answers back out and
`apply` is left to /refine, which records what it changed.

WHAT MAKES A GOOD QUESTION

Not "is this right?" A question earns a person's attention when it states what
each possible answer would change. If both answers lead to the same action, it
is not a question -- it is a note.

Questions are drawn from the audit exhibits, which are already ordered
worst-first, so a round is the top of a queue that has been ranked rather than
sampled.

USAGE
    python3 scripts/review_round.py new --n 12
    python3 scripts/review_round.py status
    python3 scripts/review_round.py read            # parse answers back out
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402

ROUNDS = P.STUDY_ROOT / "reviews"
CHOICES = {
    "V1": ["merge them", "keep separate", "need more evidence"],
    "V2": ["genuinely multi-select", "robustness refit",
           "clustering artifact - split", "need more evidence"],
    "V3": ["one question - merge the forks", "two questions - keep separate",
           "need more evidence"],
    "V4": ["split into two options", "one action - keep", "need more evidence"],
    "V5": ["genuinely contested - keep", "under-merged - re-adjudicate",
           "need more evidence"],
}
STAKES = {
    "V1": "Merging is unrecoverable if wrong; leaving them apart is visible "
          "and fixable later. When unsure, keep separate.",
    "V2": "If multi-select, this fork's modal share and effective-option count "
          "are not well defined and should not be reported.",
    "V3": "Merging two forks that are genuinely one is safe; merging two that "
          "are not destroys a distinction invisibly.",
    "V4": "A compound option makes two decisions inseparable: every run "
          "choosing it is recorded as having made both, and the second "
          "vanishes from its own fork.",
    "V5": "The most contested fork in the corpus and a clustering failure "
          "have the same shape. Only the content separates them.",
}


def _round_paths(n):
    return ROUNDS / f"round-{n:02d}.md", ROUNDS / f"round-{n:02d}.json"


def _next_n():
    ROUNDS.mkdir(parents=True, exist_ok=True)
    have = [int(m.group(1)) for f in ROUNDS.glob("round-*.json")
            if (m := re.match(r"round-(\d+)\.json$", f.name))]
    return max(have, default=0) + 1


def build(limit):
    """Draw questions from the audit exhibits, worst-first, one per item."""
    f = P.AUDITS / "vocab_exhibits.json"
    if not f.exists():
        sys.exit("no vocab_exhibits.json — run scripts/audit_vocab.py first")
    d = json.loads(f.read_text(encoding="utf-8"))
    qs = []
    for cid in ("V2", "V3", "V1", "V4", "V5"):     # conclusive first
        c = d.get(cid)
        if not isinstance(c, dict) or c.get("verdict") == "PASS":
            continue
        for ex in c.get("exhibits", []):
            for row in ex["rows"]:
                qs.append({
                    "check": cid, "claim": c["claim"],
                    "exhibit": ex["title"], "row": row,
                    "handle": row.get("handle") or row.get("trace_a", ""),
                    "choices": CHOICES.get(cid, ["yes", "no", "unsure"]),
                    "stakes": STAKES.get(cid, ""),
                    "answer": "", "comment": "", "status": "open",
                })
            break                                   # one exhibit per check
    # interleave so a round is not twelve of the same question
    out, by = [], {}
    for q in qs:
        by.setdefault(q["check"], []).append(q)
    while len(out) < limit and any(by.values()):
        for cid in list(by):
            if by[cid] and len(out) < limit:
                out.append(by[cid].pop(0))
    return out


def render(n, qs):
    L = [f"# Review round {n:02d}", "",
         f"Study `{P.STUDY_NAME}` · vocabulary `{P.FINAL_TAG}` · "
         f"opened {date.today().isoformat()}", "",
         "Questions the pipeline cannot settle for itself. Each one states "
         "what your answer would change; if both answers lead to the same "
         "action, it should not be here.",
         "",
         "**How to answer.** Write under `**Answer:**` — one of the listed "
         "choices, or your own words. `**Comment:**` is free text and is kept "
         "verbatim. Leave anything blank to defer it to the next round.",
         "",
         "Resolve any handle with:",
         "",
         "```bash",
         "python3 scripts/trace.py resolve <handle>",
         "```", ""]
    for i, q in enumerate(qs, 1):
        r = q["row"]
        L += [f"## Q{i} · {q['check']} · `{q['handle']}`", "",
              f"*{q['claim']}*", ""]
        for k, v in r.items():
            if k in ("handle",) or v in ("", None):
                continue
            L.append(f"- **{k}**: {v}")
        L += ["", f"> {q['stakes']}", "",
              "Choices: " + " · ".join(f"`{c}`" for c in q["choices"]), "",
              "**Answer:**", "", "**Comment:**", "", "---", ""]
    return "\n".join(L)


def parse(md):
    """Read answers back out. Tolerant of reformatting, blank answers, prose."""
    out = {}
    blocks = re.split(r"^## Q(\d+) ", md, flags=re.M)[1:]
    for i in range(0, len(blocks), 2):
        qn, body = int(blocks[i]), blocks[i + 1]

        def grab(label):
            m = re.search(rf"\*\*{label}:\*\*(.*?)(?=\*\*\w+:\*\*|^---|\Z)",
                          body, re.S | re.M)
            return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        out[qn] = {"answer": grab("Answer"), "comment": grab("Comment")}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["new", "status", "read"])
    ap.add_argument("--n", type=int, default=12, help="questions in a new round")
    ap.add_argument("--round", type=int, help="which round (default: latest)")
    a = ap.parse_args()

    if a.cmd == "new":
        n = _next_n()
        qs = build(a.n)
        if not qs:
            print("no open questions — every check either passes or has no "
                  "exhibits")
            return 0
        mp, jp = _round_paths(n)
        mp.write_text(render(n, qs), encoding="utf-8")
        jp.write_text(json.dumps(
            {"round": n, "study": P.STUDY_NAME, "tag": P.FINAL_TAG,
             "opened": date.today().isoformat(), "questions": qs},
            indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"round {n:02d}: {len(qs)} questions")
        for c in sorted({q['check'] for q in qs}):
            print(f"  {c}  {sum(1 for q in qs if q['check']==c)}")
        print(f"\n-> {mp}\n   answer in that file, then: "
              f"python3 scripts/review_round.py read")
        return 0

    n = a.round or (_next_n() - 1)
    if n < 1:
        print("no rounds yet — python3 scripts/review_round.py new")
        return 0
    mp, jp = _round_paths(n)
    if not mp.exists():
        sys.exit(f"no {mp}")
    st = json.loads(jp.read_text(encoding="utf-8"))
    ans = parse(mp.read_text(encoding="utf-8"))

    if a.cmd == "read":
        for i, q in enumerate(st["questions"], 1):
            g = ans.get(i, {})
            q["answer"], q["comment"] = g.get("answer", ""), g.get("comment", "")
            if q["answer"] and q["status"] == "open":
                q["status"] = "answered"
        jp.write_text(json.dumps(st, indent=1, ensure_ascii=False),
                      encoding="utf-8")

    tally = {}
    for q in st["questions"]:
        tally[q["status"]] = tally.get(q["status"], 0) + 1
    print(f"round {n:02d} · {len(st['questions'])} questions · " +
          " · ".join(f"{k} {v}" for k, v in sorted(tally.items())))
    for i, q in enumerate(st["questions"], 1):
        if q["status"] == "answered":
            print(f"  Q{i} {q['check']} {q['handle']}: {q['answer'][:60]}")
    if tally.get("answered"):
        print(f"\n{tally['answered']} answered and not yet applied — /refine")
    return 0


if __name__ == "__main__":
    sys.exit(main())
