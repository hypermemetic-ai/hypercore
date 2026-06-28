"""The channels scenario world — the derived static channels, driven through the real `delta.fold`
render step, `methodology.skill`, `anchor`, and `channels.materialize` over a seeded, isolated tree.

The verbs name channels' domain nouns — a source planted with a sentinel, the fold that re-renders the
channel, the methodology skill single-sourced from its slice, the minimal anchor and its derived index,
the discovery standard the materialized channels must meet and the pointers they must resolve — never
engine symbols, so a worker rewriting the render has nothing in the scenario to tamper with to pass.
The fixture seeds hypercore's own spec and glossary into an isolated `ENGINE_ROOT` git repo (so every
skill renders from a real slice and every `spec/<cap>.md` pointer resolves within one self-consistent
tree — the slice-22 idiom), and a `plant` verb overwrites one slice with a sentinel so a fold-rendered
artifact must reproduce THIS source, not a frozen copy. The root and `ENGINE_ROOT` are restored and
dropped on teardown.

The conformance scenario carries a real red→green: the discovery standard is RED against the pre-fix
render (skills in the bare root only, no `CLAUDE.md` bridge) and GREEN against the live channels (the
`.claude/skills/` mirror and the bridge), driven, not narrated.
"""
from __future__ import annotations

import os
import re
import shutil
import tempfile

from .. import anchor, audit, channels, delta, methodology, spec, tree, worker
from ..scenario import _git                                  # the worlds share the core's git helper
from . import World as _Base

_REAL = tree._DEFAULT_ROOT                                   # hypercore's own spec, seeded so the renders self-host
_NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")                 # Claude Code: lowercase/digit/hyphen, ≤64
_DESC_MAX = 1024                                             # Claude Code: description non-empty, ≤1024
_TRIVIAL = "# delta — trivial (no behavior change)"


def _planted(cap: str, nonce: str) -> str:
    """A controlled capability slice carrying a sentinel in its preamble and in a requirement's
    statement — a fold-rendered channel must reproduce THIS source, not a frozen copy or the fallback."""
    return (f"# {cap}\n\n"
            f"Planted overview — {nonce}: the rendered channel must reproduce this source.\n\n"
            f"### Requirement: a planted discipline\nThe agent MUST hold the planted discipline — {nonce}-stmt.\n"
            f"#### Scenario: the discipline holds\n- WHEN a planted thing is judged\n- THEN it applies\n")


def _discovery_ok(root: str) -> bool:
    """The discovery standard: every skill present under `.claude/skills/<cap>/SKILL.md` (where Claude
    Code discovers them) and a `CLAUDE.md` bridge importing the anchor (`@AGENTS.md`)."""
    landed = all(os.path.isfile(os.path.join(root, methodology.skill_path(cap, os.path.join(".claude", "skills"))))
                 for cap in methodology.METHODOLOGIES)
    bridge = os.path.join(root, anchor.BRIDGE_PATH)
    return landed and os.path.isfile(bridge) and "@AGENTS.md" in open(bridge, encoding="utf-8").read()


def _frontmatter_ok(cap: str, text: str) -> bool:
    """The rendered skill's frontmatter meets the documented schema: a `name` equal to its directory
    and matching the field's character limits, and a non-empty `description` within the length limit."""
    if not text.startswith("---\n"):
        return False
    fm = {}
    for line in text[4:text.find("\n---", 4)].splitlines():
        if ": " in line:
            k, v = line.split(": ", 1)
            fm[k.strip()] = v.strip()
    name, desc = fm.get("name", ""), fm.get("description", "")
    return bool(_NAME_RE.match(name)) and name == cap and 0 < len(desc) <= _DESC_MAX


def _pointers(text: str) -> list[str]:
    """The repo-relative pointers a rendered artifact carries — backtick-quoted `spec/<cap>.md` paths
    and `@AGENTS.md` import targets — the links that must resolve to a real file."""
    return re.findall(r"`(spec/[\w./-]+\.md)`", text) + re.findall(r"(?m)^@([\w./-]+)\s*$", text)


