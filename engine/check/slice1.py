"""Slice 1 — residue: the queue's settle path and the interface's render, awaiting their migrations.

The communication half of this slice — the thread, the architect's single operator-facing voice, the
three consequences (file / card / answer), durability landing on the tree rather than the thread, and
the no-raw-leak archive — has migrated to `communication`'s own executable scenarios
(`spec/communication.md`, `engine/worlds/communication_world.py`). What stays is the rest of the main
window: the **queue**'s three endorsements (a machine-owned card appears while awaiting, `explain`
returns the story and leaves it standing, `approve` folds and clears it, `cut` removes the words), the
**interface**'s pure-frame render (a screen built off any TTY), and the **durable record** (every act
committed). These are the queue's and the interface's concerns; they stay by-slice until those
capabilities migrate, at which point this file shrinks again and finally dissolves like the others.
"""
from __future__ import annotations

import os
import subprocess

from .harness import ok


def check(root: str) -> None:
    from .. import tree, render
    from ..communication import explain

    print("\nslice 1 — acceptance check  (residue: the queue's settle path and the interface render)\n")

    # 1. a machine-owned card stands on the queue while awaiting the operator (the queue is a view)
    card = tree.raise_card("the intake box pulls torrents from nyaa", kind="decide")
    ok(len(tree.cards()) == 1, "a machine-owned statement raises a card on the queue")
    ok(card.machine and card.is_card, "the card is machine-owned and awaiting the operator")

    # 2. explain tells the story toward the decision; the card stays on the queue
    story = explain(card, lambda _p: '{"say":"nyaa carries the releases; lean nyaa."}')
    ok(bool(story) and len(tree.cards()) == 1, "explain returns a story and leaves the card standing")

    # 3. approve endorses and the card leaves the queue — its folder folds into the archive
    tree.approve(card)
    ok(len(tree.cards()) == 0, "approve clears the card from the queue")
    endorsed = tree.find(card.id)
    ok(endorsed is not None and not endorsed.machine, "the endorsed node drops its [machine] marker")
    ok(os.path.isfile(os.path.join(root, "work", "archive", card.id, "intent.md")),
       "approving folds the decision — its folder moves to work/archive/ (location is authoritative)")

    # 4. cut removes the words: the node file leaves the tree
    doomed = tree.raise_card("a statement to cut")
    ok(len(tree.cards()) == 1, "a fresh card appears on the queue")
    tree.cut(doomed)
    ok(tree.find(doomed.id) is None, "cut removes the node from the tree")

    # 5. the render is pure and total over this state (no TTY) — the interface's pure-frame requirement
    rows = render.main_body(tree.read_tree(), 0)
    ok(isinstance(rows, list) and rows and rows[0][0][0] == "hypercore", "the main screen renders")

    # 6. durable state is version-controlled — every act committed to the one record
    log = subprocess.run(["git", "log", "--oneline"], cwd=root,
                         capture_output=True, text=True).stdout.strip().splitlines()
    ok(len(log) >= 4, f"every act committed to the durable record ({len(log)} commits)")
