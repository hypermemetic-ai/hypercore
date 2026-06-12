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

# linked projects (registry.md): their intent ratifies from hyper, but the
# words and the commits live in their own repos — the brief carries the
# pending counts so a summoned session knows the whole queue, not just ours.
linked_block=""
if [ -f registry.md ]; then
  linked_summary=$(awk '/^## /{name=substr($0,4)} /^- path: /{print name "\t" substr($0,9)}' registry.md 2>/dev/null \
    | while IFS="$(printf '\t')" read -r lname lpath; do
        case "$lpath" in "~/"*) lpath="$HOME/${lpath#\~/}";; esac
        [ -f "$lpath/intent.md" ] || continue
        lc=$(grep -c ' \[machine\]$' "$lpath/intent.md" 2>/dev/null) || lc=0
        printf '  %s: %s pending — %s/intent.md\n' "$lname" "$lc" "$lpath"
        # the project's standing work and open graphs ride along — a
        # session summoned into the repo, or answering words about it,
        # sees the whole unit (sessions go into linked repos too — the
        # operator's word, 2026-06-11)
        [ -f "$lpath/work.md" ] && awk '
          /^## /       { name = substr($0, 4) }
          /^- state: / { printf "    standing: %s — %s\n", name, substr($0, 10) }
        ' "$lpath/work.md" 2>/dev/null
        for g in "$lpath"/work/*/graph.md; do
          [ -f "$g" ] || continue
          awk -v name="$(basename "$(dirname "$g")")" '
            /^## /       { n++ }
            /^- state: / { if (root == "") root = substr($0, 10) }
            END { if (root !~ /folded/)
                    printf "    open graph: %s — %d node%s · root: %s\n", \
                           name, n, (n == 1 ? "" : "s"), root }
          ' "$g"
        done
      done) || linked_summary=""
  [ -n "$linked_summary" ] && linked_block="
Linked projects (registry.md — their intent ratifies from hyper; approve
and cut commit in the linked repo itself):
${linked_summary}
"
fi

# a dead session can strand changes between writing and committing; the
# brief flags it so every session, typed or summoned, trues it up first.
behind=$(git status --porcelain 2>/dev/null) || behind=""
behind_block=""
if [ -n "$behind" ]; then
  behind_block="
THE RECORD IS BEHIND — uncommitted changes:
${behind}
True this up before anything else: read the diff, verify what it claims
against what is on disk, finish or correct what the dead session left,
and commit with grounds.
"
fi

# only operator words the machine has not yet answered: lines after the
# last "machine (" line of their card or exchange. an answered word stops
# nagging. read from both ledgers that carry operator words.
ledgers=""
[ -f queue.md ] && ledgers="queue.md"
[ -f words.md ] && ledgers="$ledgers words.md"
words=""
if [ -n "$ledgers" ]; then
  words=$(awk '
    function flush() { if (pending != "") out = out pending; pending = "" }
    /^## /        { flush(); src = $0 }
    /^operator \(/ { pending = pending "  [" FILENAME " . " substr(src, 4) "]\n  " $0 "\n" }
    /^machine \(/  { pending = "" }
    END { flush(); printf "%s", out }
  ' $ledgers 2>/dev/null) || words=""
fi
words_block=""
if [ -n "$words" ]; then
  words_block="
Operator words awaiting the machine's answer:
${words}
Answer these first. queue.md words are explain picks — tell the story or
answer the words, then stop; the answer lands as a 'machine (date):' line
on the same card. words.md words are speech from anywhere — read them,
decide what they are (new intent, a new ask, an answer, a redirect),
answer in a 'machine (date):' line on the same block, and let what you
made of them return through the queue.
"
fi

# open execution graphs: work/<name>/graph.md, the first block the root
# ask born with its check. folded graphs live under archive/ — the fold
# moves the folder — so work/ holds only current work; the folded-root
# filter below stays as a net for a fold caught mid-move.
graphs_block=""
if [ -d work ]; then
  graphs_summary=$(for g in work/*/graph.md; do
    [ -f "$g" ] || continue
    awk -v name="$(basename "$(dirname "$g")")" '
      /^## /       { n++ }
      /^- state: / { s = substr($0, 10)
                     if (n == 1 && root == "") root = s
                     if (s ~ /open/) open++ }
      END { if (root !~ /folded/)
              printf "  %s — %d node%s, %d open · root: %s\n", \
                     name, n, (n == 1 ? "" : "s"), open, root }
    ' "$g"
  done) || graphs_summary=""
  [ -n "$graphs_summary" ] && graphs_block="
Open execution graphs (work/<name>/graph.md — the unit on disk is the
graph; read each graph.md you touch in full before growing or folding it):
${graphs_summary}"
fi

work_block=""
if [ -f work.md ]; then
  work_summary=$(awk '
    /^## /        { name = substr($0, 4) }
    /^- state: /  { printf "  %s — %s\n", name, substr($0, 10) }
  ' work.md 2>/dev/null) || work_summary=""
  [ -n "$work_summary" ] && work_block="
Standing work (work.md — keep it true; the operator reads it in hyper):
${work_summary}"
fi

context="hypercore session brief — generated from disk by .claude/hooks/session-brief.sh

Re-ratification queue: ${total} statements still marked [machine] in ${doc}.
${per_sec}
Next pending: ${next:-none — the queue is clear}
${linked_block}${behind_block}${words_block}${work_block}${graphs_block}

Recent commits:
${recent}

Protocol: CLAUDE.md and .claude/skills/hypercore/SKILL.md are the standing
orders. Every decision lands on disk and is committed before anything else
happens, so this conversation can be cleared at any moment without loss.
If the operator says nothing else, resume ratification from the next
pending statement."

# --plain prints the brief bare — hyper writes it to brief.md at every
# summon, so any harness reads the same bearings a claude hook injects.
if [ "${1:-}" = "--plain" ]; then
  printf '%s\n' "$context"
else
  jq -n --arg ctx "$context" --arg msg "hypercore: ${total} statements awaiting ratification" \
    '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}, systemMessage: $msg}'
fi
