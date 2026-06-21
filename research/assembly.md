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

This is why the living spec stays in the prompt and the depth disciplines move to a skill, even
though both are "needed every episode": the spec is **live** (it changes every fold) and so cannot
be frozen into an always-on file or a skill without a copy going stale; the depth disciplines are
**durable** and so can. And it is why the agents file stays thin: only the durable, every-episode,
*operational* residue belongs there — which §4.5's evidence says is the only part that helps.

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

## 2. The full-scan finding — resolving §6.4's tension [design]

§6.4 leaned: *"map the per-capability self-model onto skills (loaded on demand by the touched
capability), replacing the whole-spec megaprompt."* Worked against the code, that lean does not
hold whole, and the design must say why rather than paper over it.

**The worker's non-slice-confinement is by-construction, not a discipline.** `worker.py` is
emphatic: the worker holds the *whole* spec so its rescan catches a capability the handed delta
mis-named or missed, and "there is no path that runs a worker without it" — the grounding is
*assembled*, structural. If per-capability spec slices became on-demand skills loaded by the
touched set, the full scan would degrade to "the worker must remember to pull every other skill
too" — a discipline, and exactly the kind of "structural, not a discipline to remember" property
the worker is built to keep. Routing the spec would trade a structural guarantee for a habit.

**The resolution: route the expertise, not the requirements.** Split what §6.4 called "the
per-capability self-model":

- The per-capability **requirements** — the living spec, the self-model *as as-built reality* —
  stay **by-construction in the worker's grounding**, rendered live from source. They are small and
  scannable by design (the self-model's own requirement: "concise enough to scan across all of
  them at once"), so carrying all of them is cheap, and carrying all of them is what the full-scan
  guarantee *is*. This layer does not route.
- The per-capability **expertise / methodology** — the durable "how you build this capability
  well" that is *not* in the bare requirements — is what routes to **skills**, loaded on demand by
  the touched set. Plus the cross-cutting durable methodology: the **depth** disciplines (worker)
  and the **design methodologies** (architect).

So the megaprompt is replaced **in part**: the frozen methodology (`DEPTH`) and the identity prose
leave it for a skill and a thin file; the **live spec stays**, because full scan is structural.
This refines §6.4's lean rather than executing it verbatim — recorded as a machine-side resolution
(below, ADR 0009), the reasoning surfaced for the operator to ratify or overturn.

**A consequence for what ships first.** The skills with real content *today* are `depth` (worker)
and `design-it-twice` / `architecture-review` / grilling (architect) — each already a rich spec
slice or research doc. Per-capability *worker* skills are mostly empty today, because a capability
currently carries only its requirements (which stay full-scan) and little separable expertise. So
per-capability worker skills are an **as-needed growth** (a skill appears when a capability accrues
expertise beyond its requirements), not a day-one explosion of one-skill-per-capability. The
routing mechanism is built; it is populated as expertise accrues — the same "decomposition is
as-needed" discipline intent.md applies to the graph.

## 3. Single-sourcing (§6.2) — the derived render, by the fold

The smell to kill is concrete: `worker.DEPTH` is a hand-compression of `research/aposd.md` frozen
in a Python constant [code] — a second copy that drifts the moment aposd.md is sharpened. The fix
is already the shape of this system.

**Skills and agents files are derived renders of the source, exactly as the operator view is a
derived render of the self-model.** intent.md's discipline — "no statement in the as-built or gap
render is hand-authored; each is a render of the model and changes when the model changes" — is the
single-sourcing answer, applied to two more channels:

- the `depth` skill renders from `research/aposd.md` — one source for the depth disciplines, no
  frozen copy;
- a per-capability skill (when one exists, §2) renders from `spec/<cap>/spec.md`;
- the architect's methodology skills render from their spec slices / research docs;
- the agents file's operational anchor renders from one small source (the operational residue of
  the role constant).

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

## 4. Role-specialized placement (§6.3) — the filename is the router

§6.3 asked how the worker gets the worker's file and the architect gets the architect's, given the
fence is a checkout of the repo (so a repo-root file is shared). The §4 verification already
answers it: **the harness auto-load rule separates the roles for free.** [omp][claude]

- **`AGENTS.md`** (repo root) — the worker's minimal anchor. OMP auto-loads `AGENTS.md` from the
  cwd walk-up; the fence is a checkout, so the committed `AGENTS.md` is present at the fence root
  and the fenced worker loads it. [omp]
- **`CLAUDE.md`** (repo root) — the architect's minimal anchor. The architect runs at repo root
  and Claude auto-loads `CLAUDE.md`; it **ignores `AGENTS.md`** [claude], so the worker's file does
  not leak into the architect's context.
