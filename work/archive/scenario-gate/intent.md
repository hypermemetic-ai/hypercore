---
kind: ask
state: standing
owner: operator
created: 2026-06-23
---
# scenario-gate — the acceptance check is the self-model's own scenario

Two faults in the acceptance layer, one root. The red→green loop that gates a behavior change is a
command the **worker records about its own work** (`worker.py:106,259`), and whether it tests the
claimed behavior is only **watched** (`folding-conditions.md:133`) — so a frontier-model worker
authors the oracle that judges it, the self-judging the worker/architect split exists to prevent.
And the acceptance harness is partitioned by **build-slice** (`engine/check/sliceN.py`), the unit of
construction, not by capability — so one capability's checks smear across many slice files
(folding-conditions across slices 5/7/9/20/21) and "slice" carries two meanings against the
one-name-one-concept rule.

One move fixes both: the acceptance check becomes the **architect-authored scenario in the
capability's spec**. The self-model's account of a behavior *is* the executable gate that behavior
passes — read by the agent, describing the system, and validating it at once. The worker builds to
turn the architect's scenario red→green; it never authors the check that judges it. Because each
check now lives as its capability's scenario, the build-slice harness dissolves and checks home by
capability.

Seam-first: build the scenario→executable binding — a **deep module**, the scenario the high-signal
WHEN/THEN interface with the machinery hidden beneath, its interface settled by a design-it-twice —
and realize it first on **folding-conditions**, the capability most smeared across slices and the one
that gates everything. Each remaining capability's migration is named follow-on work.

Provenance: grilled 2026-06-23 from the operator's two concerns (strict red/green for frontier LLMs;
the by-slice check organization). Evidence in `research.md`; the grilling record in `contract.md`.

## folding condition
- the scenario→executable binding seam exists, its interface picked by a design-it-twice;
- folding-conditions' scenarios are realized as executable checks that gate it red→green, and the
  slice-5/7/9/20/21 content for it dissolves into them;
- the worker hand-off no longer carries a self-authored loop; a behavior change folds only when an
  architect-authored scenario goes red→green;
- `python3 -m engine --check` is green throughout, unconverted capabilities coexisting;
- each remaining capability's migration is filed as standing follow-on work.
