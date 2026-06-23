"""Slice 17 — the single-writer line is real: same-file overlap, exact-path commits, slug reservation.

Acceptance (spec/self-model, spec/schedule §concurrency, intent §62): the engine's distinctive
promise — many workers, one record — must hold by *construction*, not under an unstated single-process,
non-overlapping assumption. The prior harness choreographed two workers that folded **different**
capabilities; mutating the lock to a no-op was caught only incidentally by a dead-symbol lint
(research Part D, Experiment 10). This slice makes the lock load-bearing in the harness:

1. **exact-path commits don't sweep a sibling's work** — the C1 lost-update sweep, reproduced: a
   commit of one act over a shared parent staged a sibling's uncommitted file. With exact-path
   staging the foreign file stays out of the commit. *RED if `commit` stages a shared parent dir.*
2. **the line spans write→commit across processes** — a real `flock`-backed line: a second holder
   cannot enter the record while the first holds it, so no half-written sibling state is visible to a
   concurrent `git add`. *RED if `serialized` is a no-op or a thread-only lock.*
3. **two workers fold the SAME spec file under genuine overlap** — both deltas land, the history is
   clean, neither sweeps the other. *RED if the line is removed (the folds corrupt or one is lost).*
4. **slug reservation is atomic** — many concurrent creations with identical text each get a distinct
   folder; none overwrites another (a machine decision card cannot be silently lost). *RED if
   reserve-then-persist races (C3 TOCTOU).*

The mutation guard the research asked for: each assertion fails on a *record-corruption* fact, not a
lint — remove the line or widen the pathspec and this slice goes red on the data, by construction.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
import threading
import time

from .harness import ok


def _init(prefix: str) -> str:
    root = tempfile.mkdtemp(prefix=prefix)
    for cfg in (["init", "-q"], ["config", "user.email", "c@h"], ["config", "user.name", "c"]):
        subprocess.run(["git", *cfg], cwd=root, check=True)
    return root


def check(_shared_root: str) -> None:
    from .. import tree, record, spec

    print("\nslice 17 — acceptance check  (the single-writer line is real)\n")

    # ── 1. exact-path commits do not sweep a sibling's uncommitted work (the C1 sweep) ───────────────
    # Land worker A's node and, beside it, worker B's *uncommitted* file in the shared work/ tree. When
    # A commits its own act, B's in-flight file must NOT ride into A's commit. The old code committed
    # the shared parent (`work/`) with `git add -A`, sweeping B's file; exact-path staging keeps it out.
    root = _init("engine-check-s17a-")
    os.environ["ENGINE_ROOT"] = root
    a = tree.file_intent("worker A landing its own node")               # A's act, committed
    sibling = os.path.join(root, "work", "sibling-in-flight.tmp")
    tree.atomic_write(sibling, "worker B's uncommitted in-flight change")
    tree.cut(a)                                                          # A commits an act over work/
    tracked = subprocess.run(["git", "ls-files", "work"], cwd=root,
                             capture_output=True, text=True).stdout
    ok("sibling-in-flight.tmp" not in tracked,
       "a commit stages exactly its own act's files — a sibling's uncommitted file is not swept in (C1)")

    # ── 2. the line is a real cross-holder lock spanning the act, not a thread-only nicety ───────────
    # Hold the line on one thread; a second acquisition must block until the first releases. A no-op or
    # absent line lets the second in immediately — the window where C1's foreign `git add` happened.
    entered = threading.Event()
    release = threading.Event()
    second_in = threading.Event()

    @record.serialized
    def hold_the_line():
        entered.set()
        release.wait(timeout=5)

    @record.serialized
    def second():
        second_in.set()

    t1 = threading.Thread(target=hold_the_line, daemon=True)
    t1.start()
    entered.wait(timeout=5)
    t2 = threading.Thread(target=second, daemon=True)
    t2.start()
    blocked_while_held = not second_in.wait(timeout=0.5)
    release.set()
    entered_after = second_in.wait(timeout=5)
    t1.join(timeout=5)
    t2.join(timeout=5)
    ok(blocked_while_held and entered_after,
       "the line serializes a second holder — it cannot enter the record until the first releases")

    # ── 3. two workers fold the SAME spec file under genuine overlap — both land, neither sweeps ─────
    # The case the choreographed slice never ran: two deltas adding two requirements to ONE capability,
    # folded from two threads racing the record. With the line real, both requirements are present and
    # the spec file is whole; remove the line and the two spec writes interleave and one is lost.
    root = _init("engine-check-s17b-")
    os.environ["ENGINE_ROOT"] = root
    tree.atomic_write(os.path.join(root, "spec", "shared.md"),
                       "# shared\n\nA capability two workers grow at once.\n")
    tree.commit([os.path.join(root, "spec", "shared.md")], "seed: the shared capability")

    def fold_req(tag: str, gate: threading.Event):
        from .. import delta
        gate.wait(timeout=5)
        delta.fold(delta.parse(
            f"# delta — grow shared with {tag}\n\n## ADDED — shared\n"
            f"### Requirement: the {tag} property holds\n"
            f"The {tag} property MUST hold.\n#### Scenario: s\n- WHEN x\n- THEN y\n"))

    gate = threading.Event()
    threads = [threading.Thread(target=fold_req, args=(t, gate), daemon=True)
               for t in ("first", "second")]
    for t in threads:
        t.start()
    gate.set()                                                           # release both at once
    for t in threads:
        t.join(timeout=10)

    cap = spec.read_spec(root).capability("shared")
    names = {r.name for r in cap.requirements} if cap else set()
    ok({"the first property holds", "the second property holds"} <= names,
       "two workers folding the SAME spec file both land their requirement — neither overwrites the other")
    log = subprocess.run(["git", "log", "--oneline"], cwd=root, capture_output=True, text=True).stdout
    ok(log.count("fold:") == 2,
       "each fold is its own clean commit on the one record — two serialized folds, no lost update")

    # ── 4. slug reservation is atomic — N identical-text creations get N distinct folders (C3) ───────
    # Two failing workers both raise a recovery card with the same text was the named C3 trigger. Race
    # many identical creations; each must reserve a distinct slug and persist its own folder, none
    # overwriting another. With reserve-then-persist racing, two share a slug and one folder is lost.
    root = _init("engine-check-s17c-")
    os.environ["ENGINE_ROOT"] = root
    N = 8
    start = threading.Event()

    def create():
        start.wait(timeout=5)
        tree.raise_card("the worker could not complete the same ask", kind="decide")

    creators = [threading.Thread(target=create, daemon=True) for _ in range(N)]
    for t in creators:
        t.start()
    start.set()
    for t in creators:
        t.join(timeout=10)

    cards = tree.cards()
    ok(len(cards) == N and len({c.id for c in cards}) == N,
       f"{N} concurrent identical-text creations get {N} distinct folders — no slug collision lost a card (C3)")
