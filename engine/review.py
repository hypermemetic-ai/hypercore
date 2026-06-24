"""The architecture review — the standing scan that keeps the system deep.

A periodic scan for complexity debt, run as a standing
process, not a one-off: read live off the source tree every time, never a stored
report. It has two roles, and this module serves both from one scan:

- **The engine of deepening.** It surfaces god-files-in-the-making before they set —
  a module past the length signal, or one nearing it — each as a finding carrying its
  measure and a recommendation strength. This is the complexity debt.
- **The operator view's "what the system is" upper levels.** The same scan
  renders the structural map of as-built reality — every module by length against the
  signal, debt marked — so the operator reads the shape of the system at a glance,
  without reading code. The review is *not a separate artifact*: its output is the
  operator view's as-built and gap (`view.operator_view`), kept honest between folds.

What it measures is **length** — what a module costs a worker's window — which the
depth re-grounding keeps as one **signal** of depth, not the criterion. Depth is
the criterion: a deep module, a lot of behavior behind a small interface. The
deeper, **model-driven red-flag scan** — the deletion test, the shallow-module and
information-leakage flags, testable-through-the-interface — is the depth assessment
this review is meant to grow, and it is **not yet built**. That
shallowness is recorded here and in the operator's gap, never fabricated into a
judgment. Length is the lens this slice ships; the red flags are the lens it will grow.

The record it consults is the accepted-length record `folding-conditions` gates with
(`conditions.accepted`) — one criterion at two scopes: the per-tree gate at the fold,
and this standing whole-tree scan — so a file the gate would raise a decision on is the
same file the review flags, by construction.
"""
from __future__ import annotations

import ast
import os
from dataclasses import dataclass, field

from . import conditions, tree

# A module within this margin of the length signal is a god-file in the making — flagged
# early so deepening pressure is felt before a split is painful. A starting value to
# tune, like the signal itself, not a deep question.
NEAR = int(conditions.SIGNAL * 0.8)
BAR = 20                                  # the visual bar's width, the signal full


@dataclass
class Module:
    """One source file the review measured, with its standing against the length signal.
    `status`: ok | nearing | over | exceeded | accepted. `over` is past the signal with no
    accepted-length record (an item of complexity debt); `accepted` is past the signal but within an
    accepted-length record's accepted length; `exceeded` is past the signal *and* materially
    past the length an accepted-length record once accepted it at — a stale acceptance, the decision
    re-opened. `bar` is that accepted length for accepted/exceeded, else None."""
    rel: str
    lines: int
    status: str
    bar: int | None = None


@dataclass
class Finding:
    """A complexity-debt finding for the backlog. `strength` is the recommendation's
    weight — strong (assess/deepen now) or consider (watch it)."""
    subject: str
    lines: int
    kind: str            # past the length signal | nearing the length signal
    strength: str        # strong | consider
    note: str


@dataclass
class RedFlag:
    """One mechanical structural red flag the standing scan reads without judgment:
    a module-level symbol referenced nowhere in the package (dead code), or an import cycle
    among modules (the structural signature of information leakage — a circular dependency).
    `rule` is the smell, `subject` where it sits, `detail` the recommendation. These are the
    subset a tool can read; the model-driven red-flag *judgments* (shallow module, leakage,
    pass-through) stay judgment and are still not built — recorded, never fabricated."""
    rule: str            # dead symbol | import cycle
    subject: str
    detail: str


@dataclass
class Review:
    modules: list[Module] = field(default_factory=list)   # the structural map, largest first
    findings: list[Finding] = field(default_factory=list)  # the complexity debt (length)
    flags: list[RedFlag] = field(default_factory=list)     # the mechanical structural red flags


# The honest record of what the depth scan does and does not yet reach. The
# mechanical structural subset — dead symbols, import cycles — now runs every scan; the
# model-driven *judgment* (shallow module, information leakage, the deletion test) is judgment
# and stays not-yet-built, surfaced in the operator's gap rather than hidden.
DEPTH_NOT_YET = ("the model-driven red-flag judgment — shallow module, information leakage, the "
                 "deletion test — is judgment, not yet built; the mechanical red flags "
                 "(dead symbols, circular imports) and the length signal are what the scan reads here")


def review(root: str | None = None) -> Review:
    """Scan the source tree live and report. Reads every module's length, places it against
    the length signal, and gathers the ones over (no accepted-length record), past a stale accepted bar
    (exceeded), or nearing it into the complexity debt. A file within its accepted-length record's
    accepted length shows on the map, marked, but is not in the backlog — its size is a recorded
    decision; a file that has outgrown that bar returns to the backlog. The same scan
    reads the mechanical structural red flags (dead symbols, import cycles)."""
    src = os.path.join(root or tree._root(), "engine")
    modules = [_module(rel, n, root) for rel, n in _sources(src)]
    modules.sort(key=lambda m: -m.lines)
    return Review(modules, [f for m in modules if (f := _finding(m))], red_flags(root))


