# depth

hypercore's standing engineering discipline: build **deep modules** — a lot of behavior behind a
small interface — and build away from the **red flags** of shallowness. Imported from Ousterhout's
*A Philosophy of Software Design* and adopted as the criterion the system's structure is read in,
exactly as `design-it-twice` imports the same source (ADR 0007). The full synthesis — the reasoning
behind each discipline, the *Clean Code* contrast, the epistemic status — is provenance, cited not
inlined (`work/archive/depth-regrounding/depth-synthesis.md`). The worker is held to these every
episode so it builds deep up front, while the `folding-conditions` gate keeps a length tripwire and
`architecture-review` carries the red flags as standing judgment — advice made into a discipline,
because advice can be ignored and a discipline in the spec cannot. The load-bearing claim: a simple
interface matters more than a simple implementation, because the interface is paid by every caller
forever while the implementation is paid once — so when something must be hard, make it hard inside.

### Requirement: modules are deep — much behavior behind a small interface
A module MUST hide far more than it exposes — a powerful implementation under a simple interface,
its depth the ratio of the two. A **shallow module**, whose interface is nearly as complex as the
implementation it fronts (the limiting case a method that only forwards its arguments), is the #1
red flag: it costs the reader almost as much as no module at all. Complexity is pulled **downward** —
a simple interface is worth more than a simple implementation.

#### Scenario: a module is judged on depth
- WHEN a module is built or reviewed
- THEN it is weighed by how much it hides behind how small an interface, and a shallow one is
  surfaced as the primary red flag, never excused by being short

### Requirement: information is hidden, not leaked
A module MUST encapsulate a design decision — a format, a structure, an algorithm — that nothing
outside needs to know. The same knowledge living in two places that must change together
(**information leakage**, the gravest red flag after shallowness) is designed out, and its commonest
cause, **temporal decomposition** (structuring code by the order operations happen rather than the
knowledge each needs), is avoided: decompose by knowledge, not by time. General-purpose modules are
deeper than special-purpose ones, and adjacent layers carry different abstractions — a layer that
restates its neighbour is a pass-through doing nothing.

#### Scenario: a design decision is encapsulated
- WHEN a piece of knowledge — a format, an order, a structure — is needed in the system
- THEN it lives in exactly one module, and a structure that splits it across stages or leaks it to
  callers is reworked toward decomposition-by-knowledge

### Requirement: the build is strategic, not tactical
The worker MUST treat working code as not enough: the goal is a design that keeps the system cheap
to change, produced as a continual small **investment** in structure rather than the next feature
hacked to work. Tactical accretion — each change adding a little complexity judged not worth fixing
now — is the disease the discipline resists; the increments of progress are clean abstractions, not
features made to pass.

#### Scenario: a worker builds behind the loop
- WHEN a worker carries out an ask
- THEN it builds deep up front — investing in the abstraction, not only passing the check — so the
  result folds without tripping the depth gate, which stays a rarely-tripped backstop

### Requirement: errors are defined out of existence
A design MUST reduce the number of places that have to reason about an exception, not multiply them:
where it can, redefine the operation so the exceptional case is not exceptional (the normal case
already covers it), or mask the error low in the stack, or aggregate handling in one place. The count
of sites that must handle an error is a design variable, not a given.

#### Scenario: a special case appears
- WHEN a design meets a special or error case
- THEN the first move is to define it out of existence rather than add another handler, so the
  interface every caller pays does not grow an exception it need not

### Requirement: the disciplines are smells a reader judges, not thresholds a tool measures
The red flags MUST be carried as **judgment**, not numbers — shallow module, information leakage,
temporal decomposition, overexposure, pass-through method, repetition, special-general mixture,
conjoined methods, comment-repeats-code, vague or hard-to-pick name, nonobvious code — each a symptom
a judge weighs, none a threshold a tool checks. The system keeps at most a **length** tripwire (a
context-cost signal that raises a depth decision, never an auto-refusal); the model-driven red-flag
scan lives in `architecture-review`, recorded as not-yet-built, never fabricated.

#### Scenario: depth is assessed
- WHEN a module's depth is assessed at the gate or in the review
- THEN length raises a decision but never a verdict, and the red flags are weighed as judgment — so
  the operator reads depth, not a line count
