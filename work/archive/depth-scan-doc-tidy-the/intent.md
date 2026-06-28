---
kind: ask
state: done
owner: operator
created: 1782638347
---
Depth-scan doc-tidy — the model-driven depth scan is built, but the fold left the spec preambles, the glossary, and the self-model prose still calling it not-yet-built, and the watched scan's findings are not yet surfaced into the live operator view.

The `the-model-driven-depth-scan` crossing (folded 2026-06-27) built the seam (`engine/depth_scan.py`) and flipped `spec/architecture-review.md`'s REQUIREMENT blocks to "built" (`:190` "MUST be **built** — no longer recorded as not-yet-built", `:204`, `:213`). But a fold lands only requirement-blocks and engine code — `delta._apply` keeps a capability's PREAMBLE verbatim and never touches `glossary.md` or a render-body's prose. So the surrounding prose still describes the scan as absent, now contradicting the same spec's own updated requirement:
- `spec/architecture-review.md:54` (preamble) still reads: "shallow-module and information-leakage judgments ... is **not yet built**" — directly contradicting `:190` / `:204` / `:213`.
- `spec/depth.md:18` still reads: "the model-driven verdict — is this module actually shallow? — is **not yet built**".
- `glossary.md:208` still: "**red-flag depth scan**, recorded as not-yet-built"; `:162` likewise.
- `spec/self-model.md` render-body prose around `:236` ("not-yet-built, never fabricated") may still read the absence.

Second gap, named as deferred by the crossing: the depth scan's verdict is WATCHED — a dedicated run leaving a trace — but its findings are not yet surfaced into the live operator gap / complexity-debt view. The crossing deferred this because it needs the committed-trace path, and noted the watched scan must stay OUT of the deterministic view-render or the self-model's byte-exact gap/debt/structure scenarios go red on merged main.

This is mostly architect-direct authoring (preambles, glossary, render-body prose — the fold discards preambles, so a worker cannot carry them, exactly as `communication-mastery` was authored direct), plus possibly one fenced behavior (surfacing the watched findings into the view via the committed-trace path).

To surface in grilling: WHICH "not yet built" references are genuinely stale (about the now-built model-driven depth scan) versus which name a DIFFERENT, still-true absence and must NOT be touched — the scenario gate's red-at-base (`folding-conditions.md:14,25`), the vocabulary-check watched half held not-yet (`folding-conditions.md:298,314`), and the general "not-yet-built, never fabricated" honesty principle where it states the principle rather than the depth scan's status — a blanket find-replace would corrupt the honest absences the system still names truthfully. Whether the watched findings reach the live view in this ask or as its own follow-up, and the concrete committed-trace seam that carries them without entering the deterministic render. Folding condition: the spec preambles, the glossary, and the self-model prose no longer contradict the built scan; the watched scan's findings surface in (or are explicitly homed for) the operator's gap / debt view; `python3 -m engine --check` is green.
