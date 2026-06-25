# glossary

The ubiquitous language — terms only, devoid of implementation detail. One name
means one concept, system-wide; a use that conflicts with an entry is surfaced,
not silently absorbed. This is the seed, distilled from `intent.md`; thereafter
it sharpens inside grilling as work folds, and the **vocabulary check** guards it
against drift each time new words join the live corpus.

- **tree** — the one model: nodes, the parent→child relations between them, and the
  material attached to them. A **tree** by construction — each node has exactly one
  parent, its enclosing folder, so multiple parents, cross-edges, and cycles are
  impossible. Everything the operator sees is a view of this one tree.

- **node** — a point on the tree carrying one operation and, for a statement, its
  endorsement state. The unit on disk is the folder — a node with its subtree —
  not the bare node.

- **operation** — one move on the problem state, of four kinds: **ask** (an
  intent to carry out), **check** (an observation that lets a node fold),
  **decide** (a fork the operator settles), **do** (a move that makes material).

- **material** — what the work makes, as opposed to the intent that started it.

- **statement** — a plain, declarative claim, strong enough to be wrong, that one
  party owns and answers for. If it doesn't matter enough for the operator to
  hear about it, it isn't a statement.

- **endorsement** — who answers for a statement. **Endorsed** is the operator's
  responsibility; **unendorsed** is the machine's. Material answers to whoever is
  responsible for the statement behind it.

- **[machine] marker** — the visible sign, carried in the file itself, that a
  statement is machine-owned and awaits the operator. **approve** drops it, **cut**
  removes the words, **explain** has the machine help the operator toward a decision
  and returns the statement.

- **card** — a node awaiting the operator, surfaced on the queue. Its **kind** matches
  the call — a **grilling question** (answered during intent extraction), a
  **ratification** (blessing drafted intent into work), a **request for approval** (a go
  on a step), a **decision** (settling a fork), or an **acceptance** (signing off that
  done work meets its bar) — recorded on the node, not guessed at render time. Ratification
  and acceptance are bookends: bless the intent, accept the result.

- **queue** — the operator's decision surface, and a *view*, not a place: it is
  every awaiting node read fresh, never a list kept in sync.

- **episode** — a bounded run with its own context: it opens fresh, the work
  happens, it clears at the end, carrying nothing forward; the machine keeps no
  memory between episodes, so durability lives on the **tree**. Its two kinds are
  the **thread** and the **run**.

- **thread** — an **operator episode**: the throwaway conversation the operator
  opens by speaking and closes when they have what they came for. It holds **no
  durable state** and is **not bound to a piece of work**; durability lives on the tree.

- **run** — an **autonomous episode**: work carried end to end by a worker
  advancing the tree, no operator in the loop.

- **architect** — the operator-facing half of the split, and the holder of design
  judgment (renamed from *conversationalist* in slice 7). It owns every word that
  crosses to the operator, reads the operator's words and lands one concrete
  consequence, **authors the spec delta** (the design of the change), and runs the
  **contract check** at the archive gate — raising a decision rather than a silent
  veto. Communicating a design is part of designing it. Structurally opposed to the
  worker's investment in its own product, which is the defense against self-judging.

- **worker** — the system-facing half of the split: it carries out a spawned ask,
  fenced in its own worktree, grounded in its capability's spec slice **and in the
  depth standards** so it builds deep up front, and hands the architect a technical
  result. It has **no channel to the operator**; its audience is the architect and the spec.

- **communication** — the capability that owns the operator-facing channel end to
  end: the **thread** it happens in, the single operator-facing **voice** (every word
  comes from the architect), and the quality of what crosses it — **clear** (a
  *watched* standard; the readability literature lives in the `communication` skill)
  and **consistent** (the **vocabulary check**). Renamed from *conversation*.

- **fence** — the isolated place a worker runs: its own writable git **worktree**,
  the rest of the host read-only, the shared history writable so its commits reach
  the one **record**. The fence is the system's, not a convention a worker could break.

- **worktree** — the git mechanism behind the **fence**: a worker's own checkout on
  its own branch, isolated from sibling workers and the main line. The worker builds
  here and its commits reach the one record without touching another tree until the
  result integrates.

