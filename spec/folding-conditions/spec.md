# folding-conditions

The conditions a graph's material must meet to fold — the engineering disciplines made
structural (rebuild-spec §7). The self-model owns the delta and the atomic merge; this
capability owns the gates on the material a worker produced, run at the archive stage
before the merge. Advice can be ignored; a folding condition cannot, so the disciplines
bite by construction rather than by a reviewer remembering them.

Two of the conditions are **non-negotiable facts** — the delta applies, and a
behavior-changing graph carries a recorded red→green loop — and they auto-refuse the fold.
The third is a **judgment**: **depth** is the criterion (a deep module, a lot of behavior
behind a small interface — rebuild-spec §7.1, re-grounded in Ousterhout, ADR 0006), and
**length** is one signal of it, never the criterion. So the depth condition does not
auto-refuse on length; it raises a **decision** — re-cut, deepen, or accept-with-reason —
held on the operator's queue. An unmet fact refuses the fold and returns its reason; the
depth condition returns a decision; never a silent pass.

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

### Requirement: length past the signal raises a depth decision, never a silent refusal
A source file a graph created or grew past the **length signal** MUST raise a **depth
decision** — re-cut, deepen, or accept-with-reason — held on the operator's queue. It MUST NOT
auto-refuse on length and MUST NOT silently pass. Length is a context-cost signal — every line
is context an agent must load — not a depth verdict, and there is **no hard length ceiling**:
even a far-over-signal file raises a decision the operator can accept, never an outright
refusal (a number standing in for the judgment of depth is the error being removed). The fold
is held until the depth decision is settled, and a **structured depth-decision record**
accepting the file lets it fold. The condition is scoped to the files the graph itself touched.

#### Scenario: a graph grows a module past the signal
- WHEN a graph's material adds or grows a source file past the length signal and no structured
  depth-decision accepts it
- THEN a depth decision (re-cut / deepen / accept-with-reason) is raised, the fold is held, and
  the spec is left untouched — never a silent refusal and never a silent pass

#### Scenario: a depth-decision accepts the length
- WHEN a structured depth-decision record names the file as accepted past the signal
- THEN the depth condition is met for that file and the fold may proceed

#### Scenario: a coincidental mention is not an exception
- WHEN a decision record merely mentions the file in prose, with no structured depth-decision
  accepting it
- THEN the file is not cleared and the depth decision still stands — the exception is the
  decision, not the spelling, so a coincidental mention grants no free pass
