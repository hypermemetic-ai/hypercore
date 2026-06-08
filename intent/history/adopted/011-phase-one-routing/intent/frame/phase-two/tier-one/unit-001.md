# tier-one implementation acceptance - unit-001

reviewer: tier-one-unit-001-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
Evidence: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 011-phase-one-routing
Node: .
Unit: unit-001
Proof obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.
Signed frame directory: 011-phase-one-routing/intent/frame
Unit handoff: 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
Unit diff record: 011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
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
RATIONALE: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
EVIDENCE: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.
