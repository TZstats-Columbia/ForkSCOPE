#!/usr/bin/env python3
"""The evidence contract: every check ships what a human needs to break it.

WHY THIS EXISTS

A reported statistic once said that 2.7% of within-fork option pairs were
near-duplicates. It was reassuring and it was structurally blind -- token
overlap cannot see that "compute the mean of the two rater columns" and
"average the two raters' scores" are one action. The error was caught in
minutes by a person reading the two option lists side by side in the garden
viewer.

The summary hid the error. The artifact showing the raw items revealed it.
That is the whole lesson, and this module makes it a contract instead of an
accident.

THE CONTRACT

A check emits four things, not one:

    verdict       PASS / REVIEW, machine-readable
    measurement   what was computed, and the null it was compared against
    exhibits      the actual items, worst-first, readable without running code
    handles       trace ids, so any exhibit walks back to source lines

Two rules are enforced here rather than left to discipline:

  1. EXHIBITS ARE WORST-FIRST. `exhibit()` requires a `worst` key function and
     sorts by it. There is no way to hand it a representative sample. A system
     optimising to look good shows its best cases; a check earning trust shows
     the cases closest to breaking it. The ordering key is recorded in the
     output so a reader knows what "worst" meant.

  2. A REVIEW VERDICT WITHOUT EXHIBITS IS AN ERROR. A check that fails and
     cannot show what failed is not reviewable, and `Report.write()` refuses
     it. This is the rule that would have caught the 2.7% claim.

A note on weak metrics. Ranking exhibits by lexical similarity is legitimate;
concluding from lexical similarity is not. A weak signal is a fine sort key
for human attention and fatal as evidence of absence. Checks that rank this
way must say so in the exhibit's `note`, and must not claim PASS on the
strength of it alone.

USAGE

    from exhibit import Report
    r = Report("vocab", "falsification exhibits for the vocabulary")
    c = r.check("V1", "options within one fork are distinct actions")
    c.measured(pairs=4210, above_threshold=41)
    c.against("ranking only -- no null; see the note on weak metrics")
    c.exhibit("within-fork option pairs most likely to be one action",
              rows, worst=lambda x: x["similarity"], show=20,
              note="similarity is a sort key for attention, not evidence")
    c.verdict("REVIEW", "the top 10 pairs read as one action")
    r.write()

Writes data/audits/<name>.json (agents) and data/audits/<name>.md (humans).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                                # noqa: E402

VERDICTS = ("PASS", "REVIEW", "INFO")

# Signals the pipeline itself uses to BUILD the vocabulary. A check that leans
# on one of these is partly restating a decision the pipeline already made, and
# its result is not independent evidence. Declaring the overlap is the only way
# to keep that visible: the numbers look identical either way.
BUILD_SIGNALS = {
    "co_occurrence":
        "cannot-link constraint in merge_forks and induce_forks — two options "
        "chosen by one run is treated as evidence their forks differ",
    "label_similarity":
        "candidate screen for every merge pass",
    "model_adjudication":
        "the same adjudicator that produced the grouping",
    "option_lists":
        "what the grouping passes were shown when they decided",
}


class Check:
    """One named check: a claim, what was measured, and what could break it."""

    def __init__(self, check_id, claim):
        self.id = check_id
        self.claim = claim
        self._measured = {}
        self._against = None
        self._blind = None
        self._uses = []
        self._exhibits = []
        self._verdict = None
        self._why = None

    def measured(self, **kw):
        self._measured.update(kw)
        return self

    def against(self, description):
        """The null or comparison. Say 'ranking only' when there isn't one."""
        self._against = description
        return self

    def blind_to(self, description):
        """What a violation could look like that this measure would not register.

        Required before a PASS. A statistic once reported that 2.7% of
        within-fork option pairs were near-duplicates; the measure was token
        overlap, which cannot see two descriptions of one action sharing no
        words. It was offered as reassurance and was never evidence about the
        corpus. Naming the blind spot is what makes the difference between
        "nothing found" and "nothing findable by this".

        `"nothing — exhaustive over the population"` is a legitimate answer,
        and asserting it explicitly is the point.
        """
        self._blind = description
        return self

    def uses(self, *signals):
        """Evidence this check relies on. Names from BUILD_SIGNALS are flagged.

        A check that uses a signal the pipeline used to build the thing being
        checked is entangled: its result partly restates the pipeline's own
        decision. The identity audit reported 27 of 30 fork pairs as one
        question, and 17 of those were pairs the repair had deliberately
        refused to merge on co-occurrence -- which the audit does not see. The
        rate was real and the conclusion drawn from it was wrong.
        """
        self._uses.extend(signals)
        return self

    @property
    def entangled(self):
        return sorted(set(self._uses) & set(BUILD_SIGNALS))

    def exhibit(self, title, rows, worst, show=20, columns=None, note=""):
        """The items themselves, ordered worst-first.

        `worst` is a key function; higher means closer to breaking the claim.
        Rows should carry a `handle` where one exists so a reader can trace
        the item without searching for it.
        """
        if not callable(worst):
            raise TypeError(
                f"{self.id}: exhibit needs a `worst` key function -- an "
                f"unordered or representative sample is not an exhibit")
        rows = list(rows)
        ordered = sorted(rows, key=worst, reverse=True)
        self._exhibits.append({
            "title": title,
            "ordered_by": getattr(worst, "__doc__", None) or "worst-first",
            "shown": min(show, len(ordered)),
            "of": len(ordered),
            "columns": columns or (list(ordered[0].keys()) if ordered else []),
            "note": note,
            "rows": ordered[:show],
        })
        return self

    def verdict(self, v, why):
        if v not in VERDICTS:
            raise ValueError(f"{self.id}: verdict must be one of {VERDICTS}")
        if not why:
            raise ValueError(f"{self.id}: a verdict needs a reason")
        self._verdict, self._why = v, why
        return self

    def as_dict(self):
        # `verdict` stays a top-level key so readers written against the
        # older audit files keep working.
        return {"verdict": self._verdict, "claim": self.claim,
                "why": self._why, "against": self._against,
                "blind_to": self._blind, "uses": sorted(set(self._uses)),
                "entangled_with": self.entangled,
                "measurement": self._measured, "exhibits": self._exhibits}


