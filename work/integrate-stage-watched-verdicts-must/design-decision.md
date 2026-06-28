# design-decision — integrate-stage-watched-verdicts-must

*Recorded 2026-06-28 from the dispatch grilling (Claude architect + codex worker fence) and the
operator's direct settlement. The crossing was **not built** — the hand-cranked dispatch was wound
down before the worker ran. This file preserves the settled design and decisions so a future build
need not re-grill them. The build of preserve-and-decide remains a real crossing's job.*

## Re-grounding after the `worker-run-is-not-total` revert (2026-06-28)

This ask was filed as "one failure type, seen four times, patched one seam at a time." After this
session that framing is narrower and sharper:

- **`worker-run-is-not-total` is NOT an instance of this ask.** It was reverted this session as a
  manual-path-only guarantee — it only ever bit the bare hand-driven `worker.run(tree.find(id))`
  caller; the autonomous scheduler always had totality (`Scheduler._fail`). It is also a *different
  shape*: a build that **raises**, not an **adverse watched verdict**. Drop it from the set.
- **`the-fold-s-re-verification` (folded)** already makes a re-verify timeout a distinct
  resource-limit outcome, never a discard-as-broken.
- **`the-integrate-stage-coherence-judgment` (folded)** already makes an unreadable coherence reply
  (the absent `coherent` flag) distinct from explicit incoherence, never a refusal.

So the **unobtainable** shapes (timeout / unreadable / malformed / absent) are each individually
handled. The genuinely-open core is the **adverse** watched verdict — caveat-survival
(`survives: false`) — which still discards a gate-proven, re-verified build. It bit the
`surface-the-watched-depth-scan` crossing this session: a sound build, refused at integrate over a
dropped-caveat verdict, fence torn down, only the bytes dangling in git.

**The ask reduces to:** no watched integrate-stage verdict discards a gate-proven build; an
**adverse** one **holds** the build for a **no-rebuild** settle. The remaining value is (a) handling
the adverse case (currently unhandled) and, secondarily, (b) unifying the handled pieces under one
discipline. (The operator owns the narrowed scope; this is the architect's reading, to confirm when
the ask is next picked up.)

## Spine (operator-ratified 2026-06-28)

Preserve-and-decide. The deterministic gate is authoritative for **soundness**. A watched verdict at
integrate MAY raise a decision (the operator-altitude contract miss the gate cannot mechanize) but
MUST NEVER discard the verified build. The build is **held**, so settling the decision — or overriding
a flake — folds the **same** artifact with no rebuild. An **unobtainable** verdict is retried a
bounded number of times, then surfaced as a distinct outcome, never collapsed into a refusal.

## Contract (settled in the dispatch grilling)

A watched integrate-stage verdict over a build whose deterministic gate is green never discards the
verified build. It **retries an unobtainable** verdict (absent / unreadable / malformed / errored /
timed-out) a bounded number of times then surfaces it as a distinct outcome; for an **adverse** one it
**raises a decision with the build held for a no-rebuild fold**. The held build still re-verifies on
merged main at the eventual fold (main may have moved — `delta.fold`'s staleness pre-check and
whole-system re-verify run unchanged over the held artifact).

## The load-bearing seam (design-it-twice) — candidate **B** won

**B (chosen):** the verified `WorkerResult` {refined delta + captured base/tip engine bytes + fork
base} is serialized as durable **material on the decision node**, and re-folded at settle via the
unchanged `delta.fold` (staleness pre-check + whole-system re-verify).

- **Rejected A — the fence persists past integrate.** Fights `teardown` on every crossing exit and
  contradicts the provenance discipline that binds the trail to *what durably survives the torn-down
  fence, never the fence*.
- **Rejected C — reconstruct from the commit.** The fence branch is `branch -D`'d at teardown and is
  absent from main's lineage, so the bytes dangle unreferenced — today's exact fragility.

B keeps the deterministic gate AND the whole-system re-verify intact at the eventual no-rebuild fold.

## Scope — subsume

One shared seam: `integrate`'s non-done returns carry the held build; `worker.run` blocks the node on
the card instead of `recover` + `teardown` discarding it. The already-folded fixes (timeout,
coherence-unreadable) become instances routed through it; their distinct reason-texts are preserved.
`worker-run-is-not-total` is **excluded** (reverted, different shape). Only a genuine deterministic
re-verify failure (`CannotFold`: red-on-merge or stale) still discards — a build unsound on current
main must re-cut, not be held.

## Disposition on a decided-against held build — operator-settled: **offer modify (both)**

When the operator confirms a watched verdict was right (the held, gate-proven build genuinely missed
the contract), the decision card offers **re-cut AND modify** (plus the established change-the-ask /
abandon):

- **modify** seeds a worker fence from the held artifact's captured bytes + refined delta for a
  targeted amend (e.g. just the dropped-caveat render line) — cheaper than re-implementing the whole
  delta. It still re-clears the full deterministic gate red→green and the whole-system re-verify;
  **soundness is never skipped** — modify saves the rebuild-from-scratch, not the gate. So this node
  **builds the seed-fence-from-held-artifact seam.**
- **re-cut** discards the held artifact and rebuilds from the contract.

(Operator settled this directly, 2026-06-28, after the dispatch architect correctly refused to build
an operator-reserved decision on a coordinator relay.)
