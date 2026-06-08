#!/usr/bin/env bash
# hypercore loop orchestrator — the adapter's rigid workflow.
#
# Drives one work node through the loop's five gates (intent/loop.md), in two phases
# split at the operator's sign-off:
#
#   phase one — orient, frame — is interactive: the operator and the agent frame the
#     work together, and the operator SIGNS OFF. The machine never signs off itself.
#   phase two — implement, check, archive — runs through cleared, memoryless phase-two
#     sessions that re-derive the work from the written work-node frame alone. Builders
#     work in signed-frame implementation units; independent acceptance sessions check
#     those units before archive can fold one-way work.
#
# The gates and their order are the loop, already intent; this script only operationalizes
# them and blocks a gate whose preconditions fail. It states no rule of its own. Where this
# script and the intent disagree, the intent wins.
#
# Usage:
#   loop.sh [-C <node-path>] start    <work-name>              scaffold the work node; print the orient gate
#   loop.sh [-C <node-path>] direct   [<work-name> [<operator>]]
#                                                               select a neutral direction option
#   loop.sh [-C <node-path>] direct   [<work-name> [<operator>]]
#                                      --route|--constraint|--delegate <text-or->
#                                                               legacy/admin direction text form
#   loop.sh [-C <node-path>] review   <work-name> [--add <role>]...
#                                                               spawn/read the one-way review roster
#   loop.sh [-C <node-path>] frame    <work-name>              check the frame is written and ready for sign-off
#   loop.sh [-C <node-path>] signoff  [<work-name> [<operator>]]
#                                                               record the operator's sign-off (the human gate)
#   loop.sh [-C <node-path>] execute  [<work-name>] [--dry-run] run phase two on a cleared session
#   loop.sh [-C <node-path>] status   [--json] <work-name>     print the work node's current phase
#
# Env:
#   LOOP_HARNESS=codex (default and only supported phase-two harness)
#   HYPERCORE_LOOP_STATE_DIR (default: .hypercore/loop-runs under the root)
#   HYPERCORE_OPERATOR (optional sign-off identity when <operator> is omitted)
#   CODEX_BIN (default: codex), CODEX_APPROVAL (default: never)
#   CODEX_WRITE_SANDBOX (default: workspace-write), CODEX_READ_SANDBOX (default: read-only)
#   CODEX_BUILDER_MODEL (default: gpt-5.5 until the two-step plan/build lands), CODEX_BUILDER_EFFORT (default: xhigh)
#   CODEX_STRONG_BUILDER_MODEL (optional strong-builder escalation model)
#   CODEX_STRONG_BUILDER_EFFORT (default: CODEX_REVIEW_EFFORT or xhigh)
#   CODEX_REVIEW_MODEL (optional strong review/acceptance model), CODEX_REVIEW_EFFORT (default: xhigh)
#   HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR (optional stable dry-run acceptance dir for self-tests)

set -euo pipefail

LOOP_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOOP_SCRIPT_PATH="$LOOP_SCRIPT_DIR/$(basename "${BASH_SOURCE[0]}")"
if [ "${HYPERCORE_LOOP_SNAPSHOT_ACTIVE:-0}" = 1 ]; then
  HERE="${HYPERCORE_LOOP_ORIGINAL_HERE:-$LOOP_SCRIPT_DIR}"
  ROOT="${HYPERCORE_LOOP_ORIGINAL_ROOT:-$(cd "$HERE/.." && pwd)}"
else
  HERE="$LOOP_SCRIPT_DIR"
  ROOT="$(cd "$HERE/.." && pwd)"
fi
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
  "decision surface or open direction"
  "reversibility"
  "route"
  "acceptance condition"
  "observable acceptance"
  "excluded interpretation"
  "proof state"
  "sweep"
  "adoption or shelving claim"
)
BASE_REVIEW_ROLES=(
  "contract-checkability"
  "soundness-fit"
  "simplicity-fastness"
  "red-team"
)
OPTIONAL_REVIEW_ROLES=(
  "implementation-maintainability"
  "security-permissions"
  "operator-ergonomics"
  "migration-compatibility"
  "domain-evidence"
  "performance-cost"
)
TIER_TWO_PANEL_LENSES=(
  "whole-acceptance-conformance"
  "proof-integrity"
  "independent-coherence"
  "security-permissions"
  "red-team"
)
GATE_OUTPUT=""   # the last gate's captured output, read by cmd_execute for archive decisions and handoffs
PHASE_TWO_SESSION_ID=""
PHASE_TWO_RUN_ACTIVE=0
PHASE_TWO_FRAME_DIR=""
PHASE_TWO_ACCEPTANCE_DIR=""
PHASE_TWO_UNITS_DIR=""
PHASE_TWO_HANDOFF_DIR=""
PHASE_TWO_DIFF_DIR=""
PHASE_TWO_TIER_ONE_DIR=""
PHASE_TWO_PANEL_DIR=""
LOOP_CURRENT_UNIT=""
LOOP_FAILURE_REASON=""
LOOP_RUN_ID=""
LOOP_RUN_DIR=""
LOOP_RUN_STATE=""
LOOP_RUN_EVENTS=""
LOOP_RUN_GATE_DIR=""
LOOP_RUN_STARTED_AT=""
LOOP_CURRENT_WORK_STATE=""
LOOP_CURRENT_ROOT_STATE=""
LOOP_CURRENT_GATE=""
UNIT_ATTEMPT_REASON=""
UNIT_CHECK_STATUS_MSG=""
UNIT_ACCEPTED_STATUS_MSG=""

die() {
  local msg=$1
  LOOP_FAILURE_REASON="$msg"
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
    printf '  "current_unit": %s,\n' "$(json_string "$LOOP_CURRENT_UNIT")"
    printf '  "codex_thread_id": %s,\n' "$(json_string "$PHASE_TWO_SESSION_ID")"
    printf '  "started_at": %s,\n' "$(json_string "$LOOP_RUN_STARTED_AT")"
    printf '  "updated_at": %s,\n' "$(json_string "$updated")"
    printf '  "message": %s,\n' "$(json_string "$(short_message "$message")")"
    printf '  "failure_reason": %s,\n' "$(json_string "$LOOP_FAILURE_REASON")"
    printf '  "paths": {\n'
    printf '    "run_dir": %s,\n' "$(json_string "$LOOP_RUN_DIR")"
    printf '    "state_json": %s,\n' "$(json_string "$LOOP_RUN_STATE")"
    printf '    "events_jsonl": %s,\n' "$(json_string "$LOOP_RUN_EVENTS")"
    printf '    "gate_outputs_dir": %s,\n' "$(json_string "$LOOP_RUN_GATE_DIR")"
    printf '    "current_work_state": %s,\n' "$(json_string "$LOOP_CURRENT_WORK_STATE")"
    printf '    "current_root_state": %s,\n' "$(json_string "$LOOP_CURRENT_ROOT_STATE")"
    printf '    "phase_two_acceptance_dir": %s,\n' "$(json_string "$PHASE_TWO_ACCEPTANCE_DIR")"
    printf '    "units_dir": %s,\n' "$(json_string "$PHASE_TWO_UNITS_DIR")"
    printf '    "handoffs_dir": %s,\n' "$(json_string "$PHASE_TWO_HANDOFF_DIR")"
    printf '    "diffs_dir": %s,\n' "$(json_string "$PHASE_TWO_DIFF_DIR")"
    printf '    "tier_one_dir": %s,\n' "$(json_string "$PHASE_TWO_TIER_ONE_DIR")"
    printf '    "tier_two_panel_dir": %s\n' "$(json_string "$PHASE_TWO_PANEL_DIR")"
    printf '  }\n'
    printf '}\n'
  } > "$tmp"
  mv "$tmp" "$LOOP_RUN_STATE"
  if [ "$DRY_RUN" != 1 ]; then
    cp "$LOOP_RUN_STATE" "$LOOP_CURRENT_WORK_STATE"
    cp "$LOOP_RUN_STATE" "$LOOP_CURRENT_ROOT_STATE"
  fi
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
  local work_name=$1 node_slug active_dir
  LOOP_WORK_NAME="$work_name"
  LOOP_CURRENT_UNIT=""
  LOOP_FAILURE_REASON=""
  LOOP_RUN_STARTED_AT="$(utc_stamp)"
  node_slug="$(phase_two_node_slug "$NODE_REL")"
  LOOP_RUN_ID="$(utc_stamp_id)-$node_slug-$work_name-pid$$"
  LOOP_RUN_DIR="$HYPERCORE_LOOP_STATE_DIR/$LOOP_RUN_ID"
  LOOP_RUN_STATE="$LOOP_RUN_DIR/state.json"
  LOOP_RUN_EVENTS="$LOOP_RUN_DIR/events.jsonl"
  LOOP_RUN_GATE_DIR="$LOOP_RUN_DIR/gates"
  LOOP_CURRENT_WORK_STATE="$(current_work_state_path "$work_name")"
  LOOP_CURRENT_ROOT_STATE="$HYPERCORE_LOOP_STATE_DIR/current/root.json"
  active_dir="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  PHASE_TWO_FRAME_DIR="$(frame_dir_for "$active_dir")"
  if [ "$DRY_RUN" = 1 ] && [ -n "${HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR:-}" ]; then
    PHASE_TWO_ACCEPTANCE_DIR="$HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR"
  elif [ "$DRY_RUN" = 1 ]; then
    PHASE_TWO_ACCEPTANCE_DIR="$LOOP_RUN_DIR/phase-two-dry-run"
  else
    PHASE_TWO_ACCEPTANCE_DIR="$PHASE_TWO_FRAME_DIR/phase-two"
  fi
  PHASE_TWO_UNITS_DIR="$PHASE_TWO_ACCEPTANCE_DIR/units"
  PHASE_TWO_HANDOFF_DIR="$PHASE_TWO_ACCEPTANCE_DIR/handoffs"
  PHASE_TWO_DIFF_DIR="$PHASE_TWO_ACCEPTANCE_DIR/diffs"
  PHASE_TWO_TIER_ONE_DIR="$PHASE_TWO_ACCEPTANCE_DIR/tier-one"
  PHASE_TWO_PANEL_DIR="$PHASE_TWO_ACCEPTANCE_DIR/tier-two-panel"

  mkdir -p \
    "$LOOP_RUN_GATE_DIR" \
    "$(dirname "$LOOP_CURRENT_WORK_STATE")" \
    "$(dirname "$LOOP_CURRENT_ROOT_STATE")" \
    "$PHASE_TWO_UNITS_DIR" \
    "$PHASE_TWO_HANDOFF_DIR" \
    "$PHASE_TWO_DIFF_DIR" \
    "$PHASE_TWO_TIER_ONE_DIR" \
    "$PHASE_TWO_PANEL_DIR"
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

phase_two_reexec_from_snapshot() {
  local sub=$1 snapshot_dir snapshot_path node_slug cmd=()
  shift
  [ "$sub" = execute ] || return 0
  [ "${HYPERCORE_LOOP_SNAPSHOT_ACTIVE:-0}" = 1 ] && return 0

  node_slug="$(phase_two_node_slug "$NODE_REL")"
  snapshot_dir="$HYPERCORE_LOOP_STATE_DIR/snapshots/$(utc_stamp_id)-$node_slug-pid$$"
  snapshot_path="$snapshot_dir/loop.sh"
  mkdir -p "$snapshot_dir"
  cp "$LOOP_SCRIPT_PATH" "$snapshot_path"
  chmod 500 "$snapshot_path"

  [ "$NODE_REL" = "." ] || cmd+=(-C "$NODE_REL")
  cmd+=("$sub" "$@")
  export HYPERCORE_LOOP_SNAPSHOT_ACTIVE=1
  export HYPERCORE_LOOP_SNAPSHOT_PATH="$snapshot_path"
  export HYPERCORE_LOOP_ORIGINAL_HERE="$HERE"
  export HYPERCORE_LOOP_ORIGINAL_ROOT="$ROOT"
  exec "$snapshot_path" "${cmd[@]}"
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

work_number_for_name() {
  local name=$1
  printf '%s' "${name%%-*}"
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
  return 1
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
  [ -f "$frame/frame.md" ]
}

meaningful_text() {
  local s=${1-}
  s="$(printf '%s' "$s" | tr '\r\n\t' '   ' | sed -E 's/[[:space:]]+/ /g; s/^[[:space:]]+//; s/[[:space:]]+$//')"
  [ -n "$s" ] || return 1
  case "$(printf '%s' "$s" | tr '[:upper:]' '[:lower:]')" in
    todo|todo\ *|tbd|tbd\ *|fill\ me|fill\ me\ *|fill\ this|fill\ this\ *|fill\ in|fill\ in\ *|to\ be\ filled|to\ be\ filled\ *|placeholder|placeholder\ *|xxx|xxx\ *)
      return 1
      ;;
  esac
  printf '%s' "$s"
}

frame_label_has_content() {
  local file=$1 label=$2
  [ -f "$file" ] || return 1
  awk -v label="$label" '
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
      return 1
    }
    BEGIN {
      target = clean(label) ":"
      found = 0
    }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    {
      line = $0
      lowered = clean(line)
      if (substr(lowered, 1, length(target)) == target) {
        rest = substr(line, index(line, ":") + 1)
        if (meaningful(rest)) {
          found = 1
          exit 0
        }
      }
    }
    END { exit(found ? 0 : 1) }
  ' "$file"
}

frame_section_has_content() {
  local file=$1 heading=$2
  [ -f "$file" ] || return 1
  awk -v heading="$heading" '
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
      return 1
    }
    function heading_level(s) {
      match(s, /^#+/)
      return RLENGTH
    }
    function heading_text(s) {
      sub(/^[[:space:]]*#+[[:space:]]*/, "", s)
      return clean(s)
    }
    BEGIN {
      target = clean(heading)
      in_section = 0
      found = 0
    }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    /^[[:space:]]*#+[[:space:]]+/ {
      level = heading_level($0)
      h = heading_text($0)
      if (in_section && level <= 2) {
        exit(found ? 0 : 1)
      }
      if (level == 2 && h == target) {
        in_section = 1
        next
      }
      next
    }
    in_section && meaningful($0) {
      found = 1
      exit 0
    }
    END { exit(found ? 0 : 1) }
  ' "$file"
}

frame_label_value_from_file() {
  local file=$1 label=$2
  [ -f "$file" ] || return 1
  awk -v label="$label" '
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
      return 1
    }
    BEGIN {
      target = clean(label) ":"
      found = 0
    }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    {
      line = $0
      lowered = clean(line)
      if (substr(lowered, 1, length(target)) == target) {
        rest = substr(line, index(line, ":") + 1)
        rest = trim(rest)
        if (meaningful(rest)) {
          found = 1
          print rest
          exit 0
        }
      }
    }
    END { exit(found ? 0 : 1) }
  ' "$file"
}

