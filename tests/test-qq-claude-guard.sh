#!/usr/bin/env bash
set -euo pipefail

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# helpers.sh reads TEST_NAME while it is sourced.
# shellcheck disable=SC2034
TEST_NAME="test-qq-claude-guard"
# shellcheck source=tests/helpers.sh
source "$TESTS_DIR/helpers.sh"
ROOT="$(cd "$TESTS_DIR/.." && pwd -P)"
GUARD="$ROOT/bin/qq-claude-guard"
SETTINGS="$ROOT/.claude/settings.json"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

[ -x "$GUARD" ] || fail 'Claude Code guard is not executable'

bash_payload() {
  jq -cn --arg command "$1" \
    '{tool_name:"Bash",tool_input:{command:$command}}'
}

file_payload() {
  jq -cn --arg tool "$1" --arg path "$2" \
    '{tool_name:$tool,tool_input:{file_path:$path}}'
}

assert_blocked() {
  local payload="$1"
  local reason="$2"
  local message="$3"
  local status

  : >"$TMP/out"
  : >"$TMP/err"
  if printf '%s\n' "$payload" | "$GUARD" >"$TMP/out" 2>"$TMP/err"; then
    status=0
  else
    status=$?
  fi
  assert_equal 2 "$status" "$message: expected exit 2, got $status"
  assert_equal "" "$(<"$TMP/out")" "$message: guard wrote to stdout"
  assert_equal 1 "$(wc -l <"$TMP/err")" "$message: reason was not one line"
  assert_contains "$(<"$TMP/err")" "$reason" "$message: wrong refusal reason"
}

assert_allowed() {
  local payload="$1"
  local message="$2"
  local status

  : >"$TMP/out"
  : >"$TMP/err"
  if printf '%s\n' "$payload" | "$GUARD" >"$TMP/out" 2>"$TMP/err"; then
    status=0
  else
    status=$?
  fi
  assert_equal 0 "$status" "$message: expected exit 0, got $status"
  assert_equal "" "$(<"$TMP/out")" "$message: guard wrote to stdout"
  assert_equal "" "$(<"$TMP/err")" "$message: guard wrote to stderr"
}

assert_blocked "$(bash_payload 'gh pr merge 42 --squash')" \
  'only the operator may merge pull requests' \
  'plain gh pr merge'
assert_blocked "$(bash_payload 'git status && gh -R owner/repo pr merge --merge')" \
  'only the operator may merge pull requests' \
  'compound gh pr merge with global flag'
assert_blocked "$(bash_payload 'GH_HOST=github.example command gh pr --repo owner/repo merge 42')" \
  'only the operator may merge pull requests' \
  'wrapped gh pr merge with flags between subcommands'
assert_blocked "$(bash_payload 'bash -lc "gh pr merge 42"')" \
  'only the operator may merge pull requests' \
  'nested shell gh pr merge'
assert_blocked "$(bash_payload 'setsid -f -w gh pr merge 1')" \
  'only the operator may merge pull requests' \
  'setsid-wrapped gh pr merge'
assert_blocked "$(bash_payload 'exec gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'exec-wrapped gh pr merge'
assert_blocked "$(bash_payload 'time -p gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'time-wrapped gh pr merge'
assert_blocked "$(bash_payload '/usr/bin/time -o timing.txt gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'time output option before gh pr merge'
assert_blocked "$(bash_payload '/usr/bin/time -f elapsed gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'time format option before gh pr merge'
assert_blocked "$(bash_payload 'timeout --preserve-status 30 gh pr merge 1')" \
  'only the operator may merge pull requests' \
  'timeout-wrapped gh pr merge'
assert_blocked "$(bash_payload 'nohup gh pr merge 1')" \
  'only the operator may merge pull requests' \
  'nohup-wrapped gh pr merge'
assert_blocked "$(bash_payload 'nice -n 5 stdbuf -o L gh pr merge 1')" \
  'only the operator may merge pull requests' \
  'nice and stdbuf-wrapped gh pr merge'
assert_blocked "$(bash_payload 'printf "%s\\n" 1 | xargs -n 1 gh pr merge')" \
  'only the operator may merge pull requests' \
  'xargs-wrapped gh pr merge'

assert_allowed "$(bash_payload 'gh pr view 42 && git status')" \
  'ordinary gh and git commands'
assert_allowed "$(bash_payload 'git merge main')" \
  'ordinary git merge'
assert_allowed "$(bash_payload 'printf "%s\\n" "gh pr merge"')" \
  'quoted gh pr merge text'
assert_allowed "$(bash_payload 'git status; # gh pr merge; ignored comment')" \
  'commented gh pr merge text'
assert_allowed "$(bash_payload 'time -o out.txt make build')" \
  'time output option before an ordinary command'
