---
kind: ask
state: done
owner: operator
created: 1782536400
---
# worker-prompt-leads-with-the-task — the ask comes first, and the disciplines read in one pass

The worker reads its mission last. In `worker.prompt` (engine/worker.py) the assembled order is
salutation → the ~2,240-token disciplines → the record grounding → the ~1,481-token depth standards →
**then**, at position five, the ask. A one-pass reader spends its freshest attention on the standing
rulebook before it learns what it is being asked to do.

Lead with the mission. The ask and its handed delta come **right after the salutation**; the
disciplines, the record grounding, and the depth standards follow as "how you are held"; the reply
envelope stays **last** (the transport's reason-first, format-last invariant — `transport.instruction`).

Separately, the worker's own discipline statements are the least one-pass-readable prose in the
system. The writing-for-the-machine advisory flags `spec/worker.md` four times — including the single
longest flagged sentence in the codebase (111 words, the requirement `a worker's RESULT is trusted
only by re-derivation`, `spec/worker.md:249`) and a compound negation ("It holds the spec, never raw
code, and never the operator view", line 43). Rewrite the flagged statements to one instruction per
sentence in positive form, **at their source** (`spec/worker.md`), so the sharpened prose flows into
both the assembled prompt and the rendered disciplines.

Composes with `work/worker-disciplines-become-a-loadable-skill` (both touch `worker.py` and
`spec/worker.md`): this node sharpens the prose at the source and reorders the prompt; that node moves
the channel. Each ADDs or MODIFYs distinct requirements rather than co-MODIFYing one shared
requirement, so two fences do not clobber at fold (`work/worker-builds-proposed-delta`).

## folding condition
- the assembled worker prompt presents the ask and the handed delta before the standing disciplines,
  with the reply envelope still last;
- the `worker` requirement statements that trip the writing-for-the-machine signal (the over-long
  sentence and the compound negation) no longer trip it;
- `python3 -m engine --check` is green.
