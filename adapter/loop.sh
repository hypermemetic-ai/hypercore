#!/usr/bin/env bash
# hypercore loop orchestrator — the adapter's rigid workflow.
#
# Drives one work node through the loop's five gates (intent/loop.md), in two phases
# split at the operator's sign-off:
#
#   phase one — orient, frame — is interactive: the operator and the agent frame the
#     work together, and the operator SIGNS OFF. The machine never signs off itself.
#   phase two — implement, check, archive — runs on a CLEARED session: a fresh, memoryless
#     phase-two harness re-derives the work from the written work-node frame alone. If a
#     blank agent can build it from the frame, the frame was complete.
#
# The gates and their order are the loop, already intent; this script only operationalizes
# them and blocks a gate whose preconditions fail. It states no rule of its own. Where this
# script and the intent disagree, the intent wins.
#
# Usage:
#   loop.sh [-C <node-path>] start    <work-name>              scaffold the work node; print the orient gate
#   loop.sh [-C <node-path>] frame    <work-name>              check the frame is written and ready for sign-off
#   loop.sh [-C <node-path>] signoff  [<work-name> [<operator>]]
#                                                               record the operator's sign-off (the human gate)
#   loop.sh [-C <node-path>] execute  <work-name> [--dry-run]  run phase two on a cleared session
#   loop.sh [-C <node-path>] status   [--json] <work-name>     print the work node's current phase
#
# Env:
#   LOOP_HARNESS=codex (default and only supported phase-two harness)
#   HYPERCORE_LOOP_STATE_DIR (default: .hypercore/loop-runs under the root)
#   HYPERCORE_OPERATOR (optional sign-off identity when <operator> is omitted)
#   CODEX_BIN (default: codex), CODEX_APPROVAL (default: never)
#   CODEX_WRITE_SANDBOX (default: workspace-write), CODEX_READ_SANDBOX (default: read-only)

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
GATES="$HERE/gates"
NODE="$ROOT"
NODE_REL="."
INTENT_TREE=intent
WORKS="$NODE"
LOOP_HARNESS="${LOOP_HARNESS:-codex}"
HYPERCORE_LOOP_STATE_DIR="${HYPERCORE_LOOP_STATE_DIR:-$ROOT/.hypercore/loop-runs}"
CODEX_BIN="${CODEX_BIN:-codex}"
CODEX_APPROVAL="${CODEX_APPROVAL:-never}"
CODEX_WRITE_SANDBOX="${CODEX_WRITE_SANDBOX:-workspace-write}"
CODEX_READ_SANDBOX="${CODEX_READ_SANDBOX:-read-only}"
DRY_RUN="${DRY_RUN:-0}"
FRAME_REQUIRED_FIELDS=(
  "addressed node"
  "node-local work name"
  "target segments"
  "work in flight"
  "problem"
  "constraints"
  "route"
  "methodology adherence"
  "operator decisions"
  "authority"
  "machine assumptions"
  "evidence"
  "uncertainty"
  "open blockers"
  "feedback capture"
  "handoff state"
  "proof state"
  "sweep"
)
GATE_OUTPUT=""   # the last gate's captured output, read by cmd_execute for the sweep verdict
PHASE_TWO_SESSION_ID=""
PHASE_TWO_RUN_ACTIVE=0
LOOP_RUN_ID=""
LOOP_RUN_DIR=""
LOOP_RUN_STATE=""
LOOP_RUN_EVENTS=""
LOOP_RUN_GATE_DIR=""
LOOP_RUN_STARTED_AT=""
LOOP_CURRENT_WORK_STATE=""
LOOP_CURRENT_ROOT_STATE=""
LOOP_CURRENT_GATE=""

die() {
  local msg=$1
  if [ "${PHASE_TWO_RUN_ACTIVE:-0}" = 1 ] &&
     [ -n "${LOOP_RUN_DIR:-}" ] &&
     [ "${LOOP_STATE_DIE_ACTIVE:-0}" != 1 ]; then
    LOOP_STATE_DIE_ACTIVE=1
    loop_event failure "${LOOP_CURRENT_GATE:-unknown}" failed "$msg" || true
    loop_state_write "${LOOP_CURRENT_GATE:-unknown}" failed "$msg" || true
  fi
  printf 'loop: %s\n' "$msg" >&2
  exit 1
}

utc_stamp() {
  date -u '+%Y-%m-%dT%H:%M:%SZ'
}

utc_stamp_id() {
  date -u '+%Y%m%dT%H%M%SZ'
}

