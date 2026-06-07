#!/usr/bin/env bash
# hypercore structural check.
#
# Re-runs the mechanically-checkable statements of the intent against this
# corpus: the root node and every current child node nested under it. A node is
# any current corpus entry point holding intent/. Each line names the statement
# it holds. A non-zero exit is drift.

set -u
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 2
root=$(pwd)

fail=0
ok()  { printf '  ok    %s\n' "$1"; }
bad() { printf '  FAIL  %s\n' "$1"; fail=1; }

require_text() {
  local file=$1 needle=$2 label=$3
  grep -Fq -- "$needle" "$file" \
    && ok "$label" \
    || bad "$label ($file missing: $needle)"
}

reject_text() {
  local file=$1 needle=$2 label=$3
  [ -f "$file" ] || { ok "$label"; return; }
  grep -Fq -- "$needle" "$file" \
    && bad "$label ($file contains retired text: $needle)" \
    || ok "$label"
}

require_absent() {
  local path=$1 label=$2
  { [ ! -e "$path" ] && [ ! -L "$path" ]; } \
    && ok "$label" \
    || bad "$label ($path remains)"
}

require_symlink_target() {
  local path=$1 expected=$2 label=$3 actual
  if [ ! -L "$path" ]; then
    bad "$label ($path is not a symlink)"
    return
  fi
  actual="$(readlink "$path" 2>/dev/null || true)"
  [ "$actual" = "$expected" ] \
    && ok "$label" \
    || bad "$label ($path points at $actual instead of $expected)"
}

reject_regular_file() {
  local path=$1 label=$2
  if [ -f "$path" ] && [ ! -L "$path" ]; then
    bad "$label ($path is a regular file)"
  else
    ok "$label"
  fi
}

LEGACY_FRAME_FILES=(delta.md why.md proof.md endorsement.md plan.md)
shopt -s nullglob
HOME_GREENFIELD_CHECK_TMP=
HOME_GREENFIELD_CHECK_MOUNT=

cleanup_home_greenfield_self_test() {
  [ -n "${HOME_GREENFIELD_CHECK_MOUNT:-}" ] && rm -f "$HOME_GREENFIELD_CHECK_MOUNT"
  [ -n "${HOME_GREENFIELD_CHECK_TMP:-}" ] && rm -rf "$HOME_GREENFIELD_CHECK_TMP"
}
trap cleanup_home_greenfield_self_test EXIT

work_name_ok() {
  local name=$1
  [ "$name" != archive ] && [[ "$name" =~ ^[0-9][0-9][0-9]-[[:alnum:]][[:alnum:]._-]*$ ]]
}

check_legacy_change_folder() {
  local d=${1%/} label=$2 f
  for f in "${LEGACY_FRAME_FILES[@]}"; do
    [ -f "$d/$f" ] \
      && ok "$label has $f" \
      || bad "$label missing $f"
  done

  if [ -e "$d/changes" ]; then
    [ -d "$d/changes" ] \
      && check_legacy_changes_collection "$d/changes" "$label legacy child changes" \
      || bad "$label has non-directory legacy child changes ($d/changes)"
  fi
}

check_legacy_changes_collection() {
  local changes=$1 label=$2 archive
  local d name f
  archive=$changes/archive

  [ -d "$changes" ] \
    && ok "$label directory remains readable" \
    || { bad "$label directory missing ($changes)"; return; }
  [ -d "$archive" ] \
    && ok "$label archive directory remains readable" \
    || bad "$label archive directory missing ($archive)"
  [ -f "$archive/.gitkeep" ] \
    && ok "$label archive directory is held by git" \
    || bad "$label archive directory missing .gitkeep ($archive/.gitkeep)"

  for f in "${LEGACY_FRAME_FILES[@]}"; do
    [ ! -e "$archive/$f" ] \
      || bad "$label/archive is reserved, not a legacy change record ($archive/$f exists)"
  done

  for d in "$changes"/*/; do
    name=$(basename "${d%/}")
    [ "$name" = archive ] && continue
    work_name_ok "$name" \
      && ok "$label/$name has a scoped NNN-slug name" \
      || bad "$label/$name has malformed legacy change record name"
    check_legacy_change_folder "$d" "$label/$name"
  done

  for d in "$archive"/*/; do
    name=$(basename "${d%/}")
    work_name_ok "$name" \
      && ok "$label/archive/$name has a scoped NNN-slug name" \
      || bad "$label/archive/$name has malformed legacy change record name"
    check_legacy_change_folder "$d" "$label/archive/$name"
  done
}

