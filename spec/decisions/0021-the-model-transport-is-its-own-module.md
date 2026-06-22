# ADR 0021 — the model transport is its own module

Status: **operator-directed** (2026-06-21) — asked how the coherence arc should handle the transport
leakage the red-flag scan flags, the operator chose "name the transport now" over flag-and-park; the
machine-side extraction is below. [machine]

## Context

The architect's voice (`conversation`), the worker (`worker`), the grilling pass (`grill`), and the design
contest (`design`) all need the same two operations: one `claude -p` call to the model, and one lenient
read of the first JSON object from its reply. Those two lived as **privates of `conversation`**
(`conversation._claude`, `conversation._parse`), and the other four modules reached **through
`conversation`'s interface into its underscore internals** to get them — five modules past one module's
public surface, the information-leakage red flag (depth.md's gravest after shallowness). It also made
`conversation` and `grill` **depend on each other** (`conversation` needs `grill` to run a pass; `grill`
reached back for the transport) — the circular dependency the new mechanical red-flag scan (ADR 0020)
flags.

`conversation` was silently the home of an un-named capability — the **transport** (the model call, the
JSON read, the model identity) — that does not belong to "the architect's voice."

## Decision

**Name the transport: `engine/transport.py`.** It holds the one `claude -p` `call`, the lenient `parse`,
and the model identity (`MODEL`, `MODEL_LABEL`). `conversation`, `grill`, `design`, and `worker` each
depend on it **downward** (taking `call` and `parse` from it); `window` and `preview` read
`transport.MODEL_LABEL`. With the transport named:

- the `conversation ↔ grill` cycle dissolves — `grill` no longer reaches into `conversation`;
- no module reaches past another's interface for the model call;
- the transport stays **injectable** (the scripted fake the acceptance harness drives), unchanged.

This was the operator's call between **fixing** the finding now and the lighter **flag-and-park** (a
structured red-flag acceptance, deferring the extraction). The operator chose to fix it, which lets the
move-2 scan (ADR 0020) read genuinely green rather than green-modulo-an-accepted-exception.

## Grounds

A deep module named once and depended on downward is the textbook dissolution of both an
information-leakage smell and a circular dependency in one move — and a near-net structural win: the model
call, the JSON read, and the model identity lifted out of `conversation` into a module with a far smaller
interface than the surface that was being reached through. The acceptance harness is green; the red-flag
scan reads no cycle and no reaching-through-privates for these names.

## Relation

- **Resolves the naming/structure residue** the coherence audit recorded
  (`work/archive/coherence-audit/`): "name the transport" was its recommended option.
- **Companion to ADR 0020**: the scan flags the cycle; this extraction is the fix that makes it green.
- **Touches ADR 0009's channels framing** only in passing: the model identity (`MODEL_LABEL`) the window
  and preview render now comes from `transport`, not `conversation`.
