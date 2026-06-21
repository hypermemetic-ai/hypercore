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
slice 5's capability.

## Considered and declined — do not re-propose

Making handoff §9 ("do not re-introduce these errors") into an enforced pre-fold checklist
was raised and **declined** by the operator (2026-06-21): §9 is a bootstrap artifact — the
errors that tempted across the spec's revision rounds — not the critical invariant set, so it
is not worth hardening, and a checklist of named errors buys false comfort against the gap
that actually matters (unsurfaced, *un*-named drift). The real defenses against that gap are
the worker fix (the §6.4 keystone — a second role with full scan the first can't suppress) and
the architecture review (slice 6, now built — a standing adversarial scan rendered to the
operator). Knowing §9's errors exist is enough.

## Next — slice 7 (parallelism, re-grounded)

The worktree concurrency now also serving design quality: the design-it-twice pattern
(rebuild-spec §7.5, §9.7) for load-bearing interfaces — parallel workers in isolated worktrees
producing genuinely different interfaces for one decision, compared on depth, locality, and
seam placement. *Check:* concurrent workers advance one graph in isolation and each folds its
delta; a load-bearing interface decision can be designed twice in parallel and compared.
