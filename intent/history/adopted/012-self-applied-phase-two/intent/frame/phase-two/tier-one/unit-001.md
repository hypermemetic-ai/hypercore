# tier-one implementation acceptance - unit-001

reviewer: tier-one-unit-001-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit advances the signed frame’s first proof obligation: the diff adds execute-start self re-exec from a copied `adapter/loop.sh`, records the safety contract in `loop` and `adapter` intent plus machine statements, and adds a self-test that edits live `adapter/loop.sh` after snapshot creation while the dry-run execute continues to tier-one PASS. The handoff reports `bash -n adapter/loop.sh`, `bash -n check.sh`, and `./check.sh` passing, matching the stated mechanical green check.
Evidence: `012-self-applied-phase-two/intent/frame/frame.md` unit 1 obligation; `012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-001.md` prepared checks; `012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-001.diff` adds `phase_two_reexec_from_snapshot()`, `HYPERCORE_LOOP_SNAPSHOT_ACTIVE`, `exec "$snapshot_path" "${cmd[@]}"`, snapshot-based loop digest, self-edit survival test in `check.sh`, and matching statements in `intent/loop.md`, `intent/adapter.md`, `intent/machine-statements/loop.md`, and `intent/machine-statements/adapter.md`.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 012-self-applied-phase-two
Node: .
Unit: unit-001
Proof obligation: Add orchestrator self-edit safety. Make `adapter/loop.sh` run phase two from an immutable snapshot of itself (re-exec from a copy at execute start) so a unit that edits `loop.sh` mid-run cannot corrupt the live orchestrator. Record it in the `loop` and `adapter` intent and machine statements, and add a self-test proving a mid-run `loop.sh` edit does not corrupt the active run. `./check.sh` is green at the unit boundary. (First so no later unit edits `loop.sh` before the safety exists; 012's own bootstrap run is launched from a manual snapshot by the supervisor.)
Signed frame directory: 012-self-applied-phase-two/intent/frame
Unit handoff: 012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-001.md
Unit diff record: 012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-001.diff
Mechanical check immediately before this reviewer: check.sh green

Read only the signed frame, the intent it references, the unit handoff, and the unit diff record.
The unit diff record is a cumulative worktree snapshot after this unit, so it may include other already-built or planned unit changes. Check whether the handoff and proof-obligation-relevant diff content make this unit a proof-advancing delta toward the operator-signed acceptance; do not flag solely because unrelated cumulative diff hunks are present.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, or mismatched.

Treat uncertainty, missing evidence, or mismatch with the signed frame as FLAG.

## raw output

VERDICT: PASS
RATIONALE: The unit advances the signed frame’s first proof obligation: the diff adds execute-start self re-exec from a copied `adapter/loop.sh`, records the safety contract in `loop` and `adapter` intent plus machine statements, and adds a self-test that edits live `adapter/loop.sh` after snapshot creation while the dry-run execute continues to tier-one PASS. The handoff reports `bash -n adapter/loop.sh`, `bash -n check.sh`, and `./check.sh` passing, matching the stated mechanical green check.
EVIDENCE: `012-self-applied-phase-two/intent/frame/frame.md` unit 1 obligation; `012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-001.md` prepared checks; `012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-001.diff` adds `phase_two_reexec_from_snapshot()`, `HYPERCORE_LOOP_SNAPSHOT_ACTIVE`, `exec "$snapshot_path" "${cmd[@]}"`, snapshot-based loop digest, self-edit survival test in `check.sh`, and matching statements in `intent/loop.md`, `intent/adapter.md`, `intent/machine-statements/loop.md`, and `intent/machine-statements/adapter.md`.
