---
description: Orchestrate the open work — dispatch each ready node as its own fenced crossing (Claude architect + codex worker) from this higher thread; never build by hand.
argument-hint: "[node-id | next | (empty = plan the sweep)]"
allowed-tools: Bash, Read, Agent
---

You are the **dispatch orchestrator** — a thin higher thread over hypercore's open work. You mirror
`engine/schedule.py`'s `Scheduler`, driven watchably. Read `engine/schedule.py` once for the
authority on continuous / concurrent / off-the-operator's-path; this command is how you drive it by hand
without *doing the work* by hand.

## The one rule

You do not grill, design, build, integrate, or fold anything yourself. Each of those runs in its own
sub-thread. You read ready work, dispatch each node's crossing, reap one terminal line per node, and
surface decisions to the operator. Your context holds only the dispatch table — never a node's grilling,
a build transcript, or a diff. An orchestrator that edits `engine/` or `spec/` by hand has become the
failure this command exists to prevent.

## The roles, pinned

- **Architect = Claude.** Grilling, design-it-twice, the integrate judgment. Operator-facing.
- **Worker = codex (GPT), fenced.** It only *applies* an architect-proposed delta inside its own git
  worktree under an OS jail. It never authors the check that judges it (`spec/worker.md`,
  `work/worker-builds-proposed-delta`).
- The engine already wires this: `worker.run(node)` with no transport runs the codex worker fenced
  (`worker_transport`) and the Claude architect integrate (`communication.integrate` → `call` →
  `claude -p`). You reuse it; you do not reimplement it.

## Step 1 — read the order and the live ready work

- Read `work/the-hand-cranked-dispatch/dispatch.md`: the rank order, the **dependency & conflict map**,
  and each node's route / grilling residue (⚑) / design notes. It is a snapshot and goes stale as
  siblings fold — trust it for *grounds and ordering*, never as the live set.
- Read the live ready set: `python3 -c "from engine import tree; print([n.id for n in tree.ready()])"`.
  Re-read it after every fold; it shrinks as work lands.

## Step 2 — pick the next node, honoring three constraints

- **The conflict map.** Two fenced workers touching one `engine/*.py` file or co-modifying one spec
  requirement churn at integrate — the scheduler honors no conflict map. So never run two nodes from one
  file-contention group at once; serialize within each group, and run only the **parallel-safe singles**
  concurrently.
- **Sequencing edges.** Do the left of each edge before the right (e.g. `#7 → #11`).
- **Skip what is not a fenced-worker crossing.** Never dispatch `the-hand-cranked-dispatch` (this
  snapshot — it builds nothing) or any node whose `intent.md` declares it changes no capability. A node
  whose plan is a research campaign or architect-direct authoring (e.g. `weak-model-loop-harness`, the
  preamble of `communication-mastery`) is **not** a `worker.run` job — surface it to the operator as
  needing a different route, do not force it through a codex fence.

## Step 3 — de-risk the first live crossing

If **no** crossing has ever folded on this tree, dispatch exactly **one** node first — the safest:
**`the-candidate-prompt-speaks-as-the-architect`** (below-floor, one edit, no design). Stop after it
folds and report to the operator before widening.

Judge "no crossing has folded" by the **archive**, never the live-run gate:
`python3 -c "from engine import tree; print([n.id for n in tree.read_tree() if n.folded])"`. The
`view._live_status` signal still reads `never-run-live` even after fenced crossings fold — that gate is a
known defect with its own ask (`the-live-run-gate-sees-the-crossing`), so do not gate de-risk on it. If
the named de-risk node is itself already archived, the de-risk is done — go straight to Step 4.

## Step 4 — dispatch one crossing per node, as a sub-agent

For each chosen node, spawn one **`claude` architect sub-agent** (the Agent tool). Its prompt:

1. **Load the route's skills first** — the `route:` line in the node's `dispatch.md` entry names them
   (`skills/<name>/SKILL.md`). Work from the skill, not from memory.
2. **Grill the node** to a contract and an **architect-proposed delta + scenarios** on the node, using
   the ⚑ residue and leans in `dispatch.md` as the pre-chewed input. The delta must be the form the
   engine reads — verify with
   `python3 -c "from engine import grill, tree; print(bool(grill.delta_of(tree.find('<id>'))))"` → `True`
   before building. If a genuine fork remains, the ask touches endorsed intent, or a ⚑ cannot be
   settled, **stop and return an escalation** — never guess past a real decision.
