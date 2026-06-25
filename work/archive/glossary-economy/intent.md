---
kind: ask
state: done
owner: operator
created: 1782345113
---
# glossary-economy — the worker's glossary is its change's terms, not the whole ratified vocabulary

worker-grounding-economy (fbe26ba) collapsed the untouched spec bodies to an index; at 64 KB the single
largest block left is now the **glossary at ~20 KB (31%)**, carried whole every episode — five times the
index of the entire rest of the spec. It is the same defect one level down: the whole glossary is
high-signal *for the system*, not *for this change*. The whole ratified vocabulary is an **architect**
asset — the architect authors operator-facing prose, ratifies the vocabulary, and runs the vocabulary
check; the worker writes machine-facing spec deltas and needs only the terms its change touches.

## the selection rule — the prose selects, we don't
A glossary entry is inlined iff its **term appears in the prose the worker holds foregrounded** — the
touched capability bodies + the handed delta + the ask. The full `glossary.md` stays on disk in the
fenced checkout; a term the rescan implicates but the working set did not name is read **just-in-time**
from there — the same seam C1 placed for capability bodies. Derived from the text, never a hand-label: a
per-entry "architect-term / worker-term" tag would drift, must be maintained, and is wrong at the
boundary (`card`/`queue` stay when the change's prose names the operator's queue; a tag would mis-drop
them). The audience split the operator named — the glossary is the architect's, not the worker's — falls
out *mechanically*: the operator/infra vocabulary vanishes because it is not in the worker's prose, not
because we declared it so. Measured on vocabulary-check: 36 of 72 entries kept (~9.7 KB of 19.4) — and
that is a glossary-heavy change; a one-capability change keeps fewer.

## what holds it safe
The worker still gets **every term its prose names**, so it cannot drift on a term it is actually using.
The only residual — a worker coining a synonym for a term *not* in its working set — is exactly what the
architect's coherence read catches today and what the `vocabulary-check` guard (open) will automate. The
lean glossary is licensed by the same guard the corpus already rests on; it does not depend on that guard
being built first, so this ships independently.

## shared-seam discipline
This MODIFIES the grounding requirement's glossary clause in `spec/worker.md` ("The glossary is preloaded
whole"). It is not concurrent with the integrity-stack nodes, which **ADD** new requirements to the same
file — ADD beside a MODIFY of a different requirement composes; two MODIFYs of one requirement clobber at
fold. Rescan `spec/worker.md` at its current tip (post fbe26ba) before building.

## folding condition
- the assembled worker prompt inlines a glossary entry only when its term appears in the foregrounded
  prose, carries the rest by reading `glossary.md` just-in-time from the checkout, and the prompt names
  that read;
- the whole-picture / consistency defenses hold: the worker still sees every term its change names, and
  the existing grounding scenarios stay green;
- `spec/worker.md` carries the change with its scenario (the selection gated by a check block), and
  `python3 -m engine --check` is green.

Provenance: `work/archive/worker-grounding-economy/` (fbe26ba, the index+JIT redesign this extends); the
36/72 measurement; the operator's framing that the whole glossary is the architect's asset.
