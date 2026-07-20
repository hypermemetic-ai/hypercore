---
id: doc-66
title: >-
  Pi coerces extension tool arguments; prepareArguments is the
  refuse-don't-sanitise rail
type: guide
created_date: '2026-07-19 23:28'
updated_date: '2026-07-19 23:28'
tags:
  - solution
  - pi
  - extensions
  - tools
  - validation
---
# Pi coerces extension tool arguments; prepareArguments is the refuse-don't-sanitise rail

## Symptom

A pi extension tool declares an integer parameter bounded 30-60. A model that
sends the string "30" (or another coercible shape) must be refused, not
silently armed with a sanitized value — the bound is a policy, and refuse,
don't sanitise forbids rewriting it. Relying on the JSON-schema `parameters`
declaration alone lets the coerced call through: the schema validates what it
is given only after pi has already rewritten it.

## Root cause

Pi's tool-call pipeline mutates arguments before schema validation. In pi
0.80.10, `pi-agent-core/dist/agent-loop.js` runs
`prepareToolCallArguments` (the extension's `prepareArguments` hook) and
then `validateToolArguments`, which in `pi-ai/dist/utils/validation.js`
first calls `Value.Convert(parameters, args)` — TypeBox's coercing pass —
and, for schemas lacking the TypeBox symbol (hand-written JSON-schema
literals, the house idiom that keeps extensions importable under plain node),
additionally runs `coerceWithJsonSchema`. Only then does the validator
check the result. So a coercible argument passes validation in its rewritten
form and `execute` never sees the raw input. Any throw from
`prepareArguments` is caught by the agent loop and becomes the tool-result
content directly, bypassing `execute` entirely.

## Resolution

Treat `prepareArguments` as the policy rail, not a compatibility shim:
inspect the raw arguments and throw on any value that would need coercion,
before validation can rewrite it. Re-check bounds inside `execute` as well,
because direct or test harnesses reach `execute` without the preparation
path. Since the thrown message becomes the model-visible content verbatim,
compose it with the same identity-carrying builder the rest of the tool's
content uses (see doc-67). A test that calls `prepareArguments` directly
pins both the refusal and the message shape.

## Verification

Verified against installed pi 0.80.10 source during T-99 (PR #157):
`agent-loop.js` catch -> `createErrorToolResult(error.message)`;
`validation.js` `Value.Convert` call plus the plain-schema
`coerceWithJsonSchema` branch. Fresh review independently flagged the
selector-free throw; the fixed extension's suite asserts the refusal for
string, fractional, and out-of-range intervals and that no watch arms.