check_work_node_history_collection() {
  local collection=$1 label=$2 d name

  [ -d "$collection" ] \
    && ok "$label directory remains readable" \
    || { bad "$label directory missing ($collection)"; return; }
  [ -f "$collection/.gitkeep" ] \
    && ok "$label directory is held by git" \
    || bad "$label directory missing .gitkeep ($collection/.gitkeep)"

  for d in "$collection"/*/; do
    name=$(basename "${d%/}")
    work_name_ok "$name" \
      && ok "$label/$name has a scoped NNN-slug name" \
      || bad "$label/$name has malformed work-node history name"
    [ -d "$d/intent" ] \
      && ok "$label/$name has intent/" \
      || bad "$label/$name missing intent/"
  done
}

check_history() {
  local node=$1 label=$2 legacy_changes historical_changes adopted shelved
  legacy_changes=$node/intent/changes
  historical_changes=$node/intent/history/change-folders
  adopted=$node/intent/history/adopted
  shelved=$node/intent/history/shelved

  if [ -d "$legacy_changes" ]; then
    check_legacy_changes_collection "$legacy_changes" "$label legacy change records"
  fi
  if [ -d "$node/intent/history" ]; then
    if [ -d "$historical_changes" ]; then
      check_legacy_changes_collection "$historical_changes" "$label historical change records"
    fi
    check_work_node_history_collection "$adopted" "$label adopted work-node history"
    check_work_node_history_collection "$shelved" "$label shelved work-node history"
  fi
}

node_intent_dirs() {
  local mount
  {
    find "$root" \
      \( -path "$root/.git" \
      -o -path "$root/.agents" \
      -o -path "$root/.codex" \
      -o -path "$root/.claude" \
      -o -path "$root/material" \
      -o -path "*/intent/history" \) -prune \
      -o -type d -name intent -print

    if [ -d "$root/home" ]; then
      for mount in "$root/home"/*; do
        [ -L "$mount" ] || continue
        [ -d "$mount/intent" ] || continue
        printf '%s\n' "$mount/intent"
        find -H "$mount" \
          \( -path "*/.git" \
          -o -path "*/.agents" \
          -o -path "*/.codex" \
          -o -path "*/.claude" \
          -o -path "*/intent/history" \) -prune \
          -o -type d -name intent -print 2>/dev/null
      done
    fi
  } | sort -u
}