assert_blocked "$(bash_payload '/usr/bin/time 2>/dev/null -o /dev/null gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'time with interleaved redirection before gh pr merge'
assert_blocked "$(bash_payload 'exec 2>/dev/null -a qq gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'exec with interleaved redirection before gh pr merge'
assert_blocked "$(bash_payload '/usr/bin/time &>/dev/null -o timing.txt gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'time with ampersand redirection before gh pr merge'
assert_blocked "$(bash_payload 'time -o 2>/dev/null timing.txt gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'redirection between option and value before gh pr merge'
assert_blocked "$(bash_payload 'timeout 2 &>/dev/null gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'numeric wrapper operand before ampersand redirection'

quoted_heredoc="$({
  printf '%s\n' \
    "cat <<'MARKER' > notes.md" \
    'Documented command: gh pr merge 1' \
    'MARKER'
})"
assert_allowed "$(bash_payload "$quoted_heredoc")" \
  'single-quoted heredoc mention'

plain_heredoc="$({
  printf '%s\n' \
    'cat <<MARKER > notes.md' \
    'Documented command: gh pr merge 1' \
    'MARKER'
})"
assert_allowed "$(bash_payload "$plain_heredoc")" \
  'plain heredoc mention'

unquoted_heredoc_substitution="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    'cat <<MARKER' \
    '$(gh pr merge 42)' \
    'MARKER'
})"
assert_blocked "$(bash_payload "$unquoted_heredoc_substitution")" \
  'only the operator may merge pull requests' \
  'command substitution in an unquoted heredoc'

nested_heredoc_substitution="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    'cat <<MARKER' \
    '$(echo "$(gh pr merge 42)")' \
    'MARKER'
})"
assert_blocked "$(bash_payload "$nested_heredoc_substitution")" \
  'only the operator may merge pull requests' \
  'nested command substitution in an unquoted heredoc'

quoted_heredoc_substitution="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    "cat <<'MARKER'" \
    '$(gh pr merge 42)' \
    'MARKER'
})"
assert_allowed "$(bash_payload "$quoted_heredoc_substitution")" \
  'command substitution text in a quoted heredoc'

double_quoted_heredoc_substitution="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    'cat <<"MARKER"' \
    '$(gh pr merge 42)' \
    'MARKER'
})"
assert_allowed "$(bash_payload "$double_quoted_heredoc_substitution")" \
  'command substitution text under a double-quoted heredoc delimiter'

empty_quote_heredoc="$({
  printf '%s\n' \
    "cat <<''MARKER" \
    'gh pr merge 42' \
    'MARKER'
})"
assert_allowed "$(bash_payload "$empty_quote_heredoc")" \
  'plain merge text under an empty-quote heredoc delimiter'

leading_heredoc_redirection="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    "<<'MARKER' cat" \
    '$(gh pr merge 42)' \
    'MARKER'
})"
assert_allowed "$(bash_payload "$leading_heredoc_redirection")" \
  'substitution text under a leading quoted heredoc redirection'

unquoted_heredoc_backticks="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    'cat <<MARKER' \
    '`gh pr merge 42`' \
    'MARKER'
})"
assert_blocked "$(bash_payload "$unquoted_heredoc_backticks")" \
  'only the operator may merge pull requests' \
  'backtick substitution in an unquoted heredoc'

nested_heredoc_backticks="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    'cat <<MARKER' \
    '`echo \`gh pr merge 42\``' \
    'MARKER'
})"
assert_blocked "$(bash_payload "$nested_heredoc_backticks")" \
  'only the operator may merge pull requests' \
  'nested backtick substitution in an unquoted heredoc'

tabbed_heredoc="$(printf 'cat <<-MARKER > notes.md\n\tgh pr merge 1\n\tMARKER\n')"
assert_allowed "$(bash_payload "$tabbed_heredoc")" \
  'tab-stripped heredoc mention'

hyphen_heredoc="$({
  printf '%s\n' \
    "cat <<'END-MARKER'" \
    'gh pr merge 42' \
    'END-MARKER'
})"
assert_allowed "$(bash_payload "$hyphen_heredoc")" \
  'hyphenated quoted heredoc mention'

punctuated_heredoc="$({
  printf '%s\n' \
    "cat <<'END:MARKER'" \
    'gh pr merge 42' \
    'END:MARKER'
})"
assert_allowed "$(bash_payload "$punctuated_heredoc")" \
  'colon-punctuated quoted heredoc mention'

at_heredoc="$({
  printf '%s\n' \
    "cat <<'@END'" \
    'gh pr merge 42' \
    '@END'
})"
assert_allowed "$(bash_payload "$at_heredoc")" \
  'at-sign quoted heredoc mention'

spaced_heredoc="$({
  printf '%s\n' \
    "cat <<'END MARKER'" \
    'gh pr merge 42' \
    'END MARKER'
})"
assert_allowed "$(bash_payload "$spaced_heredoc")" \
  'whitespace quoted heredoc delimiter mention'

arithmetic_then_merge="$({
  printf '%s\n' \
    'if (( 1 << SHIFT )); then :; fi' \
    'gh pr merge 42'
})"
assert_blocked "$(bash_payload "$arithmetic_then_merge")" \
  'only the operator may merge pull requests' \
  'gh pr merge after arithmetic shift in if'

