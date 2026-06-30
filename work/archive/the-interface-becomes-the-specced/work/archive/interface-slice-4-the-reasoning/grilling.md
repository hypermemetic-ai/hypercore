surfaced: 0

[CONTRACT]
The reasoning loop opens on a model's working. A key pressed on any visible element tied to a model's working — a fenced worker running on a node, or the architect's own thread — opens a live loop onto that model's reasoning, rendered as one surface scoped to that one node, and on nothing else. The architect's own thread is fully steerable: the operator prunes a step, edits a step, and resets-and-reruns, steering the work by changing its shape. A fenced worker's trace is read-only — its steps are never edited and nothing is injected mid-run into the worker's session — and the operator acts at the node grain instead: prune the node, re-ask it, rerun it. The loop stays honest about its limit: a model's account of its own reasoning can be a confabulation, so it earns trust by what acting on it changes, not by how convincing the account looks — the surface anchors trust in the acts it offers and keeps that caveat legible. Validated against: the gated render scenarios (the loop opens on a model's working as one surface; the architect's thread steerable at the step grain while a fenced worker's trace is read-only with node-grain acts; the trust anchored in acting, not the account) go red→green. Watched on the running window: the live reasoning loop opened and steered by keystroke, confirmed on python3 -m engine.

[DELTA]
# delta — the node-grain reasoning loop

## ADDED — interface

### Requirement: a key on a model's working opens the live reasoning loop as one surface
The window MUST open a live reasoning loop when the operator presses the loop key on a visible element
tied to a model's working — a fenced worker running on a node, or the architect's own thread — and on
no other element: an at-rest node with no model working opens no loop. The loop renders onto that
model's reasoning as one surface, scoped to the one node it was opened on: the architect's own thread
and a fenced worker's trace are painted by the one loop render, never two divergent surfaces.

#### Scenario: the loop opens on a model's working, one surface for the thread and the worker trace
- WHEN the architect's own thread and a fenced worker's trace are each opened as a reasoning loop, and
  a loop is sought on an at-rest node with no model working
- THEN the working elements open a loop and the at-rest node opens none, and the thread and the worker
  trace are painted by the one loop surface, each scoped to its one node

  ```check
  loop-thread
  loop-worker
  opens-on-working
  one-surface
  ```

#### Scenario: the live reasoning loop opens and is steered by keystroke on the running window
- WHEN the operator presses the loop key on a running worker and on a thread, then acts on the loop
- THEN the loop opens onto the model's reasoning and the acts reshape the work, the live stream playing
  on the running window
- watched — a live keystroke-loop fact no headless fixture certifies, confirmed on the running window
  (`python3 -m engine`), the honest home of the interface's live loop

### Requirement: the architect's thread steers at the step grain; a fenced worker's trace is read-only with node-grain acts
The architect's own reasoning loop MUST be fully steerable at the step grain: the operator prunes a
step, edits a step, and resets-and-reruns, steering the work by changing its shape. A fenced worker's
trace MUST be read-only — its steps are never edited and nothing is injected mid-run into the worker's
session — and the operator acts at the node grain instead: prune the node, re-ask it, rerun it. The
loop MUST earn trust by what acting on it changes, not by how convincing the account looks: a model's
account of its own reasoning can be a confabulation, so the surface anchors trust in the acts it offers
and keeps that caveat legible, never presenting a trace as authoritative because it reads convincingly.

#### Scenario: the architect's thread is steerable at the step grain, a worker's trace is read-only with node-grain acts
- WHEN the architect's own thread loop and a fenced worker's trace loop are rendered
- THEN the thread offers the step-grain steering — prune a step, edit a step, reset and rerun — while
  the worker's trace is read-only, offering no step edit and instead the node-grain acts: prune the
  node, re-ask, rerun

  ```check
  loop-thread
  thread-steerable
  loop-worker
  trace-read-only
  ```

#### Scenario: the loop anchors trust in acting, not in the account
- WHEN a fenced worker's trace is rendered as a reasoning loop
- THEN the surface anchors trust in the acts it offers and carries the confabulation caveat legibly —
  trust is in what acting changes, not in how convincing the account reads

  ```check
  loop-worker
  trust-from-acting
  ```
