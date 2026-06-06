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
not say *why* (that lives in the change that made it), and it does not *prove* itself
(that runs as a check on the code). It is checked against reality and corrected as the
code changes. To start work — operator or machine — you read the intent and the code.

## structure

Every **node** is two trees: the intent, and the code that materializes it. A project is a
node, and the root corpus is a node — the same shape at every scale.

```
documentation/
  organizing-document     # names this node's segments — how its intent is divided
  <intent document>       # one per segment — the current intended state, endorsed at its foot
  machine-statements/     # one per segment — every machine statement, kept out of the orient path
  changes/                # one folder per change in flight
    <NNN-slug>/           # a change in flight
    archive/              # reserved — changes folded in, the history
implementation/           # the code: leaf code, or a child node per nested project
```

There's no universal taxonomy — generalizing one isn't useful, but dividing the intent
into segments is. Each node picks segments that fit its work, and the organizing
document names them. `machine-statements/` mirrors the same segments.

A **change** is a delta to the intent, the steps to materialize it, and its why and
proof. It lives directly in `changes/` while in flight. When it's done, its delta folds into
the intent documents and the change moves to `changes/archive/`. So the intent documents
hold only the current statements, the archive holds why each one is there, and the code
carries the checks that keep them true.

## the intent document

One segment's intended reality, written as plain statements — *every request carries a
verified user*, not "assumes," not "should." A statement is clear by being strong enough
to be wrong, never hedged to be safe. A brittle part described in clear statements beats a
sturdy one described in murky ones — and both have to work.

Behavior and dependency read the same; the prose distinguishes neither. The why and the
proof stay out of the document: the why in the change that made the statement, the proof
as a check on the code. What remains is the statements, each held true by a check that
runs, and re-runs, on the code.

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
Ownership is the right to change, not a license to break: a change that fails the sweep is
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

## the change

A change is a folder. The intent is what the system should be, the code is what it is, and
a change crosses the gap — carrying the edit to the intent and the steps to make it real.

It holds four things:

- **the delta** — the statements the change adds, alters, or removes, by segment. On
  archive these fold into the intent documents.
- **the why and the proof** — why the change was made, and the check behind every statement
  it makes. The why stays here in the archive. The proof becomes a check on the code, bound
  to the statement, that outlives the change and keeps running.
- **the endorsement** — one file, the operator's vouch: of every segment the change touches,
  they take on the whole operator set, having read it and able to reason about it. Like the
  why, it archives with the change; unlike the why, what it leaves behind lives on — on
  archive it stamps the foot of each touched segment with this operator. A segment whose
  change goes unendorsed falls to the machine.
- **the plan and its tasks** — the machine's route from the current code to the delta, in
  small units. The choices it settles on the way are machine statements, filed by segment
  in `machine-statements/`.

A folder, not a file, for two reasons: the plan and tasks need room to grow, and a task may
itself be a change, which a folder can hold and a file cannot.

When the change is done, its delta folds into the intent, every segment it touched now
endorsed by this operator at its foot, and the change moves to `archive/`.

## the loop

Every change goes through five steps.

1. **orient.** Read the intent documents, the changes in flight under `changes/`, and the code's
   conventions. Search the web for what you don't know. Ask the operator what the artifacts
   can't tell you. Don't guess.
2. **frame.** State the change plainly. Write it as a delta to the intent. Break it into
   tasks. The sweep reads the delta against the whole corpus and the changes in flight, and
   flags what it likely clashes with — a parent statement, a sibling, a machine statement
   already filed, a concurrent change still in flight under `changes/` — so a contradiction surfaces before
   the code rests on it.
3. **implement.** Build in small units.
4. **check.** Two kinds, both required:
   - **for the user** — does it behave as the intent says? Prove each statement with a
     check on the code. The checks live with the code and re-run for every statement, not
     only the ones this change touched, so drift — a check that falls without a change
     meaning to break it — surfaces wherever it happens.
   - **for the system** — is it coherent, idiomatic, secure? The **sweep** checks coherence
     with the rest of the intent; idiom and security are judged in the code.
