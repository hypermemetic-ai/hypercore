#!/usr/bin/env bash
set -euo pipefail

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TEST_NAME="test-qq-pr-watch"
# shellcheck source=tests/helpers.sh
source "$TESTS_DIR/helpers.sh"
ROOT="$(cd "$TESTS_DIR/.." && pwd -P)"
WATCH="$ROOT/bin/qq-pr-watch"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

fake_gh="$tmp/gh"
cat >"$fake_gh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >>"$FAKE_GH_LOG"
if [ "${FAKE_GH_BAD:-}" = 1 ]; then
  printf 'not-json\n'
else
  jq -cn --arg state "${FAKE_PR_STATE:-OPEN}" \
    '{state:$state,url:"https://example.test/pr/17"}'
fi
SH
chmod +x "$fake_gh"
export QQ_GH_BIN="$fake_gh"
export FAKE_GH_LOG="$tmp/gh.log"

run_watch() {
  local expected_exit="$1"
  shift
  set +e
  "$WATCH" "$@" >"$tmp/result.json"
  actual_exit=$?
  set -e
  assert_equal "$expected_exit" "$actual_exit" "unexpected qq-pr-watch exit"
  jq -e . "$tmp/result.json" >/dev/null
}

# Exit 0: an already-terminal pull request emits exactly one result/wake.
export FAKE_PR_STATE=MERGED
run_watch 0 17
jq -e '
  .status == "done"
  and .state.pr_state == "MERGED"
  and .state.notification_count == 1
' "$tmp/result.json" >/dev/null
assert_equal 1 "$(wc -l <"$FAKE_GH_LOG")" 'terminal watch polled more than once'

# A terminal dry-run mirrors the result without claiming the real wake.
run_watch 0 17 --dry-run
jq -e '
  .status == "done"
  and .state.pr_state == "MERGED"
  and .state.notification_count == 0
' "$tmp/result.json" >/dev/null

# Exit 2: inspect mirrors the watch precondition and reports current OPEN state
# without sleeping or claiming a notification.
: >"$FAKE_GH_LOG"
export FAKE_PR_STATE=OPEN
run_watch 2 inspect 17
jq -e '
  .status == "refused"
  and .state.pr_state == "OPEN"
  and (.message | contains("no completion notification"))
' "$tmp/result.json" >/dev/null
assert_equal 1 "$(wc -l <"$FAKE_GH_LOG")" 'inspect polled more than once'

# Exit 1: an unreadable provider response is an engine error.
export FAKE_GH_BAD=1
run_watch 1 17 --dry-run
jq -e '.status == "error"' "$tmp/result.json" >/dev/null

printf 'test-qq-pr-watch: pass\n'