- **isolation** — the concurrency model: each worker fenced in its own worktree,
  unable to reach a sibling's tree or the main line until its result integrates
  (intent §62). Distinct from the **fence** (the place); isolation is the property.

- **single-writer** — the invariant that the shared git history admits one
  git-touching act at a time (a repo-level lock spanning write→commit), so concurrent
  fences serialize onto the one history.

- **record** — the single-writer durable floor: an atomic write then a scoped commit,
  one writer at a time (`engine/record.py`), so concurrent fences fold without
  colliding on the one history.

- **fold** — the act that completes a node: its result becomes its parent's
  material and its steps become history. The same act applies the node's delta to
  the spec and re-renders the operator view.

- **delta** — a node's record of what it changes about the spec: **ADDED**,
  **MODIFIED**, and **REMOVED** requirements. A behavior-changing node carries
  one; a trivial node carries an empty delta and says so.

- **folding condition** — what conditions the fold: the complete set of **deterministic
  checks** plus **traces** that each appropriate judgment procedure was applied. The fold
  rests on evidence, never on unverified trust — anything that is not a hard check must
  leave a trace. A source file past the **length signal** is not one — it raises **a
  decision** (re-cut / deepen / accept-with-reason), never an auto-refusal.

- **standard** — a quality practice the work is held to: deep modules, the contract
  honored, vocabulary consistency. A standard is **not** itself a folding condition —
  what conditions the fold is the **evidence of its application**: a passing deterministic
  check if it is **gated**, a **trace** if it is **watched**.

