# intent

new-hypercore — the rebuild. Drafted from the mature intent of the system
it will supplant, every statement machine-owned and awaiting the operator's
ratification statement by statement. Until each marker drops, none of this
is endorsed.

## foundations

Operator legibility is king. When any other concern competes with it, legibility wins.

hypercore is a small system for a human and an agent to work together.

The tree is the model: nodes, the relations between them, and the material attached to them. Everything the operator sees is a view of that one tree.

The machine carries no memory between episodes in its running context. An arc of work's durable memory is the tree and the version-controlled state that holds it; an episode's conversation is disposable and clears without loss, because the next episode reads what it needs from the tree.

Inherited debt is not carried. When the system stops passing the operator's acceptance with no lingering doubts, it is torn down and rebuilt, not patched.

The operator's attention is the scarcest resource in the system. The operator never performs tree maintenance: the machine files, links, and renders; the operator ratifies, vetoes, and redirects. An operator hand-tending the bookkeeping is the first sign that ceremony has won.

The operator reads the system's state at a glance, without asking the machine. What they can read is the source of truth.

The queue is the operator's decision surface. A decision arrives there with the context to decide it, the options on the table, and what each option entails: what it unblocks, what it breaks, what keeps running unbacked, and what reversing it later would cost.

A decision is a real judgment call, and its card carries the story. What reaches the queue as a decision is a genuine fork — a choice that turns on reasoning the operator has not yet done — and it arrives carrying that reasoning: what the choice changes about their days, a worked example, where the machine leans, and the one thing that would flip it. What is not a real judgment call is not dressed as one: a step that needs only the operator's go is a request for approval, lighter and named as such — a different kind of card, not a decision. The card's kind matches the kind of the call.

The interface is the only place the operator operates, the only way they catch problems with the system, and the only thing that crosses the operator–machine boundary. Every move the system asks of the operator can be made there; a problem the interface cannot surface is one the operator will never see; blinding the operator in any meaningful way kills the program.

The interface surfaces the evidence; the operator never leaves to gather it. When judging a slice or a decision means seeing what a script produces, what a report says, or what a page shows, the machine runs it and brings the result in — the output rendered on the card, the page or app pulled up, the view opened. Asking the operator to go run something themselves is the interface failing to surface, not a task for them; a verification step the operator will not perform verifies nothing.

The interface shows everything the operator wants to know and nothing they don't. Every element on screen earns its place.

The interface is keyboard-only, high-contrast, and set in deliberate type, with color spent only where it earns its place. It opens fullscreen at login: the day starts where the decisions are.

The main screen is the face of the system and wears its best design — immaculate, tasteful. The queue of decisions and the standing work are its two principal elements, each its own place; reference detail lives in the views built for reading it.

The operator can speak from anywhere in the interface: their words land on disk verbatim, the place they spoke from travels with them, and nothing more is asked of them.

The operator's actions never make them wait. An act lands the instant the operator makes it and the interface frees at once; the durable write follows behind the screen, guaranteed to land or the operator told that it did not.

The conversation is live: words spoken in the interface summon the machine on the spot, and the answer lands while the operator watches.

A key, pressed on any visible element tied to a model's working, spawns a live visual of that model's reasoning — its shape, seen from several angles, in real time — so the operator can tune in to what a model is thinking and steer alongside it. This is a pull the operator makes on purpose, not a push the system sends; symbiosis wants the channel direct. [machine]

Reading the operator's words is machine work. Whether a word is new intent, a new ask, an answer, or a redirect is the machine's call to make and answer for, and what it made of the word returns through the queue. Every operator word lands a concrete, findable consequence — a change, a decision returned to them, or a written reason nothing moved — and the record leads from the word to what was done about it.

The queue is a view, not a place. Each decision lives where it arose — on a statement, on a node, on a piece of evidence — and showing the queue means reading all of those places fresh, every time. There is no list of its own to add to, remove from, or keep in sync, so nothing can be lost in motion and nothing can go stale.

The tree is the interface's one work surface; a thread is the throwaway conversation opened on it. Every operator word and every unit of work lives on the tree, traced to the operator action that began it; a queue card is a view onto its node; a run shows as the live work on the node that spawned it; settling the card folds it into that node, where its decision and grounds are kept. The thread itself keeps none of this — it opens when the operator speaks, lands one consequence on the tree, and closes. A fully-handled system shows an empty surface — the system at rest, not a fault.

