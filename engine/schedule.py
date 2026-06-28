"""The scheduler: the autonomous loop that keeps work moving.

hypercore's most distinctive promise is continuous, concurrent autonomous work (intent §60/§62): a
ratified ask must get *built*, not land as standing work while the system idles. The tree already
computes the ready work (`tree.ready`); this module is the loop that **consumes** it. It reads
the ready work off the one tree, runs a worker on each ready node, and keeps going while any unblocked
work remains — going quiet only when all that is left is a decision the operator owns. An idle system
with unblocked work left is a defect, not rest (intent §60).

Three properties define it, each structural, not a discipline to remember:

- **Continuous.** `step` takes the ready work and dispatches a worker per node, so work moves
  without the operator re-prompting. The same readiness that gates spawning gates scheduling
  (`tree.ready`, intent §110) — a node blocked on an open child is not taken — so the loop hands out
  the tree's own work and nothing in the schedule can go stale.

- **Concurrent, on one record.** Up to `limit` workers run at once, each fenced in its own worktree
  (the worker owns the fence). Their slow builds overlap; the shared git line is single-writer
  (`tree.serialized`), so their integrations serialize and no fold corrupts the record (intent §62).
  The scheduler is the orchestration; the fences are what make it safe, and they already exist.

- **Off the operator's path.** Each worker runs on its own thread and the loop polls; `step` never
  blocks, so the window only ever paints the live tree while work moves underneath it (the rule the
  interface keeps for the architect, held for the scheduler too). Dispatch is total: every worker
  resolves to exactly one terminal — its delta folds, or it escalates as a decision on the queue — so a
  node can neither crash the loop nor sit stranded in flight with no live worker (the folding-condition
  discipline: a tree that cannot meet its condition returns as a decision, it does not vanish).

The loop is elected per tree by a held repo-root lease. A peer window that cannot take the lease still
operates on the tree, but its scheduler dispatches nothing and recovers nothing; it keeps polling, so
when the holder exits the lease transfers on the next tick and stranded in-flight work can be recovered
by the one live loop. The transport is injectable — the live `claude -p` in the window, a scripted fake
in the acceptance check — so the loop drives deterministically under the harness without an LLM.
`--check` runs the scheduler over a throwaway root; only the live window points it at the real tree.
"""
from __future__ import annotations

import threading
import time

from . import record, tree, worker

LIMIT = 2          # workers at once — a starting value to tune, like the length signal, not a law
POLL = 0.2         # seconds between ready work reads while the background loop runs


class Scheduler:
    """The autonomous loop over the ready work. `step` is one non-blocking pass — the testable
    core; `start`/`stop` run it on a daemon thread for the live window. `running` is the node ids in
    flight under it, derived from the live threads for the view and the checks, never a stored
    work-list."""

    def __init__(self, transport=None, root: str | None = None, limit: int = LIMIT) -> None:
        # The injection point, forwarded to `worker.run` as-is. Left None for the live loop on purpose:
        # the worker then binds its own fence transport (cwd = its worktree, step 5) while the architect's
        # integrate uses the repo-root `call` — one collapsed `call` here would run the worker unfenced.
        # The harness injects a scripted fake, which both roles share.
        self.transport = transport
        self.root = root
        self.limit = limit
        self._lease = record.Lease(self.root or tree._root(), "loop")
        self._threads: dict[str, threading.Thread] = {}
        self._lock = threading.Lock()      # guards _threads only — not the shared record (tree.LINE)
        self._alive = False
        self._loop: threading.Thread | None = None

    # ── the loop ──────────────────────────────────────────────────────────────

    def step(self) -> None:
        """One pass: reap finished workers, recover any crash-stranded node, then dispatch the ready
        ready work up to the limit. Never blocks — the slow build runs on the dispatched worker's own
        thread, not here — so the caller (the window's input loop) is free the instant this returns.
        A peer scheduler that does not hold the repo-root loop lease returns before recovery or
        dispatch, so it cannot reset or double-take the holder's live node."""
        self._reap()
        if not self._lease.acquire():
            return
        self._recover_stranded()
        for node in tree.ready():
            with self._lock:
                if len(self._threads) >= self.limit:
                    break
                if node.id in self._threads:
                    continue
                t = threading.Thread(target=self._work, args=(node,), daemon=True)
                self._threads[node.id] = t
            t.start()

    def start(self) -> None:
        """Begin the background loop — a daemon thread reading the ready work on each tick — so work
        runs continuously while the operator does anything else, or nothing. Idempotent. A non-holder
        still starts this polling thread; it simply does no scheduling until it wins the lease."""
        if self._alive:
            return
        self._lease.acquire()
        self._alive = True
        self._loop = threading.Thread(target=self._run, daemon=True)
        self._loop.start()

    def stop(self) -> None:
        """Stop taking new ready work. Workers already in flight run to their natural hand-off; the
        live-loop lease releases here, and also if the process dies."""
        self._alive = False
        self._lease.release()

    @property
    def running(self) -> list[str]:
        """The node ids a worker is on right now — read off the live threads, a view not a list."""
        with self._lock:
            return list(self._threads)

    @property
    def live(self) -> bool:
        """Whether this scheduler currently holds the tree's autonomous-loop lease."""
        return self._lease.held

    # ── internals ─────────────────────────────────────────────────────────────

    def _run(self) -> None:
        while self._alive:
            try:
                self.step()
            except Exception:
                pass        # the loop outlives any one pass — a fault never stops the rest of the work
            time.sleep(POLL)

    def _work(self, node: tree.Node) -> None:
        """Run the whole crossing for one node on its own thread (`worker.run`: dispatch, build
        fenced, integrate, fold, tear down). A failure returns as a decision on the operator's queue
        rather than stalling the loop or dropping the node."""
        try:
            worker.run(node, self.transport, self.root)
        except Exception as e:
            self._fail(node, e)

    def _fail(self, node: tree.Node, err: Exception) -> None:
        """A worker that could not complete returns as a decision — never a silent stall. The node is
        in flight (it was taken); the card hands the operator the recovery the worker could not make."""
        tree.raise_card(
            f"the worker could not complete {tree._subject(node.text)!r}: {err} — "
            "abandon it, re-cut the ask, or change it",
            kind="decide", parent=node.id)

    def _reap(self) -> None:
        with self._lock:
            self._threads = {i: t for i, t in self._threads.items() if t.is_alive()}

    def _recover_stranded(self) -> None:
        """Recover a node left IN_FLIGHT with no live worker on it — a crash-stranded node (C2). The
        live worker's `run` recovers the node on every in-process exit; this catches the one path that
        bypasses it — a process killed mid-crossing, whose on-disk node still claims a worker. A node
        IN_FLIGHT that this scheduler is not running is that lie: return it to standing so the ready work
        picks it up again, never silently dropped on restart (the steady-state promise: a node never
        vanishes). The dispatched node is held under `_lock` so a just-started worker is never mistaken
        for stranded — its thread is recorded before its `dispatch` lands the IN_FLIGHT state."""
        with self._lock:
            running = set(self._threads)
        for node in tree.read_tree():
            if node.is_live and node.id not in running:
                tree.recover(node)
