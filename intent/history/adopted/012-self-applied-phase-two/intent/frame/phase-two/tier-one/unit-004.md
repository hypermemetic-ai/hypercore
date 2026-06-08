# tier-one implementation acceptance - unit-004

reviewer: tier-one-unit-004-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit satisfies the signed frame’s handoff-real obligation by adding execute auto-detection, clear zero/multiple candidate blocking, supervisor-to-executor prose, start/execute distinction, adapter intent and machine-statement coverage, and a focused check.sh self-test.
Evidence: `012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-004.md` reports `bash -n adapter/loop.sh`, `bash -n check.sh`, and `./check.sh` passed; `012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-004.diff` adds `infer_execute_work_name`, updates `cmd_execute` to accept omitted work names, adds zero/single/multiple auto-detect self-tests, updates `adapter/codex.md`, `intent/adapter.md`, and `intent/machine-statements/adapter.md`; the reviewer prompt states the immediate pre-review mechanical check was green.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 012-self-applied-phase-two
Node: .
Unit: unit-004
Proof obligation: Make the handoff real. `loop.sh execute` resolves the single signed, unarchived work node in the addressed node when `<work-name>` is omitted (and blocks with a clear message when zero or more than one exist). Add the Opus->codex launch + supervise path and the `start`-versus- `execute` distinction to `adapter/codex.md` and the `adapter` intent and machine statements, and add a `check.sh` self-test for the auto-detect resolution. `./check.sh` is green at the unit boundary.
Signed frame directory: 012-self-applied-phase-two/intent/frame
Unit handoff: 012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-004.md
Unit diff record: 012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-004.diff
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
RATIONALE: The unit satisfies the signed frame’s handoff-real obligation by adding execute auto-detection, clear zero/multiple candidate blocking, supervisor-to-executor prose, start/execute distinction, adapter intent and machine-statement coverage, and a focused check.sh self-test.
EVIDENCE: `012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-004.md` reports `bash -n adapter/loop.sh`, `bash -n check.sh`, and `./check.sh` passed; `012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-004.diff` adds `infer_execute_work_name`, updates `cmd_execute` to accept omitted work names, adds zero/single/multiple auto-detect self-tests, updates `adapter/codex.md`, `intent/adapter.md`, and `intent/machine-statements/adapter.md`; the reviewer prompt states the immediate pre-review mechanical check was green.
