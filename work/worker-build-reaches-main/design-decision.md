# design-it-twice: the verified fenced build reaches main [machine]

A load-bearing interface — how a worker's verified fenced build (its engine code, not only its spec
delta) reaches main as one atomic act with the spec fold — was designed twice: four candidates
(minimal, flexible, caller, ports), each fenced and isolated, each briefed to a radically different
shape, compared on depth, locality, and seam placement.

design-decision: the verified fenced build reaches main → hybrid — capture the code as a self-contained artifact on WorkerResult (caller seam), content-replay it inside the fold's one held transact (minimal mechanism), and re-verify the touched capability's scenarios on merged main before the commit (the keystone closing green-in-fence/red-on-main); a staleness pre-check fast-refuses an overlapping concurrent fold to a decision; no live fence is reached at fold time.

## The contest

- **minimal** — a private `_land_code` in `delta.py`, called inside `fold.land()`, replays the fence
  tip's blob content onto main and returns the exact paths. Deepest *interface* (one private function +
  one optional param, reuses the held commit and exact-path staging verbatim; the cleanest deletion
  test). Two costs decided against it: `delta.py` reaches into the fence (`git -C <worktree> show/diff`)
  — a locality leak, the fold learning about worktrees — and it is a blind file-granularity
  last-writer-wins with no conflict signal.
- **flexible** — `worker.capture_patch` → a `Patch` artifact `{diff bytes, paths, base, tip}`,
  `delta.apply_patch` with `--binary`/rename/`--3way`. Absorbs every file-op variation and is
  store-agnostic. Decided against: it buys a second durable store nobody needs yet (a richer noun,
  `Patch`, across the seam), and `--3way` is a weaker merge than git's own.
- **caller** — `WorkerResult` gains `code`, a self-contained diff captured at hand-off before teardown;
  the fold applies it exactly as it already applies `result.delta`. Best **locality** and **seam
  placement**: the seam falls on the existing worker→architect hand-off boundary, `delta.py` consumes a
  flat artifact and never touches a live fence, the fence becomes a pure build sandbox whose only
  outputs are the hand-off's strings. Its risk section carried the contest's sharpest insight — the gate
  verified against the *fence* base, so a clean apply can still be red on a moved main.
- **ports** — a `Build` port `{manifest, read, capture}` with a `FenceBuild` adapter; the fold consumes
  the port, git lives only in the adapter. Cleanest isolation. Decided against: a whole new module +
  protocol for a variation (a second store) that does not exist — over-built against the depth bar — and
  it honestly admits the core still needs a staleness guard the port alone cannot hide.

## The pick — why this is deepest

**Seam (from caller).** The code crosses as a third self-contained artifact on `WorkerResult` beside
`report` and `delta`, captured at hand-off before teardown. This places the seam exactly on hypercore's
real worker→architect boundary: the fold consumes a result, never a live fence. Best locality
(fence-knowledge stays in `worker.py`; `delta.py` only applies an artifact) and best seam placement (the
seam is the one the system already draws), where `minimal` leaks git into `delta.py` and `ports` places
its seam at a store-variation that does not yet vary.

**Mechanism (from minimal).** Content-replay of the verified bytes for the touched engine paths, landed
inside the fold's existing one held `transact` — no new commit, no new lock, exact-path staged. The
patch/`--3way` machinery (flexible, caller) becomes unnecessary under the keystone, so the simplest
apply is also the safe one: under the staleness pre-check the base is unchanged on the touched paths, so
the verified content applies onto exactly the context it was verified against — no merge to do.

**Keystone (synthesizing caller's and ports' risk sections — the contest's real yield).** The fold does
not merely trust the fence; it **re-verifies on main**. Inside the held transaction, after the code and
spec land on main and before the commit, the touched capability's scenarios run against the merged main:
green commits the one atomic act (code + spec + archive); red aborts so nothing lands, the node
recovering to standing with a decision — the existing refusal path (`schedule._fail` / `tree.recover`).
A cheap staleness pre-check (the touched paths' base images vs current main) fast-refuses the common
concurrent collision before the re-verify. This closes the verification-context ≠ application-context
hole every candidate flagged: green-in-fence can no longer mean red-on-main, because what is verified is
merged main itself.

## Held constraints
- **single-writer** — capture reads the fence (no lock); apply + re-verify + commit run inside `fold`'s
  existing `@tree.serialized` / `transact`. One writer, one held line, no new git-touching act.
- **H1 atomicity** — code + spec + archive join the one `transact`'s exact-path list: one commit, both
  directions. Idempotent retry unchanged — an already-applied delta reads as already-present, identical
  bytes re-`atomic_write` as a no-op.
- **exact-path staging (C1)** — the apply returns precisely the engine paths it wrote; never `-A` over a
  shared parent.
- **moved-main** — the staleness pre-check + re-verify-on-main: disjoint concurrent folds both land, an
  overlapping one refuses to a decision (re-dispatch off fresh HEAD), never a silent clobber or a
  stale-verified merge.
- **fence-teardown** — the code is captured into the hand-off before `run()`'s `finally` teardown; the
  fold consumes the artifact, not the fence.

## Recorded risk (machine-side, not escalated)
Re-verifying on main runs the touched scenarios inside the held single-writer line, so folds serialize
behind one another's re-verification — a throughput cost on the continuous/concurrent promise (intent
§62). It is tunable: scope the re-run to the touched capability, and the staleness pre-check skips it
when the base is unchanged. No operator-facing stake crosses — the contract (a verified build lands
atomically or becomes a decision, never a silent broken merge) is honored by the mechanism — so the pick
stays machine-side, no card.

## Carries forward (the contract for the build)
One ordinary worker `apply`, when the seam itself is built: `WorkerResult` gains a captured `code`
artifact (taken in `worker.apply`, before teardown); `delta.fold(.., code=)` content-replays it in
`land()`; the touched capability re-verifies on merged main inside the held transaction; the staleness
pre-check fast-refuses an overlapping fold. No new commit, lock, or transaction — it rides the existing
held-commit machinery. *Bootstrap note: this seam must itself be built outside the autonomy loop (it is
the thing that lets the loop land code), so its first build is freehand; once folded, code-bearing asks
can complete through the crossing.*
