# folding-conditions

The conditions a graph's material must meet to fold — the engineering disciplines made
structural (rebuild-spec §7). The self-model owns the delta and the atomic merge; this
capability owns the gates on the material a worker produced, run at the archive stage
before the merge. Advice can be ignored; a folding condition cannot, so the disciplines
bite by construction rather than by a reviewer remembering them. An unmet condition refuses
the fold and returns a decision — re-cut, fix the loop, deepen the module — never a silent
pass.

### Requirement: a behavior-changing graph cannot fold without a recorded red→green loop
A graph that carries a non-trivial delta MUST hand back a feedback-loop record — the
invocation that drives the behavior, the failing (red) verdict on that behavior before the
fix, and the passing (green) verdict after it. A missing or incomplete record refuses the
fold. The feedback loop is the skill; a correct narrative with no harness is the failure
this kills. A trivial graph changes no behavior and needs none.

#### Scenario: a fix without a loop
- WHEN a behavior-changing graph hands back a result whose loop record lacks the invocation
  or the red or the green verdict
- THEN the fold is refused, a decision is returned, and the spec is left untouched

#### Scenario: a recorded loop
- WHEN the result records the loop's invocation, its red verdict on the behavior, and its
  green verdict after the fix
- THEN the feedback-loop condition is met and the fold may proceed

### Requirement: a graph cannot fold a source file over the line-count budget
A graph MUST NOT fold if any source file it created or grew crosses the line-count budget
without a decision record justifying it. The budget is a low tripwire keyed to the context a
module costs a worker to load — its length — not a law; crossing it is allowed only with a
recorded decision, so a god-file cannot re-accrete one quiet edit at a time. The condition is
scoped to the files the graph itself touched.

#### Scenario: a graph grows a god-file
- WHEN a graph's material adds or grows a source file past the budget and no decision names it
- THEN the fold is refused and a decision is returned

#### Scenario: a justified exception
- WHEN a source file over the budget is named in a decision record justifying its size
- THEN the budget condition is met for that file and the fold may proceed
