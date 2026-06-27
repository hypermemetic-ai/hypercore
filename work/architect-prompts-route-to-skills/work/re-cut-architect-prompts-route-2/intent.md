---
kind: decide
state: settled
owner: operator
created: 1782602214
---
Re-cut: architect-prompts-route-to-skills. THIRD hand-off reporting success with nothing on the node's tree — treat the worker's self-report as untrusted and verify only against the committed tree. Acceptance is mechanical, all checked against `git`-committed state:
1. `engine/communication.py`, `engine/grill.py`, `engine/design.py`, `engine/check/scenarios.py` must each show a real diff from current main.
2. `design.SELECT` must no longer contain the strings "DEPTH", "LOCALITY", "SEAM PLACEMENT"; those axes live only in the design-it-twice skill render.
3. `communication.EXPLAIN` must exist as a module constant and be used by `explain()`.
4. Each of the six prompts (SYSTEM, COHERENCE, EXPLAIN, FLOOR, PRODUCTS, SELECT) must name and instruct loading its skill and drop the paraphrased methodology; every `*_SCHEMA` constant byte-identical.
5. `scenarios.py:120` old axis assertion REPLACED (not merely left passing) with the route-to-skill + skill-carries-axes pair, plus the six-prompt load assertion — verified RED by checking out main and ADDING only the new oracle, GREEN after the prompt changes.
Root-cause the landing gap before rebuilding: the prior fences built work that never reached the node tree. Do not fold until `git diff main` shows the prompt edits and `--check` is green on that same tree.