def bars(rv: Review) -> list[str]:
    """The structural map as a visual: each module a bar by length against the signal, debt
    marked. A picture of the system's shape that needs no code read to take in."""
    if not rv.modules:
        return ["(no modules found)"]
    w = max(len(m.rel) for m in rv.modules)
    return [f"{m.rel.ljust(w)}  {_bar(m.lines)}  {m.lines}/{conditions.SIGNAL}{_mark(m)}"
            for m in rv.modules]


def backlog(rv: Review) -> list[str]:
    """The complexity debt as the operator reads it — the gap: the length findings, then the
    mechanical red flags, and **always** the honest record that the model-driven module depth judgment beyond
    them is not yet built. The unbuilt-judgment line is unconditional, not shown only on a clean tree:
    depth is judgment, never a threshold the scan enforces (the depth de-claim), so the review
    states the judgment is unbuilt whether or not a length finding happens to be present — a length
    finding is a context-cost signal, not the module depth judgment, and must never read as one."""
    out = [f"{f.subject}: {f.note} ({f.strength})" for f in rv.findings]
    out += [f"{rf.subject}: {rf.detail} (red flag: {rf.rule})" for rf in rv.flags]
    if not out:
        out = [f"no complexity debt — every module is within the length signal "
               f"({conditions.SIGNAL} lines), no dead symbols, no circular imports"]
    return out + [DEPTH_NOT_YET]


# ── internals ────────────────────────────────────────────────────────────────

def _module(rel: str, n: int, root: str | None) -> Module:
    """Place one module against the signal and its accepted-length record. Past the signal it is
    `accepted` (within the recorded bar + margin), `exceeded` (a bar exists but the file outgrew
    it — the ratchet re-opened the decision), or `over` (no bar at all). The accepted
    bar is consulted from `conditions` so the per-tree gate and this standing scan agree on one
    criterion. Within the signal it is `nearing` or `ok`."""
    canon = _canon(rel)
    if n <= conditions.SIGNAL:
        return Module(rel, n, "nearing" if n >= NEAR else "ok")
    bar = conditions.accepted_at(canon, root)
    if conditions.accepted(canon, n, root):
        return Module(rel, n, "accepted", bar)
    return Module(rel, n, "exceeded", bar) if bar is not None else Module(rel, n, "over")


def _canon(rel: str) -> str:
    """The file's path relative to the repo root (e.g. `engine/foo.py`) — the form the
    accepted-length record names, so the standing scan and the per-tree gate agree."""
    return os.path.join("engine", rel).replace(os.sep, "/")


def _finding(m: Module) -> Finding | None:
    if m.status == "over":
        return Finding(m.rel, m.lines, "past the length signal", "strong",
                       f"{m.lines} lines, past the {conditions.SIGNAL}-line length signal — "
                       "assess its depth (no accepted-length record accepts its size); length is the "
                       "context-cost signal, the red-flag depth scan is not yet built")
    if m.status == "exceeded":
        return Finding(m.rel, m.lines, "past its accepted bar", "strong",
                       f"{m.lines} lines, materially past the {m.bar}-line bar an accepted-length record "
                       "accepted it at — the acceptance is stale; re-cut, deepen, or renew it at "
                       "the new length (acceptance ratchets, it does not silence later growth)")
    if m.status == "nearing":
        return Finding(m.rel, m.lines, "nearing the length signal", "consider",
                       f"{m.lines} lines, nearing the {conditions.SIGNAL}-line length signal — "
                       "a god-file in the making")
    return None


def _bar(n: int) -> str:
    filled = min(BAR, round(n / conditions.SIGNAL * BAR))
    return "█" * filled + "░" * (BAR - filled)


def _mark(m: Module) -> str:
    if m.status == "accepted":
        return f"  (accepted @{m.bar})"
    if m.status == "exceeded":
        return f"  ⚑ grew past its accepted bar of {m.bar} — decision re-opened"
    return {"over": "  ⚑ past the length signal — assess depth",
            "nearing": "  • nearing", "ok": ""}[m.status]


def _sources(src: str) -> list[tuple[str, int]]:
    """Every .py under the source tree, as (path-relative-to-src, line count), for the map."""
    return sorted((os.path.relpath(p, src), _count(p)) for p in _py_paths(src))


def _py_paths(src: str) -> list[str]:
    """Every .py under the source tree, as absolute paths. Recurses into subpackages (the
    per-slice check/), skips bytecode — the one file walk the whole review reads off."""
    out: list[str] = []
    for dirpath, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        out += [os.path.join(dirpath, f) for f in files if f.endswith(".py")]
    return sorted(out)


