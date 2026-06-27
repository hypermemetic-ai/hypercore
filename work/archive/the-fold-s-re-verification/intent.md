---
kind: ask
state: done
owner: operator
created: 1782588514
---
The fold's re-verification carries a fixed 180s-per-capability timeout that turns a slow run into a misleading fold refusal — a budget that does not scale and masks a perf limit as a correctness fault.

Every code-bearing fold runs `scenario.reverify` (engine/scenario.py:191) as its keystone: it re-runs ALL capabilities' scenarios against the merged tree — currently 15 capabilities, 134 scenarios — each capability's whole suite in its own fresh `python3 -m engine` subprocess, serially, each capped at `timeout=180` (scenario.py:242). The apply-stage `scenario.gate` (scenario.py:150) does the same at the fork base and tip for each *touched* capability (two subprocess runs per cap). So a fold that touches self-model runs self-model's 27-scenario suite at least three times (base, tip, merged) plus the other 14 suites once — the slow integrate tail an operator watches sweep capability-by-capability for minutes.

Three faults, all present in the code today:

1. A timeout is silently reclassified as a correctness failure. `_run_merged` and `_run_at` catch the timeout — `except (OSError, subprocess.SubprocessError): return None` (scenario.py:246, 313; `TimeoutExpired` is a `SubprocessError`) — and `None` becomes a hard refusal: reverify returns "the scenarios for X could not be re-verified — a build that cannot be re-verified does not land" (scenario.py:214), so `delta.fold` raises `CannotFold` and the entire ~20-minute verified codex build is thrown away. A slow machine reads as a broken build.

2. A performance timeout is indistinguishable from a genuine "cannot run". Both a 180s timeout and a real failure-to-run (missing binary, OSError) collapse to the same `None`, the same card. The operator cannot tell "your machine was slow" from "the scenario is broken" — exactly the signal that wastes time chasing the wrong cause.

3. The 180s bound does not scale. self-model already holds 27 scenarios in one 180s run, several doing real git folds (~6.7s of headroom each). As capabilities accumulate scenarios the per-cap run creeps toward the wall; when it crosses — load- and variance-dependent — folds begin failing NON-DETERMINISTICALLY with that misleading card. The constant is fixed; the load grows.

To surface in grilling: whether a timeout must become a DISTINCT outcome (a retry, or an honest "resource limit reached" surfaced to the operator) that never silently equals "scenario broken" and never discards a verified build on a perf blip; whether the per-fold cost (15 fresh `python3 -m engine` startups serially, 134 scenarios, the self-model suite run ~3×) should be cut by scoping, by caching the base/tip runs the gate already paid for, or by parallelizing the merged-tree sweep; whether 180s is even the right shape of bound (per-scenario vs per-suite vs whole-sweep); and a red→green scenario — a capability whose suite deterministically exceeds the budget must NOT fold-refuse as "could not re-verify", while a genuinely unrunnable scenario must still refuse.
