# intent

## foundations

Operator legibility is king. When any other concern competes with it, legibility wins.

Work on the system, above all other work, is transparent.

Inherited debt burns on a recurring basis: the system is torn down and rebuilt until it passes the operator's acceptance with no lingering doubts.

hypercore is a small system for a human and an agent to think with together.

The graph is the model: nodes, relations between them, and material attached to nodes.

The machine carries no memory between episodes of work. hypercore holds that memory outside the machine: the graph, not the running conversation, is the durable shared state.

The operator's attention is the scarcest resource in the system: the operator never performs graph maintenance. The machine files, links, and renders; the operator ratifies, vetoes, and redirects. An operator hand-tending the graph's bookkeeping is the earliest signal that ceremony has won.

The operator can read the system's state at a glance, without asking the machine; what they can read is the source of truth.

The operator's interface is a queue of decisions. A decision arrives with the context to decide it, the options on the table, and what each option entails: what it unblocks, what it breaks, what keeps running unbacked, and what reversing it later would cost.

The interface is the only place the operator is expected to operate: every move the system asks of them can be made there.

The interface is the only way the operator catches issues with the system: a problem it cannot surface is a problem the operator will never see. Blinding the operator in any meaningful way kills the program.

The interface shows everything the operator wants to know and nothing they don't. Every element on screen earns its place.

The interface is keyboard-only.

The interface opens fullscreen at login: the day starts where the decisions are.

The interface is high contrast and set in deliberate type, with color spent only where it earns its place.

Everything that crosses the operator–machine boundary crosses through the interface and lands on disk; a crossing that left no record did not happen.

The operator can speak from anywhere in the interface: their words land on disk verbatim, the place they spoke from travels with them, and nothing more is asked of them.

Reading the operator's words is machine work. Whether they are new intent, a new ask, an answer, or a redirect is the machine's call to make and answer for; what it made of them returns through the queue.

The conversation is live: words spoken in the interface summon the machine on the spot, and the answer lands while the operator watches. An answer that waits for a restart is a defect.

Until sent, words bind nothing: the operator sees everything they have typed and can change any of it before it crosses.

The queue is a view, not a place: each decision lives where it arose — on a statement, on a node, on evidence — and showing the queue means reading all of those places fresh, every time. There is no list of its own to add to, remove from, or keep in sync, so nothing can be lost in motion and nothing can go stale.

The order of the queue is the machine's claim about what the operator's attention is worth next, and it answers for that claim: every decision wears the cost of its own delay — what it blocks, what compounds while it waits. The operator's word overrides the order instantly and unconditionally — the word is the reorder, not a request for one — and whatever the machine learns from being overridden, it raises later, never in the moment.

Standing work is readable from the interface: what exists, what state each piece is in, and what it waits on. Setting priorities takes nothing the interface does not show.

The machine never silently commits the operator's resources: scope calls that change what the operator must later judge, build machinery, or decline their intent are theirs to make; within endorsed intent the machine scopes freely and visibly. Every decision records its grounds at the moment it is made.

Decisions surface while the work is underway: a call that commits the operator's resources or changes what they must later judge is settled in the queue before the material exists. Below that bar the machine scopes freely, visibly, and answers for the calls it kept.

The surfacing bar has a written floor no model may miss: at one named moment — before the first write or command that creates the material — five yes/no tests are put to the act, and any yes surfaces it as a decision. The tests: it leaves the project folder (sends, publishes, installs, spends); it touches what the operator owns or uses (their words, their files, their environment); it binds future sessions (a default, a policy, a recurring job, a dependency); it takes more than one git command or one redo to take back; or the machine catches itself arguing that none of these apply — doubt surfaces. Judgment may surface more, never less, and every commit can be held against the floor after the fact.

## structure

Intent starts work; material is what the work makes. Intent comes whole from the operator — rarely — or out of back-and-forth with the machine. It constrains the problem space; decisions along the way narrow it further. Finished material is validated against both. The point is operator knowledge: their model of the system matches what gets built and what reaches the real world.

Intent lives relative to an execution graph, folded or unfolded: the graph's folder contains its intent. hypercore is itself a folded execution graph; this repository is its folder. Everything in it that is not intent is material.

An execution graph's intent document is that graph's current intended reality.

Work that is not about hypercore lives with its project: the project's folder carries its own intent and graphs, versioned in its own repository, and hypercore keeps a registry of linked folders the interface reads.

Brownfielding an external project is distillation, then ratification: the folder enters the registry, the machine drafts intent.md from the project's own documents — machine-owned to the last word — and the operator's picks decide what survives; the project keeps running on its old documents until intent supplants them. [machine]

