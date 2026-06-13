# words

## share your findings about the claude usage…

operator (2026-06-13): share your findings about the claude usage endpoint so I can share. in another md document in home documents

machine (2026-06-13): Written — ~/Documents/claude-usage-endpoint.md. Shareable writeup of GET https://api.anthropic.com/api/oauth/usage (the endpoint Claude Code itself reads): auth is the Bearer OAuth token from ~/.claude/.credentials.json, the key header is anthropic-beta: oauth-2025-04-20, and it returns rolling plan-cap utilization as percentages (five_hour / seven_day / seven_day_opus|sonnet, each with resets_at, plus extra_usage), not token volume. Doc has the full response shape with a real example, curl + stdlib-Python fetch snippets, and caveats (short-lived token, OAuth/subscription surface, undocumented so liable to change). No secret in the doc. Deliverable, not standing work; nothing left on the queue.

## I want better thread labels. short, clear. also…

operator (2026-06-13): I want better thread labels. short, clear. also the notification sound isn't loud enough.

