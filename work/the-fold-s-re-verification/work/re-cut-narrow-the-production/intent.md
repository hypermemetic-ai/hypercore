---
kind: decide
state: awaiting you
owner: machine
created: 1782591607
---
Re-cut — narrow; the production behavior is correct and proven, the defect is one self-test's classification.

The new `verify-run` / `outcome` scenario added to `spec/self-model.md` ("an overrun is a distinct resource limit, an unrunnable run still refuses") is written as a **gated** scenario — a live ```check``` block. But its fixture (`engine/worlds/_verify_run_probe.py`) calls the brand-new `scenario._capped_run` seam, which is absent at the fork base. Confirmed empirically: carrying the tip's `self_model_world.py` onto a base checkout fails to import (`_verify_run_probe` does not exist there), so the gate's base run for the whole self-model capability errors and its red→green is spurious — the gate would claim a structural guarantee it does not have. Per `_world_source`'s own documented contract and `spec/coherence.md`, a verb whose fixture needs a seam absent at the base is the **watched** archive-gate judgment, never gated.

The substance is already proven watched in `engine/check/build_reaches_main.py`: `_resource_limit_reverify` exercises the real TimeoutExpired→resource-limit path end-to-end, and `_could_not_run_reverify` the real OSError→could-not-run path. So the gated `verify-run` scenario is also redundant.

Re-cut: drop the gated `verify-run` scenario together with its now-orphaned probe module (`engine/worlds/_verify_run_probe.py`) and the `_v_verify_run` / `_v_outcome` verbs; if that scenario is to remain a distinct line in `spec/self-model.md`, mark it **watched — proven from outside in `engine/check/build_reaches_main.py`**, mirroring the second scenario. Everything else in the hand-off lands as-is.

[machine]
