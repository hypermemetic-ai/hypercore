# tier-one implementation acceptance - unit-005

reviewer: tier-one-unit-005-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit handoff and proof-relevant diff match the signed frame’s unit-005 obligation: the builder default flips to spark, the old held-builder language is replaced by shipped two-step language in the named intent/adapter surfaces, and `check.sh` is updated to assert the spark default and reject the retired held-builder clauses.
Evidence: `013-two-step-build/intent/frame/frame.md` unit 5 requires this exact flip; `phase-two/handoffs/unit-005.md` reports `./check.sh` exits 0; `phase-two/diffs/unit-005.diff` changes `adapter/loop.sh` default to `CODEX_BUILDER_MODEL:-gpt-5.3-codex-spark`, updates shipped-language hunks in `intent/loop.md`, `intent/machine-statements/loop.md`, `intent/adapter.md`, `intent/machine-statements/adapter.md`, `adapter/codex.md`, and `adapter/claude.md`, and updates `check.sh` `require_text`/`reject_text` assertions for the shipped default and retired held-builder phrases.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 013-two-step-build
Node: .
Unit: unit-005
Proof obligation: Flip the default builder to spark and flip "held until two-step lands" to "shipped." Change the CODEX_BUILDER_MODEL default in adapter/loop.sh from gpt-5.5 to gpt-5.3-codex-spark, update the header comment and the two-step note, and update intent/loop.md, intent/machine-statements/loop.md, intent/adapter.md, intent/machine-statements/adapter.md, adapter/codex.md, and adapter/claude.md so every "builder held at the strong model until two-step lands" clause becomes "two-step has shipped; the default builder is the cheap fast model behind the plan step and plan-match check." Proof: check.sh asserts the builder default token is gpt-5.3-codex-spark and that no "held until two-step lands" clause remains.
Signed frame directory: 013-two-step-build/intent/frame
Unit handoff: 013-two-step-build/intent/frame/phase-two/handoffs/unit-005.md
Unit diff record: 013-two-step-build/intent/frame/phase-two/diffs/unit-005.diff
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
RATIONALE: The unit handoff and proof-relevant diff match the signed frame’s unit-005 obligation: the builder default flips to spark, the old held-builder language is replaced by shipped two-step language in the named intent/adapter surfaces, and `check.sh` is updated to assert the spark default and reject the retired held-builder clauses.
EVIDENCE: `013-two-step-build/intent/frame/frame.md` unit 5 requires this exact flip; `phase-two/handoffs/unit-005.md` reports `./check.sh` exits 0; `phase-two/diffs/unit-005.diff` changes `adapter/loop.sh` default to `CODEX_BUILDER_MODEL:-gpt-5.3-codex-spark`, updates shipped-language hunks in `intent/loop.md`, `intent/machine-statements/loop.md`, `intent/adapter.md`, `intent/machine-statements/adapter.md`, `adapter/codex.md`, and `adapter/claude.md`, and updates `check.sh` `require_text`/`reject_text` assertions for the shipped default and retired held-builder phrases.
