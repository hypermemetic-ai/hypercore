surfaced: 0

[CONTRACT]
Make the `fold:` and `dispatch:` commit subjects a fenced crossing composes read as faithful operator-facing provenance instead of a crude truncation. Two engine seams compose them: `tree._subject(text)` (engine/tree.py) backs every machine commit's subject — file-intent, spawn, approve, settle, cut, dispatch, recover, raise, hold, grill, and the fold's own fallback — and `delta.fold` (engine/delta.py) composes `fold: {subject} → {label}`. Today `_subject` is `" ".join(text.split())[:50]`: it leaks a leading `# ` heading marker and hard-cuts mid-token at fifty characters, so the first live crossing recorded `fold: # the-candidate-prompt-speaks-as-the-architect — t → channels`; and `label` falls back to the literal `"channels"` for a trivial delta that touched no capability. Harden `tree._subject` so it takes the node's first non-empty line, strips the leading heading marker, and cuts on a word boundary (never mid-token) under a generous limit — so every one of its call sites, the dispatch subject and the eight other machine commits included, reads the node's real title and summary. Replace the `"channels"` label sentinel with the capability the fold actually routed to: the capabilities the delta touched when it touched any, otherwise an honest token for what the fold did — `code` for a code-only crossing, `no-op` for one that changed neither spec nor code — never `channels`, which named a capability the fold merely re-rendered. This adds one gated self-model requirement and its scenario, implemented by a `fold faithful` mode and a `faithful` assertion in engine/worlds/self_model_world.py: fold a trivial delta on a node whose title carries a `# ` marker, then assert the composed `fold:` subject strips the marker, carries the node's real one-line summary, and names an honest label — never the `channels` sentinel. The scenario is red on today's engine (marker leaked, label `channels`) and green on the fix.

[DELTA]
# delta — the-fold-commit-speaks-faithfully

## ADDED — self-model
### Requirement: a fenced crossing's commit subject is faithful provenance
The `fold:` and `dispatch:` commit subjects a fenced crossing composes MUST read as faithful
operator-facing provenance, not a crude truncation. Each carries the node's title with its leading
heading marker stripped and a real one-line summary cut on a word boundary — never a `# ` leaked from
the body, never a fragment severed mid-token. The `fold:` subject names the capability the change
actually routed to: the capabilities its delta touched when it touched any, and otherwise an honest
token for what the fold did — `code` for a code-only crossing, `no-op` for one that changed neither
spec nor code — never the `channels` sentinel, which names a capability the fold merely re-rendered.
The one subject composer (`tree._subject`) backs every machine commit, so this faithfulness reaches the
dispatch subject and the eight other machine commits through the same seam.

#### Scenario: a trivial crossing's fold subject reads true
- WHEN a fenced crossing folds a trivial delta whose node title carries a leading heading marker
- THEN the composed `fold:` subject strips the marker, carries the node's real one-line summary cut on
  a word boundary, and names an honest capability — never the `channels` no-capability sentinel

  ```check
  fold faithful
  faithful
  ```
