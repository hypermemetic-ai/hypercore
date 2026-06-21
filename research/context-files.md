# Item 2 — assembling maximally skilled, specialized roles

*The investigation `next-work.md` item 2 asked for. **The goal** (operator, 2026-06-21): two roles —
**architect** and **worker** — each as **skilled, specialized, effective, and consistent** as we can
make them. We have five moving parts to assemble toward that: **repo documents, agents files, skills,
prompts**, across the **two roles**. This document fixes what each part is for, records the mechanics
that are verified on the real harnesses, and hands the next session a concrete assembly to design. It
builds nothing and settles nothing the operator owns.*

*Marks: **[omp]** / **[claude]** = verified empirically this session on that harness; **[doc]** =
vendor documentation; **[code]** = present in this repo or the parked harness; **[design]** = the
open design work for the next session.*

---

## 1. The stack — two harnesses, one open standard

hypercore's reasoning is two specialized roles, on two harnesses (`harness-parked/harness-ideas.md`
§0; sharpened by the operator):

- **Architect = Opus 4.8, via `claude -p`.** Operator-facing: design judgment, coherence, legibility.
  Reads **`CLAUDE.md`**; not `AGENTS.md`. [claude+doc]
- **Worker = GPT-5.5, via pi/OMP**, run fenced in the worktree. System-facing: builds deep, hands
  back a machine-facing result. Reads **`AGENTS.md`** natively (a superset loader — CLAUDE.md too).
  [omp+code]
- **North star: open-weight, non-proprietary** (§0). The open `AGENTS.md` standard is the durable
  centre; `CLAUDE.md` is the per-vendor edge.

## 2. The five parts, and what each is for

The point is not to pick one mechanism over another — it is to **layer all of them**, each doing what
it is best at, so a role is grounded, specialized, and consistent without one giant brittle prompt:

| Part | What it is | Lifetime | Best for |
|---|---|---|---|
| **Repo documents** | `intent.md`, rebuild-spec, the living spec, ADRs, `research/` | durable, authored/folded | the **single source of truth** every other part derives from |
| **Agents files** | `AGENTS.md` (worker) + `CLAUDE.md`→`@AGENTS.md` (architect) | always-on, per session | the role's **standing identity + disciplines** — who it is, how it works, every episode |
| **Skills** | on-demand capability/methodology packs (both harnesses have them) | loaded when relevant | **specialized expertise, routed** — pulled by the task, not always resident |
| **Prompts** | the per-node assembled context (handed delta, ask, touched spec slice, live state) | per episode | the **live, task-specific** material that only exists for this node |

The governing relationship: **repo documents are the source; agents files, skills, and prompts are
three derived delivery channels** — always-on, on-demand, and per-node respectively. Nothing is
hand-copied between them (that is the `worker.DEPTH` smell — a compressed copy of `research/aposd.md`
frozen in a Python constant [code]); each channel renders from the one source.

The earlier draft mis-cast this as a turf war ("keep routing in prompts; resist files and skills").
It is not. **Skills *are* the routing mechanism** — on-demand, per-capability loading is exactly
what hypercore's per-capability self-model wants, done by the harness instead of marshalled into one
megaprompt. **Agents files *are* where role identity belongs** — always-on grounding is what makes a
role specialized and consistent. The megaprompt that `worker.prompt()` assembles today is the thing
this *replaces*, split across the channel that fits each piece.

## 3. The two roles, specialized — the target layering [design]

What each role is assembled from, every piece single-sourced from repo documents:

- **Worker (GPT-5.5 / OMP), fenced.**
  - *Agents file* (`AGENTS.md` at the fence root): the worker's standing identity — system-facing,
    fenced, the deep-module disciplines, the worker contract, the red→green-loop discipline. Always
    on, so the worker *is* a deep-building specialist before it reads a single task.
  - *Skills*: the methodology and per-capability expertise it pulls for the node it is on — the depth
    framework in depth, the touched capability's self-model, design patterns for that capability.
  - *Prompt*: the handed delta, the ask, the touched spec slice, the live state of this node.
- **Architect (Opus 4.8 / Claude).**
  - *Agents file* (`CLAUDE.md` → `@AGENTS.md`, or its own): the architect's standing identity —
    operator-facing, design judgment, legibility, the coherence stance, the standing-guard floor.
  - *Skills*: design-it-twice, the architecture review, the grilling discipline — pulled when the
    work calls for them.
  - *Prompt*: the thread, the worker's hand-off to integrate, the live decision in front of it.

So **role *is* mapped into the agents files** — deliberately, because the standing identity is what
specialization means — while skills carry the on-demand expertise and prompts carry the live task.
Each role gets the maximal stack; the parts do not compete, they compose.

## 4. The mechanics, verified on the real harnesses [omp][claude]

