# Report 2 — The Shape of hypercore's Engine

**A synthesis of four independent research seats — architecture, code review, methodological prevention, and testing rigor — adjudicated against the primary source.**

Panel 2 · Engine Shape · 2026-06-22
Scope: `engine/` (~4,800 LOC, 38 `.py` files, built in 16 slices). Acceptance harness `python3 -m engine --check` currently GREEN.
Method: each finding below was re-verified by the synthesis lead by reading the cited lines in the read-only tree (`engine/record.py`, `conditions.py`, `worker.py`, `graph.py`, `delta.py`, `conversation.py`, `transport.py`, `schedule.py`, `review.py`, `grill.py`, `check/__init__.py`, `check/slice16.py`). The single external fact the top finding rests on (git `add -A` pathspec semantics) was confirmed against the git documentation. No repo file was modified.

---

## Executive summary

hypercore's engine is, as built, **unusually well-made**: a clean import DAG with no cycles, honest layering, and a handful of genuinely deep modules (`record`, `transport`, `channels`) that are model examples of the doctrine the system preaches. Its signature design — N continuous workers, each fenced in its own git worktree, integrating to one shared git line — places its concurrency seam in exactly the right spot conceptually: *serialize the index, not the slow builds.* Credit where due, and it is substantial.

But the green harness masks a sharp gap between what the system **claims** and what it **enforces**, and that gap falls in two places that matter:

1. **The single-writer guarantee is a lie at the boundary it most needs to hold.** The lock that makes the shared line "single-writer" is a Python *thread* lock (`record.LINE`), not a filesystem/repo lock; and the commit path stages a **shared parent directory** with `git add -A`, which sweeps a *sibling worker's* uncommitted work into the wrong commit. One seat confirmed this experimentally in a throwaway repo: worker A's fold commits worker B's in-flight `intent.md`. This is the engine's distinctive promise, and it is the engine's worst bug. (Severity weighted up because it silently corrupts the shared graph line — the highest blast radius in the system.)

2. **The system's signature disciplines are largely unenforced — and will regenerate badly.** Because the code is disposable and the spec/ADRs/checks are durable, a weakness only matters if the durable layer re-imposes its fix on the next rebuild. The durable layer re-imposes its *deterministic skeleton* in full and almost none of its *judgments*. Mutation-proven: the red→green feedback loop is **never executed** (a fabricated loop folds clean; a loop field that *says it never ran* folds clean); the coherence gate is **never driven to "incoherent"** (deleting it leaves the harness green); "depth," the system's central criterion, has **no gate but line count** (a 399-line shallow god-module passes everything). The harness verifies that nodes move through the right states; it does not verify that the model-side judgments those states represent actually happened.

The headline: **the green `--check` certifies the sequential, structural contract and is blind to every concurrency, atomicity, and model-judgment failure in this report.** The engine fails *safe* in most contention cases (it refuses and surfaces a decision rather than corrupting), but it fails *late* and, in the C1 case, it fails *silent*. The few things that actually matter, in priority order: fix the single-writer reality (P0), execute the loop (P0), put a real floor under "depth" or stop claiming it is gated (P0), and tear down + recover the failure paths the system is *designed to produce* (P1).

This report's deepest cross-cutting finding: **hypercore has successfully mechanized exactly the disciplines that were already mechanizable, and rebranded the un-mechanized ones — the loop, depth-the-criterion, coherence, the grilling floor, design-it-twice — as "folding conditions" while leaving them as advice a regenerating model can satisfy with a plausible-looking artifact.** The weaknesses most likely to survive a teardown are precisely the ones the system is proudest of.

---

## Part A — The code as it stands: severity-ordered findings register

Ranked by real blast radius: graph/line corruption and lost operator work first; resource leaks and robustness next; cosmetic last. Each entry merges the seats that raised it (de-duplicated), with `file:line`, mechanism, consequence, fix, and — where it exists — the experimental confirmation. Verified loci are marked **[verified]** where the synthesis lead read the cited lines.

### CRITICAL

---

**C1 — The "single-writer" line is a thread lock, and the commit path sweeps siblings' uncommitted work** **[verified; experimentally confirmed]**
`record.py:34` (`LINE = threading.RLock()`), `record.py:51-57` (unlocked `atomic_write`), `record.py:60-68` (`commit` → `git add -A *paths`), `graph.py:173,251,265` (commit pathspecs name the shared `work/` parent), docstring claim falsified at `record.py:11-12`.

*Mechanism — two compounding faults:*
- (a) **Wrong lock.** `LINE` is a `threading.RLock`. It serializes threads inside *one* engine process. Nothing stops a second `python3 -m engine`, a stray `git` in the repo, or the operator's own editor committing from racing the index. The "multiple workers advance one graph" promise holds *only* under an unstated single-process assumption, enforced nowhere (no lockfile, no flock, no `index.lock` reliance).
- (b) **Wrong scope.** `commit` runs `git add -A` over whatever pathspec it is handed, and the hot paths hand it a **shared parent directory**: `graph._fold` commits `[parent_dir, dest_base]` where `parent_dir` is `.../work` (`graph.py:265`); `graph.cut` commits `[os.path.dirname(node.path)]`, also `.../work` (`graph.py:173`); `graph._persist` commits `[node.path]` (`graph.py:251`). `git add -A <dir>` stages the **entire subtree** under that dir — every new, modified, and deleted file (confirmed against git docs). Meanwhile `atomic_write` runs *outside* `LINE` (only `commit` is `@serialized`), so a sibling worker's just-landed-but-uncommitted `intent.md` — or even a live `mkstemp` temp file — is globally visible in the working tree the instant A's `git add -A work` runs.

*Consequence:* worker B's in-flight change (or a half-written temp) lands inside **worker A's** commit, misattributed; B's later `commit` then no-ops or re-commits a now-different tree. **Lost or misattributed update on the shared graph line — silent.** The docstring's safety claim (`record.py:11-12`, "`-A` is scoped to the given paths, so concurrent commits to different paths never sweep each other's work into one commit") is false as implemented.

*Experimental confirmation (R2, throwaway `/tmp` repo):* with A folding `nodeA` while B had `atomic_write`-landed an uncommitted change to `nodeB`, `git add -A work work/archive` staged **both** — B's change went into A's commit. A second probe confirmed a live `mkstemp` temp from a concurrent `atomic_write` is also staged.

