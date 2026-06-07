# tier-one implementation acceptance - unit-004

reviewer: tier-one-unit-004
Verdict: PASS
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict returned PASS

## prompt

Implementation-acceptance reviewer: tier one
Work: 009-operator-acts
Node: .
Unit: unit-004
Proof obligation: Align adapter prose, gate prompts, methodology prose, and proof checks with the new operator-act contract; remove `OPERATOR-ACTS-FINDINGS.md`; leave parent intent document amendments for the archive gate to fold and stamp from this signed frame.
Signed frame directory: 009-operator-acts/intent/frame
Unit handoff: 009-operator-acts/intent/frame/phase-two/handoffs/unit-004.md
Unit diff record: 009-operator-acts/intent/frame/phase-two/diffs/unit-004.diff
Mechanical check immediately before this reviewer: check.sh green

Read only the signed frame, the intent it references, the unit handoff, and the unit diff record.
The unit diff record is a cumulative worktree snapshot after this unit, so it may include other already-built or planned unit changes. Check whether the handoff and proof-obligation-relevant diff content make this unit a proof-advancing delta toward the operator-signed acceptance; do not flag solely because unrelated cumulative diff hunks are present.
Return exactly one line:
PASS
or
FLAG

Treat uncertainty, missing evidence, or mismatch with the signed frame as FLAG.

## raw output

PASS
