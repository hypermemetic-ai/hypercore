---
id: doc-67
title: Pi drops custom-message details; identity belongs in content
type: guide
created_date: '2026-07-19 23:28'
updated_date: '2026-07-19 23:28'
tags:
  - solution
  - pi
  - extensions
  - messaging
---
# Pi drops custom-message details; identity belongs in content

## Symptom

An extension wakes its session with `pi.sendMessage({customType, content,
details}, {triggerTurn:true, deliverAs:"followUp"})`, packing the
structured payload (which PR, which state, counts) into `details` and
keeping `content` as a short human line. When two such wakes arrive, the
resumed agent cannot attribute them: every wake reads identically. The
structured payload was authored but invisible where it mattered.

## Root cause

Pi forwards only `content` to the model for custom messages. In pi
0.80.10, `dist/core/messages.js` (`convertToLlm`, custom case) maps a
custom message to a user message carrying only `content`; `details`
survives in the session file for renderers and state reconstruction but
never enters LLM context. The same split applies to tool results:
`content` reaches the model, `details` is for rendering and state.

## Resolution

Author every model-visible string — wake messages and tool-result content
alike — to carry its own attribution: name the subject (for example the
pull-request selector and URL) inside `content`, and keep `details` for
the structured payload that renderers, tests, and state reconstruction
consume. Build the strings in one place so no emission path can drift
identity-free, and assert content identity in the extension's tests. This
matters most for asynchronous wakes, which arrive detached from any tool
call the model can correlate them with.

## Verification

Verified against installed pi 0.80.10 source during T-99 (PR #157):
`convertToLlm` custom case forwards `content` only. A fresh-context
reviewer demonstrated two concurrent wakes with identical identity-free
content; after the fix, the extension suite asserts selector and URL in
terminal wakes and selector identity in every tool-result content string,
and the owner re-ran the original failing probe to a single,
identity-carrying wake.
