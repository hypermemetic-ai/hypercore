---
kind: ask
state: standing
owner: operator
created: 2026-06-27
---
# the-hand-cranked-dispatch — order the open work by hand, as a learning snapshot

The operator wants to watch the system dispatch its own open work before trusting the autonomous loop to
do it. This node is that dry-run: the **ordering** half of the architect-and-scheduler's job — ranking
the open work and recording the methodology each item would be built under — computed by hand and written
down, so the operator can read what the system *would* produce and learn the shape of it first.

"Hand-cranked" is the **order**, not the **work**. Executing the items is the orchestrator's job
(`engine/schedule.py`'s `Scheduler`, driven watchably via `.claude/commands/dispatch.md`): a Claude
architect and codex workers, each fenced, run from a higher thread. This node never authorizes an
assistant to build the items by hand in one thread — that collapses the role split and overflows the
context. It records the order; it does not run the work.

**This is a snapshot, not the schedule.** hypercore computes the order as a live view, never a stored
list (`spec/schedule.md`, `spec/queue.md`, intent §110): the ready work is read off the tree each time,
so "nothing can go stale." A written order contradicts that on purpose — it is a frozen photograph taken
2026-06-27 over the twelve open siblings, for observation only. It goes stale the moment any sibling
folds, and that is expected: when the operator is ready to trust the loop, this node is abandoned and the
live view (or the renderer that prints it) replaces it. Read it to learn the dispatch discipline, not as
a source of truth the tree must stay in sync with.

The ordering claim and every per-node path are **machine-owned** — the machine's claim about what the
operator's attention is worth next, which it answers for (intent §59). The operator's word reorders it
instantly and unconditionally; the leans here are leans, not rulings.

The plan is the node's material: `dispatch.md` — the twelve open siblings in dispatch order, each
carrying the path the orchestrator drives it under (route → grilling residue → design → fenced build →
composition → fold).

## folding condition
- the operator has read the snapshot and taken from it what they wanted to learn about how the system
  orders and dispatches its open work;
- it folds or is abandoned when the operator runs the live loop — or builds the renderer that computes
  the order — which supersedes any stored copy;
- it builds nothing and changes no capability: it is an observation scaffold, so `python3 -m engine
  --check` is unaffected by its presence.
