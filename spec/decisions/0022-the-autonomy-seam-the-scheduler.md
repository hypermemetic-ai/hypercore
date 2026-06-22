# ADR 0022 — the autonomy seam: the scheduler runs the frontier

Status: **machine-built, awaiting ratification** (2026-06-22) — the operator asked to build the worker
seam (the coherence audit's parked move 3); the autonomy loop is below, acceptance-green. [machine]

## Context

hypercore's most distinctive promise is **continuous, concurrent autonomous work** (intent §60/§62):
a ratified ask must get *built*, and while any unblocked work remains a session is on it — "an idle
system with unblocked work left is a defect, not rest." The machinery for the crossing existed:
`worker.run` does delegate → build fenced → integrate → fold, and `graph` computed the ready frontier.
But **nothing consumed the frontier.** `worker.run` and `design.py` were reachable only from the
acceptance harness, never from `window.py`; a ratified ask spawned standing work and the system then
idled — precisely the §60 defect, built into the product. The coherence audit named this its
plot-level finding and parked it as **move 3, the autonomy seam** (`work/archive/coherence-audit/`).

This is distinct from the **multi-model harness seam** (role-assembly steps 5–6 — running the worker
as OMP/GPT-5.5 with `cwd` = the fence and the reference tail pulled just-in-time), which stays parked.
The autonomy loop wires the *existing* `claude -p` worker into a running system; the model upgrade is
an orthogonal, later axis.

## Decision

**Name the loop: `engine/schedule.py` — the scheduler.** A deep module with a small interface
(`step`, `start`, `stop`, `running`) hiding the thread set, the dedupe, the concurrency bound, and the
failure path. It reads the ready frontier and runs a worker on each node, and the window starts it so
work runs while the operator does anything else. Three properties, each structural:

- **Continuous** — `step` takes `graph.ready()` and dispatches a worker per node; the system goes quiet
  only when all that remains is a decision (intent §60). The same readiness that gates spawning gates
  scheduling: `graph.ready` is the §110 predicate (standing, nothing open beneath it), so a node
  blocked on an open child is not taken.
- **Concurrent on one record** — up to `LIMIT` workers run at once, each fenced (intent §62). To make
  the shared line safe under concurrent folds, **the one record became single-writer**: the
  git-touching acts serialize on a lock while the slow builds (the model calls) overlap outside it.
- **Off the operator's path / failure as a decision** — each worker runs on its own thread and `step`
  never blocks, so the input loop is never delayed; a worker that cannot complete raises a decision on
  its node and the loop keeps serving the rest — never crashing, never silently dropping the node.

**Single-writer deepened `graph` into `engine/record.py`.** Rather than scatter a lock through the
graph mutators, the durable-write floor — atomic write, scoped commit (`-A` over named paths, so
concurrent commits to different paths never sweep each other), and the one lock — moved into a module
of its own. `graph` re-exports it, so its callers read one façade unchanged. This both gave the lock a
principled home and resolved the real deepening signal the review had begun to flag: `graph.py` fell
from 327 to 283 lines, a coherent split along the data-model / durable-write seam (the same shape as
the `transport` extraction, ADR 0021).

**A latent bug the seam surfaced.** `worker.run` had never run end-to-end under a scripted transport —
the harness drove `apply` and `integrate` separately — so no test caught that `run` dropped the
transport on the integrate step (`conversation.integrate(node, result, root=root)`), falling back to a
live `claude` call. Wiring the scheduler exercised the whole crossing and exposed it; threading the
transport through is the fix. This is the dogfooding value the audit predicted: running the methodology
reveals what reading it does not.

The acceptance check is `engine/check/slice16.py`, driving the real scheduler, real graph, real
fences, and a real fold over a scripted transport — continuity, concurrency, readiness-gates-
scheduling, off-path dispatch, and failure-as-a-decision. The honest harness limit holds (slice-7-F1
precedent): a live `claude` actually building is the watched evidence (`python3 -m engine`), never
faked into the harness.

## Grounds

The deepest structural fix and the deepest product promise were the same act. The frontier predicate,
the fence, the crossing, and the fold all existed; what was missing was the loop that runs them — so
the seam is small in code and large in consequence. Making it concurrency-correct from the start (the
single-writer record) cost ~one small module and avoided a retrofit, and the fence machinery (ADR
0007) already assumed it. The new capability `spec/schedule.md` records the behavior; the scan reads no
red flags and every module is within the length signal.

## Relation

- **Resolves the coherence audit's move 3** (`work/archive/coherence-audit/`): the autonomy seam, its
  single largest parked finding.
- **Independent of role-assembly steps 5–6**: the worker is still `claude -p`; the OMP flip is parked.
- **Companion deepening to ADR 0021**: a second extraction along a real seam — `record` is to `graph`
  what `transport` was to `conversation`.
- **Leaves parked, as the audit recorded**: the atomic-fold overclaim (the scheduler now serializes
  integration but does not make the fold transactional), and `design.py` still architect-invoked, not
  scheduler-driven.
