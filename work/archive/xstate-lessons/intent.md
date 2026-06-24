---
kind: ask
state: folded
owner: operator
created: 2026-06-23
folded: 2026-06-23
---
# xstate-lessons — absorb the three lessons from the xstate inheritance study

A study (`study.md`, this node's material) read xstate / Harel statecharts against hypercore to find
what is worth **inheriting cheaply** — emulating in the narrow form hypercore needs — versus adopting
the library, which the study rejects. The finding: hypercore has already re-derived most of the
actor/statechart core natively, so the yield is vocabulary, two small sharpenings, and one visual
lesson. The study landed three distinct moves, each its own child tree below. This node holds the
shared provenance (the two-layer framing and the declined-features list all three draw on) and folds
when all three children resolve.

The three children, in dependency order:

- **actor-guard-vocabulary** — sharpen `schedule` and `folding-conditions` **in place** so the
  actor/guard semantics they already describe become load-bearing (vocabulary; trivial/prose delta).
- **dispatch-totality** — gate the "every dispatched worker resolves to exactly one terminal"
  invariant as an executable scenario in `schedule` (the one behavior-bearing move).
- **visualizer-grammar** — capture the two-layer visualizer grammar as a design note against
  intent §44 (material/provenance for the unbuilt reasoning-visual).

The children are sibling cuts, not a chain, with one ordering note: the "dispatch is total" prose
rides with **dispatch-totality**, not **actor-guard-vocabulary**, so the sharpened requirement and the
scenario that gates it land in one fold.

## structure note
The children nest in this node's own `work/` per `spec/tree.md` ("a tree's child trees nest the same
way in its own `work/`"). The lone on-disk child example (`work/archive/scenario-gate/binding-contest`)
sits directly under its parent instead; that reads as drift from the written spec, so this tree follows
the spec. Flag, not a blocker. [machine]

## open decision — sequencing (the operator's call, reserved)
Which child runs first, and whether in this session or a separate one. **Lean: dispatch-totality** —
it is the only child with a real engine seam, so building it is the highest-information move (like
`scenario-gate` / slice-16, wiring the gate may surface a latent stranding bug the harness has never
exercised) and it is a genuine dogfood of the feedback loop. **Flip:** if the operator would rather
ground the §44 visualizer work sooner, or take the lowest-risk vocabulary fold first as a warm-up. [machine]

## folding condition
- each of the three child trees has folded (resolved, or consciously parked with a recorded reason —
  none silently dropped);
- `python3 -m engine --check` is green. [machine]

## status — all three children built, parent awaiting the acceptance pass (2026-06-23)

The sequencing decision resolved on its lean and then dissolved: **dispatch-totality** ran first (the
real engine seam, the highest-information move), then **actor-guard-vocabulary** and
**visualizer-grammar**, all in this one session. Each child carries a recorded `## result` and is
**built, awaiting the operator's acceptance to fold** — none folded yet, so the parent's folding
condition ("each child has folded") is **not yet met**: it waits on the operator's acceptance pass over
the children. `python3 -m engine --check` is green across the whole tree.

The three findings, in one line each:
- **dispatch-totality** — green regression guard, not red→green: the engine was already total; the
  invariant is now positively stated and gated (`schedule`: 4 gated, 0 watched).
- **actor-guard-vocabulary** — prose-only MODIFIED delta, no behavior moved, no scenario regressed;
  the actor/guard vocabulary is now load-bearing in `schedule` and `folding-conditions`.
- **visualizer-grammar** — design note as material against §44; no delta, nothing constraining the
  operator's authored vision.

Acceptance is the operator's act, held: nothing is committed; all of it remains `[machine]` drafts. [machine]
