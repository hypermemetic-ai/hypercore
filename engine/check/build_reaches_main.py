"""Acceptance for the verified fenced build reaching main — exercised from outside the fold it tests.

The fold's code-bearing path (`delta.fold(.., code=)`) lands a worker's verified engine code on the
merged tree, in one commit with its spec, re-verified on the merged tree before the commit. The
re-verify reaches the **whole system** — every capability's scenarios on merged main, not only the ones
the delta named — so a refactor of a shared engine module cannot break an *untouched* capability and
still land. That behavior **cannot certify itself from inside a fold**: re-verify runs the merged
tree's scenarios in a fresh process against the merged engine, so a scenario that itself folded code
would recurse — the same self-reference the scenario gate's own red→green carries. So it is proven here,
from outside, over a real runnable merged tree, never as an in-spec block. The behavior is recorded
**watched** in `spec/self-model.md` ("folding lands the verified build's code on the merged tree").

This is its own module — like the per-capability worlds — because the fixture is heavyweight: it stands
up a self-contained hypercore on disk (engine + spec) so the fold can content-replay onto it and the
re-verify subprocess can import its own merged engine. Holding it apart keeps the main scenario harness
under the length signal it exists to enforce.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

from .harness import ok
from .. import delta, scenario, tree, worker

REAL = tree._DEFAULT_ROOT                                  # hypercore's own source tree, copied into the merged fixture


def check() -> None:
    """A code-bearing fold lands the build's ENGINE CODE on the merged tree (positive); a build that would
    leave the merged tree red is refused with every write rolled back (negative — re-verify on the merged
    tree is the load-bearing keystone, not narration); and a build whose code breaks a capability the
    delta never named is refused too (untouched-capability negative — the keystone reaches the whole
    system, so green-on-the-named-capability can never mean red-on-the-system)."""
    prev = os.environ.get("ENGINE_ROOT")
    root = _full_root()
    rel, spec_rel = "engine/conditions.py", "spec/folding-conditions.md"
    path = os.path.join(root, rel)
    try:
        os.environ["ENGINE_ROOT"] = root

        # positive — the verified change is a benign marker, so the touched capability's scenarios still
        # hold on the merged tree; the fold re-verifies green and the code lands beside the spec.
        original = open(path, encoding="utf-8").read()
        marked = original + "\n# build-reaches-main: a verified marker line\n"
        node = tree.file_intent("a code-bearing ask")
        d = delta.parse("# delta — note\n## ADDED — folding-conditions\n"
                        "### Requirement: a watched build-reaches-main note\n"
                        "The note holds.\n#### Scenario: s\n- WHEN x\n- THEN y\n")
        delta.fold(d, root, node=node, code={rel: worker.CodeFile(original, marked)})
        ok("build-reaches-main: a verified marker" in open(path, encoding="utf-8").read(),
           "build-reaches-main — a code-bearing fold lands the verified ENGINE CODE on main, not only the spec")
        ok(_committed_together(root, rel, spec_rel),
           "build-reaches-main — the code and the spec land in ONE commit (atomic, both directions)")

        # negative — a verified change that breaks the touched capability on the merged tree (SIGNAL no
        # longer an int): re-verify goes red, the fold rolls back every write and refuses, nothing lands.
        before = open(path, encoding="utf-8").read()
        broken = before.replace("SIGNAL = 400", "SIGNAL = 'broken'")
        node2 = tree.file_intent("a code-bearing ask that breaks merged main")
        d2 = delta.parse("# delta — note2\n## ADDED — folding-conditions\n"
                         "### Requirement: another watched note\nIt holds.\n#### Scenario: s\n- WHEN x\n- THEN y\n")
        refused = False
        try:
            delta.fold(d2, root, node=node2, code={rel: worker.CodeFile(before, broken)})
        except delta.CannotFold:
            refused = True
        ok(refused,
           "build-reaches-main — a build red once merged is refused: re-verify on the merged tree is the keystone")
        ok(open(path, encoding="utf-8").read() == before,
           "build-reaches-main — the refused fold rolled back: nothing landed on main")

        # untouched-capability negative — the delta names ONLY folding-conditions, but the code refactors
        # engine/schedule.py, a module folding-conditions never exercises, with a bug. Under a touched-only
        # re-verify this lands green-on-the-named-capability, red-on-the-system — the blind spot the rename-op
        # crossing surfaced (it refactored a shared module and folded green on its one named capability). The
        # whole-system re-verify runs the *schedule* capability's scenarios on merged main, catches them red,
        # and refuses: nothing lands.
        sched_rel = "engine/schedule.py"
        sched = os.path.join(root, sched_rel)
        sched_before = open(sched, encoding="utf-8").read()
        sched_broken = sched_before + "\nraise RuntimeError('a refactor bug breaks the schedule capability')\n"
        node3 = tree.file_intent("names folding-conditions, code breaks the untouched schedule capability")
        d3 = delta.parse("# delta — note3\n## ADDED — folding-conditions\n"
                         "### Requirement: an untouched-break note\nIt holds.\n#### Scenario: s\n- WHEN x\n- THEN y\n")
        untouched_refused = False
        try:
            delta.fold(d3, root, node=node3, code={sched_rel: worker.CodeFile(sched_before, sched_broken)})
        except delta.CannotFold:
            untouched_refused = True
        ok(untouched_refused,
           "build-reaches-main — a code-bearing fold that breaks an UNTOUCHED capability is refused: re-verify "
           "reaches the whole system, not only the capabilities the delta names")
        ok(open(sched, encoding="utf-8").read() == sched_before,
           "build-reaches-main — the untouched-break fold rolled back: nothing landed on main")

        _resource_limit_reverify(root, rel)
    finally:
        if prev is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = prev
        shutil.rmtree(root, ignore_errors=True)


def _full_root() -> str:
    """A self-contained, runnable hypercore on disk — engine + spec + intent + glossary, git-init and
    committed — so a code-bearing fold can content-replay onto it and re-verify by importing its own
    merged engine in a fresh process (the re-verify subprocess needs the merged engine and spec present)."""
    r = tempfile.mkdtemp(prefix="scenario-codeland-")
    for c in (("init", "-q"), ("config", "user.email", "land@hypercore"), ("config", "user.name", "land")):
        subprocess.run(["git", *c], cwd=r, check=True, stdout=subprocess.DEVNULL)
    for d in ("engine", "spec"):
        shutil.copytree(os.path.join(REAL, d), os.path.join(r, d),
                        ignore=shutil.ignore_patterns("__pycache__"))
    for f in ("intent.md", "glossary.md"):
        shutil.copyfile(os.path.join(REAL, f), os.path.join(r, f))
    subprocess.run(["git", "add", "-A"], cwd=r, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-qm", "seed"], cwd=r, check=True, stdout=subprocess.DEVNULL)
    return r


def _committed_together(root: str, *rels: str) -> bool:
    """Every named path is in HEAD's single commit — the one-commit, both-directions atomicity."""
    out = subprocess.run(["git", "show", "--name-only", "--pretty=format:", "HEAD"], cwd=root,
                         capture_output=True, text=True).stdout
    names = set(out.split())
    return all(r in names for r in rels)