tracked_live_material_paths() {
  command -v git >/dev/null 2>&1 || return 0
  git -C "$root" rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 0
  git -C "$root" ls-files | while IFS= read -r p; do
    [ -e "$root/$p" ] || [ -L "$root/$p" ] || continue
    case "$p" in
      material/001-flatten-material-tree/*) ;;
      material/check.sh|material/adapter/gates/*)
        [ ! -e "$root/.hypercore-flatten-final-cleanup" ] || printf '%s\n' "$p"
        ;;
      material|material/*|*/material|*/material/*) printf '%s\n' "$p" ;;
    esac
  done
}

check_no_tracked_live_material_paths() {
  local paths
  paths="$(tracked_live_material_paths)"
  if [ -z "$paths" ]; then
    ok "tracked live material/ paths are retired"
  else
    bad "tracked live material/ paths remain: $(printf '%s' "$paths" | tr '\n' ' ')"
  fi
}

setup_home_greenfield_self_test() {
  local cli="$root/bin/home" tmp name target mount target_link nonempty_target
  local inside_target repeated_target resolve_result

  echo "root - home greenfield"
  [ -d "$root/home/intent" ] \
    && ok "home child node exists with intent/" \
    || bad "home child node missing intent/"
  [ -f "$root/home/README.md" ] \
    && ok "home README exists at the flat mount surface" \
    || bad "home README missing ($root/home/README.md)"
  require_absent "$root/material/home" \
    "retired material/home path is absent"
  require_absent "$root/home/material" \
    "retired home/material mount point is absent"
  [ -x "$cli" ] \
    && ok "bin/home exists and is executable" \
    || bad "bin/home is missing or not executable"
  [ -f "$cli" ] || return
  require_text "$cli" \
    "home/<name>" \
    "home CLI explains the linked mount path"
  require_text "$cli" \
    "bin/home resolve [<path>]" \
    "home CLI exposes mounted path resolution"
  require_text "$cli" \
    "root-managed direct-path entrypoint symlinks" \
    "home CLI explains root-managed direct-path entrypoints"
  require_text "$cli" \
    "AGENTS.md points to the mounted-node Codex entrypoint" \
    "home CLI explains the mounted Codex entrypoint link"
  require_text "$cli" \
    "signoff points to the home signoff helper" \
    "home CLI explains the mounted signoff helper link"
  reject_text "$cli" \
    "Directly opening the external target path only sees the target's local node shape." \
    "home CLI no longer says direct opens see only local shape"

  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-home-check.XXXXXX")" \
    || { bad "greenfield self-test can create temporary space"; return; }
  HOME_GREENFIELD_CHECK_TMP="$tmp"
  name="check-$(basename "$tmp")"
  target="$tmp/project"
  mount="$root/home/$name"
  HOME_GREENFIELD_CHECK_MOUNT="$mount"

  "$cli" greenfield "../bad" "$tmp/bad-name-target" >/dev/null 2>"$tmp/bad-name.err" \
    && bad "greenfield rejects path-like mount names" \
    || ok "greenfield rejects path-like mount names"

  inside_target="$root/home/$name-inside-target"
  "$cli" greenfield "$name-inside" "$inside_target" >/dev/null 2>"$tmp/inside-target.err" \
    && bad "greenfield rejects targets inside the hypercore root" \
    || ok "greenfield rejects targets inside the hypercore root"
  rm -f "$root/home/$name-inside"

  nonempty_target="$tmp/nonempty"
  mkdir -p "$nonempty_target"
  : > "$nonempty_target/existing"
  "$cli" greenfield "$name-nonempty" "$nonempty_target" >/dev/null 2>"$tmp/nonempty.err" \
    && bad "greenfield refuses non-empty targets" \
    || ok "greenfield refuses non-empty targets"
  rm -f "$root/home/$name-nonempty"

  if "$cli" greenfield "$name" "$target" >/dev/null 2>"$tmp/greenfield.err"; then
    ok "greenfield creates a temporary external project"
  else
    bad "greenfield creates a temporary external project"
    return
  fi

  repeated_target="$tmp/repeated"
  "$cli" greenfield "$name" "$repeated_target" >/dev/null 2>"$tmp/repeated.err" \
    && bad "greenfield refuses existing mount paths" \
    || ok "greenfield refuses existing mount paths"

  [ -d "$target/.git" ] \
    && ok "greenfield target is a git repository" \
    || bad "greenfield target is not a git repository"
  [ -f "$target/intent/organizing-document.md" ] \
    && ok "greenfield target has a local organizing document" \
    || bad "greenfield target missing intent/organizing-document.md"
  [ -e "$target/AGENTS.md" ] || [ -L "$target/AGENTS.md" ] \
    && ok "greenfield target has a direct-path AGENTS.md entrypoint" \
    || bad "greenfield target missing AGENTS.md"
  [ -x "$target/signoff" ] \
    && ok "greenfield target has an executable direct-path signoff helper" \
    || bad "greenfield target missing executable signoff helper"
  require_symlink_target "$target/AGENTS.md" \
    "$root/adapter/codex-mounted.md" \
    "greenfield AGENTS.md points at the root-managed mounted Codex entrypoint"
  require_symlink_target "$target/signoff" \
    "$root/bin/home-signoff" \
    "greenfield signoff points at the root-managed home signoff helper"
  reject_regular_file "$target/AGENTS.md" \
    "greenfield AGENTS.md is not a generated regular file"
  reject_regular_file "$target/signoff" \
    "greenfield signoff is not a generated regular file"
  require_absent "$target/material" \
    "greenfield target has no material/ tree"
  [ -L "$mount" ] \
    && ok "greenfield creates a mount symlink" \
    || bad "greenfield mount symlink missing"
  target_link="$(readlink "$mount" 2>/dev/null || true)"
  [ "$target_link" = "$target" ] \
    && ok "greenfield mount symlink points at the external target" \
    || bad "greenfield mount symlink points at $target_link instead of $target"
  node_intent_dirs | grep -Fxq "$mount/intent" \
    && ok "linked mounted project is discoverable as a child node" \
    || bad "linked mounted project is not discoverable as a child node"
  if resolve_result="$("$cli" resolve "$target" 2>"$tmp/resolve-target.err")" &&
     [ "$resolve_result" = "home/$name" ]; then
    ok "home resolve maps a target root to its mounted node path"
  else
    bad "home resolve did not map target root to home/$name"
  fi
  if resolve_result="$("$cli" resolve "$target/intent" 2>"$tmp/resolve-inside.err")" &&
     [ "$resolve_result" = "home/$name" ]; then
    ok "home resolve maps a path inside the target to its mounted node path"
  else
    bad "home resolve did not map path inside target to home/$name"
  fi
  if resolve_result="$(cd "$target" && "$cli" resolve 2>"$tmp/resolve-cwd.err")" &&
     [ "$resolve_result" = "home/$name" ]; then
    ok "home resolve without a path uses the current working directory"
  else
    bad "home resolve without a path did not map the current working directory"
  fi
  "$cli" resolve "$tmp" >/dev/null 2>"$tmp/resolve-outside.err" \
    && bad "home resolve rejects paths outside mounted nodes" \
    || ok "home resolve rejects paths outside mounted nodes"
  require_text "$tmp/resolve-outside.err" \
    "not under a mounted node" \
    "home resolve explains paths outside mounted nodes"
  [ ! -e "$target/hypercore.md" ] \
    && ok "greenfield does not copy root methodology prose" \
    || bad "greenfield copied hypercore.md"
  [ ! -e "$target/check.sh" ] \
    && ok "greenfield does not copy the root check script" \
    || bad "greenfield copied check.sh"
  [ ! -e "$target/adapter" ] \
    && ok "greenfield does not copy the root adapter directory" \
    || bad "greenfield copied adapter/"
  [ ! -e "$target/bin" ] \
    && ok "greenfield does not copy the root bin directory" \
    || bad "greenfield copied bin/"
  [ "$(readlink "$target/AGENTS.md" 2>/dev/null || true)" != "$root/AGENTS.md" ] \
    && ok "greenfield does not link the root AGENTS.md entry point" \
    || bad "greenfield copied the root adapter entry point"
  require_symlink_target "$target/signoff" \
    "$root/bin/home-signoff" \
    "greenfield uses the mounted signoff entry point instead of copying root signoff"
}

check_home_mounted_nodes() {
  local mount label agents signoff

  echo "root - home mounted nodes"
  [ -d "$root/home" ] || return
  for mount in "$root/home"/*; do
    [ -L "$mount" ] || continue
    [ -d "$mount/intent" ] || continue
    label=${mount#"$root"/}
    git -C "$mount" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
      && ok "$label target is a git repository" \
      || bad "$label target is not a git repository"

    agents="$mount/AGENTS.md"
    signoff="$mount/signoff"
    if [ -e "$agents" ] || [ -L "$agents" ]; then
      require_symlink_target "$agents" \
        "$root/adapter/codex-mounted.md" \
        "$label AGENTS.md points at the root-managed mounted Codex entrypoint"
      reject_regular_file "$agents" \
        "$label AGENTS.md is not a generated regular file"
    else
      ok "$label has no direct-path AGENTS.md entrypoint"
    fi

    if [ -e "$signoff" ] || [ -L "$signoff" ]; then
      require_symlink_target "$signoff" \
        "$root/bin/home-signoff" \
        "$label signoff points at the root-managed home signoff helper"
      [ -x "$signoff" ] \
        && ok "$label signoff entrypoint is executable" \
        || bad "$label signoff entrypoint is not executable"
      reject_regular_file "$signoff" \
        "$label signoff is not a generated regular file"
    else
      ok "$label has no direct-path signoff entrypoint"
    fi
  done
}

check_node() {
  local node=$1 label=$2 intent=$1/intent ms=$1/intent/machine-statements
  local segs s

  echo "$label - structure"
  [ ! -e "$node/documentation" ] && ok "documentation tree is retired" \
    || bad "documentation tree remains at $node/documentation"
  [ ! -e "$node/implementation" ] && ok "implementation tree is retired" \
    || bad "implementation tree remains at $node/implementation"
  [ -d "$intent" ] && ok "intent tree exists" \
    || bad "intent tree missing ($intent)"
  [ -f "$intent/organizing-document.md" ] && ok "organizing document exists" \
    || bad "organizing document missing ($intent/organizing-document.md)"

  segs=$(find "$intent" -maxdepth 1 -name '*.md' ! -name 'organizing-document.md' \
           -printf '%f\n' 2>/dev/null | sed 's/\.md$//' | sort)

  echo "$label - segments"
  for s in $segs; do
    [ -f "$ms/$s.md" ] \
      && ok "$s has a machine-statements file" \
      || bad "$s has no machine-statements file ($ms/$s.md)"
    grep -q '^## machine' "$intent/$s.md" \
      && ok "$s has a ## machine section" \
      || bad "$s has no ## machine section"
    tail -n 3 "$intent/$s.md" | grep -q '^endorsed by ' \
      && ok "$s is endorsed at its foot" \
      || bad "$s has no foot endorsement"
  done

  echo "$label - history"
  check_history "$node" "$label"
}

echo "root - methodology"
[ -f "$root/hypercore.md" ] && ok "hypercore.md exists" \
  || bad "hypercore.md missing"
require_text "$root/hypercore.md" \
  "## collaboration" \
  "hypercore.md materializes collaboration"
[ -x "$root/check.sh" ] \
  && ok "check.sh exists and is executable" \
  || bad "check.sh is missing or not executable"
if [ -f "$root/intent/collaboration.md" ] ||
   grep -Fq -- "- **collaboration**" "$root/intent/organizing-document.md"; then
  require_text "$root/intent/organizing-document.md" \
    "the nine segments describing the rules themselves" \
    "organizing document counts nine methodology segments"
  require_text "$root/intent/organizing-document.md" \
    "- **collaboration**" \
    "organizing document names collaboration as a methodology segment"
  [ -f "$root/intent/collaboration.md" ] \
    && ok "intent/collaboration.md exists" \
    || bad "intent/collaboration.md missing"
  [ -f "$root/intent/machine-statements/collaboration.md" ] \
    && ok "intent/machine-statements/collaboration.md exists" \
    || bad "intent/machine-statements/collaboration.md missing"
fi

echo "root - flat paths"
check_no_tracked_live_material_paths
[ -f "$root/adapter/codex.md" ] && ok "adapter/codex.md exists" \
  || bad "adapter/codex.md missing"
[ -f "$root/adapter/codex-mounted.md" ] && ok "adapter/codex-mounted.md exists" \
  || bad "adapter/codex-mounted.md missing"
[ -x "$root/adapter/loop.sh" ] && ok "adapter/loop.sh exists and is executable" \
  || bad "adapter/loop.sh is missing or not executable"
[ -x "$root/bin/home-signoff" ] && ok "bin/home-signoff exists and is executable" \
  || bad "bin/home-signoff is missing or not executable"
for gate in orient frame implement check archive; do
  [ -f "$root/adapter/gates/$gate.md" ] \
    && ok "adapter/gates/$gate.md exists" \
    || bad "adapter/gates/$gate.md missing"
done
[ -d "$root/home/intent" ] && ok "home/intent/ exists" \
  || bad "home/intent/ missing"
[ -f "$root/home/README.md" ] && ok "home/README.md exists" \
  || bad "home/README.md missing"

echo "root - adapter design phase"
retired_entry="$root"/C'LAUDE.md'
retired_prose="$root/adapter"/clau'de-code.md'
retired_local_state=.clau'de/'
require_text "$root/AGENTS.md" \
  "hypercore.md" \
  "AGENTS.md routes Codex into the methodology prose"
require_text "$root/AGENTS.md" \
  "adapter/loop.sh" \
  "AGENTS.md routes Codex into the loop"
require_absent "$retired_entry" \
  "retired root adapter entry point is absent"
require_absent "$retired_prose" \
  "retired adapter prose is absent"
reject_text "$root/.gitignore" \
  "$retired_local_state" \
  "tracked ignore material does not hide retired local state"
require_text "$root/adapter/gates/orient.md" \
  "open direction that needs operator input" \
  "orient gate names open direction for operator input"
require_text "$root/adapter/gates/orient.md" \
  "addressed node" \
  "orient gate names the addressed node"
require_text "$root/adapter/gates/orient.md" \
  "node-local work name" \
  "orient gate names the node-local work name"
require_text "$root/adapter/gates/orient.md" \
  "target segments" \
  "orient gate names target segments"
require_text "$root/adapter/gates/orient.md" \
  "work in flight" \
  "orient gate names work in flight"
require_text "$root/adapter/gates/frame.md" \
  "problem, constraints, and decision surface" \
  "frame gate names the problem, constraints, and decision surface"
require_text "$root/adapter/gates/frame.md" \
  "operator direction is missing" \
  "frame gate handles missing operator direction"
require_text "$root/adapter/gates/frame.md" \
  "wait for operator direction" \
  "frame gate waits rather than inventing a route"
require_text "$root/adapter/gates/check.md" \
  "./check.sh" \
  "check gate names the flat check command"
require_text "$root/adapter/codex.md" \
  "design-phase collaboration" \
  "Codex adapter describes phase one as design-phase collaboration"
require_text "$root/adapter/codex.md" \
  "decision surface for operator direction" \
  "Codex adapter carries the decision surface"
require_text "$root/adapter/codex.md" \
  "node-local work name" \
  "Codex adapter carries node-local work wording"
require_text "$root/adapter/codex.md" \
  "adopts or shelves the work according to the signed frame" \
  "Codex adapter describes adoption or shelving"
require_text "$root/adapter/codex.md" \
  "./signoff" \
  "Codex adapter names the root sign-off helper"
require_text "$root/adapter/codex-mounted.md" \
  "root-managed hypercore adapter material" \
  "mounted Codex entrypoint identifies root-managed adapter material"
require_text "$root/adapter/codex-mounted.md" \
  "Governing root: \`$root\`" \
  "mounted Codex entrypoint names the governing root"
require_text "$root/adapter/codex-mounted.md" \
  "read the local target \`intent/\`" \
  "mounted Codex entrypoint tells Codex to read local intent first"
require_text "$root/adapter/codex-mounted.md" \
  "$root/bin/home resolve" \
  "mounted Codex entrypoint routes through home resolve"
require_text "$root/adapter/codex-mounted.md" \
  "$root/adapter/loop.sh -C <resolved-mount-path>" \
  "mounted Codex entrypoint routes work through the resolved mount path"
require_text "$root/adapter/codex-mounted.md" \
  "$root/adapter/codex.md" \
  "mounted Codex entrypoint points to the root adapter"
require_text "$root/adapter/codex-mounted.md" \
  "proof only when they exist" \
  "mounted Codex entrypoint keeps local checks as proof only"
require_text "$root/adapter/codex-mounted.md" \
  "Stop rather than fabricate missing facts, dormant child nodes, or operator" \
  "mounted Codex entrypoint rejects fabrication"
require_text "$root/bin/home-signoff" \
  '"$ROOT/bin/home" resolve' \
  "mounted signoff helper resolves the caller mount path"
require_text "$root/bin/home-signoff" \
  'exec "$ROOT/adapter/loop.sh" -C "$mount_path" signoff "$@"' \
  "mounted signoff helper dispatches sign-off to the root loop"
require_text "$root/adapter/loop.sh" \
  'LOOP_HARNESS="${LOOP_HARNESS:-codex}"' \
  "loop defaults phase two to Codex"
require_text "$root/adapter/loop.sh" \
  'HYPERCORE_LOOP_STATE_DIR="${HYPERCORE_LOOP_STATE_DIR:-$ROOT/.hypercore/loop-runs}"' \
  "loop defaults phase-two state under .hypercore/loop-runs"
require_text "$root/adapter/loop.sh" \
  'LOOP_RUN_EVENTS="$LOOP_RUN_DIR/events.jsonl"' \
  "loop writes a run event JSONL file"
require_text "$root/adapter/loop.sh" \
  'LOOP_RUN_STATE="$LOOP_RUN_DIR/state.json"' \
  "loop writes a current run state file"
require_text "$root/adapter/loop.sh" \
  'HYPERCORE_LOOP_STATE_DIR/current/work' \
  "loop writes an addressed-work current state pointer"
require_text "$root/adapter/loop.sh" \
  'LOOP_CURRENT_ROOT_STATE="$HYPERCORE_LOOP_STATE_DIR/current/root.json"' \
  "loop writes a root current state pointer"
require_text "$root/adapter/loop.sh" \
  'mkdir -p "$LOOP_RUN_GATE_DIR" "$(dirname "$LOOP_CURRENT_WORK_STATE")" "$(dirname "$LOOP_CURRENT_ROOT_STATE")"' \
  "loop creates the phase-two state directories"
require_text "$root/adapter/loop.sh" \
  'phase_two_preflight()' \
  "loop has a phase-two Codex preflight"
require_text "$root/adapter/loop.sh" \
  'command -v "$CODEX_BIN"' \
  "loop preflight checks the Codex binary"
require_text "$root/adapter/loop.sh" \
  'CODEX_HOME' \
  "loop preflight resolves Codex home"
require_text "$root/adapter/loop.sh" \
  'can_write_dir "$codex_home/sessions"' \
  "loop preflight checks Codex session write permission"
require_text "$root/adapter/loop.sh" \
  'if ! phase_two_preflight "$work_name"; then' \
  "loop stops directly on preflight failure"
reject_text "$root/adapter/loop.sh" \
  'phase_two_preflight "$work_name" || die' \
  "loop preserves detailed preflight failure state"
require_text "$root/adapter/loop.sh" \
  'events-codex-$gate.jsonl' \
  "loop stores the raw Codex JSON event stream per gate"
require_text "$root/adapter/loop.sh" \
  'while IFS= read -r line || [ -n "$line" ]; do' \
  "loop streams Codex JSON events while the gate runs"
require_text "$root/adapter/loop.sh" \
  'record_codex_progress_line "$gate" "$line"' \
  "loop prints progress from streamed Codex events"
reject_text "$root/adapter/loop.sh" \
  'events="$(printf' \
  "loop no longer buffers the Codex JSON stream before progress"
require_text "$root/adapter/loop.sh" \
  'loop_event sweep check' \
  "loop records the sweep verdict in run events"
require_text "$root/adapter/loop.sh" \
  'loop_event archive-decision archive' \
  "loop records the archive decision in run events"
require_text "$root/adapter/loop.sh" \
  'print_phase_two_status' \
  "loop status reports phase-two run state"
require_text "$root/adapter/loop.sh" \
  '"phase_two_run":' \
  "loop status can render phase-two run state as JSON"
reject_text "$root/adapter/loop.sh" \
  C'LAUDE_BIN' \
  "loop carries no retired binary setting"
reject_text "$root/adapter/loop.sh" \
  "LOOP_BUDGET_USD" \
  "loop carries no retired budget setting"
reject_text "$root/adapter/loop.sh" \
  run_clau'de_gate' \
  "loop carries no retired gate runner"
require_text "$root/adapter/loop.sh" \
  "infer_signoff_work_name" \
  "loop can infer the single signable work node"
require_text "$root/adapter/loop.sh" \
  "HYPERCORE_OPERATOR" \
  "loop can infer sign-off operator from the environment"
require_text "$root/adapter/loop.sh" \
  "multiple frame-complete unsigned work nodes" \
  "loop blocks ambiguous work inference"
require_text "$root/adapter/loop.sh" \
  "multiple current intent foot endorsements" \
  "loop blocks ambiguous operator inference"
require_text "$root/signoff" \
  'adapter/loop.sh' \
  "root signoff helper dispatches to the loop"
require_text "$root/signoff" \
  'signoff "$@"' \
  "root signoff helper preserves explicit arguments"
[ -x "$root/signoff" ] \
  && ok "root signoff helper is executable" \
  || bad "root signoff helper is not executable ($root/signoff)"
require_text "$root/adapter/loop.sh" \
  'frame/signoff.md' \
  "loop keys new work sign-off to the signoff artifact"
reject_text "$root/adapter/loop.sh" \
  "grep -Rsl '^signed-off-by:'" \
  "loop does not trust arbitrary frame text as sign-off"

echo "root - retired user-facing path examples"
for file in "$root/README.md" "$root/hypercore.md" "$root/adapter/codex.md" \
  "$root/adapter/codex-mounted.md" \
  "$root/adapter/gates/orient.md" "$root/adapter/gates/frame.md" \
  "$root/adapter/gates/implement.md" "$root/adapter/gates/check.md" \
  "$root/adapter/gates/archive.md" "$root/bin/home" "$root/bin/home-signoff" \
  "$root/home/README.md" "$root/signoff"; do
  reject_text "$file" "material/hypercore.md" "$(basename "$file") does not point to material/hypercore.md"
  reject_text "$file" "material/check.sh" "$(basename "$file") does not point to material/check.sh"
  reject_text "$file" "material/adapter" "$(basename "$file") does not point to material/adapter"
  reject_text "$file" "material/home" "$(basename "$file") does not point to material/home"
  reject_text "$file" "material/bin/home" "$(basename "$file") does not point to material/bin/home"
done

setup_home_greenfield_self_test
check_home_mounted_nodes
check_node "$root" "root"
while IFS= read -r d; do
  node=$(dirname "$d")
  [ "$node" = "$root" ] && continue
  check_node "$node" "${node#"$root"/}"
done < <(node_intent_dirs)
cleanup_home_greenfield_self_test
HOME_GREENFIELD_CHECK_TMP=
HOME_GREENFIELD_CHECK_MOUNT=

echo
if [ $fail -eq 0 ]; then
  echo "all structural statements hold - root and every current child node."
else
  echo "drift: a structural check fell."
fi
exit $fail
