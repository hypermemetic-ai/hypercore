# Item 2 — the assembly design (`context-files.md` §6, worked concrete)

*The design `research/context-files.md` §6 handed the next session. The investigation set the
goal — two roles (**architect**, **worker**), each as skilled and specialized as we can make
them, assembled from five parts (repo documents, agents files, skills, prompts) — verified the
mechanics on the real harnesses (§4 there), and calibrated against the field evidence (§4.5
there): keep the always-on agents file minimal, carry the specialization in skills + workflow,
and **measure** the file's worth rather than assume it. This document turns that direction into a
concrete, ratifiable assembly. It is the analog of `regrounding.md` for this item: it designs,
it builds nothing, and it settles nothing the operator owns.*

*Marks: **[omp]** / **[claude]** = verified on that harness in §4 of `context-files.md`; **[doc]**
= vendor documentation; **[code]** = present in this repo; **[design]** = the resolution proposed
here, machine-side, awaiting the operator's ratification.*

---

## 0. The governing cut — two axes, not one

§2 of the investigation framed the channels as *always-on / on-demand / per-node*. That axis alone
under-determines the placement: it does not say why the living spec (needed every episode) should
not simply live in the always-on file. The sharper cut is **two axes**, and the pair places every
piece deterministically:

- **Durability** — does the piece change every fold, or is it durable across many?
- **Reach** — does *every* episode need it, or only the episodes a particular task routes to?

| | every-episode | routed-by-task |
|---|---|---|
| **durable** | **agents file** — minimal, operational (the anchor) | **skills** — the specialization, loaded on demand |
| **live (re-derived each fold)** | **prompt** — rendered fresh from source, by construction | (degenerate: a live, narrowly-routed thing is just prompt) |

This is why the live grounding stays prompt-side (the **whole spec, preloaded by construction**,
touched foregrounded — §2) while the depth disciplines move to a skill, even though both are "needed
every episode": the grounding is **live** (it changes every fold) and so cannot be frozen into an
always-on file or a skill without a copy going stale; the depth disciplines are **durable** and so
can. And it is why the agents file stays thin: only the durable, every-episode, *operational* residue
belongs there — which the evidence (§8) says is the only part that helps, and only when it is
**non-inferable** (the check command, the build/hand-back convention). The operator set this lean
(2026-06-21): a single minimal shared anchor, non-inferable content only — §7.

## 1. The assembly map (§6.1) — every current prompt-piece, placed

Today everything is one string. Here is each piece of the two roles' current prompts and the
channel the cut assigns it. [code: `worker.py`, `conversation.py`]

**Worker** (`worker.WORKER` + `worker.DEPTH` + `worker.prompt()`):

| Piece (today) | Channel | Why |
|---|---|---|
| `WORKER` role — *operational* core (build behind a feedback loop, hand back the JSON result, write for the machine) | **agents file** (`AGENTS.md`) | durable, every-episode, operational — the part §4.5 says earns its keep |
| `WORKER` role — *identity* prose ("you are the system-facing half…") | **dropped / minimal** | durable but explanatory; §4.5's documented failure mode — not load-bearing for the work |
| `DEPTH` disciplines (the aposd compression) | **skill** (`depth`), single-sourced from `research/aposd.md` | durable methodology; the frozen copy is the named smell — see §3 |
| the ask / contract | **prompt** | live, this node only |
| the handed delta (to verify + refine) | **prompt** | live, this node only |
| the touched capabilities (the grounding) | **prompt** | live (re-derived each fold), by-construction full scan — see §2 |
| the rest of the spec (the scan) | **prompt** | live, by-construction full scan — see §2 |
| the glossary | **prompt** | live (folds sharpen it), every-episode |
| the decisions (all ADRs) | **on-demand reference** (the fenced checkout / a skill), not the always-on prompt | durable, but most nodes need none of them; `conditions.py` reads depth-decisions from disk, not the worker's prompt [code] |

**Architect** (`conversation.SYSTEM` / `COHERENCE` / `explain`):

| Piece (today) | Channel | Why |
|---|---|---|
| role — *operational* core (single voice to the operator; file / card / answer / done) | **agents file** (`CLAUDE.md`) | durable, every-episode, operational |
| the design methodologies — grilling, the coherence judgment, design-it-twice, the architecture review | **skills**, rendered from their spec slices | durable specialization, routed by the work in front of the architect |
| the live thread / the contract / the worker's report to integrate | **prompt** | live, this turn only |

The weight lands on **skills + the prompt-rendered live spec**, with a thin operational agents
file — which is the calibrated shape §4.5 backs, not the thick-identity-file the earlier draft
reached for.