def _resource_limit_reverify(root: str, rel: str) -> None:
    """The re-verify hardening: capped-run classification, scaling budget, retry, and rollback."""
    env = os.environ.copy()
    over = scenario._capped_run(["python3", "-c", "import time; time.sleep(1)"], root, env, 0.01)
    missing = scenario._capped_run([os.path.join(root, "missing-hypercore-binary")], root, env, 1)
    done = scenario._capped_run(["python3", "-c", "import sys; sys.exit(7)"], root, env, 5)
    ok(over.kind == scenario.OVERRAN and missing.kind == scenario.COULD_NOT_RUN
       and done.kind == scenario.COMPLETED and done.code == 7,
       "build-reaches-main — capped-run classifies overrun, could-not-run, and completed distinctly")

    small = ">>> one\nprobe"
    large = "\n".join(f">>> s{i}\nprobe" for i in range(25))
    ok(scenario._suite_budget(large) > scenario._suite_budget(small) >= scenario.SUITE_TIMEOUT_FLOOR,
       "build-reaches-main — the re-verify suite budget scales with scenario count and keeps a floor")

    real_all, real_src, real_run = scenario._all_capabilities, scenario._check_source, scenario._run_merged
    try:
        scenario._all_capabilities = lambda _root: ["probe"]
        scenario._check_source = lambda _cap, _root: large
        calls: list[float] = []
        def over_then_green(src, cap, r, budget):
            calls.append(budget)
            return scenario.RunOutcome.overran() if len(calls) == 1 else scenario.RunOutcome.completed(0)
        scenario._run_merged = over_then_green
        ok(scenario.reverify(root) is None and len(calls) == 2 and calls[1] > calls[0],
           "build-reaches-main — a re-verify overrun is retried once with headroom")
        scenario._run_merged = lambda src, cap, r, budget: scenario.RunOutcome.overran()
        failed = scenario.reverify(root)
        ok(failed is not None and failed.kind == scenario.RESOURCE_LIMIT
           and "resource limit reached" in failed.message and "not a broken build" in failed.message,
           "build-reaches-main — a persistent overrun is a retryable resource limit, not merged-red")
        scenario._run_merged = lambda src, cap, r, budget: scenario.RunOutcome.could_not_run()
        failed = scenario.reverify(root)
        ok(failed is not None and failed.kind == scenario.COULD_NOT_RUN and "could not run" in failed.message,
           "build-reaches-main — a genuinely unrunnable re-verify still refuses as could-not-run")
    finally:
        scenario._all_capabilities, scenario._check_source, scenario._run_merged = real_all, real_src, real_run

    path = os.path.join(root, rel)
    before = open(path, encoding="utf-8").read()
    spec_rel = os.path.join(root, "spec", "folding-conditions.md")
    spec_before = open(spec_rel, encoding="utf-8").read()
    node = tree.file_intent("a code-bearing ask that exhausts the re-verify budget")
    d = delta.parse("# delta — resource limit note\n## ADDED — folding-conditions\n"
                    "### Requirement: a resource limit note\nIt holds.\n#### Scenario: s\n- WHEN x\n- THEN y\n")
    real_reverify = scenario.reverify
    try:
        scenario.reverify = lambda _root: scenario.ReverifyFailure(
            scenario.RESOURCE_LIMIT, "probe",
            "resource limit reached — retryable; this is not a broken build")
        refused, message = False, ""
        try:
            delta.fold(d, root, node=node, code={rel: worker.CodeFile(before, before + "\n# resource limit probe\n")})
        except delta.ResourceLimitReached as e:
            refused, message = True, str(e)
        except delta.CannotFold as e:
            message = f"wrong refusal type: {e}"
        ok(refused and "resource limit reached" in message and "not a broken build" in message,
           "build-reaches-main — resource-limit re-verify branches away from the broken-build refusal")
        ok(open(path, encoding="utf-8").read() == before
           and open(spec_rel, encoding="utf-8").read() == spec_before,
           "build-reaches-main — a resource-limit re-verify rolls back the merge without discarding it as broken")
    finally:
        scenario.reverify = real_reverify