- **gated** — of a standard or structural fact: its application is verified by a
  deterministic check — the fold fails unless the check passes (the delta applies; the touched
  capability's architect-authored **scenario** goes red→green). A requirement is gated exactly when one
  of its scenarios carries a **check block**; that presence *is* the classification, not a separate
  register.

- **watched** — of a standard: its application takes judgment, so the procedure must
  leave a **trace** — evidence it was applied, which conditions the fold — while its
  *quality* is overseen by the operator; a trace needing sign-off raises an **acceptance** card.

- **trace** — the evidence a **watched** judgment procedure leaves that it was applied
  (a recorded design-decision, a contract-check note, an accepted-length record). Its
  presence is a folding condition; its quality is overseen, not gated.

- **vocabulary check** — a delegated, fold-time standard and **communication's
  consistency** standard: a dedicated run reads the whole live corpus for new or
  conflicting terms and, on a finding, raises a *define / waive / dismiss* decision
  and holds the fold. Mechanical floor **gated**, semantic judgment **watched**.

- **capability** — a coherent slice of system behavior, named in the domain's own
  words, owning a spec file and any local decisions.

- **requirement** — a behavior the system exhibits, stated strongly enough to be
  wrong, carrying one or more scenarios. A requirement is a check that survives its
  node.

- **scenario** — a requirement's worked behavior in WHEN / THEN form: machine-
  checkable and human-legible at once. Where the behavior is mechanically checkable, the scenario
  carries an executable **check block** — domain verbs a deep binding (`scenario`) compiles to a
  runnable assertion — so the scenario *is* the requirement's gate, run red→green; the description and
  the test are one thing, and cannot drift.

- **living spec** — the maintained, version-controlled model of *what the system
  is* (as-built reality), organized by capability, read flat by the agent. Not
  `intent.md`, which is *what is wanted*; the gap between them is what is wanted but
  not yet built.

- **self-model** — the system's maintained model of itself, rendered two ways: the
  **living spec** (for the agent) and the **operator view** (for the operator); kept
  current as a byproduct of folding.

- **operator view** — the operator's render of the self-model: a recursive tree
  setting the **vision** (authored, from `intent.md`) beside the **as-built**
  (derived from the living spec) and the **gap** between them, at every altitude.
  *(Open question: the name. "Operator brief" historically named only the
  as-built render; now that this surface also carries the authored vision, the
  term may want revisiting — flagged, not blocking.)*

- **vision** — the authored, durable statement of what is wanted, whole and not
  capability-segmented, kept in `intent.md`. The one writable region the operator
  steers with.

- **as-built** — what the system actually does, derived from the living spec.

- **gap** — what is wanted but not yet built: the difference between vision and
  as-built, read live. Distinct from **complexity debt** (built but structurally weak).

- **complexity debt** — built code grown long or tangled enough to want restructuring
  (made deeper). Surfaced live by the architecture review; distinct from the **gap**
  (not-yet-built) and from statement debt (unendorsed statements, §100).

- **derived channel** — a grounding channel **rendered from one source**, never hand-copied:
  the worker's depth grounding and the `depth` **skill** both render from
  `spec/depth.md`. Like the **as-built**, a derived channel changes when its source changes,
  so a frozen second copy (the retired `worker.DEPTH` constant) cannot drift. Materialized on
  disk when an external harness must auto-load it (a skill, an agents file); read live otherwise.

- **anchor** — the minimal always-on shared agents file both roles auto-load,
  carrying only non-inferable operational content; a **derived channel** re-rendered
  on fold, reached by Claude Code through a derived `CLAUDE.md` bridge.

- **hand-off** — the worker's complete machine-facing result handed to the architect
  (its report, refined delta, and fence); never operator-facing — the architect authors every
  operator-facing word from it. It carries **no loop**: the check that judges it is the architect's
  own scenario, run red→green by the gate over its fence.

- **architecture review** — the standing scan of the source tree for **complexity
  debt**, read live. It surfaces god-files-in-the-making before they set and
  renders the operator view's upper levels — the structural map of as-built reality,
  debt marked — so the operator reads the system's shape without reading code. It
  measures **length** (the built signal) and is meant to grow the model-driven
  **red-flag depth scan**, recorded as not-yet-built.

- **recommendation strength** — the weight a **complexity-debt** finding carries: **strong**
  (assess/deepen now) for a module past the length signal, **consider** for one nearing it.

- **deep module** — a module that hides a lot of behavior behind a small interface;
  hypercore's positive criterion for structure (Ousterhout, `spec/depth.md`). Its
  opposite is a **shallow module**. A simple interface matters more than a simple
  implementation — interface cost is paid by every caller forever — so *pull complexity
  downward*: when something must be hard, make it hard inside the module.

- **shallow module** — a module whose interface is nearly as complicated as the
  implementation it fronts; it costs the reader almost as much as no module at all. The
  #1 **red flag**, and what a length *floor* (over-decomposition) and an un-deepened
  length *ceiling* both produce.

- **depth** — how much functionality is hidden behind how small an interface; the
  criterion the constraints are read in. A judgment, not a number — the system raises it
  as a decision, never enforces it as a threshold.

- **context cost** — what a module costs an agent's window to load: every line is
  context the worker must hold. hypercore's own concern, distinct from depth, for which
  **length** is a fair mechanical proxy. The honest job length is kept for.

- **length signal** — the line count past which a touched source file raises **a
  decision** (a starting value to tune). It is a *signal* of depth and a measure of
  context cost, **never an auto-refusal** and never a verdict on depth — there is no
  hard length ceiling above it.

- **accepted length / the ratchet** — the length `<N>` an **accepted-length record** grants
  a file, written as a parseable `accepted: <path> @<N> — …` line that names the
  exact file and the length it is accepted at, so a coincidental mention grants no exception
  (the spelling is not the decision). Acceptance is **bounded** to it, not granted forever: it
  clears the gate only while the file stays within `<N>` plus a small **materiality margin**, so
  a stable or shrinking file stays quiet but renewed growth materially past the bar re-opens the
  decision. Renewing the acceptance at the new length **ratchets** the bar up; the bar lives in
  the record (a shrink never lowers it), and the highest recorded length governs.

- **module depth judgment** — the *watched* standard: the model's call on whether a module
  is genuinely deep, not merely short. Not yet built; length raises a decision,
  never a verdict.

- **exceeded acceptance** — a file past the length signal that *was* accepted at a lower length
  and has since outgrown it (the architecture review's `exceeded` status). The acceptance is
  **stale**: the file returns to the **complexity debt**, marked as having outgrown its bar — read
  differently from a never-decided over-signal file (`over`), so a settled-then-grown decision is
  visibly distinct from one never made.

- **red flag** — a named symptom that code is more complex than it needs to be
  (Ousterhout): shallow module, information leakage, temporal decomposition, pass-through
  method, special-general mixture, conjoined methods, repetition, comment-repeats-code,
  vague or hard-to-pick name, nonobvious code. Each a smell a judge weighs, none a
  threshold a tool measures — the lens the architecture review is meant to grow.

- **strategic / tactical programming** — *tactical*: optimize for the next feature
  working, letting complexity accrete a tolerable bit at a time. *Strategic*: treat
  working code as not enough and invest in the design that keeps the system cheap to
  change. The worker is grounded to be strategic — to build deep up front.

- **design-it-twice** — the judgment use of the worktree concurrency: for a load-bearing
  interface, designing the decision several ways in parallel before committing one, then picking
  the deepest (Ousterhout). The fence that isolates a worker for throughput
  isolates several candidates for design quality.

- **design contest** — the run of design-it-twice on one decision: a set of candidates, the
  architect's comparison, and the recorded pick. It is not a node kind; it is several fenced
  candidates under one decision.

- **candidate** — one shape in a design contest: a design built to one **design brief**, in its
  own fence, isolated from its siblings. It produces an interface **design**, not an
  implementation — the interface, what it hides, the seam, and the depth argument.

- **design brief** — the instruction that pushes a candidate toward a radically different shape:
  minimize the interface / maximize flexibility / optimize the common caller / ports-and-adapters.
  Different briefs make the contest span real alternatives.

- **design-decision** — the architect's machine-side pick among candidates, recorded as a
  structured `design-decision: <subject> → <chosen> — <reason>` line in the contest node's
  material — the same structured-record idiom the **accepted-length record** uses. A load-bearing
  interface choice is hard to reverse, so it is recorded on the node and archives with the work; the
  operator sees it only when the comparison reveals a stake-bearing difference (the standing-guard
  floor).

- **seam** — the boundary a clean cut falls on, judged on where it lets checks and abstractions
  stand. Two scales: in work, where an ask splits into child nodes (a subtree); in code, where
  an interface boundary falls.

- **coherence** — the principle that the operator's and the machine's decisions hold together;
  when they stop making sense as a whole, the machine says so rather than silently applying the
  newest word (§84).

- **contract check** — the architect's judgment, at the archive gate, that a run's result
  honored its **contract** before it folds. A check at the operator's altitude, not a code review.

- **scheduler** — the loop that reads **ready work** and runs it off the operator's input loop:
  continuous and concurrent, idling only on a decision.

- **ready work** — the standing work a run can take now: open, its folding condition named,
  nothing open beneath it; read live off the tree (`tree.ready()`), never a stored list. The
  takeable subset of **standing work**.

- **execution tree** — a dynamically composed workflow: a node's ask, carried out, grows a
  **subtree** of further nodes (steps, candidates, checks, result). "The tree" for short —
  never "work tree" (reserved for the git **worktree**).

- **decomposition** — splitting an ask into **child nodes** as-needed, where a check can stand;
  a **seam** cut when work reaches it, never drawn ahead in full.

- **dispatch** — the act that hands a ready node to a run, taking it *in flight*. (Renamed
  from *delegate*.)

- **integrate** — the architect's archive-gate act: run the **contract check** on a hand-off
  and, on a pass, fold the delta in the same act.

- **ratify** — the operator's blessing of extracted/drafted intent: turns a drafted contract
  into standing work. A sibling of approve / cut / explain.

- **node states** — the live states a node wears: **standing** (open work), **in flight** (a run
  is on it), **awaiting you** (a card), **grilling** (under intent extraction), **done** (folded).
  `dispatch` is the act that takes a node to *in flight*, not a state.

- **transport** — the one call to a model and the one read of its reply; the architect's runs at
  the repo root, the worker's at its fence. Injectable, so the system runs deterministically
  under the harness.

- **registry** — a collection the system keeps (the methodologies, the linked project folders).

- **codex** — the coding agent the worker runs under, so it can run a different model from
  the architect (the operator's ratified spend decision). codex returns its reply through an
  `-o` file (not stdout) and blocks on an open stdin; `engine/codex.py` holds that shape so the
  rest of the engine learns none of it. The worker model is OpenAI GPT-5.5, on codex's own auth.
