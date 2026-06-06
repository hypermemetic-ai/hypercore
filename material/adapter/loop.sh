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
#   loop.sh [-C <node-path>] status   <work-name>              print the work node's current phase
#
# Env:
#   LOOP_HARNESS=codex (default and only supported phase-two harness)
#   HYPERCORE_OPERATOR (optional sign-off identity when <operator> is omitted)
#   CODEX_BIN (default: codex), CODEX_APPROVAL (default: never)
#   CODEX_WRITE_SANDBOX (default: workspace-write), CODEX_READ_SANDBOX (default: read-only)

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
GATES="$HERE/gates"
NODE="$ROOT"
NODE_REL="."
INTENT_TREE=intent
MATERIAL_TREE=material
WORKS="$NODE/$MATERIAL_TREE"
LEGACY_CHANGES="$NODE/$INTENT_TREE/changes"
LOOP_HARNESS="${LOOP_HARNESS:-codex}"
CODEX_BIN="${CODEX_BIN:-codex}"
CODEX_APPROVAL="${CODEX_APPROVAL:-never}"
CODEX_WRITE_SANDBOX="${CODEX_WRITE_SANDBOX:-workspace-write}"
CODEX_READ_SANDBOX="${CODEX_READ_SANDBOX:-read-only}"
DRY_RUN="${DRY_RUN:-0}"
LEGACY_FRAME_FILES=(delta.md why.md proof.md endorsement.md plan.md)
GATE_OUTPUT=""   # the last gate's captured output, read by cmd_execute for the sweep verdict
PHASE_TWO_SESSION_ID=""

die() { printf 'loop: %s\n' "$1" >&2; exit 1; }

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

