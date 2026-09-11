#!/usr/bin/env python3
"""The only module in this repo that talks to a model.

Everything else in the pipeline is deterministic. This is the boundary, and it
is deliberately narrow: one function, one transport, one cache, one log. If a
script wants a model it imports `ask`; it does not shell out on its own.

Transport is the `claude` CLI in print mode, which uses the operator's existing
Claude Code auth -- no API key is stored anywhere in this repo. Calls run from a
scratch working directory with `--strict-mcp-config` so the repo's CLAUDE.md,
skills and MCP servers are not loaded into every request; that overhead is
otherwise ~35k cached tokens per call and dwarfs the payload.

Determinism, honestly stated: the CLI exposes no temperature and no seed, so
identical inputs are *not* guaranteed to produce identical outputs. Three
things follow.

(1) Every response is cached on sha256(prompt + model + schema), so a re-run of
the pipeline is byte-identical and free -- reproducibility comes from the
cache, not from the model.

(2) The `model` in that key is an ALIAS (`sonnet`, `opus`), not a version. If an
alias is re-pointed, old entries keep hitting while new calls are served by a
different model, and one dataset can mix versions. `model_resolved` and
`cli_version` are therefore recorded on every entry and every log line -- see
`resolved_model`. They are NOT in the key: putting them there is the correct
design and costs a full rebuild, so the gap is recorded rather than closed.
Entries written before this existed have no such field, and absence means
"unknown", never "same".

(3) Genuine run-to-run variation has to be *measured* rather than assumed away.
Do it under a separate `FORKSCOPE_STUDY` root with an empty cache, not with
`nocache=True`: nocache skips the cache READ but still WRITES to the same key,
so measuring a baseline that way overwrites it. See `stability/`, which does
this and reports what it found.

Cost shape drives the call design: the fixed per-call overhead is ~$0.04 on
sonnet regardless of payload size, so the pipeline is built from few large
calls (segment a whole script at once) rather than many small ones.

Usage:
    from llm import ask
    out = ask("01_segment_code", {"path": "...", "code": "..."}, schema=SCHEMA)

    python3 scripts/llm.py selftest        # one live call, prints cost
    python3 scripts/llm.py stats           # cache and spend summary
"""
import hashlib
import json
import os
import random
import subprocess
import sys
import threading
import tempfile
import time
from pathlib import Path

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths as P                                             # noqa: E402

REPO = P.ROOT
PROMPTS = P.PROMPTS
CACHE = P.CACHE
RUNS = P.CALL_LOG
DEFAULT_MODEL = "sonnet"          # bulk extraction; adjudication passes "opus"
MAX_RETRIES = 3

# The two roles, overridable. Call sites say "sonnet" or "opus" -- a ROLE, not a
# version -- and `_role()` resolves that to whatever this build is pinned to.
# Defaults reproduce the historical behaviour exactly, so an unset environment
# changes nothing.
#
# Why this exists: `--model` also accepts a full model name, and only a few
# models publish a dated snapshot (`claude-sonnet-4-5-20250929`,
# `claude-opus-4-5-20251101`, `claude-haiku-4-5-20251001`). Current-generation
# ids -- `claude-sonnet-5`, `claude-opus-5` -- are aliases with no dated form,
# so a build pinned to one of those can be re-pointed under it without notice.
# Pinning is therefore a study-level decision, and it belongs in the
# environment beside the other study configuration rather than in twelve
# hardcoded call sites.
MODEL_BULK = os.environ.get("FORKSCOPE_MODEL_BULK", "sonnet")
MODEL_ADJ = os.environ.get("FORKSCOPE_MODEL_ADJ", "opus")

# Per-PROMPT override, which the two roles above cannot express. The roles are
# "bulk" and "adjudication", but the layers that matter are the CHANNELS -- code
# and prose -- and both are bulk. Measured on two runs, pinned Sonnet 4.5 holds
# the code channel (lenient F1 0.788, core 0.909, grouping ARI 0.655) and loses
# the prose channel (claims -32%, links -27%, ARI 0.348). Those want different
# models, and there was no way to say so.
#
#   FORKSCOPE_MODEL_MAP='{"02_segment_prose": "claude-opus-4-5-20251101"}'
#
# Keyed by prompt name, so it is legible in a manifest and survives being read
# back six months later. A prompt not named falls through to its role.
try:
    MODEL_MAP = json.loads(os.environ.get("FORKSCOPE_MODEL_MAP", "{}"))
    if not isinstance(MODEL_MAP, dict):
        raise ValueError("FORKSCOPE_MODEL_MAP must be a JSON object")
