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

- **conversationalist** — the single voice between the operator and the system. It
  owns every word that crosses to the operator, reads the operator's words, and
  lands one concrete consequence.

- **fold** — the act that completes a graph: its result becomes its parent's
  material and its steps become history. The same act applies the graph's delta to
  the spec and re-renders the operator view.

- **delta** — a graph's record of what it changes about the spec: **ADDED**,
  **MODIFIED**, and **REMOVED** requirements. A behavior-changing graph carries
  one; a trivial graph carries an empty delta and says so.

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

- **ADR** — a recorded decision, kept sparingly: only when it is hard to reverse,
  surprising without context, and the result of a real trade-off.
