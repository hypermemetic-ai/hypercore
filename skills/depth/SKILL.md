---
name: depth
description: hypercore's depth disciplines — build deep modules (a lot of behavior behind a small interface) and avoid the red flags of shallowness. Load when designing, building, or refining a module's interface or implementation.
---

# Depth — build deep modules

You are held to these standing disciplines; build deep up front so your work folds without tripping the depth gate.

## Build toward these — the design principles

- Complexity is incremental — sweat the small stuff.
- Working code is not enough — strategic beats tactical.
- Make continual small investments to improve system design.
- Modules should be deep.
- Interfaces should make the common case simple.
- It is more important for a module to have a simple interface than a simple implementation.
- General-purpose modules are deeper.
- Separate general-purpose and special-purpose code.
- Different layers should have different abstractions.
- Pull complexity downward.
- Define errors (and special cases) out of existence.
- Design it twice.
- Comments should describe things that are not obvious from the code.
- Software should be designed for ease of reading, not ease of writing.
- The increments of software development should be abstractions, not features.

## Build away from these — the red flags of shallowness

- Shallow module — the interface is complicated relative to the functionality it provides.
- Information leakage — the same knowledge appears in multiple places.
- Temporal decomposition — code structure mirrors the execution-time order, so knowledge gets split across the stages that happen to touch it.
- Overexposure — using a common feature forces the caller to learn about rarely-used ones.
- Pass-through method — a method that does nothing but forward its arguments to another with nearly the same signature.
- Repetition — the same (or nearly the same) code appears over and over.
- Special-general mixture — special-purpose code embedded in a general-purpose mechanism, coupling the two.
- Conjoined methods — two methods so entwined you cannot understand one without reading the other. (The debate's PrimeGenerator turns on this — §5.)
- Comment repeats code — the comment says what the adjacent code already plainly says.
- Implementation documentation contaminates interface — interface docs forced to expose implementation details a user does not need.
- Vague name — a name too broad to carry specific information.
- Hard to pick name — difficulty naming a thing cleanly signals the thing itself is not cleanly defined.
- Hard to describe — difficulty writing a short complete comment signals a design problem, not a writing one.
- Nonobvious code — its behavior cannot be grasped in a quick read.

## Going deeper

The full synthesis — the reasoning behind each discipline, the *Clean Code* contrast, and the epistemic status — is `research/aposd.md`, this skill's single source.