frame_section_excerpt_from_file() {
  local file=$1 heading=$2 limit=${3:-6}
  [ -f "$file" ] || return 1
  awk -v heading="$heading" -v limit="$limit" '
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
      return 1
    }
    function heading_level(s) {
      match(s, /^#+/)
      return RLENGTH
    }
    function heading_text(s) {
      sub(/^[[:space:]]*#+[[:space:]]*/, "", s)
      return clean(s)
    }
    function emit(s) {
      s = trim(s)
      if (!meaningful(s)) return
      print s
      count += 1
      if (count >= limit) exit 0
    }
    BEGIN {
      target = clean(heading)
      in_section = 0
      count = 0
    }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    /^[[:space:]]*#+[[:space:]]+/ {
      level = heading_level($0)
      h = heading_text($0)
      if (in_section && level <= 2) {
        exit(count > 0 ? 0 : 1)
      }
      if (level == 2 && h == target) {
        in_section = 1
        next
      }
      if (in_section) emit($0)
      next
    }
    in_section { emit($0) }
    END { exit(count > 0 ? 0 : 1) }
  ' "$file"
}

frame_reversibility_value_from_file() {
  local file=$1
  [ -f "$file" ] || return 1
  awk '
    function trim(s) {
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    function clean(s) {
      s = tolower(trim(s))
      gsub(/[[:space:]]+/, " ", s)
      return s
    }
    BEGIN { count = 0; value = "" }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    {
      line = $0
      lowered = clean(line)
      if (substr(lowered, 1, length("reversibility:")) == "reversibility:") {
        rest = clean(substr(line, index(line, ":") + 1))
        if (rest == "one-way" || rest == "two-way") {
          count += 1
          value = rest
        } else if (rest != "" && rest !~ /^(todo|tbd|placeholder|xxx)$/) {
          count += 100
        }
      }
    }
    END {
      if (count == 1) {
        print value
        exit 0
      }
      exit 1
    }
  ' "$file"
}

frame_reversibility_value_at() {
  local d=$1 frame
  frame="$(frame_dir_for "$d")"
  frame_reversibility_value_from_file "$frame/frame.md"
}

frame_field_has_content() {
  local frame=$1 label=$2 file="$frame/frame.md"
  [ -f "$file" ] || return 1
  case "$label" in
    "addressed node") frame_label_has_content "$file" "Addressed node" ;;
    "node-local work name") frame_label_has_content "$file" "Node-local work name" ;;
    "target segments") frame_label_has_content "$file" "Target segments" ;;
    "work in flight") frame_label_has_content "$file" "Work in flight" ;;
    "problem") frame_section_has_content "$file" "problem" ;;
    "constraints") frame_section_has_content "$file" "constraints" ;;
    "decision surface or open direction")
      frame_section_has_content "$file" "decision surface or open direction" ||
        frame_label_has_content "$file" "Decision surface" ||
        frame_label_has_content "$file" "Open direction"
      ;;
    "reversibility") frame_reversibility_value_from_file "$file" >/dev/null ;;
    "route")
      frame_section_has_content "$file" "route" ||
        frame_label_has_content "$file" "Route"
      ;;
    "acceptance condition")
      frame_section_has_content "$file" "acceptance condition" ||
        frame_label_has_content "$file" "Acceptance condition"
      ;;
    "observable acceptance")
      frame_section_has_content "$file" "observable acceptance" ||
        frame_label_has_content "$file" "Observable acceptance"
      ;;
    "excluded interpretation")
      frame_section_has_content "$file" "excluded interpretation" ||
        frame_label_has_content "$file" "Excluded interpretation"
      ;;
    "proof state") frame_section_has_content "$file" "proof state" ;;
    "sweep") frame_section_has_content "$file" "sweep" ;;
    "adoption or shelving claim")
      frame_section_has_content "$file" "adoption claim" ||
        frame_section_has_content "$file" "shelving claim" ||
        frame_label_has_content "$file" "Adoption claim" ||
        frame_label_has_content "$file" "Shelving claim"
      ;;
    *) return 1 ;;
  esac
}

frame_route_has_content_at() {
  local d=$1 frame
  frame="$(frame_dir_for "$d")"
  frame_field_has_content "$frame" route
}

loop_cmd_prefix() {
  printf 'loop.sh'
  [ "$NODE_REL" = "." ] || printf ' -C %s' "$NODE_REL"
}

direction_command_hint() {
  local work_name=$1
  if [ "$NODE_REL" = "." ]; then
    printf './direction %s [operator]' "$work_name"
  else
    printf '%s direct %s [operator]' "$(loop_cmd_prefix)" "$work_name"
  fi
}

direction_options_contract_errors_at() {
  local d=$1 frame file
  frame="$(frame_dir_for "$d")"
  file="$frame/options.md"
  if [ ! -f "$file" ]; then
    printf 'missing direction options artifact: %s\n' "$(relpath "$file")"
    return 1
  fi
  awk '
    function trim(s) {
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    function clean(s) {
      s = tolower(trim(s))
      gsub(/[`*_]/, "", s)
      gsub(/[[:space:]]+/, " ", s)
      return s
    }
    function meaningful(s) {
      s = clean(s)
      if (s == "") return 0
      if (s ~ /^(todo|tbd|fill me|fill this|fill in|to be filled|placeholder|xxx)([ .:-]|$)/) return 0
      return 1
    }
    function fail(msg) {
      printf "malformed direction options artifact: %s\n", msg
      failed = 1
    }
    function reset_option() {
      id = ""
      kind = ""
      summary = ""
      reversibility = ""
      tradeoff = ""
      current_field = ""
    }
    function append_field(line) {
      line = trim(line)
      if (line == "") return
      if (current_field == "summary") summary = trim(summary " " line)
      if (current_field == "tradeoff") tradeoff = trim(tradeoff " " line)
    }
    function supported_kind(value) {
      value = clean(value)
      return value == "selected-route" || value == "constraint" || value == "delegation"
    }
    function finish_option() {
      if (!option_open) return
      if (!meaningful(id)) fail("option " current_option " missing id:")
      if (!meaningful(kind)) {
        fail("option " current_option " missing kind:")
      } else if (!supported_kind(kind)) {
        fail("option " current_option " has unsupported kind:")
      }
      if (!meaningful(summary)) fail("option " current_option " missing summary:")
      if (!meaningful(reversibility)) {
        fail("option " current_option " missing reversibility:")
      } else if (clean(reversibility) != "one-way" && clean(reversibility) != "two-way") {
        fail("option " current_option " reversibility: must be one-way or two-way")
      }
      if (!meaningful(tradeoff)) fail("option " current_option " missing tradeoff:")
      id_key = clean(id)
      if (meaningful(id)) {
        if (id_seen[id_key]) fail("option ids must be unique")
        id_seen[id_key] = 1
      }
      summary_key = clean(summary)
      if (meaningful(summary)) {
        if (summary_seen[summary_key]) fail("option summaries must be materially distinct")
        summary_seen[summary_key] = 1
      }
      option_open = 0
    }
    BEGIN {
      failed = 0
      expected = 1
      option_count = 0
      option_open = 0
      in_rejection = 0
      none_count = 0
      abort_count = 0
      reset_option()
    }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    {
      line = $0
      lowered = clean(line)
      if (lowered ~ /^(recommended|recommendation|default|preferred|machine recommendation|machine-recommendation):/) {
        fail("neutral options must not mark a recommendation, default, or preferred choice")
      }
    }
    lowered ~ /^## option [0-9]+$/ {
      finish_option()
      heading = lowered
      sub(/^## option /, "", heading)
      number = heading + 0
      if (number != expected) fail("option headings must be numbered contiguously from 1")
      option_count += 1
      expected += 1
      current_option = number
      option_open = 1
      in_rejection = 0
      reset_option()
      next
    }
    lowered == "## rejection choices" {
      finish_option()
      in_rejection = 1
      next
    }
    lowered ~ /^## / {
      finish_option()
      in_rejection = 0
      next
    }
    option_open && lowered ~ /^(id|kind|summary|reversibility|tradeoff):/ {
      label = lowered
      sub(/:.*/, "", label)
      value = line
      sub(/^[[:space:]]*[^:]*:[[:space:]]*/, "", value)
      value = trim(value)
      if (label == "id") id = value
      if (label == "kind") kind = value
      if (label == "summary") summary = value
      if (label == "reversibility") reversibility = value
      if (label == "tradeoff") tradeoff = value
      current_field = label
      next
    }
    option_open && lowered ~ /^[[:alnum:]][[:alnum:]_-]*:/ {
      current_field = ""
      next
    }
    option_open && current_field != "" {
      append_field(line)
      next
    }
    in_rejection && lowered ~ /^none:/ {
      value = line
      sub(/^[[:space:]]*[^:]*:[[:space:]]*/, "", value)
      if (meaningful(value)) {
        none_count += 1
      } else {
        fail("none: rejection choice must be substantive")
      }
      next
    }
    in_rejection && lowered ~ /^abort:/ {
      value = line
      sub(/^[[:space:]]*[^:]*:[[:space:]]*/, "", value)
      if (meaningful(value)) {
        abort_count += 1
      } else {
        fail("abort: rejection choice must be substantive")
      }
      next
    }
    END {
      finish_option()
      if (option_count < 2) fail("at least two numbered options are required")
      if (none_count != 1) fail("exactly one none: rejection choice is required")
      if (abort_count != 1) fail("exactly one abort: rejection choice is required")
      exit(failed ? 1 : 0)
    }
  ' "$file"
}

direction_options_table_at() {
  local d=$1 frame file
  frame="$(frame_dir_for "$d")"
  file="$frame/options.md"
  awk '
    function trim(s) {
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    function clean(s) {
      s = tolower(trim(s))
      gsub(/[`*_]/, "", s)
      gsub(/[[:space:]]+/, " ", s)
      return s
    }
    function meaningful(s) {
      s = clean(s)
      if (s == "") return 0
      return 1
    }
    function reset_option() {
      id = ""
      kind = ""
      summary = ""
      reversibility = ""
      tradeoff = ""
      current_field = ""
    }
    function append_field(line) {
      line = trim(line)
      if (line == "") return
      if (current_field == "summary") summary = trim(summary " " line)
      if (current_field == "tradeoff") tradeoff = trim(tradeoff " " line)
    }
    function finish_option() {
      if (!option_open) return
      gsub(/\t/, " ", id)
      gsub(/\t/, " ", kind)
      gsub(/\t/, " ", summary)
      gsub(/\t/, " ", reversibility)
      gsub(/\t/, " ", tradeoff)
      printf "%s\t%s\t%s\t%s\t%s\t%s\n", current_option, kind, summary, reversibility, tradeoff, id
      option_open = 0
    }
    BEGIN { option_open = 0; reset_option() }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    {
      line = $0
      lowered = clean(line)
    }
    lowered ~ /^## option [0-9]+$/ {
      finish_option()
      heading = lowered
      sub(/^## option /, "", heading)
      current_option = heading + 0
      option_open = 1
      reset_option()
      next
    }
    lowered ~ /^## / {
      finish_option()
      next
    }
    option_open && lowered ~ /^(id|kind|summary|reversibility|tradeoff):/ {
      label = lowered
      sub(/:.*/, "", label)
      value = line
      sub(/^[[:space:]]*[^:]*:[[:space:]]*/, "", value)
      value = trim(value)
      if (label == "id") id = value
      if (label == "kind") kind = value
      if (label == "summary") summary = value
      if (label == "reversibility") reversibility = value
      if (label == "tradeoff") tradeoff = value
      current_field = label
      next
    }
    option_open && lowered ~ /^[[:alnum:]][[:alnum:]_-]*:/ {
      current_field = ""
      next
    }
    option_open && current_field != "" && meaningful(line) {
      append_field(line)
      next
    }
    END { finish_option() }
  ' "$file"
}

