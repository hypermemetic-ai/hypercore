# self-model

The system's maintained model of itself, rendered two ways: the **living spec**
for the agent and the **operator view** for the operator. One model, kept current
as a byproduct of folding, never as a separate decision.

### Requirement: the living spec is as-built reality, organized by capability
The living spec MUST describe what the system actually does, segmented by
capability, and read flat by the agent. It is not `intent.md` (what is wanted); the
gap between them is the backlog.

#### Scenario: reading the spec
- WHEN the spec is read
- THEN it yields the glossary and, per capability, that capability's requirements
  and their scenarios — concise enough to scan across all of them at once

### Requirement: every behavior-changing graph carries a delta
A graph that changes behavior MUST carry a delta of ADDED / MODIFIED / REMOVED
requirements matching what it built. A graph that makes no behavior change carries
an empty delta and says so.

#### Scenario: a trivial graph
- WHEN a graph changes no behavior
- THEN it carries a delta that declares itself trivial, and folding it applies nothing

### Requirement: a missing or mismatched delta cannot fold
Folding MUST refuse a behavior-changing graph that carries no delta, and refuse a
delta that does not apply cleanly to the current spec.

#### Scenario: missing delta
- WHEN a behavior-changing graph carries no delta file
- THEN the fold is refused

#### Scenario: mismatched delta
- WHEN a delta MODIFIES or REMOVES a requirement that is absent, or ADDS one that
  already exists
- THEN the fold is refused and the spec is left untouched

### Requirement: folding applies the delta to the spec, atomically, both directions
The act that folds a graph MUST apply its delta to the living spec and re-render the
operator view. The spec is never merged unless the graph folds, and the graph never
folds unless the delta merges; the living spec is therefore never separately edited.

#### Scenario: an added requirement lands
- WHEN a graph with an ADDED requirement folds
- THEN that requirement is present in the capability's spec file and committed in the
  same act

#### Scenario: a fold grows a new capability
- WHEN a delta ADDS a requirement in a capability that does not yet exist
- THEN the fold creates that capability and the operator view gains it as a top-level
  unit; a MODIFIED or REMOVED requirement in an absent capability still cannot fold

### Requirement: the operator view renders vision beside as-built and gap
The operator view MUST render, at every altitude, the **vision** (authored, from
`intent.md`) beside the **as-built** (derived from the living spec) and the **gap**
between them, as a recursive tree to the depth the work reaches. The upper levels'
"what the system is" structural map and the deepening backlog are the standing output
of the architecture review (`architecture-review` capability), kept honest between folds.
The map renders the system's **depth**, not merely its length: length is shown as a
context-cost signal against the threshold, and the deeper model-driven red-flag depth
assessment is recorded as not-yet-built (rebuild-spec §7.4, ADR 0006), never fabricated —
so the operator reads depth, not just a line count.

#### Scenario: the view is read
- WHEN the operator opens the view
- THEN it shows the vision, the as-built capabilities and their requirements, and the
  gap; drilling into a capability zooms the same three to that grain

#### Scenario: the root's upper levels
- WHEN the operator opens the root of the view
- THEN its structural map of as-built reality and its deepening backlog are the
  architecture review's standing output, derived from the scan, not hand-authored

### Requirement: the as-built and gap are derived; only the vision is authored
No statement in the as-built or gap renders MUST be hand-authored or hand-maintained
as prose; each is a render of the model and changes when the model changes. The
vision they sit beside is the one writable region.

#### Scenario: the model changes
- WHEN a delta folds into the spec
- THEN the as-built and gap renders change in the same act, with nothing hand-edited
