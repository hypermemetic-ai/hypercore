# self-model
<!-- vision: model of the system, state at a glance, source of truth, self-model, as-built -->

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

  ```check
  read spec
  self-hosts
  covered
  ```

### Requirement: the living spec is self-verifying — a scenario is the executable check of its requirement
A capability's `#### Scenario:` MUST be able to carry the **executable check** of its requirement, not
only describe it: the architect authors the scenario in domain verbs, a deep binding (`scenario`)
compiles it to a runnable assertion over the real engine seams, and the gate runs it red→green. Because
the self-model's own account of a behavior *is* the check that behavior passes, the description cannot
drift from the behavior — a requirement is a check that survives its node. The presence of the check
block is itself the gated/watched classification, not a separately authored register. A requirement
whose scenarios carry no check block is **watched** — recorded honestly as not mechanically enforced,
never faked. The binding is a hidden deep layer; the scenario stays the high-signal WHEN/THEN interface.

#### Scenario: a scenario is read as a check
- WHEN a capability's scenario carries an executable check block
- THEN it both reads as the requirement's WHEN/THEN and runs as its gate — green when the system meets
  it now, and red→green across the fork base and tip when a change builds the behavior

#### Scenario: a scenario with no check block is watched
- WHEN a requirement's scenarios carry no check block
- THEN the requirement is watched — model judgment no fixture certifies — recorded honestly as not
  mechanically gated, never scripted-and-called-tested

### Requirement: every behavior-changing tree carries a delta
A tree that changes behavior MUST carry a delta of ADDED / MODIFIED / REMOVED / RENAMED
requirements matching what it built. ADDED introduces a requirement; MODIFIED replaces the body and
scenarios of a requirement matched by its title; REMOVED drops one matched by its title; RENAMED
changes a requirement's title — its identity — leaving the body and scenarios untouched. A scope-broadening
retitle is a RENAMED paired with a MODIFIED keyed on the new title, because renames resolve first within
one delta. A tree that makes no behavior change carries an empty delta and says so.

#### Scenario: a trivial tree
- WHEN a tree changes no behavior
- THEN it carries a delta that declares itself trivial, and folding it applies nothing

  ```check
  fold trivial
  unchanged
  ```

### Requirement: a missing or mismatched delta cannot fold
Folding MUST refuse a behavior-changing tree that carries no delta, and refuse a delta that does not
apply cleanly to the current spec. A MODIFIED or REMOVED of an absent requirement, an ADDED of one that
already exists with different content, a RENAMED of an absent old title, and a RENAMED onto a title that
already exists all fail to apply and leave the spec untouched. A re-applied RENAMED — old gone, new
present — is the idempotent retry, so a crash-interrupted fold can complete.

#### Scenario: missing delta
- WHEN a behavior-changing tree carries no delta file
- THEN the fold is refused

  ```check
  fold missing
  refused
  ```

#### Scenario: mismatched delta
- WHEN a delta MODIFIES or REMOVES a requirement that is absent, or ADDS one that
  already exists with different content
- THEN the fold is refused and the spec is left untouched

  ```check
  fold mismatched
  refused
  untouched
  ```

#### Scenario: an unfoldable rename
- WHEN a delta RENAMES a requirement whose old title is absent, or onto a title that already exists
- THEN the fold is refused and the spec is left untouched

  ```check
  fold rename-absent
  refused
  untouched
  fold rename-collision
  refused
  untouched
  ```

### Requirement: folding applies the delta to the spec, atomically, both directions
The act that folds a tree MUST apply its delta to the living spec, re-render the derived
artifacts, and archive the node — **in one commit**. The spec change and the node's archive
land together or not at all: a crash can never leave the spec merged while the node is
un-archived, nor the reverse. The spec merges exactly when the tree folds, and the tree
folds exactly when the delta merges; the living spec is therefore never separately edited.
The act is **idempotently retryable**: a retry after a crash that landed the spec change on
disk but did not commit completes the fold — it does not refuse the already-applied delta as
a conflict.

#### Scenario: an added requirement lands
- WHEN a tree with an ADDED requirement folds
- THEN that requirement is present in the capability's spec file and the node is archived,
  both committed in the same single act

  ```check
  fold added
  landed
  archived
  atomic
  ```

#### Scenario: a requirement is renamed in place
- WHEN a delta RENAMES a requirement (old title → new title)
- THEN the requirement is present under the new title with its body and scenarios intact, the old
  title is gone, and the node is archived — all in the same one atomic act

  ```check
  fold renamed
  retitled
  archived
  atomic
  ```

#### Scenario: a rename paired with a modify
- WHEN a delta RENAMES a requirement and, in the same delta, MODIFIES it keyed on the new title
- THEN the renames resolve first so the modify finds its target, and the requirement lands under the
  new title carrying the modified body

  ```check
  fold renamed-modified
  retitled
  remodeled
  ```

#### Scenario: a crash mid-fold is retried
- WHEN a fold is interrupted after the spec change lands on disk but before it commits, and
  the fold is retried
- THEN the retry completes — the requirement is present exactly once and the node is
  archived — rather than wedging on a permanent already-exists refusal

  ```check
  fold crash
  half-applied
  fold retry
  landed once
  archived
  ```

