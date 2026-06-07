# tier-two implementation acceptance - whole-acceptance-conformance

reviewer: panel-whole-acceptance-conformance
Verdict: FLAG
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict returned FLAG

## prompt

Implementation-acceptance reviewer: tier two one-way panel
Work: 009-operator-acts
Node: .
Lens: whole-acceptance-conformance
Signed frame directory: 009-operator-acts/intent/frame
Active work path: 009-operator-acts
Phase-two acceptance directory: 009-operator-acts/intent/frame/phase-two

Read only the signed frame, the intent it references, the built worktree state, and phase-two acceptance artifacts.
For the whole-acceptance-conformance lens, check the built worktree and phase-two artifacts against the signed acceptance condition, observable acceptance, excluded interpretation, and route.
Return exactly one line:
PASS
or
FLAG

Treat uncertainty, missing evidence, unresolved tier-one flags, or mismatch with the signed frame as FLAG.

## raw output

FLAG
