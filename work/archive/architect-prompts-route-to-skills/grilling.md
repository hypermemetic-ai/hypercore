surfaced: 0

[CONTRACT]
This ask routes each per-episode architect prompt to its loaded skill and strips the methodology
restatement the prompt currently carries, so the skill is the one source and no second copy can drift
from `spec/<cap>.md`. The architect runs as Claude Code, which discovers `.claude/skills/` natively, so
naming the skill in the prompt is enough to load it (the worker's skill-load stays watched evidence on a
separate node — out of scope here).

Six per-episode architect prompts change. Each KEEPS its live task/material and its structured reply
envelope inline, and DROPS only the paraphrased methodology its skill single-sources:
- `communication.SYSTEM` (the operator turn) -> instruct loading the `communication` skill; keep the
  live task (decide what the operator's words are and land one consequence -- file an ask, raise a card,
  or answer); keep `SYSTEM_SCHEMA`.
- `communication.COHERENCE` (the archive judgment) -> instruct loading the `coherence` skill; keep the
  live task (judge this hand-off against the contract at the operator's altitude; the report is
  machine-facing and you author every operator-facing word yourself); the contract and report stay
  inline in `integrate`; keep `COHERENCE_SCHEMA`.
- the explain prompt inside `communication.explain()` -> extract it to a module constant
  `communication.EXPLAIN` and instruct loading the `communication` skill; keep the live task (tell the
  story toward this decision; the card stays inline); keep `EXPLAIN_SCHEMA`.
- `grill.FLOOR` (the grilling floor) -> instruct loading the `grilling` skill; keep the live material
  (the living-spec digest and the ask stay inline); keep `FLOOR_SCHEMA`.
- `grill.PRODUCTS` (the two products) -> instruct loading the `grilling` skill; keep the live material
  (the ask and the resolved Q&A) AND the delta-markdown grammar (`## ADDED|MODIFIED|REMOVED|RENAMED --
  <capability>` over `### Requirement:` / `#### Scenario:` blocks) inline -- that grammar is the
  structured output format the engine parses, not a methodology restatement, so it stays; keep
  `PRODUCTS_SCHEMA`.
- `design.SELECT` (the contest selection) -> instruct loading the `design-it-twice` skill; keep the live
  material (the candidate designs stay inline); keep `SELECT_SCHEMA`. The DEPTH / LOCALITY / SEAM
  PLACEMENT axes move wholly to the skill, which single-sources them.

The reply envelopes (`SYSTEM_SCHEMA`, `COHERENCE_SCHEMA`, `EXPLAIN_SCHEMA`, `FLOOR_SCHEMA`,
`PRODUCTS_SCHEMA`, `SELECT_SCHEMA`) are UNTOUCHED -- the world fixtures depend on them verbatim.
`design.CANDIDATE` and `design.BRIEFS` are OUT OF SCOPE: the candidate briefing and the brief set are
live per-episode material, not a methodology restatement.

The red->green oracle lives in `engine/check/scenarios.py`, watched-from-outside, the prompt-construction
pattern of its existing sections 5 / 7b / 7c (a prompt-string fact no domain verb can express without
naming the prompt, so it is asserted from outside, never as a faked in-spec block):
- REPLACE the section-5 assertion `all(ax in design.SELECT for ax in ("DEPTH","LOCALITY","SEAM
  PLACEMENT"))` -- the axes no longer live in the prompt -- with an assertion that `design.SELECT` routes
  to the `design-it-twice` skill (it names "design-it-twice" and instructs loading the skill) AND that
  the rendered `design-it-twice` skill still carries the three axes (single-sourced there, via
  `methodology.skill("design-it-twice", REAL)`).
- ADD a writing-for-the-machine assertion that each of the six prompts -- `communication.SYSTEM`,
  `communication.COHERENCE`, `communication.EXPLAIN`, `grill.FLOOR`, `grill.PRODUCTS`, `design.SELECT` --
  names and instructs loading its corresponding skill. These assertions are RED on current main (the
  prompts restate the methodology and name no skill) and GREEN after the build; `python3 -m engine
  --check` is the loop.

The change folds when: every per-episode architect prompt names and instructs loading its corresponding
skill and restates none of the methodology that skill single-sources; every reply envelope is intact
(the `*_SCHEMA` constants and their rendered instruction unchanged); the watched oracle in
`scenarios.py` goes red->green; and `python3 -m engine --check` is green. ("Restates none of the
methodology" is the watched judgment the architect attests at the archive gate.)

[DELTA]
# delta -- the architect's per-episode prompt loads its skill, never restates it

## ADDED -- writing-for-the-machine

### Requirement: the architect's per-episode prompt routes to its skill, never restating it
Each per-episode prompt the architect runs MUST instruct the model to load the one skill that
single-sources its method, and MUST carry no hand-authored restatement of that skill's methodology. The
prompt carries only the live per-episode task and material -- the living-spec digest, the contract, the
worker's report, the card, the ask and its resolved answers, the candidate designs -- together with the
structured reply envelope the transport reads, so the methodology stays the skill's alone and the prompt
cannot drift from the spec the way a second copy does. The architect runs as Claude Code, which discovers
`.claude/skills/` natively, so the load resolves on the architect's own transport; the worker's
skill-load stays watched evidence on its own node. The prompts this binds are `communication`'s operator
turn, coherence judgment, and explain story; `grilling`'s floor and products; and `design-it-twice`'s
selection.

#### Scenario: an architect prompt is authored
- WHEN a per-episode architect prompt -- the operator turn, the coherence judgment, the explain story,
  the grilling floor, the grilling products, or the design-it-twice selection -- is authored or reviewed
- THEN it names and instructs loading its corresponding skill, restates none of the methodology that
  skill single-sources, and still renders the structured reply envelope the transport reads -- so the
  skill is the one source and the prompt carries only the live task and material
