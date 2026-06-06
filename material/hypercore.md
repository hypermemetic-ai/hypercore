# hypercore

How we ship code — operator and machine together: a lot of it, kept coherent over time.

Writing code is no longer the bottleneck. A machine writes as much as you want. The
hard part is keeping it coherent as it grows. Many hands change the codebase, and most
are machines that begin each session with no memory of the last. People forget too, and
move on. So assume no one remembers anything. If it isn't written down, it's lost.

Three properties are non-negotiable:

- **scrutable** — you can read it and understand it.
- **sound** — nothing is built on unproven ground.
- **fast** — small steps, no wasted motion.

When they pull against each other, say so out loud instead of quietly trading one away.
One tension is already settled: in the intent, clarity comes before proof.

What we write down is the **intent** — the model of what each part of the system is meant
to be, set down as plain statements: how it behaves, what it depends on. The intent does
not say *why* (that lives in the work that made it), and it does not *prove* itself (that
runs as a check on the code). It is checked against reality and corrected as the code
changes. To start work — operator or machine — you read the intent and the code.

## collaboration

Collaboration is the working relation by which operator and machine keep the work
scrutable, sound, and fast across memoryless sessions. It is a first-class methodology
concern, separate from the loop mechanics that enforce it.

The relation is complementarity, not maximal automation. The operator sets purpose,
constraints, acceptance, and open direction. The machine searches, synthesizes, drafts,
executes, checks, and settles only what the intent and operator leave open.

Common ground stays written: goal, current state, assumptions, uncertainty, decisions,
authority, proof state, and handoff state are recorded where the next operator or machine
can recover them. The machine makes its capabilities, limits, uncertainty, evidence, and
failure modes visible enough for the operator to judge when to rely on it, challenge it,
redirect it, or stop it.

Operator agency is preserved without wasting motion. Before sign-off, the machine asks
before settling open direction or choices the artifacts cannot ground. After sign-off, it
proceeds without interruption when the signed frame, intent, and checks give it enough
written ground. If written ground is insufficient, the machine records the blocker and
decision surface and stops rather than fabricating content.

Feedback is material. Operator corrections, machine-discovered facts, failed checks, and
sweep flags become intent, proof, machine statements, or debt rather than remaining
transient chat. Handoff is a written state, not memory.

## structure

Every **node** is two trees: the intent, and the code that materializes it. A project is a
node, and the root corpus is a node — the same shape at every scale.

```
intent/
  organizing-document     # names this node's segments — how its intent is divided
  <intent document>       # one per segment — the current intended state, endorsed at its foot
  machine-statements/     # one per segment — every machine statement, kept out of the orient path
  history/                # readable history of adopted, shelved, and legacy work records
material/                 # leaf code, or child nodes housed by this node
  <NNN-slug>/             # a node-local work node in flight
    intent/
    material/
```

There's no universal taxonomy — generalizing one isn't useful, but dividing the intent
into segments is. Each node picks segments that fit its work, and the organizing
document names them. `machine-statements/` mirrors the same segments.

A **work node** is an ordinary child node housed in its parent's material. While active it
is bounded by the parent intent whose reach includes it, and it may propose amendments to
the parent without making those amendments parent truth. Adoption folds accepted statements
and material into the parent; shelving records the work without adopting its proposals; a
durable work node may stay active indefinitely.

Old five-file change folders are readable history of the retired abstraction. New work does
not depend on `intent/changes/`, and a work node's purpose, rationale, proof state, route,
endorsement, and adoption claims are recoverable from that work node's own intent or
material, not from universal required filenames. An unmounted child remains absent rather
than being filled with placeholder content.

## the intent document

One segment's intended reality, written as plain statements — *every request carries a
verified user*, not "assumes," not "should." A statement is clear by being strong enough
to be wrong, never hedged to be safe. A brittle part described in clear statements beats a
sturdy one described in murky ones — and both have to work.

Behavior and dependency read the same; the prose distinguishes neither. The why and the
proof stay out of the document: the why in the work that made the statement, the proof as a
check on the code. What remains is the statements, each held true by a check that runs, and
re-runs, on the code.

One name, one concept.

## statements

Every statement has an **owner**: the operator, or the machine.

**Ownership is who may change it.** An operator statement is the operator's: it holds
until they change it. The operator's intent is usually open — it allows many systems — and
the machine settles what's left open. Each thing the machine settles is a machine
statement, which the machine may change on its own. A freedom is not declared, it's taken:
the operator leaves a choice unmade, the machine settles it, and the machine statement is
the record. The unsaid is open, not an oversight.

Operator and machine each may change what they own, and both are bound by coherence.
Ownership is the right to change, not a license to break: work that fails the sweep is
turned away whoever makes it.

