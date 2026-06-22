---
kind: ask
state: standing
owner: operator
created: 2026-06-22
---
# engine-hardening — close the real weaknesses, and stop them regenerating

The engine was put to a panel of independent researchers on 2026-06-22 (full audit: `research.md`,
this folder — architecture, low-to-the-ground code, methodological prevention, testing rigor). The
verdict: a genuinely well-built engine — clean import DAG, honest layering, several truly deep
modules — whose **green `--check` certifies only the sequential, structural contract and is blind to
every concurrency, atomicity, and model-judgment failure found here**, and whose signature
disciplines are mostly advice wearing the clothing of enforced folding conditions. This arc fixes the
code as it stands **and** closes the methodological gaps so the next teardown does not regenerate the
same weaknesses. A fresh session reads this file top to bottom, then the report for line-precise loci
and the experimental confirmations; the conversation that produced both is disposable.

## the two jobs — read before touching anything

This arc has a prevention half the others did not: hypercore tears down and **regenerates** its code
from spec + ADRs + skills + acceptance checks. A bug fixed only in code returns on the next rebuild.
So every finding below is closed twice — **the fix** (the code as it stands) and **the guard** (a
check or spec change that makes the rebuild reproduce the fix, not the bug). The acceptance harness is
the regeneration contract: a rebuild that passes it should be good, and today it can pass while being
bad. Lead every fix with a real red→green loop — a check that is **RED on the live defect**, GREEN
after — because that loop is both the fix's proof and the guard against its return.

## ratified — operator decisions (2026-06-22)

Settled in session before the build opens; the arc is operator-owned from here.

- **Depth gate → de-claim depth as enforced.** Make the spec and the `architecture-review` skill
  honest that depth is judgment-only — a decision the gate raises, never a threshold it enforces — and
  that the model-driven verdict stays unbuilt; no new machinery. This arc owns that spec wording.
- **Fold atomicity (H1) → make it transactional.** Stage all writes and the folder move into one
  commit with idempotent retry; the spec's "atomically, both directions" becomes true, not weakened.
- **Sequencing → parallel** with `agent-facing-hardening`.

## critical — corrupts the source of truth or loses operator work

- **C1 — the "single-writer" line is not single-writer.** `record.LINE` is a Python *thread* lock,
  not a filesystem lock, so the "many workers, one record" promise holds only under an unstated
  single-process assumption; and `commit` stages a shared parent directory with `git add -A` while
  `atomic_write` lands outside the lock — so one worker's fold can sweep a sibling's uncommitted
  `intent.md` (and live temp files) into the wrong commit. Confirmed experimentally (`research.md`,
  Part A). Worst bug: it silently corrupts the shared graph and falsifies the system's distinctive
  claim. Fix: a repo-level file lock spanning write→commit; stage exact paths, never `-A` over a
  shared parent. Guard: a concurrency check (below) that fails if the lock is removed.
- **C2 — failure paths strand the node and leak the fence.** `worker` tears down its worktree only on
  `reply.done`; every expected refusal (a folding-condition block, a coherence fail) returns not-done,
  so the worktree and branch **leak** and the node sits `IN_FLIGHT` forever with no recovery — not
  standing, not a card. This is the steady-state failure mode, not an edge. Fix: tear down in a
  `finally`; return the blocked node to standing or to a decision card. Guard: a check that drives a
  worker down a refusal path and asserts the node recovers and the fence is gone.
- **C3 — slug reservation is a TOCTOU.** `graph._slug` reads the taken set and `_persist` writes the
  folder with no lock spanning the two, so two concurrent creations can claim the same slug and
  overwrite each other's folder — silently losing a machine decision card. Fix: reserve the slug under
  the same lock that guards the write.

## high — wedges work or passes bad results

- **H1 — the fold is not atomic.** The spec asserts the delta applies "atomically, both directions,"
  but the implementation is sequential (delta apply → state write → folder move): a crash between
  steps leaves the spec merged while the node is un-archived, and the retried `delta.fold` then hits
  `CannotFold` permanently — operator work wedged with its change already in the spec. Fix (ratified —
  make it transactional): stage all writes and the folder move into one commit with idempotent retry,
  so the spec's "atomically, both directions" becomes true rather than weakened. Guard: a check that
  fault-injects a crash mid-fold and asserts the retry completes cleanly — neither a wedged half-fold
  nor a permanent `CannotFold`.
