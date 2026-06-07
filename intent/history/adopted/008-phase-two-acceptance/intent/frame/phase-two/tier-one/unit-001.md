# tier-one implementation acceptance - unit-001

reviewer: tier-one-unit-001
Verdict: FLAG
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict returned FLAG

## prompt

Implementation-acceptance reviewer: tier one
Work: 008-phase-two-acceptance
Node: .
Unit: unit-001
Proof obligation: Frame-field unit: add `observable acceptance` and `excluded interpretation` to loop frame validation, scaffolding, gate prompts, adapter prose, and checks. This frame already includes those sections so the new validation can pass during work `008`.
Signed frame directory: 008-phase-two-acceptance/intent/frame
Unit handoff: 008-phase-two-acceptance/intent/frame/phase-two/handoffs/unit-001.md
Unit diff record: 008-phase-two-acceptance/intent/frame/phase-two/diffs/unit-001.diff

Read only the signed frame, the intent it references, the unit handoff, and the unit diff record.
Check whether this unit is a proof-advancing delta toward the operator-signed acceptance.
Return exactly one line:
PASS
or
FLAG

Treat uncertainty, missing evidence, or mismatch with the signed frame as FLAG.

## raw output

FLAG