**Endorsement is per segment.** One operator stands behind the segment's whole operator
set — every operator statement in it, not only the ones they last touched. To change a
segment is to take the set on: you endorse it because you have read it and can reason about
it as a whole. The endorsement is a single line at the foot of the document. The machine's
statements sit apart, under `## machine`, and carry no endorsement — unendorsed is the
machine's, the machine never endorses, and a segment no operator will stand behind falls to
it. The machine is the floor.

There is no partial endorsement and no handover step: you own the set or you don't. If a
segment's set is too large to take on, shrink it — split the segment into smaller ones, or
let the machine take over the statements you won't stand behind, dropping them below the
line. Either way, what's left in the operator set is wholly yours.

A machine statement is filed in `machine-statements/` — one document per segment, like the
intent but out of the orient path, holding every machine statement made. When something
comes to lean on one, the sweep copies it up into that segment's `## machine`, where the
operator meets it. The original stays, so `machine-statements/` always holds them all.

Ownership and truth are separate backings. The endorsement says who stands behind the set;
a check says each statement holds. They're independent — a segment can lose its operator
and keep every check it had, falling to the machine with its proofs still standing.

A segment reads as its operator statements, then the machine's, then the endorsement:

```
# web
the system has a frontend.
the frontend shows the signed-in user their own activity.
the frontend never renders another user's data.

## machine
the frontend is a react spa.

---
endorsed by alice
```

Alice stands behind the three operator statements as a set. The react-spa line is the
machine's — a choice it settled, below the line, under no one's endorsement.

The loop means to admit only statements that fit. Each has an owner — the segment's
endorsement covers the operator set, and the machine owns the rest. Each is falsifiable,
and carries a check that holds it true. A statement that is neither ownable nor checkable is
one the loop turns away.

## the work node

Active work is a child node with the same internal shape as any node: `intent/`,
`material/`, and whatever segments its organizing document names. It is not a second
recursive abstraction; childness is bounded freedom. Parent intent statements define their
own reach — node-local, a named child, all direct children, descendants, or a named class of
child — and a child is bound by the parent statements whose reach includes it.

A work node can carry proposed parent statements, proof state, route, endorsement,
adoption claims, and material changes, but those are recoverable from the work node's own
intent or material rather than from required change-specific filenames. A work node may be
temporary, durable, adopted, shelved, abandoned, or indefinitely active.

The loop names work by an addressed node and one node-local work name. With no node named,
the root node is assumed. A child node is addressed explicitly, then the same `NNN-slug`
work name is resolved under that node's `material/` tree. Root-directed work lives directly
under root `material/` as a sibling to `work-home`, not under `work-home`.

Adoption folds accepted child statements and material into the parent and records the
adopted work node as history. Shelving records the work node as history without making its
proposed amendments parent truth. Until adoption accepts an amendment, the parent intent
remains current.

## the loop

Every work node goes through the loop's gates when it needs adoption or shelving. Orient
and frame are the design phase: operator and machine choose direction there, before
sign-off closes the frame. When the route is still open — especially multi-task or
multi-phase work — the machine states the problem, constraints, and decision surface before
settling the route. If operator direction is missing, the frame records the open decision
and waits rather than prescribing the sequence. After sign-off, implementation autonomy
begins: phase two builds from the signed frame and stops only when the frame is incomplete,
a check fails, or the sweep flags incoherence.

1. **orient.** Read the intent documents, the work in flight across the node tree, and the
   code's conventions. Search the web for what you don't know. Ask the operator what the
   artifacts can't tell you. Don't guess. Name the addressed node, the node-local work
   name, the target segments, the work in flight, and any open direction that needs operator
   input before the frame settles a route.
2. **frame.** State the work plainly. Write enough of the work node's intent and material
   to make the proposed work scrutable. Before prescribing an open multi-task or
   multi-phase route, state the problem, constraints, and decision surface; when operator
   direction is missing, record the open decision and wait rather than filling the gap. The
   sweep reads the child work node against the parent intent, proposed parent amendments,
   sibling work, machine statements, and current nodes whose concepts it touches, and flags
   what it likely clashes with before the code rests on it.
3. **implement.** Build in small units from the signed frame.
4. **check.** Two kinds, both required:
   - **for the user** — does it behave as the intent says? Prove each statement with a
     check on the code. The checks live with the code and re-run for every statement, not
     only the ones this work touched, so drift — a check that falls without work
     meaning to break it — surfaces wherever it happens.
   - **for the system** — is it coherent, idiomatic, secure? The **sweep** checks coherence
     with the rest of the intent; idiom and security are judged in the code.