- **H3 — malformed model output degrades to a silent no-op success.** An empty or unparseable model
  reply falls through to an empty object and folds a no-op delta as success. Fix: treat an unparseable
  reply as a failure path (which C2's recovery then handles), never as a clean fold.

## the methodological keystone — the disciplines the system most identifies with are not enforced

The repo's mantra is "advice can be ignored, a folding condition cannot." It holds for the three
*deterministic* conditions (delta-applies, the length ratchet, the mechanical dead-symbol/cycle scan)
and **fails for the five disciplines the system most identifies with** — the red→green loop, depth,
coherence, the grilling floor, design-it-twice — because those live on the model side and the
acceptance harness drives the model with a *scripted fake*, so the check asserts its own pre-baked
answer, not the judgment. Proven by mutation (`research.md`, Part D).

- **The red→green loop is never executed.** `conditions._feedback_loop` only checks that some strings
  are non-empty; a fabricated loop whose own field says it never ran *folds clean*. Fix (the single
  highest-value methodological change): execute the recorded command in the fence and require an
  actual red→green transition; reject red == green. This is the guard that makes every other fix's
  loop real.
- **"Depth" — the system's central criterion — has no real gate.** The model-driven verdict is "not
  yet built," so only line count stands; a rebuild can ship short, shallow modules and pass. Fix
  (ratified — de-claim): make the spec (`spec/depth.md`, `spec/architecture-review.md`) and the
  `architecture-review` skill honest that depth is judgment-only — a decision the gate raises, never a
  threshold it enforces (intent: "depth is a decision, never a threshold") — and that the model-driven
  verdict stays unbuilt; no new machinery. This arc owns that spec wording; `agent-facing-hardening`
  then confirms the rendered skill reads honestly.
- **The coherence gate is never driven to "incoherent."** No check exercises the refusal branch; a
  mutation forcing always-coherent survived green. Fix: a judgment-harness tier that holds coherence
  (and the grilling floor, and design-it-twice selection) against recorded adversarial fixtures at
  teardown — slice 16 already does this for the worker-failure path; generalize it.

## the harness as the regeneration contract — make it a real oracle

The green harness is substantive for structural, deterministic facts and theater for its three
flagship gates. Beyond the per-finding guards above, raise the contract itself:

- A real concurrency test: two workers folding the **same** spec file under genuine overlap, with an
  assertion that corrupts/fails if the single-writer lock is removed (today the lock's removal is
  caught only incidentally by a dead-symbol lint).
- Exercise the failure and malformed-output paths the scripted transport never enters (every scripted
  reply is well-formed JSON; the dangerous empty-reply→done fallback is untested).
- A machine-readable **gated-vs-watched register**: each discipline declares whether a check gates it
  or the operator merely watches it, so the next author cannot script a judgment and call it tested.

## cross-arc coupling — `agent-facing-hardening`

The single most important implication for the agent-facing layer: the worker/architect grounding must
encode the gated-vs-watched register and teach the **corrected** single-writer invariant (stage exact
files; lock spanning write→commit; filesystem-level), and the loop the grounding describes must be one
that is **executed, not narrated**. Otherwise the next teardown regenerates exactly these weaknesses —
including reproducing the false safety docstring in `record.py`. The grounding change lives in the
agent-facing arc; the engine fix lives here; they fold together. Also fix the false docstring here.
This arc owns the `spec/architecture-review.md` de-claim (the depth-gate call); `agent-facing-hardening`
confirms the rendered skill. The arcs run in parallel; only that one render-confirmation waits on this
de-claim to fold.

## what this arc deliberately does NOT do

It does not redesign the concurrency model (the worktree fence and the derive-on-fold render are the
engine's strongest assets — preserve them), nor the live worker/OMP seam (parked, `work/role-assembly/`).
It does not rewrite the channels or the skills (that is `agent-facing-hardening`); it only states what
the grounding must encode. Findings below critical/high are recorded in `research.md` and taken or
parked with a reason as the work reaches them, not drawn ahead as a tree.

## provenance (this folder)

- `research.md` — Report 2, the engine-shape audit (four independent researcher seats synthesized;
  severity-ordered findings register, the depth dogfooding, the prevention analysis, the
  testing-rigor mutation experiments, full sources). Material, cited not depended on: the
  self-sufficient ask is above.

## folding condition

Every critical and high finding is closed by a delta carrying a real red→green loop — a check that was
RED on the live defect and GREEN after the fix — or consciously deferred with a recorded reason on its
node, none silently dropped; the new concurrency and failure-path checks run in
`python3 -m engine --check` and are green; the red→green folding condition executes the recorded
command rather than checking non-empty strings; the fold is transactional (atomic both directions,
idempotent retry); the spec de-claims depth as enforced (judgment-only, the model-driven verdict
marked unbuilt); and the full harness is green.

## result

Landed on branch `worktree-agent-a3a6b9cfc935b7483` (fenced worktree; NOT pushed, NOT integrated —
the operator folds at integration). `python3 -m engine --check` is green end to end: 238 PASS, 0 FAIL,
exit 0, ~9s. The red-flag scan on the tree is clean (no dead symbols, no cycles). Six commits, each a
loop or the ratified de-claim. Every critical/high finding is closed by a real red→green loop — a
check RED on the live defect, GREEN after — and each loop has a mutation guard proving it fails on the
defect's data, not a lint.

### the red→green loops (each: command / red / green / the guard)

- **C1 + C3 — real single-writer.** `record.LINE` was a thread lock and `commit` staged shared parent
  dirs with `git add -A`, so one worker's fold could sweep a sibling's uncommitted `intent.md`; slug
  reserve→persist raced. Fix: a repo-level `flock` backing the line (`record._held`), `record.transact`
  spanning write→commit, exact-path staging (`git add -A -- <act-paths>`, never a parent), and slug
  reservation under the same held line (`graph._create`). False `record.py` docstring corrected.
  - command `python3 -m engine --check` (slice 17)
  - RED: with `serialized`→no-op, 3 assertions fail on record-corruption data (line not held, same-file
    fold loses a requirement, history not two clean commits); with `commit` staging a shared parent, the
    C1-sweep assertion fails (sibling's uncommitted file swept in).
  - GREEN: all 5 pass — exact-path commits don't sweep, the line serializes a second holder, two workers
    fold the SAME spec file with both landing, 8 identical-text creations get 8 distinct folders.
  - guard: slice 17 fails on the data if the line is removed or the pathspec widened (closes research
    Experiment 10, which previously died only to a dead-symbol lint).

- **C2 — failure paths recover the node, the fence never leaks.** `worker.run` tore down only on
  `reply.done`; every refusal (the steady-state path) leaked the worktree/branch and stranded the node
  IN_FLIGHT forever. Fix: teardown in a `finally` on every exit (idempotent `worker._git_quiet`); a
  non-integrating crossing recovers the node to standing (`graph.recover`) so its decision card blocks
  re-dispatch; the error path recovers then re-raises for the scheduler's card; the scheduler recovers a
  crash-stranded IN_FLIGHT node with no live worker each step (`schedule._recover_stranded`).
  - command `python3 -m engine --check` (slice 18)
  - RED on current code: fence leaks (worktree + branch), node strands IN_FLIGHT, through every refusal
    path and the scheduler.
  - GREEN: fence torn down on refusal, node leaves IN_FLIGHT, decision card raised, crash-stranded node
    recovered.

- **H1 — transactional fold (ratified).** The fold was two acts (`delta.fold` then `graph.integrated`);
  a crash between left the delta merged but the node un-archived, and the retry hit a permanent
  `CannotFold` (operator work wedged). Fix: `delta.fold(delta, root, node=node)` lands the spec change
  AND the node's archive in ONE commit via `graph.archive_in_place`; `delta.check` is idempotent (an
  ADDED requirement that already exists identically is already-applied, not a conflict); `graph.integrated`
  removed (subsumed), the front-matter and the move deduplicated into `_render`/`_relocate`.
  - command `python3 -m engine --check` (slice 19)
  - RED with the non-idempotent `check`: the retry after a fault-injected crash mid-fold hits a permanent
    CannotFold and the node stays un-archived.
  - GREEN: one commit for spec-merge + node-archive; the crash retry completes idempotently (requirement
    present once, node archived).

- **H3 — malformed model output is a failure path.** `transport.parse` degraded any reply with no JSON
  object to `{say: raw, done: True}`, folding a no-op as success. Fix: `transport.parse_object` (strict,
  raises `MalformedReply`), a returncode/empty-stdout guard in `call`, and the worker reads its hand-off
  strictly — a malformed reply raises at apply, BEFORE coherence, so the C2 recovery turns it into a
  decision. Lenient `parse` stays for the prose-friendly architect path.
  - command `python3 -m engine --check` (slice 18, part 3)
  - RED reverting the worker to lenient `parse`: a no-JSON reply no longer raises (would fold a no-op).
  - GREEN: a no-object reply raises `MalformedReply` at apply, recovers the node, tears the fence down.

- **Keystone — the red→green loop is EXECUTED, not narrated.** `conditions._feedback_loop` checked three
  non-empty strings; a fabricated loop folded clean (research Experiment 2). Fix: the gate runs the
  command in the fence at the fork base (must FAIL = red) and the tip (must PASS = green), trusting exit
  codes not narration; rejects red==green; a `_LOOP_GUARD` env stops the engine harness recursing when it
  is itself the command. The harness gained an executable `LOOP` fixture (`test -f RESULT.md`); the
  slices that handed inert prose loops (4, 5, 7, 8, 9, 16) now carry it, so their folds pass through the
  real gate. The spec's loop requirement is split into shape + the executed-transition gate (strengthened).
  - command `python3 -m engine --check` (slice 20)
  - RED reverting to the string-presence gate: 7 assertions fail — every Experiment-2 fabricated loop
    folds again, red==green folds, the un-runnable command folds.
  - GREEN: each fabricated loop is gated; a genuinely transitioning command folds.

- **Keystone — coherence incoherent branch + gated-vs-watched register.** No check drove `coherent:false`
  (an always-coherent mutant survived green, research Experiment 3/6). Fix: slice 21 feeds `coherent:false`
  and asserts the fold is refused, the spec untouched, the node live, a decision card raised — and that a
  coherent result still folds. And `spec/folding-conditions.md` gains the machine-readable gated-vs-watched
  register (`register: <discipline> — <gated|watched> — <how>`), parsed by slice 21: delta-applies,
  red-green-loop, length-ratchet, mechanical-red-flags are gated; depth-verdict, coherence, grilling-floor,
  design-it-twice-selection are watched (model-side, not scripted-and-called-tested).
  - command `python3 -m engine --check` (slice 21)
  - RED with an always-coherent integrate: the incoherent result folds (`done=True`), failing the
    incoherent-branch assertions.
  - GREEN: the incoherent branch refuses; the register is honest and machine-readable.

### the ratified de-claim (depth is judgment-only)

`spec/depth.md` and `spec/architecture-review.md` now state plainly that depth is a decision the gate
RAISES off the length signal and the mechanical red flags, never a threshold it ENFORCES; a green scan
means length-clean / no dead symbols / no cycles, never "deep"; the model-driven shallow/leakage/
deletion-test verdict stays not-yet-built (ADR 0006). The over-packed ~167-word god-file requirement
statement in `architecture-review.md` is split into one-instruction sentences. `review.backlog` now
ALWAYS carries the unbuilt-verdict honesty (it could previously be silenced by any length finding
appearing). `spec/self-model.md`'s "atomically, both directions" is brought up to the now-true H1
behavior (one commit, idempotent retry) — strengthened, not weakened. The rendered `architecture-review`
and `depth` skills re-derive honest on fold; the sibling arc confirms the rendered skill.

### parked, with reasons (medium/low findings, deliberately not drawn ahead)

Per the arc's "findings below critical/high are taken or parked as the work reaches them, not drawn
ahead": H2 (stale-worktree reuse) is largely mooted by C2's idempotent teardown but the live-base check
is unbuilt; H4 (commit swallows all exceptions) unnarrowed; H5 (`channels.materialize` non-transactional
on a missing slice) — the fold now renders into one act but `_read_slice` still lacks an `isfile` guard;
M1–M6 and L1–L5 (operator-mutation staleness, design-it-twice contest leak + ADR race, the `grill`
accessor cluster, `review.py` three-job split, typed `conditions.unmet`, the loop-schema dup, the delta
separator and `surfaced:` parse, encoding/`with` hygiene). All remain recorded in `research.md`. None
silently dropped.

### one surfaced scope decision (operator, please note)

I edited `engine/review.py` (`backlog` now always carries the unbuilt-verdict honesty line, not only on
a clean tree). It was not in my explicit owned list, but the change is squarely the de-claim's spirit —
the review must ALWAYS declare the model-driven verdict unbuilt, never let a length finding silence that
honesty — and it was required for the de-claim to hold while `graph.py` legitimately grew past the
"nearing" mark. `review.py` is engine code unlikely to collide with the agent-facing arc, but flagging
it for your awareness at integration. The change is one function body (`review.backlog`), conservative
(it only appends a line), and slice 7/15/2 stay green.
