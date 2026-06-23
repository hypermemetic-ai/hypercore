"""The living spec, read from disk into a structured model.

The agent's render of the self-model: the spec is **one specification**, segmented into capabilities
for reading — each a flat `spec/<capability>.md` listing requirements with scenarios (depth among
them, a capability like the rest — ADR 0019). The ubiquitous-language `glossary.md` is root-level
(ADR 0018). A capability bears no material of its
own (a section of a document, not a node), so its on-disk form is a flat file, never a folder — the
folder shape is reserved for what genuinely bears material, the tree node (ADR 0014). A capability is
told from a cross-cutting segment by content: it declares `### Requirement:`.

This module is the one place that knows the on-disk shape; everything else (the delta, the operator
view) works against the structure it returns, so the markdown form can change without touching them.
Read live every time, like the tree — never cached.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from . import tree  # for _root only — the spec lives beside the tree

REQ = "### Requirement:"


@dataclass
class Requirement:
    name: str
    block: str                       # the exact source, heading through last line

    @property
    def scenarios(self) -> list[str]:
        return [ln.split(":", 1)[1].strip()
                for ln in self.block.splitlines()
                if ln.startswith("#### Scenario:")]


@dataclass
class Capability:
    name: str
    requirements: list[Requirement] = field(default_factory=list)

    def requirement(self, name: str) -> Requirement | None:
        return next((r for r in self.requirements if r.name == name), None)


@dataclass
class Spec:
    capabilities: list[Capability] = field(default_factory=list)
    glossary: str = ""

    def capability(self, name: str) -> Capability | None:
        return next((c for c in self.capabilities if c.name == name), None)


def spec_dir(root: str | None = None) -> str:
    return os.path.join(root or tree._root(), "spec")


def cap_path(name: str, root: str | None = None) -> str:
    return os.path.join(spec_dir(root), name + ".md")


def read_spec(root: str | None = None) -> Spec:
    d = spec_dir(root)
    if not os.path.isdir(d):
        return Spec()
    caps = []
    for fname in sorted(os.listdir(d)):
        if not fname.endswith(".md"):
            continue                              # decisions/ is a dir; skip non-.md entries
        reqs = _requirements(open(os.path.join(d, fname)).read())
        if reqs:                                  # a capability declares requirements; glossary/depth do not
            caps.append(Capability(fname[:-3], reqs))
    gloss = os.path.join(root or tree._root(), "glossary.md")   # root-level ubiquitous language (ADR 0018)
    glossary = open(gloss).read() if os.path.isfile(gloss) else ""
    return Spec(caps, glossary)


def _requirements(text: str) -> list[Requirement]:
    """Split a capability file into requirement blocks at each `### Requirement:`."""
    out: list[Requirement] = []
    block: list[str] = []
    for line in text.splitlines():
        if line.startswith(REQ):
            if block:
                out.append(_req(block))
            block = [line]
        elif block:
            block.append(line)
    if block:
        out.append(_req(block))
    return out


def _req(block: list[str]) -> Requirement:
    name = block[0].split(":", 1)[1].strip()
    return Requirement(name, "\n".join(block).rstrip() + "\n")
