---
kind: ask
state: standing
owner: operator
created: 2026-06-23
---
# requirement-rename-op — a delta operation that changes a requirement's title in place

The first full live crossing (2026-06-23, `operator-view-readiness`) surfaced a gap in the delta
grammar. A requirement's **identity is its title** — the text after `### Requirement:`, matched exact
(`spec.py:42`) — so MODIFIED, which looks a requirement up by that title and replaces its body and
scenarios, **cannot change the title itself**. A MODIFIED carrying a new title finds no match and the
fold refuses it ("MODIFIED requirement is absent").

The live worker (gpt-5.5) hit exactly this: it broadened a requirement's scope and retitled it to
match (`the operator view renders vision beside as-built and gap` → `…as-built, readiness, gap, and
complexity debt`). Reasonable authoring — the requirement genuinely grew, so its title grew — but the
format has no verb for an in-place retitle, so the broadened MODIFIED read as targeting a requirement
that does not exist, and the gate refused at the non-negotiable delta-applies condition.

hypercore's delta grammar carries ADDED / MODIFIED / REMOVED (`spec/self-model.md`, `engine/delta.py`)
but **no RENAMED** — the one OpenSpec carries that we don't, and precisely the verb a scope-broadening
retitle needs. Without it a retitle has no clean home: REMOVE-old + ADD-new loses the "same
requirement, evolved" intent and reads as two unrelated changes, and a worker that naturally writes
MODIFIED-with-new-title falls through the gate non-deterministically. A model trained on these
conventions expects the verb.

Provenance: the first full autonomous crossing (`operator-view-readiness`), gate-refused at the
delta-applies condition (commit trail `aacc396…a7082b6`). The pending `operator-view-readiness`
decision card cites the same run; this ask is the general grammar fix, independent of that node's
re-dispatch.

## grilling — resolved (2026-06-23)
- **approach → a fourth delta verb, RENAMED** (mirror OpenSpec) — not an extended MODIFIED nor
  worker-coaching alone. The clean home for a retitle, the convention a model already expects, each
  verb's job kept sharp.
- **rename scope → title only** — RENAMED changes identity; a paired MODIFIED keyed on the new title
  carries the body. Orthogonal ops, one concern each. This introduces a coupling the architect
  resolves machine-side and the delta records: within one delta the renames resolve **before** the
  modifies, and `check` validates a MODIFIED/REMOVED against the **post-rename** names — so a
  RENAMED(old→new) + MODIFIED(new) pair folds as one act.

## contract
A delta can rename a requirement in place. **RENAMED** is a fourth verb beside ADDED / MODIFIED /
REMOVED, written `## RENAMED — <capability>` with a `### Requirement: <old title>` block carrying a
`→ <new title>` line. It changes only the requirement's **title** — its identity — the body and
scenarios untouched. A scope-broadening retitle is a RENAMED paired with a MODIFIED keyed on the new
title; within one delta renames resolve first, so the modify finds its target. Refusals follow the
existing discipline: a rename of an absent old title, or onto a title that already exists, cannot fold
and leaves the spec untouched; a re-applied rename (old gone, new present) is the idempotent retry.
The rename lands in the fold's one atomic act with the spec change and the node archive, on the
single-writer line, like every other op. The spec delta this realizes is the grilling pass's `[DELTA]`
(`grilling.md` beside this file — the artifact the crossing hands the worker).

## folding condition
- the delta grammar carries RENAMED — `delta.parse` reads it, `delta.check` validates it (an absent
  old title and a colliding new title refuse; an idempotent re-apply passes), and `delta._apply`
  retitles in place, with renames resolving before modifies in the same delta;
- a scope-broadening retitle (RENAMED + MODIFIED-on-new-title) folds in one atomic act — the
  requirement lands under its new title with the modified body, the old title gone;
- the behavior is recorded in `spec/self-model.md` and `python3 -m engine --check` carries the rename
  scenarios (`renamed`, `renamed-modified`, the unfoldable-rename cases) green;
- the worker-facing delta grammar (`worker.ENVELOPE` and `spec/worker.md`) names RENAMED, so a worker
  writes a retitle correctly instead of the MODIFIED-with-new-title the gate refused on the live run.
