---
id: doc-95
title: Plan — one-row qq footer approved 2026-07-24
type: specification
created_date: '2026-07-24 18:59'
updated_date: '2026-07-24 18:59'
tags:
  - plan
---
# Plan — one-row qq footer (T-158), approved 2026-07-24

## Intended outcome

Replace the current two-line footer with one terminal row. The row keeps the existing identity/status group (`cwd (branch) • session • statuses`) on the left. A compact group containing context usage, active-provider quota bars when available, and provider/model/thinking is right-aligned on that same row. The `$cost (sub)` segment is removed entirely.

## Ownership boundary

This Change owns `extensions/qq-footer.ts`, `tests/test-qq-footer-extension.sh`, and its Task/plan records. It does not change quota endpoints, polling, parsing, auth, status filtering, Pi core, or unrelated extensions.

## Implementation

1. Delete the now-unused session cost and subscription helpers.
2. Build the compact right-hand group from context usage, optional quota text, and existing provider/model/thinking text.
3. Render one `rightAlignedLine` joining the existing first-row identity/status group with that compact group.
4. Update focused render assertions for one line and the absence of cost/subscription while retaining quota, model alignment, narrow-width, refresh, and provider coverage.

## Success evidence

1. `tests/test-qq-footer-extension.sh` passes and observes the one-row shape plus cost/subscription removal.
2. The full native test suite passes.
3. Fresh diagnostics report no blocking errors in changed source.
4. Fresh-context review accepts the locally verified Change.

## Decision dispositions

The exact one-row outcome, removed cost/subscription segment, preserved remaining segments, and right-aligned compact grouping were approved in the asked-and-answered alignment exchange on 2026-07-24. No broader decision record is required because the decisions are scoped to this Change.
