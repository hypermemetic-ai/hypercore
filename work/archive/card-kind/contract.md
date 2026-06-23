# card-kind — ratified contract

Grilled 2026-06-23. The durable record of what the grilling pass settled.

## What the scan resolved from the ratified corpus (no operator stake)

- **The taxonomy is already ratified.** `glossary.md`'s `card` entry — rewritten by the vocabulary
  sweep — lists the five distinct kinds (grilling question · ratification · request for approval ·
  decision · acceptance) and the principle "recorded on the node, **not guessed at render time**."
  So the kinds and the keep-them-distinct question (D18's open merge) are settled by the vocabulary;
  the code simply hasn't caught up. This is a bring-the-code-to-the-spec build.

## The one residual decision (operator-settled)

- **Scope: taxonomy + wire the length acceptance.** Record the card kind and have the render read it
  through one seam (retiring the guessing), all five kinds representable — AND wire the one concrete
  acceptance path: settling the depth gate's "accept the length" decision from the queue calls
  `conditions.accept()`. Gives the writer seam its production caller and completes the accepted-length
  arc. Self-contained — no dependency on the unbuilt watched-trace pipeline (D19).

## The design (architect-resolved)

- **One seam: `grill.card_kind(node) -> str`** returns the card's kind — one of the five glossary
  strings. It records the stable kinds (reads the node's `kind` field: `decide`→decision,
  `approval`→request for approval, `acceptance`→acceptance) and honestly derives the pass-stage ones
  (an unresolved grilling tree → grilling question; a resolved one → ratification). Lives in `grill.py`
  (already owns the pass-stage distinction; `tree` can't host it without a `tree`↔`grill` cycle).
  The render (`_card_label`/`_card_detail`) and the window's `a` handler both read this seam instead
  of inlining `grill.is_question`/`is_entry` — the guessing retired in both places.
- **Length acceptance.** A length-over-signal card is a **decision** (re-cut / deepen / accept); the
  gate already emits the `accepted: <rel> @<N> — …` template in its text. `conditions.length_decision(
  text)` parses `(rel, n)` back; settling such a card with approve calls `conditions.accept(rel, n,
  reason)` and clears the card. The held parent's re-fold is the scheduler's standing job (the record
  now clears the gate) — out of this node's scope. The general watched-trace→acceptance card stays
  representable, unproduced (awaits D19) — recorded honestly.

## The spec delta this realizes (`spec/queue.md`)

- retire the drifted term **weight** → **kind** (D2);
- complete the taxonomy to the five kinds incl. **acceptance**, recorded and read (not guessed);
- a scenario: approving a length decision records the accepted length through the writer seam.

## The contract (validated at the archive gate)

- `grill.card_kind` returns the right kind for each of the five; the render and window read it, not
  `is_question`/`is_entry`.
- settling a length decision writes the accepted-length record (`conditions.accept`) and clears the
  card; `accepted_at` then clears the gate.
- `spec/queue.md` carries no "weight"; the five-kind taxonomy + the length-acceptance scenario.
- `python3 -m engine --check` green with an executable check (red→green).
