# worker
<!-- vision: worker, worktree, isolat, concurren, fence, parallel -->

The system-facing half of the split. A worker carries out a spawned ask: it builds,
fenced in its own git worktree and grounded in its capability's spec slice, and hands
the architect a complete technical result. It never faces the operator — every
word that crosses to the operator is the architect's, authored from the result.

### Requirement: a worker is system-facing and never reaches the operator
A worker's audience MUST be the architect and the spec, never the operator. Its
result is written for the machine; it has no channel to the operator at all, so a raw
worker output reaches the operator through no path — the architect authors every
operator-facing word from the result.

#### Scenario: a worker hands back
- WHEN a worker produces a technical result carrying raw, machine-facing prose
- THEN none of that prose appears on any card, render, or node; only what the
  architect authors from it crosses to the operator

  ```check
  build
  leak none
  ```

### Requirement: a worker is grounded in its capability's spec slice, by construction
A worker MUST be handed the living spec with the capabilities its change touches **foregrounded in
full** as its grounding — their requirements and scenarios inlined — AND **every other capability
carried as a high-signal index** (its vision line and requirement titles, not its body), with its
glossary terms, assembled before it runs, so there is no path that runs a worker without its grounding.
The index spans the whole spec — the small, scannable, high-signal **map**, the defense against the
architect's mis-scoping and against worker myopia: the worker sees every capability even when its body
is a read away. An untouched capability's full **body** is NOT inlined — carrying every body whole
spends the worker's attention budget on tokens the change does not touch, the cost our
context-engineering standard names; the body already lives in the worker's checkout, so it reads it
**just-in-time** from `spec/<name>.md` when its rescan implicates it. The glossary is carried by the
**same economy**: a defined term's entry is inlined only when the term appears in the foregrounded
prose (the touched bodies, the handed delta, the ask); every other entry stays in `glossary.md` in
the checkout, read **just-in-time** when the rescan implicates the term. The worker still holds every
term its change names — the whole ratified vocabulary is the architect's asset, not the worker's
grounding. The **long history and grounds of past decisions** are likewise NOT inlined: they are the
long reference with no whole-picture stake, so the worker greps **just-in-time** for them in its own
checkout (`work/archive/`, where a node archives with its work) as the change needs. It holds the
spec, never raw code, and never the operator view. A worker is **not slice-confined**: a delta cannot
be authored or verified from one capability in isolation, so its rescan covers the whole map — and
pulls the body it implicates — catching a capability the handed delta mis-named or missed.

#### Scenario: assembling the context
- WHEN a worker is run on a node whose handed delta names a set of capabilities
- THEN its prompt maps the whole spec — the named capabilities foregrounded in full as its grounding,
  every other capability carried as a vision+requirement-titles index — plus the change's glossary
  terms; an untouched capability's full body, like an untouched glossary entry and the long grounds of
  past decisions, is not inlined but a checkout read away (`spec/<name>.md`, `glossary.md`, and
  `work/archive/` for the grounds) for a just-in-time pull, and the index keeps the whole map in view
  while the grounding is foregrounded

  ```check
  plant-grounds
  spawn worker communication
  grounding marks worker communication
  grounding whole-spec
  grounding foregrounds communication
  grounding indexes tree
  grounding holds-no-code
  grounding omits-grounds
  grounding points-to-archive
  ```

#### Scenario: the rescan catches a mis-mapping
- WHEN a handed delta names a capability the change does not touch, or omits one it does
- THEN the worker's prompt still maps the whole spec — every capability in view, the untouched ones as
  an index — so its rescan can catch the mis-mapping rather than trust the delta's list, pulling the
  implicated body just-in-time, which a slice-confined worker could not

  ```check
  spawn tree
  grounding marks tree
  grounding whole-spec
  grounding indexes communication
  ```

#### Scenario: the glossary carries the change's terms, the rest a read away
- WHEN a worker's grounding is assembled for a change whose foregrounded prose names some defined terms
  and not others
