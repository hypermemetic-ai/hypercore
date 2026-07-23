#!/usr/bin/env bash
# shellcheck disable=SC1091,SC2034
set -euo pipefail

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TEST_NAME="test-qq-observe-facts"
# shellcheck source=tests/helpers.sh
source "$TESTS_DIR/helpers.sh"
ROOT="$(cd "$TESTS_DIR/.." && pwd -P)"
OBSERVE="$ROOT/bin/qq-observe"
FIXTURES="$TESTS_DIR/fixtures/observer"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export XDG_STATE_HOME="$tmp/state"

assert_exact_output() {
  local command="$1" fixture="$2" expected="$3" actual="$4"
  (
    cd "$ROOT"
    "$OBSERVE" "$command" "$fixture"
  ) >"$actual"
  if ! cmp -s "$expected" "$actual"; then
    diff -u "$expected" "$actual" >&2 || true
    fail "$command output for $(basename "$fixture") did not exactly match hand-counted expectations"
  fi
}

for format in pi codex; do
  case "$format" in
    pi) fixture="$FIXTURES/pi-session.jsonl" ;;
    codex) fixture="$FIXTURES/codex-rollout.jsonl" ;;
  esac
  assert_exact_output facts "$fixture" "$FIXTURES/$format-expected-facts.json" \
    "$tmp/$format-facts.json"
  assert_exact_output signals "$fixture" "$FIXTURES/$format-expected-signals.json" \
    "$tmp/$format-signals.json"
done

jq -e '
  .unknown_entries.total == 1
  and .unknown_entries.by_shape == {"pi:future_pi_entry":1}
  and .unknown_entries.entries == [{entry:13, shape:"pi:future_pi_entry"}]
' "$tmp/pi-facts.json" >/dev/null \
  || fail 'Pi unknown entry was not counted and cited'
jq -e '
  .unknown_entries.total == 1
  and .unknown_entries.by_shape == {"codex:event_msg:future_event":1}
  and .unknown_entries.entries == [{entry:20, shape:"codex:event_msg:future_event"}]
' "$tmp/codex-facts.json" >/dev/null \
  || fail 'Codex unknown entry was not counted and cited'

no_usage="$tmp/no-usage.jsonl"
cat >"$no_usage" <<'JSONL'
{"type":"session","version":3,"timestamp":"2026-07-03T00:00:00Z"}
{"type":"message","timestamp":"2026-07-03T00:00:01Z","message":{"role":"assistant","content":[{"type":"text","text":"No usage was reported."}]}}
JSONL
(
  cd "$ROOT"
  "$OBSERVE" facts "$no_usage"
) >"$tmp/no-usage-facts.json"
jq -e '
  .token_usage == {input:null, output:null, cache_read:null, cache_write:null}
  and .tokens_unavailable == {input:1, output:1, cache_read:1, cache_write:1}
' "$tmp/no-usage-facts.json" >/dev/null \
  || fail 'absent token fields were zeroed or not counted'

malformed_pi="$tmp/malformed-pi.jsonl"
cat >"$malformed_pi" <<'JSONL'
{"type":"session","version":3,"timestamp":"2026-07-03T00:00:00Z"}
{"type":"message"
JSONL
for command in facts signals; do
  set +e
  (
    cd "$ROOT"
    "$OBSERVE" "$command" "$malformed_pi"
  ) >"$tmp/$command-malformed.stdout" 2>"$tmp/$command-malformed.stderr"
  status=$?
  set -e
  assert_equal 64 "$status" "$command accepted malformed JSONL"
  assert_file_contains "$tmp/$command-malformed.stderr" 'malformed JSON at line 2' \
    "$command failure did not cite the malformed physical line"
done

printf 'test-qq-observe-facts: pass\n'