Tested with a **canary** (a context file naming a token the model could only know by having loaded
it), with **tools disabled** on the decisive runs (`omp --no-tools`, `claude --disallowedTools …`) so
a returned token proves *auto-load*, not the agent reading the file — plus negative controls.

| Harness | Setup | Result |
|---|---|---|
| **OMP (worker)** | `AGENTS.md` at the worktree root, `--no-tools --no-session` | **token returned** — auto-loaded |
| OMP (worker) | same, file removed from cwd | **NONE** — the file is causal, no carryover |
| **Claude (architect)** | `CLAUDE.md` at cwd (incl. a real git worktree) | **token returned** — auto-loaded |
| Claude (architect) | `AGENTS.md` alone at the worktree root | **NONE** — Claude ignores AGENTS.md |
| **Claude (adapter)** | `CLAUDE.md` with `@AGENTS.md`, file tools disabled | **token returned** — the import pulls AGENTS.md in |
| Claude (adapter) | `AGENTS.md` present, no import, file tools disabled | **NONE** — without the adapter it does not reach Claude |

Load-bearing facts, each verified:

1. **OMP auto-loads `AGENTS.md` from the worktree cwd** — proven with zero tools, so genuine context
   auto-load. Its own rule says *"Load AGENTS.md from … (project walk-up + user home)."* [omp]
2. **Claude auto-loads `CLAUDE.md`, never `AGENTS.md`** — empirically and by docs. [claude+doc]
3. **The adapter works:** `CLAUDE.md` containing `@AGENTS.md` puts the AGENTS.md content in Claude's
   context. So write the durable grounding once in `AGENTS.md`; the architect's `CLAUDE.md` is a
   one-line `@AGENTS.md`. [claude+doc]
4. **Both harnesses have a skills mechanism** — OMP natively (`--skills`, `--no-skills`, `omp agents`;
   on-demand loading) [omp]; Claude Code / the Agent SDK have skills too. The exact architect-side
   skill format is to be pinned when that side is built, but the principle holds: both roles can be
   specialized by skills, not only by prose. [design]

## 5. The blocker, and the sequencing [code]

Two facts set *when* each piece can land:

- **The transport runs at the repo root, not the fence.** [code] `conversation._claude` calls
  `claude -p` with **no `cwd`**; `worker.apply` uses the fence only to write `RESULT.md`. So **no
  fence agents-file or skill reaches a worker until the transport runs the worker with `cwd = the
  fence`.** And a repo-root `CLAUDE.md` reaches the *architect* immediately (it runs at repo root) —
  not a side-effect-free drop. (`--check` is immune — scripted transport, no real model.)
- **The worker is still `claude -p`, not OMP.** [code] The pi/OMP harness seam — worker = `omp`
  fenced in the worktree — is **parked, not built** (`harness-ideas.md` §0.1). OMP's native AGENTS.md
  and skills loading arrives with that seam.

**Sequencing:** the architect side and the source-of-truth `AGENTS.md` (+ the `CLAUDE.md` adapter,
retiring `worker.DEPTH`) can start **now**; the worker-fenced side (transport cwd-awareness, the OMP
flip, OMP skills) lands **with the parked harness seam**.

## 6. The design the next session owns [design]

Not "whether" — the direction is set: assemble all five parts into two maximally specialized roles.
The open work is the concrete assembly:

1. **The assembly map.** For each role, partition its grounding across the three channels:
   what is *standing identity* → the agents file; what is *on-demand expertise* → a skill; what is
   *live task* → the prompt. Name the actual pieces (the worker's disciplines, each capability's
   self-model, the architect's design methodologies) and place each.
2. **Single-sourcing from repo documents.** Every channel renders from the one source — no second
   `worker.DEPTH`. Decide how skills and agents files are *derived* (and kept in sync as the spec
   folds — the self-model is re-derived every fold; its skill form must follow).
3. **Role-specialized file placement.** The worker's fence is a checkout of the repo, so a
   repo-root `AGENTS.md` is shared with everything that roots there. Decide how the worker gets the
   *worker's* agents file and the architect gets the *architect's* — distinct cwds, scoped files, or
   a shared core plus per-role overlays.
4. **Skills as the routing.** Map the per-capability self-model onto skills (loaded on demand by the
   touched capability), replacing the whole-spec megaprompt `worker.prompt()` marshals — for both
   harnesses, single-sourced.
5. **Sequencing the build** (§5): architect side + `AGENTS.md`/adapter now; worker-fenced side with
   the harness seam. An ADR records the assembly model when the operator ratifies the partition.

**The honest harness limit** (slice-7-F1 / slice-8 precedent): the acceptance harness drives a
scripted transport with no real model, so it cannot assert a live `omp`/`claude` loaded a file or a
skill — that is the verified experiment in §4, recorded as such, never faked into the harness. The
harness *can* assert the scaffold: the files and skills exist and are single-sourced, the megaprompt
duplication is gone, and (with the seam) the transport runs the worker with `cwd = the fence`.
