---
name: agent-messaging
description: Coordinates live agents through pi-intercom or the temporary Codex/herdr fallback and raises operator-visible notifications. Use for another live agent's state, output, or attention, or an event the operator must notice outside any transcript.
---

# Message agents through pi-intercom

pi-intercom is qq's default transport; its bundled skill documents raw
mechanics. This qq overlay does not start, own, or retire agents.

## Coordinate Pi agents

Name sessions uniquely. Call `intercom({ action: "list" })`, use its current
session name as `<id>`, and begin every `send`, `ask`, and `reply` message with
`AGENT from=<id>: <message>`.

```text
intercom({ action: "send", to: "<peer>", message: "AGENT from=<id>: <update>" })
intercom({ action: "ask", to: "<peer>", message: "AGENT from=<id>: <question>" })
intercom({ action: "reply", message: "AGENT from=<id>: <answer>" })
```

Use `send` for an update and `ask` when work needs an answer. `ask` waits for a
correlated `reply` and returns it in the asking turn.

Pass intended text directly as `message`; JSON transport preserves line breaks
and backslashes. Do not apply herdr's single-line or escape rules.

Verify the envelope's `<id>` against the transport-reported `From` sender and
`list`. Reply from the triggered turn so `reply` uses that sender and message
ID. On mismatch, ambiguity, absence, or failed delivery, report the message or
reply as unrouteable; never guess.

Busy interactive sessions queue messages until idle. Keep `inboundTrigger` at
its default `always`; receipt must wake the delegate. Alt+M opens the operator
overlay.

## Reach Codex delegates until T-95 lands

Until T-95 lands, discover Codex delegates with `herdr agent list`, inspect with
`herdr agent get <name>` and `herdr agent read <name>`, and wait with `herdr
agent wait <name> --status idle`.

Read your `terminal_id` from `herdr pane current --current`. Verify an envelope
with `herdr agent get <terminal-id>`, resolve `.result.agent.pane_id`, and submit
one single-line reply:

```sh
herdr pane run <pane-id> "AGENT from=<terminal-id>: <message>"
```

Never split text and Enter or use `herdr agent send` for a turn. Report an
unresolved source as unrouteable.

## Notify the operator

For an event the operator must notice outside a transcript:

```sh
herdr notification show "<title>" --body "<body>" --sound <sound>
```

Keep the title short, put actionable detail in the body, and use sound only
when asking the operator to act.
