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

The machine never silently commits the operator's resources: scope calls that change what the operator must later judge, build machinery, or decline their intent are theirs to make; within endorsed intent the machine scopes freely and visibly. Every decision records its grounds at the moment it is made.

## structure

Intent starts work; material is what the work makes. Intent comes whole from the operator — rarely — or out of back-and-forth with the machine. It constrains the problem space; decisions along the way narrow it further. Finished material is validated against both. The point is operator knowledge: their model of the system matches what gets built and what reaches the real world.

Intent lives relative to a work graph, folded or unfolded: the graph's folder contains its intent. hypercore is itself a folded work graph; this repository is its folder. Everything in it that is not intent is material.

A work graph's intent document is that graph's current intended reality.

## statements

A statement is plain, declarative, and strong enough to be wrong — wrong against material, evidence, or later judgment.

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

Within an execution graph, one name means one concept.

A folder holds one execution graph. The unit on disk is the execution graph, not the single node.

Work is made of operations. An operation is one move on the problem state, of four kinds: ask, check, decide, do — one word for each thing a statement must find, and do for everything else.

A new kind enters in the same edit as the statement that must find it, and stays only while a statement reads it; other new words are names for clusters.

An operation earns a node on two grounds only: it crossed the operator–machine boundary, or the fold's trust rests on it. Everything else is do, absorbed into the operation it served. The graph is a ledger of commitments, not a trace of thought.

When the work is done, the execution graph folds into the node whose ask spawned it. The result becomes that node's material, and the steps become its history.

Folding preserves relations. A folded graph keeps its nodes and the relations between them, so the history reads as the graph it was, not a flat log.

A folding condition is what makes a graph ready to fold. Its ask is met, or it is abandoned. Until then the graph stays open.

The episode that does the work is disposable; the checks at the fold's boundary are what survive it. A folded graph can be trusted only as far as those checks reach — whatever they did not cover rests on the word of a worker who no longer exists to be questioned.

Folds stack, and error compounds up the stack: whatever doubt a fold carries, everything built on it inherits. The weaker a graph's checks, the shallower it must stay before folding, and the less may be built on top of it.

A view of a graph never lags it: every view is read live from the graph or updated in the same act that folds it.
