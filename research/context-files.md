# Item 2 — context files vs. prompt-assembled grounding: the verification and the routing boundary

*The investigation `next-work.md` item 2 asked for. The operator's instinct was that hypercore
grounds its agents **only** through hand-assembled prompt strings and leaves value on the table by
holding no context file. This document does what the note demanded first — **verify** that the
agents' real harnesses auto-load a context file — then resolves which grounding belongs in a file
and which stays routed. It settles nothing the operator owns: §7 collects the genuine forks.*

*First written anchored to `claude -p` for both roles; **re-grounded** (2026-06-21) after the
operator named the actual stack: the architect is Opus 4.8 (Claude), the **worker is GPT-5.5 via
pi/OMP**, and the **north star is open-weight / non-proprietary only** (`hypercore-parked/
harness-ideas.md` §0). That inverts which file is the source of truth — and both ends are now
verified on their real harnesses.*

*Marks: **[omp]** / **[claude]** = observed empirically this session on that harness; **[doc]** =
vendor documentation; **[code]** = present in this repo or the parked harness; **[proposed]** = the
architect's design, to be grilled; **[fork]** = a genuine judgment call left to the operator.*

---

## 1. The stack this grounds — two harnesses, two files, one open standard

hypercore's reasoning is not one brain. Phase 1 (now) runs a single Claude brain as a stopgap; the
intended split (`harness-parked` §0, sharpened by the operator this session) is:

- **Architect = Opus 4.8, via `claude -p`.** Claude reads **`CLAUDE.md`**; it does **not** read
  `AGENTS.md`. [claude+doc]
- **Worker = GPT-5.5, via pi/OMP** (`omp -p … --model openai-codex/gpt-5.5`), run fenced in the
  worktree (`hypercore-parked/harness-source`, `omp_runner.py`). OMP reads **`AGENTS.md`** — and, as
  a superset loader, CLAUDE.md and many other conventions too. [omp+code]
- **North star: open-weight only** (`harness-ideas.md` §0). Every closed route — Opus for the
  architect, GPT-5.5 for the worker — is an interim the north star eventually retires.

So the design question is **not** "which proprietary file." It is: **which file is the durable,
cross-vendor source of truth, and which is a per-vendor adapter over it.** `AGENTS.md` is the open
standard (OpenAI/Codex, opencode, OMP, and others read it); `CLAUDE.md` is Anthropic's. Banking on
the open standard is the same instinct as the north star. **AGENTS.md is the source of truth;
CLAUDE.md is a thin adapter** — exactly the operator's read.

## 2. The gates — verified on the real harnesses, both ends [omp][claude]

The whole idea hinges on auto-load, so it was tested with a **canary**: a context file naming a
secret token the model could only know by having the file loaded. Crucially, to exclude the
agent *tool-reading* the file (an agentic CLI with file tools will read a small directory), the
decisive runs **disabled tools** (`omp --no-tools`, `claude --disallowedTools Read Glob Grep Bash`),
so a returned token can *only* have come from auto-loaded context — plus a negative control.

| Harness | Setup | Result |
|---|---|---|
| **OMP (worker)** | `AGENTS.md` at the worktree root, `--no-tools --no-session` | **token returned** — auto-loaded |
| **OMP (worker)** | same, `AGENTS.md` removed from cwd, `--no-tools --no-session` | **NONE** — no carryover; the file is causal |
| **Claude (architect)** | `CLAUDE.md` at cwd (incl. a real git worktree) | **token returned** — auto-loaded |
| **Claude (architect)** | `AGENTS.md` alone at the worktree root | **NONE** — Claude ignores AGENTS.md |
| **Claude (adapter)** | `CLAUDE.md` containing `@AGENTS.md`, file tools disabled | **token returned** — the import pulled AGENTS.md in |
| **Claude (adapter)** | `AGENTS.md` present but no import, file tools disabled | **NONE** — without the adapter, AGENTS.md does not reach Claude |

Three facts, each load-bearing and each verified:

1. **The worker harness (OMP) auto-loads `AGENTS.md` from the worktree cwd** — proven with zero tools
   available, so it is genuine context auto-load, not a tool read. [omp] OMP's rule descriptions
   confirm the mechanism: *"Load AGENTS.md from … (project walk-up + user home)."* `--no-rules` does
   **not** disable it — in OMP's taxonomy `AGENTS.md` is a *context file*, loaded unconditionally,
   distinct from the cursor/windsurf-style "rules" that flag gates.
2. **The architect harness (Claude) auto-loads `CLAUDE.md`, never `AGENTS.md`** — confirmed
   empirically and by the docs (*"Claude Code reads `CLAUDE.md`, not `AGENTS.md`"*). [claude+doc]
