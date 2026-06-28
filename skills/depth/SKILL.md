---
name: depth
description: hypercore's depth standards — build deep modules (a lot of behavior behind a small interface) and avoid the red flags of shallowness. Load when designing, building, or refining a module's interface or implementation.
---

# depth

hypercore's standing engineering discipline: build **deep modules** — a lot of behavior behind a
small interface — and build away from the **red flags** of shallowness. Imported from Ousterhout's
*A Philosophy of Software Design* and adopted as the criterion the system's structure is read in,
exactly as `design-it-twice` imports the same source. The full synthesis — the reasoning
behind each discipline, the *Clean Code* contrast, the epistemic status — is provenance, cited not
inlined (`work/archive/depth-regrounding/depth-synthesis.md`). The worker is held to these every
episode so it builds deep up front, while the `folding-conditions` gate keeps a length tripwire and
`architecture-review` carries the red flags as standing judgment — advice made into a discipline,
because advice can be ignored and a discipline in the spec cannot. The load-bearing claim: a simple
interface matters more than a simple implementation, because the interface is paid by every caller
forever while the implementation is paid once — so when something must be hard, make it hard inside.

**Depth is a decision the gate raises, never a threshold it enforces.** Nothing in the system scores
or certifies depth: the only mechanical facts are length (a context-cost signal that raises a
decision) and the structural red flags a tool can read (dead symbols, circular dependencies). The
model-driven verdict — is this module actually shallow? — is **built as a watched depth scan**
(`architecture-review`, `engine/depth_scan.py`): it raises a finding for a judge, never a score and never
a gate. So "the depth gate" is honest only as *length raises a decision the operator settles*; it is not
a depth threshold a rebuild can pass by shipping short, shallow modules. The proactive defense is the
worker building deep up front, not a backstop that measures depth — the watched scan judges, it does not
certify, so there is no depth gate to lean on. The spec says so plainly precisely so a regenerating
author does not assume a gate that does not exist.

## The disciplines — what good looks like

- **modules are deep — much behavior behind a small interface** — A module MUST hide far more than it exposes — a powerful implementation under a simple interface, its depth the ratio of the two. A **shallow module**, whose interface is nearly as complex as the implementation it fronts (the limiting case a method that only forwards its arguments), is the #1 red flag: it costs the reader almost as much as no module at all. Complexity is pulled **downward** — a simple interface is worth more than a simple implementation.
- **information is hidden, not leaked** — A module MUST encapsulate a decision — a format, a structure, an algorithm — that nothing outside needs to know. The same knowledge living in two places that must change together (**information leakage**, the gravest red flag after shallowness) is designed out, and its commonest cause, **temporal decomposition** (structuring code by the order operations happen rather than the knowledge each needs), is avoided: decompose by knowledge, not by time. General-purpose modules are deeper than special-purpose ones, and adjacent layers carry different abstractions — a layer that restates its neighbour is a pass-through doing nothing.
- **the build is strategic, not tactical** — The worker MUST treat working code as not enough: the goal is a design that keeps the system cheap to change, produced as a continual small **investment** in structure rather than the next feature hacked to work. Tactical accretion — each change adding a little complexity judged not worth fixing now — is the disease the discipline resists; the increments of progress are clean abstractions, not features made to pass.
- **errors are defined out of existence** — A design MUST reduce the number of places that have to reason about an exception, not multiply them: where it can, redefine the operation so the exceptional case is not exceptional (the normal case already covers it), or mask the error low in the stack, or aggregate handling in one place. The count of sites that must handle an error is a design variable, not a given.
- **the disciplines are smells a reader judges, not thresholds a tool measures** — The red flags MUST be carried as **judgment**, not numbers — shallow module, information leakage, temporal decomposition, overexposure, pass-through method, repetition, special-general mixture, conjoined methods, comment-repeats-code, vague or hard-to-pick name, nonobvious code — each a symptom a judge weighs, none a threshold a tool checks. The system keeps at most a **length** tripwire — a context-cost signal that raises a decision, not an auto-refusal. The model-driven red-flag scan lives in `architecture-review`, built as a watched scan, never fabricated.

## Going deeper

The full requirements and their scenarios are `spec/depth.md`, this skill's single source.