#### Scenario: a fold grows a new capability
- WHEN a delta ADDS a requirement in a capability that does not yet exist
- THEN the fold creates that capability and the operator view gains it as a top-level
  unit; a MODIFIED or REMOVED requirement in an absent capability still cannot fold

  ```check
  fold newcap
  grew
  read view
  gained
  fold mismatched
  refused
  ```

### Requirement: folding lands the verified build's code on the merged tree, not only its spec
The act that folds a **code-bearing** tree MUST land the worker's **verified engine code** on main —
not only its spec delta — in the **same one commit** that applies the delta and archives the node, so a
code-bearing ask completes through the crossing without leaving main red or the node falsely archived.
The code crosses as a self-contained artifact captured at the worker's hand-off — the fence's verified
bytes for the engine paths it touched — content-replayed into the fold's one held act; no live fence is
reached at fold time. Before the commit, **every capability's scenarios are re-verified on the merged
tree — the whole system, not only the capabilities the delta names**: the worker's code can reach a
shared engine module (`tree`, `delta`, `record`, `scenario`) that an **unnamed** capability depends on,
so re-verifying only the touched capabilities would let a shared-module change break an untouched one and
still land `done`. What is verified is the merged main itself, so green-in-fence can no longer mean
red-on-main, and green-on-the-touched-capability can no longer mean red-on-the-system — a build that does
not hold once merged, anywhere a full check would catch it, is refused, every write rolled back, nothing
landing, the node recovering to a decision. The whole-system reach is **structural**: the re-verify
enumerates the capabilities itself, so no caller can narrow it. The in-fence red→green **scenario gate**
stays scoped to the touched capabilities — only a capability the change builds transitions — while the
re-verify is the whole-system check the gate's scope cannot be. A **staleness pre-check** fast-refuses,
before any write, a build whose engine paths main has moved under since the fence was cut — a decision to
re-cut off current main, never a silent clobber. None of these is a new commit, lock, or transaction;
they ride the one held line the spec fold already runs on. A spec-only (trivial or no-code) fold carries
no code and runs none of them — its act is exactly as before.

#### Scenario: a code-bearing delta's implementation reaches main
- WHEN a tree whose worker built and verified engine code in its fence folds
- THEN that engine code lands on main in the same one commit as the spec delta and the node's archive,
  re-verified green on the merged tree before the commit; a build red once merged, or one whose paths
  main has moved under, is refused and nothing lands
- watched — proven from outside in `engine/check/build_reaches_main.py`, never from inside the fold it
  tests (the self-reference the scenario gate's own red→green has, and the same honest home)

#### Scenario: a shared-module change that breaks an untouched capability is refused
- WHEN a code-bearing fold's delta names one capability but its engine code breaks a *different*
  capability the delta never named — a refactor of a shared module an unnamed capability depends on
- THEN re-verifying the whole system on the merged tree catches the untouched capability red, the fold
  is refused, every write rolled back, nothing landing, the node recovering to a decision — the
  crossing's verdict is green-on-the-system, never green-on-the-touched-capability alone
- watched — proven from outside in `engine/check/build_reaches_main.py`, the keystone that cannot
  certify itself from inside a fold

### Requirement: the operator view renders vision beside as-built and gap
The operator view MUST render, at every altitude, the **vision** (authored, from
`intent.md`) beside the **as-built** (derived from the living spec) and the **gap**
between them, as a recursive tree to the depth the work reaches. The upper levels'
"what the system is" structural map and the complexity debt are the standing output
of the architecture review (`architecture-review` capability), kept honest between folds.
The map renders the system's **depth**, not merely its length: length is shown as a
context-cost signal against the threshold, and the deeper model-driven red-flag depth
assessment is recorded as not-yet-built, never fabricated —
so the operator reads depth, not just a line count.

#### Scenario: the view is read
- WHEN the operator opens the view
- THEN it shows the vision, the as-built capabilities and their requirements, and the
  gap; drilling into a capability zooms the same three to that grain

  ```check
  read view
  vision present
  asbuilt
  gap
  ```

#### Scenario: a capability's vision is a declared binding
- WHEN the view slices the vision per capability
- THEN it reads the intent each capability declares it realizes, recorded in the capability's own
  spec slice, so a newly carved capability shows its vision with no change to the view,
  and a capability that declares none — pure machinery — shows no vision, distinct from a bug

  ```check
  plant machinery
  read view
  vision derived
  vision blank
  ```

#### Scenario: the root's upper levels
- WHEN the operator opens the root of the view
- THEN its structural map of as-built reality and its complexity debt are the
  architecture review's standing output, derived from the scan, not hand-authored

  ```check
  read view-real
  structure
  debt
  ```

### Requirement: the as-built and gap are derived; only the vision is authored
No statement in the as-built or gap renders MUST be hand-authored or hand-maintained
as prose; each is a render of the model and changes when the model changes. The
vision they sit beside is the one writable region.

#### Scenario: the model changes
- WHEN a delta folds into the spec
- THEN the as-built and gap renders change in the same act, with nothing hand-edited

  ```check
  fold added
  read view
  asbuilt
  ```
