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

shopt -s nullglob
HOME_GREENFIELD_CHECK_TMP=
HOME_GREENFIELD_CHECK_MOUNT=
LOOP_FRAME_CHECK_WORK=

cleanup_home_greenfield_self_test() {
  [ -n "${HOME_GREENFIELD_CHECK_MOUNT:-}" ] && rm -f "$HOME_GREENFIELD_CHECK_MOUNT"
  [ -n "${HOME_GREENFIELD_CHECK_TMP:-}" ] && rm -rf "$HOME_GREENFIELD_CHECK_TMP"
}

cleanup_loop_frame_self_test() {
  [ -n "${LOOP_FRAME_CHECK_WORK:-}" ] && rm -rf "$root/$LOOP_FRAME_CHECK_WORK"
}

cleanup_all() {
  cleanup_home_greenfield_self_test
  cleanup_loop_frame_self_test
}
trap cleanup_all EXIT

work_name_ok() {
  local name=$1
  [ "$name" != archive ] && [[ "$name" =~ ^[0-9][0-9][0-9]-[[:alnum:]][[:alnum:]._-]*$ ]]
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
  local node=$1 label=$2 adopted shelved
  adopted=$node/intent/history/adopted
  shelved=$node/intent/history/shelved

  if [ -d "$node/intent/history" ]; then
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

check_loop_frame_contract() {
  local name tmp frame direction review fake_review status_out

  echo "root - loop frame contract"
  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-loop-frame-check.XXXXXX")" \
    || { bad "loop frame self-test can create temporary space"; return; }
  name="999-check-loop-frame-contract-$$"
  LOOP_FRAME_CHECK_WORK="$name"
  rm -rf "$root/$name"

  if "$root/adapter/loop.sh" start "$name" >"$tmp/start.out" 2>"$tmp/start.err"; then
    ok "loop start creates a temporary work node"
  else
    bad "loop start creates a temporary work node"
  fi

  frame="$root/$name/intent/frame/frame.md"
  [ -f "$frame" ] \
    && ok "loop start scaffolds intent/frame/frame.md" \
    || bad "loop start did not scaffold intent/frame/frame.md"
  require_text "$frame" "Reversibility: TODO" \
    "frame template includes exact reversibility slot"
  require_text "$frame" "## acceptance condition" \
    "frame template includes acceptance condition"
  require_text "$frame" "## adoption claim" \
    "frame template includes adoption claim"
  reject_text "$frame" "## operator deliberation" \
    "frame template no longer scaffolds operator deliberation pile"
  reject_text "$frame" "## common ground" \
    "frame template no longer scaffolds common-ground pile"

  if "$root/adapter/loop.sh" frame "$name" >"$tmp/frame.out" 2>"$tmp/frame.err"; then
    bad "loop frame rejects a placeholder-only frame"
  else
    ok "loop frame rejects a placeholder-only frame"
  fi
  require_text "$tmp/frame.err" "missing required frame field" \
    "loop frame explains missing required frame fields"

  write_lean_frame() {
    local route_text=$1 reversibility=${2:-two-way}
    cat > "$frame" <<EOF
# frame - self-test

## work

Addressed node: root

Node-local work name: $name

Target segments: loop

Work in flight: none

## problem

Lean contract completeness self-test.

## constraints

Keep this frame intentionally narrow.

## decision surface or open direction

The operator direction surface is named.

Reversibility: $reversibility

## route

$route_text

## acceptance condition

The loop reports frame_complete=yes for complete test cases.

## proof state

The proof state is recorded.

## sweep

The sweep is recorded.

## adoption claim

The adoption claim is recorded.
EOF
  }

  write_direction() {
    local field=$1 value=$2
    cat > "$direction" <<EOF
# direction - $name

direction-by: qqp-dev
direction-given-at: 2026-06-07T00:00:00Z
$field: $value
EOF
  }

  write_valid_review() {
    cat > "$review" <<'EOF'
# review - self-test

Overall: PASS
Isolation: reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter.
Disposition: resolved - base roster returned PASS.

## base roster verdicts

- contract-checkability: PASS
- soundness-fit: PASS
- simplicity-fastness: PASS
- red-team: PASS
EOF
  }

  direction="$root/$name/intent/frame/direction.md"
  review="$root/$name/intent/frame/review.md"

  write_lean_frame "Route is written before direction." two-way
  rm -f "$direction" "$review"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/no-direction.out" 2>"$tmp/no-direction.err"; then
    bad "loop frame rejects route content without direction"
  else
    ok "loop frame rejects route content without direction"
  fi
  require_text "$tmp/no-direction.err" "route is populated before substantive direction" \
    "loop frame explains route-before-direction rejection"

  write_lean_frame "TODO" two-way
  if "$root/adapter/loop.sh" direct "$name" qqp-dev --route "" >"$tmp/empty-direction.out" 2>"$tmp/empty-direction.err"; then
    bad "loop direct rejects empty direction"
  else
    ok "loop direct rejects empty direction"
  fi
  require_text "$tmp/empty-direction.err" "direction text is empty or placeholder" \
    "loop direct explains empty direction"

  write_lean_frame "Route is written before direction." two-way
  if "$root/adapter/loop.sh" direct "$name" qqp-dev --route "operator route" >"$tmp/late-direction.out" 2>"$tmp/late-direction.err"; then
    bad "loop direct refuses after route content"
  else
    ok "loop direct refuses after route content"
  fi
  require_text "$tmp/late-direction.err" "cannot record direction after route content exists" \
    "loop direct explains retrospective direction refusal"

  write_lean_frame "TODO" two-way
  rm -f "$direction" "$review"
  if "$root/adapter/loop.sh" direct "$name" qqp-dev --delegate "operator delegates route within constraints" >"$tmp/delegate.out" 2>"$tmp/delegate.err"; then
    ok "loop direct records delegation direction"
  else
    bad "loop direct records delegation direction"
  fi
  require_text "$direction" "direction-by: qqp-dev" \
    "direction artifact records direction-by"
  require_text "$direction" "direction-given-at:" \
    "direction artifact records direction-given-at"
  require_text "$direction" "delegation: operator delegates route within constraints" \
    "direction artifact records exactly one substantive delegation"
  write_lean_frame "Two-way route after operator delegation." two-way
  if status_out="$("$root/adapter/loop.sh" status "$name" 2>"$tmp/two-way-status.err")" &&
     printf '%s\n' "$status_out" | grep -Fq "frame_complete=yes"; then
    ok "two-way work with direction and no review is frame-complete"
  else
    bad "two-way work with direction and no review is frame-complete"
  fi

  write_lean_frame "One-way route after direction, but review is missing." one-way
  rm -f "$review"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/missing-review.out" 2>"$tmp/missing-review.err"; then
    bad "one-way work with direction but no review is rejected"
  else
    ok "one-way work with direction but no review is rejected"
  fi
  require_text "$tmp/missing-review.err" "missing one-way review artifact" \
    "loop frame explains missing one-way review"

  write_valid_review
  if status_out="$("$root/adapter/loop.sh" status "$name" 2>"$tmp/one-way-status.err")" &&
     printf '%s\n' "$status_out" | grep -Fq "frame_complete=yes"; then
    ok "one-way work with direction and review is frame-complete"
  else
    bad "one-way work with direction and review is frame-complete"
  fi

  write_lean_frame "TODO" two-way
  write_direction "selected-route" "route text hidden outside frame.md"
  cat > "$review" <<'EOF'
# review - self-test

## route

This route text must not satisfy the frame route field.

Overall: PASS
Disposition: resolved - no flags.
- contract-checkability: PASS
- soundness-fit: PASS
- simplicity-fastness: PASS
- red-team: PASS
EOF
  cat > "$root/$name/intent/frame/signoff.md" <<'EOF'
# signoff - self-test

signed-off-by: qqp-dev

## route

This route text must not satisfy the frame route field either.
EOF
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/excluded-artifacts.out" 2>"$tmp/excluded-artifacts.err"; then
    bad "loop frame excludes direction/review/signoff from frame field parsing"
  else
    ok "loop frame excludes direction/review/signoff from frame field parsing"
  fi
  require_text "$tmp/excluded-artifacts.err" "missing required frame field: route" \
    "loop frame reports missing route from canonical frame.md"
  rm -f "$root/$name/intent/frame/signoff.md"

  fake_review="$tmp/fake-review"
  mkdir -p "$fake_review"
  printf 'not a structured verdict\n' > "$fake_review/contract-checkability"
  printf 'VERDICT: PASS\nNOTE: ok\n' > "$fake_review/soundness-fit"
  printf 'VERDICT: PASS\nNOTE: ok\n' > "$fake_review/simplicity-fastness"
  printf 'VERDICT: PASS\nNOTE: ok\n' > "$fake_review/red-team"
  printf 'VERDICT: PASS\nNOTE: advisory ok\n' > "$fake_review/operator-ergonomics"
  write_lean_frame "TODO" one-way
  HYPERCORE_REVIEW_FAKE_DIR="$fake_review" "$root/adapter/loop.sh" review "$name" --add operator-ergonomics >"$tmp/review.out" 2>"$tmp/review.err" \
    && ok "loop review uses deterministic fake reviewer output in self-test" \
    || bad "loop review uses deterministic fake reviewer output in self-test"
  require_text "$review" "- contract-checkability: FLAG" \
    "malformed reviewer output counts as FLAG"
  require_text "$review" "- operator-ergonomics: PASS" \
    "optional reviewer verdict is recorded as advisory"
  require_text "$review" "optional reviewers are advisory only and cannot clear base-roster or red-team flags" \
    "optional reviewers cannot clear base flags"

  cat > "$frame" <<'EOF'
# frame - self-test

## work

Addressed node: root

Node-local work name: self-test

Target segments: loop

Work in flight: none

## problem

Old contract completeness self-test.

## constraints

Keep this frame intentionally missing the new deliberation record.

## decision surface or open direction

The decision surface is already named.

Reversibility: one-way

## route

Exercise a manual review with uncleared base flags.

## acceptance condition

The contract rejects optional override.

## proof state

The proof state is recorded.

## sweep

The sweep is recorded.

## adoption claim

The adoption claim is recorded.
EOF
  write_direction "selected-route" "operator chose route"
  cat > "$review" <<'EOF'
# review - self-test

Overall: FLAG
Disposition: advisory optional pass only.

## base roster verdicts

- contract-checkability: FLAG
- soundness-fit: PASS
- simplicity-fastness: PASS
- red-team: PASS

## advisory optional verdicts

- operator-ergonomics: PASS
EOF
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/optional-override.out" 2>"$tmp/optional-override.err"; then
    bad "loop frame rejects optional reviewer override of base flags"
  else
    ok "loop frame rejects optional reviewer override of base flags"
  fi
  require_text "$tmp/optional-override.err" "optional reviewers cannot clear them" \
    "loop frame explains optional reviewers cannot clear base flags"

  cleanup_loop_frame_self_test
  LOOP_FRAME_CHECK_WORK=
  rm -rf "$tmp"
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
require_text "$root/hypercore.md" \
  "understanding before route" \
  "hypercore.md carries understanding before route"
require_text "$root/hypercore.md" \
  "mechanical base review roster" \
  "hypercore.md carries mechanical base review"
require_text "$root/hypercore.md" \
  "acceptance condition" \
  "hypercore.md carries the lean acceptance condition"
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
retired_changes_path="intent/chan""ges"
retired_change_history_path="intent/history/change-fo""lders"
retired_child_change="child-chan""ge"
retired_endorsement_file="endorsement"."md"
retired_old_route_token="LEG""ACY"
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
  "ordinary conversation/read-only inspection" \
  "orient gate classifies the request surface"
require_text "$root/adapter/gates/orient.md" \
  "do not bypass the loop because the work appears small" \
  "orient gate rejects simplicity-based loop bypass"
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
require_text "$root/adapter/gates/orient.md" \
  "teach-back" \
  "orient gate requires teach-back"
require_text "$root/adapter/gates/orient.md" \
  "alternative framing" \
  "orient gate requires an alternative framing"
require_text "$root/adapter/gates/orient.md" \
  "information-gain questions" \
  "orient gate requires information-gain questions"
require_text "$root/adapter/gates/orient.md" \
  "reversibility classification" \
  "orient gate requires reversibility classification"
require_text "$root/adapter/gates/orient.md" \
  "Do not guess, do not write a route" \
  "orient gate forbids route writing"
require_text "$root/adapter/gates/frame.md" \
  "constraints, decision surface, reversibility" \
  "frame gate names the problem, constraints, and decision surface"
require_text "$root/adapter/gates/frame.md" \
  "direction.md" \
  "frame gate requires direction artifact"
require_text "$root/adapter/gates/frame.md" \
  "direction-by:" \
  "frame gate requires direction-by"
require_text "$root/adapter/gates/frame.md" \
  "selected-route:" \
  "frame gate requires substantive selected route"
require_text "$root/adapter/gates/frame.md" \
  "review.md" \
  "frame gate requires one-way review artifact"
require_text "$root/adapter/gates/frame.md" \
  "Optional reviewers are additive" \
  "frame gate prevents optional reviewer override"
require_text "$root/adapter/gates/frame.md" \
  "wait for \`./direction\`" \
  "frame gate waits for direction"
require_text "$root/adapter/gates/frame.md" \
  "one-way work" \
  "frame gate names one-way review"
require_text "$root/adapter/gates/frame.md" \
  "two-way" \
  "frame gate names two-way reversibility"
require_text "$root/adapter/gates/frame.md" \
  "non-retrospective" \
  "frame gate requires non-retrospective direction"
require_text "$root/adapter/gates/check.md" \
  "./check.sh" \
  "check gate names the flat check command"
require_text "$root/adapter/gates/implement.md" \
  "signed frame under \`intent/frame/\`" \
  "implement gate reads current work-node frames"
require_text "$root/adapter/gates/archive.md" \
  "intent/frame/signoff.md" \
  "archive gate signs current work-node frames"
require_text "$root/adapter/codex.md" \
  "design-phase collaboration" \
  "Codex adapter describes phase one as design-phase collaboration"
require_text "$root/adapter/codex.md" \
  "First classify the request surface" \
  "Codex adapter classifies the request surface"
require_text "$root/adapter/codex.md" \
  "never waives the loop for governed work" \
  "Codex adapter rejects simplicity-based loop bypass"
require_text "$root/adapter/codex.md" \
  "teach-back" \
  "Codex adapter carries teach-back before route"
require_text "$root/adapter/codex.md" \
  "alternative framing" \
  "Codex adapter carries alternative framing before route"
require_text "$root/adapter/codex.md" \
  "reversibility classification" \
  "Codex adapter carries reversibility classification"
require_text "$root/adapter/codex.md" \
  "./review <work-name> [--add <role>]..." \
  "Codex adapter names the root review helper"
require_text "$root/adapter/codex.md" \
  "contract-checkability" \
  "Codex adapter names the base review roster"
require_text "$root/adapter/codex.md" \
  "optional complete-roster reviewers are advisory" \
  "Codex adapter makes optional reviewers advisory"
require_text "$root/adapter/codex.md" \
  "./direction" \
  "Codex adapter names the root direction helper"
require_text "$root/adapter/codex.md" \
  "never write direction" \
  "Codex adapter blocks machine-authored direction"
require_text "$root/adapter/codex.md" \
  "acceptance condition" \
  "Codex adapter carries acceptance condition"
require_text "$root/adapter/codex.md" \
  "signed frame directory" \
  "Codex adapter keeps phase two tied to the signed frame directory"
require_text "$root/adapter/codex.md" \
  "decision surface" \
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
  'FRAME_REQUIRED_FIELDS=(' \
  "loop declares required frame fields"
require_text "$root/adapter/loop.sh" \
  'frame_contract_errors_at()' \
  "loop validates the frame field contract"
require_text "$root/adapter/loop.sh" \
  '"decision surface or open direction"' \
  "loop requires decision surface or open direction"
require_text "$root/adapter/loop.sh" \
  '"reversibility"' \
  "loop requires reversibility"
require_text "$root/adapter/loop.sh" \
  '"acceptance condition"' \
  "loop requires acceptance condition"
require_text "$root/adapter/loop.sh" \
  '"adoption or shelving claim"' \
  "loop requires adoption or shelving claim"
require_text "$root/adapter/loop.sh" \
  'template="$frame/frame.md"' \
  "loop start scaffolds canonical frame.md"
require_text "$root/adapter/loop.sh" \
  'frame_section_has_content "$file" "route"' \
  "loop strictly parses route from canonical frame.md"
require_text "$root/adapter/loop.sh" \
  'frame_label_has_content "$file" "Acceptance condition"' \
  "loop parses acceptance condition as a strict label"
require_text "$root/adapter/loop.sh" \
  'frame_reversibility_value_from_file' \
  "loop parses exact reversibility tokens"
require_text "$root/adapter/loop.sh" \
  'direction_contract_errors_at()' \
  "loop validates structured direction"
require_text "$root/adapter/loop.sh" \
  'cmd_direct()' \
  "loop exposes direct command"
require_text "$root/adapter/loop.sh" \
  'direction text is empty or placeholder' \
  "loop rejects empty direction"
require_text "$root/adapter/loop.sh" \
  'cannot record direction after route content exists' \
  "loop rejects retrospective direction"
require_text "$root/adapter/loop.sh" \
  'cmd_review()' \
  "loop exposes review command"
require_text "$root/adapter/loop.sh" \
  'BASE_REVIEW_ROLES=(' \
  "loop declares the base review roster"
require_text "$root/adapter/loop.sh" \
  'OPTIONAL_REVIEW_ROLES=(' \
  "loop declares complete optional review roster"
require_text "$root/adapter/loop.sh" \
  'REVIEW_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")' \
  "reviewer subprocesses use literal approval never and read-only sandbox"
require_text "$root/adapter/loop.sh" \
  'validate_review_model' \
  "loop validates CODEX_REVIEW_MODEL"
require_text "$root/adapter/loop.sh" \
  'malformed PASS/FLAG verdict; counted as FLAG' \
  "malformed reviewer output counts as FLAG"
require_text "$root/adapter/loop.sh" \
  'optional reviewers cannot clear them' \
  "loop reports optional reviewer non-override"
require_text "$root/adapter/loop.sh" \
  'archive decision must be exactly one line' \
  "loop parses archive decision exactly and singularly"
require_text "$root/adapter/loop.sh" \
  'running ./check.sh after history move' \
  "loop checks again after moving work history"
reject_text "$root/adapter/loop.sh" \
  '"problem/domain map"' \
  "loop no longer requires the problem/domain map"
reject_text "$root/adapter/loop.sh" \
  '"evidence standard"' \
  "loop no longer requires the evidence standard"
reject_text "$root/adapter/loop.sh" \
  '"operator expectation"' \
  "loop no longer requires operator expectation"
reject_text "$root/adapter/loop.sh" \
  '## common ground' \
  "loop start no longer scaffolds common-ground pile"
reject_text "$root/adapter/loop.sh" \
  '## operator deliberation' \
  "loop start no longer scaffolds operator-deliberation pile"
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
require_text "$root/direction" \
  'adapter/loop.sh' \
  "root direction helper dispatches to the loop"
require_text "$root/direction" \
  'direct "$@"' \
  "root direction helper preserves explicit arguments"
[ -x "$root/direction" ] \
  && ok "root direction helper is executable" \
  || bad "root direction helper is not executable ($root/direction)"
require_text "$root/review" \
  'adapter/loop.sh' \
  "root review helper dispatches to the loop"
require_text "$root/review" \
  'review "$@"' \
  "root review helper preserves explicit arguments"
[ -x "$root/review" ] \
  && ok "root review helper is executable" \
  || bad "root review helper is not executable ($root/review)"
require_text "$root/adapter/loop.sh" \
  'frame/signoff.md' \
  "loop keys new work sign-off to the signoff artifact"
reject_text "$root/adapter/loop.sh" \
  "grep -Rsl '^signed-off-by:'" \
  "loop does not trust arbitrary frame text as sign-off"
reject_text "$root/adapter/loop.sh" \
  "$retired_changes_path" \
  "loop carries no retired changes path"
reject_text "$root/adapter/loop.sh" \
  "$retired_change_history_path" \
  "loop carries no retired change-history path"
reject_text "$root/adapter/loop.sh" \
  "$retired_endorsement_file" \
  "loop carries no retired sign-off file"
reject_text "$root/adapter/loop.sh" \
  "$retired_old_route_token" \
  "loop carries no retired compatibility constants"
reject_text "$root/check.sh" \
  "$retired_changes_path" \
  "check.sh carries no retired changes path"
reject_text "$root/check.sh" \
  "$retired_change_history_path" \
  "check.sh carries no retired change-history path"
reject_text "$root/check.sh" \
  "$retired_endorsement_file" \
  "check.sh carries no retired sign-off file"
reject_text "$root/check.sh" \
  "$retired_old_route_token" \
  "check.sh carries no retired compatibility constants"

check_loop_frame_contract

echo "root - retired user-facing path examples"
for file in "$root/README.md" "$root/hypercore.md" "$root/adapter/codex.md" \
  "$root/adapter/codex-mounted.md" \
  "$root/adapter/gates/orient.md" "$root/adapter/gates/frame.md" \
  "$root/adapter/gates/implement.md" "$root/adapter/gates/check.md" \
  "$root/adapter/gates/archive.md" "$root/bin/home" "$root/bin/home-signoff" \
  "$root/home/README.md" "$root/signoff" "$root/direction" "$root/review"; do
  reject_text "$file" "material/hypercore.md" "$(basename "$file") does not point to material/hypercore.md"
  reject_text "$file" "material/check.sh" "$(basename "$file") does not point to material/check.sh"
  reject_text "$file" "material/adapter" "$(basename "$file") does not point to material/adapter"
  reject_text "$file" "material/home" "$(basename "$file") does not point to material/home"
  reject_text "$file" "material/bin/home" "$(basename "$file") does not point to material/bin/home"
  reject_text "$file" "$retired_changes_path" "$(basename "$file") does not point to retired changes path"
  reject_text "$file" "$retired_change_history_path" "$(basename "$file") does not point to retired change-history path"
  reject_text "$file" "$retired_child_change" "$(basename "$file") does not name the retired nested route"
  reject_text "$file" "$retired_endorsement_file" "$(basename "$file") does not name retired sign-off file"
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
