---
kind: ask
state: folded
owner: operator
created: 2026-06-23
folded: 2026-06-23
---
# visualizer-grammar — the two-layer visualizer grammar, as a design note against §44

The xstate study found the inheritable visual lesson for the unbuilt reasoning-visual (intent §44):
**draw the fixed topology once and overlay the live position on it — but only where a topology is
fixed.** hypercore has two layers: the **node lifecycle + supervision** (fixed → borrow xstate's
static chart + live highlight wholesale) and the **execution tree** (grown, not declared → borrow the
inspector's live actor-tree, never the chart editor; §104 forbids pre-drawing it). Plus the visual
grammar to steal regardless — events on edges, hierarchy as containment / fold-as-collapse, guards
shown with the unmet clause named, history as the time axis — all at the operator's altitude, not the
engine's. Full lesson in `../../study.md`.

Capture this as a **design note** — material the future §44 build reads — so the lesson outlives this
disposable thread.

## open decision — design note only, or intent/spec-touching
**Lean:** a **design note as material** (provenance for the unbuilt §44 visualizer) — no delta, no
capability, no edit to intent §44 (authored vision is the operator's). It folds when the note is
written and accepted. **Flip:** the operator wants it to land as a drafted `spec/visualizer.md`
capability stub or a sharpening of intent §44 — then it becomes vision/behavior-touching and is
grilled as such before it spawns. The lean holds because §44 is unbuilt and authored vision is the
operator's to write. [machine]

## folding condition
- a design note capturing the two-layer grammar and the inherited visual moves lands as material on
  this node, scoped to §44, with the design-note-vs-spec decision above settled;
- it cites the study as provenance and depends on nothing in this thread. [machine]

## result — built, awaiting acceptance (2026-06-23)

The design-note-vs-spec seam settled on its **lean**: a **design note as material**, no delta, no
capability, no edit to intent §44. The flip (land it as a `spec/visualizer.md` stub or a §44 sharpen)
did not bind, because §44 is unbuilt and authored vision is the operator's to write — a machine draft
of the operator's vision would invert that. So the note is captured as material the future §44 build
*reads*, not as anything that constrains what the operator authors.

What landed: `design-note.md` on this node — the two-layer grammar (Layer A node-lifecycle +
supervision → static chart + live highlight; Layer B execution tree → live actor-tree, never the chart
editor, per §104), the visual grammar to steal regardless (events-on-edges, containment / fold-as-
collapse, guards-shown-with-unmet-clause, log-as-time-axis), and the altitude to decline (developer
state-IDs → operator words). It anchors to §44's exact words, cites `../../study.md` as provenance, and
depends on nothing else in this tree.

No harness involvement — a design note touches no capability and gates nothing (correctly *watched*,
not gated). Folding condition met. Awaiting the operator's acceptance to fold (the note rides with the
node into the archive as its material); not committed. [machine]
