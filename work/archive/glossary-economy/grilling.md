surfaced: 0

[CONTRACT]
The worker's glossary stops being the whole ratified vocabulary and becomes the terms its change touches. A glossary entry reaches the worker's prompt only when its **term appears in the prose the worker holds foregrounded** — the touched capability bodies, the handed delta, and the ask; every other entry stays in `glossary.md` in the fenced checkout, read **just-in-time** when the rescan implicates a term, the same seam the index+JIT redesign placed for capability bodies. The selection is **derived from the text, never a hand-maintained audience tag** — so the architect's operator-and-infrastructure vocabulary falls away on its own (it is not in the worker's prose) while a term the change names is kept even when it is operator-facing (`card`/`queue` survive when the prose names the operator's queue). The worker still sees every term its change names, so it cannot drift on a term it is using; a synonym for a term outside its working set is caught by the architect's coherence read and, once built, the vocabulary check — so the lean glossary ships independently of that guard. On a glossary-heavy change about half the vocabulary (36 of 72 entries, ~10 KB) leaves the prompt; a focused change sheds more. The result is validated by a worker whose foregrounded prose names some terms and not others seeing only the named terms' entries inlined and an unnamed term's definition left a just-in-time read away, by the existing grounding and consistency defenses staying green, and by `python3 -m engine --check` carrying the acceptance.

[DELTA]
## MODIFIED — worker

### Requirement: a worker is grounded in its capability's spec slice, by construction
A worker MUST be handed the living spec with the capabilities its change touches **foregrounded in full**
as its grounding — their requirements and scenarios inlined — AND **every other capability carried as a
high-signal index** (its vision line and requirement titles, not its body), with the glossary, assembled
before it runs, so there is no path that runs a worker without its grounding. The index spans the whole
spec — the small, scannable, high-signal **map**, the defense against the architect's mis-scoping and
against worker myopia: the worker sees every capability even when its body is a read away. An untouched
capability's full **body** is NOT inlined — carrying every body whole spends the worker's attention budget
on tokens the change does not touch, the cost our context-engineering standard names; the body already
lives in the worker's checkout, so it reads it **just-in-time** from `spec/<name>.md` when its rescan
implicates it. The glossary is carried by the **same economy**: a defined term's entry is inlined only
when the term appears in the foregrounded prose (the touched bodies, the handed delta, the ask); every
other entry stays in `glossary.md` in the checkout, read **just-in-time** when the rescan implicates the
term. The worker still holds every term its change names — the whole ratified vocabulary is the
architect's asset, not the worker's grounding. The **long history and grounds of past decisions** are
likewise NOT inlined: they are the long reference with no whole-picture stake, so the worker greps
**just-in-time** for them in its own checkout (`work/archive/`, where a node archives with its work) as
the change needs. It holds the spec, never raw code, and never the operator view. A worker is **not
slice-confined**: a delta cannot be authored or verified from one capability in isolation, so its rescan
covers the whole map — and pulls the body it implicates — catching a capability the handed delta mis-named
or missed.

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
