#!/usr/bin/env bash
# hypercore structural check.
#
# Re-runs the mechanically-checkable statements of the intent against this
# corpus — the root node, and every child node nested under it. A node is any
# directory holding both intent/ and material/; each child is a node too, so the
# same checks run at every depth. Each line names the statement it
# holds. A non-zero exit is drift — a check that fell, at any depth.
#
# The semantic statements (one name one concept; a statement strong enough to
# be wrong; the sweep's graded read, now across node boundaries too) are held
# by the sweep, not by this script.

set -u
cd "$(dirname "$0")/.." || exit 2
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
    [ -d "$d/material" ] \
      && ok "$label/$name has material/" \
      || bad "$label/$name missing material/"
  done
}

check_history() {
  local node=$1 label=$2 legacy_changes historical_changes work_history adopted shelved
  legacy_changes=$node/intent/changes
  historical_changes=$node/intent/history/change-folders
  work_history=$node/intent/history
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
  local home_mount_dir="$root/material/home/material" mount
  {
    find "$root" -type d -name intent
    if [ -d "$home_mount_dir" ]; then
      for mount in "$home_mount_dir"/*; do
        [ -L "$mount" ] || continue
        [ -d "$mount/intent" ] && [ -d "$mount/material" ] || continue
        printf '%s\n' "$mount/intent"
        find "$mount/material" -type d -name intent 2>/dev/null
      done
    fi
  } | sort -u
}

setup_home_greenfield_self_test() {
  local cli="$root/material/bin/home" tmp name target mount target_link nonempty_target
  local inside_target repeated_target retired_home_dir
  retired_home_dir="$root/material/work"-home

  echo "root — home greenfield"
  [ -d "$root/material/home" ] \
    && ok "material/home child node exists" \
    || bad "material/home child node missing"
  [ -d "$root/material/home/material" ] \
    && ok "material/home/material mount point exists" \
    || bad "material/home/material mount point missing"
  require_absent "$retired_home_dir" \
    "retired material home path is absent"
  [ -x "$cli" ] \
    && ok "material/bin/home exists and is executable" \
    || bad "material/bin/home is missing or not executable"
  [ -f "$cli" ] || return
  require_text "$cli" \
    "material/home/material/<name>" \
    "home CLI explains the linked mount path"

  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-home-check.XXXXXX")" \
    || { bad "greenfield self-test can create temporary space"; return; }
  HOME_GREENFIELD_CHECK_TMP="$tmp"
  name="check-$(basename "$tmp")"
  target="$tmp/project"
  mount="$root/material/home/material/$name"
  HOME_GREENFIELD_CHECK_MOUNT="$mount"

  "$cli" greenfield "../bad" "$tmp/bad-name-target" >/dev/null 2>"$tmp/bad-name.err" \
    && bad "greenfield rejects path-like mount names" \
    || ok "greenfield rejects path-like mount names"

  inside_target="$root/material/home/material/$name-inside-target"
  "$cli" greenfield "$name-inside" "$inside_target" >/dev/null 2>"$tmp/inside-target.err" \
    && bad "greenfield rejects targets inside the hypercore root" \
    || ok "greenfield rejects targets inside the hypercore root"
  rm -f "$root/material/home/material/$name-inside"

  nonempty_target="$tmp/nonempty"
  mkdir -p "$nonempty_target"
  : > "$nonempty_target/existing"
  "$cli" greenfield "$name-nonempty" "$nonempty_target" >/dev/null 2>"$tmp/nonempty.err" \
    && bad "greenfield refuses non-empty targets" \
    || ok "greenfield refuses non-empty targets"
  rm -f "$root/material/home/material/$name-nonempty"

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
  [ -d "$target/material" ] \
    && ok "greenfield target has a local material tree" \
    || bad "greenfield target missing material/"
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
  [ ! -e "$target/material/hypercore.md" ] \
    && ok "greenfield does not copy root methodology prose" \
    || bad "greenfield copied material/hypercore.md"
  [ ! -e "$target/material/check.sh" ] \
    && ok "greenfield does not copy the root check script" \
    || bad "greenfield copied material/check.sh"
  [ ! -e "$target/material/adapter" ] \
    && ok "greenfield does not copy the root adapter directory" \
    || bad "greenfield copied material/adapter"
  [ ! -e "$target/AGENTS.md" ] \
    && ok "greenfield does not copy the root adapter entry point" \
    || bad "greenfield copied AGENTS.md"
}

# --- one node: its organizing document, segments, and history are well-formed ---
check_node() {
  local node=$1 label=$2
  local intent=$node/intent
  local ms=$intent/machine-statements

  echo "$label — structure"
  [ ! -e "$node/documentation" ] && ok "documentation tree is retired" \
    || bad "documentation tree remains at $node/documentation"
  [ ! -e "$node/implementation" ] && ok "implementation tree is retired" \
    || bad "implementation tree remains at $node/implementation"
  [ -d "$node/material" ] && ok "material tree exists" \
    || bad "material tree missing ($node/material)"
  [ -f "$intent/organizing-document.md" ] && ok "organizing document exists" \
    || bad "organizing document missing ($intent/organizing-document.md)"

  # segments = intent documents other than the organizing document
  local segs
  segs=$(find "$intent" -maxdepth 1 -name '*.md' ! -name 'organizing-document.md' \
           -printf '%f\n' 2>/dev/null | sed 's/\.md$//' | sort)

  echo "$label — segments"
  local s
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

  echo "$label — history"
  check_history "$node" "$label"
}

# --- the methodology node alone must materialize its prose ---
echo "root — methodology"
[ -f "$root/material/hypercore.md" ] && ok "material/hypercore.md exists" \
  || bad "material/hypercore.md missing"
require_text "$root/material/hypercore.md" \
  "## collaboration" \
  "material/hypercore.md materializes collaboration"
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

echo "root — adapter design phase"
retired_entry="$root"/C'LAUDE.md'
retired_prose="$root/material/adapter"/clau'de-code.md'
retired_local_state=.clau'de/'
require_text "$root/AGENTS.md" \
  "material/hypercore.md" \
  "AGENTS.md routes Codex into the renamed material tree"
require_text "$root/AGENTS.md" \
  "material/adapter/loop.sh" \
  "AGENTS.md routes Codex into the renamed loop"
require_absent "$retired_entry" \
  "retired root adapter entry point is absent"
require_absent "$retired_prose" \
  "retired adapter prose is absent"
reject_text "$root/.gitignore" \
  "$retired_local_state" \
  "tracked ignore material does not hide retired local state"
require_text "$root/material/adapter/gates/orient.md" \
  "open direction that needs operator input" \
  "orient gate names open direction for operator input"
require_text "$root/material/adapter/gates/orient.md" \
  "addressed node" \
  "orient gate names the addressed node"
require_text "$root/material/adapter/gates/orient.md" \
  "node-local work name" \
  "orient gate names the node-local work name"
require_text "$root/material/adapter/gates/orient.md" \
  "target segments" \
  "orient gate names target segments"
require_text "$root/material/adapter/gates/orient.md" \
  "work in flight" \
  "orient gate names work in flight"
require_text "$root/material/adapter/gates/frame.md" \
  "problem, constraints, and decision surface" \
  "frame gate names the problem, constraints, and decision surface"
require_text "$root/material/adapter/gates/frame.md" \
  "operator direction is missing" \
  "frame gate handles missing operator direction"
require_text "$root/material/adapter/gates/frame.md" \
  "wait for operator direction" \
  "frame gate waits rather than inventing a route"
require_text "$root/material/adapter/codex.md" \
  "design-phase collaboration" \
  "Codex adapter describes phase one as design-phase collaboration"
require_text "$root/material/adapter/codex.md" \
  "decision surface for operator direction" \
  "Codex adapter carries the decision surface"
require_text "$root/material/adapter/codex.md" \
  "node-local work name" \
  "Codex adapter carries node-local work wording"
require_text "$root/material/adapter/codex.md" \
  "adopts or shelves the work according to the signed frame" \
  "Codex adapter describes adoption or shelving"
require_text "$root/material/adapter/codex.md" \
  "./signoff" \
  "Codex adapter names the root sign-off helper"
require_text "$root/material/adapter/loop.sh" \
  'LOOP_HARNESS="${LOOP_HARNESS:-codex}"' \
  "loop defaults phase two to Codex"
reject_text "$root/material/adapter/loop.sh" \
  C'LAUDE_BIN' \
  "loop carries no retired binary setting"
reject_text "$root/material/adapter/loop.sh" \
  "LOOP_BUDGET_USD" \
  "loop carries no retired budget setting"
reject_text "$root/material/adapter/loop.sh" \
  run_clau'de_gate' \
  "loop carries no retired gate runner"
require_text "$root/material/adapter/loop.sh" \
  "infer_signoff_work_name" \
  "loop can infer the single signable work node"
require_text "$root/material/adapter/loop.sh" \
  "HYPERCORE_OPERATOR" \
  "loop can infer sign-off operator from the environment"
require_text "$root/material/adapter/loop.sh" \
  "multiple frame-complete unsigned work nodes" \
  "loop blocks ambiguous work inference"
require_text "$root/material/adapter/loop.sh" \
  "multiple current intent foot endorsements" \
  "loop blocks ambiguous operator inference"
require_text "$root/signoff" \
  'material/adapter/loop.sh' \
  "root signoff helper dispatches to the loop"
require_text "$root/signoff" \
  'signoff "$@"' \
  "root signoff helper preserves explicit arguments"
[ -x "$root/signoff" ] \
  && ok "root signoff helper is executable" \
  || bad "root signoff helper is not executable ($root/signoff)"
require_text "$root/material/adapter/loop.sh" \
  'frame/signoff.md' \
  "loop keys new work sign-off to the signoff artifact"
reject_text "$root/material/adapter/loop.sh" \
  "grep -Rsl '^signed-off-by:'" \
  "loop does not trust arbitrary frame text as sign-off"

# --- the root node, then every child node nested anywhere beneath it ---
setup_home_greenfield_self_test
check_node "$root" "root"
while IFS= read -r d; do
  node=$(dirname "$d")
  [ "$node" = "$root" ] && continue            # the root is checked above
  [ -d "$node/material" ] || continue          # a node has both trees
  check_node "$node" "${node#"$root"/}"
done < <(node_intent_dirs)
cleanup_home_greenfield_self_test
HOME_GREENFIELD_CHECK_TMP=
HOME_GREENFIELD_CHECK_MOUNT=

echo
if [ $fail -eq 0 ]; then
  echo "all structural statements hold — root and every child node."
else
  echo "drift: a structural check fell."
fi
exit $fail
