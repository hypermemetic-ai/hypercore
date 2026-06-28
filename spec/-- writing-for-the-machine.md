# -- writing-for-the-machine

### Requirement: the architect's per-episode prompt routes to its skill, never restating it
Each per-episode prompt the architect runs MUST instruct the model to load the one skill that
single-sources its method. The prompt MUST carry no hand-authored restatement of that skill's
methodology. It carries only the live per-episode task and material -- the living-spec digest, the
contract, the worker's report, the card, the ask and resolved answers, and the candidate designs --
together with the structured reply envelope the transport reads. The architect runs as Claude Code,
which discovers `.claude/skills/` natively, so naming the skill is the load path. The worker's
skill-load stays watched evidence on its own node. The bound architect prompts are communication's
operator turn, coherence judgment, explain story, grilling floor, grilling products, and
design-it-twice selection.

#### Scenario: an architect prompt is authored
- WHEN a per-episode architect prompt -- the operator turn, the coherence judgment, the explain story,
  the grilling floor, the grilling products, or the design-it-twice selection -- is authored or reviewed
- THEN it names and instructs loading its corresponding skill, restates none of the methodology that
  skill single-sources, and still renders the structured reply envelope the transport reads -- so the
  skill is the one source and the prompt carries only the live task and material
