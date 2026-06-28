surfaced: 0

[CONTRACT]
Build the gated caveat-survival routing into the architect's archive render (`integrate`) so a load-bearing
caveat dropped by the compression is caught before it reaches the operator. This adds ONE gated requirement
to `communication` — "a dropped caveat never reaches the operator" — holding the watched/gated line exactly:
the entailment VERDICT is model-driven and stays watched (a live NLI call can never be the gate, since
`python3 -m engine --check` is deterministic and in-process), while the ROUTING is gated (a dropped caveat
is provably caught against a scripted oracle in the world fixture).

The engine seam to build:
- `engine/communication.py` — a built routing function `caveat_survives(say, caveat, transport) ->
  (bool, reason)`. An empty caveat short-circuits to `(True, "")` with NO second model call, so the existing
  "a worker hands back" scenario (whose COHERENCE reply names no caveat) is untouched. Otherwise it reads a
  one-flag entailment envelope from the injectable transport (live: a model call; harness: a scripted
  oracle) and returns `(False, "...the load-bearing caveat was dropped...")` when the words do not entail
  the caveat. Wire it into `integrate`: extend `COHERENCE_SCHEMA` with a `caveat` tag (the load-bearing
  qualifier the words must carry); after a coherent verdict authors `say`, run `caveat_survives` — a dropped
  caveat routes exactly like incoherence (raise a decision card parented on the node; the words do not fold
  as drafted).
- `engine/worlds/communication_world.py` — verbs over the REAL `integrate` with scripted transports:
  `contract-caveat` stages a worker hand-off whose contract carries a load-bearing caveat; `drafts-without`
  integrates with a COHERENCE reply that is coherent but whose `say` omits the caveat, carrying the caveat
  tag plus an ENTAIL reply {survives: false}; `caught` asserts the result did NOT fold and a decision was
  raised; `drafts-with` integrates with the caveat kept in `say` plus ENTAIL {survives: true}; `crosses`
  asserts it folded. The scripted oracle makes the gate deterministic; the live entailment is the model,
  watched.

The architect-authored scenario goes red->green on this seam: at the fork base `integrate` does no caveat
routing, so the dropped-caveat draft folds and `caught` fails (red); at the tip it routes to a decision and
`caught` passes, the surviving caveat still crossing (green). Do not weaken the existing communication
scenarios; the whole system must re-verify green on merge. You build the engine and the world fixture; you
do not author the scenario or its check block — those are fixed.

[DELTA]
# delta — gated caveat-survival on the architect's render

## ADDED — communication
### Requirement: a dropped caveat never reaches the operator
The architect MUST run the clarity self-check on its own draft before the words cross, and a load-bearing
**caveat dropped by the compression MUST be caught before it reaches the operator**. The four-count
self-check (re-derivable · caveat survives · truth survives form-strip · this reader, not the gallery) is
watched judgment and edits expression only, never the decision. The one count a tool holds without a
model — caveat-survival — is built into the architect's archive render: the operator-facing words are
checked against the load-bearing caveat the contract carries, and words that drop it do not cross as
drafted. The entailment verdict is model-driven and stays **watched** — live it is the architect's
judgment — so only the **routing** is mechanically **gated**: a dropped caveat is provably caught and
raises a decision, never silently passed.

#### Scenario: a dropped caveat is caught, a surviving one crosses
- WHEN the architect integrates a worker hand-off whose contract carries a load-bearing caveat
- THEN words that drop the caveat are caught before they cross — the routing gated on the survival verdict,
  raising a decision — while words that keep it cross and fold, the verdict itself the architect's watched
  judgment

  ```check
  contract-caveat
  drafts-without
  caught
  drafts-with
  crosses
  ```
