surfaced: 0

[CONTRACT]
Correct the salutation of the `CANDIDATE` prompt constant in `engine/design.py` so it speaks as the architect, matching the seat the prompt actually runs on. Today `design.CANDIDATE` opens "You are a hypercore worker designing ONE interface for a load-bearing decision" — but that prompt runs on the architect's transport (`transport.call`, Claude), because designing a candidate interface is architect work (the operator's ruling), exactly as the sibling `SELECT` prompt already opens "You are hypercore's architect". Change only the salutation's role name to the architect; leave the rest of the CANDIDATE prompt, its transport (`call`, unchanged), and the "like workers" similes in the module docstring exactly as they are — those are similes for the fenced isolation, not a claim about the seat. This corrects a contradiction between the salutation and the seat; it changes no behavior the living spec describes, so the delta is trivial.

[DELTA]
# delta — the-candidate-prompt-speaks-as-the-architect

(trivial — no behavior change. The correction touches one prompt constant's salutation in `engine/design.py`. No spec requirement describes the candidate-design prompt's wording — `design-it-twice` requires only that a candidate produces a design and that the architect selects — so no capability requirement is ADDED, MODIFIED, REMOVED, or RENAMED. The delta declares itself trivial and folding it applies nothing to the spec; the verified engine-code change still lands on main.)
