# design decision — the window navigation/interaction model

design-decision: the window navigation/interaction model → Locus-and-Lens hybrid (a pure `key`/`land`/`resolve` nav core in a new `nav.py`; one identity-keyed cursor over a single queue+work spine; reading faces as a lens back-stack; one compose overlay as the sole text place; the reasoning loop and threads node-scoped on the selected element; the masthead a selectable architect-seat) → on DEPTH the four candidates tie (each collapses the eight modes plus the scattered selection state and reasoning_input's five handler clusters into one transition law and fixes all four diagnosed failures the same way); the decision falls to LOCALITY and SEAM, where Locus-and-Lens wins decisively — it is the only candidate that preserves the existing pure-render INT-index signatures (via `resolve() → Resolved(lens, sel_index, payload_handle)`) and keeps engine internals out of the core (opaque handles + declarative Effects + `land()`), so the `designing-the-face` preview tool and the headless scenario checks keep working verbatim and the new `nav.py` is insulated on both sides by data-only boundaries. Grafts: the single pure `selectables()` ordering function (cand A) behind `resolve()` for desync-proof selection order without changing any render signature; a per-kind verb *declaration* (cand B) feeding each lens's footer act-row as `(letter,label)` data while keeping `a/c/e` direct (dissolving the leader-vs-direct stake); and the masthead-as-architect-seat (cand C) for a concrete architect-scoped speak/loop home in place of the fragile `ARCHITECT_THREAD` fallback.

This is the architect's machine-side selection (depth / locality / seam placement), recorded with the candidate set reachable below per `design-it-twice`. The pick's reason is watched (creative); only the structural reachability — that a real contest of N candidates exists — is gated.

## the contest — the recorded candidate set (4 isolated briefs)

Each candidate designed the same interface in its own isolation, under a different brief. Designs only, no implementation.

### A — "One Cursor, One Line" (brief: minimize the interface)
The fewest concepts: 4 verbs (move/open/back/speak) + 3 acts (a/c/e) + 2 pulls (loop/view). One reducer; one pure `selectables(surface,nodes)` owning selection order for BOTH the reducer and render; cursor held as a node id. Folds edit-step / re-ask / reprioritize into the one `i` compose door with machine word-routing.
- strongest: the single pure `selectables()` as the one owner of selection order, shared by movement and paint — structurally desync-proof.
- weakest: leans hardest on machine word-routing; changes the render signature from int to id, loading the otherwise-fixed render seam and its headless checks.

### B — "The One Cursor" (brief: maximize flexibility)
An `Element` abstraction; every element answers `verbs()`; a leader key (Space) opens a generated palette of the focused element's live verbs. A new kind/verb is pure data, zero new keys.
- strongest: verbs-as-data behind a generated palette — a new element kind arrives with full support and no new key.
- weakest: mandates leader-then-letter (two keystrokes) for acts that are one key today; forcing five heterogeneous kinds through one `verbs()` may leak.

### C — "The Carried Place" (brief: optimize the common caller)
One id-keyed spine; `step(state,key,tree) → (state, effects)` with engine calls as effect descriptors the window runs. The masthead `hypercore` row is a selectable architect SEAT (architect speak/loop one key from it). Keeps direct keys a/c/e/r.
- strongest: effect-descriptors keep IO/git out of the core; the masthead-architect-seat is the one concrete answer to where architect-scoped actions live.
- weakest: names the largest one-shot refactor risk; the masthead seat is invisible (discoverability); `a` = affirm/advance stretched over approve-a-card AND re-ask-a-worker is the most abstract single-key meaning.

### D — "Locus and Lens" (brief: ports and adapters) — the chosen skeleton
A new `nav.py` pure core: `key(state,ch,snapshot)→(state,[Effect])`, `land(state,result)→state`, `resolve(state,snapshot)→Resolved(lens, sel_index, payload_handle)`. Imports neither curses nor IO. A `Snapshot` of `Locus(id, place, kind, is_question, can_loop, loop_source, has_held_build)` plus OPAQUE handles (Thread/ViewNode/ReasoningLoop) the core stores but never inspects. All IO leaves as declarative `Effect`s the adapter runs off-loop and folds via `land()`. Eight modes → five lenses × one compose bit.
- strongest: the only candidate that preserves the existing int-index render signatures (via `resolve()→sel_index`) AND insulates the core from engine internals — the most surgical fit to the fixed render seam and the existing tooling.
- weakest: the `Snapshot` must carry enough projected flags to keep the core pure (risk of a second model if it grows); folds worker re-ask into the speak door (shares A's word-routing bet for that one act).

## the comparison (neutral, the architect overrode toward the hybrid)
- DEPTH: near-indistinguishable across all four.
- LOCALITY: D best (data-only boundaries on both sides); A concentrates risk in one reducer; C is a candid big-bang lift.
- SEAM: D sharpest — the only one preserving the fixed pure-render int-index signatures and the `designing-the-face`/headless tooling verbatim.
- Recommended build: D skeleton + A's `selectables()` graft + B's verb-data footer (keeping a/c/e direct) + C's masthead-architect-seat. Adopted.

## stake-bearing differences — settled by the operator (2026-06-29)
1. **Act keys → DIRECT.** `a`/`c`/`e` act in one keystroke; each lens's footer names its live acts as `(letter,label)` data handed to render (graft B), so a new act is data, not a new key. No leader.
2. **re-ask / reprioritize / edit-step → FOLDED INTO SPEAK (`i`).** The operator chose word-routing over dedicated keys: these are spoken intents on the selected element, classified by the machine (intent §54 "reading the operator's words is machine work"; §66 "the word is the reorder, not a request for one"). More intent-aligned than the architect's reliability lean; the universal acts `a`/`c`/`e` stay direct, the nuanced intents go through `i`.
3. **New urgent decision on the spine → STAY PUT, signal on the queue.** The cursor never moves under the operator; the new decision announces itself with a cue on the queue (the one reserved alarm hue earns its place). The operator jumps to it on their word.
4. **`q` → STAYS A QUIT COMMAND, made uniform.** Not Ctrl-Q-only. The operator corrected the framing: every letter is a command on a command surface and text in compose — `q` is no different. The real drift was `q` quitting on some command surfaces (browse/card/view) and going inert in others (the loop); the fix is uniformity — `q` quits on *every* command lens and is text in the compose overlay like `a`/`c`/`e`/`v`.

Settled by §-already-decided (build to it, not a fork): a late architect reply when the operator has backed out lands on the node, which keeps it with a live indicator (intent §64).