## 2. The full scan stays whole and by-construction — the keystone [corrected 2026-06-21]

This section flip-flopped, and the final answer is the one the original slice-4 build already holds.
§6.4 leaned "map the per-capability self-model onto skills, replacing the whole-spec megaprompt."
The first draft pushed back (keep the spec whole). The second pass then over-corrected to
just-in-time on the field evidence. The operator re-raised the whole-picture concern — for the
second time — and that exposed the just-in-time move as wrong here. The settled answer: **the worker
holds the whole spec, preloaded, by construction; "touched" foregrounds attention, it never filters
what is available.**

**Why whole, not just-in-time.** The worker needs the whole picture for three things, and a
conditional pull only safely covers the first:

1. *Awareness* — knowing a capability exists. (A thin index could cover this.)
2. *Cross-impact verification* — the **keystone** (rebuild-spec §6.4): the worker's full rescan is
   the structural defense against the architect's delta mis-naming or missing a capability. Catching
   "my change to X also breaks an invariant Y guarantees" needs Y's actual contract in view, not a
   one-liner. `slice4` tests exactly this ("the context contains the whole spec, not only the touched
   slice").
3. *Design coherence* — building a module that fits the existing seams and abstractions, not one
   locally sensible but globally discordant.

A just-in-time pull fails 2 and 3, and fails them in the worst way: the pull is **gated on the
worker already suspecting it must look** — which a *myopic* worker will not. Its trigger assumes the
absence of the very myopia it must guard against. That converts a by-construction guarantee into a
discipline, the one thing the worker design refuses ("structural, not a discipline to remember").

**Why the field's just-in-time evidence does not apply here.** That guidance targets *large/external*
context — sprawling codebases, retrieved documents, million-token windows. hypercore's living spec is
the opposite: deliberately **small and wholly scannable** (a `self-model` requirement, "concise
enough to scan across all of them at once"). And the field's *actual* recommendation is a hybrid —
**preload the high-signal core, JIT the long tail.** The spec *is* the high-signal core; preloading
it whole is what the hybrid endorses, not what it warns against. If the spec ever grew too big to
preload, that would be a `self-model` "scannable" violation to fix at the source, never a reason to
blind the worker.

**Where just-in-time does belong: the reference tail.** The economy target is not the spec — it is
the **ADRs/decisions**, which grow fastest and are least relevant per node (and which §1 already put
on-demand). They carry no whole-picture stake, so they are the right thing to pull from the fenced
checkout once the worker runs there. The capability-index idea is dropped as premature: redundant
when the whole spec is already present.

**What still routes to skills.** The per-capability *expertise / methodology* (the durable "how you
build this capability well," beyond the requirements) and the cross-cutting **depth** disciplines
(worker) and **design methodologies** (architect). The spec *requirements* are not routed — they are
preloaded whole. The skills with real content today are `depth` and the architect's three
methodologies; per-capability worker skills are an **as-needed growth**, not a day-one split.

**Consequence for the build.** Because "whole spec preloaded, touched foregrounded" is exactly what
`worker.context`/`worker.prompt` already do, item 2 makes **no change** to the worker's spec
grounding and does not perturb the keystone or its checks. The only on-demand shift is moving the
ADR/reference tail off the prompt — and that lands with the harness seam (the worker needs the fence
to pull from).

## 3. Single-sourcing (§6.2) — the derived render, by the fold

The smell to kill is concrete: `worker.DEPTH` is a hand-compression of `research/aposd.md` frozen
in a Python constant [code] — a second copy that drifts the moment aposd.md is sharpened. The fix
is already the shape of this system.

**Skills and agents files are derived renders of the source, exactly as the operator view is a
derived render of the self-model.** intent.md's discipline — "no statement in the as-built or gap
render is hand-authored; each is a render of the model and changes when the model changes" — is the
single-sourcing answer, applied to two more channels:

- the `depth` skill — and, pre-seam, the worker's prompt-side depth grounding — render from
  `research/aposd.md`: one source for the depth disciplines, no frozen copy;
- a per-capability skill (when one exists, §2) renders from `spec/<cap>/spec.md`;
- the architect's methodology skills render from their spec slices / research docs;
- the agents file's operational anchor renders from one small source (the non-inferable operational
  residue of the role constant — §0).

**Kept in sync by the fold.** The self-model is re-derived every fold; its derived channels
follow. The fold gains a **render step** that regenerates the derived channel files from source —
the same act that re-renders the operator view. Because the channels are *generated, never
hand-edited*, drift is structurally impossible, not a thing discipline must prevent — the exact
guarantee `delta.fold` already gives the spec.

**The one new mechanism.** The operator view is never a file — it is read live in the TUI from the
spec [code: `view.py`/`render.py`]. Agents files and skills are static files an *external* harness
auto-loads, so they cannot be read live; they must be **materialized** on disk — generated by the
render step, committed, regenerated when the source changes. That materialize-on-fold step is the
single genuinely new piece the build adds; everything else is the existing derived-render
discipline pointed at two new targets.

## 4. Placement — one shared anchor, symlinked [operator-amended 2026-06-21]

§6.3 asked how the worker gets the worker's file and the architect gets the architect's. The first
draft answered "two role-specialized files, separated by the harness auto-load rule." The
second-pass research (§8) made that unnecessary and the operator simplified it: **one shared
anchor.**

Two facts collapse the placement. First, role specialization lives entirely in **skills** (field
consensus, §8), so the always-on file carries only the *shared, non-inferable* operational residue
(the check command, the hand-back convention) — which is the same for both roles; there is nothing
role-specific left to put in it. Second, Claude now reads `AGENTS.md` (when no `CLAUDE.md` is
present), and the clean, standard pattern is a single file with a symlink. [claude+doc, §8] So:

- **`AGENTS.md`** (repo root) — the one minimal shared anchor. OMP auto-loads it from the fence
  (a checkout, so the committed file is present at the fence root) [omp]; the architect reads the
  same content via the symlink below.
- **`CLAUDE.md` → `AGENTS.md`** — a symlink (`ln -s AGENTS.md CLAUDE.md`), which the architect's
  harness treats as its own. One file, one source; no `@import` adapter, no two role files, nothing
  to keep in sync between roles. [claude+doc, §8]

Skills live in each harness's skills location (OMP native; Claude Code / the Agent SDK [doc]); the
exact skill *format* per side is pinned when that side is built (§4.4 of the investigation), but the
principle — both roles specialized by skills, not by prose — holds on both. (The `@AGENTS.md` adapter
the investigation verified still works and is the fallback if the symlink is ever inconvenient; the
symlink is simply cleaner.)

## 5. Sequencing the build (§6.5)

Set by the two facts in §5 of the investigation: the transport runs at the repo root with no `cwd`,
and the worker is still `claude -p`, not OMP (the pi/OMP seam is parked).

**Now — no harness seam needed:**

1. **Retire the `DEPTH` smell.** Render the worker's depth grounding from `research/aposd.md`
   (single source), deleting the frozen constant. Pre-seam the worker is still `claude -p` with no
   fence cwd, so its depth grounding stays **in the prompt** — but rendered from aposd.md, not a
   frozen copy. The depth **skill artifact** is created now for when the seam lands. The concrete
   first build: kills the named smell and single-sources it, no change to what the worker is
   grounded in. Harness-assertable (the constant is gone; the render reads aposd.md).
2. **The derived-render / materialize-on-fold mechanism** (§3) — skills and the agents file
   regenerate from source on fold. Harness-assertable (nothing hand-edited; regenerates).
3. **The minimal shared `AGENTS.md` + `CLAUDE.md` symlink** (§0, §4) — non-inferable content the
   operator set: the check command, the hand-back convention, a pointer to the skills. The architect
   runs at repo root, so the symlinked file reaches it immediately (not side-effect-free) — which is
   why the content is kept to the non-inferable minimum the evidence endorses.
4. **The architect's methodology skill artifacts** (design-it-twice, architecture-review,
   grilling), rendered from their spec slices.

The worker's **spec grounding is untouched** — whole spec preloaded, touched foregrounded (§2) — so
no step here perturbs the slice-4 keystone or its checks.

**With the parked harness seam:**

5. **The transport runs the worker with `cwd` = the fence.** The **reference tail** (the
   ADRs/decisions) is dropped from the prompt and pulled just-in-time from the checkout (read/grep);
   **the spec capabilities stay preloaded** (the whole-picture keystone, §2). OMP auto-loads the
   fence's `AGENTS.md` and loads skills on demand; the worker's depth + per-capability expertise move
   from the prompt to skills.
6. **The OMP flip** (worker = `omp`, GPT-5.5), and OMP-native skill loading.

## 6. The honest harness limit

The acceptance harness drives a scripted transport with no real model (slice-7-F1 / slice-8
precedent), so it cannot assert that a live `omp` or `claude` loaded a file or a skill — that is the
verified experiment in §4 of the investigation, recorded as such, never faked into the harness. The
harness **can** assert the scaffold: the frozen `DEPTH` copy is gone and the depth grounding renders
from `research/aposd.md`; the derived channel files regenerate from source and nothing is
hand-edited; the skill and file artifacts exist and are single-sourced; and (with the seam) the
transport runs the worker with `cwd` = the fence.

## 7. Ratified — what the operator decided (2026-06-21)

The assembly model is **operator-ratified** (ADR 0009), with two decisions made at ratification:

- **The agents file is a single minimal shared anchor, non-inferable content only.** Of the three
  positions weighed — skills-only / minimal anchor / anchor-then-measure — the operator chose the
  minimal anchor: one `AGENTS.md` (symlinked as `CLAUDE.md`) holding only the check command, the
  build/hand-back convention, and a pointer to the skills. This is exactly the §8 study's endorsed
  "non-inferable details." No overview/identity prose, no per-capability requirements. The file's
  worth stays measurable, but the lean is set: keep it minimal; specialization is in skills.
- **The full scan stays whole and by-construction (§2).** At first ratification this was amended to
  just-in-time; the operator then re-raised the whole-picture concern and the amendment was
  **withdrawn** the same day. The worker holds the *whole* spec, preloaded, touched foregrounded for
  attention only — the slice-4 keystone, the defense against the architect's mis-scoping and against
  worker myopia. Just-in-time is reserved for the ADR/reference tail, which carries no whole-picture
  stake. (Coherence note: the just-in-time amendment over-applied field evidence calibrated for
  large/external context to a spec deliberately kept small and scannable.)

Ratified alongside: the governing two-axis cut (§0) and the assembly map (§1); single-sourcing as a
derived render regenerated by the fold, with the materialize-on-fold step (§3); the one-shared-anchor
symlink placement (§4); the sequencing (§5) and the honest harness limit (§6). Residual machine-side
specifics — the exact per-harness skill format, and the harness-seam build — remain to be pinned when
that side is built. The build now proceeds in §5 order, lowest-regret first.

## 8. Second-pass validation (live sources, 2026-06-21)

Before ratifying, the design was checked a second time against current sources — open to
contradicting itself. Three things validated and sharpened; two facts moved the design.

- **Validated (strong) — the agents-file evidence.** The ETH Zurich study `context-files.md` §4.5
  cited is real and its numbers hold: *Evaluating AGENTS.md* ([arXiv 2602.11988]; [InfoQ 2026-03]).
  LLM-generated context files **−3% success / +20% cost**; human-written **+4% / +19% cost**
  ("marginal and inconsistent"; no gain for Claude Code). Its recommendation is *sharper* than
  "minimal/operational": **omit generated files; limit human-written ones to non-inferable details
  — highly specific tooling or custom build commands.** Files hurt by being over-followed (more
  tests/reads/greps) and *"do not function as effective repository overviews."* → the minimal,
  non-inferable, no-overview anchor (§0, §7) is the paper's exact prescription; the check command is
  the textbook non-inferable detail.
- **Validated (strong) — skills as the specialization mechanism.** Progressive disclosure (three
  levels: ~50-token metadata → 2–5k `SKILL.md` → resources) and *"one general-purpose agent + a
  library of specialized capabilities"* over specialized agents — an **open standard** (Dec 2025,
  adopted cross-vendor). The AGENTS.md-vs-skill division of labor (always-on standard checks → the
  file; specialized multi-step workflows → skills) is field consensus that maps 1:1 onto §1.
  ([Anthropic: Agent Skills], [Anthropic: context engineering])