- THEN every glossary entry the prompt inlines is one whose term appears in that prose, at least one
  defined term the prose does not name is omitted, and the omitted term's definition is reachable
  just-in-time from `glossary.md` in the checkout — the worker carries its change's vocabulary, not the
  whole ratified set

  ```check
  spawn worker communication
  grounding glossary-economical
  ```

### Requirement: a worker is grounded in the depth standards, every episode
A worker MUST be handed the **depth standards** as standing grounding in every episode — the
deep-module framework (a lot of behavior behind a small interface; a simple interface matters
more than a simple implementation; pull complexity downward), strategic over tactical
programming, and the **red flags** of shallowness. This grounding makes it build **deep up front**
rather than rely on the gate to catch shallowness after the fact. This is
the *proactive* primary anti-complexity defense: a worker that shares the long-term-health
concern produces deep modules, so the folding-conditions depth gate stays a rarely-tripped
backstop, not an operator-load generator. The grounding is assembled into the worker's prompt
by construction, like its spec slice — there is no path that runs a worker without it.

The disciplines MUST be **single-sourced**, not a frozen copy: depth is a capability like any other
(`spec/depth.md`), carried in the worker's whole-spec grounding and foregrounded **in full** in its
prompt every episode, so a sharpened slice reaches the next worker with no second copy to drift. The
same slice renders the `depth` **skill** through the methodology seam, materialized on disk for the
harness that loads skills natively — one source, the channels derived from it, the way the as-built
is derived from the model and only the vision is authored.

#### Scenario: the depth standards are in the grounding
- WHEN a worker is assembled to run
- THEN its prompt carries the deep-module framework and the red flags, foregrounded as
  disciplines it is held to, so it builds deep up front

  ```check
  spawn worker
  grounding carries-depth
  ```

#### Scenario: the disciplines are derived from their source
- WHEN the depth capability (`spec/depth.md`) is sharpened
- THEN the next worker's depth grounding renders the change with nothing hand-copied, and the
  retired frozen constant cannot drift from the source because it no longer exists

  ```check
  spawn worker
  sharpen
  grounding renders
  ```

### Requirement: a worker runs fenced in its own git worktree
A worker MUST run in its own git worktree — a separate checkout on its own branch — and that worktree
MUST be the **only** filesystem location it can write. The main tree, every sibling worker's worktree,
and the rest of the host are **read-only at the operating-system level**. A worker's attempt to modify any
path outside its own worktree fails as an OS refusal, not a convention it could break by accident — the
2026-06-24 escape (a live worker editing tracked files on main from a cwd-only fence) is barred by
construction. Its own worktree stays writable and the shared git object store stays **reachable and
writable**, so the worker's own commits reach the one record without touching another tree or the main
line until the result integrates. The enforcement wraps the **transport that spawns the worker's model**
(`transport.worker_transport`): that transport MUST spawn the worker inside a real OS jail rooted at the
worktree, not merely set the subprocess's working directory to it — a starting directory is not a jail.
The jail is built from an **unprivileged** OS sandbox primitive present on the host, needing no root and
no daemon. Because the jail roots at the worktree, the checkout remains the worker's working directory: its
source, the archived grounds (`work/archive/`), and the derived channel files (the anchor and skills) are
read from the checkout, and the harness auto-loads the fence's anchor and discovers its skills. The fence
is **working-trees only**: it walls the filesystem, not the shared object store — a worker deliberately
rewriting a sibling's branch or the main ref in the shared `.git` is out of scope, already barred where it
stands by the single-writer record lock and the fold being the only path to main, and unwinnable without
per-worker object stores. §74's net stays open: only the filesystem and the shared `.git` are fenced.
Because the host must carry the sandbox primitive for the fence to stand, the acceptance harness's
enforcement check surfaces a clear **skip or failure** where the primitive is absent, never a silent pass.

