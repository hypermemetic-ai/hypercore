---
kind: ask
state: in flight
owner: operator
created: 1782190800
---
# vocabulary-check — wire vocabulary coverage to the fold so the corpus can't silently drift

The vocabulary sweep's root-cause finding: the glossary is **hand-tended and tied to nothing**, so
it drifted ~16 terms behind the built system, while the derive-on-fold channels never drifted. The
fix is a standard that rides the fold (D11/D16): a **vocabulary check** — communication's
**consistency** standard (D15).

A dedicated **run** (a strong model, cheap because the whole live corpus fits one context window)
reads the corpus for **new or conflicting** vocabulary and, on a finding, raises a
**define / waive / dismiss** decision and **holds the fold** — the length-signal pattern applied to
words. Mechanical floor **gated** (a term used but undefined), semantic judgment **watched**. The
architect never carries it.

Per D19, a watched standard must emit a **trace** and the fold must check the trace's presence — so
this node also carries the trace-emits-and-fold-checks wiring for the watched half.

Provenance: `work/archive/vocabulary-sweep/decisions.md` (build-work #3; D11, D15, D16, D19).

## folding condition
- a vocabulary check runs at fold time over the whole live corpus, raises a define/waive/dismiss
  decision on a finding, and holds the fold until settled; its mechanical floor is gated and its
  watched half emits a trace the fold checks;
- `python3 -m engine --check` carries an acceptance check for it and is green.