5. **archive.** Adopt or shelve the work. Adoption folds accepted statements and material
   into the parent intent and material, stamps each touched segment's foot with this
   operator (or leaves it the machine's if the work went unendorsed), and records the work
   node as history. Shelving records the work node as history without changing parent
   truth.

Large work breaks into related work at **frame**, and related work is an ordinary work node
in the node it alters. A coordinating work node may name related work in its plan and proof;
before it adopts or shelves, related unfinished work is either resolved in its own node or
carried as explicit debt. The sweep reads a child node against the parent statements whose
reach includes it, and reads related deltas together wherever their nodes are.

## the adapter

A machine harness begins each session with no memory of the last. Nothing reaches it but what it
loads — so something has to carry it, before it has read a word of the intent, the instruction to read
the intent and run the loop, and the discipline that holds it there once read. That something is the
**adapter**: the artifact the harness loads at the start of work. Its one job is a **promise** —
agreement between the harness and the methodology, that the machine acts in accordance with the intent
and the loop. Absent the adapter, agreement is left to chance.

The adapter both **routes and drives**. It points the machine at the intent and the loop — the single
source of truth — and states no rule of its own; where the adapter and the intent disagree, the intent
wins. But pointing alone is only a request. So the adapter's specifics are a **rigid workflow** over the
loop's gates: each gate's preconditions must hold before the next is allowed, and a gate whose
preconditions fail *blocks rather than warns*. The workflow restates no rule — the gates and their order
are the loop, already intent — it only operationalizes them, so the adapter stays pure routing plus
enforcement, not new ground.

The workflow turns on the operator. It is **interactive** through orient and frame as the
design phase, and through the operator's **sign-off** as the human gate, which the machine
never crosses for itself. Before the machine settles open direction, it surfaces the
problem, constraints, and decision surface for operator direction. Then the session
**clears**, and a fresh, memoryless run re-derives implement, check, and archive from the
written frame alone. The clear is the test: a blank machine that can build the work from
its frame proves the frame was complete — *if it is not written down, it is lost*, made
into a gate.

The adapter also makes the intent **intelligible** — explaining a statement in plain language on request,
without altering it. And it carries only what the intent cannot yet reach the machine with on its own:
the order to read the intent first, and the disciplines not yet written as statements. Each such
discipline is a **debt** — folded into the intent by later work, then dropped from the adapter — so
the adapter trends toward pure routing as the intent catches up.

An adapter is per harness; one node may be bound by more than one, each loaded by its own harness. It is
materialized once, with the methodology prose it routes to, at the methodology root — not in every node;
a machine working in a nested node is bound by the harness loading that root adapter, the same way one
materialization of `check.sh` checks every node. The adapter is not in the orient path — loading it is
how orient begins, not part of the intent it routes to — and the sweep reads it against the intent, so a
rule it drifts into restating, or a debt the intent has since absorbed, surfaces as drift like any other.

## the sweep

The sweep runs in two passes, and only the first is cheap. **The map:** because the
documents name one thing one way, following a concept — not the word — to everywhere it
appears is fast, and it narrows the field to the statements that bear on each other. **The
read:** among those, the sweep judges the relation. The judgment is semantic, so it is
graded, not certain — one concept under two names, one name over two concepts, a statement
leaning on a concept nothing grounds, statements that should be read together, a statement
that *likely contradicts* another. The map is built to make the read cheap, then thrown
away.

The read is graded on purpose. We don't make every statement formal — that would be absurd
— so the sweep doesn't prove a clash, it rates one. *This likely contradicts a parent* is a
datapoint, surfaced before the decision that would build on it. The proof settles; the
sweep only points. It runs early, at **frame**, over the whole corpus and the work in
flight across the node tree, including related work named by a coordinating frame,
so a clash with a parent contract, a sibling, a machine statement already filed, or a
concurrent work node still in flight shows up before the code is written — and a fresh
operator meets those machine statements there, without carrying them through orient. When a
work node names related work, the sweep reads those deltas together wherever their
nodes are so a task cannot silently contradict the coordinating scope or a child node's
parent contract. It runs again at **check**, on the built work, to confirm the corpus
stayed coherent before adoption or shelving.

Where two names are surely one concept and merging loses no clarity, merge them — take a
name out, never put a shape in; the merge is itself work. Where it's unsure, or the
distinction is real (*verified* is not *authenticated*), surface it, don't guess. Merging
only removes, so the sweep can settle it.

The map spans everything written — the intent and `machine-statements/` alike — and
relations are read across all of it. A machine statement can contradict an intent statement
whether or not anything leans on it yet, and the sweep must see it either way. Gathering the
machine statements here, by segment, instead of scattering them through work history is what
keeps this from costing a scan of history.

So when a statement leans on a concept, three things can happen. It's grounded in the intent
— fine. It's grounded only in `machine-statements/` — the machine statement has become
load-bearing, so copy it up into that segment's intent. It's grounded nowhere — then
something is built on unstated ground, and the fix is to ground it: write the missing
statement, or name the reality it rests on. Absence is never a verdict. We don't assume the
corpus is complete, only that whatever is leaned on is grounded somewhere.

The sweep reaches as far as the touched statement's concepts reach — every statement about
the same ones, whatever words they use, across segments and up and down the tree. Touching
one segment re-checks the others that bear on it, which is how it keeps them in agreement.

## hardening

Hardening is the loop applied to real-world failure modes across hypercore's segments, node
boundaries, adapters, and materializations before calling any of them hardened. Real-world
use includes interrupted sessions, memoryless machines, dirty worktrees, missing or failing
tools, concurrent work, operator handoff, nested nodes, external harness behavior, and
absent mounted work folders.

A hardening pass starts from the current intent and materialization. It never invents
child-node content, and it never assumes an unmounted work folder exists. Each phase is
bounded work that names the segment, node boundary, adapter, or materialization under
review; the failure modes it examines; the statements it strengthens; the proof it adds or
preserves; and any debt it leaves.

A phase changes the taxonomy only when the existing segments hide a real concern; otherwise
it changes the segment that owns the concern. A hardening effort is multi-phase when its
scope spans more than one bounded phase: coordinating work states the scope and sequence,
and related phase work runs the loop in the node it alters. Hypercore does not
call a segment, node boundary, adapter, or materialization hardened while a named failure
mode lacks proof; unproven failure modes are carried as explicit debt instead.

## collisions

Two work nodes touching the same intent document is a smell, with two causes.

- **concurrency** — they're genuinely about the same segment at once. The taxonomy is fine,
  and no one sequences them; the loop's gates do. Orient and the frame sweep both read work
  in flight across the node tree, so later work sees the in-flight delta and builds on it.
  Adoption is the commit: the check sweep reads the whole corpus, including any sibling
  that adopted first, so work can't land until it's coherent with what's there. First to
  adopt wins; a tie breaks by any fixed rule, since either order leaves the corpus
  coherent. When one segment collides over and over, the work nodes are really one concern
  — promote them into coordinating work and name the related work in its plan.
- **orthogonality** — the document sits where two taxonomies cross. Fix the taxonomy, and
  prefer more documents over more mechanism: if the crossing concern has its own coherent
  intent, give it its own intent document for the others to lean on, and the crossing
  dissolves. Reserve tags — a managed axis named in the organizing document — for a genuine
  second partition of everything (say, feature × layer), added the first time a real facet
  forces it, not before.

## nodes

A project under hypercore is not a new kind of thing. It's a **node** — the same two trees,
governed by the same loop — nested inside another. Where a segment isn't materialized by leaf
code, it's materialized by a child node: a node like any other, with its own intent and its
own material. Nodes nest to any depth.

Childness is bounded freedom. A parent intent statement defines its own reach: node-local,
a named child, all direct children, descendants, or a named class of child. A child is
bound by the parent statements whose reach includes it, and any parent segment that houses
the child states the contract the child must satisfy. A node holds only its own corpus; only
the statements whose reach includes the child cross the boundary.

Two things stop at the boundary on purpose. Endorsement doesn't cross: the operator endorses
the contract in the parent and the child's whole operator set in the child, as two separate
acts, and the floor stands per node — no one is ever forced to endorse everything beneath
them. The checks don't cross either: each node's statements are proven against that node's own
code, while coherence across the boundary — a child's intent against its parent's contract — is
the sweep's, read like any other relation between statements.

This is the recursion the loop already runs, seen from the other side. Nodes recurse; work
is a node rather than a separate recursive shape. A task may be large enough to run the
loop, but it lives as work in the node it alters. A task that reaches into a child is work
in the child node, addressed there like any other node-local work.

hypercore ships with the mechanism in place and one home — **work-home**, the home your
projects mount into. It is itself a child node: its own two trees, carrying one real segment
— how a work folder mounts and is governed — and an empty mount point. Each project you mount
becomes a child node of the home in turn — its own distinct git repository, a submodule under
`material/work-home/material/`, governed within itself, its intent and material together.
The home holds zero work folders yet; the recursion deepens the moment you mount the
first, with your work, not a placeholder.

## not yet decided

- **grade.** Statements once carried a second reading — a *grade* that said how each was
  backed, and sorted them by how much doubt they drew. It's set aside for now. The
  check-on-code layer keeps every statement honest without it; if a real need for grading
  returns, it comes back then.
- **per-statement endorsement.** Endorsement is per segment: touch it, own the whole
  operator set. A finer grain — one endorsement per statement — makes sense, but it's set
  aside until per-segment proves too coarse. The relief for an over-large set is a smaller
  segment, not a finer endorsement.
- **how a statement is pinned.** Work names the statements it alters or removes by their
  words. How that naming pins one exact statement as it gets reworded over time isn't
  settled yet.
