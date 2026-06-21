# next work

## Done — slice 6, the architecture review render (2026-06-21)

The standing review (`hyper/review.py`, rebuild-spec §7.4) scans the source tree live for
deepening opportunities — modules over or nearing the line-count budget — and renders two
things from one scan: the **deepening backlog** (the engine that surfaces
god-files-in-the-making) and the operator view's **upper levels**, a visual structural map
of as-built reality with debt marked. The review is not a separate artifact: its output *is*
the operator view's as-built and gap (`view.operator_view`), so the operator reads the
system's shape without reading code (§9.6 acceptance met). It consults the budget
`folding-conditions` owns — one budget, the per-graph gate at the fold and this standing
whole-tree scan. New capability `architecture-review` (ADR 0005, the eighth and last unit ADR
0001 forecast); self-model's view requirement MODIFIED to record the upper levels as the
review's standing output.

The first deepening work the review surfaced, landed in the same slice: the acceptance harness
`hyper/check.py` (491 lines, over budget — ADR 0004 named it the first candidate) was split
into the per-slice `hyper/check/` package (`harness` + `__init__` orchestrator + `slice1…6`),
each well under budget, so the review reports the real tree honestly clean. Building the
god-file *detector* while growing a god-file would have been self-contradictory.

## Known debt — the justification escape hatch is a loose substring match

`conditions.justified` (and so the review) treats a file as justified-over-budget when its
basename merely *appears* in any decision record — not when the record actually justifies its
size. It surfaced this slice: `check.py` read "(justified)" only because ADR 0004 *named* it
while saying it should be split. The check.py split made it moot (no over-budget file remains),
but the hole is latent: a future ADR that names a coincidentally-over-budget file would hide it.
A tightening (require an explicit justification phrase, or a structured ADR field) is
folding-conditions' to make and carries its own delta — not done here to avoid scope creep into
slice 5's capability. **Folded into slice 7's scope** (below): the whole budget heuristic is
being reconsidered, so this hole is fixed or made moot as part of that re-grounding, not before.

## Considered and declined — do not re-propose