3. **The adapter works end-to-end:** a `CLAUDE.md` containing `@AGENTS.md` pulls the AGENTS.md content
   into Claude's context; without the import Claude has nothing. [claude+doc] This is the documented
   pattern (`@AGENTS.md`, or a `ln -s AGENTS.md CLAUDE.md` symlink) — the exact adapter the operator
   wanted, now verified rather than assumed.

**Net:** author the grounding **once in `AGENTS.md`**; the worker reads it natively; a one-line
`CLAUDE.md` → `@AGENTS.md` gives the architect (and any Claude-Code building session) the same
content. The adapter is the temporary, proprietary edge; AGENTS.md is the durable centre.

## 3. The blocker, and the sequencing — the worker does not yet run in its fence [code]

Two facts gate *when* this lands, neither of which the surface note saw:

- **The current transport runs at the repo root, not the worktree.** [code] `conversation._claude`
  calls `claude -p` with **no `cwd`**; `worker.apply` uses the fence only to write `RESULT.md` after
  the fact — the model call runs where the python process launched (the repo root). So **no
  worktree context file can reach a worker until the transport runs the worker with `cwd = the
  fence`.** And because the architect already runs at the repo root, a repo-root `CLAUDE.md` reaches
  the *architect* immediately — committing one is not a side-effect-free file drop. (`--check` is
  immune: it drives a scripted transport, no real model call.)
- **The worker is still `claude -p`, not OMP.** [code] The pi/OMP harness — the seam that makes the
  worker `omp` fenced in the worktree (`harness.py`, `omp_runner.py`) — is **parked, not built in
  the fresh repo** (`harness-ideas.md` §0.1). The worker-side payoff of AGENTS.md (OMP auto-loads it
  in the fence) arrives with that seam.

This is why the investigation recommends rather than builds: the *content* move (depth disciplines →
`AGENTS.md`, single-sourced) is worth doing now and is immediately used by the architect and by
building sessions; the *worker* wiring (run the worker fenced and cwd-aware; flip the worker to OMP)
is the phase-2 harness seam. Author the file now; wire the worker when the seam lands.

## 4. The routing boundary — what belongs in the file, what stays assembled [proposed]

hypercore **routes** context deliberately (rebuild-spec §6): each role gets only its render — the
worker gets its touched capabilities foregrounded plus the scan, glossary, decisions, delta, ask;
the architect gets operator-facing prompts; neither holds the other's view. A context file is the
**opposite** of routing: it is ambient — every session rooted at or under it gets it, identically.
So the boundary is **which grounding is genuinely role-invariant and ambient** (a fit for the file)
versus **which is per-node and routed** (must stay assembled, or it flattens into one shared file —
the §6.2 failure).

- **→ `AGENTS.md` (ambient, durable, role-invariant):** the **depth-discipline *framework*** — what
  a deep module is, the red flags — and the "what hypercore is" frame. Same every episode,
  version-controlled, operator-legible: exactly `intent.md`'s *"durable state in version-controlled
  files,"* which a Python string literal is not. This **single-sources the live smell** the note
  named: `worker.DEPTH` is a hand-compressed copy of `research/aposd.md` pasted into a constant
  [code]. `AGENTS.md` carrying the framework (the architect's `CLAUDE.md` importing it via
  `@AGENTS.md`) makes the source the source — the duplication is *deleted*, not maintained.
- **stays assembled (per-node, routed):** the **per-capability spec slice and its touched/scan
  split** — this *is* the routing; it is computed per node and cannot be a static file. With it: the
  **glossary** (part of the self-model, *derived* and re-rendered every fold — pinning it into a
  static file would flatten the model and need regenerating on each fold), the **decisions**, the
  **handed delta**, the **ask**, and the role **stance** (the worker's *"build deep"* vs. the
  architect's *"judge depth at the gate"* — role-specific instruction over a role-invariant
  framework; putting the worker's stance in the shared file leaks it to the architect — the §6
  failure).

The note's guess ("durable role-invariant → files; self-model routing → stays assembled") was right
in shape. The only correction is the file: the durable layer lives in **`AGENTS.md`** (the open
standard the worker harness reads), with `CLAUDE.md` a generated `@AGENTS.md` adapter for the
architect — not the first draft's "CLAUDE.md, since the worker runs `claude -p`," which had the
worker's harness wrong.

## 5. The richer option OMP opens — skills (and why it is also a fork) [omp]

