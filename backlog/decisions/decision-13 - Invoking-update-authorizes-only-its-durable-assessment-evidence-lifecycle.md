---
id: decision-13
title: Invoking update authorizes only its durable assessment evidence lifecycle
date: '2026-07-24 16:30'
status: accepted
---
## Context

A complete qq ecosystem update assessment is decision-grade research. The
`research` Skill therefore requires durable Task, Change, plan/report, review,
and pull-request evidence, while the first `/update` prompt draft prohibited
all file and runtime-state writes. Requiring a separate explanation or new
workflow decision on every cycle would defeat the reusable command; treating
an assessment request as permission to change the assessed ecosystem would
cross the operator's mutation boundary.

## Decision

Invoking qq's project-local `/update` command is standing operator
authorization for that assessment cycle's governance-required evidence
lifecycle only: its Task, Change, plan and research documents, Checks,
independent review, and pull-request handoff. The command never authorizes an
agent to merge.

Apart from the listed evidence artifacts and their Git/GitHub lifecycle, this
standing authorization does not cover installing, updating, removing, enabling,
disabling, replacing, or configuring assessed software; changing state of the
assessed ecosystem, including its pins, channels, credentials, runtime state,
or data; or implementing an assessment recommendation. Each such mutation
requires a separate operator-approved Change.

## Consequences

- A future `/update` run may follow the normal research and GitHub Flow
  procedures without asking the operator to restate the recurring evidence
  shape.
- Its owning Task cites this decision for the durable evidence lifecycle; the
  invocation supplies the cycle-specific intent and context.
- Every recommendation remains non-executing. The operator still owns follow-up
  intent, acceptance, merge, and any privacy, compatibility, or replacement
  decision.
- If an assessment cannot preserve this boundary, it stops and reports the
  gap rather than broadening authorization.
