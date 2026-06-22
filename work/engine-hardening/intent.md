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