*Fix (two parts, both needed):*
1. Stage **exactly the act's files**: `git add -A -- <file1> <file2>`, never a shared parent dir.
2. Hold `LINE` across `atomic_write` + `commit` so no foreign temp/half-state is visible to a concurrent `add`. And — to match the marketing — replace (or back) the thread lock with a **repo-level advisory `flock`** around `serialized`, so a second process or stray git cannot race the index.

*Why ranked #1:* it is the only finding that silently corrupts the shared source of truth, and it directly falsifies the system's distinctive claim. Cheap fix, largest correctness gap. (R2 critical C1; R1 §4.2.1; R4 §3.1.)

---

**C2 — Failure paths strand the node `IN_FLIGHT` forever and leak the worktree/branch** **[verified]**
`worker.py:197-207` (`run` tears down only on `reply.done`), `conversation.py:104-122` (`integrate` returns not-done on every refused path), `schedule.py:116-122` (`_fail` raises a card but never tears down, never moves the node off `IN_FLIGHT`).

*Mechanism:* `teardown(node)` is gated behind `if reply.done:` (`worker.py:205-206`). But `integrate` returns `done=False` on **every expected refusal**: a delta that won't apply, a missing loop, a depth decision, or a judged-incoherent result (`conversation.py:106-109, 115-119`). On any of these, `graph.integrated` is never called, so the node never leaves `IN_FLIGHT`; and `work/worktrees/<id>` + branch `worker/<id>` persist. The node is not in `ready()` (requires `STANDING`), not a card on its own behalf, and nothing scans for stranded `IN_FLIGHT`. The `_fail` path (`schedule.py:116`) raises a recovery card parented to the node but likewise never tears down and never re-states the node.

*Consequence:* abandoned worktrees and branches accumulate **per failed build** — and the failures are precisely the cases the system is *designed* to produce (decisions returned to the operator). Over a long session, the disk and branch namespace fill. On a process restart, an `IN_FLIGHT`-on-disk node with no live thread and no card is silently dropped — contradicting "never silently dropping the node" (`schedule.py:26-27`).

