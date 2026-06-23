---
kind: ask
state: standing
owner: operator
created: 2026-06-22
---
# vocabulary-sweep — bring the language into one consistent corpus, and keep it there

A total vocabulary sweep across the whole live corpus — spec, engine, intent, glossary,
skills, ADRs — surfaced that the glossary had drifted ~16 load-bearing terms behind the
built system, alongside genuine name conflicts (one concept under two names, one name over
two concepts), one place where built behavior contradicts ratified intent, and a handful of
stale leftovers. Root cause: the glossary is hand-tended and nothing ties it to the fold,
while the derive-on-fold channels never drifted (the slice-15 lesson, restated).

Settle the vocabulary the operator finds clearest, bring glossary + spec + intent + code into
one language, and wire vocabulary coverage to the fold so it cannot silently drift again.

The settled decisions and full wording are material on this node: see `decisions.md`.

## folding condition
- the ratified decisions (D0–D12 + amendments in `decisions.md`) are applied to `glossary.md`,
  the spec, and `intent.md`, and the rename map is executed across spec + engine;
- the open items (vocabulary-check name; the "ready frontier" rename; the **communication**
  capability scope; the graph/node abstraction question; the engine-term review pass) are each
  resolved or spun out as their own asks;
- the build-work graphs it spawns (operator-view readiness surface; card `kind`; the delegated
  vocabulary check) are filed as their own nodes;
- `python3 -m engine --check` is green.