3. **Run design-it-twice** if the node is marked for it: an isolated candidate contest, pick on depth /
   locality / seam placement, record the decision as material on the contest node.
4. **Dispatch the codex worker as a tracked background job — never synchronously.** A real crossing
   builds for ~15–25 min, longer than any single Bash call may run (the tool caps one call near 10 min).
   Do **not** run `worker.run` in one foreground Bash call — it is killed mid-build and strands the node
   in flight. Do **not** detach it with raw `nohup` — the harness does not track it, so nothing reaps it
   and you are left guessing whether it finished. Instead launch a tiny driver as a **harness-tracked
   background job** (Bash `run_in_background: true`); the driver runs `worker.run(tree.find('<id>'))` and,
   as its **last** action, writes a small **result file** holding `done`, the post-run
   `tree.find('<id>').folded`, and any exception text — never a transcript. Then **poll to completion**
   across as many tool calls as the build needs: block in bounded waits
   (`timeout 540 tail --pid=<pid> -f /dev/null`) until the driver exits, then read the result file.
   `worker.run` builds fenced on codex, turns the `#### Scenario:` checks red→green, integrates as the
   architect, and folds on success; its codex/integrate subprocess transcripts never enter your context.
5. **Return one line — one of three terminals**, read off the result file, never guessed mid-flight:
   - `folded` — `tree.find('<id>').folded` is `True` (the folder is under `work/archive/`; `find` returns
     archived nodes, so check `.folded`, never `find is None`) and `python3 -m engine --check` is green.
   - `escalated: <the decision, in the operator's terms>` — the crossing returned **not-done with a
     decision card** (an integrate refusal: a folding condition unmet, judged incoherent, or a build that
     did not hold on merge — a scenario-subprocess timeout surfaces this way too). The card is on the
     queue.
   - `failed: <the reason>` — the crossing **raised** (a codex/transport error, or the job was killed) or
     recovered the node **without** a card. Under this hand-driven `worker.run` no card is raised on the
     raise path (only the live scheduler raises it), so you carry the reason out. Do **not** retry.
   Return nothing else — no diff, no transcript.

Run parallel-safe nodes by spawning their sub-agents in one message; cap concurrency at **2** (the
scheduler's default `LIMIT`) so the watch stays legible.

## Step 5 — reap and surface

- Keep a dispatch table in your reply: node → `queued` / `in-flight` / `folded` / `escalated` / `failed`.
- Confirm each fold structurally: read `tree.find('<id>').folded` (location-authoritative — the folder
  sits under `work/archive/`; `find` returns archived nodes, so a folded node is `.folded`, never
  `find is None`) and `python3 -m engine --check` is green.
- Each crossing resolves to one of three terminals. **folded** — confirmed as above. **escalated** — it
  came back not-done with a decision card on the queue; surface the decision (abandon / re-cut / change
  the ask). **failed** — it raised or recovered without a card; surface the reason yourself (this
  hand-driven path raises no card on a raise — only the live scheduler does; the engine fix is a filed
  ask). Do not auto-resolve and do not retry by hand.
- **Confirm a crossing is dead before you touch its fence.** Before recovering a stranded node or
  removing a worktree, positively confirm no live process is on it: read the driver's result file *and*
  scan the full process tree of its pid and children (`ps`/`pstree`), never a narrow name grep — a
  harness-tracked background build can be mid-flight and invisible to a filtered `ps`, and acting on a
  wrong "it's dead" destroys a live ~20-min build.

## The floor

Dispatching spends codex and edits the live tree — a decisions-floor act (`intent.md` §70). Confirm the
operator's go before the first dispatch. Stop and hand back a decision whenever a node escalates, a
grilling pass hits a real fork, or a crossing fails. Going quiet with every ready node either folded or
escalated is success, not idleness.

## Arguments

`$ARGUMENTS` — a node id dispatches just that node; `next` dispatches the next ready node by the order
above; empty plans the full sweep and starts with the de-risk crossing (Step 3).
