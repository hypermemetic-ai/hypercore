---
kind: ask
state: standing
owner: operator
created: 2026-06-23
---
# communication-clarity — the clarity intent and the communication skill

The `conversation`→`communication` rename is done; what the capability expansion (D15) still owes is
the **clarity** standard. **clarity** is a **watched** standard: the principle stated in the
`communication` spec, and the readability literature (concision, chunking, plain words, sentence
structure, type/legibility) carried in a **loaded `communication` skill** — the same
grilling/coherence/design-it-twice pattern. **No gated readability metrics** (gameable, and they
punish terse technical writing).

Two pieces of build:
- a **clarity intent** — a watched principle in the spec/intent, not a one-line reword (it was
  deliberately spun out of the sweep's stage-3 intent edits);
- the **`communication` skill** — author the readability literature and **register it in the
  methodology registry** so it renders on fold like the other four skills.

Provenance: `work/archive/vocabulary-sweep/decisions.md` (build-work #4; D12, D15).

## folding condition
- a watched **clarity** intent lands in the spec, and a `communication` skill carrying the
  readability literature is authored and registered in the methodology registry (rendered on fold);
- `python3 -m engine --check` carries an acceptance check for it and is green.