def _count(path: str) -> int:
    return len(_read(path).splitlines())


def _read(path: str) -> str:
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


# ── the mechanical structural red flags ─────────────────────────────

def red_flags(root: str | None = None) -> list[RedFlag]:
    """The mechanical subset of the depth scan, read live off the engine package: the structural
    red flags a tool can read without judgment — dead module-level symbols and import cycles — so
    they bite every scan, while the model-driven judgment (shallow module, leakage) stays the
    review's to grow. One file walk feeds both rules."""
    files = _py_paths(os.path.join(root or tree._root(), "engine"))
    return _dead_symbols(files) + _import_cycles(files)


def _dead_symbols(files: list[str]) -> list[RedFlag]:
    """Module-level names (assignments, functions, classes) used nowhere in the package — dead
    code, the floor of the nonobvious-code red flag. A name counts as used when it is *loaded* or
    reached as an attribute anywhere in the package's code (`_used_names`) — read off the AST, so
    a mention in a docstring or comment is prose, not a use, and cannot mask a dead symbol.
    Conservative: any real use — by a sibling, a check, or its own module — clears it; dunders are
    framework hooks, skipped."""
    used = _used_names(files)
    defined: dict[str, list[str]] = {}                 # name -> the modules defining it at top level
    for path in files:
        for name in _module_level_names(_read(path)):
            defined.setdefault(name, []).append(_modname(path))
    return [RedFlag("dead symbol", f"{mod}.{name}",
                    "defined at module level but used nowhere in the package — dead; cut it")
            for name, mods in sorted(defined.items())
            for mod in mods
            if name not in used]


def _used_names(files: list[str]) -> set[str]:
    """Every name the package's code *uses* — loaded as a name or reached as an attribute —
    across all files, read off the AST so docstrings, comments, and the definitions themselves
    (assignment targets are stores, not loads) are excluded. The complement of this set, among the
    module-level definitions, is dead code."""
    used: set[str] = set()
    for path in files:
        try:
            tree = ast.parse(_read(path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used.add(node.id)
            elif isinstance(node, ast.Attribute):
                used.add(node.attr)
    return used


def _import_cycles(files: list[str]) -> list[RedFlag]:
    """Import cycles among the package's modules — a circular dependency, the structural signature
    of information leakage (depth.md's gravest red flag after shallowness): two modules that each
    reach into the other cannot be read or changed apart, and usually one is reaching past the
    other's interface. Reads module-level sibling imports; catches the two-module cycle (the
    common shape — a longer ring is the model-driven scan's still-unbuilt job)."""
    deps = {_modname(p): _sibling_imports(_read(p)) for p in files}
    mods, flags, seen = set(deps), [], set()
    for a in sorted(deps):
        for b in sorted(deps[a]):
            if b in mods and a in deps.get(b, set()) and (b, a) not in seen:
                seen.add((a, b))
                flags.append(RedFlag("import cycle", f"{a} ↔ {b}",
                    f"{a} and {b} depend on each other — a circular dependency; pull the shared "
                    "knowledge into a module they both rest on, downward"))
    return flags


def _module_level_names(text: str) -> list[str]:
    """The names a module binds at top level — assignment targets, functions, classes — skipping
    dunders. The granularity dead-code is judged at: a module-level name, not a method or local."""
    try:
        body = ast.parse(text).body
    except SyntaxError:
        return []
    out: list[str] = []
    for node in body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append(node.name)
        elif isinstance(node, ast.Assign):
            out += [t.id for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            out.append(node.target.id)
    return [n for n in out if not n.startswith("__")]


def _sibling_imports(text: str) -> set[str]:
    """The sibling modules a module imports at top level — the edges of the package's import graph.
    The binding edge of `from .x import y` is the **module** `x` (whatever `y` is — a function, a
    class, a constant): importing a symbol depends on its module, not on a sibling that happens to
    share the symbol's name. Only `from . import x, y` names *modules* directly, so its names are
    edges. Reading every imported name as an edge would forge a false cycle the moment a symbol's
    name matched another module's (e.g. `from .transport import render` against the `render` module)
    — a preventable false positive, so it is prevented. Deferred (in-function) imports are left out:
    they do not bind the module at load and are how a real cycle is usually broken."""
    try:
        body = ast.parse(text).body
    except SyntaxError:
        return set()
    out: set[str] = set()
    for node in body:
        if isinstance(node, ast.ImportFrom) and node.level >= 1:
            if node.module:
                out.add(node.module.split(".")[0])       # from .module import sym, … — the module is the edge
            else:
                out.update(a.name for a in node.names)    # from . import module, … — each name is a sibling module
    return out


def _modname(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]