class World(_Base):
    """A scenario's fixture: an isolated, git-backed `ENGINE_ROOT` seeded with hypercore's own spec and
    glossary, the real fold / skill render / anchor / `channels.materialize` run over it. `plant`
    overwrites a slice with a sentinel; `fold` runs the fold's render step; `materialize` runs the live
    channel render; the assertion verbs read what landed, what it derived from, and its conformance."""

    def __init__(self):
        self._prev_root = os.environ.get("ENGINE_ROOT")
        self.root = tempfile.mkdtemp(prefix="scenario-channels-")
        os.environ["ENGINE_ROOT"] = self.root              # the spec/tree/channel seams read the ambient root
        for cmd in (("init", "-q"), ("config", "user.email", "scenario@hypercore"),
                    ("config", "user.name", "scenario")):
            _git(self.root, *cmd)
        shutil.copytree(os.path.join(_REAL, "engine"), os.path.join(self.root, "engine"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(os.path.join(_REAL, "spec"), os.path.join(self.root, "spec"),
                        ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("glossary.md", "intent.md"):
            shutil.copyfile(os.path.join(_REAL, name), os.path.join(self.root, name))
        _git(self.root, "add", "-A"); _git(self.root, "commit", "-qm", "seed: hypercore's own spec")
        self._nonce = "ZQX-channel-sentinel"
        self._cap = "depth"                                 # the slice a plant overwrites
        self._new_cap = "fold-born"
        self._art = None                                    # the planted capability's skill artifact
        self._anchor = None                                 # the rendered anchor text

    # ── action verbs ──────────────────────────────────────────────────────────────
    def _v_plant(self, args: list[str]) -> tuple[bool, str]:
        """plant [cap] — overwrite a slice (default `depth`) with a sentinel source and remove its prior
        skill artifact, so the proof is that the FOLD rendered it from THIS source, not that it lingered."""
        self._cap = args[0] if args else "depth"
        tree.atomic_write(spec.cap_path(self._cap, self.root), _planted(self._cap, self._nonce))
        self._art = os.path.join(self.root, methodology.skill_path(self._cap))
        if os.path.isfile(self._art):
            os.remove(self._art)
        return True, ""

    def _v_fold(self, args: list[str]) -> tuple[bool, str]:
        """fold — run a fold; its render step re-derives every static channel from the current source."""
        delta.fold(delta.parse(_TRIVIAL), self.root)
        return True, ""

    def _v_edit(self, args: list[str]) -> tuple[bool, str]:
        """edit — change the planted source, so a later fold must re-render the channel to follow it."""
        src = spec.cap_path(self._cap, self.root)
        tree.atomic_write(src, _planted(self._cap, self._nonce).replace(self._nonce, "EDITED-" + self._nonce))
        return True, ""

    def _v_materialize(self, args: list[str]) -> tuple[bool, str]:
        """materialize — run the live channel render (the fold's render step in isolation): every skill
        into both locations, the anchor, and the `CLAUDE.md` bridge."""
        channels.materialize(self.root)
        return True, ""

    def _v_register_methodology(self, args: list[str]) -> tuple[bool, str]:
        """register-methodology — a code-bearing fold replays engine code that registers a new
        methodology while its delta adds that methodology's spec slice."""
        rel = os.path.join("engine", "methodology.py")
        path = os.path.join(self.root, rel)
        base = open(path, encoding="utf-8").read()
        tip = _with_registered_methodology(base, self._new_cap)
        d = delta.parse(_new_methodology_delta(self._new_cap))
        delta.fold(d, self.root, code={rel: worker.CodeFile(base, tip)})
        return True, ""

    def _v_old_render(self, args: list[str]) -> tuple[bool, str]:
        """old-render — reconstruct the pre-fix render: skills in the bare root `skills/` only, the
        anchor with no `CLAUDE.md` bridge — the targeting defect, rebuilt so the gate can be shown RED."""
        for cap in methodology.METHODOLOGIES:
            methodology.materialize(cap, self.root, skill_dir="skills")
        anchor.materialize(self.root)
        return True, ""

    def _v_anchor(self, args: list[str]) -> tuple[bool, str]:
        """anchor — render the shared anchor (the agents file)."""
        self._anchor = anchor.agents_file(self.root)
        return True, ""

    # ── assertion verbs ───────────────────────────────────────────────────────────
    def _v_materialized(self, args: list[str]) -> tuple[bool, str]:
        """materialized — the fold wrote the planted capability's skill artifact to disk."""
        return ((True, "") if os.path.isfile(self._art)
                else (False, "the fold did not materialize the channel on disk"))

    def _v_derived(self, args: list[str]) -> tuple[bool, str]:
        """derived — the artifact is the pure render of its planted source: it carries the sentinel and
        equals the render of that source exactly, nothing hand-authored."""
        rendered = open(self._art, encoding="utf-8").read()
        if self._nonce not in rendered or self._nonce + "-stmt" not in rendered:
            return False, "the artifact was not rendered from the planted source"
        return ((True, "") if rendered == methodology.skill(self._cap, self.root)
                else (False, "the artifact is not exactly the render of its source"))

    def _v_follows(self, args: list[str]) -> tuple[bool, str]:
        """follows — a later fold re-rendered the channel from the changed source: a committed channel
        cannot drift."""
        return ((True, "") if "EDITED-" + self._nonce in open(self._art, encoding="utf-8").read()
                else (False, "the channel did not follow its changed source — a committed channel drifted"))

    def _v_skill_rendered(self, args: list[str]) -> tuple[bool, str]:
        """skill-rendered — the methodology skill is a progressive-disclosure SKILL.md that renders the
        slice's overview and discipline statement and points back to the slice as its single source."""
        sk = methodology.skill(self._cap, self.root)
        if not (sk.startswith("---") and f"name: {self._cap}" in sk):
            return False, "the skill is not a SKILL.md naming its capability"
        if self._nonce not in sk or self._nonce + "-stmt" not in sk:
            return False, "the skill does not render the slice's overview and discipline statement"
        return ((True, "") if f"spec/{self._cap}.md" in sk
                else (False, "the skill does not point back to its slice as the single source"))

    def _v_single_sourced(self, args: list[str]) -> tuple[bool, str]:
        """single-sourced — the skill carries the discipline statements but leaves the scenarios in the
        slice (progressive disclosure), so there is no second copy of the requirement set to drift."""
        sk = methodology.skill(self._cap, self.root)
        return ((True, "") if "a planted thing is judged" not in sk
                else (False, "the skill copied the slice's scenarios — not progressive disclosure"))

    def _v_minimal(self, args: list[str]) -> tuple[bool, str]:
        """minimal — the anchor carries the non-inferable operational lines (the check command, the
        build-deep discipline, and the hand-back convention) and nothing inferable: no per-capability
        requirements, no code, no prose."""
        if anchor.CHECK not in self._anchor:
            return False, "the anchor drops the non-inferable check command"
        if "build deep" not in self._anchor.lower():
            return False, ("the anchor drops the build-deep discipline — the builder's proactive defense; "
                           "without it the always-on context reverts to the whole-tree check as the build bar")
        if "for the machine" not in self._anchor or "operator-facing word" not in self._anchor:
            return False, "the anchor drops the build/hand-back convention"
        if "### Requirement:" in self._anchor or "import " in self._anchor or "You are hypercore" in self._anchor:
            return False, "the anchor carries inferable content — a requirement, code, or identity prose"
        return True, ""

    def _v_index_derived(self, args: list[str]) -> tuple[bool, str]:
        """index-derived — the anchor's skills index is pulled from the channels' registry: every
        registered skill is listed, and a newly registered one appears by construction."""
        if not ("`depth`" in self._anchor and all(f"`{c}`" in self._anchor for c in methodology.METHODOLOGIES)):
            return False, "the anchor's index does not list every registered skill"
        methodology.METHODOLOGIES["__planted__"] = "a planted methodology — load when testing drift."
        try:
            return ((True, "") if "`__planted__`" in anchor.agents_file(self.root)
                    else (False, "a newly registered skill did not appear in the index by construction"))
        finally:
            del methodology.METHODOLOGIES["__planted__"]

    def _v_bridge(self, args: list[str]) -> tuple[bool, str]:
        """bridge — the derived `CLAUDE.md` bridge imports the anchor (`@AGENTS.md`), the way Claude Code
        reaches an anchor it would otherwise not read."""
        return ((True, "") if "@AGENTS.md" in anchor.bridge(self.root)
                else (False, "the CLAUDE.md bridge does not import the anchor"))

    def _v_discovery_red(self, args: list[str]) -> tuple[bool, str]:
        """discovery-red — the pre-fix render fails the discovery standard (skills in the bare root only,
        no bridge), as the system would have before the targeting fix."""
        return ((True, "") if not _discovery_ok(self.root)
                else (False, "the pre-fix render passed the discovery standard — the red half is not real"))

    def _v_discovery_green(self, args: list[str]) -> tuple[bool, str]:
        """discovery-green — the live channels land skills where the harness discovers them and bridge
        the anchor, so the discovery standard passes."""
        return ((True, "") if _discovery_ok(self.root)
                else (False, "the live channels did not meet the discovery standard"))

    def _v_conforms(self, args: list[str]) -> tuple[bool, str]:
        """conforms — every rendered skill's frontmatter meets the documented SKILL.md schema."""
        bad = [c for c in methodology.METHODOLOGIES
               if not _frontmatter_ok(c, open(os.path.join(self.root, methodology.skill_path(c)), encoding="utf-8").read())]
        return (True, "") if not bad else (False, f"a rendered skill's frontmatter does not conform: {bad}")

    def _v_resolves(self, args: list[str]) -> tuple[bool, str]:
        """resolves — every pointer a rendered artifact carries (`spec/<cap>.md`, `@AGENTS.md`) names a
        file that exists, so a moved slice fails loudly here instead of silently."""
        arts = [os.path.join(self.root, methodology.skill_path(c)) for c in methodology.METHODOLOGIES]
        arts += [os.path.join(self.root, anchor.PATH), os.path.join(self.root, anchor.BRIDGE_PATH)]
        broken = [f"{os.path.basename(a)}→{p}" for a in arts
                  for p in _pointers(open(a, encoding="utf-8").read())
                  if not os.path.isfile(os.path.join(self.root, p))]
        return (True, "") if not broken else (False, f"a rendered pointer does not resolve: {broken}")

    def _v_skill_materialized(self, args: list[str]) -> tuple[bool, str]:
        """skill-materialized — the methodology registered by replayed code has both skill artifacts,
        and they are the same render of the new spec slice."""
        paths = [os.path.join(self.root, methodology.skill_path(self._new_cap, d))
                 for d in methodology.SKILL_DIRS]
        missing = [p for p in paths if not os.path.isfile(p)]
        if missing:
            return False, f"the fold did not materialize the new methodology skill: {missing}"
        texts = [open(p, encoding="utf-8").read() for p in paths]
        want = (f"name: {self._new_cap}", f"spec/{self._new_cap}.md",
                f"{self._new_cap} discipline")
        if texts[0] != texts[1] or not all(w in texts[0] for w in want):
            return False, "the new methodology skills are not faithful mirrored renders"
        return True, ""

    def _v_index_lists_new(self, args: list[str]) -> tuple[bool, str]:
        """index-lists-new — the anchor's derived skills index lists the methodology registered by the
        replayed code, proving it read the merged registry."""
        text = open(os.path.join(self.root, anchor.PATH), encoding="utf-8").read()
        return ((True, "") if f"`{self._new_cap}`" in text
                else (False, "the anchor's skills index does not list the registered methodology"))

    def _v_no_post_fold_drift(self, args: list[str]) -> tuple[bool, str]:
        """no-post-fold-drift — a fresh-process audit of the merged tree sees no channel drift."""
        drift = audit.channel_drift(self.root)
        return (True, "") if not drift else (False, f"post-fold channel drift remains: {drift}")

    def teardown(self) -> None:
        if self._prev_root is None:
            os.environ.pop("ENGINE_ROOT", None)
        else:
            os.environ["ENGINE_ROOT"] = self._prev_root
        shutil.rmtree(self.root, ignore_errors=True)


def _with_registered_methodology(text: str, cap: str) -> str:
    entry = (f'    "{cap}":\n'
             f'        "{cap} methodology - load when testing same-act channel renders.",\n')
    marker = "METHODOLOGIES = {\n"
    if marker not in text:
        raise AssertionError("methodology registry marker not found")
    return text.replace(marker, marker + entry, 1)


def _new_methodology_delta(cap: str) -> str:
    return (f"# delta - register {cap}\n"
            f"## ADDED {cap}\n"
            f"### Requirement: {cap} discipline\n"
            f"The {cap} methodology MUST render from the registry landed by the fold.\n"
            f"#### Scenario: watched\n"
            f"- WHEN the methodology is loaded\n"
            f"- THEN the discipline applies\n")
