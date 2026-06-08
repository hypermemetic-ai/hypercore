# tier-two implementation acceptance - proof-integrity

reviewer: panel-proof-integrity
Verdict: FLAG
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The built code and tier-one verdicts support structural progress, but proof-integrity is not clean because the accepted phase-two run has no real per-unit plan or plan-match artifacts, while the signed frame’s proof depends on recorded plan-before-build and plan-match-before-build evidence. The remaining proof is dry-run/self-test coverage plus stale run records.
Evidence: `013-two-step-build/intent/frame/phase-two/` contains units, handoffs, diffs, and tier-one artifacts but no `plans/` or `plan-match/` files; `.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/events.jsonl` starts units at `implement-unit-*-fast-*` and records no plan or plan-match gates; `.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/state.json` lacks `plans_dir` and `plan_match_dir`; `check.sh` plan/plan-match order assertions are dry-run/self-test paths; tier-one artifacts are `source: real-reviewer` and `dry-run: no`, but they rely on diffs/check claims rather than real plan/plan-match artifacts for this accepted run.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict FLAG with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier two one-way panel
Work: 013-two-step-build
Node: .
Lens: proof-integrity
Signed frame directory: 013-two-step-build/intent/frame
Active work path: 013-two-step-build
Phase-two acceptance directory: 013-two-step-build/intent/frame/phase-two

Read only the signed frame, the intent it references, the built worktree state, and phase-two acceptance artifacts.
For the proof-integrity lens, check whether the recorded unit handoffs, diffs, mechanical checks, and acceptance artifacts support the proof claims with real-source proof and without dry-run, fake, or stale evidence.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, unresolved, or mismatched.

Treat uncertainty, missing evidence, unresolved tier-one flags, or mismatch with the signed frame as FLAG.

## raw output

VERDICT: FLAG
RATIONALE: The built code and tier-one verdicts support structural progress, but proof-integrity is not clean because the accepted phase-two run has no real per-unit plan or plan-match artifacts, while the signed frame’s proof depends on recorded plan-before-build and plan-match-before-build evidence. The remaining proof is dry-run/self-test coverage plus stale run records.
EVIDENCE: `013-two-step-build/intent/frame/phase-two/` contains units, handoffs, diffs, and tier-one artifacts but no `plans/` or `plan-match/` files; `.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/events.jsonl` starts units at `implement-unit-*-fast-*` and records no plan or plan-match gates; `.hypercore/loop-runs/20260608T062609Z-root-013-two-step-build-pid3177438/state.json` lacks `plans_dir` and `plan_match_dir`; `check.sh` plan/plan-match order assertions are dry-run/self-test paths; tier-one artifacts are `source: real-reviewer` and `dry-run: no`, but they rely on diffs/check claims rather than real plan/plan-match artifacts for this accepted run.
