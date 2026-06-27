surfaced: 0

[CONTRACT]
The worker prompt will lead with the mission instead of the rulebook: the ask and its handed delta move to the top, right after the salutation, and the standing disciplines, the record grounding, and the depth standards follow as "how you are held", with the reply envelope still last. Separately, the two worker spec statements that read worst in one pass -- the 111-word re-derivation sentence and the "never raw code, and never the operator view" compound negation -- are rewritten at their source into short, positive, one-instruction sentences, so the sharpened prose flows into both the assembled prompt and the rendered worker skill. A worker prompt assembled after the change presents the task before the disciplines with the envelope last, and the writing-for-the-machine signal no longer flags those two statements.

[DELTA]
# delta — worker-prompt-leads-with-the-task

## ADDED — worker
### Requirement: the worker prompt is built for the one-pass reader
The assembled worker prompt MUST lead with the task. The ask and the handed delta come first, right after the salutation, so the worker spends its freshest attention on the job. The standing disciplines, the record grounding, and the depth standards follow the task as "how you are held". The reply envelope MUST stay last — the transport's reason-first, format-last invariant (`transport.instruction`). The worker's own discipline prose MUST read in one pass: the over-long re-derivation statement is split so no sentence runs past the writing-for-the-machine length signal, and the grounding requirement's compound negation becomes a positive instruction, so neither construct trips the signal.

#### Scenario: the prompt leads with the task and ends with the envelope
- WHEN a worker prompt is assembled for a node whose handed delta names a set of capabilities
- THEN the ask and the handed delta both appear before the standing disciplines, the record grounding, and the depth standards, and the reply envelope is the prompt's final block

  ```check
  spawn worker communication
  order ask-leads
  order envelope-last
  ```

#### Scenario: the worker's flagged disciplines no longer trip the signal
- WHEN the writing-for-the-machine signal reads the worker capability's requirement statements
- THEN the grounding requirement raises no compound-negation flag and the re-derivation requirement raises no over-long-sentence flag

  ```check
  signal worker-prose-sharpened
  ```

## MODIFIED — worker
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
checkout (`work/archive/`, where a node archives with its work) as the change needs. The grounding holds the
spec. The architect carries the raw code and the operator view. A worker is **not slice-confined**: a delta cannot
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

### Requirement: a worker's RESULT is trusted only by re-derivation, never by the fence the fold tears down
A worker's RESULT and refined delta are a **derived** record. The provenance gate MUST attest them by **re-deriving** the touched capability's scenarios red→green — failing at the fork base, passing at the tip in the fence, and re-verified on the merged tree. The gate MUST NOT rely on the worker's fence branch or commit as the trail. That fence is removed on every exit. The fold re-applies the delta as a fresh commit on main, so the worker commit is absent from main lineage (`a worker runs fenced in its own git worktree`; `folding lands the verified build's code on the merged tree, not only its spec`). A RESULT hand-authored without ever running a fenced worker leaves no red→green to re-derive — its scenarios do not transition — so it has **no trail** and MUST NOT fold: it is refused with `no trail — re-run the mechanism`, never an operator-waveable decision. This attests that the build **ran**; whether its scenarios test the property is deferred to `gate-vouches-for-the-new-verb`.

#### Scenario: a hand-authored RESULT does not re-derive red→green and is refused
- WHEN a RESULT is handed back that a role authored without a fenced build, and, separately, a RESULT carried by a real fenced build
- THEN the hand-authored one fails to re-derive the touched scenarios red→green and is refused at the gate (`no trail`), while the real build re-derives and folds

  ```check
  build
  integrates
  forge result
  fold held because provenance
  ```
