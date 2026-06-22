"""Slice 19 — the fold is transactional: atomic both directions, idempotent retry (H1).

Acceptance (spec/self-model §folding applies the delta atomically, both directions): the spec asserts
the fold is atomic in both directions, but the implementation was two separate acts — apply the delta
and commit (`delta.fold`), then archive the node (`graph.integrated`). A crash between them left the
**delta merged into the spec but the node un-archived**, and the retry hit `delta.check`'s "ADDED
requirement already exists" → a permanent `CannotFold`: operator work wedged with its change already in
the spec (research H1). The ratified fix makes the fold one transactional act with idempotent retry.

This slice fault-injects a crash mid-fold and asserts the retry completes cleanly:

1. **spec-merge and node-archive land in ONE commit** — folding a node moves the folder *and* lands
   the delta in a single commit, so the record never shows one without the other. *RED if they are two
   separate commits.*
2. **a crash mid-fold does not wedge** — inject a failure after the spec write but before the node
   moves; the spec change is on disk. The retry must complete — archive the node, commit — not refuse
   with `CannotFold`. *RED if `check` treats the already-applied ADDED as a conflict.*
3. **the retry is idempotent** — after recovery the requirement is present exactly once and the node
   is folded; no half-fold, no duplicate, no permanent `CannotFold`.
"""
from __future__ import annotations

import os
import subprocess
import tempfile

from .harness import ok


def _init(prefix: str) -> str:
    root = tempfile.mkdtemp(prefix=prefix)
    for cfg in (["init", "-q"], ["config", "user.email", "c@h"], ["config", "user.name", "c"]):
        subprocess.run(["git", *cfg], cwd=root, check=True)
    return root


def _delta_text(cap: str, req: str) -> str:
    return (f"# delta — grow {cap}\n\n## ADDED — {cap}\n### Requirement: {req}\n"
            f"The {cap} MUST hold.\n#### Scenario: s\n- WHEN x\n- THEN y\n")


def check(_shared_root: str) -> None:
    from .. import delta, graph, spec

    print("\nslice 19 — acceptance check  (the fold is transactional: atomic both directions, retryable)\n")

    # ── 1. spec-merge and node-archive land in ONE commit ───────────────────────────────────────────
    root = _init("engine-check-s19a-")
    os.environ["ENGINE_ROOT"] = root
    node = graph.file_intent("grow the alpha capability")
    before = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root,
                            capture_output=True, text=True).stdout.strip()
    delta.fold(delta.parse(_delta_text("alpha", "the alpha property holds")), root, node=node)
    after = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root,
                           capture_output=True, text=True).stdout.strip()
    cap = spec.read_spec(root).capability("alpha")
    folded = graph.find(node.id)
    ok(cap is not None and cap.requirement("the alpha property holds") is not None,
       "folding a node lands its delta in the spec")
    ok(folded is not None and folded.folded,
       "the same fold archives the node — both directions in one act")
    ok(int(after) - int(before) == 1,
       "the spec merge and the node archive are ONE commit — atomic, both directions (H1)")

    # ── 2 & 3. a crash mid-fold does not wedge; the retry completes idempotently ─────────────────────
    # Inject a failure inside the fold after the spec atomic_write but before the node moves. The spec
    # change lands on disk (uncommitted); the act raises. This is the crash that left the old code
    # wedged: the delta was in the spec, the node was IN_FLIGHT, and the retry hit a permanent
    # CannotFold. The retry here must instead complete — archive the node, commit — idempotently.
    root = _init("engine-check-s19b-")
    os.environ["ENGINE_ROOT"] = root
    node2 = graph.file_intent("grow the beta capability under a crash")
    d = delta.parse(_delta_text("beta", "the beta property holds"))

    real_archive = graph.archive_in_place
    graph.archive_in_place = lambda n: (_ for _ in ()).throw(RuntimeError("crash mid-fold"))
    crashed = False
    try:
        delta.fold(d, root, node=node2)
    except RuntimeError:
        crashed = True
    finally:
        graph.archive_in_place = real_archive
    ok(crashed, "the injected crash mid-fold raises — the act did not complete")

    # the spec change is on disk now (the half-applied state the crash leaves). The retry must NOT
    # refuse with CannotFold on the already-present ADDED — it must read it as already-applied and
    # complete the fold (archive the node, commit).
    on_disk = spec.read_spec(root).capability("beta")
    ok(on_disk is not None and on_disk.requirement("the beta property holds") is not None,
       "the crash left the delta applied to the spec on disk — the wedge precondition")
    retried_ok = True
    try:
        delta.fold(d, root, node=graph.find(node2.id))
    except delta.CannotFold:
        retried_ok = False
    ok(retried_ok, "the retry does NOT hit a permanent CannotFold on the already-applied delta (H1 wedge closed)")

    final = spec.read_spec(root).capability("beta")
    reqs = [r.name for r in final.requirements] if final else []
    ok(reqs.count("the beta property holds") == 1,
       "the retry is idempotent — the requirement is present exactly once, no duplicate")
    ok(graph.find(node2.id).folded,
       "the retry archives the node — the work is no longer wedged, the fold completed")