- **Shared core, if the operator wants one:** write it once in `AGENTS.md`; `CLAUDE.md` pulls it
  with `@AGENTS.md` (the verified adapter [claude]) plus any architect-only lines. If the two
  operational anchors do not actually overlap, each file stands alone — decide when the content is
  set (it is the operator's, §6.0).

No distinct-cwd trick and no per-role subdirectories are needed: the two filenames are the router,
and that fact is verified, not assumed. Skills live in each harness's skills location (OMP native;
Claude Code / the Agent SDK [doc]); the exact skill *format* per side is pinned when that side is
built (§4.4 of the investigation), but the principle — both roles specialized by skills, not only
by prose — holds on both.

## 5. Sequencing the build (§6.5)

Set by the two facts in §5 of the investigation: the transport runs at the repo root with no `cwd`,
and the worker is still `claude -p`, not OMP (the pi/OMP seam is parked).

**Now — no harness seam needed:**

1. **Retire the `DEPTH` smell.** Render the worker's depth grounding from `research/aposd.md`
   (single source), deleting the frozen constant. Pre-seam the worker is still `claude -p` with no
   fence cwd, so its depth grounding stays **in the prompt** — but rendered from aposd.md, not a
   frozen copy. The depth **skill artifact** is created now for when the seam lands. This is the
   concrete first build: it kills the named smell and single-sources it, with no change to what the
   worker is actually grounded in. Harness-assertable (the constant is gone; the render reads
   aposd.md).
2. **The derived-render mechanism + the render-on-fold step** (§3). Harness-assertable (the
   channel files regenerate from source; nothing hand-edited).
3. **The architect's `CLAUDE.md`** (minimal) and the worker's **`AGENTS.md`** (minimal) — *only if*
   the operator ratifies having them and sets the content (§6.0). The architect runs at repo root,
   so a repo-root `CLAUDE.md` reaches it immediately — this is the one channel that is **not**
   side-effect-free to drop, so it lands only on the operator's word.
4. **The architect's methodology skill artifacts** (design-it-twice, architecture-review,
   grilling), rendered from their spec slices.

**With the parked harness seam:**

5. **The transport runs the worker with `cwd` = the fence.** Then OMP auto-loads the fence's
   `AGENTS.md` and loads skills on demand; the worker's depth + per-capability expertise move from
   the prompt to skills, and the prompt shrinks to the live task + the full-scan spec.
6. **The OMP flip** (worker = `omp`, GPT-5.5), and OMP-native skill loading.

## 6. The honest harness limit

The acceptance harness drives a scripted transport with no real model (slice-7-F1 / slice-8
precedent), so it cannot assert that a live `omp` or `claude` loaded a file or a skill — that is the
verified experiment in §4 of the investigation, recorded as such, never faked into the harness. The
harness **can** assert the scaffold: the frozen `DEPTH` copy is gone and the depth grounding renders
from `research/aposd.md`; the derived channel files regenerate from source and nothing is
hand-edited; the skill and file artifacts exist and are single-sourced; and (with the seam) the
transport runs the worker with `cwd` = the fence.

## 7. What the operator ratifies — and what stays the operator's

**Proposed for ratification (machine-side, ADR 0009):**

- the governing two-axis cut (§0) and the assembly map it produces (§1);
- the full-scan resolution (§2) — *route the expertise, keep the requirements by-construction* —
  which **refines §6.4's lean** rather than executing it verbatim;
- single-sourcing as a derived render regenerated by the fold (§3), with the materialize-on-fold
  step as the one new mechanism;
- the filename-as-router placement (§4);
- the sequencing (§5) and the honest harness limit (§6).

**Left to the operator — not committed here (§6.0):**

- what "**minimal**" means; what (if anything) goes in the agents file; **whether to have one at
  all**. The illustrative shape is a handful of operational lines (the check command, the
  build/hand-back convention, a pointer to the skills); the depth philosophy, the "what hypercore
  is" prose, and the per-capability requirements do **not** belong in it. This is a lean, not a
  decision — the operator may define minimal differently or decline the file entirely.
- **measuring the file's worth** before leaning on it: §4.5 found context files often do not help
  and add ~20% cost, so the agents file's value for hypercore's own agents is to be measured (an
  A/B on real tasks), not assumed — the verify-don't-assume ethos that settled the mechanics,
  applied to the worth.

The build follows ratification; steps 1–2 of §5 (retiring the `DEPTH` smell, the derived-render
mechanism) are the lowest-regret start and depend on none of the operator-owned content.
