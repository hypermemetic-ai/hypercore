# tier-two implementation acceptance - proof-integrity

reviewer: panel-proof-integrity
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The signed frame’s proof-integrity claims are supported by real-source unit evidence: all four units have accepted records, handoffs, diff records, and real-reviewer tier-one PASS artifacts; the built worktree contains the claimed snapshot safety, prompt relocation/reconciliation, cache soft-miss handling, and execute auto-detect changes; and fresh mechanical checks are green. The absent cache-key files are consistent with the new soft-miss contract, not relied on as correctness proof.
Evidence: `012-self-applied-phase-two/intent/frame/signoff.md`; `012-self-applied-phase-two/intent/frame/phase-two/units/unit-001.md` through `unit-004.md`; `handoffs/unit-001.md` through `unit-004.md`; `diffs/unit-001.diff` through `unit-004.diff`; `tier-one/unit-001.md` through `unit-004.md` all record PASS, `source: real-reviewer`, `dry-run: no`; fresh `bash -n adapter/loop.sh`, `bash -n check.sh`, `git diff --check ...`, and `./check.sh` all exited 0; `check.sh` includes passing assertions for snapshot survival, re-read gate prompts, proof-required intent edits, cache-record soft miss/rebuild, and execute auto-detect.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier two one-way panel
Work: 012-self-applied-phase-two
Node: .
Lens: proof-integrity
Signed frame directory: 012-self-applied-phase-two/intent/frame
Active work path: 012-self-applied-phase-two
Phase-two acceptance directory: 012-self-applied-phase-two/intent/frame/phase-two

Read only the signed frame, the intent it references, the built worktree state, and phase-two acceptance artifacts.
For the proof-integrity lens, check whether the recorded unit handoffs, diffs, mechanical checks, and acceptance artifacts support the proof claims with real-source proof and without dry-run, fake, or stale evidence.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, unresolved, or mismatched.

Treat uncertainty, missing evidence, unresolved tier-one flags, or mismatch with the signed frame as FLAG.

## raw output

VERDICT: PASS
RATIONALE: The signed frame’s proof-integrity claims are supported by real-source unit evidence: all four units have accepted records, handoffs, diff records, and real-reviewer tier-one PASS artifacts; the built worktree contains the claimed snapshot safety, prompt relocation/reconciliation, cache soft-miss handling, and execute auto-detect changes; and fresh mechanical checks are green. The absent cache-key files are consistent with the new soft-miss contract, not relied on as correctness proof.
EVIDENCE: `012-self-applied-phase-two/intent/frame/signoff.md`; `012-self-applied-phase-two/intent/frame/phase-two/units/unit-001.md` through `unit-004.md`; `handoffs/unit-001.md` through `unit-004.md`; `diffs/unit-001.diff` through `unit-004.diff`; `tier-one/unit-001.md` through `unit-004.md` all record PASS, `source: real-reviewer`, `dry-run: no`; fresh `bash -n adapter/loop.sh`, `bash -n check.sh`, `git diff --check ...`, and `./check.sh` all exited 0; `check.sh` includes passing assertions for snapshot survival, re-read gate prompts, proof-required intent edits, cache-record soft miss/rebuild, and execute auto-detect.