The open work is the operator's working channel; the queue is for decisions. A thread is scoped to one node — speaking on a node opens a thread there — so a conversation stays scoped to one part of the arc and never spans the whole. The thread is throwaway and holds no durable state; the node it spoke on keeps what was decided, and a live indicator shows when a run is on it. Standing work is readable from the interface, and setting priorities takes nothing the interface does not show.

The order of the queue is the machine's claim about what the operator's attention is worth next, and it answers for that claim: every decision wears the cost of its own delay — what it blocks, what compounds while it waits. The operator's word overrides the order instantly and unconditionally — the word is the reorder, not a request for one.

The machine never silently commits the operator's resources. Scope calls that change what the operator must later judge, build machinery, or decline their intent are theirs to make; within endorsed intent the machine scopes freely and visibly, and records its grounds at the moment each decision is made.

Decisions surface while the work is underway: a call that commits the operator's resources or changes what they must later judge is settled before the material exists. The bar has a written floor, checked at one named moment before the first write or command that creates the material — five yes/no tests, and any yes surfaces the act as a decision. It leaves the project folder (sends, publishes, installs, spends); it touches what the operator owns or uses; it binds future runs; it takes more than one git command or one redo to take back; or the machine catches itself arguing that none of these apply. Judgment may surface more, never less, and every commit can be held against the floor after the fact.

Work runs continuously; the only thing that stops it is a decision the operator must make. While any unblocked unit of work remains, a run is on it: the scheduler cuts the next seam and keeps building, and never idles waiting to be re-prompted. The system goes quiet only when all that is left is a decision the operator owns, and that decision is then on the queue with the reason the work paused. An idle system with unblocked work left is a defect, not rest.

Work runs concurrently as well as continuously: more than one run advances the one tree at once. Each worker is isolated — it runs in its own git worktree, fenced by the operating system from its siblings and from the main line, so it can neither corrupt another worker's tree nor reach the shared line until its result is integrated. The fence is the system's, not a convention a worker could break by accident: the worker's own worktree is writable, the rest of the host read-only, and the shared git history writable so the worker's own commits reach the one record. The fence guards parallel work, not the network: a worker is an agent that thinks over the net, so the net stays open; the one thing an open net could do that the operator should weigh — spend, publish, or pull in outside state — is caught at the decisions floor, not walled off here. Isolation is the concurrency model the whole system rides.

## structure

Intent starts work; material is what the work makes. Intent constrains the problem space, decisions along the way narrow it further, and finished material is validated against both. The point is operator knowledge: their model of the system matches what gets built and what reaches the real world.

Intent-setting is extraction, not transcription. While a project's intent is forming, the machine works the gap between what the operator wants and what it knows — requirements drawn out of the operator, facts fetched from the world — and that work is visible as open asks on the queue. A quiet queue during intent-setting signals stalled extraction, not finished work.

Intent lives relative to an execution tree, folded or unfolded: the tree's folder contains its intent, and a tree's intent document is its current intended reality. hypercore is itself a folded execution tree, this repository is its folder, and everything in it that is not intent is material.

Work that is not about hypercore lives with its project: the project's folder carries its own intent and trees, versioned in its own repository, and hypercore keeps a registry of the linked folders the interface reads. A linked project's intent ratifies from the interface, and every ratifying commit lands in the project's own repository — hypercore holds the link, never the words.

Brownfielding a project is distillation, then ratification: the folder enters the registry, the machine drafts its intent (machine-owned to the last word) from the project's own record, and the operator's picks decide what survives. The project keeps running on its old record until intent supplants it, and what the cuts leave unbacked becomes the project's first absorption work.

The durable state lives in version-controlled files. Everything that crosses the operator–machine boundary lands on disk and is committed, so the operator reads the state directly and any episode can be recovered from the record. A storage backend is adopted only if it keeps this direct legibility and recoverability.

## statements

A statement is plain, declarative, and strong enough to be wrong — against material, evidence, or later judgment. It reads as if written from scratch, with no trace of the conversation that produced it.

Every statement is ownable: one party can put their name on it and answer for changing it. If it doesn't matter enough for the operator to hear about it, it isn't a statement.

