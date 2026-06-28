surfaced: 0

[CONTRACT]
The worker is the one role whose standing disciplines are inlined into its prompt every episode rather than loaded as a skill. This change makes them loadable. The `worker` capability is registered as a methodology skill, so the fold materializes `worker/SKILL.md` from `spec/worker.md` through `channels` into both skill locations, single-sourced and audited like every other methodology. The worker prompt is routed to LOAD its `worker`, `depth`, and `writing-for-the-machine` skills from its own checkout, and the full inline re-send of the disciplines and the depth body is cut.

The de-inlining is gated on watched evidence that a live worker loads its skills inside the fence. The recorded fenced-run trace shows only that a worker has *run* in the fence, never that it *loaded a skill* there, so the prompt keeps a minimal inline hedge — the depth framework in brief and the no-loop discipline — rather than trust an unproven load. The hedge drops only once a worker is observed loading its skills. The whole-spec index stays (the cheap anti-myopia map), the record facts are kept but relevance-filtered to the actionable ones, and a worker-touching change now renders `spec/worker.md` once, not twice.

[DELTA]
# delta — worker disciplines become a loadable skill

## MODIFIED — worker
### Requirement: a worker is grounded in the depth standards, every episode
A worker MUST be grounded in the **depth standards** every episode — the deep-module framework (much
behavior behind a small interface; a simple interface matters more than a simple implementation; pull
complexity downward), strategic over tactical, and the **red flags** of shallowness — so it builds
**deep up front** rather than relying on the gate to catch shallowness after the fact. This is the
*proactive* primary anti-complexity defense: a worker that shares the long-term-health concern produces
deep modules, so the folding-conditions depth gate stays a rarely-tripped backstop.

The standards reach the worker as the **loaded `depth` skill** the prompt routes it to
(`skills/depth/SKILL.md` in its checkout), **plus a minimal inline hedge** that names the framework in
brief. The full depth **body** is no longer inlined in the prompt. It is single-sourced through the
methodology seam into the `depth` skill the worker loads and into the worker's whole-spec index, so a
sharpened slice reaches the next worker through the skill it loads with no second inline copy to drift.
The inline hedge is the watched-evidence backstop, kept because whether a live worker loads its skills
in the fence is unproven, not a frozen second source of the standards.

#### Scenario: the depth standards are in the grounding
- WHEN a worker is assembled to run
- THEN its prompt routes it to load the `depth` skill and carries a minimal hedge naming the
  deep-module framework and the red flags, so it builds deep up front

  ```check
  spawn worker
  grounding carries-depth
  ```

#### Scenario: the disciplines are derived from their source
- WHEN the depth capability (`spec/depth.md`) is sharpened
- THEN the `depth` skill the worker loads renders the change with nothing hand-copied, so the standards
  the worker carries cannot drift from their source

  ```check
  spawn worker
  sharpen
  grounding renders
  ```

## ADDED — worker
### Requirement: a worker loads its standing skills, hedged inline while the load is unproven
A worker MUST be routed to **load** its standing skills from its own checkout — the `worker` skill (its
own disciplines), the `depth` skill (the depth standards), and the `writing-for-the-machine` skill (the
standard for the delta and scenario prose it authors) — each at `skills/<name>/SKILL.md` in its working
directory. The `worker` capability MUST be registered as a methodology skill, so the fold materializes
`worker/SKILL.md` from `spec/worker.md` through `channels` into both skill locations, single-sourced and
audited against the slice exactly like the other methodologies.

The de-inlining is **gated on watched evidence** that a live worker loads its skills inside the fence,
evidence the recorded fenced-run trace does not yet carry: a worker has been observed *running* in the
fence, never *loading a skill* there. Until that evidence lands, the prompt MUST keep a **minimal inline
hedge** — the depth framework in brief and the no-loop discipline — rather than trust an unproven load.
The full inline re-send of the worker disciplines and the depth body is removed; the hedge is what
remains, and it drops only once a worker is observed loading its skills.

