---
id: doc-49
title: Mount set roots instead of mirroring members
type: guide
created_date: '2026-07-17 03:30'
updated_date: '2026-07-17 03:30'
tags:
  - solution
  - install
  - drift
  - by-construction
---
# Mount set roots instead of mirroring members

## Symptom

A new shared Skill landed in the methodology Repository and no runtime saw
it: per-member symlinks were live for edits to existing members but silent
for additions and removals, and the installer that reconciled membership had
to be remembered — nobody re-ran it. A linked Repository's glossary forked
the same way: its local file held only project terms, so agents there never
saw the canonical vocabulary the shared Skills are written in.

## Root cause

Mirroring. Each member of a consumed set (Skills, commands, glossary terms)
had its own link or copy, which makes set membership itself state that must
be reconciled. Every reconciler needs a trigger, no trigger existed at the
moment membership changed, and the drift stayed invisible until a failure
surfaced it. Symlinks per member solve content staleness, never membership
staleness.

## Resolution

Mount the set's root instead of mirroring its members: one whole-directory
symlink per runtime for Skills, one PATH entry for commands, one live link
to the canonical glossary plus a local appendix (append, never redefine) for
vocabulary. Day-0 bootstrap becomes the only installation act; afterward
every addition, removal, and edit is live by construction and the installer
ceases to exist. Residual truths that survive the principle:

- Per-consumer values that must differ (a project's own convention fields)
  cannot be mounted; they still need conformance Checks or push-based
  propagation to stay aligned.
- Anything that writes into a mounted root now writes into the source
  Repository. That visibility is the desired behavior — foreign writes
  surface as untracked files for operator disposition — not a defect.
- A file read by CI in a bare checkout cannot be an absolute-path link:
  point read-based Checks at files that exist in the checkout and pin the
  link itself with a dereference-free readlink contract.

## Verification

Landed and operator-merged as qq #119 (installer retirement, Skill and
command mounts), qq #121 (canonical glossary with local appendix), and
deciq #51 (adoption with repointed read Checks and a readlink contract). A
headless runtime discovered the full Skill set through the mount, including
a Skill nothing had ever linked; the shell-fragment battery proved
idempotence, shadow ordering, empty-entry preservation, and namespace
hygiene; the linked Repository's full CI suite ran green against the
dangling canonical link; and the primary checkout surfaced a foreign Skill
write the same day, demonstrating the visibility property in production.
