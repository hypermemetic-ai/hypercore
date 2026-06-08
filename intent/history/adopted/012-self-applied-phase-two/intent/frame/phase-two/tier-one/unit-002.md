# tier-one implementation acceptance - unit-002

reviewer: tier-one-unit-002-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit-002 diff matches the signed frame obligation: it moves implement/archive contract text into re-read gate files, leaves only dynamic context inline, reconciles intent-edit/adoption semantics, updates targeted intent and machine statements, and adds check assertions for the contract and inline-prompt absence.
Evidence: `012-self-applied-phase-two/intent/frame/signoff.md` is signed by `qqp-dev`; `phase-two/handoffs/unit-002.md` reports `./check.sh` green; `phase-two/diffs/unit-002.diff` shows changes to `adapter/gates/implement.md`, `adapter/gates/archive.md`, `adapter/loop.sh`, `check.sh`, `intent/active-work.md`, `intent/loop.md`, `intent/adapter.md`, and their machine statements.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 012-self-applied-phase-two
Node: .
Unit: unit-002
Proof obligation: Relocate the inline gate prompts into the re-read gate files, reconcile them, and make the bounded `active-work` clarification. Move the contract-bearing implement and archive prompt text out of the inline strings in `adapter/loop.sh` (`run_unit_build_attempt`, `cmd_execute`) into `adapter/gates/implement.md` and `adapter/gates/archive.md`, which `run_gate` re-reads per invocation via `cat`, leaving only dynamic per-unit data (unit id, proof obligation, decision line) inline — so a loop-self-change's prompt edits take effect mid-run and the inline bootstrap floor is gone. Reconcile while moving: the implement gate permits a unit to edit intent when the unit's own proof is a check over that intent (removing the blanket "do not edit the intent documents" prohibition that contradicts `intent/loop.md`'s vertical-slice statement); the archive gate adopts — verifies the applied delta against the signed frame, stamps each touched segment foot, and records history — rather than requiring a separate content-fold of intent the units already applied. Clarify in `intent/active-work.md` that intent a signed work node applies in place during phase two is in-flight, not adopted; adoption is the act that stamps the operator's endorsement and records history, making the change adopted-current, and "the parent intent remains current until adoption" governs adopted truth, consistent with the loop's existing in-flight-vs-adopted concurrency reading. Update the `loop` and `adapter` intent and machine statements to match, and add `check.sh` assertions encoding (a) the reconciled contract and (b) that no contract-bearing implement/archive prompt remains frozen inline in `loop.sh` — so neither the self-contradiction nor the inline floor can silently return. `./check.sh` is green at the unit boundary.
Signed frame directory: 012-self-applied-phase-two/intent/frame
Unit handoff: 012-self-applied-phase-two/intent/frame/phase-two/handoffs/unit-002.md
Unit diff record: 012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-002.diff
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
RATIONALE: The unit-002 diff matches the signed frame obligation: it moves implement/archive contract text into re-read gate files, leaves only dynamic context inline, reconciles intent-edit/adoption semantics, updates targeted intent and machine statements, and adds check assertions for the contract and inline-prompt absence.
EVIDENCE: `012-self-applied-phase-two/intent/frame/signoff.md` is signed by `qqp-dev`; `phase-two/handoffs/unit-002.md` reports `./check.sh` green; `phase-two/diffs/unit-002.diff` shows changes to `adapter/gates/implement.md`, `adapter/gates/archive.md`, `adapter/loop.sh`, `check.sh`, `intent/active-work.md`, `intent/loop.md`, `intent/adapter.md`, and their machine statements.