json_escape() {
  local s=${1-}
  s=${s//\\/\\\\}
  s=${s//\"/\\\"}
  s=${s//$'\n'/\\n}
  s=${s//$'\r'/\\r}
  s=${s//$'\t'/\\t}
  printf '%s' "$s"
}

json_string() {
  printf '"%s"' "$(json_escape "${1-}")"
}

short_message() {
  local s=${1-}
  if [ "${#s}" -gt 240 ]; then
    printf '%.237s...' "$s"
  else
    printf '%s' "$s"
  fi
}

phase_two_node_slug() {
  local s=$1
  [ "$s" = "." ] && s=root
  printf '%s' "$s" | tr '/ ' '__' | tr -c '[:alnum:]._-' '_'
}

current_work_state_path() {
  local work_name=$1 dir="$HYPERCORE_LOOP_STATE_DIR/current/work"
  [ "$NODE_REL" = "." ] || dir="$dir/$NODE_REL"
  printf '%s/%s.json' "$dir" "$work_name"
}

loop_execute_command() {
  local work_name=$1
  printf './adapter/loop.sh'
  [ "$NODE_REL" = "." ] || printf ' -C %q' "$NODE_REL"
  printf ' execute %q' "$work_name"
}

loop_state_write() {
  local gate=$1 status=$2 message=${3-} updated tmp
  [ -n "${LOOP_RUN_STATE:-}" ] || return 0
  LOOP_CURRENT_GATE="$gate"
  updated="$(utc_stamp)"
  tmp="$LOOP_RUN_STATE.tmp"
  {
    printf '{\n'
    printf '  "run_id": %s,\n' "$(json_string "$LOOP_RUN_ID")"
    printf '  "node": %s,\n' "$(json_string "$NODE_REL")"
    printf '  "work_name": %s,\n' "$(json_string "${LOOP_WORK_NAME:-}")"
    printf '  "phase": "phase-two",\n'
    printf '  "gate": %s,\n' "$(json_string "$gate")"
    printf '  "status": %s,\n' "$(json_string "$status")"
    printf '  "codex_thread_id": %s,\n' "$(json_string "$PHASE_TWO_SESSION_ID")"
    printf '  "started_at": %s,\n' "$(json_string "$LOOP_RUN_STARTED_AT")"
    printf '  "updated_at": %s,\n' "$(json_string "$updated")"
    printf '  "message": %s,\n' "$(json_string "$(short_message "$message")")"
    printf '  "paths": {\n'
    printf '    "run_dir": %s,\n' "$(json_string "$LOOP_RUN_DIR")"
    printf '    "state_json": %s,\n' "$(json_string "$LOOP_RUN_STATE")"
    printf '    "events_jsonl": %s,\n' "$(json_string "$LOOP_RUN_EVENTS")"
    printf '    "gate_outputs_dir": %s,\n' "$(json_string "$LOOP_RUN_GATE_DIR")"
    printf '    "current_work_state": %s,\n' "$(json_string "$LOOP_CURRENT_WORK_STATE")"
    printf '    "current_root_state": %s\n' "$(json_string "$LOOP_CURRENT_ROOT_STATE")"
    printf '  }\n'
    printf '}\n'
  } > "$tmp"
  mv "$tmp" "$LOOP_RUN_STATE"
  cp "$LOOP_RUN_STATE" "$LOOP_CURRENT_WORK_STATE"
  cp "$LOOP_RUN_STATE" "$LOOP_CURRENT_ROOT_STATE"
}

loop_event() {
  local event=$1 gate=$2 status=$3 message=${4-} ts
  [ -n "${LOOP_RUN_EVENTS:-}" ] || return 0
  ts="$(utc_stamp)"
  printf '{"ts":%s,"run_id":%s,"node":%s,"work_name":%s,"phase":"phase-two","gate":%s,"status":%s,"event":%s,"message":%s}\n' \
    "$(json_string "$ts")" \
    "$(json_string "$LOOP_RUN_ID")" \
    "$(json_string "$NODE_REL")" \
    "$(json_string "${LOOP_WORK_NAME:-}")" \
    "$(json_string "$gate")" \
    "$(json_string "$status")" \
    "$(json_string "$event")" \
    "$(json_string "$(short_message "$message")")" >> "$LOOP_RUN_EVENTS"
}

phase_two_run_init() {
  local work_name=$1 node_slug
  LOOP_WORK_NAME="$work_name"
  LOOP_RUN_STARTED_AT="$(utc_stamp)"
  node_slug="$(phase_two_node_slug "$NODE_REL")"
  LOOP_RUN_ID="$(utc_stamp_id)-$node_slug-$work_name-pid$$"
  LOOP_RUN_DIR="$HYPERCORE_LOOP_STATE_DIR/$LOOP_RUN_ID"
  LOOP_RUN_STATE="$LOOP_RUN_DIR/state.json"
  LOOP_RUN_EVENTS="$LOOP_RUN_DIR/events.jsonl"
  LOOP_RUN_GATE_DIR="$LOOP_RUN_DIR/gates"
  LOOP_CURRENT_WORK_STATE="$(current_work_state_path "$work_name")"
  LOOP_CURRENT_ROOT_STATE="$HYPERCORE_LOOP_STATE_DIR/current/root.json"

  mkdir -p "$LOOP_RUN_GATE_DIR" "$(dirname "$LOOP_CURRENT_WORK_STATE")" "$(dirname "$LOOP_CURRENT_ROOT_STATE")"
  : > "$LOOP_RUN_EVENTS"
  PHASE_TWO_RUN_ACTIVE=1
  loop_state_write preflight running "phase-two run initialized"
  loop_event preflight preflight running "phase-two run initialized"
}

can_write_dir() {
  local dir=$1 probe
  [ -d "$dir" ] || return 1
  probe="$dir/.hypercore-loop-preflight-$$"
  if ( : > "$probe" ) 2>/dev/null; then
    rm -f "$probe"
    return 0
  fi
  rm -f "$probe" 2>/dev/null || true
  return 1
}

phase_two_preflight_fail() {
  local reason=$1 work_name=$2 msg
  msg="preflight failed before codex exec: $reason; rerun the outer loop with that permission, using: $(loop_execute_command "$work_name")"
  loop_event preflight preflight failed "$msg"
  loop_state_write preflight failed "$msg"
  printf 'phase-two preflight failed: %s\n' "$reason" >&2
  printf 'rerun with outer escalation: %s\n' "$(loop_execute_command "$work_name")" >&2
  return 1
}

phase_two_preflight() {
  local work_name=$1 codex_home codex_parent reason msg
  LOOP_CURRENT_GATE=preflight
  msg="checking Codex binary and writable Codex home/session state"
  loop_event preflight preflight running "$msg"
  loop_state_write preflight running "$msg"

  if [ "$DRY_RUN" = 1 ]; then
    msg="dry-run: would check Codex binary and Codex home/session write permission before launching codex exec"
    loop_event preflight preflight skipped "$msg"
    loop_state_write preflight skipped "$msg"
    return 0
  fi

  command -v "$CODEX_BIN" >/dev/null 2>&1 \
    || phase_two_preflight_fail "Codex binary '$CODEX_BIN' is not on PATH" "$work_name" \
    || return 1

  if [ -n "${CODEX_HOME:-}" ]; then
    codex_home=$CODEX_HOME
  else
    [ -n "${HOME:-}" ] \
      || phase_two_preflight_fail "HOME is unset and CODEX_HOME is not set, so Codex home cannot be resolved" "$work_name" \
      || return 1
    codex_home=$HOME/.codex
  fi

  if [ -d "$codex_home/sessions" ]; then
    can_write_dir "$codex_home/sessions" \
      || reason="missing write permission for Codex sessions directory $codex_home/sessions"
  elif [ -d "$codex_home" ]; then
    can_write_dir "$codex_home" \
      || reason="missing write permission to create Codex sessions under $codex_home"
  else
    codex_parent="$(dirname "$codex_home")"
    can_write_dir "$codex_parent" \
      || reason="missing write permission to create Codex home $codex_home under $codex_parent"
  fi

  [ -z "${reason:-}" ] \
    || phase_two_preflight_fail "$reason" "$work_name" \
    || return 1

  msg="preflight passed: Codex binary is present and $codex_home can hold session state"
  loop_event preflight preflight passed "$msg"
  loop_state_write preflight passed "$msg"
}

ensure_work_history() {
  local d
  [ "$DRY_RUN" = 1 ] && return
  for d in \
    "$NODE/$INTENT_TREE/history/adopted" \
    "$NODE/$INTENT_TREE/history/shelved"
  do
    mkdir -p "$d"
    : > "$d/.gitkeep"
  done
}

work_name_ok() {
  local name=$1
  [ "$name" != archive ] && [[ "$name" =~ ^[0-9][0-9][0-9]-[[:alnum:]][[:alnum:]._-]*$ ]]
}

relpath() {
  local path=$1
  [ "$path" = "$ROOT" ] && { printf '.'; return; }
  printf '%s' "${path#"$ROOT"/}"
}

validate_work_name() {
  local name=$1
  [ -n "$name" ] || die "missing work name"
  [[ "$name" != */* ]] \
    || die "work name must be node-local: $name (use -C <node-path> to address another node)"
  work_name_ok "$name" || die "invalid work name: $name"
}

set_node() {
  local node_path=${1:-}
  [ -n "$node_path" ] || die "missing node path after -C"
  [[ "$node_path" != /* && "$node_path" != *//* ]] \
    || die "invalid node path: $node_path"

  [ -d "$ROOT/$node_path/$INTENT_TREE" ] \
    || die "node has no $INTENT_TREE/: $node_path"

  NODE="$(cd "$ROOT/$node_path" && pwd)"
  case "$NODE" in
    "$ROOT"|"$ROOT"/*) ;;
    *) die "node path escapes repository: $node_path" ;;
  esac
  NODE_REL="$(relpath "$NODE")"
  WORKS="$NODE"
}

is_work_node() {
  local d=${1%/}
  [ -d "$d/$INTENT_TREE" ]
}

frame_dir_for() {
  local d=${1%/}
  if is_work_node "$d"; then
    printf '%s' "$d/$INTENT_TREE/frame"
  else
    printf '%s' "$d"
  fi
}

active_work_dir() {
  local name=$1 d
  validate_work_name "$name"
  d=$WORKS/$name
  if is_work_node "$d"; then
    printf '%s' "$d"
    return 0
  fi
}

archived_work_dir() {
  local name=$1 d
  validate_work_name "$name"
  for d in \
    "$NODE/$INTENT_TREE/history/adopted/$name" \
    "$NODE/$INTENT_TREE/history/shelved/$name"
  do
    [ -d "$d" ] && { printf '%s' "$d"; return 0; }
  done
  return 1
}

any_work_dir() {
  local name=$1 active archived
  validate_work_name "$name"
  active="$(active_work_dir "$name" || true)"
  archived="$(archived_work_dir "$name" || true)"
  [ -n "$active" ] && [ -n "$archived" ] \
    && die "work exists both active and historical in node $NODE_REL: $name"
  [ -n "$active" ] && { printf '%s' "$active"; return 0; }
  [ -n "$archived" ] && { printf '%s' "$archived"; return 0; }
  return 1
}

new_work_collection() {
  ensure_work_history
  printf '%s' "$WORKS"
}

archive_collection_for_active_dir() {
  local d=${1%/} decision=${2:-adopted} collection
  ensure_work_history
  if [ "$decision" = shelved ]; then
    collection="$NODE/$INTENT_TREE/history/shelved"
  else
    collection="$NODE/$INTENT_TREE/history/adopted"
  fi
  [ "$DRY_RUN" = 1 ] || mkdir -p "$collection"
  printf '%s' "$collection"
}

archive_move() {
  local src=${1%/} dst_dir=${2%/} src_rel dst_rel tracked
  src_rel="$(relpath "$src")"
  dst_rel="$(relpath "$dst_dir")/$(basename "$src")"
  [ ! -e "$ROOT/$dst_rel" ] || die "archive destination already exists: $dst_rel"

  tracked="$(git -C "$ROOT" ls-files -- "$src_rel/")"
  if [ -n "$tracked" ]; then
    git -C "$ROOT" mv "$src_rel" "$(relpath "$dst_dir")/"
  else
    mv "$src" "$dst_dir/"
  fi
}

frame_has_markdown_files() {
  local frame=$1
  [ -n "$(find "$frame" -type f -name '*.md' ! -name signoff.md -print -quit 2>/dev/null)" ]
}

frame_field_has_content() {
  local frame=$1 label=$2
  [ -d "$frame" ] || return 1
  frame_has_markdown_files "$frame" || return 1
  find "$frame" -type f -name '*.md' ! -name signoff.md -exec awk -v label="$label" '
    function trim(s) {
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    function clean(s) {
      s = tolower(s)
      gsub(/<!--[^>]*-->/, " ", s)
      gsub(/[`*_]/, "", s)
      gsub(/[[:space:]]+/, " ", s)
      return trim(s)
    }
    function meaningful(s) {
      s = clean(s)
      if (s == "") return 0
      if (s ~ /^(todo|tbd|fill me|fill this|fill in|to be filled|placeholder|xxx)([ .:-]|$)/) return 0
      if (s ~ /^[^:]+:[[:space:]]*(todo|tbd|fill me|fill this|fill in|to be filled|placeholder|xxx)([ .:-]|$)/) return 0
      return 1
    }
    function heading_text(s) {
      sub(/^[[:space:]]*#+[[:space:]]*/, "", s)
      return clean(s)
    }
    BEGIN {
      target = clean(label)
      in_section = 0
      found = 0
    }
    /^[[:space:]]*```/ {
      fence = !fence
      next
    }
    fence { next }
    /^[[:space:]]*#+[[:space:]]+/ {
      h = heading_text($0)
      in_section = (h == target || index(h, target) > 0)
      next
    }
    {
      line = clean($0)
      prefix = target ":"
      if (substr(line, 1, length(prefix)) == prefix) {
        rest = substr(line, length(prefix) + 1)
        if (meaningful(rest)) {
          found = 1
          exit 0
        }
        next
      }
      if (in_section && meaningful($0)) {
        found = 1
        exit 0
      }
    }
    END { exit(found ? 0 : 1) }
  ' {} +
}

frame_any_field_has_content() {
  local frame=$1 field
  shift
  for field in "$@"; do
    frame_field_has_content "$frame" "$field" && return 0
  done
  return 1
}

frame_contract_errors_at() {
  local d=$1 frame field failed=0
  [ -d "$d" ] || { printf 'missing work directory\n'; return 1; }
  is_work_node "$d" || { printf 'active work must be a node with intent/\n'; return 1; }
  frame="$(frame_dir_for "$d")"
  [ -d "$frame" ] || { printf 'missing frame directory: %s\n' "$(relpath "$frame")"; return 1; }
  frame_has_markdown_files "$frame" \
    || { printf 'missing non-signoff markdown frame file under %s\n' "$(relpath "$frame")"; return 1; }

  for field in "${FRAME_REQUIRED_FIELDS[@]}"; do
    if ! frame_field_has_content "$frame" "$field"; then
      printf 'missing required frame field: %s\n' "$field"
      failed=1
    fi
  done
  if ! frame_any_field_has_content "$frame" "decision surface" "open direction"; then
    printf 'missing required frame field: decision surface or open direction\n'
    failed=1
  fi
  if ! frame_any_field_has_content "$frame" "adoption claim" "shelving claim"; then
    printf 'missing required frame field: adoption claim or shelving claim\n'
    failed=1
  fi
  [ "$failed" = 0 ]
}

frame_complete_at() {
  local d=$1
  [ -d "$d" ] || return 1
  frame_contract_errors_at "$d" >/dev/null
}

frame_complete() {
  local d
  d="$(any_work_dir "$1")" || return 1
  frame_complete_at "$d"
}

signed_off() {
  local d
  d="$(any_work_dir "$1")" || return 1
  signed_off_at "$d"
}

signed_off_at() {
  local d=$1 frame
  frame="$(frame_dir_for "$d")"
  [ -f "$frame/signoff.md" ] && grep -q '^signed-off-by:' "$frame/signoff.md"
}

signable_work_candidates() {
  local d name
  for d in "$WORKS"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "${d%/}")"
    work_name_ok "$name" || continue
    is_work_node "$d" || continue
    frame_complete_at "$d" || continue
    signed_off_at "$d" && continue
    printf '%s\n' "$name"
  done
}

infer_signoff_work_name() {
  local candidates=() name
  while IFS= read -r name; do candidates+=("$name"); done < <(signable_work_candidates)
  case "${#candidates[@]}" in
    1) printf '%s' "${candidates[0]}" ;;
    0) die "cannot infer work name: no frame-complete unsigned work node in node $NODE_REL; pass <work-name>" ;;
    *) die "cannot infer work name: multiple frame-complete unsigned work nodes in node $NODE_REL: ${candidates[*]}; pass <work-name>" ;;
  esac
}

current_operator_candidates() {
  local f
  for f in "$NODE/$INTENT_TREE"/*.md; do
    [ -f "$f" ] || continue
    tail -n 3 "$f" | sed -n 's/^endorsed by[[:space:]]\{1,\}//p'
  done | sort -u
}

infer_operator() {
  local env_operator="${HYPERCORE_OPERATOR:-}" candidates=() who
  if [ -n "$env_operator" ]; then
    case "$env_operator" in
      *$'\n'*|*$'\r'*) die "HYPERCORE_OPERATOR must be a single-line operator identity" ;;
    esac
    printf '%s' "$env_operator"
    return
  fi

  while IFS= read -r who; do candidates+=("$who"); done < <(current_operator_candidates)
  case "${#candidates[@]}" in
    1) printf '%s' "${candidates[0]}" ;;
    0) die "cannot infer operator: HYPERCORE_OPERATOR is unset and no current intent foot endorsement exists in node $NODE_REL; pass <operator>" ;;
    *) die "cannot infer operator: HYPERCORE_OPERATOR is unset and multiple current intent foot endorsements exist in node $NODE_REL: ${candidates[*]}; pass <operator> or set HYPERCORE_OPERATOR" ;;
  esac
}

check_green() { ( cd "$ROOT" && ./check.sh >/dev/null 2>&1 ); }

archive_decision_from_output() {
  case "$GATE_OUTPUT" in
    *"ARCHIVE_DECISION: SHELVED"*) printf 'shelved' ;;
    *"ARCHIVE_DECISION: ADOPTED"*) printf 'adopted' ;;
    *) die "no readable archive decision — phase two stops before recording history" ;;
  esac
}

phase() {
  local d
  d="$(archived_work_dir "$1")" && { echo "done"; return; }
  if d="$(active_work_dir "$1")"; then
    signed_off_at "$d" && { echo execute; return; }
    echo frame
    return
  fi
  echo missing
}

json_file_string_value() {
  local file=$1 key=$2
  if command -v jq >/dev/null 2>&1; then
    jq -r --arg key "$key" '.[$key] // empty | if type == "string" then . else empty end' "$file" 2>/dev/null
  else
    sed -nE 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/p' "$file" | sed -n '1p'
  fi
}

json_file_path_value() {
  local file=$1 key=$2
  if command -v jq >/dev/null 2>&1; then
    jq -r --arg key "$key" '.paths[$key] // empty | if type == "string" then . else empty end' "$file" 2>/dev/null
  else
    sed -nE 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/p' "$file" | sed -n '1p'
  fi
}

phase_two_state_file_for() {
  current_work_state_path "$1"
}

print_phase_two_status() {
  local work_name=$1 state run_id gate status updated message events
  state="$(phase_two_state_file_for "$work_name")"
  [ -s "$state" ] || return 0
  run_id="$(json_file_string_value "$state" run_id)"
  gate="$(json_file_string_value "$state" gate)"
  status="$(json_file_string_value "$state" status)"
  updated="$(json_file_string_value "$state" updated_at)"
  message="$(json_file_string_value "$state" message)"
  events="$(json_file_path_value "$state" events_jsonl)"
  printf 'phase-two run: run_id=%s gate=%s status=%s updated_at=%s state=%s events=%s message=%s\n' \
    "$run_id" "$gate" "$status" "$updated" "$state" "$events" "$message"
}

print_status_json() {
  local work_name=$1 ph frame_ok signed_ok state
  ph="$(phase "$work_name")"
  frame_ok=false
  signed_ok=false
  frame_complete "$work_name" && frame_ok=true
  signed_off "$work_name" && signed_ok=true
  state="$(phase_two_state_file_for "$work_name")"
  printf '{'
  printf '"work_name":%s,' "$(json_string "$work_name")"
  printf '"node":%s,' "$(json_string "$NODE_REL")"
  printf '"phase":%s,' "$(json_string "$ph")"
  printf '"frame_complete":%s,' "$frame_ok"
  printf '"signed_off":%s,' "$signed_ok"
  printf '"phase_two_run":'
  if [ -s "$state" ]; then
    cat "$state"
  else
    printf 'null'
  fi
  printf '}\n'
}

codex_sandbox_for_tools() {
  case "$1" in
    *Edit*|*Write*) printf '%s' "$CODEX_WRITE_SANDBOX" ;;
    *)              printf '%s' "$CODEX_READ_SANDBOX" ;;
  esac
}

codex_thread_id() {
  if command -v jq >/dev/null 2>&1; then
    jq -r 'select(.type=="thread.started") | .thread_id' 2>/dev/null | sed -n '1p'
  else
    sed -nE 's/.*"type":"thread\.started".*"thread_id":"([^"]+)".*/\1/p' | sed -n '1p'
  fi
}

codex_json_string_value() {
  local line=$1 key=$2
  if command -v jq >/dev/null 2>&1; then
    printf '%s\n' "$line" | jq -r --arg key "$key" '.[$key] // empty | if type == "string" then . else empty end' 2>/dev/null
  else
    printf '%s\n' "$line" | sed -nE 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/p' | sed -n '1p'
  fi
}

codex_progress_detail() {
  local line=$1
  if command -v jq >/dev/null 2>&1; then
    printf '%s\n' "$line" | jq -r '
      (.message? // .msg? // .text? // .command? // .name? // empty)
      | if type == "string" then . else empty end
    ' 2>/dev/null | sed -n '1p'
  else
    printf '%s\n' "$line" | sed -nE 's/.*"(message|msg|text|command|name)"[[:space:]]*:[[:space:]]*"([^"]*)".*/\2/p' | sed -n '1p'
  fi
}

record_codex_progress_line() {
  local gate=$1 line=$2 type detail thread_id msg
  type="$(codex_json_string_value "$line" type)"
  if [ -z "$type" ]; then
    msg="codex output: $(short_message "$line")"
    printf '[phase-two:%s] %s\n' "$gate" "$msg"
    loop_event codex-output "$gate" running "$msg"
    loop_state_write "$gate" running "$msg"
    return
  fi

  case "$type" in
    *delta*|*.delta|token.count) return ;;
  esac

  if [ "$type" = "thread.started" ]; then
    thread_id="$(codex_json_string_value "$line" thread_id)"
    msg="codex thread discovered"
    [ -n "$thread_id" ] && msg="$msg: $thread_id"
    printf '[phase-two:%s] %s\n' "$gate" "$msg"
    loop_event codex-thread "$gate" running "$msg"
    loop_state_write "$gate" running "$msg"
    return
  fi

  detail="$(codex_progress_detail "$line")"
  msg="$type"
  [ -n "$detail" ] && msg="$msg: $detail"
  printf '[phase-two:%s] %s\n' "$gate" "$(short_message "$msg")"
  loop_event codex-event "$gate" running "$msg"
  loop_state_write "$gate" running "$msg"
}

codex_cmd_prefix() {
  local sandbox="$1"
  CODEX_CMD=("$CODEX_BIN" -a "$CODEX_APPROVAL" -s "$sandbox" -C "$ROOT")
  [ -n "${CODEX_MODEL:-}" ] && CODEX_CMD+=(-m "$CODEX_MODEL")
  [ -n "${CODEX_PROFILE:-}" ] && CODEX_CMD+=(-p "$CODEX_PROFILE")
  return 0
}

run_codex_gate() {
  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" sys="$6" sandbox final combined
  local codex_events gate_output cmd_status pipeline_status msg
  sandbox="$(codex_sandbox_for_tools "$tools")"
  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-loop-codex-$gate-final.XXXXXX")"
  combined="$(printf '%s\n\n---\n\n%s' "$sys" "$prompt")"
  codex_events="$LOOP_RUN_DIR/events-codex-$gate.jsonl"
  gate_output="$LOOP_RUN_GATE_DIR/$gate.final.md"
  codex_cmd_prefix "$sandbox"

  case "$mode" in
    start)  CODEX_CMD+=(exec --json -o "$final" -) ;;
    resume)
      [ -n "$sid" ] || die "cannot resume codex gate $gate without a session id"
      CODEX_CMD+=(exec resume --json -o "$final" "$sid" -)
      ;;
    *) die "unknown gate mode: $mode" ;;
  esac

  msg="starting $gate gate with Codex sandbox $sandbox"
  loop_event gate-start "$gate" running "$msg"
  loop_state_write "$gate" running "$msg"

  if [ "$DRY_RUN" = 1 ]; then
    printf '{"type":"dry-run","gate":%s,"mode":%s}\n' "$(json_string "$gate")" "$(json_string "$mode")" > "$codex_events"
    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
    if [ "$mode" = start ]; then
      PHASE_TWO_SESSION_ID=dry-run-codex-session
      loop_event codex-thread "$gate" running "dry-run Codex thread: $PHASE_TWO_SESSION_ID"
    fi
    GATE_OUTPUT="(dry-run) $gate gate final output would be written by Codex."
    printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
    loop_event gate-finish "$gate" skipped "dry-run stored $gate final message at $gate_output"
    loop_state_write "$gate" skipped "dry-run stored $gate final message at $gate_output"
    rm -f "$final"
    return 0
  fi

  : > "$codex_events"
  set +e
  printf '%s' "$combined" | "${CODEX_CMD[@]}" | while IFS= read -r line || [ -n "$line" ]; do
    printf '%s\n' "$line" >> "$codex_events"
    record_codex_progress_line "$gate" "$line"
  done
  pipeline_status=("${PIPESTATUS[@]}")
  set -e
  cmd_status=${pipeline_status[1]}
  if [ "$cmd_status" -ne 0 ]; then
    [ -s "$final" ] && cp "$final" "$gate_output"
    msg="gate $gate failed: codex exec exited $cmd_status"
    loop_event gate-failure "$gate" failed "$msg"
    loop_state_write "$gate" failed "$msg"
    rm -f "$final"
    die "$msg"
  fi

  if [ "$mode" = start ]; then
    PHASE_TWO_SESSION_ID="$(codex_thread_id < "$codex_events")"
    [ -n "$PHASE_TWO_SESSION_ID" ] \
      || { rm -f "$final"; die "could not read codex thread id from gate $gate"; }
    loop_state_write "$gate" running "codex thread discovered: $PHASE_TWO_SESSION_ID"
  fi

  GATE_OUTPUT="$(cat "$final")"
  printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
  rm -f "$final"
  loop_event gate-finish "$gate" passed "stored $gate final message at $gate_output"
  loop_state_write "$gate" passed "stored $gate final message at $gate_output"
  printf '%s\n' "$GATE_OUTPUT"
}

# a single phase-two gate, run on the one cleared session.
# args: <gate-name> <allowed-tools> <mode> <session-id> <prompt>
# mode is start for the first gate (opens the cleared session) and resume for the rest
# (continues it), so phase two clears once, then works.
run_gate() {
  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" sys
  sys="$(cat "$GATES/$gate.md")"

  case "$LOOP_HARNESS" in
    codex) run_codex_gate "$gate" "$tools" "$mode" "$sid" "$prompt" "$sys" ;;
    *) die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)" ;;
  esac
}

cmd_start() {
  local work_name="${1:-}" collection d frame address template
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] start <work-name>"
  validate_work_name "$work_name"
  collection="$(new_work_collection)"
  d="$collection/$work_name"
  frame="$d/$INTENT_TREE/frame"
  address="$work_name"
  [ "$NODE_REL" = "." ] || address="$NODE_REL:$work_name"
  archived_work_dir "$work_name" >/dev/null 2>&1 \
    && die "work already historical in node $NODE_REL: $work_name"
  [ -e "$d" ] && ! is_work_node "$d" \
    && die "work path exists but is not a node in node $NODE_REL: $work_name"
  if [ ! -d "$d" ]; then
    mkdir -p "$frame"
    printf '# organizing document - %s\n\nThis work node keeps its design frame under intent/frame/.\n' "$address" > "$d/$INTENT_TREE/organizing-document.md"
    printf 'scaffolded %s\n' "$d"
  fi
  mkdir -p "$frame"
  template="$frame/frame.md"
  if [ ! -e "$template" ]; then
    {
      printf '# frame - %s\n\n' "$work_name"
      printf '## work\n\n'
      printf 'Addressed node: TODO\n\n'
      printf 'Node-local work name: %s\n\n' "$work_name"
      printf 'Target segments: TODO\n\n'
      printf 'Work in flight: TODO\n\n'
      printf '## problem\n\nTODO\n\n'
      printf '## constraints\n\nTODO\n\n'
      printf '## decision surface or open direction\n\nTODO\n\n'
      printf '## route\n\nTODO\n\n'
      printf '## methodology adherence\n\n'
      printf 'Work classification: TODO\n\n'
      printf 'Loop waiver: TODO\n\n'
      printf '## common ground\n\n'
      printf '### operator decisions\n\nTODO\n\n'
      printf '### authority\n\nTODO\n\n'
      printf '### machine assumptions\n\nTODO\n\n'
      printf '### evidence\n\nTODO\n\n'
      printf '### uncertainty\n\nTODO\n\n'
      printf '### open blockers\n\nTODO\n\n'
      printf '### feedback capture\n\nTODO\n\n'
      printf '### handoff state\n\nTODO\n\n'
      printf '## proof state\n\nTODO\n\n'
      printf '## sweep\n\nTODO\n\n'
      printf '## adoption claim\n\nTODO\n\n'
      printf '## shelving claim\n\nTODO\n'
    } > "$template"
  fi
  printf '\n=== gate: orient ===\n\n'; cat "$GATES/orient.md"
}

cmd_frame() {
  local work_name="${1:-}" d errors
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] frame <work-name>"
  validate_work_name "$work_name"
  d="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  if ! frame_complete_at "$d"; then
    errors="$(frame_contract_errors_at "$d" || true)"
    die "work-node frame incomplete under $(relpath "$(frame_dir_for "$d")"):
$errors"
  fi
  check_green || die "check.sh is red — fix before sign-off"
  if signed_off_at "$d"; then
    printf 'frame complete and already signed off; next: loop.sh'
    [ "$NODE_REL" = "." ] || printf ' -C %s' "$NODE_REL"
    printf ' execute %s\n' "$work_name"
  else
    printf 'frame complete and check.sh green. Awaiting the operator:\n'
    printf '  '
    if [ "$NODE_REL" = "." ]; then
      printf './signoff'
    else
      printf 'loop.sh -C %s signoff' "$NODE_REL"
    fi
    printf '        # infer unambiguous work and operator\n'
    printf '  loop.sh'
    [ "$NODE_REL" = "." ] || printf ' -C %s' "$NODE_REL"
    printf ' signoff %s <operator>\n' "$work_name"
  fi
}

cmd_signoff() {
  local work_name="${1:-}" who="${2:-}" d frame
  [ -z "${3:-}" ] || die "usage: loop.sh [-C <node-path>] signoff [<work-name> [<operator>]]"
  [ -n "$work_name" ] || work_name="$(infer_signoff_work_name)"
  [ -n "$who" ] || who="$(infer_operator)"
  validate_work_name "$work_name"
  d="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  frame_complete_at "$d" || die "cannot sign off an incomplete frame"
  check_green || die "check.sh is red — not signable"
  signed_off_at "$d" && die "already signed off"
  frame="$(frame_dir_for "$d")"
  printf '# signoff - %s\n\nsigned-off-by: %s\n' "$work_name" "$who" > "$frame/signoff.md"
  printf 'signed off by %s. The session now clears; phase two re-derives from the frame:\n' "$who"
  printf '  loop.sh'
  [ "$NODE_REL" = "." ] || printf ' -C %s' "$NODE_REL"
  printf ' execute %s\n' "$work_name"
}

cmd_execute() {
  local work_name="${1:-}" active_dir active_rel frame_rel source_desc archive_collection archive_decision
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] execute <work-name> [--dry-run]"
  validate_work_name "$work_name"
  shift
  [ "${1:-}" = "--dry-run" ] && DRY_RUN=1
  active_dir="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  active_rel="$(relpath "$active_dir")"
  frame_rel="$(relpath "$(frame_dir_for "$active_dir")")"
  signed_off_at "$active_dir" || die "not signed off — phase two is sealed until the operator signs off"
  source_desc="$frame_rel/ (the signed work-node frame)"

  # the session clears once at sign-off: one fresh Codex thread, opened by implement,
  # then resumed after.
  local sid
  [ "$LOOP_HARNESS" = codex ] \
    || die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)"
  sid=""
  printf '=== phase two: %s cleared session %s, re-deriving %s in node %s from its frame ===\n' \
    "$LOOP_HARNESS" "${sid:-new}" "$work_name" "$NODE_REL"
  phase_two_run_init "$work_name"
  if ! phase_two_preflight "$work_name"; then
    PHASE_TWO_RUN_ACTIVE=0
    exit 1
  fi

  run_gate implement "Read Edit Write Bash" start "$sid" \
    "Implement node-local work $work_name in addressed node $NODE_REL. Read only $source_desc and the intent it references; build the delta in code."
  sid="$PHASE_TWO_SESSION_ID"

  printf '\n--- gate: check (mechanical) ---\n'
  loop_event check check running "running ./check.sh"
  loop_state_write check running "running ./check.sh"
  if [ "$DRY_RUN" = 1 ]; then
    printf '(dry-run) would run: ./check.sh\n'
    loop_event check check skipped "dry-run skipped ./check.sh"
    loop_state_write check skipped "dry-run skipped ./check.sh"
  else
    if check_green; then
      loop_event check check passed "check.sh green after implement"
      loop_state_write check passed "check.sh green after implement"
    else
      loop_event check check failed "check.sh red after implement — drift, stopping"
      die "check.sh red after implement — drift, stopping"
    fi
    printf 'check.sh green\n'
  fi
  run_gate check "Read Write Bash" resume "$sid" \
    "Run the sweep on the built node-local work $work_name in addressed node $NODE_REL at $active_rel against the whole corpus and work in flight across the node tree, including related work named by the frame; return coherent (bool) and notes."

  # honor the sweep's flag: read the check gate's verdict sentinel and, when it flags the
  # corpus incoherent — or when no verdict can be read — halt phase two and hand the flag to
  # the operator rather than folding the delta. The sweep flags; the operator (with the proof)
  # settles; no archive decision rests on the sweep itself. Skipped under --dry-run (no output).
  if [ "$DRY_RUN" != 1 ]; then
    case "$GATE_OUTPUT" in
      *"SWEEP_VERDICT: INCOHERENT"*)
        loop_event sweep check failed "sweep verdict: incoherent"
        loop_state_write check failed "sweep verdict: incoherent"
        die "sweep flagged the corpus incoherent — phase two stops here for the operator; $work_name stays in flight, not adopted" ;;
      *"SWEEP_VERDICT: COHERENT"*)
        loop_event sweep check passed "sweep verdict: coherent"
        loop_state_write check passed "sweep verdict: coherent"
        printf 'sweep verdict: coherent — proceeding to adoption\n' ;;
      *)
        loop_event sweep check failed "no readable sweep verdict"
        loop_state_write check failed "no readable sweep verdict"
        die "no readable sweep verdict — phase two stops here for the operator; could not confirm coherence, so $work_name stays in flight, not adopted" ;;
    esac
  else
    loop_event sweep check skipped "dry-run skipped sweep verdict enforcement"
  fi

  run_gate archive "Read Edit Write" resume "$sid" \
    "Adopt or shelve node-local work $work_name in addressed node $NODE_REL from $active_rel according to its signed frame. If adopting, fold its accepted delta into that node's intent documents and stamp each touched segment's foot with the signed-off-by operator. End with ARCHIVE_DECISION: ADOPTED or ARCHIVE_DECISION: SHELVED."
  printf '\n--- gate: adoption history (move) ---\n'
  if [ "$DRY_RUN" = 1 ]; then
    archive_collection="$(archive_collection_for_active_dir "$active_dir" adopted)"
    printf '(dry-run) would: check.sh green, then git mv %s %s/\n' \
      "$active_rel" "$(relpath "$archive_collection")"
    loop_event archive archive skipped "dry-run would record $work_name in adopted history"
    loop_state_write archive skipped "dry-run would record $work_name in adopted history"
  else
    loop_event check archive running "running ./check.sh after archive fold"
    loop_state_write archive running "running ./check.sh after archive fold"
    if check_green; then
      loop_event check archive passed "check.sh green after archive fold"
    else
      loop_event check archive failed "check.sh red after fold — stopping before archive"
      die "check.sh red after fold — stopping before archive"
    fi
    archive_decision="$(archive_decision_from_output)"
    loop_event archive-decision archive passed "archive decision: $archive_decision"
    loop_state_write archive passed "archive decision: $archive_decision"
    archive_collection="$(archive_collection_for_active_dir "$active_dir" "$archive_decision")"
    archive_move "$active_dir" "$archive_collection"
    printf 'recorded %s in %s history for node %s\n' "$work_name" "$archive_decision" "$NODE_REL"
  fi
  loop_event completion archive complete "phase two complete for $work_name"
  loop_state_write archive complete "phase two complete for $work_name"
  PHASE_TWO_RUN_ACTIVE=0
}

cmd_status() {
  local json=0 work_name
  if [ "${1:-}" = "--json" ]; then
    json=1
    shift
  fi
  work_name="${1:-}"
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] status [--json] <work-name>"
  validate_work_name "$work_name"
  if [ "$json" = 1 ]; then
    print_status_json "$work_name"
    return
  fi
  printf '%s in node %s: phase=%s frame_complete=%s signed_off=%s\n' "$work_name" "$NODE_REL" "$(phase "$work_name")" \
    "$(frame_complete "$work_name" && echo yes || echo no)" \
    "$(signed_off "$work_name" && echo yes || echo no)"
  print_phase_two_status "$work_name"
}

main() {
  while [ "${1:-}" = "-C" ]; do
    shift
    set_node "${1:-}"
    shift
  done

  local sub="${1:-}"; shift || true
  case "$sub" in
    start)   cmd_start   "$@";;
    frame)   cmd_frame   "$@";;
    signoff) cmd_signoff "$@";;
    execute) cmd_execute "$@";;
    status)  cmd_status  "$@";;
    *) die "usage: loop.sh [-C <node-path>] {start|frame|signoff|execute|status} <work-name> [...]";;
  esac
}
main "$@"