#### Scenario: the prompt routes the worker to load its skills
- WHEN a worker prompt is assembled for a node
- THEN it routes the worker to load its `worker`, `depth`, and `writing-for-the-machine` skills from
  `skills/<name>/SKILL.md` in its checkout, and carries a minimal inline hedge of the depth framework
  and the no-loop discipline in place of the full inline re-send

  ```check
  spawn worker
  grounding loads-skills
  ```

## Build notes — guidance for applying this delta (NOT folded; the parser ignores this section)

Realize the two requirements above with these exact engine edits. Keep the change minimal and coherent.

1. `engine/methodology.py` — register `worker` in `METHODOLOGIES` (one new entry), so
   `channels.materialize` writes `skills/worker/SKILL.md` and `.claude/skills/worker/SKILL.md` on fold.
   Suggested entry value: "hypercore's worker discipline — the system-facing half of the split: build
   fenced in your own git worktree, grounded in the spec slice, and hand the architect a complete
   machine-facing result; refine the delta you were handed and author no loop. Load when carrying out a
   spawned ask as the worker." (Keep the description under 1024 chars.) Mention `worker` in the module
   docstring's skill list beside the others.

2. `engine/worker.py` — restructure `prompt()` and relevance-filter `GROUNDING`:
   - DELETE the `_worker_disciplines` function and its call; DELETE the separate full-depth-body
     foregrounding (`depth_text`). Drop the `and n != "depth"` special-case so `depth` flows through the
     normal touched/index economy like every other capability (foregrounded when the delta names it,
     indexed otherwise). This removes the double-render of `spec/worker.md`.
   - The "How you are held:" block becomes, IN THIS ORDER (these three section headers MUST stay
     verbatim — the `order ask-leads` scenario matches them as substrings):
       "Your standing disciplines — load the `worker` skill from your checkout
       (`skills/worker/SKILL.md`) and the `writing-for-the-machine` skill
       (`skills/writing-for-the-machine/SKILL.md`); in brief, your audience is the architect and the
       spec, never the operator, and you refine the delta you were handed rather than author one."
       then the GROUNDING block (which MUST begin with "Two facts about the shared record"),
       then "The depth standards — load the `depth` skill (`skills/depth/SKILL.md`); in brief, build
       deep up front: deep modules, much behavior behind a small interface, complexity pulled downward,
       strategic over tactical, away from the red flags (a shallow module above all)."
   - Relevance-filter `GROUNDING` to the two ACTIONABLE record facts, dropping the merely-true mechanism
     (the repo-level lock spanning write→commit, "do nothing outside your worktree between them"). Keep
     it starting with "Two facts about the shared record". Keep "Stage the exact files your change
     touches" / never `git add -A`, and "You author no check that judges you" / "you record no loop" /
     gated-versus-watched. Carry no code tokens (`import `, `curses`).
   - Keep everything else (the ask-leads order, the whole-spec index, the glossary economy, the
     archive-grounds note, and the ENVELOPE last) unchanged.

3. `engine/worlds/worker_world.py` — import `methodology`; add and re-point two grounding properties:
   - ADD `loads-skills`: assert the assembled prompt contains all three skill paths
     ("skills/worker/SKILL.md", "skills/depth/SKILL.md", "skills/writing-for-the-machine/SKILL.md") and
     tells the worker to load them (the word "load" present). Fail with the missing paths otherwise.
   - RE-POINT `renders`: assert the sharpened depth nonce reaches the loaded depth SKILL render
     (`methodology.skill("depth", self.root)`), not the prompt body — proving the depth skill the worker
     loads is single-sourced from `spec/depth.md`, not a frozen copy.
   - Leave `carries-depth` checking the framework tokens; the minimal depth hedge carries them.

The gate runs the `worker` suite red at the fork base (the new `loads-skills` scenario fails — the base
prompt has no skill paths) and green at the tip (all `worker` scenarios pass). Do not weaken any verb to
make the base pass.