OMP is not only a context-file loader; it has a native **skills** mechanism — on-demand capability
loading (`--no-skills`, `--skills=<glob>`, `omp agents`), selected per task rather than always
present. A *parked* investigation hit exactly hypercore's question (`Trash/…/pi-omp-skill-loading-
report`): prior work *"flattened skills into always-present prompt text rather than preserving OMP's
skill selection and on-demand loading."* That is the same shape as the `worker.DEPTH` smell — and it
suggests the **routed per-capability self-model could map onto OMP skills** (loaded on demand by the
touched capability) rather than assembled into one prompt: routing, done by the harness.

But skills are **OMP-specific**: the Claude architect has no OMP skills, and a skill mechanism is not
the open `AGENTS.md` standard. Leaning on it coreward cuts against the north star and re-splits the
two roles' grounding paths. So it is a genuine fork (§7 F3), not a free win — powerful for the
worker, unavailable to the architect, and proprietary to one harness.

## 6. Two uses, and the audience collision (unchanged by the re-grounding) [proposed]

The note separated two uses; they still collide in one repo-root file. **(a)** grounding hypercore's
*roles* wants the depth framework — content both the worker (builds deep) and the architect (judges
depth) should hold. **(b)** onboarding agents that *build* hypercore (this meta-workflow) wants the
reading order, the slice workflow, `python3 -m hyper --check`. Because the architect runs at the repo
root, a single repo-root file holding (b) would feed the architect *"you are a building agent, read
next-work.md"* — wrong-context noise for a role mid-conversation with the operator. **(a) and (b) are
different audiences; one ambient file cannot serve both.** Keep (b) separate, or defer it.

## 7. The open forks — the operator's to settle

- **[fork] F1 — adopt file-grounding, with `AGENTS.md` as the source of truth and `CLAUDE.md` as the
  `@AGENTS.md` adapter?** *Lean: yes, for the depth framework only.* It deletes the `worker.DEPTH`
  duplication, is operator-legible and version-controlled, is read natively by the worker harness,
  and banks on the open standard (north-star-aligned). The architect's adapter is one line and
  verified. *Flips it:* if running the worker fenced+cwd-aware is far off and de-duplication is the
  only near-term win, a shared `research/aposd.md`-imported constant gets that without a file.
- **[fork] F2 — what crosses into `AGENTS.md`:** the role-invariant framework (depth disciplines, the
  "what hypercore is" frame), **not** the routed per-capability self-model. *Lean: framework only;*
  the routing (spec slice, glossary, decisions, delta, stance) stays assembled (§4).
- **[fork] F3 — the routed layer: prompt-assembled (portable) vs. OMP skills (routed, on-demand, but
  OMP-only).** *Lean: stay prompt-assembled for now* — it serves both the Claude architect and the
  OMP worker and stays vendor-neutral; revisit OMP skills only if/when the architect also moves to a
  harness with skills. This is the deeper form of the original "self-model routing" tension (§5).
- **[fork] F4 — sequencing.** Author `AGENTS.md` + the `CLAUDE.md` adapter **now** (used immediately
  by the architect and building sessions; `worker.DEPTH` retired); land the **worker** side (run the
  worker fenced + cwd-aware; flip the worker to OMP) **with the parked harness seam**. *Lean: split
  it this way* rather than waiting for the seam to start, or building worker-grounding against a
  transport that does not yet run in the fence.
- **[fork] F5 — user-level files are un-routed inputs to every role.** OMP loads `AGENTS.md` from
  *user home* too, and Claude always loads `~/.claude/CLAUDE.md`. The operator's personal files leak
  into both roles, outside any fence. *Lean: note the exposure; do not engineer around it now* — it
  is the operator's own machine.

## 8. What a build would touch, and the honest acceptance story

The recommended near-term core (F1+F2+F4's "author now" half) touches: a committed **`AGENTS.md`**
(the depth framework, importing/condensing `research/aposd.md`) at the repo root, present in every
worktree checkout; a one-line **`CLAUDE.md`** (`@AGENTS.md`) adapter; **`hyper/worker.py`** —
`DEPTH` leaves the Python constant, the prompt keeps only the worker's *stance*; **`spec/worker`**
and **`spec/self-model`** deltas (grounding now arrives partly ambient, partly routed; the boundary
stated); the **glossary** (ambient context file / source-of-truth vs. routed context; the
CLAUDE.md-adapter term); and an **ADR** (file-grounding adopted, `AGENTS.md` the source of truth,
`CLAUDE.md` the adapter, the routing boundary — it *adds* an ambient layer beside the routed one,
superseding nothing). The worker-side half (F4) — the transport running fenced + cwd-aware, the OMP
flip — folds into the parked harness seam when it is built.

**The honest limit, the slice-7-F1 / slice-8 precedent:** the acceptance harness drives a *scripted*
transport with no real model and no network, so it **cannot** assert that a real `omp`/`claude`
loaded the file — that is the canary experiment in §2, run by hand, recorded as verified-by-
experiment, not faked into the harness. The harness *can* assert the mechanical scaffold: `AGENTS.md`
and the `CLAUDE.md` adapter exist at the repo root, the worker prompt no longer carries the
duplicated `DEPTH` constant, and (when the seam lands) the transport threads a cwd and runs the
worker with `cwd = the fence`. The model-side fact (the file actually grounds the agent) is the
verified experiment above — the same self-honesty the depth scan and load-bearing detection carry.
