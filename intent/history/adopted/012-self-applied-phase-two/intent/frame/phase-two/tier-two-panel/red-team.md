# tier-two implementation acceptance - red-team

reviewer: panel-red-team
Verdict: FLAG
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The signed frame requires the mid-run gate-prompt re-read self-test, but the current built worktree contains that `check.sh` hunk without matching accepted unit diff, handoff, or tier-one evidence. That makes the phase-two evidence stale/mismatched.
Evidence: `./check.sh` exited 0. `git diff -- check.sh` shows `gate_prompt_*`, `HYPERCORE_DYNAMIC_GATE_PROMPT_MARKER_$$`, and “archive gate prompt reflects the mid-run gate file edit”; `rg` over `012-self-applied-phase-two/intent/frame/phase-two/{diffs,handoffs,tier-one}` finds no matches. `012-self-applied-phase-two/intent/frame/phase-two/tier-two-panel/independent-coherence.md` already records `Verdict: FLAG` for the same stale/mismatched evidence.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict FLAG with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier two one-way panel
Work: 012-self-applied-phase-two
Node: .
Lens: red-team
Signed frame directory: 012-self-applied-phase-two/intent/frame
Active work path: 012-self-applied-phase-two
Phase-two acceptance directory: 012-self-applied-phase-two/intent/frame/phase-two

Read only the signed frame, the intent it references, the built worktree state, and phase-two acceptance artifacts.
For the red-team lens, look for bypasses, overclaims, stale artifacts, route mismatch, and ways the work could pass checks while failing the operator-signed acceptance.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, unresolved, or mismatched.

Treat uncertainty, missing evidence, unresolved tier-one flags, or mismatch with the signed frame as FLAG.

## raw output

VERDICT: FLAG
RATIONALE: The signed frame requires the mid-run gate-prompt re-read self-test, but the current built worktree contains that `check.sh` hunk without matching accepted unit diff, handoff, or tier-one evidence. That makes the phase-two evidence stale/mismatched.
EVIDENCE: `./check.sh` exited 0. `git diff -- check.sh` shows `gate_prompt_*`, `HYPERCORE_DYNAMIC_GATE_PROMPT_MARKER_$$`, and “archive gate prompt reflects the mid-run gate file edit”; `rg` over `012-self-applied-phase-two/intent/frame/phase-two/{diffs,handoffs,tier-one}` finds no matches. `012-self-applied-phase-two/intent/frame/phase-two/tier-two-panel/independent-coherence.md` already records `Verdict: FLAG` for the same stale/mismatched evidence.