5. **archive.** Fold the delta into the intent documents, stamp each touched segment's foot
   with this operator (or leave it the machine's if the change went unendorsed), and move the
   change to the archive.

A large change breaks into tasks at **frame**, and a task may itself be a change that runs
this same loop. The structure is the same at every level: a change holds tasks, a task can
be a change, and the loop, the folder, and the statements keep their shape all the way
down. We don't require deep nesting yet, but the recursion is by design, and the sweep
reads relations up and down it — a child against its parent — as readily as across a
segment.

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

The workflow turns on the operator. It is **interactive** through orient, frame, and the operator's
**sign-off** — the human gate, which the machine never crosses for itself. Then the session **clears**,
and a fresh, memoryless run re-derives implement, check, and archive from the written frame alone. The
clear is the test: a blank machine that can build the change from its frame proves the frame was
complete — *if it is not written down, it is lost*, made into a gate.

The adapter also makes the intent **intelligible** — explaining a statement in plain language on request,
without altering it. And it carries only what the intent cannot yet reach the machine with on its own:
the order to read the intent first, and the disciplines not yet written as statements. Each such
discipline is a **debt** — folded into the intent by a later change, then dropped from the adapter — so
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
sweep only points. It runs early, at **frame**, over the whole corpus and the changes in
flight, so a clash with a parent, a sibling, a machine statement already filed, or a
concurrent change still in flight shows up before the code is written — and a fresh operator
meets those machine statements there, without carrying them through orient. It runs again
at **check**, on the built change, to confirm the corpus stayed coherent before the delta
archives.

Where two names are surely one concept and merging loses no clarity, merge them — take a
name out, never put a shape in; the merge is itself a change. Where it's unsure, or the
distinction is real (*verified* is not *authenticated*), surface it, don't guess. Merging
only removes, so the sweep can settle it.

The map spans everything written — the intent and `machine-statements/` alike — and
relations are read across all of it. A machine statement can contradict an intent statement
whether or not anything leans on it yet, and the sweep must see it either way. Gathering the
machine statements here, by segment, instead of scattering them through the changes is what
keeps this from costing a scan of history.

So when a statement leans on a concept, three things can happen. It's grounded in the intent
— fine. It's grounded only in `machine-statements/` — the machine statement has become
load-bearing, so copy it up into that segment's intent. It's grounded nowhere — then
something is built on unstated ground, and the fix is to ground it: write the missing
statement, or name the reality it rests on. Absence is never a verdict. We don't assume the
corpus is complete, only that whatever is leaned on is grounded somewhere.

The sweep reaches as far as the changed statement's concepts reach — every statement about
the same ones, whatever words they use, across segments and up and down the tree. Touching
one segment re-checks the others that bear on it, which is how it keeps them in agreement.

## collisions

Two changes touching the same intent document is a smell, with two causes.

- **concurrency** — they're genuinely about the same segment at once. The taxonomy is fine,
  and no one sequences them; the loop's gates do. Orient and the frame sweep both read
  `changes/`, so the later change sees the in-flight delta and builds on it. Archive is the
  commit: the check sweep reads the whole corpus, including any sibling that archived first,
  so a change can't land until it's coherent with what's there. First to archive wins; a tie
  breaks by any fixed rule, since either order leaves the corpus coherent. When one segment
  collides over and over, the changes are really one concern — promote them into a parent
  change and order them as its tasks.
- **orthogonality** — the document sits where two taxonomies cross. Fix the taxonomy, and
  prefer more documents over more mechanism: if the crossing concern has its own coherent
  intent, give it its own intent document for the others to lean on, and the crossing
  dissolves. Reserve tags — a managed axis named in the organizing document — for a genuine
  second partition of everything (say, feature × layer), added the first time a real facet
  forces it, not before.

## nodes

A project under hypercore is not a new kind of thing. It's a **node** — the same two trees,
governed by the same loop — nested inside another. Where a segment isn't materialized by leaf
code, it's materialized by a child node: a node like any other, with its own intent, its own
code, its own changes. Nodes nest to any depth.

The parent segment a child materializes is the child's **contract** — the child's intent must
satisfy it, and that's the whole obligation. A node holds only its own corpus; the contract is
the one thing that crosses between parent and child. So a hundred-project portfolio is a
hundred small corpora, not one sprawling one — only contracts cross.

Two things stop at the boundary on purpose. Endorsement doesn't cross: the operator endorses
the contract in the parent and the child's whole operator set in the child, as two separate
acts, and the floor stands per node — no one is ever forced to endorse everything beneath
them. The checks don't cross either: each node's statements are proven against that node's own
code, while coherence across the boundary — a child's intent against its parent's contract — is
the sweep's, read like any other relation between statements.

This is the recursion the loop already runs, seen from the other side. A task may be a change,
so changes nest in time; nodes nest in space; and the two are one nesting, because a change
always lives in the corpus of the node it changes. A task that reaches into a child *is* a
change in the child. The composition tree and the change tree are one tree.

hypercore ships with the mechanism in place and one home — **work-home**, the home your
projects mount into. It is itself a child node: its own two trees, carrying one real segment
— how a work folder mounts and is governed — and an empty mount point. Each project you mount
becomes a child node of the home in turn — its own distinct git repository, a submodule under
`implementation/work-home/implementation/`, governed within itself, its documentation and code
together. The home holds zero work folders yet; the recursion deepens the moment you mount the
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
- **how a statement is pinned.** A change names the statements it alters or removes by their
  words. How that naming pins one exact statement as it gets reworded over time isn't
  settled yet.
