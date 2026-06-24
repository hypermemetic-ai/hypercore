---
kind: ask
state: standing
owner: operator
created: 2026-06-24
---
# worker-grounding-economy — the worker's grounding is the smallest high-signal set, not the whole spec inlined

Testing the second half surfaced it: the first real fenced worker died at `E2BIG` — the assembled
worker prompt is 131,323 B, past the OS argv limit. The argv crash is only the messenger. The defect
is that the prompt **violates our own solidified context-engineering standard**.
`work/archive/agent-facing-hardening/research.md` settles that standard (the arXiv context-files paper,
verified directly; Chroma *Context Rot* across 18 frontier models; Anthropic *effective context
engineering*): the goal is the *smallest possible set of high-signal tokens*, every token spends an
**attention budget**, *unnecessary requirements from context files make tasks harder*, and bloated
context *reduces task success rates*. The worker prompt is **70 % untouched-capability spec carried
whole "for scan"** and **4 % actual task** — the maximal attention budget spent on the least
decision-relevant tokens, **every episode**. We apply this standard ruthlessly to the 18-line anchor
and then violate it maximally in the worker prompt; the standard cannot hold in one channel and not
the other.

This **reopens `role-assembly`** (the whole-spec-preload, which the operator settled twice). That
decision waved off the context-rot evidence by asserting "the spec IS the high-signal core, preload it
whole" — conflating *high-signal for the system* with *high-signal for this change*, on a "small,
scannable" premise the spec's growth has falsified. The anti-myopia goal it defended needs the worker
to **see every capability and rescan on demand** — the *index*, not 92 KB of inlined bodies.

Redesign the worker's grounding so it is the smallest high-signal set while preserving the
whole-picture / anti-myopia defense `role-assembly` required.

## folding condition
- the worker prompt foregrounds the touched capabilities in full, carries every other capability as a
  high-signal **index** (not its full body), and the worker pulls a full capability just-in-time from
  its fenced checkout — so the assembled prompt drops well under the OS argv limit with margin;
- the myopia-defense holds: `spec/worker.md`'s rescan-catches-a-mis-mapping scenario still passes,
  because the index lists every capability and the worker pulls the body it implicates;
- `spec/worker.md` carries the change with its scenarios, and `python3 -m engine --check` is green.

Provenance: `work/archive/agent-facing-hardening/research.md` (:116, :118, :238, :239);
`work/archive/role-assembly/assembly.md` (the whole-spec-preload this supersedes).
