---
kind: ask
state: standing
owner: operator
created: 2026-06-23
---
# accepted-length-home — a proper home for the accepted-length records

Dissolving the decision corpus left one record homeless: the **accepted-length** record
(`accepted: <path> @<N> — <reason>`), which the depth gate reads every fold. Unlike a decision's
grounds, it is **live state that must outlive the work** that grew the file past the length signal —
so it cannot archive on a node. It now lives in a provisional repo-root `accepted-lengths.md` the
gate reads (`conditions.accepted_at`); there are zero records today, so this was a pure repoint.

Decide its proper home and shape — and the write path, since the operator's acceptance-card flow
that emits these records is not built yet.

## folding condition
- a settled home + shape for accepted-length records; `conditions.accepted_at` reads it; the
  provisional repo-root file is retired; `python3 -m engine --check` is green.
