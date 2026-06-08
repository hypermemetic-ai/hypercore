# tier-one implementation acceptance - unit-004

reviewer: tier-one-unit-004-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit advances the signed frame’s unit-004 obligation: the loop now states the signed frame’s judgeability floor, adapter and collaboration keep that altitude coherent with lean-frame language, and check.sh adds direct assertions for those statements.
Evidence: `013-two-step-build/intent/frame/frame.md` defines unit-004 and its proof; `013-two-step-build/intent/frame/phase-two/handoffs/unit-004.md` reports `bash -n check.sh`, `git diff --check -- ...`, and `./check.sh` passed; `013-two-step-build/intent/frame/phase-two/diffs/unit-004.diff` adds the judgeability-floor statements to `intent/loop.md`, `intent/adapter.md`, and `intent/collaboration.md`, plus `check.sh` assertions for loop, adapter, collaboration, and adapter machine statements.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 013-two-step-build
Node: .
Unit: unit-004
Proof obligation: Short-but-judgeable frame altitude rule. Add the loop intent statement that the signed frame is held to the floor of judgeability — legible and falsifiable, not implementation-complete; the plan carries implementation-completeness; the panel must be able to FLAG a wrong result against a frame claim without reading code. Keep the collaboration segment's lean-frame language coherent with it. Proof: check.sh asserts the altitude statement is present and coherent across loop, adapter, and collaboration.
Signed frame directory: 013-two-step-build/intent/frame
Unit handoff: 013-two-step-build/intent/frame/phase-two/handoffs/unit-004.md
Unit diff record: 013-two-step-build/intent/frame/phase-two/diffs/unit-004.diff
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
RATIONALE: The unit advances the signed frame’s unit-004 obligation: the loop now states the signed frame’s judgeability floor, adapter and collaboration keep that altitude coherent with lean-frame language, and check.sh adds direct assertions for those statements.
EVIDENCE: `013-two-step-build/intent/frame/frame.md` defines unit-004 and its proof; `013-two-step-build/intent/frame/phase-two/handoffs/unit-004.md` reports `bash -n check.sh`, `git diff --check -- ...`, and `./check.sh` passed; `013-two-step-build/intent/frame/phase-two/diffs/unit-004.diff` adds the judgeability-floor statements to `intent/loop.md`, `intent/adapter.md`, and `intent/collaboration.md`, plus `check.sh` assertions for loop, adapter, collaboration, and adapter machine statements.
