---
kind: ask
state: standing
owner: operator
created: 2026-06-27
---
# the-candidate-prompt-speaks-as-the-architect — the salutation matches the seat

`design.CANDIDATE` (engine/design.py) opens "You are a hypercore worker designing ONE interface", but
the candidate runs on the **architect's** transport (`transport.call`, Claude), because designing a
candidate interface is architect work — the operator's ruling. The salutation contradicts the seat the
model is in.

Correct the salutation to speak as the architect; the transport stays `call`. This is the one place
the candidate-designer is *called* a worker — the "like workers" lines in the module docstring are
similes for the fenced isolation and stay as they are.

## folding condition
- the candidate-design prompt's salutation names the architect, not the worker;
- the candidate still runs on the architect transport (`call`), unchanged;
- `python3 -m engine --check` is green.
