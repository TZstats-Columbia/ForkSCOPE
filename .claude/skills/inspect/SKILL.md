---
name: inspect
description: >-
  Phase 7 — examine what an itinerary run actually produced, with a human,
  before it is filed into the garden. Use after /itinerary has built and run a
  path.
---

Decide together whether the run did what the path said, and what its result
shows. Argument: the run id.

Nothing is filed until this phase agrees. A run added before it is understood
is a run nobody can interpret later.

## Did it do what was specified?

```bash
python3 scripts/distill.py run <run-id>
python3 scripts/trace.py run <run-id>
```

Distil the new run through the same pipeline as any other and compare its path
to the itinerary, fork by fork. **Divergences are the finding here.** A run
that took an option the user did not choose either had that choice forced by an
earlier one — foreclosure the phase-4 audit missed — or the build is wrong.

Check what the specification did not cover, too. A path fixes a handful of
forks; the run had to decide the rest, and those are choices *you* made on the
user's behalf. List them.

**There is no itinerary runner**, so the whole build is your implementation of
their choices rather than the corpus's. That makes this phase load-bearing
rather than a formality: every divergence is either a foreclosure the phase-4
audit missed or a mistake in code you wrote, and the user cannot tell those
apart without you.

## Is the estimate plausible?

Report it beside the distribution of real runs, and beside the nearest paths:

```bash
python3 -c "import json,sys;sys.path.insert(0,'scripts');import paths as P;\
d=json.load(open(P.OUTCOMES));import statistics as s;\
v=[x['or_scale_estimate'] for x in d if x.get('or_scale_estimate')];\
print(f'corpus n={len(v)} median={s.median(v):.3f} range={min(v):.2f}-{max(v):.2f}')"
```

If it lands outside the corpus range, that is interesting **or** a bug, and the
two look identical. Trace the estimate back through the run before calling it
either.

**One run is one observation.** It does not update a finding, confirm a
hypothesis, or move a Shapley result. Say that plainly, especially when the
number is striking.

## Set the provenance tag

| | |
|---|---|
| `itinerary` | every option came from the corpus |
| `authored` | any operation no corpus run performed — including a novel *combination* of attested actions |

When in doubt, `authored`. The tag is a claim about where the analysis came
from, and over-claiming corpus provenance is the error that matters.

## Then file it

`/refine` or the filing step of `/itinerary`. Then recompute the statistics
**including** it:

```bash
python3 scripts/stability.py --corpus <tag>
```

Once any non-corpus run exists, that prints a `PROVENANCE` block giving every
concentration statistic with and without them. Report the delta. A large one is
not an error — it is the finding that this path was unlike the corpus — but it
must be stated, because a headline that drifts silently as paths are walked is
the thing the tag exists to prevent.
