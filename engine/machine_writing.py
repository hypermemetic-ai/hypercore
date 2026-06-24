"""writing-for-the-machine's one mechanical aid: a non-blocking signal over the spec's own prose.

The discipline is watched — held by judgment, like `communication`'s clarity. But three of its
constructs are mechanically detectable, so the system raises them as a signal the author weighs, never
a gate the fold must clear: the length tripwire's idiom (a context-cost signal that raises a decision,
never an auto-refusal — `folding-conditions`, `depth`), pointed at writing instead of module length.

The three, each tied to a measured machine-reading failure (the evidence is provenance,
`work/archive/agent-facing-hardening/research.md`, Part C):

- **a sentence past sixty words** — instruction density has a primacy cliff, so obligations after the
  first few are dropped; one over-long sentence is the corpus's densest, most-droppable construct;
- **a compound negation** — two `never`s in one sentence; negation is the most failure-prone
  construction and compounding it is worse, and it defines the wanted behaviour only by what it is not;
- **a provenance reference off the line-end** — an `(ADR NNNN)` wedged mid-clause splits the
  subject–verb–object binding exactly where the model resolves it.

The signal reads the same statements the skills render (`methodology._statement`, the one definition of
a requirement's statement), so it judges precisely the prose that reaches an agent. It returns located
flags; it never raises and never refuses — the caller surfaces them as advice, and the only true verdict
remains the behavioural A/B eval.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from . import methodology, spec

MAX_WORDS = 60                                  # the hard flag for one sentence (research.md, Part C / C.4)
_SENTENCE = re.compile(r"(?<=\.)\s+")           # split a joined statement at a period followed by space
_NEVER = re.compile(r"\bnever\b", re.IGNORECASE)
_REF = re.compile(r"\(ADR \d+\)")               # a provenance reference; flagged only when mid-clause


@dataclass(frozen=True)
class Flag:
    kind: str                                   # "long sentence" | "compound negation" | "mid-clause reference"
    excerpt: str                                # the offending fragment, clipped


@dataclass(frozen=True)
class Signal:
    cap: str
    requirement: str
    flag: Flag


def flags(statement: str) -> list[Flag]:
    """The three-construct detector over one requirement statement — the unit the live scan applies and
    the acceptance check exercises. Pure: a string in, the flags out, never a verdict."""
    out: list[Flag] = []
    for sentence in _SENTENCE.split(statement):
        words = len(sentence.split())
        if words > MAX_WORDS:
            out.append(Flag("long sentence", f"{words} words — {_clip(sentence)}"))
        if len(_NEVER.findall(sentence)) >= 2:
            out.append(Flag("compound negation", _clip(sentence)))
    for m in _REF.finditer(statement):
        tail = statement[m.end():].lstrip()
        if tail and tail[0] not in ".;":        # a word follows the ref → it sits mid-clause, not at line-end
            out.append(Flag("mid-clause reference", _clip(statement[m.start():m.end() + 32])))
    return out


def signals(root: str | None = None) -> list[Signal]:
    """Every flag the spec's own requirement statements raise right now, located by capability and
    requirement — the live, non-gating scan the advisory prints on every check."""
    return [Signal(cap.name, req.name, f)
            for cap in spec.read_spec(root).capabilities
            for req in cap.requirements
            for f in flags(methodology._statement(req))]


def advisory(root: str | None = None) -> list[str]:
    """The signal, formatted for the acceptance harness — a non-gating advisory the author reads as a
    prompt to look. It reports even when clean, so its silence is evidence, not absence."""
    found = signals(root)
    if not found:
        return ["  writing-for-the-machine — advisory signal: no construct flagged (non-gating)"]
    head = f"  writing-for-the-machine — advisory signal: {len(found)} flagged for judgment (non-gating)"
    return [head] + [f"    · {s.cap} / {s.requirement}: {s.flag.kind} — {s.flag.excerpt}" for s in found]


def _clip(text: str, width: int = 84) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[:width] + "…"
