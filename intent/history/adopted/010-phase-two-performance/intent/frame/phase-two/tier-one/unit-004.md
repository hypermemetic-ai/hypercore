# tier-one implementation acceptance - unit-004

reviewer: tier-one-unit-004
Verdict: PASS
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict returned PASS

## prompt

Implementation-acceptance reviewer: tier one
Work: 010-phase-two-performance
Node: .
Unit: unit-004
Proof obligation: Resumable execute cache: add a signed-frame-derived per-unit cache key covering the frame, unit proof obligation, relevant prior-unit state, loop implementation version, diff/check evidence, and tier-one PASS; on rerun, skip unchanged accepted units, rebuild cache misses, and invalidate downstream units when prior state changes; prove skip and invalidation behavior in `./check.sh`.
Signed frame directory: 010-phase-two-performance/intent/frame
Unit handoff: 010-phase-two-performance/intent/frame/phase-two/handoffs/unit-004.md
Unit diff record: 010-phase-two-performance/intent/frame/phase-two/diffs/unit-004.diff
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