arithmetic_then_benign="$({
  printf '%s\n' \
    'if (( 1 << SHIFT )); then :; fi' \
    'git status'
})"
assert_allowed "$(bash_payload "$arithmetic_then_benign")" \
  'arithmetic shift in if before ordinary command'

for_arithmetic_then_merge="$({
  printf '%s\n' \
    'for (( i=0; i << SHIFT; i++ )); do :; done' \
    'gh pr merge 42'
})"
assert_blocked "$(bash_payload "$for_arithmetic_then_merge")" \
  'only the operator may merge pull requests' \
  'gh pr merge after arithmetic shift in C-style for'

assert_blocked "$(bash_payload 'exec &>/dev/null gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'exec with ampersand redirection before gh pr merge'
assert_blocked "$(bash_payload 'gh 2>/dev/null pr merge 42')" \
  'only the operator may merge pull requests' \
  'gh with interleaved numeric redirection before pr merge'
assert_blocked "$(bash_payload 'gh &>/dev/null pr merge 42')" \
  'only the operator may merge pull requests' \
  'gh with interleaved ampersand redirection before pr merge'
assert_blocked "$(bash_payload 'gh --repo 2>/dev/null hypermemetic-ai/qq pr merge 42')" \
  'only the operator may merge pull requests' \
  'gh with redirection between a global option and its value'
assert_blocked "$(bash_payload '/usr/bin/time -o 2>/dev/null out.txt gh pr merge 42')" \
  'only the operator may merge pull requests' \
  'time with redirection between an option and its value'
assert_allowed "$(bash_payload 'gh pr view 42 &>/dev/null')" \
  'ampersand redirection after an ordinary gh command'
assert_allowed "$(bash_payload 'gh --repo 2>/dev/null hypermemetic-ai/qq pr view 42')" \
  'redirection inside a global option before an ordinary gh command'

unterminated_heredoc="$({
  # shellcheck disable=SC2016
  printf '%s\n' \
    'cat <<MARKER' \
    '$(gh pr merge 42)'
})"
assert_blocked "$(bash_payload "$unterminated_heredoc")" \
  'only the operator may merge pull requests' \
  'substitution in an unterminated expanding heredoc'

heredoc_then_merge="$({
  printf '%s\n' \
    'cat <<MARKER > notes.md' \
    'documentation only' \
    'MARKER' \
    'gh pr merge 1'
})"
assert_blocked "$(bash_payload "$heredoc_then_merge")" \
  'only the operator may merge pull requests' \
  'gh pr merge after heredoc terminator'

semicolon_heredoc_then_merge="$({
  printf '%s\n' \
    'cat <<MARKER;' \
    'documentation only' \
    'MARKER' \
    'gh pr merge 1'
})"
assert_blocked "$(bash_payload "$semicolon_heredoc_then_merge")" \
  'only the operator may merge pull requests' \
  'gh pr merge after semicolon-terminated heredoc'

assert_blocked "$(file_payload Edit "$ROOT/backlog/tasks/example.md")" \
  'managed Backlog markdown must be edited through the backlog CLI' \
  'backlog markdown Edit'
assert_blocked "$(
  jq -cn --arg cwd "$ROOT" \
    '{cwd:$cwd,tool_name:"MultiEdit",tool_input:{file_path:"backlog/docs/example.md",edits:[]}}'
)" \
  'managed Backlog markdown must be edited through the backlog CLI' \
  'relative backlog markdown MultiEdit'
assert_blocked "$(
  jq -cn --arg path "$ROOT/backlog/tasks/notebook.md" \
    '{tool_name:"NotebookEdit",tool_input:{notebook_path:$path}}'
)" \
  'managed Backlog markdown must be edited through the backlog CLI' \
  'backlog markdown NotebookEdit'

assert_blocked "$(file_payload Write "$ROOT/backlog/tasks/assets/x.md")" \
  'managed Backlog markdown must be edited through the backlog CLI' \
  'non-document Backlog assets Write'
assert_allowed "$(file_payload Write "$ROOT/backlog/docs/plans/assets/doc-38/note.md")" \
  'Backlog plan asset Write'
assert_blocked "$(file_payload Write "$ROOT/backlog/docs/research/assets/note.md")" \
  'managed Backlog markdown must be edited through the backlog CLI' \
  'non-plan docs assets Write'
assert_allowed "$(file_payload Write "$ROOT/README.md")" \
  'non-Backlog Write'
assert_allowed "$(file_payload Write "$ROOT/backlog/tasks/example.txt")" \
  'non-markdown Backlog Write'
assert_allowed 'not valid JSON' 'malformed JSON'

jq -e '
  .hooks.PreToolUse == [
    {
      matcher: "Bash|Edit|Write|MultiEdit|NotebookEdit",
      hooks: [
        {
          type: "command",
          command: "${CLAUDE_PROJECT_DIR}/bin/qq-claude-guard",
          args: []
        }
      ]
    }
  ]
' "$SETTINGS" >/dev/null || fail 'Claude Code PreToolUse hook is not wired to the guard'

printf 'test-qq-claude-guard: pass\n'