is_legacy_change_dir() {
  local d=${1%/}
  case "$d" in
    "$LEGACY_CHANGES"/*) [ "$(basename "$d")" != archive ] ;;
    *) return 1 ;;
  esac
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
  [ -d "$ROOT/$node_path/$MATERIAL_TREE" ] \
    || die "node has no $MATERIAL_TREE/: $node_path"

  NODE="$(cd "$ROOT/$node_path" && pwd)"
  case "$NODE" in
    "$ROOT"|"$ROOT"/*) ;;
    *) die "node path escapes repository: $node_path" ;;
  esac
  NODE_REL="$(relpath "$NODE")"
  WORKS="$NODE/$MATERIAL_TREE"
  LEGACY_CHANGES="$NODE/$INTENT_TREE/changes"
}

is_work_node() {
  local d=${1%/}
  [ -d "$d/$INTENT_TREE" ] && [ -d "$d/$MATERIAL_TREE" ]
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
  d=$LEGACY_CHANGES/$name
  [ -d "$d" ] && printf '%s' "$d"
}

archived_work_dir() {
  local name=$1 d
  validate_work_name "$name"
  for d in \
    "$NODE/$INTENT_TREE/history/adopted/$name" \
    "$NODE/$INTENT_TREE/history/shelved/$name" \
    "$NODE/$INTENT_TREE/history/change-folders/archive/$name" \
    "$LEGACY_CHANGES/archive/$name"
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
  mkdir -p "$WORKS"
  ensure_work_history
  printf '%s' "$WORKS"
}

archive_collection_for_active_dir() {
  local d=${1%/} decision=${2:-adopted} collection
  ensure_work_history
  if is_legacy_change_dir "$d"; then
    collection="$NODE/$INTENT_TREE/history/change-folders/archive"
  elif [ "$decision" = shelved ]; then
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

frame_complete_at() {
  local d=$1 frame f
  [ -d "$d" ] || return 1
  frame="$(frame_dir_for "$d")"
  if is_legacy_change_dir "$d"; then
    for f in "${LEGACY_FRAME_FILES[@]}"; do [ -s "$frame/$f" ] || return 1; done
    return 0
  fi
  [ -d "$frame" ] || return 1
  [ -n "$(find "$frame" -type f ! -name signoff.md -size +0c -print -quit 2>/dev/null)" ]
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
  if is_legacy_change_dir "$d"; then
    [ -f "$frame/endorsement.md" ] && grep -q '^signed-off-by:' "$frame/endorsement.md"
  else
    [ -f "$frame/signoff.md" ] && grep -q '^signed-off-by:' "$frame/signoff.md"
  fi
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

check_green() { ( cd "$ROOT" && ./material/check.sh >/dev/null 2>&1 ); }

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

codex_cmd_prefix() {
  local sandbox="$1"
  CODEX_CMD=("$CODEX_BIN" -a "$CODEX_APPROVAL" -s "$sandbox" -C "$ROOT")
  [ -n "${CODEX_MODEL:-}" ] && CODEX_CMD+=(-m "$CODEX_MODEL")
  [ -n "${CODEX_PROFILE:-}" ] && CODEX_CMD+=(-p "$CODEX_PROFILE")
  return 0
}

run_codex_gate() {
  local gate="$1" tools="$2" mode="$3" sid="$4" prompt="$5" sys="$6" sandbox final events combined
  sandbox="$(codex_sandbox_for_tools "$tools")"
  final="$(mktemp "${TMPDIR:-/tmp}/hypercore-loop-codex-$gate-final.XXXXXX")"
  combined="$(printf '%s\n\n---\n\n%s' "$sys" "$prompt")"
  codex_cmd_prefix "$sandbox"

  case "$mode" in
    start)  CODEX_CMD+=(exec --json -o "$final" -) ;;
    resume)
      [ -n "$sid" ] || die "cannot resume codex gate $gate without a session id"
      CODEX_CMD+=(exec resume --json -o "$final" "$sid" -)
      ;;
    *) die "unknown gate mode: $mode" ;;
  esac

  if [ "$DRY_RUN" = 1 ]; then
    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
    [ "$mode" = start ] && PHASE_TWO_SESSION_ID=dry-run-codex-session
    rm -f "$final"
    return 0
  fi

  events="$(printf '%s' "$combined" | "${CODEX_CMD[@]}")" \
    || { rm -f "$final"; die "gate $gate failed (codex exec exited non-zero)"; }

  if [ "$mode" = start ]; then
    PHASE_TWO_SESSION_ID="$(printf '%s\n' "$events" | codex_thread_id)"
    [ -n "$PHASE_TWO_SESSION_ID" ] \
      || { rm -f "$final"; die "could not read codex thread id from gate $gate"; }
  fi

  GATE_OUTPUT="$(cat "$final")"
  rm -f "$final"
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
  local work_name="${1:-}" collection d frame address
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] start <work-name>"
  validate_work_name "$work_name"
  collection="$(new_work_collection)"
  d="$collection/$work_name"
  frame="$d/$INTENT_TREE/frame"
  address="$work_name"
  [ "$NODE_REL" = "." ] || address="$NODE_REL:$work_name"
  archived_work_dir "$work_name" >/dev/null 2>&1 \
    && die "work already historical in node $NODE_REL: $work_name"
  [ -d "$LEGACY_CHANGES/$work_name" ] \
    && die "legacy change record already exists in node $NODE_REL: $work_name"
  [ -e "$d" ] && ! is_work_node "$d" \
    && die "work path exists but is not a node in node $NODE_REL: $work_name"
  if [ ! -d "$d" ]; then
    mkdir -p "$frame" "$d/$MATERIAL_TREE"
    printf '# organizing document - %s\n\nThis work node keeps its design frame under intent/frame/.\n' "$address" > "$d/$INTENT_TREE/organizing-document.md"
    printf 'scaffolded %s\n' "$d"
  fi
  printf '\n=== gate: orient ===\n\n'; cat "$GATES/orient.md"
}

cmd_frame() {
  local work_name="${1:-}" d
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] frame <work-name>"
  validate_work_name "$work_name"
  d="$(active_work_dir "$work_name")" || die "work is not active in node $NODE_REL: $work_name"
  if ! frame_complete_at "$d"; then
    if is_legacy_change_dir "$d"; then
      die "legacy frame incomplete — need non-empty: ${LEGACY_FRAME_FILES[*]}"
    fi
    die "work-node frame incomplete — write the frame under $(relpath "$(frame_dir_for "$d")")"
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
  if is_legacy_change_dir "$d"; then
    printf '\nsigned-off-by: %s\n' "$who" >> "$frame/endorsement.md"
  else
    printf '# signoff - %s\n\nsigned-off-by: %s\n' "$work_name" "$who" > "$frame/signoff.md"
  fi
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
  if is_legacy_change_dir "$active_dir"; then
    source_desc="$frame_rel/ (legacy delta, plan, and proof)"
  else
    source_desc="$frame_rel/ (the signed work-node frame)"
  fi

  # the session clears once at sign-off: one fresh Codex thread, opened by implement,
  # then resumed after.
  local sid
  [ "$LOOP_HARNESS" = codex ] \
    || die "unsupported LOOP_HARNESS: $LOOP_HARNESS (only codex is supported)"
  sid=""
  printf '=== phase two: %s cleared session %s, re-deriving %s in node %s from its frame ===\n' \
    "$LOOP_HARNESS" "${sid:-new}" "$work_name" "$NODE_REL"

  run_gate implement "Read Edit Write Bash" start "$sid" \
    "Implement node-local work $work_name in addressed node $NODE_REL. Read only $source_desc and the intent it references; build the delta in code."
  sid="$PHASE_TWO_SESSION_ID"

  printf '\n--- gate: check (mechanical) ---\n'
  if [ "$DRY_RUN" = 1 ]; then
    printf '(dry-run) would run: ./material/check.sh\n'
  else
    check_green || die "check.sh red after implement — drift, stopping"
    printf 'check.sh green\n'
  fi
  run_gate check "Read Bash" resume "$sid" \
    "Run the sweep on the built node-local work $work_name in addressed node $NODE_REL at $active_rel against the whole corpus and work in flight across the node tree, including related work named by the frame; return coherent (bool) and notes."

  # honor the sweep's flag: read the check gate's verdict sentinel and, when it flags the
  # corpus incoherent — or when no verdict can be read — halt phase two and hand the flag to
  # the operator rather than folding the delta. The sweep flags; the operator (with the proof)
  # settles; no archive decision rests on the sweep itself. Skipped under --dry-run (no output).
  if [ "$DRY_RUN" != 1 ]; then
    case "$GATE_OUTPUT" in
      *"SWEEP_VERDICT: INCOHERENT"*)
        die "sweep flagged the corpus incoherent — phase two stops here for the operator; $work_name stays in flight, not adopted" ;;
      *"SWEEP_VERDICT: COHERENT"*)
        printf 'sweep verdict: coherent — proceeding to adoption\n' ;;
      *)
        die "no readable sweep verdict — phase two stops here for the operator; could not confirm coherence, so $work_name stays in flight, not adopted" ;;
    esac
  fi

  run_gate archive "Read Edit Write" resume "$sid" \
    "Adopt or shelve node-local work $work_name in addressed node $NODE_REL from $active_rel according to its signed frame. If adopting, fold its accepted delta into that node's intent documents and stamp each touched segment's foot with the signed-off-by operator. End with ARCHIVE_DECISION: ADOPTED or ARCHIVE_DECISION: SHELVED."
  printf '\n--- gate: adoption history (move) ---\n'
  if [ "$DRY_RUN" = 1 ]; then
    archive_collection="$(archive_collection_for_active_dir "$active_dir" adopted)"
    printf '(dry-run) would: check.sh green, then git mv %s %s/\n' \
      "$active_rel" "$(relpath "$archive_collection")"
  else
    check_green || die "check.sh red after fold — stopping before archive"
    if is_legacy_change_dir "$active_dir"; then
      archive_decision=adopted
    else
      archive_decision="$(archive_decision_from_output)"
    fi
    archive_collection="$(archive_collection_for_active_dir "$active_dir" "$archive_decision")"
    archive_move "$active_dir" "$archive_collection"
    printf 'recorded %s in %s history for node %s\n' "$work_name" "$archive_decision" "$NODE_REL"
  fi
}

cmd_status() {
  local work_name="${1:-}"
  [ -n "$work_name" ] || die "usage: loop.sh [-C <node-path>] status <work-name>"
  validate_work_name "$work_name"
  printf '%s in node %s: phase=%s frame_complete=%s signed_off=%s\n' "$work_name" "$NODE_REL" "$(phase "$work_name")" \
    "$(frame_complete "$work_name" && echo yes || echo no)" \
    "$(signed_off "$work_name" && echo yes || echo no)"
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