direction_rejection_choice_text_at() {
  local d=$1 choice=$2 frame file
  frame="$(frame_dir_for "$d")"
  file="$frame/options.md"
  awk -v choice="$choice" '
    function trim(s) {
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    function clean(s) {
      s = tolower(trim(s))
      gsub(/[`*_]/, "", s)
      gsub(/[[:space:]]+/, " ", s)
      return s
    }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    {
      line = $0
      lowered = clean(line)
    }
    lowered == "## rejection choices" { in_rejection = 1; next }
    lowered ~ /^## / { in_rejection = 0; next }
    in_rejection && index(lowered, choice ":") == 1 {
      value = line
      sub(/^[[:space:]]*[^:]*:[[:space:]]*/, "", value)
      print trim(value)
      exit
    }
  ' "$file"
}

direction_selected_field_value_from_file() {
  local file=$1
  awk '
    function trim(s) {
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    {
      line = $0
      lowered = tolower(line)
      gsub(/^[[:space:]]+/, "", lowered)
      if (lowered ~ /^(selected-route|constraint|delegation):/) {
        label = lowered
        sub(/:.*/, "", label)
        value = line
        sub(/^[[:space:]]*[^:]*:[[:space:]]*/, "", value)
        print label "\t" trim(value)
        exit
      }
    }
  ' "$file"
}

direction_selection_matches_options_at() {
  local d=$1 selected_field=$2 selected_value=$3
  local number kind summary reversibility tradeoff id
  while IFS=$'\t' read -r number kind summary reversibility tradeoff id; do
    if [ "$kind" = "$selected_field" ] && [ "$summary" = "$selected_value" ]; then
      return 0
    fi
  done < <(direction_options_table_at "$d")
  return 1
}

direction_options_prompt_at() {
  local d=$1 work_name=$2 frame file number kind summary reversibility tradeoff id none_text abort_text
  frame="$(frame_dir_for "$d")"
  file="$frame/options.md"
  none_text="$(direction_rejection_choice_text_at "$d" none)"
  abort_text="$(direction_rejection_choice_text_at "$d" abort)"
  {
    printf 'operator gate: direction for %s\n' "$work_name"
    printf 'Select one neutral option from %s.\n\n' "$(relpath "$file")"
    while IFS=$'\t' read -r number kind summary reversibility tradeoff id; do
      printf '%s. %s\n' "$number" "$summary"
      printf '   kind: %s; reversibility: %s; id: %s\n' "$kind" "$reversibility" "$id"
      printf '   tradeoff: %s\n' "$tradeoff"
    done < <(direction_options_table_at "$d")
    printf '\nn. none of these - %s\n' "$none_text"
    printf 'q. abort - %s\n' "$abort_text"
    printf 'Choice: '
  }
}

direction_option_choice_from_tty() {
  local d=$1 work_name=$2 errors prompt choice normalized number kind summary reversibility tradeoff id
  if ! errors="$(direction_options_contract_errors_at "$d")"; then
    die "$errors"
  fi
  prompt="$(direction_options_prompt_at "$d" "$work_name")"
  OPERATOR_GATE_TOKEN=""
  operator_gate_read_token "$prompt"
  choice="$(meaningful_text "$OPERATOR_GATE_TOKEN" || true)"
  normalized="$(printf '%s' "$choice" | tr '[:upper:]' '[:lower:]')"
  case "$normalized" in
    n|none)
      die "direction not recorded: operator selected none-of-these; return to frame"
      ;;
    q|abort)
      die "direction aborted by operator"
      ;;
    ""|*[!0-9]*)
      die "invalid direction option: ${OPERATOR_GATE_TOKEN:-<empty>}"
      ;;
  esac
  while IFS=$'\t' read -r number kind summary reversibility tradeoff id; do
    if [ "$number" = "$choice" ]; then
      DIRECTION_SELECTED_FIELD="$kind"
      DIRECTION_SELECTED_VALUE="$summary"
      DIRECTION_SELECTED_GATE="tty"
      return 0
    fi
  done < <(direction_options_table_at "$d")
  die "invalid direction option: $choice"
}

operator_gate_contract_errors_in_file() {
  local file=$1 label=$2
  [ -f "$file" ] || { printf 'malformed %s: missing operator-gate:\n' "$label"; return 1; }
  awk -v label="$label" '
    BEGIN {
      count = 0
      failed = 0
      value = ""
    }
    /^operator-gate:/ {
      count += 1
      rest = $0
      sub(/^operator-gate:[[:space:]]*/, "", rest)
      sub(/[[:space:]]+$/, "", rest)
      gate_value = rest
      next
    }
    END {
      if (count == 0) {
        printf "malformed %s: missing operator-gate:\n", label
        exit 1
      }
      if (count > 1) {
        printf "malformed %s: exactly one operator-gate: line is required\n", label
        failed = 1
      }
      if (count == 1) {
        # B-ready gate token: a scheme, optionally <scheme>:<value> (e.g. a later
        # hmac:<...>). The syntax stays open so a future keyed scheme parses without
        # a format change, but only the tty liveness scheme is implemented here.
        colon = index(gate_value, ":")
        if (colon > 0) {
          scheme = substr(gate_value, 1, colon - 1)
          payload = substr(gate_value, colon + 1)
        } else {
          scheme = gate_value
          payload = ""
        }
        if (scheme !~ /^[a-z][a-z0-9-]*$/ || (colon > 0 && payload == "")) {
          printf "malformed %s: operator-gate: must be a gate token (tty or <scheme>:<value>)\n", label
          failed = 1
        } else if (scheme != "tty") {
          printf "malformed %s: operator-gate: unsupported scheme %s; only tty is implemented in this route\n", label, scheme
          failed = 1
        } else if (payload != "") {
          printf "malformed %s: operator-gate: tty takes no value\n", label
          failed = 1
        }
      }
      exit(failed ? 1 : 0)
    }
  ' "$file"
}

operator_gate_bootstrap_allowed_at() {
  local d=$1 frame_file
  # Narrow bootstrap for the signed work that introduces the gate. Its frame explicitly
  # excludes a retroactive claim that its already-recorded operator artifacts used it.
  [ "$NODE_REL" = "." ] || return 1
  [ "$(basename "$d")" = "009-operator-acts" ] || return 1
  frame_file="$(frame_dir_for "$d")/frame.md"
  [ -f "$frame_file" ] || return 1
  grep -Fq "this work's already" "$frame_file" \
    && grep -Fq "recorded \`direction.md\` and later sign-off" "$frame_file" \
    && grep -Fq "gate exists" "$frame_file"
}

operator_gate_open() {
  if [ "${HYPERCORE_OPERATOR_GATE_TEST_NO_TTY:-0}" = 1 ]; then
    die "operator gate requires /dev/tty; no controlling terminal is available"
  fi
  if ! exec {OPERATOR_GATE_FD}<>/dev/tty; then
    OPERATOR_GATE_FD=""
    die "operator gate requires /dev/tty; no controlling terminal is available"
  fi
}

operator_gate_close() {
  if [ -n "${OPERATOR_GATE_FD:-}" ]; then
    exec {OPERATOR_GATE_FD}>&- || true
    OPERATOR_GATE_FD=""
  fi
}

operator_gate_read_token() {
  local prompt=$1 token
  operator_gate_open
  printf '%s' "$prompt" >&"$OPERATOR_GATE_FD"
  if ! IFS= read -r token <&"$OPERATOR_GATE_FD"; then
    operator_gate_close
    die "operator gate failed to read from /dev/tty"
  fi
  operator_gate_close
  OPERATOR_GATE_TOKEN="$token"
}

operator_gate_confirm_work() {
  local action=$1 work_name=$2 prompt
  OPERATOR_GATE_TOKEN=""
  prompt="operator gate: $action for $work_name
Type $work_name to confirm: "
  operator_gate_read_token "$prompt"
  [ "$OPERATOR_GATE_TOKEN" = "$work_name" ] \
    || die "operator gate confirmation failed: expected $work_name"
  printf 'tty'
}

signoff_attestation_section_at() {
  local d=$1 title=$2 heading=$3 limit=${4:-6} frame file
  frame="$(frame_dir_for "$d")"
  file="$frame/frame.md"
  printf '%s:\n' "$title"
  if ! frame_section_excerpt_from_file "$file" "$heading" "$limit" | sed 's/^/  /'; then
    printf '  <missing from frame.md>\n'
  fi
}

signoff_attestation_brief_at() {
  local d=$1 work_name=$2 who=$3 frame file work_number target_segments reversibility
  frame="$(frame_dir_for "$d")"
  file="$frame/frame.md"
  work_number="$(work_number_for_name "$work_name")"
  target_segments="$(frame_label_value_from_file "$file" "Target segments" || printf '<missing from frame.md>')"
  reversibility="$(frame_reversibility_value_from_file "$file" || printf '<missing from frame.md>')"
  {
    printf 'operator gate: sign-off for %s\n' "$work_name"
    printf 'Operator: %s\n' "$who"
    printf 'Frame: %s\n' "$(relpath "$file")"
    printf 'Target segments: %s\n' "$target_segments"
    printf 'Reversibility: %s\n\n' "$reversibility"
    printf 'Attestation brief from frame.md:\n'
    signoff_attestation_section_at "$d" "Route" "route" 8
    signoff_attestation_section_at "$d" "Acceptance condition" "acceptance condition" 5
    signoff_attestation_section_at "$d" "Observable acceptance" "observable acceptance" 5
    signoff_attestation_section_at "$d" "Excluded interpretation" "excluded interpretation" 5
    printf '\nType work number %s to confirm: ' "$work_number"
  }
}

operator_gate_confirm_signoff() {
  local d=$1 work_name=$2 who=$3 expected prompt
  OPERATOR_GATE_TOKEN=""
  expected="$(work_number_for_name "$work_name")"
  prompt="$(signoff_attestation_brief_at "$d" "$work_name" "$who")"
  operator_gate_read_token "$prompt"
  [ "$OPERATOR_GATE_TOKEN" = "$expected" ] \
    || die "operator gate confirmation failed: expected work number $expected"
  printf 'tty'
}

review_command_hint() {
  local work_name=$1
  if [ "$NODE_REL" = "." ]; then
    printf './review %s [--add <role>]...' "$work_name"
  else
    printf '%s review %s [--add <role>]...' "$(loop_cmd_prefix)" "$work_name"
  fi
}

direction_given_at() {
  local d=$1 frame file
  frame="$(frame_dir_for "$d")"
  file="$frame/direction.md"
  [ -f "$file" ] || return 1
  sed -nE 's/^direction-given-at:[[:space:]]*([^[:space:]].*)$/\1/p' "$file" | sed -n '1p'
}

direction_contract_errors_at() {
  local d=$1 frame file field count=0 failed=0 errors selection selected_field="" selected_value=""
  frame="$(frame_dir_for "$d")"
  file="$frame/direction.md"
  if [ ! -f "$file" ]; then
    printf 'missing direction artifact: %s; next: %s\n' "$(relpath "$file")" "$(direction_command_hint "$(basename "$d")")"
    return 1
  fi

  frame_label_has_content "$file" "direction-by" \
    || { printf 'malformed direction artifact: missing direction-by:\n'; failed=1; }
  if frame_label_has_content "$file" "direction-given-at"; then
    sed -nE 's/^direction-given-at:[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z[[:space:]]*$/ok/p' "$file" | grep -qx ok \
      || { printf 'malformed direction artifact: direction-given-at must be UTC YYYY-MM-DDTHH:MM:SSZ\n'; failed=1; }
  else
    printf 'malformed direction artifact: missing direction-given-at:\n'
    failed=1
  fi
  if ! operator_gate_bootstrap_allowed_at "$d" &&
     ! operator_gate_contract_errors_in_file "$file" "direction artifact"; then
    failed=1
  fi

  for field in selected-route constraint delegation; do
    frame_label_has_content "$file" "$field" && count=$((count + 1))
  done
  if [ "$count" -eq 0 ]; then
    printf 'malformed direction artifact: exactly one of selected-route:, constraint:, or delegation: must be substantive\n'
    failed=1
  elif [ "$count" -gt 1 ]; then
    printf 'malformed direction artifact: only one of selected-route:, constraint:, or delegation: may be present\n'
    failed=1
  else
    selection="$(direction_selected_field_value_from_file "$file" || true)"
    if [ -n "$selection" ]; then
      IFS=$'\t' read -r selected_field selected_value <<< "$selection"
    fi
  fi
  if ! operator_gate_bootstrap_allowed_at "$d"; then
    if ! errors="$(direction_options_contract_errors_at "$d")"; then
      printf '%s\n' "$errors"
      failed=1
    elif [ "$count" -eq 1 ] &&
         ! direction_selection_matches_options_at "$d" "$selected_field" "$selected_value"; then
      printf 'malformed direction artifact: selected direction must be copied from a numbered option in options.md\n'
      failed=1
    fi
  fi
  [ "$failed" = 0 ]
}

signoff_contract_errors_at() {
  local d=$1 frame file failed=0
  frame="$(frame_dir_for "$d")"
  file="$frame/signoff.md"
  if [ ! -f "$file" ]; then
    printf 'missing sign-off artifact: %s\n' "$(relpath "$file")"
    return 1
  fi
  frame_label_has_content "$file" "signed-off-by" \
    || { printf 'malformed sign-off artifact: missing signed-off-by:\n'; failed=1; }
  if ! operator_gate_bootstrap_allowed_at "$d"; then
    if frame_label_has_content "$file" "signed-off-at"; then
      sed -nE 's/^signed-off-at:[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z[[:space:]]*$/ok/p' "$file" | grep -qx ok \
        || { printf 'malformed sign-off artifact: signed-off-at must be UTC YYYY-MM-DDTHH:MM:SSZ\n'; failed=1; }
    else
      printf 'malformed sign-off artifact: missing signed-off-at:\n'
      failed=1
    fi
    if ! operator_gate_contract_errors_in_file "$file" "sign-off artifact"; then
      failed=1
    fi
  fi
  [ "$failed" = 0 ]
}

direction_is_retrospective_at() {
  local d=$1 frame file frame_file frame_mtime direction_mtime
  frame="$(frame_dir_for "$d")"
  file="$frame/direction.md"
  frame_file="$frame/frame.md"
  [ -f "$file" ] && [ -f "$frame_file" ] || return 1
  frame_route_has_content_at "$d" || return 1
  frame_mtime="$(stat -c %Y "$frame_file" 2>/dev/null || printf 0)"
  direction_mtime="$(stat -c %Y "$file" 2>/dev/null || printf 0)"
  [ "$direction_mtime" -gt "$frame_mtime" ]
}

review_role_verdict() {
  local file=$1 role=$2
  [ -f "$file" ] || return 1
  awk -v role="$role" '
    function clean(s) {
      s = tolower(s)
      gsub(/[`*_]/, "", s)
      gsub(/[[:space:]]+/, " ", s)
      sub(/^[[:space:]-]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    BEGIN { found = 0; verdict = "" }
    {
      line = clean($0)
      prefix = role ":"
      if (substr(line, 1, length(prefix)) == prefix) {
        rest = substr(line, length(prefix) + 1)
        sub(/^[[:space:]]+/, "", rest)
        if (rest ~ /^pass([[:space:]]|$)/) { verdict = "PASS"; found = 1; exit }
        if (rest ~ /^flag([[:space:]]|$)/) { verdict = "FLAG"; found = 1; exit }
      }
    }
    END {
      if (found) {
        print verdict
        exit 0
      }
      exit 1
    }
  ' "$file"
}

review_disposition_ok() {
  local file=$1
  [ -f "$file" ] || return 1
  awk '
    function clean(s) {
      s = tolower(s)
      gsub(/[`*_]/, "", s)
      gsub(/[[:space:]]+/, " ", s)
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    BEGIN { found = 0 }
    {
      line = clean($0)
      if (substr(line, 1, length("disposition:")) == "disposition:") {
        rest = substr(line, length("disposition:") + 1)
        sub(/^[[:space:]]+/, "", rest)
        if (rest ~ /^(resolved|escalated)([[:space:]-]|$)/) {
          found = 1
          exit
        }
      }
    }
    END { exit(found ? 0 : 1) }
  ' "$file"
}

review_contract_errors_at() {
  local d=$1 frame file role verdict failed=0 base_flag=0
  frame="$(frame_dir_for "$d")"
  file="$frame/review.md"
  if [ ! -f "$file" ]; then
    printf 'missing one-way review artifact: %s; next: %s\n' "$(relpath "$file")" "$(review_command_hint "$(basename "$d")")"
    return 1
  fi
  frame_label_has_content "$file" "Overall" \
    || { printf 'malformed review artifact: missing Overall: PASS or FLAG\n'; failed=1; }
  for role in "${BASE_REVIEW_ROLES[@]}"; do
    verdict="$(review_role_verdict "$file" "$role" || true)"
    case "$verdict" in
      PASS) ;;
      FLAG) base_flag=1 ;;
      *) printf 'malformed review artifact: missing base verdict for %s as PASS or FLAG\n' "$role"; failed=1 ;;
    esac
  done
  if [ "$base_flag" = 1 ] && ! review_disposition_ok "$file"; then
    printf 'unresolved base-roster or red-team review flags require Disposition: resolved or Disposition: escalated; optional reviewers cannot clear them\n'
    failed=1
  elif ! frame_label_has_content "$file" "Disposition"; then
    printf 'malformed review artifact: missing Disposition:\n'
    failed=1
  fi
  [ "$failed" = 0 ]
}

frame_contract_errors_at() {
  local d=$1 frame field failed=0 reversibility errors
  [ -d "$d" ] || { printf 'missing work directory\n'; return 1; }
  is_work_node "$d" || { printf 'active work must be a node with intent/\n'; return 1; }
  frame="$(frame_dir_for "$d")"
  [ -d "$frame" ] || { printf 'missing frame directory: %s\n' "$(relpath "$frame")"; return 1; }
  frame_has_markdown_files "$frame" \
    || { printf 'missing canonical frame file: %s\n' "$(relpath "$frame/frame.md")"; return 1; }

  for field in "${FRAME_REQUIRED_FIELDS[@]}"; do
    if ! frame_field_has_content "$frame" "$field"; then
      printf 'missing required frame field: %s\n' "$field"
      failed=1
    fi
  done
  if ! errors="$(direction_contract_errors_at "$d")"; then
    printf '%s\n' "$errors"
    failed=1
  fi
  if frame_route_has_content_at "$d" && [ ! -f "$frame/direction.md" ]; then
    printf 'route is populated before substantive direction; next: clear route content, then run %s before framing the route\n' "$(direction_command_hint "$(basename "$d")")"
    failed=1
  fi
  if direction_is_retrospective_at "$d"; then
    printf 'direction appears retrospective: %s is newer than a populated %s; record operator direction before framing the route\n' \
      "$(relpath "$frame/direction.md")" "$(relpath "$frame/frame.md")"
    failed=1
  fi
  reversibility="$(frame_reversibility_value_at "$d" || true)"
  if [ "$reversibility" = "one-way" ]; then
    if ! errors="$(review_contract_errors_at "$d")"; then
      printf '%s\n' "$errors"
      failed=1
    fi
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
  [ -f "$frame/signoff.md" ] && signoff_contract_errors_at "$d" >/dev/null
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

executable_work_candidates() {
  local d name
  for d in "$WORKS"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "${d%/}")"
    work_name_ok "$name" || continue
    is_work_node "$d" || continue
    signed_off_at "$d" || continue
    printf '%s\n' "$name"
  done
}

infer_execute_work_name() {
  local candidates=() name
  while IFS= read -r name; do candidates+=("$name"); done < <(executable_work_candidates)
  case "${#candidates[@]}" in
    1) printf '%s' "${candidates[0]}" ;;
    0) die "cannot infer work name: no signed, unarchived work node in node $NODE_REL; pass <work-name>" ;;
    *) die "cannot infer work name: multiple signed, unarchived work nodes in node $NODE_REL: ${candidates[*]}; pass <work-name>" ;;
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
  local adopted shelved
  adopted="$(printf '%s\n' "$GATE_OUTPUT" | grep -Ec '^ARCHIVE_DECISION:[[:space:]]*ADOPTED[[:space:]]*$' || true)"
  shelved="$(printf '%s\n' "$GATE_OUTPUT" | grep -Ec '^ARCHIVE_DECISION:[[:space:]]*SHELVED[[:space:]]*$' || true)"
  if [ "$adopted" -eq 1 ] && [ "$shelved" -eq 0 ]; then
    printf 'adopted'
  elif [ "$shelved" -eq 1 ] && [ "$adopted" -eq 0 ]; then
    printf 'shelved'
  else
    die "archive decision must be exactly one line: ARCHIVE_DECISION: ADOPTED or ARCHIVE_DECISION: SHELVED"
  fi
}

phase_two_units_from_frame_file() {
  local file=$1
  [ -f "$file" ] || return 1
  awk '
    function trim(s) {
      sub(/^[[:space:]]+/, "", s)
      sub(/[[:space:]]+$/, "", s)
      return s
    }
    function emit() {
      if (current != "") {
        count += 1
        printf "unit-%03d\t%s\n", count, trim(current)
        current = ""
      }
    }
    BEGIN {
      in_units = 0
      current = ""
      count = 0
    }
    /^[[:space:]]*##[[:space:]]+/ && in_units {
      emit()
      exit
    }
    tolower($0) ~ /^[[:space:]]*implementation units for phase two:[[:space:]]*$/ {
      in_units = 1
      next
    }
    in_units {
      line = $0
      if (line ~ /^[[:space:]]*[0-9]+[.)][[:space:]]+/) {
        emit()
        sub(/^[[:space:]]*[0-9]+[.)][[:space:]]+/, "", line)
        current = trim(line)
        next
      }
      if (current != "" && line !~ /^[[:space:]]*$/) {
        current = current " " trim(line)
      }
    }
    END {
      if (in_units) {
        emit()
      }
      if (count == 0) {
        exit 1
      }
    }
  ' "$file"
}

write_current_diff_record() {
  local path=$1 tmp
  tmp="$path.tmp.$$"
  if command -v git >/dev/null 2>&1 &&
     git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    {
      printf '# worktree diff record\n\n'
      printf 'Recorded at: %s\n\n' "$(utc_stamp)"
      printf '## status\n\n'
      printf 'Tracked changes only; untracked files are excluded from this unit diff record.\n\n'
      git -C "$ROOT" status --short --untracked-files=no
      printf '\n## diff\n\n'
      git -C "$ROOT" diff --binary
    } > "$tmp"
  else
    {
      printf '# worktree diff record\n\n'
      printf 'Recorded at: %s\n\n' "$(utc_stamp)"
      printf 'git diff unavailable; repository state could not be captured.\n'
    } > "$tmp"
  fi
  mv "$tmp" "$path"
}

phase_two_unit_tier_one_resumable() {
  # Dead-simple resume: a unit is reusable on a rerun iff its tier-one
  # acceptance artifact is already on disk as a clean PASS for this signed
  # frame. No content hashing, no loop-version key, no per-unit cache record --
  # the artifact lives in this frame's own phase-two tree, so its presence is
  # the signal. In a real run it must be a real-reviewer, non-dry-run PASS.
  local tier_one_path=$1 verdict
  [ -f "$tier_one_path" ] || return 1
  verdict="$(acceptance_artifact_verdict "$tier_one_path" || true)"
  [ "$verdict" = PASS ] || return 1
  acceptance_artifact_field_meaningful "$tier_one_path" Rationale || return 1
  acceptance_artifact_field_meaningful "$tier_one_path" Evidence || return 1
  acceptance_artifact_field_meaningful "$tier_one_path" source-proof || return 1
  if [ "$DRY_RUN" != 1 ]; then
    [ "$(acceptance_artifact_source "$tier_one_path" || true)" = real-reviewer ] || return 1
    acceptance_artifact_dry_run "$tier_one_path" && return 1
  fi
  return 0
}
phase_two_write_handoff() {
  local unit_id=$1 proof=$2 output_path=$3 handoff_path=$4 tmp
  tmp="$handoff_path.tmp.$$"
  {
    printf '# handoff - %s\n\n' "$unit_id"
    printf 'unit: %s\n\n' "$unit_id"
    printf 'proof obligation: %s\n\n' "$proof"
    printf 'builder-output-path: %s\n\n' "$output_path"
    printf '## builder final output\n\n'
    printf '%s\n' "$GATE_OUTPUT"
  } > "$tmp"
  mv "$tmp" "$handoff_path"
}

phase_two_write_unit_record() {
  local unit_id=$1 status=$2 proof=$3 handoff_path=$4 diff_path=$5 tier_one_path=$6 message=${7-} tmp path
  path="$PHASE_TWO_UNITS_DIR/$unit_id.md"
  tmp="$path.tmp.$$"
  {
    printf '# phase-two unit - %s\n\n' "$unit_id"
    printf 'unit: %s\n' "$unit_id"
    printf 'status: %s\n' "$status"
    printf 'updated-at: %s\n' "$(utc_stamp)"
    printf 'proof-obligation: %s\n' "$proof"
    printf 'handoff-path: %s\n' "$(relpath "$handoff_path")"
    printf 'diff-path: %s\n' "$(relpath "$diff_path")"
    printf 'tier-one-verdict-path: %s\n' "$(relpath "$tier_one_path")"
    [ -n "$message" ] && printf 'message: %s\n' "$(short_message "$message")"
  } > "$tmp"
  mv "$tmp" "$path"
}

acceptance_output_field_count() {
  local output=$1 field=$2
  printf '%s\n' "$output" | awk -v field="$field" '
    BEGIN { target = toupper(field) ":"; count = 0 }
    {
      line = $0
      sub(/^[[:space:]]+/, "", line)
      upper = toupper(line)
      if (index(upper, target) == 1) count++
    }
    END { print count + 0 }
  '
}

acceptance_output_first_field_value() {
  local output=$1 field=$2
  printf '%s\n' "$output" | awk -v field="$field" '
    BEGIN { target = toupper(field) ":" }
    {
      line = $0
      sub(/^[[:space:]]+/, "", line)
      upper = toupper(line)
      if (index(upper, target) == 1) {
        sub(/^[^:]*:[[:space:]]*/, "", line)
        sub(/[[:space:]]+$/, "", line)
        print line
        exit
      }
    }
  '
}

acceptance_output_verdict_value() {
  local output=$1
  printf '%s\n' "$output" | awk '
    {
      line = $0
      sub(/^[[:space:]]+/, "", line)
      upper = toupper(line)
      if (index(upper, "VERDICT:") == 1) {
        sub(/^[^:]*:[[:space:]]*/, "", line)
        sub(/[[:space:]]+$/, "", line)
        value = toupper(line)
        if (value == "PASS" || value == "FLAG") print value
        exit
      }
    }
  '
}

acceptance_output_has_required_fields() {
  local output=$1 verdict_count rationale_count evidence_count verdict rationale evidence
  verdict_count="$(acceptance_output_field_count "$output" VERDICT)"
  rationale_count="$(acceptance_output_field_count "$output" RATIONALE)"
  evidence_count="$(acceptance_output_field_count "$output" EVIDENCE)"
  verdict="$(acceptance_output_verdict_value "$output")"
  rationale="$(acceptance_output_first_field_value "$output" RATIONALE)"
  evidence="$(acceptance_output_first_field_value "$output" EVIDENCE)"
  [ "$verdict_count" -eq 1 ] || return 1
  [ "$verdict" = PASS ] || [ "$verdict" = FLAG ] || return 1
  [ "$rationale_count" -ge 1 ] || return 1
  [ "$evidence_count" -ge 1 ] || return 1
  meaningful_text "$rationale" >/dev/null || return 1
  meaningful_text "$evidence" >/dev/null || return 1
}

acceptance_verdict_from_output() {
  local output=$1 status=$2
  [ "$status" -eq 0 ] || { printf 'FLAG'; return; }
  if acceptance_output_has_required_fields "$output"; then
    acceptance_output_verdict_value "$output"
  else
    printf 'FLAG'
  fi
}

acceptance_note_from_output() {
  local output=$1 status=$2 verdict_count rationale_count evidence_count verdict rationale evidence
  if [ "$status" -ne 0 ]; then
    short_message "acceptance reviewer subprocess exited $status; counted as FLAG"
    return
  fi
  verdict_count="$(acceptance_output_field_count "$output" VERDICT)"
  rationale_count="$(acceptance_output_field_count "$output" RATIONALE)"
  evidence_count="$(acceptance_output_field_count "$output" EVIDENCE)"
  verdict="$(acceptance_output_verdict_value "$output")"
  rationale="$(acceptance_output_first_field_value "$output" RATIONALE)"
  evidence="$(acceptance_output_first_field_value "$output" EVIDENCE)"
  if [ "$verdict_count" -ne 1 ] || { [ "$verdict" != PASS ] && [ "$verdict" != FLAG ]; }; then
    short_message "missing or malformed VERDICT field; counted as FLAG"
  elif [ "$rationale_count" -lt 1 ] || ! meaningful_text "$rationale" >/dev/null; then
    short_message "missing or empty RATIONALE field; counted as FLAG"
  elif [ "$evidence_count" -lt 1 ] || ! meaningful_text "$evidence" >/dev/null; then
    short_message "missing or empty EVIDENCE field; counted as FLAG"
  elif [ "$verdict" = PASS ]; then
    short_message "structured acceptance verdict PASS with rationale and evidence"
  else
    short_message "structured acceptance verdict FLAG with rationale and evidence"
  fi
}

acceptance_source_proof() {
  case "$1" in
    real-reviewer)
      printf 'real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only'
      ;;
    dry-run/self-test)
      printf 'dry-run self-test output generated by loop; rejected by real archive'
      ;;
    fake/self-test)
      printf 'fake acceptance loaded from HYPERCORE_ACCEPTANCE_FAKE_DIR in dry-run; rejected by real archive'
      ;;
    *)
      printf 'unsupported acceptance source'
      ;;
  esac
}

acceptance_finalize_result() {
  local output=$1 status=$2 source=$3
  ACCEPTANCE_OUTPUT="$output"
  ACCEPTANCE_SOURCE="$source"
  ACCEPTANCE_VERDICT="$(acceptance_verdict_from_output "$output" "$status")"
  ACCEPTANCE_NOTES="$(acceptance_note_from_output "$output" "$status")"
  ACCEPTANCE_RATIONALE="$(acceptance_output_first_field_value "$output" RATIONALE)"
  ACCEPTANCE_EVIDENCE="$(acceptance_output_first_field_value "$output" EVIDENCE)"
}

run_acceptance_reviewer() {
  local reviewer_key=$1 prompt=$2 output status final tmpout tmperr fake_file timeout_seconds
  ACCEPTANCE_VERDICT=FLAG
  ACCEPTANCE_NOTES="missing acceptance reviewer output; counted as FLAG"
  ACCEPTANCE_OUTPUT=""
  ACCEPTANCE_SOURCE=""
  ACCEPTANCE_RATIONALE=""
  ACCEPTANCE_EVIDENCE=""

  if [ -n "${HYPERCORE_ACCEPTANCE_FAKE_DIR:-}" ]; then
    [ "$DRY_RUN" = 1 ] \
      || die "real execute refuses HYPERCORE_ACCEPTANCE_FAKE_DIR; fake acceptance is dry-run/self-test only"
    fake_file="$HYPERCORE_ACCEPTANCE_FAKE_DIR/$reviewer_key"
    if [ ! -f "$fake_file" ]; then
      case "$reviewer_key" in
        tier-one-unit-[0-9][0-9][0-9]-*)
          fake_file="$HYPERCORE_ACCEPTANCE_FAKE_DIR/$(printf '%s' "$reviewer_key" | sed -E 's/-(fast|strong)-[0-9]+$//')"
          ;;
      esac
    fi
    if [ -f "$fake_file" ]; then
      output="$(cat "$fake_file")"
      status=0
    else
      output="missing fake acceptance reviewer output for $reviewer_key"
      status=1
    fi
    acceptance_finalize_result "$output" "$status" "fake/self-test"
    return 0
  fi

  if [ "$DRY_RUN" = 1 ]; then
    output="VERDICT: PASS
RATIONALE: dry-run self-test default acceptance.
EVIDENCE: dry-run mode skipped the real reviewer, and the artifact source marker prevents real archive use."
    status=0
    acceptance_finalize_result "$output" "$status" "dry-run/self-test"
    return 0
  fi

  command -v "$CODEX_BIN" >/dev/null 2>&1 \
    || die "acceptance review cannot spawn Codex reviewers: Codex binary '$CODEX_BIN' is not on PATH"
  timeout_seconds="${HYPERCORE_ACCEPTANCE_TIMEOUT_SECONDS:-600}"
  case "$timeout_seconds" in
    ""|*[!0-9]*) die "HYPERCORE_ACCEPTANCE_TIMEOUT_SECONDS must be a positive integer" ;;
    0) die "HYPERCORE_ACCEPTANCE_TIMEOUT_SECONDS must be greater than zero" ;;
  esac
  command -v timeout >/dev/null 2>&1 \
    || die "acceptance review requires the timeout command so reviewer subprocesses cannot hang indefinitely"
  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-acceptance-$reviewer_key-final.XXXXXX")"
  tmpout="$(mktemp "${TMPDIR:-/tmp}/hypercore-acceptance-$reviewer_key-out.XXXXXX")"
  tmperr="$(mktemp "${TMPDIR:-/tmp}/hypercore-acceptance-$reviewer_key-err.XXXXXX")"
  CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")
  codex_add_review_route_args
  ACCEPTANCE_CMD=("${CODEX_CMD[@]}")
  ACCEPTANCE_CMD+=(exec -o "$final" -)
  set +e
  printf '%s' "$prompt" | timeout --kill-after=5s "$timeout_seconds" "${ACCEPTANCE_CMD[@]}" >"$tmpout" 2>"$tmperr"
  status=$?
  set -e
  if [ -s "$final" ]; then
    output="$(cat "$final")"
  else
    output="$(cat "$tmpout" "$tmperr")"
  fi
  if [ "$status" -eq 124 ] || [ "$status" -eq 137 ]; then
    output="${output:-acceptance reviewer timed out after ${timeout_seconds}s}"
  fi
  acceptance_finalize_result "$output" "$status" "real-reviewer"
  rm -f "$final" "$tmpout" "$tmperr"
}

tier_two_lens_instruction() {
  case "$1" in
    whole-acceptance-conformance)
      printf 'For the whole-acceptance-conformance lens, check the built worktree and phase-two artifacts against the signed acceptance condition, observable acceptance, excluded interpretation, and route.'
      ;;
    proof-integrity)
      printf 'For the proof-integrity lens, check whether the recorded unit handoffs, diffs, mechanical checks, and acceptance artifacts support the proof claims with real-source proof and without dry-run, fake, or stale evidence.'
      ;;
    independent-coherence)
      printf 'For the independent-coherence lens, perform the semantic sweep judgement for one-way adoption; do not claim to solve semantic indexing.'
      ;;
    security-permissions)
      printf 'For the security-permissions lens, check whether the implementation preserves the signed security and permission constraints, including read-only reviewer isolation and operator-gate limits.'
      ;;
    red-team)
      printf 'For the red-team lens, look for bypasses, overclaims, stale artifacts, route mismatch, and ways the work could pass checks while failing the operator-signed acceptance.'
      ;;
    *)
      die "unknown tier-two implementation-acceptance lens: $1"
      ;;
  esac
}

write_acceptance_artifact() {
  local path=$1 title=$2 reviewer_key=$3 verdict=$4 source=$5 rationale=$6 evidence=$7 notes=$8 prompt=$9 output=${10} tmp
  tmp="$path.tmp.$$"
  {
    printf '# %s\n\n' "$title"
    printf 'reviewer: %s\n' "$reviewer_key"
    printf 'Verdict: %s\n' "$verdict"
    printf 'source: %s\n' "$source"
    printf 'source-proof: %s\n' "$(acceptance_source_proof "$source")"
    printf 'Rationale: %s\n' "$rationale"
    printf 'Evidence: %s\n' "$evidence"
    printf 'dry-run: %s\n' "$([ "$DRY_RUN" = 1 ] && printf yes || printf no)"
    printf 'Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.\n'
    printf 'Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.\n'
    printf 'Notes: %s\n\n' "$notes"
    printf '## prompt\n\n'
    printf '%s\n\n' "$prompt"
    printf '## raw output\n\n'
    printf '%s\n' "$output"
  } > "$tmp"
  mv "$tmp" "$path"
}

acceptance_artifact_verdict() {
  local file=$1
  [ -f "$file" ] || return 1
  sed -nE 's/^Verdict:[[:space:]]*(PASS|FLAG)[[:space:]]*$/\1/p' "$file" | sed -n '1p'
}

acceptance_artifact_dry_run() {
  local file=$1
  [ -f "$file" ] || return 1
  grep -Eq '^dry-run:[[:space:]]*yes[[:space:]]*$' "$file"
}

acceptance_artifact_source() {
  local file=$1
  [ -f "$file" ] || return 1
  sed -nE 's/^source:[[:space:]]*(real-reviewer|dry-run\/self-test|fake\/self-test)[[:space:]]*$/\1/p' "$file" | sed -n '1p'
}

acceptance_artifact_field_meaningful() {
  local file=$1 label=$2 value
  [ -f "$file" ] || return 1
  value="$(sed -nE "s/^$label:[[:space:]]*(.*)$/\1/p" "$file" | sed -n '1p')"
  meaningful_text "$value" >/dev/null
}

required_acceptance_artifact_fields_clean() {
  local stage=$1 artifact_desc=$2 file=$3 source
  acceptance_artifact_field_meaningful "$file" Rationale \
    || die "$stage blocked by $artifact_desc without rationale"
  acceptance_artifact_field_meaningful "$file" Evidence \
    || die "$stage blocked by $artifact_desc without evidence"
  acceptance_artifact_field_meaningful "$file" source-proof \
    || die "$stage blocked by $artifact_desc without source proof"
  if [ "$DRY_RUN" != 1 ]; then
    source="$(acceptance_artifact_source "$file" || true)"
    [ "$source" = real-reviewer ] \
      || die "$stage blocked by non-real $artifact_desc acceptance source: ${source:-missing}"
    if acceptance_artifact_dry_run "$file"; then
      die "$stage blocked by dry-run $artifact_desc"
    fi
  fi
}

run_tier_one_acceptance() {
  local work_name=$1 unit_id=$2 proof=$3 frame_rel=$4 handoff_path=$5 diff_path=$6 check_status=$7 attempt_key="${8:-}"
  local verdict_path prompt reviewer_key
  reviewer_key="tier-one-$unit_id"
  [ -n "$attempt_key" ] && reviewer_key="$reviewer_key-$attempt_key"
  verdict_path="$PHASE_TWO_TIER_ONE_DIR/$unit_id.md"
  prompt="Implementation-acceptance reviewer: tier one
Work: $work_name
Node: $NODE_REL
Unit: $unit_id
Proof obligation: $proof
Signed frame directory: $frame_rel
Unit handoff: $(relpath "$handoff_path")
Unit diff record: $(relpath "$diff_path")
Mechanical check immediately before this reviewer: $check_status

Read only the signed frame, the intent it references, the unit handoff, and the unit diff record.
The unit diff record is a cumulative worktree snapshot after this unit, so it may include other already-built or planned unit changes. Check whether the handoff and proof-obligation-relevant diff content make this unit a proof-advancing delta toward the operator-signed acceptance; do not flag solely because unrelated cumulative diff hunks are present.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, or mismatched.

Treat uncertainty, missing evidence, or mismatch with the signed frame as FLAG."
  printf '\n--- acceptance: tier one %s ---\n' "$unit_id"
  LOOP_CURRENT_GATE=check
  loop_event acceptance check running "tier-one implementation acceptance for $unit_id"
  loop_state_write check running "tier-one implementation acceptance for $unit_id"
  run_acceptance_reviewer "$reviewer_key" "$prompt"
  write_acceptance_artifact "$verdict_path" "tier-one implementation acceptance - $unit_id" \
    "$reviewer_key" "$ACCEPTANCE_VERDICT" "$ACCEPTANCE_SOURCE" "$ACCEPTANCE_RATIONALE" "$ACCEPTANCE_EVIDENCE" "$ACCEPTANCE_NOTES" "$prompt" "$ACCEPTANCE_OUTPUT"
  loop_event acceptance check "$([ "$ACCEPTANCE_VERDICT" = PASS ] && printf passed || printf failed)" \
    "tier-one $unit_id verdict: $ACCEPTANCE_VERDICT - $ACCEPTANCE_NOTES"
  loop_state_write check "$([ "$ACCEPTANCE_VERDICT" = PASS ] && printf passed || printf failed)" \
    "tier-one $unit_id verdict: $ACCEPTANCE_VERDICT - $ACCEPTANCE_NOTES"
  printf 'tier-one %s verdict: %s (%s; %s)\n' "$unit_id" "$ACCEPTANCE_VERDICT" "$(relpath "$verdict_path")" "$ACCEPTANCE_NOTES"
  if [ "$ACCEPTANCE_VERDICT" = PASS ]; then
    return 0
  fi
  UNIT_ATTEMPT_REASON="tier-one implementation-acceptance FLAG for $unit_id"
  return 1
}

acceptance_artifact_notes() {
  local file=$1
  [ -f "$file" ] || return 1
  sed -nE 's/^Notes:[[:space:]]*(.*)$/\1/p' "$file" | sed -n '1p'
}

run_tier_two_lens_acceptance() {
  local work_name=$1 frame_rel=$2 active_rel=$3 lens=$4
  local reviewer_key verdict_path prompt lens_instruction
  reviewer_key="panel-$lens"
  verdict_path="$PHASE_TWO_PANEL_DIR/$lens.md"
  lens_instruction="$(tier_two_lens_instruction "$lens")"
  prompt="Implementation-acceptance reviewer: tier two one-way panel
Work: $work_name
Node: $NODE_REL
Lens: $lens
Signed frame directory: $frame_rel
Active work path: $active_rel
Phase-two acceptance directory: $(relpath "$PHASE_TWO_ACCEPTANCE_DIR")

Read only the signed frame, the intent it references, the built worktree state, and phase-two acceptance artifacts.
$lens_instruction
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, unresolved, or mismatched.

Treat uncertainty, missing evidence, unresolved tier-one flags, or mismatch with the signed frame as FLAG."
  PHASE_TWO_RUN_ACTIVE=0
  run_acceptance_reviewer "$reviewer_key" "$prompt"
  write_acceptance_artifact "$verdict_path" "tier-two implementation acceptance - $lens" \
    "$reviewer_key" "$ACCEPTANCE_VERDICT" "$ACCEPTANCE_SOURCE" "$ACCEPTANCE_RATIONALE" "$ACCEPTANCE_EVIDENCE" "$ACCEPTANCE_NOTES" "$prompt" "$ACCEPTANCE_OUTPUT"
}

run_tier_two_panel() {
  local work_name=$1 frame_rel=$2 active_rel=$3 lens reviewer_key verdict_path prompt any_flag=0 verdict
  local pid wait_status notes
  declare -A panel_pids
  printf '\n--- acceptance: tier two one-way panel ---\n'
  LOOP_CURRENT_GATE=check
  printf 'tier-two panel starting %s concurrent lenses\n' "${#TIER_TWO_PANEL_LENSES[@]}"
  loop_event acceptance check running "tier-two panel starting ${#TIER_TWO_PANEL_LENSES[@]} concurrent lenses"
  loop_state_write check running "tier-two panel starting ${#TIER_TWO_PANEL_LENSES[@]} concurrent lenses"
  for lens in "${TIER_TWO_PANEL_LENSES[@]}"; do
    reviewer_key="panel-$lens"
    verdict_path="$PHASE_TWO_PANEL_DIR/$lens.md"
    rm -f "$verdict_path"
    printf 'tier-two %s started concurrently (%s)\n' "$lens" "$(relpath "$verdict_path")"
    loop_event acceptance check running "tier-two implementation acceptance lens $lens started concurrently"
    run_tier_two_lens_acceptance "$work_name" "$frame_rel" "$active_rel" "$lens" &
    panel_pids["$lens"]=$!
  done

  for lens in "${TIER_TWO_PANEL_LENSES[@]}"; do
    reviewer_key="panel-$lens"
    verdict_path="$PHASE_TWO_PANEL_DIR/$lens.md"
    pid="${panel_pids[$lens]}"
    wait_status=0
    wait "$pid" || wait_status=$?
    if [ "$wait_status" -ne 0 ]; then
      prompt="tier-two lens $lens failed before writing a reviewer artifact"
      write_acceptance_artifact "$verdict_path" "tier-two implementation acceptance - $lens" \
        "$reviewer_key" FLAG "unsupported" "" "" \
        "tier-two lens subprocess exited $wait_status; counted as FLAG" "$prompt" ""
    fi
    verdict="$(acceptance_artifact_verdict "$verdict_path" || true)"
    notes="$(acceptance_artifact_notes "$verdict_path" || true)"
    [ -n "$notes" ] || notes="missing acceptance artifact notes; counted as FLAG"
    [ "$verdict" = PASS ] || verdict=FLAG
    loop_event acceptance check "$([ "$verdict" = PASS ] && printf passed || printf failed)" \
      "tier-two $lens verdict: $verdict - $notes"
    loop_state_write check "$([ "$verdict" = PASS ] && printf passed || printf failed)" \
      "tier-two $lens verdict: $verdict - $notes"
    printf 'tier-two %s verdict: %s (%s; %s)\n' "$lens" "$verdict" "$(relpath "$verdict_path")" "$notes"
    [ "$verdict" = PASS ] || any_flag=1
  done
  if [ "$any_flag" = 1 ]; then
    die "tier-two implementation-acceptance panel FLAG — one-way archive is blocked; $work_name stays in flight for the operator"
  fi

  for lens in "${TIER_TWO_PANEL_LENSES[@]}"; do
    verdict_path="$PHASE_TWO_PANEL_DIR/$lens.md"
    verdict="$(acceptance_artifact_verdict "$verdict_path" || true)"
    [ "$verdict" = PASS ] \
      || die "one-way archive blocked by missing or non-PASS tier-two verdict for $lens"
  done
  loop_event acceptance check passed "tier-two panel all lenses clean"
  loop_state_write check passed "tier-two panel all lenses clean"
}

required_tier_one_evidence_clean() {
  local stage=$1 unit_id verdict_path verdict
  shift
  for unit_id in "$@"; do
    verdict_path="$PHASE_TWO_TIER_ONE_DIR/$unit_id.md"
    verdict="$(acceptance_artifact_verdict "$verdict_path" || true)"
    [ "$verdict" = PASS ] \
      || die "$stage blocked by missing or non-PASS tier-one verdict for $unit_id"
    required_acceptance_artifact_fields_clean "$stage" "tier-one verdict for $unit_id" "$verdict_path"
  done
}

required_tier_one_clean_for_panel() {
  required_tier_one_evidence_clean "tier-two panel" "$@"
}

required_acceptance_clean_for_archive() {
  local reversibility=$1 lens verdict_path verdict
  shift
  required_tier_one_evidence_clean "archive" "$@"
  if [ "$reversibility" = one-way ]; then
    for lens in "${TIER_TWO_PANEL_LENSES[@]}"; do
      verdict_path="$PHASE_TWO_PANEL_DIR/$lens.md"
      verdict="$(acceptance_artifact_verdict "$verdict_path" || true)"
      [ "$verdict" = PASS ] \
        || die "one-way archive blocked by missing or non-PASS tier-two verdict for $lens"
      required_acceptance_artifact_fields_clean "one-way archive" "tier-two verdict for $lens" "$verdict_path"
    done
  fi
  return 0
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
  local work_name=$1 state run_id gate status updated message events unit failure acceptance tier_one panel
  state="$(phase_two_state_file_for "$work_name")"
  [ -s "$state" ] || return 0
  run_id="$(json_file_string_value "$state" run_id)"
  gate="$(json_file_string_value "$state" gate)"
  status="$(json_file_string_value "$state" status)"
  unit="$(json_file_string_value "$state" current_unit)"
  updated="$(json_file_string_value "$state" updated_at)"
  message="$(json_file_string_value "$state" message)"
  failure="$(json_file_string_value "$state" failure_reason)"
  events="$(json_file_path_value "$state" events_jsonl)"
  acceptance="$(json_file_path_value "$state" phase_two_acceptance_dir)"
  tier_one="$(json_file_path_value "$state" tier_one_dir)"
  panel="$(json_file_path_value "$state" tier_two_panel_dir)"
  printf 'phase-two run: run_id=%s gate=%s unit=%s status=%s updated_at=%s state=%s events=%s acceptance=%s tier_one=%s tier_two_panel=%s failure=%s message=%s\n' \
    "$run_id" "$gate" "$unit" "$status" "$updated" "$state" "$events" "$acceptance" "$tier_one" "$panel" "$failure" "$message"
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
  if [ "$ph" != done ] && [ -s "$state" ]; then
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

codex_model_token_ok() {
  local value=$1
  [[ "$value" =~ ^[A-Za-z0-9][A-Za-z0-9._:/+-]*$ ]]
}

codex_effort_token_ok() {
  local value=$1
  [[ "$value" =~ ^[A-Za-z0-9][A-Za-z0-9._+-]*$ ]]
}

validate_codex_model_var() {
  local var=$1 value=$2
  [ -z "$value" ] && return 0
  codex_model_token_ok "$value" || die "$var must be a single model token"
}

validate_codex_effort_var() {
  local var=$1 value=$2
  [ -z "$value" ] && return 0
  codex_effort_token_ok "$value" || die "$var must be a single effort token"
}

codex_add_model_and_effort_args() {
  local model=$1 effort=$2 model_var=$3 effort_var=$4
  validate_codex_model_var "$model_var" "$model"
  validate_codex_effort_var "$effort_var" "$effort"
  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
  return 0
}

codex_route_model_and_effort() {
  local route=$1 model="" effort=""
  case "$route" in
    builder-fast)
      model="${CODEX_BUILDER_MODEL:-gpt-5.5}"
      effort="${CODEX_BUILDER_EFFORT:-xhigh}"
      codex_add_model_and_effort_args "$model" "$effort" CODEX_BUILDER_MODEL CODEX_BUILDER_EFFORT
      ;;
    builder-strong)
      model="${CODEX_STRONG_BUILDER_MODEL:-${CODEX_REVIEW_MODEL:-${CODEX_MODEL:-}}}"
      effort="${CODEX_STRONG_BUILDER_EFFORT:-${CODEX_REVIEW_EFFORT:-xhigh}}"
      codex_add_model_and_effort_args "$model" "$effort" CODEX_STRONG_BUILDER_MODEL CODEX_STRONG_BUILDER_EFFORT
      ;;
    default)
      model="${CODEX_MODEL:-}"
      effort="${CODEX_EFFORT:-}"
      codex_add_model_and_effort_args "$model" "$effort" CODEX_MODEL CODEX_EFFORT
      ;;
    *)
      die "unknown Codex route: $route"
      ;;
  esac
}

codex_cmd_prefix() {
  local sandbox="$1" route="${2:-default}"
  CODEX_CMD=("$CODEX_BIN" -a "$CODEX_APPROVAL" -s "$sandbox" -C "$ROOT")
  codex_route_model_and_effort "$route"
  [ -n "${CODEX_PROFILE:-}" ] && CODEX_CMD+=(-p "$CODEX_PROFILE")
  return 0
}

run_codex_gate() {
  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" sys="$6" route="${7:-default}" allow_failure="${8:-0}"
  local sandbox final combined codex_events gate_output cmd_status pipeline_status msg
  local fake_file fake_status_file fake_status_line
  sandbox="$(codex_sandbox_for_tools "$tools")"
  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-loop-codex-$gate-final.XXXXXX")"
  combined="$(printf '%s\n\n---\n\n%s' "$sys" "$prompt")"
  codex_events="$LOOP_RUN_DIR/events-codex-$gate.jsonl"
  gate_output="$LOOP_RUN_GATE_DIR/$gate.final.md"
  codex_cmd_prefix "$sandbox" "$route"

  case "$mode" in
    start)  CODEX_CMD+=(exec --json -o "$final" -) ;;
    *) die "unknown gate mode: $mode" ;;
  esac

  msg="starting $gate gate with Codex sandbox $sandbox"
  loop_event gate-start "$gate" running "$msg"
  loop_state_write "$gate" running "$msg"

  if [ -n "${HYPERCORE_BUILDER_FAKE_DIR:-}" ] && [[ "$route" == builder-* ]]; then
    [ "$DRY_RUN" = 1 ] \
      || die "real execute refuses HYPERCORE_BUILDER_FAKE_DIR; fake builders are dry-run/self-test only"
    fake_file="$HYPERCORE_BUILDER_FAKE_DIR/$gate"
    fake_status_file="$fake_file.status"
    if [ -f "$fake_file" ]; then
      GATE_OUTPUT="$(cat "$fake_file")"
    else
      GATE_OUTPUT="fake builder output for $gate"
    fi
    cmd_status=0
    if [ -f "$fake_status_file" ]; then
      fake_status_line="$(sed -n '1p' "$fake_status_file")"
      case "$fake_status_line" in
        ""|*[!0-9]*) die "fake builder status for $gate must be a non-negative integer" ;;
        *) cmd_status=$fake_status_line ;;
      esac
    fi
    printf '{"type":"fake-builder","gate":%s,"route":%s,"status":%s}\n' \
      "$(json_string "$gate")" "$(json_string "$route")" "$cmd_status" > "$codex_events"
    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
    printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
    PHASE_TWO_SESSION_ID="fake-builder-$gate"
    loop_event codex-thread "$gate" running "fake builder session: $PHASE_TWO_SESSION_ID"
    if [ "$cmd_status" -ne 0 ]; then
      msg="gate $gate failed: fake builder exited $cmd_status"
      loop_event gate-failure "$gate" failed "$msg"
      loop_state_write "$gate" failed "$msg"
      rm -f "$final"
      [ "$allow_failure" = 1 ] && return "$cmd_status"
      die "$msg"
    fi
    loop_event gate-finish "$gate" passed "fake builder stored $gate final message at $gate_output"
    loop_state_write "$gate" passed "fake builder stored $gate final message at $gate_output"
    rm -f "$final"
    printf '%s\n' "$GATE_OUTPUT"
    return 0
  fi

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
    if [ -s "$final" ]; then
      GATE_OUTPUT="$(cat "$final")"
    else
      GATE_OUTPUT="codex exec exited $cmd_status"
      printf '%s\n' "$GATE_OUTPUT" > "$gate_output"
    fi
    msg="gate $gate failed: codex exec exited $cmd_status"
    loop_event gate-failure "$gate" failed "$msg"
    loop_state_write "$gate" failed "$msg"
    rm -f "$final"
    [ "$allow_failure" = 1 ] && return "$cmd_status"
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

# a single fresh phase-two executor session.
# args: <gate-name> <allowed-tools> <mode> <session-id> <prompt> [instruction-gate]
# mode is start; every phase-two builder, acceptance reviewer, and archive actor is fresh.
run_gate() {
  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" instruction_gate="${6:-$1}" route="${7:-default}" allow_failure="${8:-0}" sys
  sys="$(cat "$GATES/$instruction_gate.md")"

  case "$LOOP_HARNESS" in
    codex) run_codex_gate "$gate" "$tools" "$mode" "$sid" "$prompt" "$sys" "$route" "$allow_failure" ;;
    *) die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)" ;;
  esac
}

cmd_start() {
  local work_name="${1:-}" collection d frame address template options_template
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
      printf 'Reversibility: TODO\n\n'
      printf '## route\n\nTODO\n\n'
      printf '## acceptance condition\n\nTODO\n\n'
      printf '## observable acceptance\n\nTODO\n\n'
      printf '## excluded interpretation\n\nTODO\n\n'
      printf '## proof state\n\nTODO\n\n'
      printf '## sweep\n\nTODO\n\n'
      printf '## adoption claim\n\nTODO\n\n'
      printf '## shelving claim\n\nTODO\n'
    } > "$template"
  fi
  options_template="$frame/options.md"
  if [ ! -e "$options_template" ]; then
    {
      printf '# options - %s\n\n' "$work_name"
      printf 'Direction options are drafted by the machine for operator selection. The operator\n'
      printf 'selects one route, rejects all options, or aborts without writing direction.\n\n'
      printf '## option 1\n\n'
      printf 'id: TODO\n'
      printf 'kind: selected-route\n'
      printf 'summary: TODO\n'
      printf 'reversibility: TODO\n'
      printf 'tradeoff: TODO\n\n'
      printf '## option 2\n\n'
      printf 'id: TODO\n'
      printf 'kind: selected-route\n'
      printf 'summary: TODO\n'
      printf 'reversibility: TODO\n'
      printf 'tradeoff: TODO\n\n'
      printf '## rejection choices\n\n'
      printf 'none: The operator may reject all options and send the work back to frame.\n'
      printf 'abort: The operator may abort without writing direction.\n'
    } > "$options_template"
  fi
  printf '\n=== gate: orient ===\n\n'; cat "$GATES/orient.md"
}

direction_work_candidates() {
  local d name
  for d in "$WORKS"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "${d%/}")"
    work_name_ok "$name" || continue
    is_work_node "$d" || continue
    signed_off_at "$d" && continue
    direction_contract_errors_at "$d" >/dev/null 2>&1 && continue
    printf '%s\n' "$name"
  done
}

infer_direction_work_name() {
  local candidates=() name
  while IFS= read -r name; do candidates+=("$name"); done < <(direction_work_candidates)
  case "${#candidates[@]}" in
    1) printf '%s' "${candidates[0]}" ;;
    0) die "cannot infer work name: no unsigned active work node needing direction in node $NODE_REL; pass <work-name>" ;;
    *) die "cannot infer work name: multiple unsigned active work nodes need direction in node $NODE_REL: ${candidates[*]}; pass <work-name>" ;;
  esac
}

read_direction_text() {
  local raw=$1 text
  if [ "$raw" = "-" ]; then
    raw="$(cat)"
  fi
  text="$(meaningful_text "$raw" || true)"
  [ -n "$text" ] || return 1
  printf '%s' "$text"
}

cmd_direct() {
  local positional=() form="" value_arg="" value="" work_name="" who="" d frame file tmp field gate
  while [ $# -gt 0 ]; do
    case "$1" in
      --route|--constraint|--delegate)
        [ -z "$form" ] || die "usage: loop.sh [-C <node-path>] direct [<work-name> [<operator>]] --route|--constraint|--delegate <text-or->"
        form="${1#--}"
        shift
        [ $# -gt 0 ] || die "direction $form requires <text-or->"
        value_arg=$1
        shift
        ;;
      --*) die "unknown direction option: $1" ;;
      *)
        [ -z "$form" ] || die "direction takes no positional arguments after the direction form"
        positional+=("$1")
        shift
        ;;
    esac
  done
  [ "${#positional[@]}" -le 2 ] || die "usage: loop.sh [-C <node-path>] direct [<work-name> [<operator>]] --route|--constraint|--delegate <text-or->"
  case "${#positional[@]}" in
    0) work_name="$(infer_direction_work_name)" ;;
    1) work_name="${positional[0]}" ;;
    2) work_name="${positional[0]}"; who="${positional[1]}" ;;
  esac
  [ -n "$who" ] || who="$(infer_operator)"
  case "$who" in
    *$'\n'*|*$'\r'*) die "operator identity must be a single line" ;;
  esac
  validate_work_name "$work_name"
  d="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  signed_off_at "$d" && die "cannot record direction after sign-off"
  frame="$(frame_dir_for "$d")"
  [ -d "$frame" ] || die "missing frame directory: $(relpath "$frame")"
  file="$frame/direction.md"
  if [ -f "$file" ]; then
    if direction_contract_errors_at "$d" >/dev/null; then
      die "direction already recorded at $(relpath "$file")"
    fi
    die "direction artifact already exists but is malformed at $(relpath "$file"); fix or remove it before recording direction"
  fi
  frame_route_has_content_at "$d" \
    && die "cannot record direction after route content exists in $(relpath "$frame/frame.md"); clear the route and record operator direction before framing it"
  # Explicit --route/--constraint/--delegate text is a legacy/admin form. It must not
  # make a new frame signable when gated operator acts are required: a real operator
  # choice is the numbered options.md selection through /dev/tty, not machine-supplied
  # text the operator merely confirms. Only the narrow gate-introducing bootstrap work
  # may still record direction without that selection.
  if [ -n "$form" ] && ! operator_gate_bootstrap_allowed_at "$d"; then
    die "explicit direction forms cannot record gated operator direction for new work; run $(direction_command_hint "$work_name") with no --route/--constraint/--delegate so the operator selects a numbered option through /dev/tty"
  fi
  if [ -z "$form" ]; then
    DIRECTION_SELECTED_FIELD=""
    DIRECTION_SELECTED_VALUE=""
    DIRECTION_SELECTED_GATE=""
    direction_option_choice_from_tty "$d" "$work_name"
    field="$DIRECTION_SELECTED_FIELD"
    value="$DIRECTION_SELECTED_VALUE"
    gate="$DIRECTION_SELECTED_GATE"
  else
    value="$(read_direction_text "$value_arg" || true)"
    [ -n "$value" ] || die "direction text is empty or placeholder"
    case "$form" in
      route) field=selected-route ;;
      constraint) field=constraint ;;
      delegate) field=delegation ;;
      *) die "unknown direction form: $form" ;;
    esac
    gate="$(operator_gate_confirm_work "direction" "$work_name")"
  fi
  tmp="$file.tmp.$$"
  {
    printf '# direction - %s\n\n' "$work_name"
    printf 'direction-by: %s\n' "$who"
    printf 'direction-given-at: %s\n' "$(utc_stamp)"
    printf 'operator-gate: %s\n' "$gate"
    printf '%s: %s\n' "$field" "$value"
  } > "$tmp"
  mv "$tmp" "$file"
  printf 'recorded operator direction at %s\n' "$(relpath "$file")"
}

valid_optional_review_role() {
  local role=$1 r
  for r in "${OPTIONAL_REVIEW_ROLES[@]}"; do
    [ "$role" = "$r" ] && return 0
  done
  return 1
}

validate_review_model() {
  local model=${CODEX_REVIEW_MODEL:-}
  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
  validate_codex_model_var CODEX_REVIEW_MODEL "$model"
  validate_codex_effort_var CODEX_REVIEW_EFFORT "$effort"
}

codex_add_review_route_args() {
  local model=${CODEX_REVIEW_MODEL:-}
  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
  validate_review_model
  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
  return 0
}

reviewer_verdict_from_output() {
  local output=$1 status=$2
  [ "$status" -eq 0 ] || { printf 'FLAG'; return; }
  if printf '%s\n' "$output" | grep -Eq '^VERDICT:[[:space:]]*PASS[[:space:]]*$'; then
    printf 'PASS'
  elif printf '%s\n' "$output" | grep -Eq '^VERDICT:[[:space:]]*FLAG[[:space:]]*$'; then
    printf 'FLAG'
  else
    printf 'FLAG'
  fi
}

reviewer_note_from_output() {
  local output=$1 status=$2 note diag
  if [ "$status" -ne 0 ]; then
    note="reviewer subprocess exited $status; counted as FLAG"
    diag="$(printf '%s\n' "$output" | sed -n '/[^[:space:]]/{s/^[[:space:]]*//;p;q;}')"
    [ -n "$diag" ] && note="$note; diagnostic: $diag"
  elif printf '%s\n' "$output" | grep -Eq '^VERDICT:[[:space:]]*(PASS|FLAG)[[:space:]]*$'; then
    note="$(printf '%s\n' "$output" | sed -nE 's/^NOTE:[[:space:]]*(.*)$/\1/p' | sed -n '1p')"
    [ -n "$note" ] || note="structured verdict returned"
  else
    note="missing or malformed PASS/FLAG verdict; counted as FLAG"
  fi
  short_message "$note"
}

write_indented_diagnostic_block() {
  local title=$1 content=$2
  printf '#### %s\n\n' "$title"
  if [ -n "$content" ]; then
    printf '%s\n' "$content" | sed 's/^/    /'
  else
    printf '    (none)\n'
  fi
  printf '\n'
}

run_reviewer_role() {
  local role=$1 work_name=$2 frame_rel=$3 output status final tmpout tmperr prompt fake_file fake_status_file status_line
  local stdout_output stderr_output final_output output_source
  REVIEWER_VERDICT=FLAG
  REVIEWER_NOTES="missing reviewer output; counted as FLAG"
  REVIEWER_STATUS=1
  REVIEWER_OUTPUT=""
  REVIEWER_STDOUT=""
  REVIEWER_STDERR=""
  REVIEWER_FINAL_OUTPUT=""
  REVIEWER_OUTPUT_SOURCE=none

  if [ -n "${HYPERCORE_REVIEW_FAKE_DIR:-}" ]; then
    fake_file="$HYPERCORE_REVIEW_FAKE_DIR/$role"
    fake_status_file="$fake_file.status"
    if [ -f "$fake_file" ]; then
      output="$(cat "$fake_file")"
      status=0
    else
      output="missing fake reviewer output for $role"
      status=1
    fi
    if [ -f "$fake_status_file" ]; then
      status_line="$(sed -n '1p' "$fake_status_file")"
      case "$status_line" in
        ""|*[!0-9]*) die "fake reviewer status for $role must be a non-negative integer" ;;
        *) status=$status_line ;;
      esac
    fi
    REVIEWER_STATUS="$status"
    REVIEWER_OUTPUT="$output"
    REVIEWER_FINAL_OUTPUT="$output"
    REVIEWER_OUTPUT_SOURCE=fake-output
    REVIEWER_VERDICT="$(reviewer_verdict_from_output "$output" "$status")"
    REVIEWER_NOTES="$(reviewer_note_from_output "$output" "$status")"
    return 0
  fi

  command -v "$CODEX_BIN" >/dev/null 2>&1 \
    || die "review cannot spawn Codex reviewers: Codex binary '$CODEX_BIN' is not on PATH"
  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-review-$role-final.XXXXXX")"
  tmpout="$(mktemp "${TMPDIR:-/tmp}/hypercore-review-$role-out.XXXXXX")"
  tmperr="$(mktemp "${TMPDIR:-/tmp}/hypercore-review-$role-err.XXXXXX")"
  prompt="Review role: $role
Work: $work_name
Frame directory: $frame_rel

Read only the signed work frame and the intent it references. Do not debate other reviewers.
Return exactly one structured verdict line:
VERDICT: PASS
or
VERDICT: FLAG

Then optionally add one NOTE: line. Treat uncertainty as FLAG."
  CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")
  codex_add_review_route_args
  REVIEW_CMD=("${CODEX_CMD[@]}")
  REVIEW_CMD+=(exec -o "$final" -)
  set +e
  printf '%s' "$prompt" | "${REVIEW_CMD[@]}" >"$tmpout" 2>"$tmperr"
  status=$?
  set -e
  stdout_output="$(cat "$tmpout")"
  stderr_output="$(cat "$tmperr")"
  final_output=""
  if [ -s "$final" ]; then
    final_output="$(cat "$final")"
    output="$final_output"
    output_source=final-output
  elif [ -n "$stdout_output" ] && [ -n "$stderr_output" ]; then
    output="$(printf '%s\n%s' "$stdout_output" "$stderr_output")"
    output_source=stdout-stderr
  elif [ -n "$stdout_output" ]; then
    output="$stdout_output"
    output_source=stdout
  else
    output="$stderr_output"
    output_source=stderr
  fi
  REVIEWER_STATUS="$status"
  REVIEWER_OUTPUT="$output"
  REVIEWER_STDOUT="$stdout_output"
  REVIEWER_STDERR="$stderr_output"
  REVIEWER_FINAL_OUTPUT="$final_output"
  REVIEWER_OUTPUT_SOURCE="$output_source"
  REVIEWER_VERDICT="$(reviewer_verdict_from_output "$output" "$status")"
  REVIEWER_NOTES="$(reviewer_note_from_output "$output" "$status")"
  rm -f "$final" "$tmpout" "$tmperr"
}

cmd_review() {
  local work_name="${1:-}" d frame frame_rel reversibility role add_role tmp overall disposition
  local roles=() optional_roles=() required_flag=0 advisory_flag=0 role_type
  declare -A verdicts
  declare -A notes
  declare -A statuses
  declare -A outputs
  declare -A stdout_outputs
  declare -A stderr_outputs
  declare -A final_outputs
  declare -A output_sources
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] review <work-name> [--add <role>]..."
  validate_work_name "$work_name"
  shift
  while [ $# -gt 0 ]; do
    case "$1" in
      --add)
        shift
        [ $# -gt 0 ] || die "review --add requires a role"
        add_role=$1
        valid_optional_review_role "$add_role" \
          || die "invalid optional review role: $add_role"
        optional_roles+=("$add_role")
        shift
        ;;
      *) die "usage: loop.sh [-C <node-path>] review <work-name> [--add <role>]..." ;;
    esac
  done
  d="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  frame="$(frame_dir_for "$d")"
  [ -f "$frame/frame.md" ] || die "review requires canonical frame file: $(relpath "$frame/frame.md")"
  reversibility="$(frame_reversibility_value_at "$d" || true)"
  [ -n "$reversibility" ] || die 'review requires exact "Reversibility: one-way" or "Reversibility: two-way" in intent/frame/frame.md'
  roles=("${BASE_REVIEW_ROLES[@]}" "${optional_roles[@]}")
  frame_rel="$(relpath "$frame")"
  for role in "${roles[@]}"; do
    run_reviewer_role "$role" "$work_name" "$frame_rel"
    verdicts["$role"]="$REVIEWER_VERDICT"
    notes["$role"]="$REVIEWER_NOTES"
    statuses["$role"]="$REVIEWER_STATUS"
    outputs["$role"]="$REVIEWER_OUTPUT"
    stdout_outputs["$role"]="$REVIEWER_STDOUT"
    stderr_outputs["$role"]="$REVIEWER_STDERR"
    final_outputs["$role"]="$REVIEWER_FINAL_OUTPUT"
    output_sources["$role"]="$REVIEWER_OUTPUT_SOURCE"
    if [ "$REVIEWER_VERDICT" = FLAG ]; then
      if valid_optional_review_role "$role"; then
        advisory_flag=1
      else
        required_flag=1
      fi
    fi
  done
  if [ "$required_flag" = 1 ]; then
    overall=FLAG
    disposition="escalated - FLAG verdicts must be answered in the frame; optional reviewers are advisory only and cannot clear base-roster or red-team flags"
  else
    overall=PASS
    disposition="resolved - base roster returned PASS; optional reviewers remain advisory"
  fi
  tmp="$frame/review.md.tmp.$$"
  {
    printf '# review - %s\n\n' "$work_name"
    printf 'Overall: %s\n' "$overall"
    printf 'Isolation: reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.\n'
    printf 'Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.\n'
    printf 'Disposition: %s\n\n' "$disposition"
    printf '## base roster verdicts\n\n'
    for role in "${BASE_REVIEW_ROLES[@]}"; do
      printf -- '- %s: %s\n' "$role" "${verdicts[$role]}"
    done
    if [ "${#optional_roles[@]}" -gt 0 ]; then
      printf '\n## advisory optional verdicts\n\n'
      for role in "${optional_roles[@]}"; do
        printf -- '- %s: %s\n' "$role" "${verdicts[$role]}"
      done
    fi
    printf '\n## unresolved flags\n\n'
    if [ "$required_flag" = 1 ]; then
      for role in "${roles[@]}"; do
        [ "${verdicts[$role]}" = FLAG ] || continue
        role_type=base
        valid_optional_review_role "$role" && role_type=advisory
        [ "$role_type" = base ] || continue
        printf -- '- %s (%s): %s\n' "$role" "$role_type" "${notes[$role]}"
      done
    else
      printf 'None.\n'
    fi
    if [ "${#optional_roles[@]}" -gt 0 ]; then
      printf '\n## advisory optional flags\n\n'
      if [ "$advisory_flag" = 1 ]; then
        for role in "${optional_roles[@]}"; do
          [ "${verdicts[$role]}" = FLAG ] || continue
          printf -- '- %s (advisory): %s\n' "$role" "${notes[$role]}"
        done
      else
        printf 'None.\n'
      fi
    fi
    printf '\n## reviewer notes\n\n'
    for role in "${roles[@]}"; do
      printf '### %s\n\n%s\n\n' "$role" "${notes[$role]}"
    done
    printf '## reviewer diagnostics\n\n'
    for role in "${roles[@]}"; do
      printf '### %s\n\n' "$role"
      printf 'status: %s\n' "${statuses[$role]}"
      printf 'selected-output-source: %s\n\n' "${output_sources[$role]}"
      write_indented_diagnostic_block "selected output" "${outputs[$role]}"
      write_indented_diagnostic_block "final output" "${final_outputs[$role]}"
      write_indented_diagnostic_block "stdout" "${stdout_outputs[$role]}"
      write_indented_diagnostic_block "stderr" "${stderr_outputs[$role]}"
    done
  } > "$tmp"
  mv "$tmp" "$frame/review.md"
  printf 'wrote review artifact at %s\n' "$(relpath "$frame/review.md")"
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
  local work_name="${1:-}" who="${2:-}" d frame errors gate signed_at
  [ -z "${3:-}" ] || die "usage: loop.sh [-C <node-path>] signoff [<work-name> [<operator>]]"
  [ -n "$work_name" ] || work_name="$(infer_signoff_work_name)"
  [ -n "$who" ] || who="$(infer_operator)"
  validate_work_name "$work_name"
  d="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  if ! frame_complete_at "$d"; then
    errors="$(frame_contract_errors_at "$d" || true)"
    die "cannot sign off: work-node frame is incomplete under $(relpath "$(frame_dir_for "$d")"):
$errors"
  fi
  frame="$(frame_dir_for "$d")"
  if [ -f "$frame/signoff.md" ]; then
    if signoff_contract_errors_at "$d" >/dev/null; then
      die "already signed off"
    fi
    die "sign-off artifact already exists but is malformed at $(relpath "$frame/signoff.md"); fix or remove it before signing off"
  fi
  gate="$(operator_gate_confirm_signoff "$d" "$work_name" "$who")"
  check_green || die "check.sh is red — not signable"
  signed_at="$(utc_stamp)"
  printf '# signoff - %s\n\nsigned-off-by: %s\nsigned-off-at: %s\noperator-gate: %s\n' "$work_name" "$who" "$signed_at" "$gate" > "$frame/signoff.md"
  printf 'signed off by %s. The session now clears; phase two re-derives from the frame:\n' "$who"
  printf '  loop.sh'
  [ "$NODE_REL" = "." ] || printf ' -C %s' "$NODE_REL"
  printf ' execute %s\n' "$work_name"
}

fake_check_status_for_attempt() {
  local key=$1 status_file status_line
  [ -n "${HYPERCORE_CHECK_FAKE_DIR:-}" ] || return 0
  [ "$DRY_RUN" = 1 ] \
    || die "real execute refuses HYPERCORE_CHECK_FAKE_DIR; fake checks are dry-run/self-test only"
  status_file="$HYPERCORE_CHECK_FAKE_DIR/$key.status"
  [ -f "$status_file" ] || return 0
  status_line="$(sed -n '1p' "$status_file")"
  case "$status_line" in
    ""|*[!0-9]*) die "fake check status for $key must be a non-negative integer" ;;
  esac
  return "$status_line"
}

run_unit_mechanical_check() {
  local unit_id=$1 attempt_key=$2 status_msg
  UNIT_CHECK_STATUS_MSG=""
  printf '\n--- gate: check (mechanical after %s, %s) ---\n' "$unit_id" "$attempt_key"
  loop_event check check running "running ./check.sh after $unit_id ($attempt_key)"
  loop_state_write check running "running ./check.sh after $unit_id ($attempt_key)"
  if [ "$DRY_RUN" = 1 ]; then
    if [ -n "${HYPERCORE_CHECK_FAKE_DIR:-}" ]; then
      if fake_check_status_for_attempt "$unit_id-$attempt_key"; then
        printf '(dry-run fake) check.sh green after %s (%s)\n' "$unit_id" "$attempt_key"
        loop_event check check passed "dry-run fake check.sh green after $unit_id ($attempt_key)"
        loop_state_write check passed "dry-run fake check.sh green after $unit_id ($attempt_key)"
        status_msg="dry-run fake mechanical check green"
      else
        UNIT_ATTEMPT_REASON="check.sh red after $unit_id ($attempt_key)"
        phase_two_write_unit_record "$unit_id" failed "$proof" "$handoff_path" "$diff_path" "$tier_one_path" "$UNIT_ATTEMPT_REASON"
        loop_event check check failed "dry-run fake check.sh red after $unit_id ($attempt_key)"
        loop_state_write check failed "dry-run fake check.sh red after $unit_id ($attempt_key)"
        return 1
      fi
    else
      printf '(dry-run) would run: ./check.sh after %s (%s)\n' "$unit_id" "$attempt_key"
      loop_event check check skipped "dry-run skipped ./check.sh after $unit_id ($attempt_key)"
      loop_state_write check skipped "dry-run skipped ./check.sh after $unit_id ($attempt_key)"
      status_msg="dry-run mechanical check skipped"
    fi
  elif check_green; then
    printf 'check.sh green after %s (%s)\n' "$unit_id" "$attempt_key"
    loop_event check check passed "check.sh green after $unit_id ($attempt_key)"
    loop_state_write check passed "check.sh green after $unit_id ($attempt_key)"
    status_msg="check.sh green"
  else
    UNIT_ATTEMPT_REASON="check.sh red after $unit_id ($attempt_key)"
    phase_two_write_unit_record "$unit_id" failed "$proof" "$handoff_path" "$diff_path" "$tier_one_path" "$UNIT_ATTEMPT_REASON"
    loop_event check check failed "$UNIT_ATTEMPT_REASON"
    loop_state_write check failed "$UNIT_ATTEMPT_REASON"
    return 1
  fi
  UNIT_CHECK_STATUS_MSG="$status_msg"
  return 0
}

run_unit_build_attempt() {
  local work_name=$1 unit_id=$2 proof=$3 source_desc=$4 attempt_kind=$5 attempt_number=$6
  local handoff_path=$7 diff_path=$8 tier_one_path=$9
  local attempt_key gate_name gate_output_path route status_msg
  UNIT_ATTEMPT_REASON=""
  UNIT_ACCEPTED_STATUS_MSG=""
  attempt_key="$attempt_kind-$attempt_number"
  gate_name="implement-$unit_id-$attempt_key"
  route="builder-$attempt_kind"
  phase_two_write_unit_record "$unit_id" running "$proof" "$handoff_path" "$diff_path" "$tier_one_path" "$attempt_key builder session starting"

  printf '\n--- gate: implement %s (%s builder attempt %s) ---\n' "$unit_id" "$attempt_kind" "$attempt_number"
  PHASE_TWO_SESSION_ID=""
  if ! run_gate "$gate_name" "Read Edit Write Bash" start "" \
    "Implement phase-two unit $unit_id for node-local work $work_name in addressed node $NODE_REL.
Proof obligation: $proof
Signed frame: $source_desc" \
    implement "$route" 1; then
    UNIT_ATTEMPT_REASON="$attempt_kind builder subprocess failed for $unit_id on attempt $attempt_number"
    phase_two_write_unit_record "$unit_id" failed "$proof" "$handoff_path" "$diff_path" "$tier_one_path" "$UNIT_ATTEMPT_REASON"
    return 1
  fi

  gate_output_path="$LOOP_RUN_GATE_DIR/$gate_name.final.md"
  phase_two_write_handoff "$unit_id" "$proof" "$gate_output_path" "$handoff_path"
  write_current_diff_record "$diff_path"

  if ! run_unit_mechanical_check "$unit_id" "$attempt_key"; then
    return 1
  fi
  status_msg="$UNIT_CHECK_STATUS_MSG"

  if run_tier_one_acceptance "$work_name" "$unit_id" "$proof" "$frame_rel" "$handoff_path" "$diff_path" "$status_msg" "$attempt_key"; then
    UNIT_ACCEPTED_STATUS_MSG="$status_msg; tier-one PASS; $attempt_kind builder attempt $attempt_number"
    return 0
  fi
  return 1
}

cmd_execute() {
  local work_name="" active_dir active_rel frame_rel frame_file source_desc archive_collection archive_decision
  local reversibility errors units_text unit_entry unit_id proof gate_name handoff_path diff_path tier_one_path
  local gate_output_path status_msg fast_attempt unit_accepted units=() unit_ids=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --dry-run)
        [ "$DRY_RUN" = 0 ] || die "usage: loop.sh [-C <node-path>] execute [<work-name>] [--dry-run]"
        DRY_RUN=1
        ;;
      --*)
        die "usage: loop.sh [-C <node-path>] execute [<work-name>] [--dry-run]"
        ;;
      *)
        [ -z "$work_name" ] || die "usage: loop.sh [-C <node-path>] execute [<work-name>] [--dry-run]"
        work_name="$1"
        ;;
    esac
    shift
  done
  [ -n "$work_name" ] || work_name="$(infer_execute_work_name)"
  validate_work_name "$work_name"
  active_dir="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  active_rel="$(relpath "$active_dir")"
  frame_rel="$(relpath "$(frame_dir_for "$active_dir")")"
  frame_file="$(frame_dir_for "$active_dir")/frame.md"
  if ! signed_off_at "$active_dir"; then
    errors="$(signoff_contract_errors_at "$active_dir" || true)"
    die "not signed off — phase two is sealed until the operator signs off:
$errors"
  fi
  if ! frame_complete_at "$active_dir"; then
    errors="$(frame_contract_errors_at "$active_dir" || true)"
    die "signed frame is incomplete under $frame_rel:
$errors"
  fi
  reversibility="$(frame_reversibility_value_at "$active_dir")"
  units_text="$(phase_two_units_from_frame_file "$frame_file" || true)"
  [ -n "$units_text" ] \
    || die "signed frame does not name implementation units for phase two; cannot re-derive unit boundaries without inventing"
  mapfile -t units <<< "$units_text"
  source_desc="$frame_rel/ (the signed work-node frame)"
  if [ "$DRY_RUN" != 1 ] && [ -n "${HYPERCORE_ACCEPTANCE_FAKE_DIR:-}" ]; then
    die "real execute refuses HYPERCORE_ACCEPTANCE_FAKE_DIR; fake acceptance is dry-run/self-test only"
  fi
  if [ "$DRY_RUN" != 1 ] && [ -n "${HYPERCORE_BUILDER_FAKE_DIR:-}" ]; then
    die "real execute refuses HYPERCORE_BUILDER_FAKE_DIR; fake builders are dry-run/self-test only"
  fi
  if [ "$DRY_RUN" != 1 ] && [ -n "${HYPERCORE_CHECK_FAKE_DIR:-}" ]; then
    die "real execute refuses HYPERCORE_CHECK_FAKE_DIR; fake checks are dry-run/self-test only"
  fi

  [ "$LOOP_HARNESS" = codex ] \
    || die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)"
  printf '=== phase two: %s cleared per-unit sessions, re-deriving %s in node %s from its frame ===\n' \
    "$LOOP_HARNESS" "$work_name" "$NODE_REL"
  phase_two_run_init "$work_name"
  if ! phase_two_preflight "$work_name"; then
    PHASE_TWO_RUN_ACTIVE=0
    exit 1
  fi

  for unit_entry in "${units[@]}"; do
    unit_id="${unit_entry%%$'\t'*}"
    proof="${unit_entry#*$'\t'}"
    [ -n "$unit_id" ] && [ "$unit_id" != "$proof" ] \
      || die "malformed implementation unit record parsed from signed frame"
    unit_ids+=("$unit_id")
    LOOP_CURRENT_UNIT="$unit_id"
    gate_name="implement-$unit_id"
    handoff_path="$PHASE_TWO_HANDOFF_DIR/$unit_id.md"
    diff_path="$PHASE_TWO_DIFF_DIR/$unit_id.diff"
    tier_one_path="$PHASE_TWO_TIER_ONE_DIR/$unit_id.md"

    if phase_two_unit_tier_one_resumable "$tier_one_path"; then
      printf 'resume: skipping %s (tier-one PASS already on disk for this frame)\n' "$unit_id"
      loop_event resume check skipped "resume: skipping $unit_id (tier-one PASS already on disk)"
      loop_state_write check skipped "resume: skipping $unit_id"
      phase_two_write_unit_record "$unit_id" accepted "$proof" "$handoff_path" "$diff_path" "$tier_one_path" \
        "resume: reused tier-one PASS already on disk for this frame"
      continue
    fi
    printf 'building %s (no reusable tier-one PASS on disk)\n' "$unit_id"
    rm -f "$handoff_path" "$diff_path" "$tier_one_path"
    phase_two_write_unit_record "$unit_id" running "$proof" "$handoff_path" "$diff_path" "$tier_one_path" "builder session starting"

    unit_accepted=0
    for fast_attempt in 1 2 3; do
      if run_unit_build_attempt "$work_name" "$unit_id" "$proof" "$source_desc" fast "$fast_attempt" "$handoff_path" "$diff_path" "$tier_one_path"; then
        unit_accepted=1
        status_msg="$UNIT_ACCEPTED_STATUS_MSG"
        printf 'fast builder attempt %s for %s accepted\n' "$fast_attempt" "$unit_id"
        break
      fi
      printf 'fast builder attempt %s for %s failed: %s\n' "$fast_attempt" "$unit_id" "$(short_message "$UNIT_ATTEMPT_REASON")"
      loop_event builder check failed "fast builder attempt $fast_attempt for $unit_id failed: $UNIT_ATTEMPT_REASON"
      loop_state_write check failed "fast builder attempt $fast_attempt for $unit_id failed: $UNIT_ATTEMPT_REASON"
    done

    if [ "$unit_accepted" != 1 ]; then
      printf 'escalating %s to strong builder after 3 failed fast attempts\n' "$unit_id"
      loop_event builder check running "escalating $unit_id to strong builder after 3 failed fast attempts"
      loop_state_write check running "escalating $unit_id to strong builder after 3 failed fast attempts"
      if run_unit_build_attempt "$work_name" "$unit_id" "$proof" "$source_desc" strong 1 "$handoff_path" "$diff_path" "$tier_one_path"; then
        unit_accepted=1
        status_msg="$UNIT_ACCEPTED_STATUS_MSG"
        printf 'strong builder attempt 1 for %s accepted\n' "$unit_id"
      else
        phase_two_write_unit_record "$unit_id" failed "$proof" "$handoff_path" "$diff_path" "$tier_one_path" "$UNIT_ATTEMPT_REASON"
        die "strong-builder attempt failed for $unit_id; phase two stops for the operator and $work_name stays in flight: $UNIT_ATTEMPT_REASON"
      fi
    fi

    phase_two_write_unit_record "$unit_id" accepted "$proof" "$handoff_path" "$diff_path" "$tier_one_path" "$status_msg; tier-one PASS"
  done

  LOOP_CURRENT_UNIT=""
  printf '\n--- gate: check (pre-archive acceptance) ---\n'
  loop_event check check running "running ./check.sh before archive acceptance"
  loop_state_write check running "running ./check.sh before archive acceptance"
  if [ "$DRY_RUN" = 1 ]; then
    printf '(dry-run) would run: ./check.sh before archive acceptance\n'
    loop_event check check skipped "dry-run skipped ./check.sh before archive acceptance"
    loop_state_write check skipped "dry-run skipped ./check.sh before archive acceptance"
  else
    if check_green; then
      printf 'check.sh green before archive acceptance\n'
      loop_event check check passed "check.sh green before archive acceptance"
      loop_state_write check passed "check.sh green before archive acceptance"
    else
      loop_event check check failed "check.sh red before archive acceptance"
      die "check.sh red before archive acceptance — drift, stopping"
    fi
  fi

  if [ "$reversibility" = one-way ]; then
    required_tier_one_clean_for_panel "${unit_ids[@]}"
    run_tier_two_panel "$work_name" "$frame_rel" "$active_rel"
  else
    printf 'two-way work: one-way tier-two panel skipped after tier-one acceptance\n'
    loop_event acceptance check skipped "two-way work skips one-way tier-two panel"
    loop_state_write check skipped "two-way work skips one-way tier-two panel"
  fi
  required_acceptance_clean_for_archive "$reversibility" "${unit_ids[@]}"

  PHASE_TWO_SESSION_ID=""
  run_gate archive "Read Edit Write" start "" \
    "Archive node-local work $work_name in addressed node $NODE_REL from $active_rel.
Signed frame: $frame_rel/
Clean phase-two acceptance artifacts: $(relpath "$PHASE_TWO_ACCEPTANCE_DIR").
Decision line: ARCHIVE_DECISION: ADOPTED or ARCHIVE_DECISION: SHELVED."
  printf '\n--- gate: adoption history (move) ---\n'
  if [ "$DRY_RUN" = 1 ]; then
    archive_collection="$(archive_collection_for_active_dir "$active_dir" adopted)"
    printf '(dry-run) would: check.sh green, then git mv %s %s/\n' \
      "$active_rel" "$(relpath "$archive_collection")"
    loop_event archive archive skipped "dry-run would record $work_name in adopted history"
    loop_state_write archive skipped "dry-run would record $work_name in adopted history"
  else
    loop_event check archive running "running ./check.sh after archive decision"
    loop_state_write archive running "running ./check.sh after archive decision"
    if check_green; then
      loop_event check archive passed "check.sh green after archive decision"
    else
      loop_event check archive failed "check.sh red after archive decision — stopping before history move"
      die "check.sh red after archive decision — stopping before history move"
    fi
    archive_decision="$(archive_decision_from_output)"
    loop_event archive-decision archive passed "archive decision: $archive_decision"
    loop_state_write archive passed "archive decision: $archive_decision"
    archive_collection="$(archive_collection_for_active_dir "$active_dir" "$archive_decision")"
    archive_move "$active_dir" "$archive_collection"
    loop_event check archive running "running ./check.sh after history move"
    loop_state_write archive running "running ./check.sh after history move"
    if check_green; then
      loop_event check archive passed "check.sh green after history move"
      loop_state_write archive passed "check.sh green after history move"
    else
      loop_event check archive failed "check.sh red after history move"
      die "check.sh red after history move — history recording is not proved"
    fi
    printf 'recorded %s in %s history for node %s\n' "$work_name" "$archive_decision" "$NODE_REL"
  fi
  loop_event completion archive complete "phase two complete for $work_name"
  loop_state_write archive complete "phase two complete for $work_name"
  PHASE_TWO_RUN_ACTIVE=0
}

cmd_status() {
  local json=0 work_name d errors ph
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
  ph="$(phase "$work_name")"
  printf '%s in node %s: phase=%s frame_complete=%s signed_off=%s\n' "$work_name" "$NODE_REL" "$ph" \
    "$(frame_complete "$work_name" && echo yes || echo no)" \
    "$(signed_off "$work_name" && echo yes || echo no)"
  [ "$ph" = done ] && return
  if d="$(active_work_dir "$work_name")"; then
    if ! frame_complete_at "$d"; then
      errors="$(frame_contract_errors_at "$d" || true)"
      printf 'frame blockers under %s:\n%s' "$(relpath "$(frame_dir_for "$d")")" "$errors"
    elif ! signed_off_at "$d"; then
      printf 'next: '
      if [ "$NODE_REL" = "." ]; then
        printf './signoff\n'
      else
        printf '%s signoff %s <operator>\n' "$(loop_cmd_prefix)" "$work_name"
      fi
    fi
  fi
  print_phase_two_status "$work_name"
}

main() {
  while [ "${1:-}" = "-C" ]; do
    shift
    set_node "${1:-}"
    shift
  done

  local sub="${1:-}"; shift || true
  phase_two_reexec_from_snapshot "$sub" "$@"
  case "$sub" in
    start)   cmd_start   "$@";;
    direct)  cmd_direct  "$@";;
    review)  cmd_review  "$@";;
    frame)   cmd_frame   "$@";;
    signoff) cmd_signoff "$@";;
    execute) cmd_execute "$@";;
    status)  cmd_status  "$@";;
    *) die "usage: loop.sh [-C <node-path>] {start|direct|review|frame|signoff|execute|status} <work-name> [...]";;
  esac
}
main "$@"
