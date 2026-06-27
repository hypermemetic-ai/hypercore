---
kind: decide
state: settled
owner: operator
created: 1782533582
---
no trail — re-run the mechanism

settled — the refusal was a gate **false-negative**, not a real missing trail. The scenario gate reads the
fork base as `HEAD~1`, which holds only when the worker adds exactly one commit (the scripted harness
transport). The live **codex** agent self-commits its build, then `_record` adds a second commit, so
`HEAD~1` lands on codex's already-built tip → "the scenarios already passed at the fork base." The build
is correct — `python3 -m engine --check` passes on the fence tip (`6a9c992`) — and was folded manually
off that verified tree. Re-running would only repeat the bug; the fork-base seam defect is filed
separately for a proper fix (operator, 2026-06-26).
