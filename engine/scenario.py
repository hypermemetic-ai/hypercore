"""The scenario binding — a capability's prose scenario is its executable check.

`run` executes check blocks against the live engine for acceptance. `gate` carries the tip's check
source and world fixture to the fork base and tip, requiring red→green for the gated source a delta
changed. `reverify` runs every capability's suite on merged main before code-bearing folds commit.
The gated/watched register is derived from check-block presence.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

from . import delta, spec, worlds

# Set while the gate runs a capability's scenarios at a ref: a nested folding check sees it and skips
# the base/tip gate, so running scenarios can never recurse into running scenarios. One name, system-wide.
_GATE_GUARD = "HYPERCORE_SCENARIO_GATE"

COMPLETED, OVERRAN, COULD_NOT_RUN = "completed", "overran", "could-not-run"
RED = "red"
RESOURCE_LIMIT = "resource-limit"

SUITE_TIMEOUT_FLOOR = 180.0
SUITE_TIMEOUT_PER_SCENARIO = 10.0
SUITE_RETRY_HEADROOM = 1.5


# ── parsing: a capability's scenarios, and the check blocks they carry ─────────

@dataclass
class Check:
    """One scenario's executable check: the requirement and scenario it lives under, the parsed
    `(verb, args)` statements, and the verbatim block source (carried to the base and tip runs)."""
    capability: str
    requirement: str
    scenario: str
    statements: list[tuple[str, list[str]]]
    source: str


@dataclass(frozen=True)
class RunOutcome:
    kind: str
    code: int | None = None

    @classmethod
    def completed(cls, code: int) -> "RunOutcome":
        return cls(COMPLETED, code)

    @classmethod
    def overran(cls) -> "RunOutcome":
        return cls(OVERRAN)

    @classmethod
    def could_not_run(cls) -> "RunOutcome":
        return cls(COULD_NOT_RUN)


@dataclass(frozen=True)
class ReverifyFailure:
    kind: str
    capability: str
    message: str


def checks(capability: str, root: str | None = None) -> list[Check]:
    """Every check block in a capability's spec, in document order — empty when the file or its
    blocks are absent (a capability with no executable scenarios is wholly watched)."""
    path = spec.cap_path(capability, root)
    if not os.path.isfile(path):
        return []
    return _parse(open(path, encoding="utf-8").read(), capability)


def classification(capability: str, root: str | None = None) -> list[tuple[str, str]]:
    """Per requirement, `(name, "gated"|"watched")` — gated when one of its scenarios carries a check
    block, watched when none does. The classification is *read off* the blocks, never separately
    authored, so a register and the gates it names cannot disagree (derive-don't-hand-tend)."""
    gated = {c.requirement for c in checks(capability, root)}
    cap = spec.read_spec(root).capability(capability)
    return [(r.name, "gated" if r.name in gated else "watched") for r in cap.requirements] if cap else []


def _parse(text: str, capability: str) -> list[Check]:
    out: list[Check] = []
    req = scen = ""
    block: list[str] | None = None
    for line in text.splitlines():
        s = line.strip()
        if block is not None:
            if s.startswith("```"):
                out.append(Check(capability, req, scen, _statements(block), "\n".join(block)))
                block = None
            else:
                block.append(line)
        elif s.startswith("### Requirement:"):
            req, scen = s.split(":", 1)[1].strip(), ""
        elif s.startswith("#### Scenario:"):
            scen = s.split(":", 1)[1].strip()
        elif s == "```check":
            block = []
    return out


def _statements(lines: list[str]) -> list[tuple[str, list[str]]]:
    return [(t[0], t[1:]) for ln in lines if (t := ln.split())]


# ── the acceptance runner: a capability's scenarios, in-process, against the live engine ──

@dataclass
class Outcome:
    scenario: str
    passed: bool
    detail: str


def run(capability: str, root: str | None = None) -> list[Outcome]:
    """Run every check block of a capability against the live engine — the acceptance path. Each
    scenario gets an isolated fixture (planted, torn down); the scenario passes only when every one of
    its assertions holds."""
    return [_run_one(c) for c in checks(capability, root)]


def run_blocks_file(path: str, capability: str) -> int:
    """Run a carried block file (the gate writes one into each checkout) against THIS checkout's
    engine and return an exit code — 0 when every scenario passed, 1 otherwise. The entry point the
    base/tip subprocess calls; the guard is set so a scenario's own gate check never re-enters here."""
    os.environ[_GATE_GUARD] = "1"
    failed = 0
    for c in _carried(open(path, encoding="utf-8").read(), capability):
        o = _run_one(c)
        print(f"  [{'PASS' if o.passed else 'FAIL'}] {o.scenario}{'' if o.passed else ': ' + o.detail}")
        failed += not o.passed
    return 1 if failed else 0


def _run_one(c: Check) -> Outcome:
    w = worlds.for_capability(c.capability)
    try:
        for verb, args in c.statements:
            ok, detail = w.do(verb, args)
            if not ok:
                return Outcome(c.scenario, False, detail)
        return Outcome(c.scenario, True, "")
    except Exception as e:                                  # a fixture that cannot be built is a red, not a crash
        return Outcome(c.scenario, False, f"{type(e).__name__}: {e}")
    finally:
        w.teardown()


# ── the fold gate: the touched capability's scenarios, red at the base, green at the tip ──

def gate(result, root: str | None = None) -> str | None:
    """The scenario gate — the folding condition that replaces the worker's self-authored loop. For
    each capability the result's delta *touches* that carries scenarios, run the tip's scenarios at the
    fork base (they MUST fail — the behavior was not yet built) and at the tip (they MUST pass), in the
    fence, trusting exit codes. A change folds only when the architect's scenario actually transitioned
    red→green; the worker records nothing the gate trusts. None when every touched capability
    transitioned (or carries no scenarios — watched, never faked).

    The base is the worker's **recorded fork base** (`result.base`), the commit its fence was cut from —
    never `HEAD~1` of the tip, which is the fork base only for a worker that adds exactly one commit. A
    real coding agent self-commits its build, so the tip's parent is the agent's own already-built tree;
    running the base there would find the scenarios already green and false-refuse a correct build.

    Each run carries the tip's **world fixtures** onto the checkout (`_world_source`) beside the tip's
    check source, so a brand-**new** verb already exists at the base run — base-red can then mean only that
    the behavior is genuinely absent, never that the verb was missing, and a vacuous fixture that asserts
    nothing goes green at the base too and cannot clear the gate. The one residue this cannot reach — a
    verb whose fixture needs an engine seam absent at the base — is the watched archive-gate judgment
    (`spec/coherence.md`), never a structural guarantee silently assumed."""
    if os.environ.get(_GATE_GUARD):
        return None                                        # inside a base/tip run — never recurse
    base_ref = getattr(result, "base", "") or "HEAD~1"     # the recorded fork base, never the tip's parent — a self-committing worker makes HEAD~1 its own already-built tree
    ops = delta.parse(result.delta).ops
    for cap in sorted({op.capability for op in ops}):
        src = _check_source(cap, result.worktree)
        if not src:
            continue                                       # a capability with no scenarios is watched, not gated
        cap_ops = [op for op in ops if op.capability == cap]
        if (_adds_only_watched(cap_ops)
                and not _engine_changed(result.worktree, base_ref)
                and _check_blocks_source_at(cap, result.worktree, base_ref) == _check_blocks_source(cap, result.worktree)):
            continue                                       # the delta changed no gated source for this capability
        world = _world_source(cap, result.worktree)        # the tip's fixtures, carried onto the base so a new verb exists there
        budget = _suite_budget(src)
        base = _run_at(src, world, cap, result.worktree, base_ref, budget)
        tip = _run_at(src, world, cap, result.worktree, "HEAD", budget)
        if base.kind == OVERRAN or tip.kind == OVERRAN:
            return (f"resource limit reached while running the scenarios for {cap!r} in the fence — "
                    "retry the fold when the machine has enough headroom")
        if base.kind == COULD_NOT_RUN or tip.kind == COULD_NOT_RUN:
            return (f"the scenarios for {cap!r} could not run in the fence — a scenario that cannot "
                    "run did not gate the behavior")
        if base.code == 0:
            return (f"the scenarios for {cap!r} already passed at the fork base — the change is not "
                    "what makes them green, so it proved nothing")
        if tip.code != 0:
            return (f"the scenarios for {cap!r} did not pass at the tip — the behavior is not green "
                    "after the change")
    return None


def reverify(root: str) -> ReverifyFailure | None:
    """Run every capability's suite on merged main before code-bearing folds commit."""
    if os.environ.get(_GATE_GUARD):
        return None
    for cap in _all_capabilities(root):
        src = _check_source(cap, root)
        if not src:
            continue                                       # a watched capability has nothing to re-verify
        budget = _suite_budget(src)
        run = _run_merged(src, cap, root, budget)
        if run.kind == OVERRAN:
            retry_budget = _retry_budget(budget)
            run = _run_merged(src, cap, root, retry_budget)
            if run.kind == OVERRAN:
                return ReverifyFailure(
                    RESOURCE_LIMIT, cap,
                    f"resource limit reached while re-verifying {cap!r}: the suite overran its "
                    f"{_format_budget(budget)}s budget and its {_format_budget(retry_budget)}s retry "
                    "with headroom. Retry the fold; this is a resource limit, not a broken build.")
        if run.kind == COULD_NOT_RUN:
            return ReverifyFailure(
                COULD_NOT_RUN, cap,
                f"the scenarios for {cap!r} could not run on merged main — a build that cannot be "
                "re-verified does not land")
        if run.code != 0:
            return ReverifyFailure(
                RED, cap,
                f"the scenarios for {cap!r} are red on merged main — the verified fenced build does "
                "not hold once merged (red-on-the-system), so it does not land")
    return None


def _all_capabilities(root: str) -> list[str]:
    """Every capability in the merged spec at `root`, sorted — the whole-system re-verify scope read
    structurally from the spec, so no caller chooses it and the blind spot cannot be reintroduced."""
    return sorted(c.name for c in spec.read_spec(root).capabilities)


def _run_merged(src: str, capability: str, root: str, budget: float) -> RunOutcome:
    """Run the carried scenarios against the merged working tree at `root` in a fresh process, returning
    a typed capped-run outcome. The subprocess runs with `cwd=root`, so
    `python3 -m engine` imports `root`'s on-disk engine — the just-replayed code — and its worlds read
    the merged tree (`root` is the imported engine's default root); the verdict is therefore merged
    main's behavior under the touched capability's scenarios. Its **ambient record root is a throwaway
    sink**, never `root`: the parent fold holds the one record line's `flock` on `root/.git` across this
    call, so any record op the merged engine runs must lock elsewhere or it would deadlock against the
    held line. The guard is set so a scenario that itself folds code does not re-enter re-verification."""
    check_file = os.path.join(root, ".reverify.check")
    sink = tempfile.mkdtemp(prefix="reverify-sink-")
    try:
        _write(check_file, src)
        env = {**os.environ, _GATE_GUARD: "1", "ENGINE_ROOT": sink}
        return _capped_run(["python3", "-m", "engine", "--run-blocks", ".reverify.check",
                            "--cap", capability], root, env, budget)
    finally:
        if os.path.isfile(check_file):
            os.remove(check_file)
        shutil.rmtree(sink, ignore_errors=True)


def _check_source(capability: str, where: str) -> str:
    """The tip's check blocks for a capability, read from the fence's spec and serialized for the
    carried run — each block under a `>>> <scenario>` header the carried parser splits on."""
    path = os.path.join(where, "spec", capability + ".md")
    if not os.path.isfile(path):
        return ""
    parts = [f">>> {c.scenario}\n{c.source}" for c in _parse(open(path, encoding="utf-8").read(), capability)]
    return "\n".join(parts)


def _check_blocks_source(capability: str, where: str) -> str:
    path = os.path.join(where, "spec", capability + ".md")
    if not os.path.isfile(path):
        return ""
    return _check_blocks_source_from_text(open(path, encoding="utf-8").read(), capability)


def _check_blocks_source_at(capability: str, fence: str, ref: str) -> str | None:
    r = subprocess.run(["git", "show", f"{ref}:spec/{capability}.md"], cwd=fence,
                       capture_output=True, text=True)
    return _check_blocks_source_from_text(r.stdout, capability) if r.returncode == 0 else None


def _check_blocks_source_from_text(text: str, capability: str) -> str:
    return "\n---\n".join(c.source for c in _parse(text, capability))


def _adds_only_watched(ops: list[delta.Op]) -> bool:
    return bool(ops) and all(op.verb == "ADDED" and not _parse(op.requirement.block, op.capability)
                             for op in ops)


def _engine_changed(fence: str, base_ref: str) -> bool:
    r = subprocess.run(["git", "diff", "--name-only", base_ref, "HEAD", "--", "engine"], cwd=fence,
                       capture_output=True, text=True)
    return any(line.endswith(".py") for line in r.stdout.splitlines())


def _world_source(capability: str, where: str) -> str | None:
    """The tip's world fixture for a capability — the `_v_<verb>` methods that give its scenario verbs
    meaning (`engine/worlds/<capability>_world.py`), read from the fence so the gate can carry them onto
    each checkout exactly as it carries the check source. None when the capability has no world module.
    Carrying the binding is what lets a brand-new verb exist at the base run: base-red then means the
    behavior is absent, not the verb — a vacuous fixture goes green at the base too and cannot clear the
    gate. The one residue this cannot reach — a verb whose fixture needs an engine seam absent at the
    base — is the watched archive-gate judgment (`spec/coherence.md`)."""
    path = os.path.join(where, "engine", "worlds", capability.replace("-", "_") + "_world.py")
    return open(path, encoding="utf-8").read() if os.path.isfile(path) else None


def _carried(text: str, capability: str) -> list[Check]:
    out: list[Check] = []
    scen, block = "", []
    def flush() -> None:
        if block:
            out.append(Check(capability, "", scen, _statements(block), "\n".join(block)))
    for line in text.splitlines():
        if line.startswith(">>> "):
            flush(); scen, block = line[4:].strip(), []
        else:
            block.append(line)
    flush()
    return out


def _run_at(src: str, world: str | None, capability: str, fence: str, ref: str,
            budget: float) -> RunOutcome:
    """Run the carried scenarios against an isolated checkout of `ref` cut from the fence, returning
    a typed capped-run outcome. A throwaway detached worktree keeps
    the fence's own tip untouched; the carried block file **and the tip's world fixtures** (`world`) ride
    into the checkout, and the checkout's own `engine` runs them — so the verdict is that revision's
    behavior under the tip's scenarios, and a brand-new verb exists even at the base run (its fixture
    carried), so base-red means the behavior is absent, not the verb missing."""
    co = tempfile.mkdtemp(prefix="scenario-gate-")
    try:
        add = subprocess.run(["git", "worktree", "add", "--detach", "-q", co, ref], cwd=fence,
                             capture_output=True, text=True)
        if add.returncode != 0:
            return RunOutcome.could_not_run()
        _write(os.path.join(co, ".scenario-gate.check"), src)
        if world is not None:                              # carry the tip's binding onto the (possibly older) checkout
            _write(os.path.join(co, "engine", "worlds", capability.replace("-", "_") + "_world.py"), world)
        env = {**os.environ, _GATE_GUARD: "1"}
        return _capped_run(["python3", "-m", "engine", "--run-blocks", ".scenario-gate.check",
                            "--cap", capability], co, env, budget)
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", co], cwd=fence,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.rmtree(co, ignore_errors=True)


def _capped_run(argv: list[str], cwd: str, env: dict[str, str], budget: float) -> RunOutcome:
    try:
        r = subprocess.run(argv, cwd=cwd, env=env, timeout=budget,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return RunOutcome.completed(r.returncode)
    except subprocess.TimeoutExpired:
        return RunOutcome.overran()
    except OSError:
        return RunOutcome.could_not_run()


def _suite_budget(src: str) -> float:
    return max(SUITE_TIMEOUT_FLOOR, _scenario_count(src) * SUITE_TIMEOUT_PER_SCENARIO)


def _scenario_count(src: str) -> int:
    return max(1, sum(1 for line in src.splitlines() if line.startswith(">>> ")))


def _retry_budget(budget: float) -> float:
    return budget * SUITE_RETRY_HEADROOM


def _format_budget(budget: float) -> str:
    return str(int(budget)) if budget.is_integer() else f"{budget:.1f}"


def _git(cwd: str, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