except (ValueError, TypeError) as e:
    raise SystemExit(f"FORKSCOPE_MODEL_MAP is not usable: {e}")


def _role(model, prompt=None):
    """Resolve prompt-then-role to the concrete model this build is pinned to.

    A per-prompt entry wins over the role, because it is the more specific
    statement and the only way to assign a model per channel.
    """
    if prompt and prompt in MODEL_MAP:
        return MODEL_MAP[prompt]
    if model == "sonnet":
        return MODEL_BULK
    if model == "opus":
        return MODEL_ADJ
    return model                  # already a concrete id; pass through
# Extended reasoning is ~86% of output tokens on these tasks. Off by default;
# the retry ladder buys it back only when the cheap attempt fails to parse.
THINKING_BUDGET = int(os.environ.get("LLM_THINKING", "0"))
# Measured: the 0-budget rung fails to parse ~65% of the time, so it costs a
# wasted round trip on two calls in three -- ~24% fewer tokens but roughly
# double the wall time. When the binding constraint is throttling rather than
# tokens, fewer calls wins. Start where the model actually succeeds.
THINKING_RETRY = [4000, 8000, 16000]
TIMEOUT_S = 900
# Throttling arrives as a burst, so back off hard and jitter to de-sync workers.
TRANSPORT_TRIES = int(os.environ.get("LLM_TRANSPORT_TRIES", "6"))
TRANSPORT_BACKOFF = [20, 60, 180, 420, 900, 900]


class LLMError(RuntimeError):
    """Bad content: unparseable, schema-invalid, or failing a semantic check.
    Retried by rephrasing -- the model is told what was wrong."""


class TransportError(LLMError):
    """The call never produced content: non-zero exit, timeout, throttling.

    Kept separate because the remedies are opposites. Rephrasing a prompt does
    nothing for a rate limit, and retrying instantly three times just burns the
    attempt budget inside the throttle window -- which is exactly how a full
    corpus run lost 154 of 204 runs in a burst while single calls kept working.
    These retry with backoff and an unchanged prompt."""


def prompt_text(name):
    p = PROMPTS / f"{name}.md"
    if not p.exists():
        raise LLMError(f"no prompt template: {p}")
    return p.read_text(encoding="utf-8")


def prompt_hash(name):
    """Templates are versioned by content hash; changing one invalidates its
    cache entries automatically, which is the point."""
    return hashlib.sha256(prompt_text(name).encode("utf-8")).hexdigest()[:16]


def _render(name, payload):
    """Template + payload. The template owns the instructions and the output
    contract; the payload is appended as a fenced JSON block so there is never
    any ambiguity about where instructions end and data begins."""
    return (prompt_text(name).rstrip() + "\n\n## Input\n\n```json\n"
            + json.dumps(payload, ensure_ascii=False, indent=1) + "\n```\n")


def resolved_model(env):
    """The model version that actually served a call, from the CLI envelope.

    `--model sonnet` is an ALIAS. The envelope's `modelUsage` is keyed by the
    resolved id -- `{"claude-sonnet-5": {...}}` -- so the version is available
    on every call and was simply being discarded.

    Recorded but deliberately NOT in the cache key. Putting it there is the
    correct design and costs a full rebuild: every existing entry was written
    under an alias-only key and would miss, which on this corpus is ~2,300 calls
    and several hundred dollars. So the field is additive, and the honest
    consequence is stated rather than hidden -- a cache HIT may return an entry
    produced by a different version than a miss would be served by today. What
    this buys is that from now on we can *tell*, which was impossible before.

    Returns a string when one model served the call, a sorted list when several
    did (fallbacks, sub-agents), or None on an older CLI that omits the field.
    Absence in an entry means "unknown", never "same".
    """
    mu = env.get("modelUsage")
    if not isinstance(mu, dict) or not mu:
        return None
    ids = sorted(mu)
    return ids[0] if len(ids) == 1 else ids