#### Scenario: the fence holds
- WHEN a worker is dispatched a node
- THEN it gets a worktree distinct from the main tree, commits its result there on its own
  branch, and that commit is reachable in the record but absent from the main line

  ```check
  fence off-main
  ```

#### Scenario: the worker runs at its fence
- WHEN a worker's model is summoned to build
- THEN its transport runs with the worktree as its working directory, so it reads the archived
  grounds and its channel files from its own checkout rather than from an inlined prompt

  ```check
  fence binds-cwd
  ```

#### Scenario: a live worker cannot write outside its worktree
- WHEN a worker is spawned inside its real fence and attempts to modify a path outside its own worktree —
  the main tree, a sibling's worktree, or elsewhere on the host — and, separately, writes inside its own
  worktree and commits
- THEN the outside write fails at the OS level (the host is read-only to the worker), while the in-worktree
  write and the git commit both succeed and the commit reaches the shared record — and where the host lacks
  the sandbox primitive the check surfaces a clear skip or failure rather than a silent pass

  ```check
  fence host-read-only
  fence worktree-writable
  fence commit-lands
  ```

### Requirement: concurrent workers advance the tree in isolation, each folding its own delta
The fence MUST compose: several workers MAY hold distinct worktrees at once, each building and
committing on its own branch, none touching a sibling's tree or the main line, and each folding
its own delta into the one spec independently. Isolation is the concurrency model — throughput is
many fences at once, and the same composition is what `design-it-twice` runs a contest of
candidates on.

#### Scenario: two workers advance at once
- WHEN two workers hold two distinct fences at the same time
- THEN each commits in its own tree off the main line, and each folds its own delta into the
  spec with no interference between them

### Requirement: the worker applies and refines the delta the architect proposed
A worker MUST rescan the current spec to verify the handed delta against present reality,
build to turn the capability's architect-authored scenarios **red→green**, and refine the delta —
including any new or sharpened scenario the behavior needs — to match what it built. The worker-facing
reply grammar MUST name every delta verb the fold accepts — ADDED / MODIFIED / REMOVED / RENAMED — so a
worker writes a retitle as RENAMED instead of a MODIFIED keyed on a title that the current spec does not
yet contain. The hand-off rides a **tag-delimited envelope** the transport renders and reads — each
field's content carried **verbatim** between its tags with no escaping, so the worker's markdown delta
(its `##` headers and fenced `check` blocks) round-trips losslessly and a field can never arrive as a
typed object to crash on; a reply carrying none of the envelope's tags surfaces as a malformed hand-off
rather than folding a no-op. It authors **no loop** and no check that judges its own work: the oracle is the self-model's
own scenario, run red→green by the gate over its fence, so the builder can never write the check that
clears it. The architect then coherence-checks the result against the contract and archives the delta.
The crossing is propose (architect) → apply (worker) → archive (architect), one delta end to end.

#### Scenario: the result integrates
- WHEN a worker hands back a refined delta and the architect judges the result
  coherent with the contract
- THEN the delta folds into the spec — only when the touched capability's scenarios went red→green —
  and the work leaves the work view in the same act; an incoherent result, or a scenario that did not
  transition, raises a decision instead of folding

  ```check
  build
  integrates
  ```

#### Scenario: the worker-facing delta grammar names retitles
- WHEN a worker is asked to refine a delta
- THEN its reply grammar names RENAMED beside ADDED / MODIFIED / REMOVED, so a title-only retitle is
  written as a rename operation

  ```check
  spawn self-model
  envelope names-renamed
  ```

#### Scenario: the hand-off round-trips authored content verbatim
- WHEN a worker hands back a report and a markdown delta carrying `####` headers and a fenced `check`
  block, and when a reply carries none of the envelope's tags
- THEN the transport reads the report and delta back byte-for-byte with no escaping — the
  report-as-object crash class gone by construction — and the tagless reply surfaces as a malformed
  hand-off rather than folding a no-op

  ```check
  handoff round-trips
  handoff surfaces-malformed
  ```