class Report:
    """A set of checks, written for both agents and people."""

    def __init__(self, name, subtitle="", corpus=None):
        self.name = name
        self.subtitle = subtitle
        self.corpus = corpus
        self.checks = []

    def check(self, check_id, claim):
        c = Check(check_id, claim)
        self.checks.append(c)
        return c

    def _validate(self):
        for c in self.checks:
            if c._verdict is None:
                raise ValueError(f"{c.id}: no verdict set")
            if c._verdict == "REVIEW" and not c._exhibits:
                raise ValueError(
                    f"{c.id}: REVIEW with no exhibits. A check that fails and "
                    f"cannot show what failed is not reviewable -- attach the "
                    f"items that failed, worst-first.")
            if c._verdict == "PASS" and not c._blind:
                raise ValueError(
                    f"{c.id}: PASS without blind_to(). Before a check may say "
                    f"nothing was found, it has to say what it could not have "
                    f"found. If the answer is genuinely nothing, write "
                    f"'nothing -- exhaustive over the population'.")
            if c.entangled and c._verdict == "PASS":
                raise ValueError(
                    f"{c.id}: PASS while entangled with {c.entangled}. This "
                    f"check leans on a signal the pipeline used to build what "
                    f"it is checking, so agreement is partly the pipeline "
                    f"agreeing with itself. Report INFO and say so.")

    def write(self, quiet=False):
        self._validate()
        P.AUDITS.mkdir(parents=True, exist_ok=True)
        jp = P.AUDITS / f"{self.name}.json"
        payload = {"report": self.name, "subtitle": self.subtitle,
                   "corpus": self.corpus,
                   **{c.id: c.as_dict() for c in self.checks}}
        jp.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                      encoding="utf-8")
        mp = P.AUDITS / f"{self.name}.md"
        mp.write_text(self.markdown(), encoding="utf-8")
        if not quiet:
            print(f"\nwrote {jp}")
            print(f"wrote {mp}")
        return jp, mp

    # -- human rendering ---------------------------------------------------

    def markdown(self):
        L = [f"# {self.name}", ""]
        if self.subtitle:
            L += [self.subtitle, ""]
        if self.corpus:
            L += [f"Corpus `{self.corpus}`.", ""]
        L += ["Exhibits are ordered **worst-first** — the cases closest to",
              "breaking each claim, never a representative sample. Handles",
              "resolve with `python3 scripts/trace.py resolve <handle>`.", ""]
        L += ["| check | verdict | claim |", "|---|---|---|"]
        for c in self.checks:
            L.append(f"| {c.id} | **{c._verdict}** | {c.claim} |")
        L.append("")
        for c in self.checks:
            L += [f"## {c.id} — {c.claim}", "",
                  f"**{c._verdict}** — {c._why}", ""]
            if c._against:
                L += [f"*Compared against:* {c._against}", ""]
            if c._blind:
                L += [f"*Cannot see:* {c._blind}", ""]
            if c.entangled:
                L += [f"> **Entangled.** This check uses "
                      f"{', '.join('`'+x+'`' for x in c.entangled)}, which the "
                      f"pipeline also used to build what is being checked "
                      f"({'; '.join(BUILD_SIGNALS[x] for x in c.entangled)}). "
                      f"Its agreement is not independent evidence.", ""]
            if c._measured:
                L += ["| measure | value |", "|---|---|"]
                L += [f"| {k} | {v} |" for k, v in c._measured.items()]
                L.append("")
            for ex in c._exhibits:
                L += [f"### {ex['title']}", ""]
                if ex["shown"] < ex["of"]:
                    L += [f"Showing the worst **{ex['shown']} of "
                          f"{ex['of']}**.", ""]
                else:
                    L += [f"All **{ex['of']}**.", ""]
                if ex["note"]:
                    L += [f"> {ex['note']}", ""]
                L += self._render_rows(ex)
        return "\n".join(L) + "\n"

    @staticmethod
    def _render_rows(ex):
        cols, rows = ex["columns"], ex["rows"]
        if not rows:
            return ["*(none)*", ""]
        longest = max((len(str(r.get(c, ""))) for r in rows for c in cols),
                      default=0)
        if longest <= 48 and len(cols) <= 6:
            out = ["| " + " | ".join(cols) + " |",
                   "|" + "|".join("---" for _ in cols) + "|"]
            for r in rows:
                out.append("| " + " | ".join(
                    str(r.get(c, "")).replace("|", "\\|") for c in cols) + " |")
            return out + [""]
        out = []
        for i, r in enumerate(rows, 1):
            head = r.get("handle") or r.get("id") or f"#{i}"
            out.append(f"**{i}. `{head}`**")
            out.append("")
            for c in cols:
                if c in ("handle", "id"):
                    continue
                v = r.get(c, "")
                if v == "" or v is None:
                    continue
                out.append(f"- *{c}*: {v}")
            out.append("")
        return out
