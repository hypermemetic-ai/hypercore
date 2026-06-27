"""The vocabulary folding condition — glossary consistency over the live corpus.

The condition owns the whole corpus read it needs: `glossary.md`, `intent.md`, and
the flat `spec/*.md` traversal. Callers hand it only the corpus root; the glossary
format, the corpus assembly, and the orphan-term verdict stay hidden here.
"""
from __future__ import annotations

import os
import re

from . import spec

_STOP = {"the", "a", "an", "of", "and", "or", "to", "its", "it", "is", "in", "on", "as", "at", "by"}


def check(root: str | None = None) -> str | None:
    """The fold's vocabulary verdict, or None when the gated floor is met.

    Today this is only the gated floor: a term `glossary.md` defines but the live
    corpus no longer uses. The watched semantic half remains held not-yet until
    its dedicated run exists, so a corpus consistent on the floor folds.
    """
    gloss = _glossary(root)
    if gloss is None:
        return None
    orphan = _orphan_term(gloss, _other_corpus(root))
    if orphan:
        return (f"decision — vocabulary: the live corpus no longer uses the defined term "
                f"'{orphan}' — define / waive / dismiss. A defined term fallen out of use is the "
                f"glossary out of step with the language; the fold is held until you settle it.")
    return None


def _orphan_term(gloss: str, other: str) -> str | None:
    """The first defined term the corpus no longer uses, excluding its own glossary line."""
    lines = gloss.splitlines()
    heads = [(i, m.group(1)) for i, ln in enumerate(lines)
             if (m := re.match(r"\s*-\s+\*\*(.+?)\*\*", ln))]
    for i, head in heads:
        text = _norm(other + "\n" + "\n".join(ln for j, ln in enumerate(lines) if j != i))
        if not all(w in text for w in _words(head)):
            return head
    return None


def _glossary(root: str | None) -> str | None:
    path = os.path.join(_corpus_root(root), "glossary.md")
    return open(path, encoding="utf-8", errors="ignore").read() if os.path.isfile(path) else None


def _other_corpus(root: str | None) -> str:
    """The live corpus minus the glossary: `intent.md` and every `spec/*.md` file."""
    base, parts = _corpus_root(root), []
    intent = os.path.join(base, "intent.md")
    if os.path.isfile(intent):
        parts.append(open(intent, encoding="utf-8", errors="ignore").read())
    spec_dir = spec.spec_dir(root)
    if os.path.isdir(spec_dir):
        parts += [open(os.path.join(spec_dir, f), encoding="utf-8", errors="ignore").read()
                  for f in sorted(os.listdir(spec_dir)) if f.endswith(".md")]
    return "\n".join(parts)


def _corpus_root(root: str | None) -> str:
    return os.path.dirname(spec.spec_dir(root))


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text.lower()))


def _words(text: str) -> list[str]:
    return [w for w in _norm(text).split() if w not in _STOP and len(w) >= 3]
