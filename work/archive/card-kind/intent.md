---
kind: ask
state: standing
owner: operator
created: 2026-06-23
---
# card-kind — record a card's kind on its node, don't guess it at render

A card carries a **kind**, but nothing records it: the render guesses. Make **kind** a real recorded
property of the node so the queue render reads it instead of inferring it.

The five kinds along the work's life (D18): **grilling question · request for approval ·
ratification · decision · acceptance** — ratification (bless intent, at the front) and acceptance
(sign off the result meets its bar, at the back) the bookends; "request for approval" (before a
step) stays distinct from acceptance (after the work) unless the operator merges them. The full
taxonomy is settled here.

The hinge with the folding model (D19): a **watched** standard whose **trace** needs human sign-off
raises an **acceptance** card — the operator clearing a condition no check could.

Provenance: `work/archive/vocabulary-sweep/decisions.md` (build-work #2; D2, D18).

## folding condition
- a card's **kind** is a recorded property on the node and the queue render reads it rather than
  guessing; all five kinds are representable;
- `python3 -m engine --check` carries an acceptance check for it and is green.
