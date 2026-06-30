---
kind: ask
state: abandoned
owner: operator
created: 1782779600
---
> Abandoned 2026-06-29 — superseded by `the-interface-leaves-the-terminal`: the
> owned-window rebuild retires the curses interface this tree was redesigning.

The navigation becomes one cursor — redesign the window's interaction/runtime model as a coherent whole, the holistic pass it never had (it accreted across four serialized render slices). The static faces are fixed and good; this carves the model *between* the faces.

Design (design-it-twice, chosen machine-side — `design-decision.md`, candidate set reachable): a pure `nav.py` core (`key`/`land`/`resolve`) over one identity-keyed cursor on a single queue+work spine; reading faces as a lens back-stack with one universal back key; one compose overlay as the sole text place; the reasoning loop and threads node-scoped on the *selected* element (no first-worker misfire, no converse chain); the masthead a selectable architect-seat; engine calls as declarative effects run off-loop so keystrokes stay instant. The fixed pure-render int-index signatures are preserved (`resolve()→sel_index`), so the `designing-the-face` tool and the headless scenario checks keep working verbatim.

This fixes the four diagnosed failures: inert work rows, non-node-scoped threads, the misfiring loop key, the non-universal back key — and the key-grammar drift across modes.

Open stake-bearing decisions (raised to the operator, parented here): leader-vs-direct act keys; deterministic acts vs. word-routed speak for re-ask/reprioritize/edit-step; snap-to-new-decision vs. stay-put on the unified spine; `q`-no-longer-quits.

Folding condition: the window navigates as one cursor over the spine with the lens back-stack and node-scoped loop/speak; the interface scenarios (existing + any added for selection/back/loop-scope) go red→green; the new faces are judged by eye on a real render beside the operator; `python3 -m engine --check` is green.
