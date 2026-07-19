#!/usr/bin/env bash
set -euo pipefail

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
TEST_NAME="test-qq-status"
# shellcheck source=tests/helpers.sh
source "$TESTS_DIR/helpers.sh"
ROOT="$(cd "$TESTS_DIR/.." && pwd -P)"
STATUS="$ROOT/bin/qq-status"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

repo="$tmp/repo"
git init -q -b main "$repo"
git -C "$repo" -c user.name=test -c user.email=test@example.com \
  commit --allow-empty -qm initial
mkdir -p "$tmp/runtime"
export TMPDIR="$tmp/runtime"

fake_herdr="$tmp/herdr"
cat >"$fake_herdr" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "$*" >>"$FAKE_HERDR_LOG"
printf '%s\n' '{"result":{"shown":true}}'
SH
chmod +x "$fake_herdr"
export QQ_HERDR_BIN="$fake_herdr"
export FAKE_HERDR_LOG="$tmp/herdr.log"

status_args=(
  --repo "$repo"
  --dispatcher-workspace home-1
  --work-session change-1
  --pane change-1:p1
  --agent worker-1
  --ticket T-83
  --label engines
)

run_status() {
  local expected_exit="$1"
  shift
  set +e
  "$STATUS" "$@" >"$tmp/result.json"
  actual_exit=$?
  set -e
  assert_equal "$expected_exit" "$actual_exit" "unexpected qq-status exit"
  jq -e . "$tmp/result.json" >/dev/null
}

# Exit 0: one invocation performs an atomic detail rewrite and two Herdr calls
# with strictly increasing wall-clock-derived sequence values.
run_status 0 dispatched "${status_args[@]}" \
  --runtime codex --events "$tmp/events" --stderr "$tmp/stderr"
jq -e '
  .status == "done"
  and .state.detail_written == true
  and .state.herdr_available == true
  and (.state.sequences | length) == 2
  and .state.sequences[1] > .state.sequences[0]
' "$tmp/result.json" >/dev/null
status_file="$(jq -r '.state.status_file' "$tmp/result.json")"
assert_file_contains "$status_file" 'stage: dispatched since '
assert_file_contains "$status_file" 'events: '
assert_file_contains "$FAKE_HERDR_LOG" \
  'workspace report-metadata change-1 --source qq-dispatch --token stage=dispatched'
assert_file_contains "$FAKE_HERDR_LOG" \
  'pane report-agent change-1:p1 --source qq-dispatch --agent worker-1 --state working'

# A batch label namespaces the derived detail file, while malformed labels are
# command errors rather than rewritten path components.
run_status 0 inspect dispatched "${status_args[@]}" --batch-label t107-followon
batch_status_file="$(jq -r '.state.status_file' "$tmp/result.json")"
assert_equal "${status_file%.status}-t107-followon.status" "$batch_status_file" \
  'batch label did not namespace the derived status file'
run_status 1 inspect dispatched "${status_args[@]}" --batch-label bad_label
jq -e '
  .status == "error"
  and (.message | contains("--batch-label must match [A-Za-z0-9-]{1,30}"))
' "$tmp/result.json" >/dev/null

# Terminal is idempotent glass cleanup: remove the block, clear the token, and
# release presence with a fresh sequence for each call.
: >"$FAKE_HERDR_LOG"
run_status 0 terminal "${status_args[@]}"
if grep -Fq -- 'qq-delegate:worker-1' "$status_file"; then
  fail 'terminal status retained the delegate detail block'
fi
jq -e '
  (.state.sequences | length) == 2
  and .state.sequences[1] > .state.sequences[0]
' "$tmp/result.json" >/dev/null
assert_file_contains "$FAKE_HERDR_LOG" '--clear-token stage'
assert_file_contains "$FAKE_HERDR_LOG" 'pane release-agent change-1:p1'

# Herdr absence degrades to a noted no-op and exit 0 while retaining the local
# detail file; visibility never gates the caller's automation contract.
export QQ_HERDR_BIN="$tmp/missing-herdr"
run_status 0 queued "${status_args[@]}"
jq -e '
  .status == "done"
  and .state.herdr_available == false
  and .state.degraded == true
  and any(.state.notes[]; contains("herdr unavailable"))
