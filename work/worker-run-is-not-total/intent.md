---
kind: ask
state: standing
owner: operator
created: 1782588514
---
`worker.run` is not total on its own — a crossing that raises surfaces no decision card unless the scheduler is the caller, so the documented hand-driven dispatch path loses the failure silently.

The system's totality promise (engine/schedule.py:24-27) is that every worker resolves to exactly one terminal: its delta folds, or it escalates as a decision card on the operator's queue — a node can neither crash the loop nor sit stranded in flight. But that guarantee is split across two modules. `worker.run`'s exception path is `tree.recover(node); raise` (engine/worker.py:304-306) — it recovers the node to standing and RE-RAISES, delegating the card to the caller ("the scheduler turns it into a decision card"). The card is only ever raised in `Scheduler._fail` → `tree.raise_card(parent=node.id)` (engine/schedule.py:136-142), reached via `_work`'s `except` (schedule.py:131-134).

So `worker.run` is total only when the scheduler wraps it. Called bare — exactly what a hand-driven dispatch does (`worker.run(tree.find(id))`, the documented dispatch-command path) — a raise (a codex/transport error, a mid-build kill) recovers the node to standing with NO card: the failure reason is lost, and the node silently returns to `tree.ready()`, immediately re-dispatchable. The "whole crossing, one terminal" abstraction `worker.run` advertises in its own docstring (worker.py:286-295, which claims the not-done path's "decision card, parented to it, blocks re-dispatch") is only whole under the scheduler; the docstring overstates what `worker.run` alone delivers. Evidence: a hand-driven crossing this session raised, recovered the node, and left only a `recover:` commit — no card, no block, re-dispatchable, which invited a blind retry.

(The not-done-WITH-card paths — a folding condition unmet, an incoherent judgment, a `CannotFold` on merge — DO raise a parented card inside `communication.integrate` (engine/communication.py:116,125,136), so those are total even bare. The gap is the RAISE path only.)

To surface in grilling: whether `worker.run` should raise its own decision card in its `except` before re-raising (so the terminal is total at the worker boundary and the scheduler's `_fail` becomes a redundant safety net, or is removed), versus keeping the split and instead forbidding any bare `worker.run` caller (make the scheduler the only legal entry, and have the dispatch command drive through it) — the load-bearing seam is WHERE the totality guarantee lives, at the worker boundary or at the loop. A red→green scenario: a `worker.run` whose build raises, called WITHOUT a scheduler, leaves a decision card parented to the node (so the node is blocked, not silently re-ready) — red on today's engine, green on the fix.
