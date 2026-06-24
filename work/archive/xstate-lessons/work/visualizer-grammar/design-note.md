# design note — the two-layer visualizer grammar (for the unbuilt §44 reasoning-visual)

**Status: design note, material on this node.** Not a spec, not a delta, not an edit to intent §44 —
the authored vision is the operator's to write. This is provenance the future §44 build reads, so the
one inheritable lesson from the xstate study outlives the disposable thread that found it. Provenance:
`../../study.md` (the full xstate inheritance read); the lesson here depends on nothing else in this
tree.

§44, the vision this serves: *"A key, pressed on any visible element tied to a model's working,
spawns a live visual of that model's reasoning — its shape, seen from several angles, in real time …
a pull the operator makes on purpose, not a push."*

## The one inherited move

**Draw the fixed topology once; overlay the live position on it.** One picture, two readings — the
*shape* (what can happen) and *where execution sits right now* (what is happening). This is the whole
yield of xstate's visual tooling, and it is worth stealing. But it has a precondition that decides
everything below: **it works only where a topology is fixed.** A picture of "all the states and the
legal moves between them" can only be drawn ahead of time if the states and moves are known ahead of
time.

hypercore has two layers, and they fall on opposite sides of that precondition. Conflating them is the
mistake to design against.

## Layer A — node lifecycle + supervision (fixed → borrow the chart wholesale)

A node wears a small, **fixed** set of states (standing → in flight → awaiting-you | done, plus
grilling); the scheduler supervises workers; a worker is an invoked child with two total exits
(integrate-and-fold, or escalate). This topology is known ahead of time and never grows. So:

- **Borrow the static chart + live highlight directly.** Draw the five states and the legal
  transitions once; light the one a given node is in. The overlay answers *"what is happening to
  **this** node, and what can happen next."*
- It is small enough to draw by hand and never needs an editor — it is authored once and is done.

## Layer B — the execution tree (grown → borrow the inspector, never the editor)

The execution tree is a **dynamically composed workflow, not a fixed template** (intent §104). Its
shape *is* the runtime state: it grows as work decomposes, and it cannot be declared ahead. There is
no chart to draw, because the topology does not exist until the work creates it. So:

- **Do not reach for the statechart editor here** — there is nothing fixed to lay out, and §104
  forbids pre-drawing it. Borrowing the chart metaphor for Layer B is the category error.
- **Borrow the live actor-tree (the inspector model):** a tree that grows as work decomposes, lights
  as runs land, and collapses as subtrees fold. The picture is the live tree itself, projected — not a
  diagram of a tree that was planned.

## The visual grammar to steal regardless of layer

These carry over to both readings and are worth fixing as house style for the build:

- **Events on the edges.** Every move shows its cause — *dispatch / integrate / escalate / settle*. A
  transition without its trigger named is half a picture.
- **Hierarchy as containment; fold as collapse.** A subtree is drawn inside its parent; the archive is
  a collapsed subtree. Folding is visually *closing a box*, which matches what it is.
- **Guards shown, with the unmet clause named.** "Why isn't this running?" must be answerable from the
  picture — show the guard and which clause is open (the visual form of intent §60: an idle system
  with unblocked work is a defect, so the picture must always say *why* something is idle).
- **The event log as the time axis.** The folded steps *are* the history. "Several angles" (§44) =
  project the one tree by **structure / state / owner / time** — the time projection is the log read
  as an axis.

## What to decline — xstate's altitude

xstate's tools are a **developer** instrument: they show state IDs, function names, machine internals.
§44 and "operator legibility is king" put hypercore's visual at the **operator's** altitude — operator
words on the edges, the *shape* of a model's reasoning, not its call stack. Inherit the *grammar*
(topology-once + overlay-live, events-on-edges, containment, guards-shown, log-as-axis); decline the
*altitude*.

One consequence for the build's weighting: §44's "several angles, in real time, a pull not a push"
describes the **inspector**, not the **editor**. The operator is tuning in to live reasoning, not
authoring a machine. Weight the §44 build toward **live inspection of the running tree**, and keep the
fixed-topology chart (Layer A) as the small, static companion it is.