' "$tmp/result.json" >/dev/null

# Exit 2: unexplained filesystem state is preserved rather than overwritten.
rail_args=(
  --repo "$repo"
  --dispatcher-workspace rail-home
  --work-session change-1
  --pane change-1:p1
  --agent worker-1
  --ticket T-83
  --label engines
)
run_status 0 inspect dispatched "${rail_args[@]}"
rail_file="$(jq -r '.state.status_file' "$tmp/result.json")"
mkdir -p "$(dirname "$rail_file")"
ln -s "$tmp/unexplained" "$rail_file"
run_status 2 inspect dispatched "${rail_args[@]}"
jq -e '
  .status == "refused"
  and (.message | contains("never justifies overwriting"))
' "$tmp/result.json" >/dev/null
run_status 2 dispatched "${rail_args[@]}"
jq -e '
  .status == "refused"
  and (.message | contains("never justifies overwriting"))
' "$tmp/result.json" >/dev/null

# Intermediate symlinks beneath the qq-delegates base are the same unexplained
# filesystem state, including during inspection.
intermediate_runtime="$tmp/intermediate-runtime"
intermediate_target="$tmp/intermediate-target"
mkdir -p "$intermediate_runtime/qq-delegates" "$intermediate_target"
export TMPDIR="$intermediate_runtime"
repo_first_component="${repo#/}"
repo_first_component="${repo_first_component%%/*}"
ln -s "$intermediate_target" \
  "$TMPDIR/qq-delegates/$repo_first_component"
run_status 2 inspect dispatched "${rail_args[@]}"
jq -e '
  .status == "refused"
  and (.message | contains("never justifies overwriting"))
' "$tmp/result.json" >/dev/null
run_status 2 dispatched "${rail_args[@]}"
jq -e '
  .status == "refused"
  and (.message | contains("never justifies overwriting"))
' "$tmp/result.json" >/dev/null
export TMPDIR="$tmp/runtime"

# If an intermediate directory is replaced after the pre-write rail, the
# outcome guard removes the redirected write and refuses the transition.
race_bin="$tmp/race-bin"
mkdir -p "$race_bin"
real_mv_bin="$(command -v mv)"
race_component="$TMPDIR/qq-delegates/$repo_first_component"
cat >"$race_bin/mv" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
source_path="$3"
destination="$4"
race_backup="$RACE_COMPONENT.before-redirect"
"$REAL_MV_BIN" -- "$RACE_COMPONENT" "$race_backup"
ln -s "$RACE_REDIRECT_TARGET" "$RACE_COMPONENT"
source_suffix="${source_path#"$RACE_COMPONENT"}"
exec "$REAL_MV_BIN" -f -- "$race_backup$source_suffix" "$destination"
SH
chmod +x "$race_bin/mv"
race_args=(
  --repo "$repo"
  --dispatcher-workspace race-home
  --work-session change-1
  --pane change-1:p1
  --agent worker-1
  --ticket T-83
  --label engines
)
repo_status_before="$(git -C "$repo" status --porcelain=v1 --untracked-files=all)"
original_path="$PATH"
export REAL_MV_BIN="$real_mv_bin"
export RACE_COMPONENT="$race_component"
export RACE_REDIRECT_TARGET="/$repo_first_component"
export PATH="$race_bin:$PATH"
run_status 2 dispatched "${race_args[@]}"
export PATH="$original_path"
jq -e '
  .status == "refused"
  and (.message | contains("never justifies overwriting"))
' "$tmp/result.json" >/dev/null
escaped_status="$(find "$repo" -name '*.status' -print -quit)"
assert_equal '' "$escaped_status" 'redirected status write persisted outside the status tree'
assert_equal "$repo_status_before" \
  "$(git -C "$repo" status --porcelain=v1 --untracked-files=all)" \
  'redirected status write changed the Repository working tree'

# Exit 1: invalid events are command errors.
run_status 1 invented "${status_args[@]}"
jq -e '.status == "error"' "$tmp/result.json" >/dev/null

printf 'test-qq-status: pass\n'
