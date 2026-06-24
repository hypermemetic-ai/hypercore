---
kind: ask
state: done
owner: operator
created: 2026-06-24
---
# handoff-format — JSON is the wrong format for the model→engine hand-offs; design the format for all of them

Every model→engine reply in the system is a JSON object, parsed through one seam
(`transport.parse` / `transport.parse_object`). The `operator-view-readiness` re-run (2026-06-24)
crashed because the worker (gpt-5.5) returned `report` as a JSON **object** and `apply` called
`.strip()` on it — but the crash is a symptom. The root question, raised by the operator: **is JSON
the right format for these hand-offs at all?**

The evidence says no, for the channels that carry authored content:
- **Format restriction degrades reasoning.** *"Let Me Speak Freely?"* (Tam et al., arXiv 2408.02442)
  measures **10–30% reasoning degradation** under JSON-mode vs. free-form, because constrained
  decoding can force the model to emit answer fields **before it finishes reasoning**. The mitigation
  is **reason-in-natural-language-first, then format** (field order matters too).
- **Models are specifically bad at code/markdown inside JSON** (aider, 2024-08-14): they produce
  better artifacts returned as markdown text than JSON-wrapped, because escaping
  newlines/quotes/backticks is error-prone *and* a reasoning tax. Malformed JSON (bad escaping, type
  mismatches) is a leading cause of agent failures in production.
- **The nuance** (the consensus across the surveys): plain-text/markdown wins for *reasoning + content
  the model authors*; a keyed format (JSON/YAML) earns its keep for *multiple entities needing
  unambiguous attribution* or a strict downstream schema.

Our worker hand-off is the textbook-worst JSON case: **a prose `report` plus a markdown `delta` with
fenced `check` blocks**, authored by a reasoning-intensive worker. JSON there is not just risking the
parse crash — by this research it is plausibly **degrading the delta itself**. And the channel is the
**single most important artifact in the system**, in its least legible form — against hypercore's own
legibility-is-king and writing-for-the-machine standards. The ENVELOPE is even annotated as "the one
authored residue… the reply shape the transport parses": the seam built to be reconsidered.

## scope — all six hand-offs
Every channel that parses a model reply, two shapes among them:
- **authored content** — worker `{report, delta}`, architect conversation `{say, done}`, integrate
  verdict `{say, done}`. The research's plain-text zone.
- **structured records** — design candidate `{interface, hides, seam, depth}`, design selection
  `{chosen, hybrid, reasoning, comparison{…}, stake}`, grilling `{questions: [{q, lean, flip}]}`. The
  multi-entity-attribution zone where a keyed format is defensible.
A format for "all hand-offs" must serve both, or pick per shape — the load-bearing decision below.

## the design choice → design-it-twice the format (the `transport` envelope+parse seam)
The model-reply envelope and the shared parse are a load-bearing interface; the format is designed as
a contest of candidates and picked machine-side on depth, locality, and seam placement. The standing
question the contest resolves: **one uniform non-JSON format for every channel** (uniformity, one
parser, full legibility — if it can carry the record-shaped channels' attribution), **vs. a
shape-aware split** (plain-text for content, a keyed format for records — faithful to the research's
nuance, at the cost of two formats). The pick + grounds are recorded as material on the contest node
(`design-decision.md`). H3 robustness (a malformed/unexpected reply surfaces, never crashes) falls out
of the chosen parser for free — the crash that started this is dissolved, not patched.

## folding condition
- the model→engine hand-offs use the chosen format across all six channels (or per the recorded
  per-shape split); `transport` renders the envelope and parses it through one tolerant seam that takes
  authored content **verbatim** (no escaping) and surfaces a missing required field rather than
  crashing — the `report-as-object` failure class is gone by construction;
- the format pick and its grounds (depth, locality, seam placement; why uniform or per-shape) are
  recorded as a structured design decision, material on the contest node;
- `python3 -m engine --check` carries an acceptance check that a worker reply carrying a markdown delta
  (with fenced `check` blocks) and a non-trivial report round-trips through the parse without loss and
  without a crash, and is green.
