"""Slice 2 — residue: the glossary's content, awaiting the communication/channels migration.

The self-model half of this slice — the delta, the transactional fold, the operator view's
vision/as-built/gap, and the read that self-hosts hypercore's own capabilities — has migrated to
`self-model`'s own executable scenarios (`spec/self-model.md`, `engine/worlds/self_model_world.py`),
and the fold's atomic-both-directions transactionality with it (slice 19). What stays is the one
communication-facing assertion: the **glossary** the spec yields carries the shared vocabulary —
`thread` defined as the operator's throwaway conversation, and the open *operator view* naming question
flagged honestly rather than silently settled. This is the glossary's *content*, the communication
group's concern (slices 1 / 11 / 12 / 13 / 22), and it stays by-slice until that group migrates, at
which point this file dissolves like the others. Run against hypercore's own seeded glossary.
"""
from __future__ import annotations

import os
import shutil

from .harness import ok


def check(root: str) -> None:
    from .. import spec, tree

    src = tree._DEFAULT_ROOT
    shutil.copytree(os.path.join(src, "spec"), os.path.join(root, "spec"))
    shutil.copyfile(os.path.join(src, "glossary.md"), os.path.join(root, "glossary.md"))
    tree.commit([os.path.join(root, "spec"), os.path.join(root, "glossary.md")],
                "seed: hypercore's own glossary")

    print("\nslice 2 — acceptance check  (residue: the glossary's shared vocabulary)\n")

    glossary = spec.read_spec().glossary
    ok("throwaway conversation" in glossary,
       "the glossary defines thread as the operator's throwaway conversation")
    ok("Open question: the name" in glossary,
       "the glossary flags the open 'operator view' naming question")
