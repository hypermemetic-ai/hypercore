# tier-two implementation acceptance - independent-coherence

reviewer: panel-independent-coherence
Verdict: FLAG
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The semantic route is broadly coherent, but the phase-two evidence is stale/mismatched: the current built `check.sh` contains the signed frame’s dynamic gate-prompt self-test, while the final accepted unit diff and tier-one evidence do not cover that hunk. Under the lens instruction, stale or mismatched acceptance evidence must flag one-way adoption.
Evidence: `./check.sh` exits 0; all four `phase-two/tier-one/unit-*.md` artifacts are PASS/real-source. But `diff -q <(git diff) <(awk ... unit-004.diff)` reports a difference, and `git diff -- check.sh` includes `gate_prompt_*`, `HYPERCORE_DYNAMIC_GATE_PROMPT_MARKER_$$`, and “archive gate prompt reflects the mid-run gate file edit”; `rg` finds those only in current `check.sh`, not in `012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-*.diff`, handoffs, or tier-one evidence. `tier-one/unit-004.md` evidence covers only execute auto-detect, while the signed frame’s observable acceptance requires the mid-run gate-prompt self-test.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict FLAG with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier two one-way panel
Work: 012-self-applied-phase-two
Node: .
Lens: independent-coherence
Signed frame directory: 012-self-applied-phase-two/intent/frame
Active work path: 012-self-applied-phase-two
Phase-two acceptance directory: 012-self-applied-phase-two/intent/frame/phase-two

Read only the signed frame, the intent it references, the built worktree state, and phase-two acceptance artifacts.
For the independent-coherence lens, perform the semantic sweep judgement for one-way adoption; do not claim to solve semantic indexing.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, unresolved, or mismatched.

Treat uncertainty, missing evidence, unresolved tier-one flags, or mismatch with the signed frame as FLAG.

## raw output

VERDICT: FLAG
RATIONALE: The semantic route is broadly coherent, but the phase-two evidence is stale/mismatched: the current built `check.sh` contains the signed frame’s dynamic gate-prompt self-test, while the final accepted unit diff and tier-one evidence do not cover that hunk. Under the lens instruction, stale or mismatched acceptance evidence must flag one-way adoption.
EVIDENCE: `./check.sh` exits 0; all four `phase-two/tier-one/unit-*.md` artifacts are PASS/real-source. But `diff -q <(git diff) <(awk ... unit-004.diff)` reports a difference, and `git diff -- check.sh` includes `gate_prompt_*`, `HYPERCORE_DYNAMIC_GATE_PROMPT_MARKER_$$`, and “archive gate prompt reflects the mid-run gate file edit”; `rg` finds those only in current `check.sh`, not in `012-self-applied-phase-two/intent/frame/phase-two/diffs/unit-*.diff`, handoffs, or tier-one evidence. `tier-one/unit-004.md` evidence covers only execute auto-detect, while the signed frame’s observable acceptance requires the mid-run gate-prompt self-test.
