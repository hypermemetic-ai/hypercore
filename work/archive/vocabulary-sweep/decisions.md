# vocabulary-sweep — decisions & wording

Compiled 2026-06-22. This is the durable record so the conversation that produced it is
disposable. **Nothing here has been applied to the live glossary/spec/intent/code yet** — this
is the ratified-decision record + drafted wording; applying it is the next step.

---

## Why this exists

The operator asked "how far are we from trusting hypercore to do operator-initiated work on
itself without drifting?" Answering it surfaced that the **operator view can't answer that
question** (it models depth-debt, not readiness), which in turn surfaced that the **glossary
had drifted ~16 load-bearing terms behind the built system**. That triggered a total
vocabulary sweep across the whole live corpus.

## How we worked (method, for resume)

- Five parallel sub-sweeps, one per **concept domain** (graph & work / worker & fence / spec &
  self-model / depth & review / interface & operator), each owning its terms across all files,
  reconciled centrally. Six conflict classes: missing / synonym / homonym / stale / code↔prose
  / invented.
- Then **grilling**: one concept at a time, each as a practical story + concrete options with a
  lean and a flip; the operator picks or reshapes. The decisions below are the result.

---

## Settled decisions (D0–D12)

| # | decision |
|---|---|
| D0 | one glossary; engine terms admitted as concepts (definitions only, no implementation) |
| D1 | **episode** (umbrella) → **thread** (operator) + **run** (autonomous); "session" retired; intent §60/§62 fixed (meant *worker*, not session) |
| D2 | card **kind** becomes a real recorded property; "weight" retired; §26 reworded |
| D3 | **gap** = wanted-but-not-built (plain); **complexity debt** = built-but-structurally-weak (replaces "deepening backlog") |
| D4 | **coherence** = the §84 principle; **contract check** = the architect's archive-gate judgment |
| D5 | **standard** = a quality practice work must meet; each is **gated** or **watched**; "register" + "discipline" retired |
| D6 | **design-decision** = the architect's recorded pick; depth.md's Ousterhout sense → **encapsulated decision** |
| D7 | **fence** is the headword (the isolated place a worker runs); **worktree** = its git mechanism |
| D8 | keep **depth / deep module / shallow module**; *depth decision* → "a decision" (raised by the length signal); *depth-accepted* → **accepted length**; *depth verdict* → **module depth judgment** |
| D9 | **seam** = one concept, two altitudes (work cut + interface boundary) |
| D10 | worker model = **OpenAI GPT-5.5 (xhigh)**; code's `gpt-5.2` was a mix-up with the unrelated GLM-5.2 (a bug to fix); **OMP** = the harness concept, `omp` = the binary, `pi/OMP` retired |
| D11 | a **delegated vocabulary check** as a fold condition over the whole live corpus: a dedicated run (strong model, cheap because the corpus is one context window), raising a *define/waive/dismiss* decision and holding the fold only when new vocabulary appears (the length-signal pattern). Mechanical floor *gated*, semantic judgment *watched*. The architect never carries it. |
| D12 | **conversation** capability → **communication**, with expanded scope (see Open items — needs grilling) |
| D13 | **graph → tree** (resolves Open #4). The structure is a tree *by construction* — `Node` has a single `parent` derived from folder containment, so multiple parents / cross-edges / cycles are impossible — and flat in practice (no nesting used yet; README already says "tree"). Rename graph→**tree**, keep recursive decomposition (a tree property). The whole is the **execution tree** ("the tree"); **not "work tree"** — collides with the git **worktree**. The unit stays a **node**. Vocabulary fix, no data-structure restructure. |
| D14 | **ready work** = the frontier name (resolves Open #2). The takeable subset of **standing work**; matches `tree.ready()`. Operator caught the irony in `graph.ready()` — "what graph?" — which **confirms** the module rename `engine/graph.py` → `engine/tree.py` (+ `graph.` call-sites → `tree.`): keeping `graph.py` while the concept is "tree" re-creates the drift. |
| D15 | **communication** capability (resolves Open #3 encoding). Rename `conversation`→**communication**; it owns the operator-facing channel end to end. **clarity** = a *watched* standard — the principle stated in spec, the readability literature (concision, chunking, plain words, sentence structure, type/legibility) in a loaded **`communication` skill** (the grilling/coherence/design-it-twice pattern); no gated readability metrics (gameable, punish terse technical writing). **consistency** = *gated floor + watched* = the vocabulary check (D11). **Thread stays** here: the two episode kinds live with their owners — run↔schedule, thread↔communication. Likely a new/expanded **intent** section + a new skill. |
| D16 | **vocabulary check** = the name (resolves Open #1). Most literal — checks the vocabulary across the corpus; inherits this effort's lineage ("vocabulary sweep"). It is communication's *consistency* standard (D15). |
| D17 | **folding condition is the umbrella** (corrects an apply-phase mis-draft). A folding condition = *anything that must hold before work folds* — "what must be true to call it done." **standard kept** (Model 2) as the quality-practice subset. Each folding condition is **gated** or **watched**. *(Membership corrected by D19: standards are NOT folding conditions; their evidence/**traces** are.)* |
| D18 | **acceptance** = a fifth **card kind** (refines D2). The five along the work's life: grilling question · ratification · request for approval · decision · **acceptance**. Ratification (bless intent, front) and acceptance (sign off the result meets its bar, back) are bookends. The hinge with D17/D19: a **watched** condition whose **trace** needs human sign-off raises an *acceptance* card — the operator clearing a condition no check could. "Request for approval" (before a step) stays distinct from acceptance (after the work) unless the operator merges them; full taxonomy lands in build-work #2. |
| D19 | **standards aren't folding conditions — their evidence is** (corrects D17's membership). A quality practice (**standard**) is *not* a folding condition; the **evidence of its application** is. Anything that isn't a hard (deterministic) check must produce a **trace**. The complete set conditioning the fold = **deterministic checks + traces of all appropriate judgment procedures** — the fold rests on evidence, never unverified trust. **gated** = application verified by a deterministic check; **watched** = application takes judgment, so it must leave a **trace** (which conditions the fold) while its quality is overseen (→ acceptance card). New coined term: **trace**. *Build implication:* each watched standard must emit a trace and the fold must check the trace's presence (folds into build-work #1/#3, and the register/folding-conditions wiring). |

### Amendments (operator, this session, post-D11)

- **dispatch, not delegate.** The verb for handing a ready node to a run is **dispatch**
  (operator preference). Rename `graph.delegate` → `dispatch`; the scheduler already says
  dispatch. (Reverses the earlier propose-to-apply lean toward "delegate".)
- **ratify** confirmed = the operator's blessing of **extracted/drafted intent** — turning a
  grilled, drafted contract into standing work. A sibling of approve / cut / explain.

---

## Glossary delta — full drafted wording

> **STATUS: SUPERSEDED BY THE LIVE GLOSSARY.** Stage 1 of the apply is done — `glossary.md` is
> now written to the ratified vocabulary (incl. D13–D19 and the cut retired-footnote) and the
> harness is green. The draft wording below is the pre-application record; where it disagrees with
> `glossary.md`, **the live file wins** (notably: folding-condition / standard / gated / watched /
> **trace** per D17+D19; card kinds per D18). Read `glossary.md` for the current text.

### New entries (the terms we coined / settled)

- **episode** — a bounded run with its own context: it opens fresh, the work happens, it clears
  at the end, carrying nothing forward; the machine keeps no memory between episodes, so
  durability lives on the graph. Its two kinds are the **thread** and the **run**.
- **run** — an *autonomous* episode: work carried end to end by a worker advancing the graph,
  no operator in the loop.
- **complexity debt** — built code grown long or tangled enough to want restructuring (made
  deeper). Surfaced live by the architecture review; distinct from the **gap** (not-yet-built)
  and from statement debt (unendorsed statements, §100).
- **coherence** — the principle that the operator's and the machine's decisions hold together;
  when they stop making sense as a whole, the machine says so rather than silently applying the
  newest word (§84).
- **contract check** — the architect's judgment, at the archive gate, that a run's result
  honored its contract before it folds. A check at the operator's altitude, not a code review.
- **standard** — one of the quality practices finished work must meet before the system trusts
  it enough to fold. Every standard is either **gated** or **watched**.
- **gated** — of a standard: enforced by a check — the fold fails unless it actually happened.
- **watched** — of a standard: not enforceable by a check, so it rests on the model's judgment
  and the operator watches it; honestly recorded as not mechanically enforced.
- **module depth judgment** — the watched standard: the model's call on whether a module is
  genuinely deep, not merely short. Not yet built (ADR 0006); length raises a decision, never a
  verdict.
- **fence** — the isolated place a worker runs: its own writable git worktree, the rest of the
  host read-only, the shared history writable so its commits reach the one record. The fence is
  the system's, not a convention a worker could break.
- **seam** — the boundary a clean cut falls on, judged on where it lets checks and abstractions
  stand. Two scales: in work, where an ask splits into child graphs; in code, where an interface
  boundary falls.
- **OMP** — the multi-model harness the worker runs under, so it can run a different model from
  the architect (the operator's ratified spend decision, ADR 0009). The worker model is OpenAI
  GPT-5.5 (xhigh); `omp` is the binary, OMP the concept.
- **vocabulary check** *(D16)* — a delegated, fold-time standard: a dedicated run reads the whole
  live corpus for new or conflicting terms and, on a finding, raises a *define / waive / dismiss*
  decision and holds the fold. Mechanical floor gated, semantic judgment watched. It is
  **communication's consistency standard** (D15).

### New entries (engine terms, per D0) — PENDING operator review

> The operator has not yet vetted these; wording is provisional ("We'll have to go over the
> engine terms"). Several names are themselves candidates for change (see Open items).

- **scheduler** — the loop that reads the **frontier** and runs work off the operator's input
  loop: continuous and concurrent, idling only on a decision.
- **ready work** *(was "ready frontier"/"schedulable frontier" — D14)* — the standing work a run
  can take now: open, folding condition named, nothing open beneath it; read live off the tree
  (`tree.ready()`), never a stored list. The takeable subset of **standing work**.
- **transport** — the one call to a model and the one read of its reply; the architect's runs at
  the repo root, the worker's at its fence. Injectable, so the system runs deterministically
  under the harness.
- **record** — the single-writer durable floor: an atomic write then a scoped commit, one writer
  at a time, so concurrent fences serialize onto the one history.
- **single-writer** — the invariant that the shared git history admits one git-touching act at a
  time (a repo-level lock spanning write→commit).
- **isolation** — the concurrency model: each worker fenced in its own worktree, unable to reach
  a sibling's tree or the main line until its result integrates.
- **anchor** — the minimal always-on shared agents file both roles auto-load, carrying only
  non-inferable operational content; a derived channel re-rendered on fold, reached by Claude
  Code through a derived CLAUDE.md bridge.
- **hand-off** — the worker's complete machine-facing result handed to the architect (its report,
  refined delta, executed loop, and fence); never operator-facing.
- **self-model** — the system's maintained model of itself, rendered two ways: the living spec
  (for the agent) and the operator view (for the operator); kept current as a byproduct of
  folding.
- **execution tree** *(was "execution graph" — D13)* — a dynamically composed workflow: a node's
  ask, carried out, grows a **subtree** of further nodes (steps, candidates, checks, result). Single
  parent by construction (folder containment); recursive, never a general graph. "The tree" for short
  — never "work tree" (collides with the git **worktree**).
- **decomposition** — splitting an ask into **child nodes** as-needed, where a check can stand; a
  seam cut when work reaches it, never drawn ahead in full.
- **dispatch** — the act that hands a ready node to a run, taking it *in flight*. (Was "delegate".)
- **integrate** — the architect's archive-gate act: run the contract check on a hand-off and, on
  a pass, fold the delta in the same act.
- **ratify** — the operator's blessing of extracted/drafted intent: turns a drafted contract into
  standing work. A sibling of approve / cut / explain.
- **registry** — a collection the system keeps (the methodologies, the linked project folders) —
  unambiguous now that "register" is retired.
- **node states** — the live states a node wears: **standing** (open work), **in flight** (a run
  is on it), **awaiting you** (a card), **grilling** (under intent extraction), **done** (folded).
  `dispatch` is the act that takes a node to *in flight*, not a state.

### Refits to existing entries

- **thread** → "an *operator episode*: the throwaway conversation the operator opens by speaking
  and closes when done; no durable state, not bound to a piece of work." (drops "session")
- **card** → its **kind** (decision / request for approval / grilling question / ratification)
  replaces the "weight" language.
- **gap** → "the difference between vision and as-built: what is wanted but not yet built." (drops
  the "= the backlog" equation)
- **worktree** → "the git mechanism behind the **fence**."
- **accepted length / the ratchet** → the record keyword `depth-decision: …accepted@N` becomes
  `accepted: …@N`. (absorbs "depth-accepted")
- **length signal** → "raises a **decision** (re-cut / deepen / accept-with-reason)." (drops
  "depth decision")
- **architecture review** → "deepening backlog" replaced by "complexity debt".
- **architect** / **worker** → "depth disciplines" → "depth standards"; the archive-gate
  judgment → "runs the **contract check**".
- **folding condition** → "depth decision" → "a decision"; align with standard / gated / watched.

### Retired terms
**session** · **weight** · **register** · **discipline** · **deepening backlog** ·
**depth decision** · **depth verdict** · **delegate** (→ dispatch) · ~~schedulable frontier~~

### Prose-only fix
depth.md: *"a module encapsulates a design decision"* → *"a module hides a decision — a format,
a data structure, an algorithm"* (an **encapsulated decision**), freeing the bare phrase.

---

## Rename map (spec + code)

- `register:` lines / "register" / "discipline" → the register holds the **folding conditions**
  (umbrella, D17). Rename `register: <name> — <gated|watched> — <how>` → `folding-condition:
  <name> — <gated|watched> — <how>`; "discipline" retired; **standard** kept (D17) for the
  quality-practice subset in prose. — `spec/folding-conditions.md`, `engine/check/slice21.py`
  (parse the new prefix; still assert 4 gated + 4 watched), `engine/worker.py`.
- "deepening backlog" → **complexity debt** — `engine/review.py`, `engine/view.py`,
  `spec/architecture-review.md`, `spec/self-model.md`, glossary.
- "depth decision" → "a decision"; "depth verdict" → **module depth judgment**;
  `depth-decision: …accepted@N` → `accepted: …@N` — `engine/conditions.py`, `engine/review.py`,
  `spec/folding-conditions.md`, glossary.
- `graph.delegate` → **dispatch** — `engine/graph.py`, callers, `spec/*`.
- "schedulable frontier" → **frontier** (final name pending) — `engine/graph.py`,
  `spec/schedule.md`.
- worker model `"gpt-5.2"` → `"gpt-5.5"` (xhigh) — `engine/transport.py` (+ correct the two ADRs
  that say GPT-5.5 are right).
- `conversation` capability/module → **communication** (pending the scope grilling) —
  `spec/conversation.md`, `engine/conversation.py`, ADR refs.
- **graph → tree** (D13, D14) — "graph" / "execution graph" → **tree** / **execution tree** across
  prose: `README.md`, `intent.md` (§structure / §work), `spec/*`, glossary, docstrings. The data
  structure is unchanged (single `parent`, folder containment). **Module rename confirmed** (D14):
  `engine/graph.py` → `engine/tree.py`, and every `graph.` call-site → `tree.` (the imports in
  `worker.py`, `schedule.py`, `view.py`, `review.py`, `engine/check/*`, etc.). Guard: never produce
  "work tree" (reserved for the git **worktree**). "schedulable frontier" / "ready frontier" → **ready
  work**; `graph.ready()` → `tree.ready()`.

## Intent rewordings (operator-ratifiable)

- §26 — drop "weight of the card"; speak of the card's **kind** carrying different information.
- §60 / §62 — "a session is on it" / "more than one session advances the graph" → **worker** /
  **run** (a session is operator-present; an autonomous unit is a run).

## Build-work this spawns (separate graphs, not glossary edits)

1. **operator-view readiness surface** — the original ask: render the gated/watched standards
   honest-list + the never-run-live status; split `gap` (not-yet-built) from `complexity debt`.
2. **card `kind`** — record it on the node (decision / request for approval / grilling question /
   ratification); the render reads it instead of guessing.
3. **the delegated vocabulary check** (D11/D16) — dedicated fold-time run; raises a decision. This
   is communication's *consistency* standard (D15).
4. **the communication capability expansion** (D15) — rename `conversation`→`communication`; add the
   clarity intent (watched principle) + author the new **`communication` skill** (the readability
   literature); register it in the methodology registry. The rename itself is in the rename map;
   the *clarity intent + skill* is new build.

---

## OPEN — to settle on resume

**ALL RESOLVED (2026-06-22 session 2).** D13 (graph→tree), D14 (ready work), D15 (communication
scope), D16 (vocabulary check name), and the engine-term review (#5) closed the five open items;
D17/D18/D19 then refined the folding-condition model (umbrella → standards aren't conditions, their
**traces** are) and added the **acceptance** card kind. The decision record is complete and ratified.
**Apply phase: STAGES 1–2 DONE** — `glossary.md` rewritten (stage 1) + full rename map executed across
spec/engine/checks/derived-channels (stage 2), `--check` green (260 pass), still uncommitted. Stages 3–5
pending (intent ratification, file build-work nodes, fold) — see Resume.

1. ~~**vocabulary-check name**~~ — **RESOLVED → D16: vocabulary check.**
2. ~~**"ready frontier" rename**~~ — **RESOLVED → D14: ready work** (the takeable subset of standing
   work; matches `tree.ready()`).
3. ~~**communication capability (D12)**~~ — **RESOLVED → D15.** Rename `conversation`→**communication**;
   clarity = *watched* (principle in spec + a loaded `communication` skill carrying the readability
   literature; no gated metrics), consistency = *gated floor + watched* (the **vocabulary check**, D16).
   Thread stays (run↔schedule, thread↔communication). The clarity *intent + skill* is new build
   (build-work #4) and still wants its own grilling/authoring; the rename is in the rename map.
4. ~~**graph/node abstraction**~~ — **RESOLVED → D13.** It was a vocabulary over-claim, not an
   architectural defect: the structure is a tree by construction and flat in practice. Renamed
   graph→tree, recursion kept. (a) was the right read — decomposition is tree-like, not graph-like.
5. ~~**engine-term review pass**~~ — **RESOLVED.** Triaged: most ratified as-is (transport, record,
   scheduler, integrate, hand-off, self-model, anchor, registry, dispatch, ratify, single-writer,
   isolation, node states, fence, seam). Two stake-bearing ones resolved → D13 (graph→tree) and D14
   (ready work). The `single-writer / isolation / record` overlap checked against the corpus: three
   distinct, ratified, layered terms (intent §62, spec/worker.md, spec/schedule.md, ADR 0022) — kept
   all three; `fence` (place) stays distinct from `isolation` (the concurrency property). Engine
   terms are no longer "PENDING" — they're reviewed.

## Resume instructions

After compaction / in a fresh session, re-read **this file** + **`glossary.md`** to restore the
full state. The apply runs in five stages; **stages 1–2 are DONE and green** (260 checks pass).

1. ~~**Rewrite `glossary.md`**~~ — **DONE** (live file is authoritative; harness green).
2. ~~**Execute the rename map** across `spec/` + `engine/` + checks~~ — **DONE (session 3).** All nine
   renames applied and `python3 -m engine --check` green:
   - `gpt-5.2`→`gpt-5.5` (transport.py); `register:`→**`standard:`** (see judgment call below) +
     slug `depth-verdict`→`module-depth-judgment`; `deepening backlog`→`complexity debt`;
     `depth decision`→`a decision`, `depth verdict`→`module depth judgment`, record keyword
     `depth-decision: <p> accepted@<N>`→**`accepted: <p> @<N>`** (conditions.py parser + all
     producers/consumers); `depth disciplines`→`depth standards`; `delegate`→`dispatch`;
     `schedulable/ready frontier`→`ready work`; `conversation`→`communication` (module + capability,
     `git mv`); `graph`→`tree` (module `engine/graph.py`→`engine/tree.py` + capability + prose).
   - Derived channels re-materialized (`channels.materialize()`): AGENTS.md, CLAUDE.md, skills/,
     .claude/skills/ all current.
   - **STILL UNCOMMITTED** — working tree only; `git status` shows the renames as `R` moves.

   **Judgment calls made in session 3 (flag to operator):**
   - **`standard:` not `folding-condition:`** for the gated/watched register lines (spec/folding-
     conditions.md, slice21 parser). The rename map's literal said `folding-condition:`, but the
     ratified D19 glossary says *"a standard is **not** itself a folding condition — its evidence is."*
     So labelling each line `folding-condition:` would contradict the live glossary; the register
     classifies **standards**. Per the STATUS box ("live glossary wins"), chose `standard:`.
   - **ADRs (`spec/decisions/*`) treated as historical record** — swept only the live operative corpus
     (live `spec/<cap>.md`, README, glossary, engine, derived channels, checks), NOT ADR bodies.
     Rewriting "graph" inside `0011-graph-on-disk-is-the-folder.md` would falsify the decision record.
     Reversible: a full-corpus ADR sweep can be a follow-up if the operator wants history rewritten too.
   - **`graph`→`tree` surfaced a name collision**: worktree-path locals named `tree` collided with the
     renamed module. Renamed those locals to **`fence`** (worker.py, design.py, slices 4/5/7/9/18/23) —
     vocabulary-correct per D7 (the worktree *is* the fence). The dependency-graph in `review.py`
     (`import graph`, has cycles by nature) was **kept** as "graph" (not the execution tree).
   - **`intent.md` NOT touched** (operator-owned) — deferred to stage 3 below.

3. **Intent rewordings — DRAFTED, awaiting operator ratification** (intent.md is operator-owned; do not
   apply unilaterally). The changes needed, by section:
   - **§26** — drop "weight of the card"; the card's **kind** carries it. The five kinds (D18):
     decision · request for approval · grilling question · ratification · acceptance.
   - **§60 / §62** — "a session is on it" / "more than one session advances the one graph" →
     "a **run** is on it" / "more than one **run** advances the one **tree**" (D1: autonomous episode =
     run; session retired). Also §16 "a session's conversation" → "an **episode's** conversation";
     §50/§52 "a running session" → a **run** / a live worker.
   - **§110** — "the **ready frontier**" → "the **ready work**" (D14); "graph"→"tree".
   - **graph→tree across intent** (16 occurrences: §14, §70, §104, §106, §108, §112, §116, §118, etc.) —
     "execution graph"→"execution tree", "a graph"→"a tree", "child graph"→"child tree". Keep the
     common noun "conversation" (a dialogue) and "thread"; only the *capability/structure* terms change.
   - **New communication clarity intent (D15)** — a *watched* clarity principle (readability lives in a
     new `communication` skill, no gated metrics). This is **build-work #4**, not a one-line reword —
     spin it out, don't inline it here.
4. **File the four build-work nodes** (see "Build-work this spawns") as standing asks under `work/`
   (mirror `work/vocabulary-sweep/intent.md` frontmatter). Note D19: watched standards must emit a
   **trace** and the fold must check its presence (folds into build-work #1/#3).
5. **Fold** this node (`work/vocabulary-sweep/`) once stage 3 is ratified + applied and `--check` is
   green. The node's own `intent.md` folding condition lists the five open items as a gate — all
   resolved (D13–D19), so treat that clause as satisfied; the remaining real gate is **intent.md
   updated** (stage 3) + build-work filed (stage 4).
