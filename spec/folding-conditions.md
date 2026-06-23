# folding-conditions

The conditions a tree's material must meet to fold — the engineering standards made
structural. The self-model owns the delta and the atomic merge; this
capability owns the gates on the material a worker produced, run at the archive stage
before the merge. Advice can be ignored; a folding condition cannot, so the standards
bite by construction rather than by a reviewer remembering them.

Two of the conditions are **non-negotiable facts** — the delta applies, and a
behavior-changing tree carries a recorded red→green loop — and they auto-refuse the fold.
The third is a **judgment**: **depth** is the criterion (a deep module, a lot of behavior
behind a small interface — re-grounded in Ousterhout, ADR 0006), and
**length** is one signal of it, never the criterion. So the depth condition does not
auto-refuse on length; it raises a **decision** — re-cut, deepen, or accept-with-reason —
held on the operator's queue. An unmet fact refuses the fold and returns its reason; the
depth condition returns a decision; never a silent pass.

### Requirement: a behavior-changing tree cannot fold without a recorded red→green loop
A tree that carries a non-trivial delta MUST hand back a feedback-loop record naming the
invocation that drives the behavior. A missing or incomplete record refuses the fold. A
trivial tree changes no behavior and needs none.

#### Scenario: a fix without a loop
- WHEN a behavior-changing tree hands back a result whose loop record lacks the invocation
  or the red or the green verdict
- THEN the fold is refused, a decision is returned, and the spec is left untouched

### Requirement: the recorded loop is executed, not trusted as narration
The gate MUST **run** the recorded command in the fence and require a real red→green
transition, never trust the loop's words. The command is executed against the fork base and
the tip: it MUST fail at the base (red — the behavior was not yet built) and pass at the tip
(green — the fix works), and identical or absent verdicts are no transition. The feedback
loop is the skill; a correct narrative with no executed harness is the failure this kills —
so a fabricated loop whose words say it passed, or that it never ran, cannot fold, because
the exit codes are the gate, not the strings.

#### Scenario: a loop that is executed and transitions
- WHEN the result records a command that fails at the fork base and passes at the tip
- THEN the gate runs it, observes the red→green transition, and the feedback-loop condition
  is met

#### Scenario: a fabricated loop that did not run
- WHEN the result records a loop whose command does not make the red→green transition — it
  passes at the base, fails at the tip, cannot run, or names identical red and green verdicts
- THEN the gate runs the command, observes no transition, and refuses the fold — the loop's
  narration is never the gate

### Requirement: length past the signal raises a decision, never a silent refusal
A source file a tree created or grew past the **length signal** MUST raise a **decision** —
re-cut, deepen, or accept-with-reason — held on the operator's queue. It MUST NOT
auto-refuse on length and MUST NOT silently pass. Length is a context-cost signal — every line
is context an agent must load — not a verdict on depth, and there is **no hard length ceiling**:
even a far-over-signal file raises a decision the operator can accept, never an outright
refusal (a number standing in for the judgment of depth is the error being removed). The fold
is held until the decision is settled, and an **accepted-length record**
accepting the file lets it fold. The condition is scoped to the files the tree itself touched.

#### Scenario: a tree grows a module past the signal
- WHEN a tree's material adds or grows a source file past the length signal and no
  accepted-length record accepts it
- THEN a decision (re-cut / deepen / accept-with-reason) is raised, the fold is held, and
  the spec is left untouched — never a silent refusal and never a silent pass

#### Scenario: an accepted-length record accepts the length
- WHEN an accepted-length record names the file as accepted **at a stated length** and
  the file is still within that length
- THEN the depth condition is met for that file and the fold may proceed

#### Scenario: a coincidental mention is not an exception
- WHEN a decision record merely mentions the file in prose, with no accepted-length record
  accepting it
- THEN the file is not cleared and the decision still stands — the exception is the
  decision, not the spelling, so a coincidental mention grants no free pass

### Requirement: an accepted length is bounded to the length it names, and ratchets
An accepted-length record MUST accept a file **at a stated length** (`@<N>`), and that
acceptance is bounded to it: it clears the gate only while the file stays within the accepted
length plus a small **materiality margin**, so a one-line edit past the bar does not re-open a
settled decision. A file that grows **materially past** the length it was accepted at MUST re-raise
the decision — acceptance ratchets, it does not silence later growth — and renewing the
acceptance at the new length raises the bar. A stable or shrinking file stays cleared; the bar
lives in the record, so a shrink never lowers it. A record with **no stated length** (no `@<N>`)
names no bound and MUST NOT clear the gate — the exception is the decision *at a stated size*, not
the spelling. When several records name one file, the highest accepted length governs (the ratchet
only rises).

#### Scenario: an accepted file grows materially past its bar
- WHEN a file an accepted-length record accepted at length N grows materially past N (beyond the margin)
- THEN the decision is re-raised at the new length and the fold is held until it is renewed —
  the old acceptance does not silence the growth

#### Scenario: an accepted file stays within its bar, or shrinks
- WHEN a file an accepted-length record accepted at length N is touched but stays within N (plus the
  margin), or shrinks
- THEN it stays cleared and raises no new decision — no nagging on a stable file

#### Scenario: a record with no stated length names no bound
- WHEN an accepted-length record names the file with no `@<N>`
- THEN it does not clear the gate — an acceptance must name the length it is bounded to

### Requirement: the standards declare gated or watched, machine-readably
The system MUST carry a **machine-readable classification** of every standard, each declared either
**gated** — a check fails unless the standard actually happened — or **watched** — the operator
watches it, no check gates it because the judgment lives on the model side. The classification exists
so a regenerating author cannot mistake advice for a gate: a scripted transport is licensed only for
behavior the engine computes deterministically; any model-side judgment a check cannot drive against
an adversarial fixture is declared *watched, not gated*, never scripted-and-called-tested. Each entry
is a parseable line — `standard: <standard> — <gated|watched> — <how>` — so a check reads the
classification rather than trusting prose. A standard declared *gated* MUST have a real gate behind
it; one declared *watched* is honestly recorded as not mechanically enforced.

The standards, as they stand (the honest classification the research established):

- standard: delta-applies — gated — `delta.check` parses the delta against the live spec; a mismatch refuses
- standard: red-green-loop — gated — `conditions._feedback_loop` executes the command in the fence and requires a real red→green transition
- standard: length-ratchet — gated — `conditions.accepted`/`accepted_at` bound an accepted length and re-raise on material growth
- standard: mechanical-red-flags — gated — `review.red_flags` scans for dead module-level symbols and circular dependencies
- standard: module-depth-judgment — watched — the model-driven shallow/leakage/deletion-test judgment is not yet built (ADR 0006); length raises a decision, never a verdict
- standard: coherence — watched — the architect's archive-gate judgment is the model's; the incoherent→decision *branch* is exercised, but whether a result truly honors the contract is watched, not gated
- standard: grilling-floor — watched — whether the floor surfaced the right stakes is the model's judgment; the harness drives the routing, not the finding
- standard: design-it-twice-selection — watched — whether the deepest candidate was picked is the model's judgment; the fences and the ADR record are gated, the pick is watched

#### Scenario: a standard is classified
- WHEN the classification is read for a standard
- THEN it declares the standard gated or watched on a parseable line, so a check can read the
  classification and a regenerating author cannot script a watched judgment and call it gated

#### Scenario: a gated standard has a real gate
- WHEN the classification declares a standard gated
- THEN a check fails unless the standard actually happened — the gate is real, not a presence-of-
  strings check — and a watched standard is honestly recorded as not mechanically enforced
