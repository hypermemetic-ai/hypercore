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
| **Agents files** | `AGENTS.md` (worker) + `CLAUDE.md`→`@AGENTS.md` (architect) | always-on, per session | **minimal, operational** grounding — the check command, the tools, the workflow pointer (kept small; see §4.5) |
| **Skills** | on-demand capability/methodology packs (both harnesses have them) | loaded when relevant | **specialized expertise, routed** — pulled by the task, not always resident; the heavy methodology lives here |
| **Prompts** | the per-node assembled context (handed delta, ask, touched spec slice, live state) | per episode | the **live, task-specific** material that only exists for this node |

The governing relationship: **repo documents are the source; agents files, skills, and prompts are
three derived delivery channels** — always-on, on-demand, and per-node respectively. Nothing is
hand-copied between them (that is the `worker.DEPTH` smell — a compressed copy of `research/aposd.md`
frozen in a Python constant [code]); each channel renders from the one source.

The earlier draft mis-cast this as a turf war ("keep routing in prompts; resist files and skills").
That was wrong. But the *next* draft over-corrected the other way — "agents files are where role
identity belongs, always on" — and **§4.5's evidence does not support that**. The calibrated shape:
**skills carry the specialization** (on-demand, per-capability loading is exactly what hypercore's
self-model wants — and the better-backed mechanism), the **always-on agents file stays minimal and
operational** (overview/identity prose in it is the failure mode the evidence names), and hypercore's
real specialization leverage is its **workflow** (routing, fence, folding) plus skills — not a thick
context file. The megaprompt `worker.prompt()` assembles is still what this replaces; it just lands
mostly in **skills**, not in the agents file.

## 3. The two roles, specialized — the target layering [design]

What each role is assembled from, every piece single-sourced from repo documents:

- **Worker (GPT-5.5 / OMP), fenced.**
  - *Agents file* (`AGENTS.md` at the fence root): **minimal and operational** — that this is a
    hypercore worker, the feedback-loop/check command, the tools and conventions to use, a pointer to
    the skills. Small and high-signal (§4.5: thick "identity" prose in the always-on file is the
    documented failure mode).
  - *Skills*: where the worker's specialization actually lives — the depth/deep-module methodology,
    the touched capability's self-model, the red→green-loop discipline, design patterns — pulled on
    demand for the node it is on.
  - *Prompt*: the handed delta, the ask, the touched spec slice, the live state of this node.
- **Architect (Opus 4.8 / Claude).**
  - *Agents file* (`CLAUDE.md` → `@AGENTS.md`, or its own): minimal — that this is hypercore's
    architect, operator-facing, with the workflow pointer. Not the design philosophy as prose.
  - *Skills*: where the architect's specialization lives — design-it-twice, the architecture review,
    the grilling and coherence disciplines — pulled when the work calls for them.
  - *Prompt*: the thread, the worker's hand-off to integrate, the live decision in front of it.

So the specialization is carried mostly by **skills** (on-demand) and by hypercore's **workflow**;
the agents file is a thin, operational anchor, not the role's whole identity. The parts compose; the
weight sits where the evidence (§4.5) says it earns its keep.

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

## 4.5 Is the model backed? What field consensus does and does not support

The mechanics above are observations, not opinions. The *design model* (§2–§3) needs more than
confidence, so it was checked against current authoritative sources — and the check moved it:

- **Backed (strong):** **`AGENTS.md` as the open standard to bank on.** ~28+ tools read it natively,
  60k+ repos, stewarded by the Linux Foundation's Agentic AI Foundation. The source-of-truth choice
  is well-founded. ([agents.md], [InfoQ 2025-08])
- **Backed (Anthropic's own guidance):** **skills + progressive disclosure as the on-demand
  specialization mechanism** — *"skills transform general-purpose agents into specialized agents,"*
  loaded only when relevant — and **minimal, high-signal always-on context** as a *hybrid* with
  just-in-time retrieval (*"the smallest set of high-signal tokens"*). This backs "specialization via
  skills" and "keep the agents file small." ([Anthropic: Agent Skills], [Anthropic: context engineering])
- **NOT backed — partly contradicted:** the bet that **loading role grounding into an agents file
  makes a role more skilled.** A 2026 study ([arXiv 2602.11988], [InfoQ 2026-03]) found context files
  **often reduce success and reliably add ~20% cost** (+2.5–3.9 steps): LLM-generated files −0.5% to
  −2% success; developer-authored +4% but *"marginal and inconsistent"* (no gain for Claude Code).
  What **helped** was minimal, specific *operational* instructions (a named tool was used 1.6× vs
  0.01×); what **hurt** was codebase overviews and identity/explanatory prose (*"context files do not
  provide effective overviews"*; *"unnecessary requirements make tasks harder"*). Their recommendation:
  **omit generated context files; include only minimal requirements.**

The correction this forces, already folded into §2–§3: the heavy methodology — the depth disciplines,
the per-capability self-model — belongs in **on-demand skills**, not the always-on agents file (it is
exactly the "overview/identity prose" the evidence flags). The agents file stays **minimal and
operational**. And hypercore must treat the file's value for *its own* agents as something to
**measure, not assume** — the "verify, don't assume" ethos that settled the mechanics, applied to the
*worth*. (My own extrapolations — mapping the self-model onto skills, the clean three-channel
taxonomy — are reasonable and consistent with the above, but they are design, not consensus.)

Sources: [agents.md](https://agents.md/) · [InfoQ 2025-08](https://www.infoq.com/news/2025/08/agents-md/) ·
[Anthropic: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) ·
[Anthropic: context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) ·
[arXiv 2602.11988](https://arxiv.org/html/2602.11988v1) ·
[InfoQ 2026-03](https://www.infoq.com/news/2026/03/agents-context-file-value-review/)

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

The direction is set: specialize the two roles via **skills + workflow**, with a **minimal**
agents file — calibrated by §4.5's evidence, not the over-confident "thick identity file." The open
work is the concrete assembly:

0. **Earn the always-on file empirically.** §4.5: context files often don't help and add ~20% cost.
   So keep the agents file minimal and operational, do **not** auto-generate it, and **measure**
   whether it helps hypercore's own agents (an A/B on real tasks) before leaning on it — the same
   verification ethos that settled the mechanics, applied to the worth. **"Minimal" is not defined
   here and nothing about the file's content is committed** — what (if anything) goes in the agents
   file is the operator's to set. The illustrative shape is a handful of operational lines (the check
   command, the build/hand-back convention, a pointer to skills); the depth philosophy, "what
   hypercore is" prose, and the per-capability self-model do **not** belong in it. The operator may
   define "minimal" differently, or decline the agents file entirely; this is a lean, not a decision.
1. **The assembly map.** For each role, partition its grounding: *minimal operational anchor* → the
   agents file; *the heavy expertise* (the worker's disciplines, each capability's self-model, the
   architect's design methodologies) → skills; *live task* → the prompt. Name the actual pieces and
   place each, with the weight on skills.
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
