# hypercore

hypercore is a way to keep a growing codebase coherent when the machine starts each
session with no memory.

The method has three tests:

- **scrutable**: a reader can recover what the system means.
- **sound**: nothing important rests on unproven ground.
- **fast**: work moves in small steps with little ceremony.

When those tests pull against each other, name the tension instead of hiding the tradeoff.

```text
operator purpose + written intent + checked material
        \              |              /
         \             |             /
          ---------- hypercore -------
```

## intent

Intent is the current written model of the system: what each part is meant to be, how it
behaves, and what it depends on.

It does not carry memory or rationale. The reason a statement exists lives in the work
that made it. The proof lives in checks on the material.

```text
intent says:     what is meant to be true
work records:    why this became true
checks prove:    whether the material still holds it
```

Work starts by reading the intent and the material. If something needed is not written,
it is not assumed.

## collaboration

The operator and the machine keep common ground written.

- The operator sets purpose, constraints, acceptance, and open direction.
- The machine searches, synthesizes, drafts, executes, checks, and settles what is left
  open.
- The machine makes uncertainty, evidence, limits, and failure modes visible enough for
  the operator to rely on it, challenge it, redirect it, or stop it.
- When written ground is insufficient, the machine records the blocker and stops instead
  of fabricating content.

Feedback becomes durable: corrections, discovered facts, failed checks, and sweep flags
become intent, proof, machine statements, or debt.

## nodes

A node is a governed corpus. The root is a node; any node-local corpus entry with
`intent/` can be a child node too.

```text
node/
  intent/
    organizing-document.md
    <segment>.md
    machine-statements/<segment>.md
    history/
  leaf material
  child nodes
  active work nodes
```

The node boundary matters. A child is free except where a parent statement explicitly
reaches into it.

```text
parent node
  statement reach:
    node-local        -> parent only
    named child       -> one child
    direct children   -> every immediate child
    descendants       -> the tree below
```

An unmaterialized child slot is dormant. Do not invent its content.

## segments

Each node chooses its own segments in `intent/organizing-document.md`.

At the methodology root, the methodology has nine segments:

- foundations
- collaboration
- structure
- statements
- endorsement
- active-work
- loop
- sweep
- adapter

The governed work group names durable child nodes and mounted work governed by this root.

Each segment has:

- `intent/<segment>.md` for current statements.
- `intent/machine-statements/<segment>.md` for machine statements.

The methodology prose is this file. The mechanical check over nodes is `check.sh`.

## statements

A statement is plain, declarative, and strong enough to be wrong.

```text
good statement:  check.sh checks every node in the tree.
weak statement:  checks should probably cover most important things.
```

One name means one concept. Behavior and dependency are both written as statements.

Every statement must be ownable and checkable. If it is neither, the work turns it away.

## ownership

Ownership is the right to change a statement, not permission to break it.

```text
endorsed statement   -> operator owned
unendorsed statement -> machine owned
```

The machine never endorses, so unendorsed statements fall to the machine by default. Both
operator and machine are still bound by coherence.

Machine freedom is taken, not declared: when the operator leaves a choice open and the
machine settles it, the machine statement records that settlement.

## endorsement

Endorsement is per segment and per node.

```text
intent/<segment>.md

... statements ...

## machine
... machine statements ...

---
endorsed by <operator>
```

Changing a segment means taking on the segment's whole operator set. There is no partial
endorsement. If a segment becomes too large to own, split it or move suitable statements
under `## machine`.

A work frame carries sign-off. On adoption, that sign-off stamps each touched segment.

## active work

Active work is a child node directly under the addressed node.

```text
002-simplify-methodology-doc/
  intent/
    frame/
```

A work node can propose parent intent or parent material amendments without making them
current. Until adoption accepts the amendment, the parent intent remains current.

Adoption folds accepted child statements and material into the parent and records history.
Shelving records history without changing parent truth.

## loop

Every work node that needs adoption or shelving goes through five gates.

```text
orient -> frame -> implement -> check -> archive
\___ phase one ___/  \______ phase two _____/
          |
       sign-off
```

- **orient**: read the intent, work in flight, and material conventions.
- **frame**: write the problem, constraints, route, proof state, target segments, work in
  flight, and any open decisions.
- **implement**: after sign-off, build from the written frame in small units.
- **check**: run mechanical checks and the sweep.
- **archive**: adopt or shelve according to the signed frame.

The session clears at sign-off. Phase two must be able to re-derive the work from the
frame alone.

## sweep

The sweep checks semantic coherence. It does not replace proof.

```text
map:  where does this concept appear?
read: do those appearances agree?
flag: what must proof or operator judgment settle?
```

The sweep spans current intent, machine statements, material, proposed parent amendments,
work in flight, related work, and node boundaries.

It distinguishes current truth from proposed amendments. A child statement that contradicts
the parent blocks unless the frame presents it as an amendment for adoption.

## adapter

The adapter binds a harness to the methodology.

```text
harness loads adapter -> adapter points to intent + loop -> gates become enforceable
```

For Codex, the root `AGENTS.md` points at the adapter. The adapter does not replace the
intent; it routes the machine to the intent and makes the loop's gates rigid.

Phase one is interactive design work. Phase two is cleared, heads-down execution from the
signed frame. If a gate precondition fails, the adapter blocks instead of warning.

## collisions

Two kinds of collision matter most:

- **Concurrency**: two work nodes touch the same intent. The first adopted work wins; later
  work builds on the adopted or in-flight material it reads.
- **Orthogonality**: one segment is carrying two separable concerns. Fix the taxonomy,
  preferring clearer documents over more mechanism.

If two names are surely one concept, merge them by taking one name out. If the distinction
is real or uncertain, surface it.

## undecided topics

Absence is not a verdict. The corpus is open-world: only what the work leans on must be
grounded.

When the artifacts cannot settle a choice, the machine records the problem, constraints,
and decision surface for the operator. It does not fill the gap with invented content.
