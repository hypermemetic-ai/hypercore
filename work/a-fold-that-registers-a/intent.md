---
kind: ask
state: in flight
owner: operator
created: 1782608910
---
A fold that registers a new methodology cannot self-materialize its skill in the same process — `channels.CHANNELS` is frozen at module import, so the fold that adds a methodology to the registry renders the static channels from the pre-registration registry, leaving the new skill file and the anchor's skills index unwritten until a fresh `channels.materialize` runs in a new process.

Discovered on the `worker-disciplines-become-a-loadable-skill` fold (2026-06-27): registering `worker` in `methodology.METHODOLOGIES` and folding in one act materialized the channels with the pre-replay registry, so `skills/worker/SKILL.md`, `.claude/skills/worker/SKILL.md`, and the `AGENTS.md` skills-index line were never written — the crossing's architect had to re-run `channels.materialize` in a fresh process to reconcile the drift (commit c699304). The channel-drift audit (`audit — every committed derived channel matches a fresh render`) DOES catch the gap red, so nothing ships silently broken; but the fold that registers a methodology should re-derive the registry after the code replay so it materializes the skill it just registered, rather than leaning on a manual follow-up the audit would otherwise fail on.

To surface in grilling: whether `delta.fold` should re-derive `channels.CHANNELS` after the verified code is replayed onto the merged tree and before `channels.materialize`, so a methodology-registering fold is self-consistent in one act; whether this generalizes to any module-level registry the replayed code mutates, not only `METHODOLOGIES`; and a red->green scenario — a fold that registers a new methodology materializes that methodology's skill and anchor-index line in the same act, with no post-fold drift.