A linked project's intent ratifies from hyper, and every ratifying commit lands in the project's own repository — hypercore holds the link, never the words.

What a brownfield's cuts leave unbacked — documents, gates, machinery with no statement behind them — becomes the project's first absorption work, opened as a graph in its own folder.

## statements

A statement is plain, declarative, and strong enough to be wrong — wrong against material, evidence, or later judgment.

A statement reads as if written from scratch: no trace of the conversation that produced it survives in the words.

Every statement should be ownable: one party can put their name on it and answer for changing it.

If it doesn't matter enough for the operator to hear about it, it isn't a statement.

The operator and the machine are both bound by coherence. When the operator's decisions stop making sense together, the machine calls it out rather than silently applying the newest word.

A revision lands as one edit and one commit; nothing we build may grow that path. What it breaks becomes work, after it lands.

## endorsement

The machine never endorses for the operator.

Every statement is endorsed or unendorsed: endorsed is the operator's responsibility, unendorsed is the machine's. Material answers to whoever is responsible for the statement behind it.

Ownership does not make a statement true. When evidence turns against a statement — whoever owns it — the operator hears about it; only the owner changes the words.

Ownership is visible in the file itself: a machine-owned statement ends with the marker [machine]. The operator has three commands: approve — the marker drops; cut — the words leave; explain — with or without the operator's words, the machine helps them reach a decision, and the statement returns.

The default motion is ratification: the machine drafts concrete statements and the operator decides. The operator is rarely asked to author from nothing.

A cut can be informed disagreement or a refusal to incorporate what is not understood; either way the words leave intent. What a cut breaks — references left dangling, machinery left running with no statement behind it — is put before the operator as part of the decision, not discovered after it.

When the operator leaves a meaningful choice open and the machine settles it, that settlement is visible as machine-owned intent until the operator endorses it.

Unendorsed statements are debt. Leaving one unprocessed doesn't stop the machine from asking again; and as unendorsed statements come to depend on each other, the operator's model of the system drifts from reality.

## work

Work happens as a graph. A node expresses an ask, and carrying it out grows a graph of further nodes: the steps, the candidates, the checks, the result.

That growing graph is an execution graph. It is a dynamically composed workflow, not a fixed template.

An ask splits only when it outruns what one episode can do or one check can vouch for; what can be done and checked whole stays whole.

Decomposition is as-needed: a seam is cut when the work reaches it, never drawn ahead as a tree.

Cuts fall where checks can stand: open siblings meet only through folding conditions, and two graphs that must trade internals to proceed are one graph cut wrong.

A child graph is born with its ask and its folding condition together; an ask whose check cannot be named is not ready to spawn.

Within an execution graph, one name means one concept.

A folder holds one execution graph. The unit on disk is the execution graph, not the single node.

Work is made of operations. An operation is one move on the problem state, of four kinds: ask, check, decide, do — one word for each thing a statement must find, and do for everything else.

A new kind enters in the same edit as the statement that must find it, and stays only while a statement reads it; other new words are names for clusters.

An operation earns a node on two grounds only: it crossed the operator–machine boundary, or the fold's trust rests on it. Everything else is do, absorbed into the operation it served. The graph is a ledger of commitments, not a trace of thought.

When the work is done, the execution graph folds into the node whose ask spawned it. The result becomes that node's material, and the steps become its history.

Folding preserves relations. A folded graph keeps its nodes and the relations between them, so the history reads as the graph it was, not a flat log.

A folded graph's folder holds its history, kept whole; everything else the work made lands in the parent as if made there directly.

An open graph's folder sits in its parent's work/; the act that folds it moves it to archive/. Neither exists empty.

A folding condition is what makes a graph ready to fold. Its ask is met, or it is abandoned. Until then the graph stays open.

A graph that cannot meet its folding condition does not fold dirty: it returns as a decision — abandon, re-cut, or change the ask — and a changed ask that touches endorsed intent is the operator's.

A check names an observation about the work, not an act of trust in it.

The episode that does the work is disposable; the checks at the fold's boundary are what survive it. A folded graph can be trusted only as far as those checks reach — whatever they did not cover rests on the word of a worker who no longer exists to be questioned.

Folds stack, and error compounds up the stack: whatever doubt a fold carries, everything built on it inherits. The weaker a graph's checks, the shallower it must stay before folding, and the less may be built on top of it.

However deep the graph grows, the operator's queue grows only with decisions that narrow intent; the day operator load tracks work volume, decomposition has failed.

A view of a graph never lags it: every view is read live from the graph or updated in the same act that folds it.
