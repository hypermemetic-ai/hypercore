---
name: researcher
description: Research the assigned question without modifying the Repository.
# Runtime model-identity verification is assigned to T-95 ticket 3.
model: openai-codex/gpt-5.6-sol
tools: read, grep, find, ls, bash
extensions:
systemPromptMode: replace
inheritProjectContext: false
inheritSkills: false
defaultContext: fresh
acceptanceRole: read-only
completionGuard: false
timeoutMs: 900000
acceptance:
  level: none
  reason: >-
    qq acceptance is the strict completion-envelope schema plus owner
    verification against the tree plus fresh-context review; the
    pi-subagents attestation layer duplicates it and rejects runs whose
    structured-output envelope is already complete (T-124).
---

Research only the assigned question. Return the strict Completion Envelope requested by the parent.
