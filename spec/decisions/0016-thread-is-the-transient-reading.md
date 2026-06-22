# ADR 0016 — `thread` is the transient conversation; the graph is the work surface

Status: **operator-directed** (2026-06-21) — a coherence pass surfaced that `intent.md` and the
living spec defined `thread` two incompatible ways; the operator chose the transient reading. The
machine-side reconciliation below is the mechanism. [machine]

## Context

`thread` is the system's most-used interface noun ("the thread is the interface's one work
surface"), and it carried two flatly contradictory definitions:

- **`intent.md`** read a thread as **durable** and **bound to work**: every unit of work lives on a
  thread, a card is a view onto its thread, settling folds into its thread "where its decision and
  grounds are kept," a thread "is a durable view… and stays whether or not a session is on it."
- **`glossary.md` and `conversation.md`** read a thread as **throwaway** and **not bound to work**:
  "the throwaway operator-facing vessel for one conversational session… holds no durable state and
  is not bound to a piece of work; durability lives on the graph."

Worse, the *living spec was split against itself*: `conversation` used the throwaway sense while
`interface`, `coherence`, and `worker` used "threads" for the standing-work panel, and the renderer
labelled standing work "threads." The glossary's own first rule — "one name means one concept,
system-wide; a use that conflicts with an entry is surfaced, not silently absorbed" — was violated
by the glossary's own corpus.

## Decision

**A thread is the throwaway conversation, and nothing more.** The transient reading wins:

- A **thread** is one conversational session — opened when the operator speaks, it lands exactly
  one consequence on the graph, and closes. It holds no durable state and is not bound to a piece
  of work. (This is the glossary's and `conversation`'s existing definition, now the only one.)
- The **durable work surface is the graph**; the operator's standing **work** is the second
  principal screen element beside the queue. A card is a view onto its **node**; settling folds
  into that **node**, where its decision and grounds are kept. Durability is the graph's, never the
  thread's. A conversation is still scoped to one node — speaking on a node opens a thread *there* —
  but the scoping rides the node, not a durable thread.

`intent.md`'s durable-thread language is rewritten to this; `interface`/`coherence`/`worker` and the
renderer rename the standing-work panel from "threads" to **work**.

## Grounds

The transient reading is the one the *code already implements* — `conversation.Thread` is a
throwaway in-process session, and durability already lives on the graph folders. Keeping the strong
reading would have meant inventing thread persistence the system deliberately does not have; keeping
the weak reading costs only words. The graph is already "the model… everything the operator sees is
a view of that one graph" (intent), so naming it the work surface is the system saying what it
already is, and frees `thread` to mean one concept.

## Consequences

- `intent.md` §interface/§thread passages rewritten; `spec/interface.md`, `spec/coherence.md`,
  `spec/worker.md` and `engine/render.py`/`engine/graph.py` rename the standing-work view "threads"
  → "work." `spec/conversation.md` and `glossary.md` are unchanged — they already held the surviving
  definition. No behavior changes; the acceptance harness is green.
- "Thread" now names the throwaway conversation everywhere; "work" names the standing arcs; "graph"
  is the durable surface. A future change that gives threads durable state carries an ADR superseding
  this one.