The operator and the machine are both bound by coherence. When the operator's decisions stop making sense together, the machine calls it out rather than silently applying the newest word.

A revision lands as one edit and one commit, and nothing we build may grow that path. What a revision breaks becomes work, after it lands.

## endorsement

The machine never endorses for the operator. Every statement is endorsed or unendorsed: endorsed is the operator's responsibility, unendorsed is the machine's, and material answers to whoever is responsible for the statement behind it.

Ownership is visible in the file itself: a machine-owned statement ends with the marker [machine]. The operator has three commands — approve drops the marker, cut removes the words, and explain has the machine help them toward a decision and returns the statement.

The default motion is ratification: the machine drafts concrete statements and the operator decides; the operator is rarely asked to author from nothing. When the operator leaves a meaningful choice open and the machine settles it, that settlement is visible as machine-owned intent until the operator endorses it.

Ownership does not make a statement true. When evidence turns against a statement — whoever owns it — the operator hears about it. A change to the words is the owner's to authorize: the machine drafts and makes it on the owner's word, and an operator-owned statement is never changed without that word.

A cut is informed disagreement or a refusal to incorporate what is not understood; either way the words leave intent. What a cut breaks — references left dangling, machinery left running with no statement behind it — is put before the operator as part of the decision, not discovered after it.

Unendorsed statements are debt. Leaving one unprocessed doesn't stop the machine from asking again, and as unendorsed statements come to depend on each other, the operator's model of the system drifts from reality.

## work

Work happens as a tree. A node expresses an ask, and carrying it out grows a tree of further nodes — the steps, the candidates, the checks, the result. That growing tree is an execution tree: a dynamically composed workflow, not a fixed template.

Decomposition is as-needed. An ask splits only when it outruns what one episode can do or one check can vouch for; a seam is cut when the work reaches it, never drawn ahead in full; and what can be done and checked whole stays whole.

Cuts fall where checks can stand: open siblings meet only through folding conditions, and two trees that must trade internals to proceed are one tree cut wrong. A child tree is born with its ask and its folding condition together; an ask whose check cannot be named is not ready to spawn.

The work schedule is a view, not a stored list. The ready work — the nodes a run can take now: open, their folding condition named, and nothing open beneath them — is read live off the one tree each time it is asked for, never a work-queue kept in sync. The same readiness that gates spawning gates scheduling, read structurally as the predicate, so the tree hands out its own work and nothing in the schedule can go stale. When a tree holds no ready leaf, its open root is the ready work — the place the next seam is cut — which is how work keeps moving without waiting to be re-prompted.

A folder holds one execution tree; the unit on disk is the tree, not the single node. Within an execution tree, one name means one concept.

Work is made of operations, each one move on the problem state, of four kinds — ask, check, decide, and do, one word for each thing a statement must find and do for everything else. A new kind of operation enters only in the same edit as the statement that needs it, and stays only while a statement reads it. An operation earns a node on two grounds only: it crossed the operator–machine boundary, or the fold's trust rests on it; everything else is do, absorbed into the operation it served. The tree is a ledger of commitments, not a trace of thought.

When the work is done, the execution tree folds into the node whose ask spawned it: the result becomes that node's material and the steps become its history. Folding preserves relations, so the history reads as the tree it was, not a flat log; the folded tree's folder holds that history whole, and everything else the work made lands in the parent as if made there directly. An open tree sits in its parent's work/; the act that folds it moves it into that work/'s own archive/, tucked one level below the live work so the front of the tree stays legible; neither work/ nor its archive/ exists empty.

A folding condition is what makes a tree ready to fold: its ask is met, or it is abandoned. A tree that cannot meet its condition does not fold dirty — it returns as a decision to abandon, re-cut, or change the ask, and a changed ask that touches endorsed intent is the operator's.

A check names an observation about the work, not an act of trust in it. The episode that does the work is disposable; the checks at the fold's boundary are what survive it. A fold can be trusted only as far as its checks reach, and error compounds up the stack: the weaker a tree's checks, the shallower it must stay before folding, and the less may be built on top of it.

However deep the tree grows, the operator's queue grows only with decisions that narrow intent. The day operator load tracks work volume, decomposition has failed.

A view of a tree never lags it: every view is read live from the tree, or updated in the same act that folds it.

