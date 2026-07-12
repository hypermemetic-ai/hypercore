---
name: agent-messaging
description: Coordinates directly with other live agents through herdr. Use when the work needs another agent's state, output, or attention — finding live agents, sending them prompts, reading their panes, or waiting for them to finish.
---

# Message agents through herdr

herdr names every agent session and exposes it to the others. `herdr agent
list` shows who is live, `herdr agent get <name>` inspects one, `herdr agent
read <name>` reads its pane, and `herdr agent wait <name>` blocks until it
finishes.

Message text is literal: escape sequences such as `\n` render as characters,
not formatting, so send prompts as clean single-line text. `herdr agent send`
types into the target without submitting; follow it with `herdr pane run
<pane-id>` to submit the line as a turn.

No further protocol exists. Coordinate when it helps; skip the ceremony when
it does not.