Making handoff §9 ("do not re-introduce these errors") into an enforced pre-fold checklist
was raised and **declined** by the operator (2026-06-21): §9 is a bootstrap artifact — the
errors that tempted across the spec's revision rounds — not the critical invariant set, so it
is not worth hardening, and a checklist of named errors buys false comfort against the gap
that actually matters (unsurfaced, *un*-named drift). The real defenses against that gap are
the worker fix (the §6.4 keystone — a second role with full scan the first can't suppress) and
the architecture review (slice 6, now built — a standing adversarial scan rendered to the
operator). Knowing §9's errors exist is enough.

## Next — slice 7 (re-grounding the architecture in Ousterhout)

The operator's call (2026-06-21), inserted ahead of parallelism: reconsider the line-count
budget (rebuild-spec §7.1) and the slice-6 `check.py` split against John Ousterhout's *A
Philosophy of Software Design* — and, **if the impression holds after a deep run through its
ideas**, rebuild hypercore's architectural constraints around it. The line budget's standing as
the central constraint is what's in question; design-it-twice / parallelism moves to **slice 8**.

The slice runs in three phases, in order:

1. **Research — a faithful, durable synthesis of APoSD.** Web-grounded, landed as material in
   the repo (not throwaway chat): the framework (complexity = dependencies + obscurity; deep vs
   shallow modules; information hiding/leakage; the full red-flags list; strategic vs tactical;
   define-errors-out-of-existence; design-it-twice), its **epistemic status** (reasoned opinion,
   judgment-based — not mechanical or empirically-proven), and the contrast with *Clean Code*
   (the Ousterhout–Martin debate on method length, comments, TDD) — that contrast being the crux
   of "ESPECIALLY when compared to clean code."

2. **Back-and-forth — grilling, one fork at a time, each with a lean and what flips it.** The
   design spine to resolve: Ousterhout is a **judgment** framework; hypercore's folding
   conditions are **mechanical** gates. So the re-grounding falls along the seam already cut —
   the mechanical **gate** (folding-conditions) keeps at most a minimal tripwire; the **judgment
   layer** (architecture-review) is where the red flags actually live, applied as a standing
   scan (likely model-driven). Forks: replace vs. demote the line budget and with what; which
   signals stay mechanical; whether the `check.py` split was classitis and reverts; scope
   (an in-place §7 revision vs. a larger constraint rebuild).

3. **Reimplementation — scoped by what phases 1–2 conclude.** Revise §7.1 and the affected
   ADRs (0004, 0005), rebuild `conditions.py` (the gate) and `review.py` (the scan) to the
   resolved design, re-decide the slice-6 split on the new criteria, and land it with deltas;
   amend §9's slice list. The justification-match hole above is fixed or made moot here.

*Check:* the architectural constraints read in Ousterhout's terms (deep modules, the red flags),
the mechanical gate and the standing review reflect them, the operator reads the system's
**depth** and not merely its **length**, and the slice-6 split is re-decided on the new criteria
with its reasoning recorded.

### Progress — phase 1 done, phase 2 grilled (2026-06-21)

Phase 1 landed: `research/aposd.md` — the faithful APoSD synthesis (the framework, its epistemic
status, the primary-sourced *Clean Code* debate). Phase 2 grilling resolved five forks and grew
the slice into a full architectural re-grounding, designed in `research/regrounding.md`:

- **Length demoted beneath depth.** Depth is the governing criterion; length stays only as a
  context-cost signal — every line is window an agent loads, hypercore's own concern, which
  survives Ousterhout's objection because it polices *context cost*, not *depth*.
- **The depth verdict is the architect's, raised as a decision.** On "shallow" the gate raises a
  decision (re-cut / deepen / accept), never a silent veto. The worker is grounded in the depth
  disciplines so it builds deep up front — the gate is a rarely-tripped backstop, not an
  operator-load generator (the operator's stated condition for adopting this).
- **conversationalist → architect.** Putting the depth verdict at its gate exposed the role as an
  architect with communication duties; renamed, two roles (split by audience) preserved.
- **The slice-6 `check.py` split keeps**, on locality grounds — partitioning along the per-slice
  seam, not classitis, not deep modules; ADRs 0004/0005 re-grounded.
- **The justification-match hole is closed by construction**: length no longer auto-refuses, so
  the loose substring escape-hatch is deleted, replaced by a structured depth-decision record.

**F1 — resolved (defer both).** The depth-assessment machinery — both the model-driven verdict
*and* the mechanical proxies — is **not built this slice**; it is recorded not-yet-built and
likely wants its own later slice (a model-driven standing red-flag scan is a real capability, and
cramming it in would itself be tactical). Phase 3 builds only the settled, fully harness-testable
scaffold: length demoted to a signal that raises a *decision*, not an auto-refusal; the substring
escape-hatch deleted and replaced by a structured depth-decision record; the review re-rendered
around depth (length + the red-flags framework as the lens, the depth-assessment marked
not-yet-built); the worker grounded in the depth disciplines; the §7/§6 + ADR 0004/0005 revisions;
the check.py split kept on locality; the §9/README housekeeping. The operator reads the system
through the *depth lens* (the framework, the decision-raising gate, the grounded worker) this
slice; the automated depth *measurement* lands later.

**Still open for the implementing session:** **F2** — does any high *pathological* length ceiling
survive mechanically (architect's lean: yes, one high context-cost tripwire, far above the old
400); **F3** — the capability naming (architect's lean: keep `conversation`, rename only the role).

### Handoff (smart-zone, rebuild-spec §5.3) — clear the session; implement phase 3 fresh

Design (phases 1–2) is complete and durable; the implementing work wants a clean window. A fresh
episode implements phase 3 by reading, in order: this section of `next-work.md`, then
`research/regrounding.md` (§8 = the change list, §7 = the open forks F2/F3), then
`research/aposd.md` (the grounding), then the touched specs and `hyper/{conditions,review}.py`.
Settle F2/F3 first (both small), then build the scaffold above, carry the spec deltas, and meet
the acceptance check. Phase 1 and phase 2 are committed (`e136ac1`, `5777961`).

## Later — slice 8 (parallelism, re-grounded)

The worktree concurrency now also serving design quality: the design-it-twice pattern
(rebuild-spec §7.5) for load-bearing interfaces — parallel workers in isolated worktrees
producing genuinely different interfaces for one decision, compared on depth, locality, and
seam placement. *Check:* concurrent workers advance one graph in isolation and each folds its
delta; a load-bearing interface decision can be designed twice in parallel and compared.
