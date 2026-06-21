# glossary

The ubiquitous language — terms only, devoid of implementation detail. One name
means one concept, system-wide; a use that conflicts with an entry is surfaced,
not silently absorbed. This is the seed, distilled from `intent.md`; thereafter
it sharpens inside grilling as work folds.

- **graph** — the one model: nodes, the relations between them, and the material
  attached to them. Everything the operator sees is a view of this one graph.

- **node** — a point on the graph carrying one operation and, for a statement, its
  endorsement state. The unit on disk is the graph (a folder), not the node.

- **operation** — one move on the problem state, of four kinds: **ask** (an
  intent to carry out), **check** (an observation that lets a graph fold),
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

- **card** — a node awaiting the operator, surfaced on the queue. Its weight
  matches the call: a real judgment is a decision; a step needing only the
  operator's go is a lighter request for approval.

- **queue** — the operator's decision surface, and a *view*, not a place: it is
  every awaiting node read fresh, never a list kept in sync.

- **thread** — the throwaway operator-facing vessel for one conversational
  session, opened when the operator types in and closed when they have what they
  came for. It holds **no durable state** and is **not bound to a piece of work**;
  durability lives on the graph. "One session per thread" means the thread simply
  *is* that one session, then closes.

- **architect** — the operator-facing half of the split, and the holder of design
  judgment (renamed from *conversationalist* in slice 7). It owns every word that
  crosses to the operator, reads the operator's words and lands one concrete
  consequence, **authors the spec delta** (the design of the change), and **judges
  depth at the archive gate** — raising a decision on shallowness rather than a silent
  veto. Communicating a design is part of designing it. Structurally opposed to the
  worker's investment in its own product, which is the defense against self-judging.

- **worker** — the system-facing half of the split: it carries out a spawned ask,
  fenced in its own worktree, grounded in its capability's spec slice **and in the
  depth disciplines** so it builds deep up front, and hands the architect a technical
  result. It has **no channel to the operator**; its audience is the architect and the spec.

- **worktree** — the fence a worker runs in: its own git checkout on its own branch,
  isolated from sibling workers and the main line. The worker builds here and its
  commits reach the one record without touching another tree until the result integrates.

- **fold** — the act that completes a graph: its result becomes its parent's
  material and its steps become history. The same act applies the graph's delta to
  the spec and re-renders the operator view.

- **delta** — a graph's record of what it changes about the spec: **ADDED**,
  **MODIFIED**, and **REMOVED** requirements. A behavior-changing graph carries
  one; a trivial graph carries an empty delta and says so.

- **folding condition** — a structural gate a graph must clear to fold. Two are
  **non-negotiable facts** that auto-refuse: its delta applies, and a behavior-changing
  graph carries a recorded **red→green feedback loop**. The third is a **judgment**:
  **depth** — a source file past the **length signal** raises a **depth decision**
  (re-cut / deepen / accept-with-reason), never an auto-refusal on length. An engineering
  discipline made into a check — advice can be ignored, a folding condition cannot. An
  unmet fact returns its reason; the depth condition returns a decision; never a silent pass.

- **capability** — a coherent slice of system behavior, named in the domain's own
  words, owning a spec file and any local decisions.

- **requirement** — a behavior the system exhibits, stated strongly enough to be
  wrong, carrying one or more scenarios. A requirement is a check that survives its
  graph.

- **scenario** — a requirement's worked behavior in WHEN / THEN form: machine-
  checkable and human-legible at once.

- **living spec** — the maintained, version-controlled model of *what the system
  is* (as-built reality), organized by capability, read flat by the agent. Not
  `intent.md`, which is *what is wanted*; the gap between them is the backlog.

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

- **gap** — the difference between vision and as-built; the backlog, read live.

- **architecture review** — the standing scan of the source tree for deepening
  opportunities, read live. It surfaces god-files-in-the-making before they set and
  renders the operator view's upper levels — the structural map of as-built reality,
  debt marked — so the operator reads the system's shape without reading code. It
  measures **length** (the built signal) and is meant to grow the model-driven
  **red-flag depth scan**, recorded as not-yet-built.

- **deepening backlog** — the architecture review's findings, read as the gap: the
  modules grown long or shallow enough to want a depth look, each carrying a
  recommendation strength.

- **recommendation strength** — the weight a deepening finding carries: **strong**
  (assess/deepen now) for a module past the length signal, **consider** for one nearing it.

- **deep module** — a module that hides a lot of behavior behind a small interface;
  hypercore's positive criterion for structure (Ousterhout, `research/aposd.md`). Its
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

- **length signal** — the line count past which a touched source file raises a **depth
  decision** (a starting value to tune). It is a *signal* of depth and a measure of
  context cost, **never an auto-refusal** and never a depth verdict — there is no hard
  length ceiling above it.

- **depth decision** — what the gate raises when a file is past the length signal with
  no depth-decision accepting it *at a length it is still within*: re-cut / deepen /
  accept-with-reason, surfaced to the operator. Recorded, when accepted, as a **structured
  depth-decision** — a parseable `depth-decision: <path> accepted@<N> — …` line that names the
  exact file and the length it is accepted at, so a coincidental mention can grant no exception
  (the spelling is not the decision) and the acceptance is bounded (the ratchet, below).

- **accepted length / the ratchet** — the length `<N>` a structured depth-decision accepts a file
  at (ADR 0008). Acceptance is **bounded** to it, not granted forever: it clears the gate only
  while the file stays within `<N>` plus a small **materiality margin**, so a stable or shrinking
  file stays quiet but renewed growth materially past the bar re-opens the depth decision.
  Renewing the acceptance at the new length **ratchets** the bar up; the bar lives in the record
  (a shrink never lowers it), and the highest recorded length governs (the ratchet only rises).

- **exceeded acceptance** — a file past the length signal that *was* accepted at a lower length
  and has since outgrown it (the architecture review's `exceeded` status). The acceptance is
  **stale**: the file returns to the deepening backlog, marked as having outgrown its bar — read
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
  the deepest (Ousterhout, rebuild-spec §7.5). The fence that isolates a worker for throughput
  isolates several candidates for design quality.

- **design contest** — the run of design-it-twice on one decision: a set of candidates, the
  architect's comparison, and the recorded pick. It is not a node kind; it is several fenced
  candidates under one decision.

- **candidate** — one shape in a design contest: a design built to one **design brief**, in its
  own fence, isolated from its siblings. It produces an interface **design**, not an
  implementation — the interface, what it hides, the seam, and the depth argument.

- **design brief** — the instruction that pushes a candidate toward a radically different shape:
  minimize the interface / maximize flexibility / optimize the common caller / ports-and-adapters
  (rebuild-spec §7.5). Different briefs make the contest span real alternatives.

- **design-decision** — the architect's machine-side pick among candidates, recorded as a
  structured `design-decision: <subject> → <chosen> — <reason>` line in an ADR — the same
  structured-record idiom the depth-decision uses. A load-bearing interface choice is hard to
  reverse, so it is ADR-worthy; the operator sees it only when the comparison reveals a
  stake-bearing difference (the standing-guard floor).

- **ADR** — a recorded decision, kept sparingly: only when it is hard to reverse,
  surprising without context, and the result of a real trade-off.
