#!/usr/bin/env bash
# session-brief: injected at every session start (including after /clear).
# This is what makes clearing context a single keystroke — the conversation
# is disposable because this brief rebuilds the machine's bearings from disk.
set -euo pipefail
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

doc=intent.md

total=$(grep -c ' \[machine\]$' "$doc" 2>/dev/null) || total=0
per_sec=$(awk '
  /^## / { sec = substr($0, 4); if (!(sec in c)) { order[++n] = sec; c[sec] = 0 } }
  / \[machine\]$/ { c[sec]++ }
  END { for (i = 1; i <= n; i++) printf "  %s: %d pending\n", order[i], c[order[i]] }
' "$doc" 2>/dev/null) || per_sec=""

next=$(grep -m1 ' \[machine\]$' "$doc" 2>/dev/null) || next=""
recent=$(git log --oneline -3 2>/dev/null) || recent="(no git history)"

context="hypercore session brief — generated from disk by .claude/hooks/session-brief.sh

Re-ratification queue: ${total} statements still marked [machine] in ${doc}.
${per_sec}
Next pending: ${next:-none — the queue is clear}

Recent commits:
${recent}

Protocol: CLAUDE.md and .claude/skills/hypercore/SKILL.md are the standing
orders. Every decision lands on disk and is committed before anything else
happens, so this conversation can be cleared at any moment without loss.
If the operator says nothing else, resume ratification from the next
pending statement."

jq -n --arg ctx "$context" --arg msg "hypercore: ${total} statements awaiting ratification" \
  '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}, systemMessage: $msg}'
