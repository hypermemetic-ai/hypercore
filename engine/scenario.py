"""The scenario binding — a capability's prose scenario IS its executable check.

The self-model is self-verifying: a `#### Scenario:` in `spec/<capability>.md` carries a fenced
``` ```check ``` ``` block of **domain verbs**, and this module is the deep layer that turns those
verbs into a runnable assertion over the real engine seams. The architect authors the verbs (the
high-signal WHEN/THEN interface); the worker turns them red→green; nothing below the seam is the
architect's to write, and there is no escape hatch into raw code — a scenario that needs something
the vocabulary cannot say either earns a new verb here, in the same edit, or stays *watched*. So the
builder can never author the oracle that judges it, and the description of a behavior cannot drift
from the behavior, because the description is the test. *(design-decision: `binding-contest`.)*

The verbs name domain nouns, never engine symbols or paths-into-the-code, so a worker rewriting the
engine has nothing in the scenario to tamper with to pass. The per-capability vocabularies and the
fixtures they drive live in `engine/worlds/` — **one module per capability** (folding-conditions'
`grow` / `accept` / `gate` / `spec` drive the real `conditions` gate over a planted fixture) — so no
single file carries every capability's verbs, and the vocabulary extends one verb at a time as each
migrating capability first needs it (`spec/depth.md`'s locality discipline), never pre-built. This
module reaches a capability's world through the one `worlds.for_capability` seam.

Two runners share the one interpreter:

- **run** — the acceptance path. A capability's check blocks run in-process against the live engine
  (green here means the system meets its own spec right now). This is what `python3 -m engine --check`
  reads instead of a by-slice harness.
- **gate** — the fold gate (replacing the worker's self-authored loop). The capability a behavior
  change *touches* has its tip scenarios run at the fork base (must be red — the behavior was not yet
  built) and at the tip (must be green), trusting exit codes, so a change folds only when the
  architect's scenario actually transitioned.

The gated/watched classification is **derived, not hand-tended**: a requirement is gated exactly when
one of its scenarios carries a check block, watched when none does (`scenario.classification`). The
register cannot drift from what is actually gated, because the block's presence *is* the register.
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
    transitioned (or carries no scenarios — watched, never faked)."""
    if os.environ.get(_GATE_GUARD):
        return None                                        # inside a base/tip run — never recurse
    for cap in sorted({op.capability for op in delta.parse(result.delta).ops}):
        src = _check_source(cap, result.worktree)
        if not src:
            continue                                       # a capability with no scenarios is watched, not gated
        base, tip = _run_at(src, cap, result.worktree, "HEAD~1"), _run_at(src, cap, result.worktree, "HEAD")
        if base is None or tip is None:
            return (f"the scenarios for {cap!r} could not run in the fence — a scenario that cannot "
                    "run did not gate the behavior")
        if base == 0:
            return (f"the scenarios for {cap!r} already passed at the fork base — the change is not "
                    "what makes them green, so it proved nothing")
        if tip != 0:
            return (f"the scenarios for {cap!r} did not pass at the tip — the behavior is not green "
                    "after the change")
    return None


def _check_source(capability: str, where: str) -> str:
    """The tip's check blocks for a capability, read from the fence's spec and serialized for the
    carried run — each block under a `>>> <scenario>` header the carried parser splits on."""
    path = os.path.join(where, "spec", capability + ".md")
    if not os.path.isfile(path):
        return ""
    parts = [f">>> {c.scenario}\n{c.source}" for c in _parse(open(path, encoding="utf-8").read(), capability)]
    return "\n".join(parts)


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


def _run_at(src: str, capability: str, fence: str, ref: str) -> int | None:
    """Run the carried scenarios against an isolated checkout of `ref` cut from the fence, returning
    the exit code (None when the checkout or run could not happen). A throwaway detached worktree keeps
    the fence's own tip untouched; the carried block file rides into the checkout, and the checkout's
    own `engine` runs it — so the verdict is that revision's behavior under the tip's scenarios."""
    co = tempfile.mkdtemp(prefix="scenario-gate-")
    try:
        add = subprocess.run(["git", "worktree", "add", "--detach", "-q", co, ref], cwd=fence,
                             capture_output=True, text=True)
        if add.returncode != 0:
            return None
        _write(os.path.join(co, ".scenario-gate.check"), src)
        env = {**os.environ, _GATE_GUARD: "1"}
        try:
            r = subprocess.run(["python3", "-m", "engine", "--run-blocks", ".scenario-gate.check",
                                "--cap", capability], cwd=co, env=env, timeout=180,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return r.returncode
        except (OSError, subprocess.SubprocessError):
            return None
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", co], cwd=fence,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.rmtree(co, ignore_errors=True)


def _git(cwd: str, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