*Fix:* tear the fence down in a `finally` regardless of `reply.done`; on a refusal, move the node to a recoverable state (or make the raised card the node's re-entry so the operator can resume/abandon). On scheduler start, scan for `IN_FLIGHT` nodes with no live worker and re-queue or raise a recovery card.

*Why critical, not high:* this is the failure mode the architecture *normally* takes (operator decisions are the steady state), so the leak is not an edge case — it is the common path. (R2 critical C2 + high H5; R1 §4.2.3; R4 §3.4.)

---

**C3 — Slug reservation is a TOCTOU; concurrent node creation overwrites a sibling node (can lose a machine decision card)** **[verified]**
`graph.py:207-214` (`_slug` reads `taken` then loops), `graph.py:246-251` (`_persist` → `atomic_write` then `commit`, only `commit` serialized).

*Mechanism:* `_slug` computes `taken = {n.id for n in read_graph()}`, picks a free slug, and `_new`→`_persist` writes the folder — **all outside `LINE`**. Two concurrent creations with similar text compute the **same** slug and both `_persist` to the same folder; the second `atomic_write` overwrites the first. Concrete trigger: two failing workers both call `schedule._fail → graph.raise_card` from their own threads.

*Consequence:* a **machine-owned decision card is silently lost** — the recovery the operator was supposed to settle vanishes. This is also the un-handled tail of the "a failing worker returns as a decision, never a silent drop" promise: if `_fail`'s own `raise_card` collides, the node strands `IN_FLIGHT` with no backstop.

*Fix:* make slug-reserve→persist atomic under `LINE` (the lock already exists), or reserve the folder with `os.makedirs(exist_ok=False)` and bump on `FileExistsError`.

(R2 critical C3; R1 §4.2 family.)

### HIGH

---

**H1 — The fold is non-atomic in two ways: a half-folded spec on crash, and "spec-merged-but-node-unarchived" wedges operator work permanently** **[verified]**
`delta.py:117-143` (multi-file `atomic_write` loop, then `channels.materialize`, then one `commit`), `conversation.py:120-121` (`delta.fold` and `graph.integrated` are two separate acts).

*Mechanism:* `fold` is `@graph.serialized`, so it cannot interleave with a sibling fold — good. But internally it loops `atomic_write` over each touched capability (`delta.py:132-136`), then calls `channels.materialize`, then a single `commit` (`delta.py:141-143`). A crash or exception mid-loop leaves the spec **half-applied on disk, uncommitted** (cap A new, cap B old); the next `read_spec` sees inconsistent state. Separately, `conversation.integrate` calls `delta.fold` (`:120`) and *then* `graph.integrated` (`:121`) as two acts: if the process dies between them, the **delta is merged into the spec but the node is never archived** → it stays `IN_FLIGHT`, and a retry hits `delta.check`'s "ADDED requirement already exists" (`delta.py:108-109`) and can **never integrate**. The operator's work is wedged with its change already in the spec.

*Consequence:* graph/spec divergence on crash (low-frequency but high-cost), and a permanent wedge on the merged-but-unarchived window. The docstrings promise "archive ⟺ fold, one act" (`delta.py:6-9`, `conversation.py:120`); the code does not deliver it.

*Fix:* render all channels into memory first; write + commit the spec changes **and** move the node folder in one serialized git transaction so "spec merged ⟺ node archived" is atomic.

(R2 high H1; R1 §4.2; R4 §3.5 idempotency corollary.)

---

**H2 — A leaked/reused worktree is silently reused at a stale base** **[verified]**
`worker.py:147-159` (`worktree` returns early if the dir exists).

*Mechanism:* `if os.path.isdir(path): return path` (`worker.py:155-156`) — so a retried node id whose tree dir already exists (e.g. after a C2 leak or a slug re-use) **skips `git worktree add`** and builds in an old tree pinned to a stale `HEAD`.

*Consequence:* the worker never sees the current line; the depth diff (`conditions._touched_py` over `HEAD~1..HEAD`, `conditions.py:136`) and the delta verification run against stale reality. Compounds C2.

*Fix:* verify a found dir is a live worktree at the expected branch/base; else tear it down and re-create.

(R2 high H2; R4 §3.4.)

---

**H3 — Malformed model output degrades to a silent empty object, and a no-op delta folds as if the worker succeeded** **[verified]**
`transport.py:37-49` (`parse` falls back to `{"say": raw, "done": True}`), consumed by `worker.apply` (`worker.py:188-194`) and gated by `conditions.unmet`.

*Mechanism:* `parse` returns `{"say": raw, "done": True}` on any reply with no JSON object (`transport.py:49`). A worker whose model returns prose/truncated/non-object then yields empty `report`/`delta`/`loop` (`worker.py:189-191`). `conditions._feedback_loop` skips the loop check for a *trivial* delta (`conditions.py:82`), and an empty delta parses to `trivial` (`delta.py:60-61`), so `unmet` *passes* a no-op delta **with no loop required**. A model failure folds a no-op as a success, indistinguishable from a real minimal result.

*Consequence:* the model-seam robustness gap is invisible because the failure raises nothing. A timeout (empty stdout, `transport.py:34` returns `r.stdout` with no returncode check) becomes a silent `done:True`.

*Fix:* distinguish "no JSON object" (an error/retry) from a real object missing optional keys; reject a worker result whose `parse` hit the fallback rather than treating absent `delta`/`loop` as "trivial, fold it." Guard `call` on returncode and empty output.

(R2 high H3; R4 §3.3.)

---

**H4 — `commit` swallows all exceptions, so a systematic git failure degrades durability silently** **[verified]**
`record.py:67-68` (`except Exception: pass`).

*Mechanism:* the swallow is intended for the benign "act already on disk, a failed commit loses nothing." But it also hides **systematic** failure: index-lock contention, a detached/conflicted worktree, disk full — every `_persist`/`fold`/`materialize` then silently stops reaching git with **zero signal**.

*Consequence:* the graph (on disk, authoritative) and the git record drift apart unobserved. For a system whose discipline is "location is authoritative, the record follows behind," this is the one place the two truths diverge with no observer.

*Fix:* narrow the except to the benign "nothing to commit"/transient cases; at minimum increment a counter or log so a persistent commit failure is detectable.

(R2 high H4; R1 §4.2.2.)

---

**H5 — `channels.materialize` is not transactional and a missing slice aborts the fold mid-way**
`channels.py:33-37` → `methodology.py:108` (`_read_slice` opens with no `isfile` guard), inside `delta.fold` (`delta.py:141`).

*Mechanism:* a registered methodology whose `spec/<cap>.md` is absent in both root and repo raises `FileNotFoundError` inside `materialize` — *after* `fold` has already `atomic_write`-applied the touched capability files (`delta.py:132-136`) and before the single `commit`. The spec is mutated on disk but uncommitted; the fold neither completes nor cleanly aborts. Ties C1/H1.

*Fix:* guard the fallback read with `os.path.isfile`; render all channels into memory and commit only if all succeed (true all-or-nothing — folds into H1's fix).

(R2 high H6.)

### MEDIUM

---

**M1 — Operator mutations run against stale `Node` snapshots while the scheduler moves the same folder**
`window.py:135-145`. The input loop snapshots `nodes = graph.read_graph()` per pass; an operator `cut` (`shutil.rmtree(node.path)`) or `approve→_fold` (`shutil.move(node.path,…)`) can act on a path a worker just moved → `FileNotFoundError` or acting on the wrong folder. `_fold` guards re-folds (`if node.folded`, `graph.py:257`) but `cut`/`approve` don't re-validate. *Fix:* re-`find(node.id)` and re-check state under `LINE` immediately before the mutation. (R2 M1.)

**M2 — The design-it-twice contest leaks every prior candidate's fence on failure, and ADR numbering is a read-number→write race**
`design.py:127-130,158-176,234`. A raise on candidate K never reaches the teardown loop, orphaning `work/worktrees/<id>-<tag>` + branches that then block a re-run; and two concurrent `design_twice` runs computing the same `_next_adr` overwrite each other's ADR (number read + write + commit not under `LINE`) — **a recorded decision lost**. *Fix:* teardown in `finally`; atomic ADR reserve+write+commit under `LINE`. (R2 M2.)

**M3 — `grill.py` accessor cluster: a pass-through-of-a-pass-through and 5× disk re-reads per paint** **[verified]**
`grill.py:143-177`. Eight near-identical accessors over the loaded `_Pass`; `contract_of` (`grill.py:175-176`) does nothing but `return contract(node)` — the **#1 red flag the doctrine names explicitly** ("a method that only forwards its arguments," `spec/depth.md`), shipped in the engine that preaches it. Each accessor re-runs `_load` (a full `grilling.md` read+parse); a single card render calls four of them. The *shape* of `_Pass` is restated once per field across the public surface — a mild information leak. *Fix:* expose the loaded pass (or a small read-only view) once; let `render`/`window` read fields off it, collapsing eight functions and the repeated disk parse into one. (R1 §2.2.)

**M4 — `review.py` is a god-file-in-the-making by concern (three jobs under the length radar)** **[verified]**
`review.py` (316 lines) does measurement/backlog (`review`,`_finding`,`_module`), the mechanical AST red-flag scan (`red_flags`,`_dead_symbols`,`_import_cycles`,…), and operator-view presentation (`bars`,`backlog`) which leaks into `view.operator_view` (`view.py:50-51`). The module whose *job* is to spot god-files is the clearest one forming, and its own length-only scan cannot see it. *Fix:* split the AST scanner into its own `scan.py`; keep `review.py` as backlog; move rendering toward `view`. A design-it-twice candidate. (R1 §3.1.)

**M5 — `conditions.unmet` flattens a fact and a judgment into one stringly-typed channel** **[verified]**
`conditions.py:63-70`. Returns `str | None` for three conditions, two facts (delta applies, loop recorded → hard refuse) and one judgment (depth → operator decision). The caller `conversation.integrate` (`conversation.py:106-109`) can't tell which it got, so it raises the same card for "your delta is malformed" (a worker bug to retry) and "this file is long, please decide" (genuine operator work). A special/general mixture. *Fix:* return a typed result (`Refusal(reason)` vs `Decision(text)`). (R1 §3.3.)

**M6 — Information leakage: `graph._persist`/`graph._subject` reached across the seam** **[verified]**
`grill._save` calls `graph._persist(...)` and must pre-flip `held.state = graph.AWAITING` (`grill.py:194-195`); `schedule._fail` and `design.record` also reach `graph._subject`. The knowledge of *how a node is persisted* (front-matter, atomic write, commit convention) now lives in `graph` **and** is invoked from `grill` — two modules that must change together. The same `transport` extraction that fixed the `conversation/grill` leak left this one. *Fix:* a `graph`-owned `persist_node(node, message)` public method. (R1 §3.2.)

### LOW

- **L1 — Delta heading parse is separator-fragile.** `delta.py:81` — `head.partition("—")` only when an em-dash is present, else partition on space; a model writing `## ADDED - capability` (ASCII hyphen) yields capability `- capability` → spurious `CannotFold`. *Fix:* normalize separators before matching. (R2 L1.)
- **L2 — `grilling.md` corruption breaks every predicate for a card.** `grill.py:222` — `int(line.split(":",1)[1].strip() or 0)` on `surfaced:` raises `ValueError` out of `_load`, making the card unreadable in the queue. *Fix:* guard with try/except → default 0. (R2 L2.)
- **L3 — Per-file reads not OS-error isolated; `preview` leaks a temp dir per `--frame`.** `review.py:208-210`, `preview.py:16`. A file deleted between walk and read aborts the whole review; preview temp dirs accumulate. *Fix:* guard `_read`; `atexit`/`finally` cleanup. (R2 L3.)
- **L4 — Bare `open().read()` without `with`/`encoding=` across read paths.** `spec.py:71,75`, `worker.py:228,235`, `graph.py:218`, `view.py`, etc. A non-UTF-8 locale + the box-drawing glyphs this codebase writes can `UnicodeDecodeError` the entire spec read (no per-file isolation), and leaked handles accumulate on the keystroke-driven re-render. *Fix:* `with open(..., encoding="utf-8", errors="ignore")` and per-file try/except. (R2 M4.)
- **L5 — Duplicated loop schema key-set.** `conditions.py:85` and `worker.py:254` each independently name `("command","red","green")` — the literal information leak the doctrine warns of, caught by a single shared `Loop` dataclass. (R1 §3.5.)

### Adjudication notes (where the seats differed)

- **C1 severity.** R2 ranked it critical with an experiment; R1 named it "the single biggest architectural fragility" but framed it as a *risk* (process boundary). I rank it **#1 overall** — the experiment beats the assertion, and the in-process variant (two workers' uncommitted state visible to one `add -A work`) is reachable *within a single process* via the `atomic_write`-outside-the-lock window, so it is not only a multi-process hazard. Both the wrong-lock and the wrong-scope faults are real and compose.
- **C2 vs "resource leak."** R1 framed the worktree leak as operational robustness (its §4.2.3); R2 ranked it critical because it strands the node and the failure path is the *normal* path. I side with R2: this is the steady-state failure mode, not an edge.
- **Depth/`grill`/`review` findings** (M3–M6) are real but lower blast radius than the concurrency family; R1 is right that they are the on-the-nose *dogfooding* misses, and they belong in Part B's verdict even though they sit mid-register here.

---

## Part B — Architecture & depth dogfooding

### B.1 The seam map (verified clean DAG)

The module dependency graph (module-level sibling imports only) is a **clean DAG with no import cycles** — confirmed by running the engine's own `review.red_flags()` (zero cycles, zero dead symbols) and by reading the imports directly:

```
L0  record (threading+git, leaf)        transport (subprocess+json, leaf)
L1  graph -> record                     spec -> graph
L2  delta -> graph,spec,channels        conditions -> delta,spec
    review -> conditions,graph          channels -> anchor,methodology
L3  grill -> graph,spec,transport       conversation -> conditions,delta,graph,grill,transport
    worker -> conversation,delta,graph,grill,spec,transport     design -> graph,grill,spec,worker,transport
L4  schedule -> graph,worker,transport  view -> graph,review,spec   render -> grill,graph,conversation
    window -> conversation,graph,grill,render,schedule,transport,view
```

The historically-cited defects this codebase grew out of — a `conversation <-> grill` cycle and five modules reaching into `conversation._claude`/`conversation._parse` — were **genuinely dissolved** by extracting `transport` (ADR 0021): the shared knowledge (the `claude -p` call + lenient JSON read) was pulled *downward* into a leaf everything rests on. Textbook Parnas. Credit where due.

### B.2 The deep-vs-shallow verdict

**Genuinely deep (the honor roll):** `record` (durable write + single-writer line behind three functions), `transport` (the model call + lenient parse, two functions), `channels`/`anchor`/`methodology` (the entire "which artifacts exist + how each renders" registry behind `materialize(root)`), `delta.fold`, `schedule.Scheduler`, `design`. Each hides far more than it exposes. **The engine can build deep, and for the bulk of its mass, does.**

**Named offenders (the dogfooding misses), in the system's own vocabulary:**
1. **`grill.contract_of` (`grill.py:175-176`)** — a pass-through-of-a-pass-through, the doctrine's *literal* #1 red flag, plus eight accessors that each re-parse `grilling.md`. (See M3.)
2. **`graph._persist` reached from `grill._save` (`grill.py:194-195`)** — information leakage, the gravest red flag after shallowness, through *call* edges (so the mechanical import-cycle scan cannot see it). (See M6.)
3. **`review.py` itself** — three-job weak cohesion under the 400-line radar; the god-file-spotter is the god-file forming. (See M4.)
4. **`conditions.unmet`** — special/general fact-vs-judgment mixture. (See M5.)
5. **The `conditions`/`worker` loop-key duplication** — the literal information leak. (See L5.)

### B.3 The self-review's blind spots

I ran the engine's own architecture review against the live tree: **it reports a perfectly clean bill of health** — every module under the signal, zero dead symbols, zero import cycles, "no deepening opportunities." A real review (this one) found, on that same tree, all five offenders above. **The self-scan is structurally blind to every one.**

This is not dishonesty — the module scrupulously records the model-driven verdict as `DEPTH_NOT_YET` ("not yet built," `review.py:94-96`) rather than faking it, which is admirable and rare. But the architectural consequence must be stated plainly:

> **The engine's self-assessment measures the one dimension its own doctrine says is *not* the criterion (length), plus the two mechanical flags a tool can read (dead code, 2-cycles), and is structurally incapable of seeing the named red flags — shallow module, pass-through, information leakage, special/general mixture — that the doctrine calls the *actual* criterion.** A length-clean tree is presented to the operator as a deep tree, and the gap between those is exactly the gap this report fills.

Two further mechanical limits, verified: `_dead_symbols` counts a name "used" if it appears as **any attribute access anywhere** (`review.py:257-258`, `node.attr`), a known false-negative class; and `_import_cycles` is explicitly a **2-cycle-only** detector (`review.py:267`, "a longer ring is the model-driven scan's still-unbuilt job"), so a 3+ module ring passes.

### B.4 The concurrency architecture, judged

This is the best-designed part of the system, and the seam placement is **correct**: workers build in isolated worktrees (sharing one object store, independent working trees and HEADs), their slow model calls run unlocked, and every git-touching act runs under one lock — *the index is the shared mutable resource, not the worktrees.* The fold is serialized on the same line; the scheduler guards its own thread dict with a *separate* lock and is explicit it is not the record lock (`schedule.py:56`). The separation of "what guards my bookkeeping" from "what guards the shared record" is exactly right.

Its weaknesses are all at the **edges**, not the core insight: the process boundary (C1's wrong lock), the commit scope (C1's wrong pathspec), failure cleanup (C2), contention. Two workers briefed on overlapping spec regions fail *safe* (the second fold's `delta.check` refuses → a decision) but *late* (after both expensive builds) — there is no admission control on overlapping deltas at dispatch. And `graph.ready` re-walks the whole `work/` tree per `step` at 5Hz: free at hypercore's scale, a scaling cliff with no incremental story. The core insight — serialize the index, not the builds — is right; the implementation does not yet deliver it across the process boundary or at commit granularity.

---

## Part C — Methodological prevention: stopping the regeneration

hypercore's defining commitment is that **the code is disposable and the spec/ADRs/checks are durable** ("inherited debt is not carried… torn down and rebuilt, not patched," `intent.md:18`). This is, almost verbatim, spec-driven development: the regenerated system is exactly as good as what the durable layer can re-impose. **Everything the durable layer leaves to chance re-enters on every rebuild.**

### C.1 The regeneration loop

On a teardown, four artifact classes survive: `intent.md` (the vision), `glossary.md` (the language), `spec/*.md` (the living spec), `spec/decisions/*.md` (22 ADRs) — plus the acceptance harness `engine/check/sliceN.py` and the *derived* agent grounding (`AGENTS.md`, `skills/`). A slice becomes code via: grilling → scheduler dispatch → fenced worker grounded in the whole spec → folding conditions → architect coherence check → `delta.fold` (applies the delta and re-derives the channels in one act) → the standing acceptance floor.

**What the methodology guarantees vs. leaves to chance** (verified against the gates):

| Property of the regenerated code | Guaranteed by a mechanical gate? | Where |
|---|---|---|
| Spec and graph never drift | **Yes** | `delta.fold` / `delta.check` |
| Grounding channels match the spec | **Yes** | `channels.materialize` on fold |
| Workers are isolated | **Yes** | `worker.worktree` + `graph.serialized` |
| The length ratchet (bounded acceptance) | **Yes** | `conditions.accepted` / `accepted_at` |
| The mechanical red-flag scan (dead code, 2-cycles) | **Yes** | `review.red_flags` |
| A behavior change records *something* called a loop | **Shape only** | `_feedback_loop` checks 3 non-empty strings |
| The recorded loop was *actually run* | **No** | nothing executes the loop command |
| Modules are *deep* (the actual criterion) | **No** | model verdict "not yet built" |
| The coherence judgment happened | **No** | `integrate` trusts the model verdict |
| The grilling floor found the right stakes | **No** | model returns the question list |
| design-it-twice candidates genuinely differ / deepest picked | **No** | `design.select` unpacks model JSON, defaults to candidate 0 |

The pattern is exact: **everything deterministic is guaranteed; everything that is a judgment is left to the regenerating model and never re-checked.** Weaknesses re-enter through every "No."

### C.2 The enforced-vs-advice audit

The repo's mantra is stated four times: *"Advice can be ignored; a folding condition cannot."* Taking it at its word and testing whether each discipline is wired to a gate the build genuinely cannot pass without the discipline *having happened*:

| Discipline | Claimed | Enforced by a real gate? | The gap |
|---|---|---|---|
| Delta applies to current spec | fact | **YES — gold standard.** `delta.check` parses + validates against live spec | None |
| **red->green feedback loop** | fact ("a correct narrative with no harness is the failure this kills") | **NO — advice in fact's clothing.** `conditions._feedback_loop:84-88` checks 3 non-empty strings; the command is never run | A worker fabricating `{"command":"run","red":"failed","green":"passed"}` folds. The exact failure the docstring names **passes** |
| depth — length signal | judgment surfaced as decision | **YES for length only** (`_depth:92-110`, real diff, real records) | Length != depth (the system says so). A 399-line shallow god-module is silent |
| the model-driven shallow/leakage **verdict** | "the assessment this review is meant to grow… not yet built" | **NO — explicitly absent** | This is the *primary positive criterion of the entire system* and nothing enforces it |
| mechanical red-flag scan (dead, 2-cycle) | "bites by construction" | **YES — real and honest** (`red_flags:215`, slice15) | Narrow by design; honest about it |
| build deep up front (proactive defense) | "no path runs a worker without it" | **NO.** Foregrounded in the *prompt* (`worker.py:130`); slice7 asserts the *words* appear | "Grounded in depth" is verified as *these words appear in a string*, not that anything deep was built |
| coherence at the archive gate | "the defense against self-judging" | **NO.** `integrate` asks the model `{"coherent":...}` and trusts it; every check hands back scripted `true` | A rebuild could rubber-stamp or omit the check and pass every acceptance check |
| grilling floor | the decisions floor | **NO.** The model returns `questions:[…]` vs `[]`; the check feeds both pre-baked | A floor that asks about everything, or nothing, passes |
| design-it-twice (pick deepest) | the judgment use of the fence | **NO** for the judgment (YES for the fences). `design.select` defaults to `candidates[0]` — the degenerate selector is the literal default | "Picks the deepest" is asserted as `cands[0].brief == "minimal"` |
| the length ratchet | bounded acceptance | **YES — real, well-tested** (slice9, 19 assertions) | A model of how to turn a discipline into a gate |

**Verdict on the repo's own claim:** "Advice can be ignored, a folding condition cannot" is **true for the three deterministic conditions** (delta-applies, the ratchet, the mechanical scan) and **false for everything that requires judgment** — the loop, depth-the-criterion, coherence, the floor, design-it-twice. The system has mechanized the disciplines that were *already mechanizable* and **rebranded the un-mechanized ones as conditions** while leaving them as advice. The loop is the sharpest case: dressed in the language of a non-negotiable fact ("there is nothing to judge," `conditions.py:8-9`) while being, mechanically, a non-emptiness check on three strings the model wrote itself.

### C.3 The seam where weaknesses re-enter: the scripted transport

The live system reaches the model through one call (`transport.call` → `claude -p`). The harness replaces it with a queue-popping fake that hands back pre-baked JSON (`harness.scripted`). This is the **right call for the deterministic parts** — you don't want an LLM in a fast acceptance run, and the graph/fold/worktree logic is fully exercised without one. But it is fatal for the regeneration contract: **for every behavior that lives only in the model, the scripted transport does not *drive* the behavior, it *replaces* it, and the check then asserts on the harness's own pre-baked answer.** This is the textbook test-oracle problem resolved the wrong way — *the oracle supplies the answer it then checks*. The check passes by construction; it tests nothing about the judgment. Goodhart's law applies directly: the check is the measure, and a regenerating agent satisfies the measure (non-empty strings, `coherent:true`) without the target.

### C.4 The largest single regeneration gap: the deferred depth verdict

The whole architecture is *named* "depth." The positive criterion — a lot of behavior behind a small interface — is the thing every other discipline serves. And **the only mechanical proxy for it in the entire durable layer is line count.** On a teardown the regenerator is told *length is not the criterion; depth is* (~6x in `depth.md`), given **no check that distinguishes a deep module from a shallow one**, and gated only at 400 lines. The predictable failure: the next rebuild produces modules that are **short and shallow** — passing the length gate, the mechanical scan, and every acceptance check, while violating the system's central criterion. The prior epoch's 6,348-line god-file is the failure length catches; *its negative image — over-decomposed shallow modules, the "classitis" the glossary itself names* — is invisible to the durable layer. The methodology has a name for this enemy and no gate against it. It advertises depth as enforced while the only enforcement is a context-cost proxy the spec explicitly says is not depth.

### C.5 How to stop each weakness CLASS from regenerating

The fix is not more prose — it is to point the system's *own best mechanism* (derive/observe, don't hand-tend; gate by construction, never by a reviewer remembering) at the judgments themselves:

1. **Fabricated/never-run loops ->** the loop condition must **execute** the recorded command in the worker's fence and confirm a real red->green transition (fail at `HEAD~1`, pass at `HEAD`), not check three strings. Where a command genuinely can't be auto-run, the gate must *say so as a decision*, never silently pass on string-presence.
2. **Short-and-shallow modules ->** ship a mechanical **shallowness proxy** (an interface-to-implementation ratio — public-symbol/signature surface vs. body size, readable off the AST — surfaced as a *signal that raises a decision*, exactly the length pattern, scoped to low-false-positive rules per ADR 0020's own discipline) **or** stop describing depth as enforced. Truth-in-advertising is itself prevention: a regenerator told the truth won't assume a gate exists.
3. **Rubber-stamp coherence / no-judgment floor / pick-0 contest ->** a **judgment-harness tier**: run each judgment once against the **live** transport on a fixed fixture and check the verdict in as a golden transcript, *and* assert against an **injected-bad** case (a deliberately incoherent result must raise a decision; an above-floor ask must produce questions). slice16 already does this for the *failure* path (the injected `RuntimeError` at `slice16.py:63-64,133`); extend the pattern to coherence, the floor, and selection.
4. **Spelling-coupled checks ->** forbid asserting on rendered prose substrings except where the substring is a structured, parsed token (like `accepted@<N>`); assert system state, never wording. (The harness violates its own "the exception is the decision, not the spelling" principle in slice7:64-68,120 and slice8:104.)
5. **The meta-weakness (the next author scripts the judgment and calls it tested) ->** the keystone. Add an explicit methodology principle: **a scripted transport is licensed only for behavior the engine computes deterministically; for any model-side behavior the check must drive the live model against an adversarial fixture or be honestly recorded as "watched, not gated."** Carry a machine-readable "what the harness gates vs. watches" register in `spec/` so a regenerator cannot mistake advice for a gate. Generalize `architecture-review.md`'s "not yet built, never fabricated" honesty from the depth verdict to *every* model-side judgment.

---

## Part D — Testing & verification rigor: theater vs. substance

### D.1 What the harness genuinely proves (substance)

A scripted transport over real infrastructure is the *classicist* test style and is fine when assertions verify the **system's** state and only mock the LLM's *content*. The harness does this well for **structural, deterministic, file-and-graph facts**, and mutations to that machinery were **killed**:

- **slice9** (ratchet arithmetic) — strongest pure-logic slice, 19 assertions with rich negatives.
- **slice2/4** — real fold round-trips, real `CannotFold` negatives, and the information-flow test that a raw worker report (a planted SENTINEL) reaches **no** card/render/node (a genuine leak-containment test).
- **slices 10–13** — the planted-sentinel idiom genuinely proves *derivation*: plant a slice, fold, assert the sentinel appears in the materialized artifact.
- **slice6/15** — real AST scans over planted god-file and dead-symbol/cycle fixtures, both polarities.
- **slice16 §4** — a **real injected mid-build exception** exercising the `_fail`->decision path (`slice16.py:133`). The one place a failure is real, not scripted.

A rebuild reproducing these reproduces the deterministic skeleton faithfully.

### D.2 The theater (mutation-proven)

The harness's three flagship methodological claims cross the line where a check asserts "the system does X" but X was *authored into the script*:

- **The red->green loop is a presence-of-strings check (the central finding).** `_feedback_loop` checks only that `command`/`red`/`green` are non-empty (`conditions.py:84-88`); the command is never run; no code anywhere relates red to green. **Mutation Experiment 2 (R4):** calling the gate directly with fabricated loops — `{red:"PASSED",green:"PASSED"}`, `{red:"green",green:"red"}`, `{red:".",green:"."}`, and **`{red:"i did not run this",green:"nor this"}`** — **all FOLD.** A worker that *says in the loop field that it never ran the loop* passes the most-emphasized folding condition.
- **The coherence gate's incoherent branch is never exercised.** No check in the harness drives `coherent:false`; every check feeds `coherent:true` (e.g. `slice16.py:52`). **Mutation Experiment 3/6 (R4):** replacing the gate with `if False:` (always coherent) left the harness **fully GREEN — the mutant survived.** The coherence gate could be entirely removed and `--check` would not notice.
- **The single-writer lock is unverified by any concurrency test.** slice16's two workers are *choreographed* (held on a `threading.Event`, then released) and fold **different** capabilities — there is no test of two folds racing the **same** spec file, no `index.lock` contention, no assertion that `LINE` is held. **Mutation Experiment 10 (R4):** making `serialized` a no-op went RED 5/5 — *but for the wrong reason*: only slice15's **dead-symbol lint** fired (`record.LINE` now unreferenced). **No concurrency assertion failed.** The lock could be removed and the only thing that notices is a lint rule about an unused variable.

The grilling-floor (slice3) and the carve (slice14) are honest *plumbing* tests, not capability tests: slice3 proves routing given a questions-list, never that the system *finds* the right stakes; slice14 verifies the spec *prose moved verbatim* (a string-equality test on documentation), never that the carve changed no behavior.

### D.3 Mutation results (full)

| # | Mutation | Result | Proves |
|---|---|---|---|
| 1 | `_feedback_loop -> return None` | **KILLED** | The *presence* of a loop dict is tested |
| **2** | **fabricated/"never-ran" loops** | **SURVIVED (FOLDS)** | **The loop's *truth* is not tested — central theater finding** |
| **3/6** | **coherence -> always coherent** | **SURVIVED (GREEN)** | **The incoherent->decision path is entirely unexercised** |
| 4 | `teardown -> no-op` | KILLED (slices 4,8) | Teardown-*on-success* is checked (not on failure — C2) |
| 5b | `SIGNAL = 5000` | KILLED (slice9) | Only the *relative* ratchet is pinned; the value 400 is not independently asserted |
| 7 | `_apply` drops all ops | KILLED (14 fails) | The fold->spec landing is well tested |
| **10** | **`serialized -> no-op`** | **"KILLED" wrong reason** (only the lint) | **The single-writer lock is unverified** |

The pattern is sharp: **mutations to structural file/graph/fold machinery are killed; mutations to the three flagship methodological gates survive** (or die only incidentally to an unrelated lint).

### D.4 The untested surface

| Surface | Risk | Coverage |
|---|---|---|
| graph/fold/delta, leak-containment, ratchet, red-flag scan | low–high | **High** |
| **red->green loop truth** | **high** | **None** (presence only) |
| **coherence incoherent path** | **high** | **None** (mutant survived) |
| **concurrency / single-writer lock** | **high** | **None** (choreographed; lock unverified) |
| crash / partial-write / `fsync` (`atomic_write` has none) | high | **None** |
| live transport + malformed `parse` fallback | high | **None** |
| worktree cleanup on failure | med | **None** |
| fold idempotency (a second fold of a non-trivial delta raises `CannotFold` — intended?) | med | **None / unspecified** |
| window / live loop wiring | med | **None** (manual only — a defensible boundary) |

### D.5 Fixes to make the harness a real contract

P0: make the loop a **replayable oracle** (capture the command + verdicts; re-run it in the fence, assert red at `HEAD~1` and green at `HEAD`; at minimum reject `red==green` or empty/un-runnable, and add a slice that drives Experiment 2's fabricated loops and asserts they are **gated**). P1: drive the **incoherent path** (feed `coherent:false`, assert the fold is refused, the spec untouched, the node live, a `decide` card carries the architect's words). P2: a **same-spec-file concurrency** check run with real overlap N times, asserting both folds land and the history is two clean commits — *and* a mutation-guard so removing `serialized` fails on a **fold-corruption** assertion, not a lint. P3: **fuzz `transport.parse`** and pin the dangerous empty/timeout->`done:True` fallback; add a contract test that the scripted fake and a recorded real `claude -p` reply share a shape. P4: `fsync` + crash/partial-write injection for `atomic_write`/`commit`. P7: run a real mutation pass (`mutmut`/`cosmic-ray`) in CI so "is this check theater?" becomes a continuously-measured number.

---

## Part E — Prioritized roadmap (P0–P3)

Code fixes (CF) and methodological fixes (MF) interleaved; each tied to the finding it closes. Ranked by blast radius — graph corruption and lost operator work first.

### P0 — the things that actually matter

- **CF-1 · Fix the single-writer reality (closes C1).** Stage exactly the act's files (`git add -A -- <files>`, never a shared parent dir); hold `LINE` across `atomic_write`+`commit`; back the thread lock with a repo-level advisory `flock` so a second process/stray git cannot race the index. Update the false docstring at `record.py:11-12`. *Largest correctness gap, cheapest fix.*
- **CF-2 · Tear down + recover on every path (closes C2, H2).** `teardown` in a `finally`; on a refusal move the node to a recoverable state; on scheduler start, scan for orphaned `IN_FLIGHT` and re-queue/raise. Verify a found worktree is live-at-base before reuse. *Closes the steady-state failure mode.*
- **MF-1 · Execute the red->green loop (closes the loop theater; D.5 P0).** The gate runs the recorded command in the fence and requires a real red->green transition; otherwise it raises a decision. Add the spec scenario *WHEN the command does not transition red->green THEN refuse*, and drive a real failing-then-passing command in the check.
- **MF-2 · Put a floor under "depth" or stop claiming it is gated (closes the largest regeneration gap; §C.4).** Ship an interface-to-implementation-ratio shallowness signal that *raises a decision* (low-false-positive, ADR-0020-disciplined) **or** de-claim depth-as-enforced in `depth.md`/`folding-conditions.md`/glossary. Do at least one.

### P1 — robustness and the judgment contract

- **CF-3 · Make the fold one transaction (closes H1, H5).** Render channels into memory; write+commit the spec and move the node folder in one serialized git act so "spec merged <-> node archived" is atomic. Guard `_read_slice` with `os.path.isfile`.
- **CF-4 · Reject the parse fallback as a worker error (closes H3).** Distinguish "no JSON object" from "object missing optional keys"; guard `call` on returncode/empty stdout.
- **CF-5 · Surface commit failures (closes H4).** Narrow the except; count/log persistent failures so graph/git drift is observable.
- **MF-3 · Judgment-harness tier (closes the coherence/floor/contest theater; D.5 P1/P2).** Drive each judgment once against the live transport on a golden fixture *and* assert against an injected-bad case. Drive the incoherent coherence path.
- **MF-4 · Behavioral asserts, never prose-wording.** A one-line discipline in `harness.py`: a check asserts system state, never rendered wording (fixes slice7/8 spelling-coupling).

### P2 — cohesion, leaks, and the methodological keystone

- **CF-6 · Operator mutations through the serialized path (closes M1).** Re-`find` + re-check state under `LINE` before `cut`/`approve`.
- **CF-7 · Atomic ADR numbering + contest teardown (closes M2).**
- **CF-8 · Collapse the `grill` accessor cluster (closes M3).** Expose the loaded pass once; remove `contract_of`.
- **CF-9 · Seal the `graph._persist` leak (closes M6);** share the loop schema (closes L5); type `conditions.unmet` (closes M5).
- **MF-5 · The "drive, don't replace" rule + a gated-vs-watched register (the keystone; §C.5.5).** The single most important methodological artifact: a machine-readable list in `spec/` of every model-side judgment the harness does *not* gate, so a regenerator cannot mistake advice for a gate.

### P3 — hygiene and the long pole

- **CF-10 · Split `review.py` by concern (closes M4);** OS-error-isolate per-file reads, add `encoding=`/`with` (closes L3, L4); guard the delta separator and `surfaced:` parse (closes L1, L2); `preview` temp cleanup.
- **CF-11 · `fsync` in `atomic_write`** if durability is claimed; crash/partial-write injection tests (D.5 P4).
- **MF-6 · Grow the model-driven depth verdict as a skill** (the honest long pole; ties to Part F) and run a CI mutation pass (D.5 P7).

---

## Part F — Implications for the agent-facing layer (feeds Report 1)

The agent-facing grounding (`AGENTS.md`, `skills/`) is *derived* from the spec on every fold via `channels.materialize`. That is the engine's **strongest asset** for the skills work and should be the model the whole agent layer is built on: any new agent-facing artifact joins the `CHANNELS` registry rather than being hand-authored — the by-construction no-drift guarantee (ADR 0020's natural experiment: derive-on-fold never rotted; every hand-maintained restatement did) is exactly what an AGENTS.md/skills regime needs. `anchor.py` already encodes the right field-grounded caution (an agents file is "marginal and ~20% cost"); the skills report should lean on this, not re-litigate it.

But the dogfooding gap *is* the agent-facing risk. The next regeneration will be only as good as what the worker/architect grounding encodes, so the grounding must carry these four things — each closing a finding above:

1. **The single-writer reality (closes C1).** The worker/architect grounding must encode that the shared line is made safe by *staging exact files + a process-level lock*, not by `git add -A` pathspec scoping (which the docstring wrongly claims). If a regenerated `record.py` reproduces the false docstring, it reproduces the bug. The grounding must teach the *correct* invariant — "each commit contains exactly its act's files; the lock spans write->commit; the lock is filesystem-level" — so the rebuild gets the seam right.

2. **A depth proxy, or honesty about its absence (closes MF-2 / §C.4).** The worker is grounded in `spec/depth.md` via the prompt, but nothing it produces is *audited* for depth beyond length. The skills layer is the natural home for the unbuilt model-driven red-flag review — **build "the depth verdict" as an `architecture-review` skill** that actually runs the shallow/pass-through/leakage judgment. Until it exists, the grounding must tell the worker that **depth is not gated** — "build deep up front" is the *only* defense, not a backstop it can lean on. (Today the skill descriptions promise more depth-judgment than the engine delivers; a coherence pass should align them.)

3. **Execute, don't narrate, the loop (closes MF-1).** The worker's grounding must instruct that the red->green loop will be **executed**, not narrated — the worker must hand back a *replayable* command, not three strings. This is the single most important change to the worker prompt, because the loop is the system's red->green discipline and it is currently advice.

4. **The gated-vs-watched register (closes MF-5).** The architect/worker grounding must carry the machine-readable list of which disciplines are *gated by construction* and which are *watched, not gated* (coherence, the floor, design selection, depth-the-verdict). A building agent that reads this list at teardown cannot script a judgment and call it tested — which is the meta-weakness that regenerates all of Part C.

**The convergent recommendation across all four seats and both reports: point the system's own best mechanism — derive/observe, gate by construction — at the judgments themselves. The agent-facing layer is where that grounding lives, so it is where the next regeneration becomes structurally better or stays a sieve sized to pass exactly the weaknesses this audit found.**

---

## Sources

In-repo primary (read-only, verified by the synthesis lead 2026-06-22): `engine/record.py`, `conditions.py`, `worker.py`, `graph.py`, `delta.py`, `conversation.py`, `transport.py`, `schedule.py`, `review.py`, `grill.py`, `engine/check/__init__.py`, `engine/check/slice16.py`; doctrine `spec/depth.md`, `glossary.md`, `intent.md`, the ADRs in `spec/decisions/`. Experimental confirmations (throwaway `/tmp` repos, originals untouched): the C1 lost-update sweep (R2), and mutation experiments 2/3/6/10 (R4).

External (accessed 2026-06-22):
- git `add -A` pathspec semantics (the basis of C1): [git-add documentation](https://git-scm.com/docs/git-add) — `git add -A <dir>` stages the entire subtree under the pathspec, including modifications, additions, and deletions throughout all subdirectories.
- John Ousterhout, *A Philosophy of Software Design* (deep/shallow modules, pass-through methods): [aposd landing](https://web.stanford.edu/~ouster/cgi-bin/aposd.php); summaries [softengbook](https://softengbook.org/articles/deep-modules), [Zdrazil](https://www.vladimirzdrazil.com/posts/deep-shallow-modules/).
- David Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (1972): [canonical](http://sunnyday.mit.edu/16.355/parnas-criteria.html).
- Spec-driven development as executable contract / regenerate-not-edit: [arXiv 2602.00180](https://arxiv.org/html/2602.00180v1); [InfoQ](https://www.infoq.com/articles/spec-driven-development/); [Augment Code](https://www.augmentcode.com/guides/spec-driven-development-ai-agents-explained).
- Test-oracle problem (the oracle supplies the answer it then checks): Barr, Harman et al., *The Oracle Problem in Software Testing: A Survey*, IEEE TSE 2015: [IEEE](https://ieeexplore.ieee.org/document/6963470/).
- Mutation testing (a surviving mutant = an undetected fault class): [PIT/pitest](https://pitest.org/); Jia & Harman, IEEE TSE 2011.
- Change-detector / tautological tests: [Google Testing Blog](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html).
- Limits of mocks (a mock that returns the assumed behavior encodes the assumption under test): Fowler, [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html).
- Goodhart's law / specification gaming (measure becomes target): [AI alignment, Wikipedia](https://en.wikipedia.org/wiki/AI_alignment).
- Concurrency / Heisenbugs (example-based tests exercise only the interleaving that occurs): Musuvathi et al., CHESS, OSDI 2008.