- **Moved the design (fact 1) — placement simplifies.** Claude now reads `AGENTS.md` (when no
  `CLAUDE.md` is present), and the clean standard pattern is one file with a `CLAUDE.md → AGENTS.md`
  symlink. With specialization in skills, the always-on anchor is one shared file — retiring the
  two-role-files / `@import`-adapter plan (§4). ([Claude Code #34235]; community guides)
- **Fact 2, over-applied then corrected — the spec stays preloaded.** The field leans **just-in-time
  over preloading**, but that guidance targets *large/external* context, and its actual shape is a
  hybrid: *preload the high-signal core, JIT the long tail* (Claude Code itself preloads a small file
  and uses glob/grep for the rest). Read first as "move the spec scan to just-in-time," it was
  corrected when the operator re-raised whole-picture: hypercore's spec is the small,
  scannable-by-design high-signal core, so it stays **preloaded whole** (§2); just-in-time is for the
  ADR/reference tail. ([Anthropic: context engineering])

Sources: [arXiv 2602.11988](https://arxiv.org/abs/2602.11988) ·
[InfoQ 2026-03](https://www.infoq.com/news/2026/03/agents-context-file-value-review/) ·
[Anthropic: Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) ·
[Anthropic: context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) ·
[Claude Code #34235](https://github.com/anthropics/claude-code/issues/34235)
