#!/usr/bin/env bash
set -euo pipefail

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck disable=SC2034
TEST_NAME="test-qq-observe"
# shellcheck source=tests/helpers.sh
# shellcheck disable=SC1091
source "$TESTS_DIR/helpers.sh"
ROOT="$(cd "$TESTS_DIR/.." && pwd -P)"
OBSERVE="$ROOT/bin/qq-observe"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

[ -x "$OBSERVE" ] || fail "qq-observe is not executable"
export HOME="$tmp/home"
export XDG_STATE_HOME="$tmp/state"
mkdir -p "$HOME"
store="$XDG_STATE_HOME/qq/spans/$(basename "$ROOT")/spans.jsonl"

span_id="$($OBSERVE id span)"
trace_id="$($OBSERVE id trace)"
[[ "$span_id" =~ ^[0-9a-f]{16}$ ]] || fail "span ID has the wrong shape"
[[ "$trace_id" =~ ^[0-9a-f]{32}$ ]] || fail "trace ID has the wrong shape"

(
  cd "$ROOT"
  "$OBSERVE" record \
    --name execute_tool --phase implementation --actor engine \
    --start 2026-07-21T10:00:00Z --end 2026-07-21T10:00:01.250Z \
    --trace-id 11111111111111111111111111111111 \
    --span-id 2222222222222222 --root-span-id 2222222222222222 \
    --attribute tool=qq-test >/dev/null
)
[ -f "$store" ] || fail "span store was not created"
assert_equal 600 "$(stat -c '%a' "$store")" "span store mode is not private"
jq -e '
  .schema_version == 1
  and .name == "execute_tool"
  and .phase == "implementation"
  and .actor == "engine"
  and .trace_id == "11111111111111111111111111111111"
  and .span_id == "2222222222222222"
  and .root_span_id == "2222222222222222"
  and .parent_span_id == null
  and .duration_ms == 1250
  and .attributes.tool == "qq-test"
' "$store" >/dev/null

session="$tmp/session.jsonl"
cat >"$session" <<'JSONL'
{"type":"session","timestamp":"2026-07-21T11:00:00.000Z"}
{"type":"message","timestamp":"2026-07-21T11:00:03.500Z","message":{"role":"user"}}
JSONL
(
  cd "$ROOT"
  "$OBSERVE" read-session "$session" \
    --phase orientation --actor accountable-session \
    --trace-id aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
    --span-id bbbbbbbbbbbbbbbb >/dev/null
)
assert_equal 2 "$(wc -l <"$store")" "span records were not appended"
tail -n 1 "$store" | jq -e \
  --arg session "$(realpath "$session")" '
  .name == "invoke_workflow"
  and .source == "pi-session-jsonl"
  and .duration_ms == 3500
  and .attributes["session.file"] == $session
  and .attributes["session.entries"] == 2
' >/dev/null

set +e
(
  cd "$ROOT"
  XDG_STATE_HOME="$ROOT/.observation-test-state" \
    "$OBSERVE" record --name invoke_agent --actor test \
      --start 2026-07-21T00:00:00Z --end 2026-07-21T00:00:01Z
) >"$tmp/refusal.stdout" 2>"$tmp/refusal.stderr"
refusal_status=$?
set -e
assert_equal 65 "$refusal_status" "worktree-local store was not refused"
assert_file_contains "$tmp/refusal.stderr" "refusing span store inside Git worktree"
[ ! -e "$ROOT/.observation-test-state" ] || fail "refusal wrote runtime state into the worktree"

set +e
(
  cd "$ROOT"
  "$OBSERVE" record --name invoke_agent --actor test \
    --start 2026-07-21T00:00:00Z --end 2026-07-21T00:00:01Z \
    --trace-id NOT-A-TRACE-ID
) >"$tmp/malformed.stdout" 2>"$tmp/malformed.stderr"
malformed_status=$?
set -e
assert_equal 64 "$malformed_status" "malformed trace context was accepted"
assert_equal 2 "$(wc -l <"$store")" "a refused record was appended"

printf 'test-qq-observe: pass\n'
