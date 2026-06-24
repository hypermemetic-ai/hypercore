---
kind: ask
state: folded
owner: operator
created: 2026-06-23
folded: 2026-06-23
---
# worker-build-reaches-main — close the fence→main gap so a code-bearing ask can complete autonomously

The first live worker run (2026-06-23, build-only, on `operator-view-readiness`) surfaced a gap
deeper than the timeout it tripped on: **the fold merges the worker's spec delta but never its engine
code.** A worker builds and proves its implementation inside its fence, and the gates verify it
*there* — `conditions._depth` reads `result.worktree`, `scenario.gate` runs the touched capability's
scenarios red→green in the fence — and then `delta.fold` writes only three things to main: the spec
capability files, the re-rendered channels, and the node's archive move (`delta.py:150–159`).
`teardown` then deletes the fence branch. No `git merge` / `cherry-pick` / `rebase` of `worker/<id>`
exists anywhere in the engine, and nothing copies the fence's `.py` files out — so the implementation
the worker built is thrown away with the branch, and only the spec delta crosses.

For a spec-only or trivial delta this is invisible: the acceptance harness folds exactly those, which
is why `--check` is green and the seam reads "built". For a **code-bearing** ask it is a correctness
hole. The worker's `view.py` build (say) is verified in the fence, the spec scenario folds to main,
the node archives **done** — and main's engine never changed, so the folded scenario's check now runs
against the old engine and goes **red**, the ask falsely marked complete. This is the real content of
the "never run live" honest limit the README records: the autonomy seam can evolve the spec, but it
cannot yet land a code-bearing build on main.

Closing it is a load-bearing interface decision, not a patch — **design-it-twice** territory: how does
a fenced build reach main as one act with the spec fold? Candidate seams to weigh — the architect
cherry-picks the verified `worker/<id>` tip into the fold's held commit; the worker hands back a patch
beside its delta and the fold applies it; the fold fast-forwards main onto the fence tip. Each must
hold against the single-writer line (`tree.serialized`) and the H1 atomic spec⟺archive guarantee:
whatever merges the code must be the **same held commit** that folds the spec and archives the node,
or the atomicity the system already guarantees breaks. The gate that proves the build in the fence and
the act that lands it on main must not diverge.

A related, smaller finding from the same run, independent of this one and notable so it is not lost:
the model transport's `_summon` timeout is a single hardcoded 120s (`transport.py:56`) shared by the
architect's quick calls and the worker's long build. A real worker build exceeds it — the run timed
out at 120s, while a small `omp` probe returned in ~9s, so it is build time, not baseline latency. The
summon timeout should be role-aware (generous for the worker, short for the architect, named in the
one transport module). It blocks any live worker run and can be fixed anytime; it is **not** folded
into this node's design work.

Provenance: this session's first autonomous run (build-only, `operator-view-readiness`) and the read
of the crossing — `worker.run` → `apply` → `communication.integrate` → `delta.fold` →
`worker.teardown`. Nothing standing depends on this note; it cites the run as a footnote.

## folding condition
- a worker's verified fenced build — its engine code, not only its spec delta — reaches main as part
  of the same atomic act that folds the spec and archives the node, so a code-bearing ask completes
  through the crossing without leaving main red or the node falsely archived;
- the design pick and its grounds are recorded as material on the contest node (design-it-twice);
- `python3 -m engine --check` carries an acceptance check that a code-bearing delta's implementation
  lands on main, and is green.
