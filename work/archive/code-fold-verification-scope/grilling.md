surfaced: 1

[Q] How wide must a code-bearing fold's re-verify reach on merged main — the touched capabilities the delta names, or the whole system?
lean: The whole system — re-verify every capability's scenarios on merged main, not only the named ones
flip: if a code-bearing fold's re-verify were a large fraction of the crossing's wall-time (it is ~7s against a minutes-long build), the derived dependency-closure scope would earn its drift surface
answer: The whole system

[RESOLVED machine-side — not surfaced]
- The blind spot lives in ONE of the two gates. The in-fence **scenario gate** (`scenario.gate`,
  red→green) is correctly touched-only — only a capability the change *builds* transitions red→green;
  an untouched capability is green at both base and tip, so widening it is meaningless. The
  **re-verify keystone** (`scenario.reverify`) asks a different question — "is merged main green
  here?" — meaningful for every capability. So the fix is the re-verify's scope, not a new mechanism.
- **Completeness wins over throughput — settled by intent + the existing contract, not a fork.** The
  `worker-build-reaches-main` decision scoped re-verify to *touched* as a throughput optimization,
  recorded "no operator-facing stake crosses." The rename-op crossing falsified that: broken code
  reaching main with `done: True` is exactly an operator-facing stake and a breach of that decision's
  own contract ("never a silent broken merge"). Intent settles direction — legibility/trust is king; a
  fold reporting `done` over code it never verified is a lie. Measured cost ~7s on a crossing whose
  worker build alone takes minutes, code folds only (the minority) — immaterial.
- **Candidate 2 (derived module→capability closure) rejected**: a drift surface against
  derive-don't-hand-tend, and the shared core (`tree`/`delta`/`record`/`scenario`) makes the closure
  ≈ the whole system for any engine work anyway — it buys ~6s on a minutes-long, rare operation.
  **Candidate 3 (separate full-`--check` precondition gate) collapses into candidate 1** while
  redundantly re-running the touched caps and dragging in the gate's own red→green self-tests
  (recursion, ~12s). Candidate 1 dominates once the spec discipline and the measurement are applied.

[DESIGN PICK — machine-side material on the contest node]
**Re-verify owns the whole-system scope structurally.** `scenario.reverify` enumerates every capability
from the merged spec at `root` and runs each one's scenarios on the merged tree; the caller
(`delta.fold`) passes no scope at all. The blind spot is then impossible to reintroduce — no caller can
narrow the re-verify the way `delta.fold` narrowed it to `touched`. It reuses the one re-verify seam
(`_run_merged` per capability, the `_GATE_GUARD` recursion skip, the throwaway record sink) unchanged;
only the set of capabilities widens, from the delta's names to all of them. It does NOT reuse the full
`python3 -m engine --check` (which includes the gate's own red→green self-tests that spawn folds/git —
recursion and ~12s); it runs each capability's acceptance scenarios on merged main (~7s), the strongest
whole-system correctness claim that does not self-recurse. The acceptance proof stays out-of-band in
`engine/check/build_reaches_main.py` (watched) — the keystone cannot certify itself from inside a fold,
the same self-reference the existing code-bearing proof carries.

[CONTRACT]
A code-bearing fold's verdict is **green-on-the-system, never green-on-the-touched-capability alone**.
Before the commit, the fold re-verifies **every** capability's scenarios on the merged tree — the whole
system — so a worker that refactors a shared engine module (`tree`, `delta`, `record`, `scenario`)
cannot break an **untouched** capability the delta never named and still land `done`. A build red
anywhere a full `python3 -m engine --check` would catch it is refused: every write rolled back, nothing
landing, the node recovering to a decision — the existing refusal path, now reaching the whole system.
The in-fence red→green **scenario gate** stays scoped to the touched capabilities (only they
transition); the whole-system reach lives in the **re-verify**, where the question "is merged main
green?" is meaningful for every capability. The scope is **structural** — re-verify enumerates the
capabilities itself, so no caller can narrow it and reopen the blind spot. The cost (~7s on a
minutes-long, code-only crossing) is paid for completeness; the dependency-closure narrowing was
rejected as a drift surface that saves nothing for shared-core work. Acceptance: `python3 -m engine
--check` carries a check that a code-bearing fold whose delta names one capability but whose code breaks
a *different, unnamed* one is refused with nothing landing — and is green.

[DELTA]
# delta — a code-bearing fold re-verifies the whole system on merged main, not only the named capabilities

## MODIFIED — self-model

### Requirement: folding lands the verified build's code on the merged tree, not only its spec
The act that folds a **code-bearing** tree MUST land the worker's **verified engine code** on main —
not only its spec delta — in the **same one commit** that applies the delta and archives the node, so a
code-bearing ask completes through the crossing without leaving main red or the node falsely archived.
The code crosses as a self-contained artifact captured at the worker's hand-off — the fence's verified
bytes for the engine paths it touched — content-replayed into the fold's one held act; no live fence is
reached at fold time. Before the commit, **every capability's scenarios are re-verified on the merged
tree — the whole system, not only the capabilities the delta names**: the worker's code can reach a
shared engine module (`tree`, `delta`, `record`, `scenario`) that an **unnamed** capability depends on,
so re-verifying only the touched capabilities would let a shared-module change break an untouched one and
still land `done`. What is verified is the merged main itself, so green-in-fence can no longer mean
red-on-main, and green-on-the-touched-capability can no longer mean red-on-the-system — a build that does
not hold once merged, anywhere a full check would catch it, is refused, every write rolled back, nothing
landing, the node recovering to a decision. The whole-system reach is **structural**: the re-verify
enumerates the capabilities itself, so no caller can narrow it. The in-fence red→green **scenario gate**
stays scoped to the touched capabilities — only a capability the change builds transitions — while the
re-verify is the whole-system check the gate's scope cannot be. A **staleness pre-check** fast-refuses,
before any write, a build whose engine paths main has moved under since the fence was cut — a decision to
re-cut off current main, never a silent clobber. None of these is a new commit, lock, or transaction;
they ride the one held line the spec fold already runs on. A spec-only (trivial or no-code) fold carries
no code and runs none of them — its act is exactly as before.

#### Scenario: a code-bearing delta's implementation reaches main
- WHEN a tree whose worker built and verified engine code in its fence folds
- THEN that engine code lands on main in the same one commit as the spec delta and the node's archive,
  re-verified green on the merged tree before the commit; a build red once merged, or one whose paths
  main has moved under, is refused and nothing lands
- watched — proven from outside in `engine/check/build_reaches_main.py`, never from inside the fold it
  tests (the self-reference the scenario gate's own red→green has, and the same honest home)

#### Scenario: a shared-module change that breaks an untouched capability is refused
- WHEN a code-bearing fold's delta names one capability but its engine code breaks a *different*
  capability the delta never named — a refactor of a shared module an unnamed capability depends on
- THEN re-verifying the whole system on the merged tree catches the untouched capability red, the fold
  is refused, every write rolled back, nothing landing, the node recovering to a decision — the
  crossing's verdict is green-on-the-system, never green-on-the-touched-capability alone
- watched — proven from outside in `engine/check/build_reaches_main.py`, the keystone that cannot
  certify itself from inside a fold
