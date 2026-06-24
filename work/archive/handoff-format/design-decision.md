# design-it-twice: the model→engine hand-off format [machine]

A load-bearing interface — the format every model reply uses to cross into the engine, and the one
`transport` seam that parses it — designed as a contest of four candidates, each briefed to shape the
*same* interface differently, judged on depth, locality, and seam placement. The decision spans all six
channels: the worker `{report, delta}`, the architect `{say, done}`, the integrate verdict, the design
candidate `{interface, hides, seam, depth}`, the design selection `{chosen, hybrid, reasoning,
comparison, stake}`, and the grilling `{questions:[{q, lean, flip}]}`.

design-decision: the model→engine hand-off format → uniform tag-delimited envelope (minimize-the-interface), hybridized with reason-first field ordering (common-caller) — one tolerant tag scanner in `transport` takes authored content verbatim (no escaping) and nested/repeated tags carry the record-shaped channels' attribution, so a single non-JSON format serves every channel; JSON is retired from model-reply parsing and the report-as-object crash class is structurally impossible.

## The crux the contest turns on
The worker's `delta` is markdown carrying `##`/`###`/`####` headers and fenced ` ```check ` blocks.
Any delimiter must not collide with those, and the authored content must round-trip **verbatim** — the
JSON-escaping of exactly this content is what degrades the artifact (aider) and what crashed the run.
Tag sentinels (`<delta>…</delta>`) are collision-safe: markdown content essentially never emits a
closing `</delta>`. The second axis: the record channels (design selection, grilling) need
**unambiguous attribution** of multiple entities — the one place the research still favors a keyed
format. The contest's real question is whether one format can serve both shapes.

## The contest

- **minimize the interface → uniform tag-delimited.** One `transport.read(raw, schema)` tolerant tag
  scanner: a field is `<name>verbatim inner</name>`; a repeated `<name>` collects to a list; nested
  tags parse to a sub-record. Each role declares a tiny field schema; the same schema renders the
  envelope instruction. **Deepest interface** (one parser hides all delimiter/verbatim/list/nesting/
  tolerance logic; every role a few-line reader), best locality (format knowledge stays in `transport`),
  seam on the existing `transport.parse` boundary. Tags carry **both** verbatim content (the worker's
  markdown delta passes through untouched) **and** records (nested/repeated tags = attribution), so it
  dissolves the uniform-vs-shape-aware tension instead of trading it. Cost: a small hand-rolled tag
  scanner replaces stdlib `json` — held to a minimal subset (no attributes/namespaces/XML library) so
  it cannot grow a dependency.
- **maximize flexibility → per-field extractor toolkit.** `field(raw,name)`, `records(raw,name,subs)`,
  `flag(raw,name)` — a toolkit each role composes, free to mix JSON where it likes. Absorbs every
  channel's shape. **Decided against**: the "which extractor / which format" knowledge leaks to all six
  callers (the information-leakage red flag, a locality leak), and every channel's shape is *fixed* — no
  caller needs the runtime flexibility it buys.
- **optimize the common caller → prose-first body + sentinel payload, JSON tail for records.** Treats
  the worker (and the architect `say`) as the dominant case: free-prose report first (reason-first),
  then the delta in one sentinel region; record channels keep a **minimal JSON tail** after a prose
  preamble. **Decided against as the whole answer**: a split-brain seam — two formats the transport must
  both know, and the record channels keep JSON's escaping brittleness for nested `comparison`/`questions`
  that tags carry cleanly. But its **reason-first ordering** is the research's actual mitigation, lifted
  into the pick as a held constraint.
- **ports-and-adapters → a `ReplyFormat` port + `JsonReply`/`TaggedReply` adapters.** Roles depend on a
  port; the format is swappable at runtime. **Decided against**: over-built against the depth bar — a
  whole protocol + adapters for a variation that does not vary (we want to *delete* JSON, not abstract
  over it), the same red flag the `worker-build-reaches-main` "ports" candidate hit.

## The pick — why this is deepest

**Format (from minimize).** A uniform tag-delimited envelope. Authored content lives in `<report>…
</report>`, `<delta>…</delta>`, `<say>…</say>` and is taken **verbatim** — no unescaping, so the
worker's `delta` (with its `##` headers and ` ```check ` fences) round-trips losslessly and the
`report-as-object` crash is structurally impossible (inner text is text, never typed-then-`.strip()`ed).
Record channels nest: `<questions><question><q>…</q><lean>…</lean><flip>…</flip></question>…</questions>`
— repeated tags to a list, nested tags to sub-records, attribution unambiguous. One format, both shapes.

**Ordering (from common-caller).** Every envelope lists prose/reasoning fields **before** answer/flag
fields (`<report>` before `<delta>`; a `<reasoning>` before `<chosen>`), so the model reasons in
natural language first and the structured answer follows — the *"Let Me Speak Freely?"* mitigation made
structural, recovering the 10–30% reasoning headroom JSON-mode spent.

**Seam (the existing boundary).** Every role already depends on `transport` downward; the change is the
format *inside* `transport.read`/render, not the seam's location. `json`, `_object`, `parse_object`, and
the lenient `{say,done}` fallback leave model-reply parsing entirely.

## Held constraints
- **verbatim content, collision-safe delimiter** — inner tag text is exact; `<delta>` never collides
  with markdown headers or ` ``` ` fences, so the most important artifact round-trips losslessly.
- **tolerant + H3** — the scanner takes inner text, collects repeats to a list, recurses nested tags;
  a missing **required** field raises `MalformedReply` (→ the recover/decision path), never a crash and
  never a silent `{done:True}`. A reply with no tags at all degrades to "the whole text is the prose
  body" (right for the architect answering in prose).
- **minimal tag subset** — a deliberately small hand-rolled scanner, no attributes/namespaces/XML
  library; the interface stays tiny and the complexity pulls downward into `transport`.
- **reason-first ordering** — reasoning/content fields precede answer/flag fields in every envelope.

## Recorded risk (machine-side, not escalated)
A hand-rolled tag scanner is new parsing code where `json` was free; it must handle unclosed tags,
unexpected nesting, and a model that wraps tags in stray prose. Mitigated by the tolerant contract
(scan-and-surface, never crash) and a round-trip acceptance check (a markdown delta with fenced check
blocks in, the same bytes out). No operator-facing stake crosses — the format is **below the contract**
(the operator's trust anchor is "the worker hands a result the architect integrates," not the wire
format); operator-visible behavior is unchanged and the change is reversible — so the pick stays
machine-side, no card (design-it-twice: the interface shape does not spend the operator's go).

## Carries forward (the contract for the build)
`transport` grows a tag envelope: `instruction(schema) -> str` (the reply instruction the role's
prompt carries — named `instruction`, not `render`, to avoid colliding with the `render` module, a
collision the review's import-cycle scan reads as a false dependency edge) and `read(raw, schema) ->
dict` (the one tolerant scanner), with `emit(schema, values) -> str` its inverse for the fixtures. Each of the six channels swaps its JSON
ENVELOPE for a tag schema, reason-first; `parse`/`parse_object`/`_object` and `import json` leave
model-reply parsing. The acceptance check round-trips a worker reply (markdown delta with check blocks +
a non-trivial report) through `read` with no loss and no crash, and exercises a missing-required-field
surfacing. *Bootstrap note: this is the worker hand-off the autonomy loop rides and the seam that just
crashed it, so its first build is freehand outside the loop — like `worker-build-reaches-main` and the
re-verify keystone — never dispatched to a fenced worker that would hand back through the very format
being replaced.*
