# tier-one implementation acceptance - unit-002

reviewer: tier-one-unit-002
Verdict: PASS
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict returned PASS

## prompt

Implementation-acceptance reviewer: tier one
Work: 010-phase-two-performance
Node: .
Unit: unit-002
Proof obligation: Phase-one review crash and lens-specific proof: fix or harden the phase-one review subprocess path that produced exit-1 base-roster flags, preserve diagnostic output in `review.md`, keep optional reviewers advisory, and prove each tier-two panel lens uses its own live instruction rather than stale copied text.
Signed frame directory: 010-phase-two-performance/intent/frame
Unit handoff: 010-phase-two-performance/intent/frame/phase-two/handoffs/unit-002.md
Unit diff record: 010-phase-two-performance/intent/frame/phase-two/diffs/unit-002.diff
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