_CLI_VERSION = None


def cli_version():
    """`claude --version`, resolved once per process.

    The client is part of what produced a result -- prompt handling and
    defaults change between releases -- and it is the one component version we
    can obtain without a per-call cost. Memoised because it is a subprocess and
    would otherwise run thousands of times.
    """
    global _CLI_VERSION
    if _CLI_VERSION is None:
        try:
            r = subprocess.run(["claude", "--version"], capture_output=True,
                               text=True, timeout=30)
            _CLI_VERSION = (r.stdout or "").strip() or "unrecorded"
        except Exception:                                       # noqa: BLE001
            _CLI_VERSION = "unrecorded"
    return _CLI_VERSION


def _key(name, payload, model, schema):
    h = hashlib.sha256()
    h.update(prompt_hash(name).encode())
    h.update(model.encode())
    h.update(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    h.update(json.dumps(schema or {}, sort_keys=True).encode())
    return h.hexdigest()


def _extract_json(text):
    """The model is asked for bare JSON, but tolerate a fenced block or leading
    prose rather than failing a whole run on formatting."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.lstrip().lower().startswith("json"):
            t = t.lstrip()[4:]
    t = t.strip()
    if not t.startswith(("{", "[")):
        i = min([j for j in (t.find("{"), t.find("[")) if j >= 0], default=-1)
        if i < 0:
            raise LLMError("no JSON found in response")
        t = t[i:]
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        # trailing commentary after a complete value
        dec = json.JSONDecoder()
        try:
            return dec.raw_decode(t)[0]
        except json.JSONDecodeError as e:
            # THE SAME BUG _validate GUARDS AGAINST, ONE FUNCTION UP.
            #
            # raw_decode raises json.JSONDecodeError, which is not an LLMError,
            # so it sailed past the retry ladder below and killed the whole run
            # -- on a fault the model could simply be asked to fix. One of two
            # runs in the soccer-C smoke test died this way, and distill.py
            # still exited 0, which at 207 runs is a silently smaller corpus.
            #
            # Re-raised as LLMError so the informed-retry path appends the
            # specific failure to the prompt and asks again.
            # Truncation and a formatting fault need DIFFERENT advice, so the
            # test is where the parse died, not what it said: a cut-off answer
            # fails at the very end of the text, a malformed one in the middle.
            # Matching on the message instead flags almost everything as
            # truncated, because "Expecting" prefixes most JSON errors.
            hint = (" The answer was CUT OFF mid-value. Return a COMPLETE and "
                    "SHORTER document: keep every line covered, but write "
                    "terser snippets and rationales."
                    if len(t) - e.pos <= 2 else
                    " Fix the syntax at that position and return the whole "
                    "document again.")
            raise LLMError(
                f"response is not valid JSON: {e.msg} at line {e.lineno} "
                f"column {e.colno} (char {e.pos} of {len(t)}).{hint}") from None


def _validate(obj, schema):
    """jsonschema if available, else a minimal required-keys check so the
    pipeline still runs in a bare environment.

    Every failure is re-raised as LLMError. jsonschema raises ValidationError,
    which is not an LLMError, so letting it escape would sail straight past the
    retry loop and kill the run on a fault the model could simply be asked to
    fix -- an omitted echo field took out a whole batch that way.
    """
    if not schema:
        return
    try:
        import jsonschema
    except ImportError:
        for k in schema.get("required", []):
            if k not in obj:
                raise LLMError(f"missing required key: {k}")
        return
    try:
        jsonschema.validate(obj, schema)
    except jsonschema.ValidationError as e:
        path = "/".join(str(p) for p in e.absolute_path) or "(root)"
        raise LLMError(f"schema violation at {path}: {e.message}")


# Callers parallelise at two levels -- runs in a pool, and the two independent
# segment calls inside each run -- which would otherwise multiply. Every CLI
# invocation spawns a Node process of a few hundred MB, so the ceiling on
# concurrent model calls lives here, once, where it cannot be bypassed.
_SEM = threading.Semaphore(int(os.environ.get("LLM_CONCURRENCY", "12")))


def _invoke(text, model, thinking=None):
    """One CLI call from a scratch cwd, under the global concurrency cap.

    `thinking` caps extended reasoning. It is the dominant cost here and not by
    a little: a measured segmentation call billed 25,794 output tokens for a
    1,949-token answer -- one turn, one iteration, no retry. Setting the budget
    to 0 cuts output ~86%. It also makes malformed JSON more likely, which is
    why it is only viable behind the informed-retry path above: one retry at
    ~3.5k tokens still costs a fraction of one clean answer at ~26k.
    """
    with _SEM, tempfile.TemporaryDirectory() as scratch:
        cmd = ["claude", "-p", "--model", model,
               "--output-format", "json", "--strict-mcp-config"]
        penv = dict(os.environ)
        if thinking is not None:
            penv["MAX_THINKING_TOKENS"] = str(thinking)
        t0 = time.time()
        try:
            r = subprocess.run(cmd, input=text, capture_output=True, text=True,
                               cwd=scratch, timeout=TIMEOUT_S, env=penv,
                               encoding="utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            raise TransportError(f"timeout after {TIMEOUT_S}s")
        if r.returncode != 0:
            raise TransportError(
                f"claude exited {r.returncode}: "
                f"{(r.stderr or r.stdout or chr(40)+chr(41))[:300].strip()}")
        try:
            env = json.loads(r.stdout)
        except json.JSONDecodeError:
            raise TransportError(f"CLI did not return JSON: {r.stdout[:200]}")
        env["_wall_s"] = round(time.time() - t0, 1)
        return env


def ask(name, payload, schema=None, model=DEFAULT_MODEL, nocache=False,
        run_id="default", check=None, thinking=THINKING_BUDGET):
    """Render `name` with `payload`, call the model, return parsed JSON.

    Cached by (prompt content, model, payload, schema). Retries on transport
    error, unparseable output, or schema violation -- appending the specific
    failure to the prompt so the retry is informed rather than a coin flip.

    `check` is an optional callable taking the parsed object and raising
    ValueError with a specific message when a *semantic* contract is broken.
    Schema validation cannot express "these line ranges must partition 1..n",
    and that invariant is the whole basis of the coverage claim, so it is
    enforced here with the same informed-retry path rather than checked after
    the fact and shrugged at.
    """
    # parents=True, because both live under cache/ and a fresh study root has
    # no cache/ at all. Without it the first call into a new root dies on
    # FileNotFoundError rather than creating what it needs -- which is exactly
    # what a replicate is.
    CACHE.mkdir(parents=True, exist_ok=True)
    RUNS.mkdir(parents=True, exist_ok=True)
    # Resolve the ROLE to the pinned model before the key is computed, so a
    # build pinned to a dated snapshot gets its own cache namespace and cannot
    # silently hit entries produced by whatever the alias meant that week.
    model = _role(model, name)
    key = _key(name, payload, model, schema)
    cpath = CACHE / f"{key}.json"
    # A cache entry truncated by an interrupted write is a half-written file,
    # not a cache hit. Reading it raised a bare JSONDecodeError from inside the
    # cache-read path, where there is no retry ladder at all -- so one bad file
    # would kill every future run that hashed to it, and the only cure was
    # knowing which file to delete. Treat it as a miss and re-ask.
    rec = None
    if cpath.exists() and not nocache:
        try:
            rec = json.loads(cpath.read_text(encoding="utf-8"))
            rec["result"]
        except (json.JSONDecodeError, OSError, KeyError, TypeError):
            cpath.unlink(missing_ok=True)
            rec = None
    if rec is not None:
        # Re-apply the semantic check to cached results. `check` is a callable
        # and cannot go in the cache key, so a *tightened* invariant would
        # otherwise be silently unenforced on everything already cached -- the
        # cache would quietly grandfather in data the current rules reject.
        # A cached result that now fails is discarded and the call redone.
        if check:
            try:
                check(rec["result"])
                return rec["result"]
            except ValueError:
                cpath.unlink(missing_ok=True)
        else:
            return rec["result"]

    base = _render(name, payload)
    text, last = base, None
    attempt, transport_tries = 0, 0

    def _log(env, ok, err=None):
        """Every PAID attempt, not only the one that worked.

        Logging successes alone made cost blind to exactly the calls that cost
        most. Measured on the soccer-C stratified sample: 30 logged calls, 44
        attempts actually paid for, so 14 were invisible and the logged total
        was 47% low ($6.71 against $9.84). `/distill` tells you to report cost
        from this file, so the reported figure was wrong by half whenever
        retries were common -- and retries are common: 11 of 30 calls here.

        A transport error never produced content and is not logged; it has no
        cost and would otherwise inflate the call count with non-calls.
        """
        with (RUNS / f"{run_id}.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "key": key,
                "prompt": name, "prompt_hash": prompt_hash(name), "model": model,
                "model_resolved": resolved_model(env),
                "cli_version": cli_version(),
                "attempt": attempt, "ok": ok, "error": err,
                "cost_usd": float(env.get("total_cost_usd") or 0.0),
                "wall_s": env.get("_wall_s"),
                "usage": env.get("usage", {}),
                "payload_keys": sorted(payload)}, ensure_ascii=False) + "\n")

    while attempt < MAX_RETRIES:
        attempt += 1
        env = None
        try:
            budget = (THINKING_RETRY[min(attempt - 1, len(THINKING_RETRY) - 1)]
                      if thinking == 0 else thinking)
            env = _invoke(text, model, budget)
            out = _extract_json(env.get("result", ""))
            _validate(out, schema)
            if check:
                try:
                    check(out)
                except ValueError as ce:
                    raise LLMError(str(ce))
        except TransportError as e:
            # Never produced content: wait it out, keep the prompt, and do not
            # spend a content attempt. Capped so a genuine outage still ends.
            last = str(e)
            transport_tries += 1
            attempt -= 1
            if transport_tries > TRANSPORT_TRIES:
                raise LLMError(f"{name}: transport failed {transport_tries}x; "
                               f"last: {last}")
            delay = TRANSPORT_BACKOFF[min(transport_tries - 1,
                                          len(TRANSPORT_BACKOFF) - 1)]
            time.sleep(delay + random.uniform(0, delay * 0.3))  # de-sync workers
            continue
        except LLMError as e:
            last = str(e)
            if env is not None:          # content was produced, so it was paid for
                _log(env, ok=False, err=last)
            text = (base + f"\n## Correction\n\nA previous attempt failed with: "
                    f"{last}\nReturn only valid JSON meeting the contract above.\n")
            continue

        cost = float(env.get("total_cost_usd") or 0.0)
        resolved = resolved_model(env)
        cpath.write_text(json.dumps({
            "key": key, "prompt": name, "prompt_hash": prompt_hash(name),
            "model": model, "model_resolved": resolved,
            "cli_version": cli_version(),
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "attempt": attempt, "cost_usd": cost,
            "result": out}, ensure_ascii=False), encoding="utf-8")
        _log(env, ok=True)
        return out
    raise LLMError(f"{name}: {MAX_RETRIES} attempts failed; last: {last}")


def stats():
    n = spend = 0
    for f in CACHE.glob("*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        n += 1
        spend += d.get("cost_usd", 0.0)
    print(f"cache: {n} entries, ${spend:.2f} spent to fill it")
    for f in sorted(RUNS.glob("*.jsonl")):
        rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l]
        if not rows:
            continue
        c = sum(r.get("cost_usd", 0) for r in rows)
        w = sum(r.get("wall_s") or 0 for r in rows)
        print(f"  run {f.stem}: {len(rows)} calls, ${c:.2f}, {w/60:.1f} min wall")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "stats":
        stats()
    elif cmd == "selftest":
        S = {"type": "object", "required": ["ok"],
             "properties": {"ok": {"type": "boolean"}}}
        PROMPTS.mkdir(exist_ok=True)
        t = PROMPTS / "_selftest.md"
        t.write_text("Return only the JSON object {\"ok\": true}. No prose.\n",
                     encoding="utf-8")
        try:
            print("uncached:", ask("_selftest", {"n": 1}, schema=S, nocache=True,
                                   run_id="selftest"))
            print("cached  :", ask("_selftest", {"n": 1}, schema=S,
                                   run_id="selftest"))
            stats()
        finally:
            t.unlink(missing_ok=True)
    else:
        sys.exit(__doc__)
