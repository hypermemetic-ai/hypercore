# next work — correct the worker's spec grounding

A fix-forward queued from the slice-4 session (2026-06-21), to do in a **fresh
session** before or alongside slice 5. Read this, then `hyper/worker.py` and the
`worker` capability in `spec/worker/spec.md`.

## The finding

Slice 4 built the worker **slice-confined**: `worker.context` returns only the
capabilities the handed delta names. This is the error the build handoff §9 names
outright — *"Agents are not slice-confined. (Do not revert to 'the worker is confined
to one capability slice.')"* — and it breaks the keystone in rebuild-spec §6.4: the
worker is the role with **full scan access**, and its rescan *"catches both mis-mapping
and any drift"* in the conversationalist-authored delta. A touched-only worker trusts
the delta's capability list and so cannot catch a mis-mapping; it also cannot author a
sound delta, which §4.1 says *"cannot be established from one capability in isolation."*

The over-sharing worry (a real 2026 failure mode) does not bite here: the whole `spec/`
is a few hundred lines of high-signal markdown. §6.3 controls over-sharing *"by the spec
being high-signal and scannable, not by hard slice-walls."* The corpus that is cheap to
read is the corpus that is low-noise — the two reasons the methodology bets on full scan.

## The change

- `hyper/worker.py` — `context` returns **all** capabilities, with the touched ones
  flagged as the grounding/focus; `prompt` foregrounds the touched slice and carries the
  rest as scan context. "Grounded in its slice" means foreground emphasis, not exclusion.
- The delta it carries — **MODIFY** the `worker` requirement *"a worker is grounded in
  its capability's spec slice, by construction"*: it is grounded in the touched
  capabilities **and holds full scan access to the whole spec**; its rescan verifies the
  handed delta against the whole spec and catches mis-mapping. (Drop "its context is
  exactly those capabilities.")
- `hyper/check.py` `_slice4` — change the assertion from "context is *exactly* the
  touched capabilities" to: the context **contains** the touched slice **and** the
  untouched capabilities (proving non-confinement); add a case where the handed delta
  **mis-names** a capability and the worker's rescan **catches** it (the keystone).

## Acceptance

Slices 1–4 still pass; the worker's context contains the whole spec with the touched
capabilities marked as grounding; a mis-mapped handed delta is caught by the worker's
rescan, not trusted.
