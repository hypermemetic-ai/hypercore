surfaced: 0

[Q] The queue is a live computed view of awaiting nodes, never stored — a node that resolves already falls out of the view on its own, and there is no card object to delete. So does "sweep the queue / drop the stale card" mean **cut the underlying nodes** (an operator endorsement the live view then reflects), or is it a **bug report** that the view is rendering duplicate/stale cards it should already have dropped (a defect in the view's dedup or liveness)?
lean: Treat it as cuts on nodes: collapse a duplicate set by cutting the redundant awaiting node(s), and "drop the stale card" by cutting only if re-derivation from the tree shows the node genuinely resolved — which, by spec, should already have dropped it from the live view, so expect that branch to be a no-op. The view recomputes; no card-edit mechanism is added. This honors "leave it if still live" directly: a still-awaiting node keeps its card untouched.
flip: If the operator can point at a card the live view should already have dropped — a resolved node still showing, or one node rendered twice — then it is the second reading: a queue-computation defect, and the ask reframes as fixing dedup/liveness in the view, not endorsing any cut.
answer: 

[Q] For the collapse: what marks two cards as "duplicates," and when collapsing a set, which one survives the cut? (Cut is destructive, and the view shows one card per awaiting node, so "duplicates" are distinct awaiting nodes.)
lean: Duplicate = same recorded kind + same call (same verb against the same target node). Since work does not spawn until a card is ratified, the redundant ones are unspawned and cheap to cut; keep the earliest-filed node (or the one carrying provenance / resolved descendants) and cut the rest.
flip: If a later duplicate carries more resolved state than the earliest — descendants, a partial verdict — keep the richer node and cut the earlier ones; "earliest survives" only holds when the duplicates are bare.
answer:
