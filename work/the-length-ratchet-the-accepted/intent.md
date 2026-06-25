---
kind: ask
state: standing
owner: operator
created: 1782355621
---
The length ratchet — the accepted-length record that lets a file exceed the length signal when the increase is justified — was built without associated, ratified intent, so its intended behavior has no durable owner and a check has already drifted from it.

Concretely: `engine/check/scenarios.py:108`, the standing "the real engine tree is honestly clean" check, lists `"accepted"` in its failure set — `any(m.status in ("over", "exceeded", "accepted") for m in rv.modules)` — so an engine module past the length signal that carries a *justified* accepted-length record still fails the check. That contradicts the ratchet's purpose (the operator confirmed the intent: a justified increase should be allowed), and it is inconsistent with the rest of the system: the per-tree fold gate (`conditions.accepted`) honors the acceptance, and `review._finding` excludes accepted files from the complexity-debt backlog ("a recorded decision, not debt").

The likely fix is to drop `"accepted"` from that tuple so the standing check reads `("over", "exceeded")`, matching `_finding` and the fold gate — but the deeper ask is to give the ratchet ratified intent so the behavior has a single owner and no check can silently diverge from it again. This wall was hit independently by two sessions in one day, so it is live, not hypothetical.
