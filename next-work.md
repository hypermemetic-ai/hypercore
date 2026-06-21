# next work

## Done — the worker's spec grounding (landed with slice 5, 2026-06-21)

The slice-4 worker was built **slice-confined** (`worker.context` returned only the touched
capabilities) — the error build-handoff §9 names by name, and a violation of rebuild-spec
§6.4 (the worker is the role with full scan access, whose rescan catches the
conversationalist's mis-mapping). Corrected: `worker.context` now returns the **whole spec**
with the touched capabilities flagged as grounding; `worker.prompt` foregrounds the grounding
and carries the rest for the rescan; the `worker` spec requirement was MODIFIED to drop "its
context is exactly those capabilities" and assert full scan + the mis-mapping rescan. The
`_slice4` check now proves non-confinement and the mis-mapping keystone.

## Considered and declined — do not re-propose

Making handoff §9 ("do not re-introduce these errors") into an enforced pre-fold checklist
was raised and **declined** by the operator (2026-06-21): §9 is a bootstrap artifact — the
errors that tempted across the spec's revision rounds — not the critical invariant set, so it
is not worth hardening, and a checklist of named errors buys false comfort against the gap
that actually matters (unsurfaced, *un*-named drift). The real defenses against that gap are
the worker fix above (restoring the §6.4 keystone — a second role with full scan the first
can't suppress) and the architecture review (slice 6, a standing adversarial scan rendered to
the operator). Knowing §9's errors exist is enough.

## Next — slice 6 (the architecture review render)

The standing review (rebuild-spec §7.4) producing the operator view's **upper levels**
("what the system is" at each altitude) and the deepening backlog — vision beside as-built,
debt marked, read without reading code. One thread to pick up from slice 5: the acceptance
harness `hyper/check.py` is over the line-count budget and is the first candidate for the
per-slice split the deep-module discipline asks for (ADR 0004).
