# hypercore

hypercore is a way to keep a growing codebase coherent when the machine starts each
session without memory.

The method cares about three properties:

- **scrutable**: a reader can recover what the system means.
- **sound**: important claims rest on grounded evidence.
- **fast**: the system avoids ceremony that does not improve understanding or evidence.

When those properties pull against each other, name the tension instead of hiding the
tradeoff.

```text
operator purpose + written intent + grounded material
        \              |              /
         \             |             /
          ---------- hypercore -------
```

## intent

Intent is the current written model of the system: what each part is meant to be, how it
behaves, and what it depends on.

Intent is not memory. It should not carry every reason a statement ever existed. It
should carry the current shape clearly enough that a memoryless reader can continue
without inventing missing ground.

```text
intent says:    what is meant to be true
material shows: what exists
evidence asks:  whether the two still agree
```

If something needed is not written or visible in the material, it is not assumed.

## nodes

A node is a governed corpus. The root is a node; any child corpus with its own `intent/`
can be a node too.

```text
node/
  intent/
    organizing-document.md
    <segment>.md
  leaf material
  child nodes
```

The node boundary matters. A child is free except where a parent statement explicitly
reaches into it.

```text
parent reach:
  node-local      -> the parent only
  named child     -> one child
  direct children -> immediate children
  descendants     -> the tree below
```

An unmaterialized child is a dormant possibility, not an invitation to invent its
content.

## segments

Each node chooses its own segments in `intent/organizing-document.md`. A segment is a
coherent set of statements that can be read and owned together.

The methodology root currently uses these segments:

- foundations
- structure
- statements
- collaboration
- endorsement
- sweep
- decomposition

Segments should split when one document starts carrying separable concerns.

## statements

A statement is plain, declarative, and strong enough to be wrong.

```text
strong: every child node names the parent statements that reach it.
weak: child nodes should probably stay compatible with parents.
```

One name means one concept. Behavior, dependency, boundary, and responsibility are all
written as statements when they matter.

Every statement should have an owner and a possible way to be contradicted by the
material. A statement that is neither ownable nor falsifiable belongs in discussion, not
in intent.

## collaboration

The operator and the machine keep common ground written.

The operator supplies purpose, constraints, taste, risk tolerance, and final judgment.
The machine searches, compares, drafts, implements, questions, and names uncertainty.

The machine should make uncertainty visible enough that the operator can rely on it,
challenge it, redirect it, or stop it. The operator should keep the purpose legible
enough that the machine is not forced to invent it.

Good collaboration is not maximal automation. It is the smallest shared surface that
keeps the work scrutable, sound, and fast.

## endorsement

Endorsement names who stands behind a set of statements.

An endorsed statement is operator-owned. An unendorsed statement is machine-owned until an
operator takes it on. Ownership is the right to change a statement, not permission to
break coherence.

Endorsement is coarse on purpose: if a set is too large to stand behind, split it.

## sweep

The sweep is the semantic coherence pass.

```text
map:  where does this concept appear?
read: do those appearances agree?
flag: what needs evidence, revision, or judgment?
```

The sweep does not prove truth. It finds relationships, collisions, naming drift, hidden
assumptions, and ungrounded claims.

Absence is not a verdict. The corpus is open-world: only what the system leans on must be
grounded.

## decomposition

Large work can be understood by decomposing it into child nodes.

The useful idea is simple: a parent can hold the whole purpose while children explore or
build bounded parts. The children are real nodes, not a third kind of thing. When the
parts return to the parent, the parent is responsible for whether the assembled whole
still means what it was supposed to mean.

This is a design idea, not a recipe. The important pressure is integration: a
decomposition is not good merely because each part looked locally coherent.

## collisions

Two collisions matter most:

- **Concurrency**: two efforts change the same meaning at once.
- **Orthogonality**: one segment carries concerns that should be separated.

Prefer clearer documents over more mechanism. If two names are surely one concept, merge
them by taking one name out. If the distinction is real or uncertain, surface it.
