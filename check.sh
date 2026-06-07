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

require_order() {
  local file=$1 first=$2 second=$3 label=$4 first_line second_line
  first_line="$(grep -Fn -- "$first" "$file" | sed -n '1s/:.*//p')"
  second_line="$(grep -Fn -- "$second" "$file" | sed -n '1s/:.*//p')"
  if [ -n "$first_line" ] && [ -n "$second_line" ] && [ "$first_line" -lt "$second_line" ]; then
    ok "$label"
  else
    bad "$label ($file does not contain ordered markers: $first before $second)"
  fi
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
  local name tmp frame options direction review fake_review fake_acceptance fake_builder fake_check retry_handoff status_out route_with_one_unit route_with_two_units panel_events
  local panel_start_line panel_first_result_line
  local resume_cache resume_out_first resume_out_second resume_out_third resume_unit_001_cache resume_unit_002_cache

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
  options="$root/$name/intent/frame/options.md"
  [ -f "$frame" ] \
    && ok "loop start scaffolds intent/frame/frame.md" \
    || bad "loop start did not scaffold intent/frame/frame.md"
  [ -f "$options" ] \
    && ok "loop start scaffolds intent/frame/options.md" \
    || bad "loop start did not scaffold intent/frame/options.md"
  require_text "$frame" "Reversibility: TODO" \
    "frame template includes exact reversibility slot"
  require_text "$frame" "## acceptance condition" \
    "frame template includes acceptance condition"
  require_text "$frame" "## observable acceptance" \
    "frame template includes observable acceptance"
  require_text "$frame" "## excluded interpretation" \
    "frame template includes excluded interpretation"
  require_text "$frame" "## adoption claim" \
    "frame template includes adoption claim"
  require_text "$options" "## option 1" \
    "options template includes numbered option 1"
  require_text "$options" "## option 2" \
    "options template includes numbered option 2"
  require_text "$options" "## rejection choices" \
    "options template includes rejection choices"
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

## observable acceptance

Run loop status for this self-test work.

## excluded interpretation

This self-test does not adopt parent intent.

## proof state

The proof state is recorded.

## sweep

The sweep is recorded.

## adoption claim

The adoption claim is recorded.
EOF
    if [ -f "${direction:-}" ]; then
      local existing_selection existing_field existing_value
      existing_selection="$(awk '
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
            sub(/^[[:space:]]+/, "", value)
            sub(/[[:space:]]+$/, "", value)
            print label "\t" value
            exit
          }
        }
      ' "$direction" 2>/dev/null || true)"
      if [ -n "$existing_selection" ]; then
        IFS=$'\t' read -r existing_field existing_value <<< "$existing_selection"
        write_options "$existing_field" "$existing_value"
      else
        write_options selected-route "operator chose route"
      fi
    else
      write_options selected-route "operator chose route"
    fi
  }

  write_options() {
    local selected_kind=${1:-selected-route} selected_summary=${2:-operator chose route}
    cat > "$options" <<EOF
# options - $name

Direction options are drafted by the machine for operator selection.

## option 1

id: chosen-option
kind: $selected_kind
summary: $selected_summary
reversibility: two-way
tradeoff: exercises the selected operator direction while keeping the self-test narrow.

## option 2

id: alternate-option
kind: selected-route
summary: operator chose alternate route
reversibility: two-way
tradeoff: keeps the option surface materially distinct without changing the fixture.

## rejection choices

none: The operator may reject all options and send the work back to frame.
abort: The operator may abort without writing direction.
EOF
  }

  write_direction() {
    local field=$1 value=$2
    write_options "$field" "$value"
    cat > "$direction" <<EOF
# direction - $name

direction-by: qqp-dev
direction-given-at: 2026-06-07T00:00:00Z
operator-gate: tty
$field: $value
EOF
  }

  write_ungated_direction() {
    local field=$1 value=$2
    write_options "$field" "$value"
    cat > "$direction" <<EOF
# direction - $name

direction-by: qqp-dev
direction-given-at: 2026-06-07T00:00:00Z
$field: $value
EOF
  }

  write_bad_gate_direction() {
    local field=$1 value=$2
    write_options "$field" "$value"
    cat > "$direction" <<EOF
# direction - $name

direction-by: qqp-dev
direction-given-at: 2026-06-07T00:00:00Z
operator-gate: tty-extra
$field: $value
EOF
  }

  write_hmac_ready_direction() {
    local field=$1 value=$2
    write_options "$field" "$value"
    cat > "$direction" <<EOF
# direction - $name

direction-by: qqp-dev
direction-given-at: 2026-06-07T00:00:00Z
operator-gate: hmac:reservedvalue
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

  write_signoff() {
    cat > "$root/$name/intent/frame/signoff.md" <<EOF
# signoff - $name

signed-off-by: qqp-dev
signed-off-at: 2026-06-07T00:00:00Z
operator-gate: tty
EOF
  }

  write_ungated_signoff() {
    cat > "$root/$name/intent/frame/signoff.md" <<EOF
# signoff - $name

signed-off-by: qqp-dev
EOF
  }

  write_untimestamped_signoff() {
    cat > "$root/$name/intent/frame/signoff.md" <<EOF
# signoff - $name

signed-off-by: qqp-dev
operator-gate: tty
EOF
  }

  write_bad_gate_signoff() {
    cat > "$root/$name/intent/frame/signoff.md" <<EOF
# signoff - $name

signed-off-by: qqp-dev
signed-off-at: 2026-06-07T00:00:00Z
operator-gate: tty-extra
EOF
  }

  run_without_operator_tty() {
    if command -v setsid >/dev/null 2>&1; then
      setsid "$@" </dev/null
    else
      HYPERCORE_OPERATOR_GATE_TEST_NO_TTY=1 "$@" </dev/null
    fi
  }

  dry_run_artifact() {
    local rel=$1
    find "$tmp/loop-runs" -path "*/phase-two-dry-run/$rel" -type f -print | sort | tail -1
  }

  panel_lens_instruction_marker() {
    case "$1" in
      whole-acceptance-conformance) printf 'For the whole-acceptance-conformance lens' ;;
      proof-integrity) printf 'For the proof-integrity lens' ;;
      independent-coherence) printf 'For the independent-coherence lens' ;;
      security-permissions) printf 'For the security-permissions lens' ;;
      red-team) printf 'For the red-team lens' ;;
      *) printf 'unknown lens marker' ;;
    esac
  }

  require_panel_lens_prompt() {
    local rel=$1 lens=$2 artifact other marker expected
    artifact="$(dry_run_artifact "$rel")"
    if [ -z "$artifact" ]; then
      bad "tier-two $lens prompt artifact is present"
      return
    fi
    require_text "$artifact" "Lens: $lens" \
      "tier-two $lens artifact names its own lens"
    expected="$(panel_lens_instruction_marker "$lens")"
    require_text "$artifact" "$expected" \
      "tier-two $lens prompt is lens-specific"
    for other in whole-acceptance-conformance proof-integrity independent-coherence security-permissions red-team; do
      [ "$other" = "$lens" ] && continue
      marker="$(panel_lens_instruction_marker "$other")"
      reject_text "$artifact" "$marker" \
        "tier-two $lens prompt does not carry stale $other instruction"
    done
  }

  write_acceptance_output() {
    local path=$1 verdict=$2 rationale=$3 evidence=$4
    {
      printf 'VERDICT: %s\n' "$verdict"
      printf 'RATIONALE: %s\n' "$rationale"
      printf 'EVIDENCE: %s\n' "$evidence"
    } > "$path"
  }

  write_builder_output() {
    local path=$1 status=$2 message=$3
    printf '%s\n' "$message" > "$path"
    printf '%s\n' "$status" > "$path.status"
  }

  write_fake_status() {
    local path=$1 status=$2
    printf '%s\n' "$status" > "$path.status"
  }

  run_with_operator_tty() {
    local token=$1 command
    shift
    command="$(printf '%q ' "$@")"
    printf '%s\n' "$token" | script -qefc "$command" /dev/null
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
  rm -f "$direction" "$review"
  write_options selected-route "operator chose route from option one"
  if "$root/adapter/loop.sh" direct "$name" qqp-dev --route "operator chose route from option one" >"$tmp/explicit-newwork.out" 2>"$tmp/explicit-newwork.err"; then
    bad "loop direct refuses explicit forms for new gated work"
  else
    ok "loop direct refuses explicit forms for new gated work"
  fi
  require_text "$tmp/explicit-newwork.err" "explicit direction forms cannot record gated operator direction for new work" \
    "loop direct explains explicit-form refusal for new work"
  [ ! -f "$direction" ] \
    && ok "loop direct explicit form for new work writes no direction artifact" \
    || bad "loop direct explicit form for new work wrote a direction artifact"

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
  write_options selected-route "operator chose route from option one"
  if run_without_operator_tty "$root/adapter/loop.sh" direct "$name" qqp-dev >"$tmp/delegate.out" 2>"$tmp/delegate.err"; then
    bad "loop direct refuses without /dev/tty"
  else
    ok "loop direct refuses without /dev/tty"
  fi
  require_text "$tmp/delegate.err" "operator gate requires /dev/tty" \
    "loop direct explains /dev/tty refusal"
  [ ! -f "$direction" ] \
    && ok "loop direct without /dev/tty writes no direction artifact" \
    || bad "loop direct without /dev/tty wrote a direction artifact"

  write_lean_frame "TODO" two-way
  rm -f "$direction" "$review"
  write_options selected-route "operator chose route from option one"
  if run_with_operator_tty 1 "$root/adapter/loop.sh" direct "$name" qqp-dev >"$tmp/direct-option.out" 2>"$tmp/direct-option.err"; then
    ok "loop direct records a numbered options selection through /dev/tty"
  else
    bad "loop direct records a numbered options selection through /dev/tty"
  fi
  require_text "$direction" "operator-gate: tty" \
    "option-selected direction records the tty operator gate"
  require_text "$direction" "selected-route: operator chose route from option one" \
    "loop direct copies the selected option summary into direction.md"
  require_text "$tmp/direct-option.out" "Select one neutral option" \
    "loop direct renders neutral numbered options"

  write_lean_frame "TODO" two-way
  rm -f "$direction" "$review"
  write_options selected-route "operator chose route from option one"
  if run_with_operator_tty n "$root/adapter/loop.sh" direct "$name" qqp-dev >"$tmp/direct-none.out" 2>"$tmp/direct-none.err"; then
    bad "loop direct none-of-these writes no direction"
  else
    ok "loop direct none-of-these writes no direction"
  fi
  require_text "$tmp/direct-none.out" "operator selected none-of-these" \
    "loop direct explains none-of-these selection"
  [ ! -f "$direction" ] \
    && ok "loop direct none-of-these leaves direction absent" \
    || bad "loop direct none-of-these wrote a direction artifact"

  write_lean_frame "TODO" two-way
  rm -f "$direction" "$review"
  write_options selected-route "operator chose route from option one"
  if run_with_operator_tty q "$root/adapter/loop.sh" direct "$name" qqp-dev >"$tmp/direct-abort.out" 2>"$tmp/direct-abort.err"; then
    bad "loop direct abort writes no direction"
  else
    ok "loop direct abort writes no direction"
  fi
  require_text "$tmp/direct-abort.out" "direction aborted by operator" \
    "loop direct explains abort selection"
  [ ! -f "$direction" ] \
    && ok "loop direct abort leaves direction absent" \
    || bad "loop direct abort wrote a direction artifact"

  write_lean_frame "Two-way route after operator direction." two-way
  write_direction "selected-route" "operator chose route"
  rm -f "$options"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/missing-options.out" 2>"$tmp/missing-options.err"; then
    bad "loop frame rejects direction without options.md"
  else
    ok "loop frame rejects direction without options.md"
  fi
  require_text "$tmp/missing-options.err" "missing direction options artifact" \
    "loop frame explains missing options.md"

  write_lean_frame "Two-way route after operator direction." two-way
  write_direction "selected-route" "operator chose route"
  awk '
    /^abort:/ { next }
    { print }
  ' "$options" > "$options.tmp" && mv "$options.tmp" "$options"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/missing-abort.out" 2>"$tmp/missing-abort.err"; then
    bad "loop frame rejects options without abort handling"
  else
    ok "loop frame rejects options without abort handling"
  fi
  require_text "$tmp/missing-abort.err" "exactly one abort: rejection choice is required" \
    "loop frame explains missing abort rejection choice"

  write_lean_frame "Two-way route after operator direction." two-way
  write_direction "selected-route" "operator chose route"
  awk '
    /^kind:/ && !done { print; print "recommended: yes"; done = 1; next }
    { print }
  ' "$options" > "$options.tmp" && mv "$options.tmp" "$options"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/recommended-option.out" 2>"$tmp/recommended-option.err"; then
    bad "loop frame rejects recommended/default option markers"
  else
    ok "loop frame rejects recommended/default option markers"
  fi
  require_text "$tmp/recommended-option.err" "neutral options must not mark a recommendation" \
    "loop frame explains neutrality-relevant option rejection"

  write_lean_frame "Two-way route after operator direction." two-way
  write_direction "selected-route" "operator chose route"
  write_options selected-route "different option summary"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/option-mismatch.out" 2>"$tmp/option-mismatch.err"; then
    bad "loop frame rejects direction text not copied from options.md"
  else
    ok "loop frame rejects direction text not copied from options.md"
  fi
  require_text "$tmp/option-mismatch.err" "selected direction must be copied from a numbered option" \
    "loop frame explains direction/options mismatch"

  write_lean_frame "Route populated before a later direction timestamp." two-way
  write_direction "selected-route" "operator chose route"
  touch -d '2026-06-07 00:00:00 UTC' "$frame"
  touch -d '2026-06-07 00:00:02 UTC' "$direction"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/retrospective-direction.out" 2>"$tmp/retrospective-direction.err"; then
    bad "loop frame rejects retrospective direction timestamp"
  else
    ok "loop frame rejects retrospective direction timestamp"
  fi
  require_text "$tmp/retrospective-direction.err" "direction appears retrospective" \
    "loop frame explains retrospective direction timestamp"

  write_direction "delegation" "operator delegates route within constraints"
  require_text "$direction" "operator-gate: tty" \
    "direction artifact records the tty operator gate"
  write_lean_frame "Two-way route after ungated operator delegation." two-way
  write_ungated_direction "delegation" "operator delegates route within constraints"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/ungated-direction.out" 2>"$tmp/ungated-direction.err"; then
    bad "loop frame rejects direction without operator-gate"
  else
    ok "loop frame rejects direction without operator-gate"
  fi
  require_text "$tmp/ungated-direction.err" "missing operator-gate:" \
    "loop frame explains missing direction operator-gate"
  write_bad_gate_direction "delegation" "operator delegates route within constraints"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/bad-gate-direction.out" 2>"$tmp/bad-gate-direction.err"; then
    bad "loop frame rejects direction with invalid operator-gate"
  else
    ok "loop frame rejects direction with invalid operator-gate"
  fi
  require_text "$tmp/bad-gate-direction.err" "operator-gate: unsupported scheme tty-extra" \
    "loop frame explains invalid direction operator-gate"
  write_hmac_ready_direction "delegation" "operator delegates route within constraints"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/hmac-ready-direction.out" 2>"$tmp/hmac-ready-direction.err"; then
    bad "loop frame rejects a reserved hmac operator-gate scheme not yet implemented"
  else
    ok "loop frame rejects a reserved hmac operator-gate scheme not yet implemented"
  fi
  require_text "$tmp/hmac-ready-direction.err" "operator-gate: unsupported scheme hmac" \
    "loop frame keeps operator-gate syntax B-ready while implementing only tty"
  write_direction "delegation" "operator delegates route within constraints"
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

  rm -f "$root/$name/intent/frame/signoff.md"
  if run_without_operator_tty "$root/adapter/loop.sh" signoff "$name" qqp-dev >"$tmp/signoff-no-tty.out" 2>"$tmp/signoff-no-tty.err"; then
    bad "loop signoff refuses without /dev/tty"
  else
    ok "loop signoff refuses without /dev/tty"
  fi
  require_text "$tmp/signoff-no-tty.err" "operator gate requires /dev/tty" \
    "loop signoff explains /dev/tty refusal"
  [ ! -f "$root/$name/intent/frame/signoff.md" ] \
    && ok "loop signoff without /dev/tty writes no signoff artifact" \
    || bad "loop signoff without /dev/tty wrote a signoff artifact"
  if run_with_operator_tty "$name" "$root/adapter/loop.sh" signoff "$name" qqp-dev >"$tmp/signoff-brief.out" 2>"$tmp/signoff-brief.err"; then
    bad "loop signoff requires the work number rather than the full work name"
  else
    ok "loop signoff requires the work number rather than the full work name"
  fi
  require_text "$tmp/signoff-brief.out" "Attestation brief from frame.md" \
    "loop signoff renders a frame-derived attestation brief"
  require_text "$tmp/signoff-brief.out" "Target segments: loop" \
    "loop signoff brief includes target segments"
  require_text "$tmp/signoff-brief.out" "Reversibility: two-way" \
    "loop signoff brief includes reversibility"
  require_text "$tmp/signoff-brief.out" "Route:" \
    "loop signoff brief includes route"
  require_text "$tmp/signoff-brief.out" "Acceptance condition:" \
    "loop signoff brief includes acceptance condition"
  require_text "$tmp/signoff-brief.out" "Observable acceptance:" \
    "loop signoff brief includes observable acceptance"
  require_text "$tmp/signoff-brief.out" "Excluded interpretation:" \
    "loop signoff brief includes excluded interpretation"
  require_text "$tmp/signoff-brief.out" "Type work number ${name%%-*} to confirm:" \
    "loop signoff prompts for the work number"
  require_text "$tmp/signoff-brief.out" "expected work number ${name%%-*}" \
    "loop signoff rejects full-name confirmation"
  [ ! -f "$root/$name/intent/frame/signoff.md" ] \
    && ok "loop signoff with wrong token writes no signoff artifact" \
    || bad "loop signoff with wrong token wrote a signoff artifact"
  write_ungated_signoff
  if status_out="$("$root/adapter/loop.sh" status "$name" 2>"$tmp/ungated-signoff-status.err")" &&
     printf '%s\n' "$status_out" | grep -Fq "signed_off=no"; then
    ok "bare signoff without operator-gate does not satisfy signed-off validation"
  else
    bad "bare signoff without operator-gate does not satisfy signed-off validation"
  fi
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/ungated-signoff-execute.out" 2>"$tmp/ungated-signoff-execute.err"; then
    bad "loop execute rejects signoff without operator-gate"
  else
    ok "loop execute rejects signoff without operator-gate"
  fi
  require_text "$tmp/ungated-signoff-execute.err" "missing operator-gate:" \
    "loop execute explains missing signoff operator-gate"
  require_text "$tmp/ungated-signoff-execute.err" "missing signed-off-at:" \
    "loop execute explains missing signoff timestamp"
  write_untimestamped_signoff
  if status_out="$("$root/adapter/loop.sh" status "$name" 2>"$tmp/untimestamped-signoff-status.err")" &&
     printf '%s\n' "$status_out" | grep -Fq "signed_off=no"; then
    ok "timestamp-less signoff does not satisfy signed-off validation"
  else
    bad "timestamp-less signoff does not satisfy signed-off validation"
  fi
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/untimestamped-signoff-execute.out" 2>"$tmp/untimestamped-signoff-execute.err"; then
    bad "loop execute rejects signoff without signed-off-at"
  else
    ok "loop execute rejects signoff without signed-off-at"
  fi
  require_text "$tmp/untimestamped-signoff-execute.err" "missing signed-off-at:" \
    "loop execute explains missing timestamp on gated signoff"
  write_bad_gate_signoff
  if status_out="$("$root/adapter/loop.sh" status "$name" 2>"$tmp/bad-gate-signoff-status.err")" &&
     printf '%s\n' "$status_out" | grep -Fq "signed_off=no"; then
    ok "signoff with invalid operator-gate does not satisfy signed-off validation"
  else
    bad "signoff with invalid operator-gate does not satisfy signed-off validation"
  fi
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/bad-gate-signoff-execute.out" 2>"$tmp/bad-gate-signoff-execute.err"; then
    bad "loop execute rejects signoff with invalid operator-gate"
  else
    ok "loop execute rejects signoff with invalid operator-gate"
  fi
  require_text "$tmp/bad-gate-signoff-execute.err" "operator-gate: unsupported scheme tty-extra" \
    "loop execute explains invalid signoff operator-gate"
  write_signoff
  require_text "$root/$name/intent/frame/signoff.md" "signed-off-at: 2026-06-07T00:00:00Z" \
    "signoff artifact records signed-off-at"
  require_text "$root/$name/intent/frame/signoff.md" "operator-gate: tty" \
    "signoff artifact records the tty operator gate"

  write_lean_frame "Two-way route with observable acceptance removed." two-way
  awk '
    /^## observable acceptance/ { skip = 1; next }
    /^## excluded interpretation/ { skip = 0 }
    !skip { print }
  ' "$frame" > "$frame.tmp" && mv "$frame.tmp" "$frame"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/missing-observable.out" 2>"$tmp/missing-observable.err"; then
    bad "loop frame rejects missing observable acceptance"
  else
    ok "loop frame rejects missing observable acceptance"
  fi
  require_text "$tmp/missing-observable.err" "missing required frame field: observable acceptance" \
    "loop frame explains missing observable acceptance"

  write_lean_frame "Two-way route with excluded interpretation removed." two-way
  awk '
    /^## excluded interpretation/ { skip = 1; next }
    /^## proof state/ { skip = 0 }
    !skip { print }
  ' "$frame" > "$frame.tmp" && mv "$frame.tmp" "$frame"
  if "$root/adapter/loop.sh" frame "$name" >"$tmp/missing-excluded.out" 2>"$tmp/missing-excluded.err"; then
    bad "loop frame rejects missing excluded interpretation"
  else
    ok "loop frame rejects missing excluded interpretation"
  fi
  require_text "$tmp/missing-excluded.err" "missing required frame field: excluded interpretation" \
    "loop frame explains missing excluded interpretation"

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
  printf 'fixture crash stderr from codex exec\npartial stdout before failure\n' > "$fake_review/red-team"
  printf '1\n' > "$fake_review/red-team.status"
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
  require_text "$review" "## reviewer diagnostics" \
    "review artifact preserves reviewer diagnostic section"
  require_text "$review" "status: 1" \
    "review artifact records nonzero reviewer subprocess status"
  require_text "$review" "fixture crash stderr from codex exec" \
    "review artifact preserves nonzero reviewer diagnostic output"
  require_text "$review" "selected-output-source: fake-output" \
    "review artifact records diagnostic output source"

  rm -rf "$fake_review"
  mkdir -p "$fake_review"
  printf 'VERDICT: PASS\nNOTE: ok\n' > "$fake_review/contract-checkability"
  printf 'VERDICT: PASS\nNOTE: ok\n' > "$fake_review/soundness-fit"
  printf 'VERDICT: PASS\nNOTE: ok\n' > "$fake_review/simplicity-fastness"
  printf 'VERDICT: PASS\nNOTE: ok\n' > "$fake_review/red-team"
  printf 'VERDICT: FLAG\nNOTE: advisory performance concern\n' > "$fake_review/performance-cost"
  write_lean_frame "TODO" one-way
  HYPERCORE_REVIEW_FAKE_DIR="$fake_review" "$root/adapter/loop.sh" review "$name" --add performance-cost >"$tmp/review-advisory.out" 2>"$tmp/review-advisory.err" \
    && ok "loop review records optional flags without making them required" \
    || bad "loop review records optional flags without making them required"
  require_text "$review" "Overall: PASS" \
    "optional reviewer FLAG does not override clean base roster"
  require_text "$review" "- performance-cost: FLAG" \
    "optional reviewer FLAG is still recorded"
  require_text "$review" "## advisory optional flags" \
    "optional reviewer flags have a separate advisory section"
  require_text "$review" "- performance-cost (advisory): advisory performance concern" \
    "optional reviewer FLAG remains advisory"
  require_text "$review" "Disposition: resolved - base roster returned PASS; optional reviewers remain advisory" \
    "optional reviewer FLAG does not escalate base-roster disposition"

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

## observable acceptance

Run loop frame for this self-test work.

## excluded interpretation

Optional advisory reviewers cannot clear base flags.

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

  route_with_one_unit="Exercise phase-two acceptance in dry-run.

Implementation units for phase two:

1. Acceptance dry-run unit: prove tier-one and panel behavior."

  route_with_two_units="Exercise phase-two acceptance in dry-run.

Implementation units for phase two:

1. First acceptance dry-run unit: prove tier-one behavior.
2. Second acceptance dry-run unit: prove full-panel ordering."

  fake_acceptance="$tmp/fake-acceptance"
  rm -rf "$fake_acceptance" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance"
  printf 'PASS\nRATIONALE: bare verdict fixture\nEVIDENCE: old one-word contract\n' > "$fake_acceptance/tier-one-unit-001"
  write_lean_frame "$route_with_one_unit" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/tier-one-flag.out" 2>"$tmp/tier-one-flag.err"; then
    bad "loop execute blocks malformed tier-one acceptance output"
  else
    ok "loop execute blocks malformed tier-one acceptance output"
  fi
  require_text "$tmp/tier-one-flag.err" "tier-one implementation-acceptance FLAG" \
    "loop execute explains tier-one required flag blocking"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "Verdict: FLAG" \
    "tier-one malformed output is recorded as FLAG"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "missing or malformed VERDICT field" \
    "tier-one malformed output records actionable parser notes"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "Mechanical check immediately before this reviewer" \
    "tier-one prompt carries the pre-review mechanical check result"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "cumulative worktree snapshot" \
    "tier-one prompt explains cumulative diff records"
  [ ! -e "$root/$name/intent/frame/phase-two/tier-one/unit-001.md" ] \
    && ok "execute dry-run keeps tier-one artifacts out of the active work frame" \
    || bad "execute dry-run wrote tier-one artifacts into the active work frame"

  rm -rf "$fake_acceptance" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance"
  printf 'VERDICT: PASS\nRATIONALE: fixture deliberately omits evidence\n' > "$fake_acceptance/tier-one-unit-001"
  write_lean_frame "$route_with_one_unit" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/tier-one-no-evidence.out" 2>"$tmp/tier-one-no-evidence.err"; then
    bad "loop execute blocks evidence-free tier-one acceptance output"
  else
    ok "loop execute blocks evidence-free tier-one acceptance output"
  fi
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "Verdict: FLAG" \
    "tier-one evidence-free output is recorded as FLAG"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "missing or empty EVIDENCE field" \
    "tier-one evidence-free output records the evidence defect"

  rm -rf "$fake_acceptance" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance"
  write_acceptance_output "$fake_acceptance/tier-one-unit-001" FLAG \
    "fixture structured flag blocks the required tier-one gate" \
    "unit handoff fixture states the proof is incomplete"
  write_lean_frame "$route_with_one_unit" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/tier-one-structured-flag.out" 2>"$tmp/tier-one-structured-flag.err"; then
    bad "loop execute blocks structured tier-one FLAG output"
  else
    ok "loop execute blocks structured tier-one FLAG output"
  fi
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "Rationale: fixture structured flag blocks the required tier-one gate" \
    "tier-one structured FLAG preserves rationale"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "Evidence: unit handoff fixture states the proof is incomplete" \
    "tier-one structured FLAG preserves evidence"

  rm -rf "$fake_acceptance" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance"
  write_acceptance_output "$fake_acceptance/tier-one-unit-001" PASS \
    "fixture structured pass satisfies the signed unit proof in dry-run" \
    "dry-run artifact path tier-one/unit-001.md"
  write_lean_frame "$route_with_one_unit" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/two-way-execute.out" 2>"$tmp/two-way-execute.err"; then
    ok "two-way execute dry-run pays tier one and completes without one-way panel"
  else
    bad "two-way execute dry-run pays tier one and completes without one-way panel"
  fi
  require_text "$tmp/two-way-execute.out" "tier-one unit-001 verdict: PASS" \
    "two-way execute dry-run runs tier-one acceptance"
  require_text "$tmp/two-way-execute.out" "two-way work: one-way tier-two panel skipped" \
    "two-way execute dry-run skips the one-way panel"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "source: fake/self-test" \
    "tier-one dry-run fake acceptance records fake source"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "source-proof: fake acceptance loaded from HYPERCORE_ACCEPTANCE_FAKE_DIR in dry-run; rejected by real archive" \
    "tier-one dry-run fake acceptance records non-real source proof"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "Rationale: fixture structured pass satisfies the signed unit proof in dry-run" \
    "tier-one structured PASS preserves rationale"
  require_text "$(dry_run_artifact "tier-one/unit-001.md")" "Evidence: dry-run artifact path tier-one/unit-001.md" \
    "tier-one structured PASS preserves evidence"
  [ ! -e "$root/$name/intent/frame/phase-two/tier-two-panel/whole-acceptance-conformance.md" ] &&
  [ -z "$(dry_run_artifact "tier-two-panel/whole-acceptance-conformance.md")" ] \
    && ok "two-way execute dry-run writes no one-way panel verdicts" \
    || bad "two-way execute dry-run wrote one-way panel verdicts"

  rm -rf "$fake_acceptance" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance"
  write_acceptance_output "$fake_acceptance/tier-one-unit-001" PASS \
    "first unit passes in the panel dry-run fixture" \
    "tier-one fixture for unit-001"
  write_acceptance_output "$fake_acceptance/tier-one-unit-002" PASS \
    "second unit passes in the panel dry-run fixture" \
    "tier-one fixture for unit-002"
  write_acceptance_output "$fake_acceptance/panel-whole-acceptance-conformance" PASS \
    "whole acceptance fixture conforms" \
    "signed frame fixture and dry-run acceptance directory"
  write_acceptance_output "$fake_acceptance/panel-proof-integrity" PASS \
    "proof integrity fixture passes" \
    "unit handoffs, diffs, and structured fake acceptance fixtures"
  write_acceptance_output "$fake_acceptance/panel-independent-coherence" FLAG \
    "independent coherence fixture blocks archive" \
    "semantic sweep fixture names an unresolved mismatch"
  write_acceptance_output "$fake_acceptance/panel-security-permissions" PASS \
    "security permissions fixture passes" \
    "read-only reviewer prompt and source marker fixture"
  write_acceptance_output "$fake_acceptance/panel-red-team" PASS \
    "red-team fixture passes" \
    "bypass review fixture names no blocker"
  write_lean_frame "$route_with_two_units" one-way
  write_valid_review
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/panel-flag.out" 2>"$tmp/panel-flag.err"; then
    bad "one-way execute dry-run blocks tier-two panel flags"
  else
    ok "one-way execute dry-run blocks tier-two panel flags"
  fi
  require_text "$tmp/panel-flag.err" "tier-two implementation-acceptance panel FLAG" \
    "loop execute explains one-way panel flag blocking"
  panel_events="$(find "$tmp/loop-runs" -path "*/events.jsonl" -type f -print | sort | tail -1)"
  require_text "$tmp/panel-flag.out" "tier-two panel starting 5 concurrent lenses" \
    "one-way tier-two panel reports concurrent lens start"
  require_text "$tmp/panel-flag.out" "tier-two red-team started concurrently" \
    "one-way tier-two panel starts every lens before collecting results"
  require_text "$panel_events" "tier-two panel starting 5 concurrent lenses" \
    "tier-two panel records a concurrent panel start event"
  require_order "$panel_events" "tier-one unit-002 verdict: PASS" "tier-two implementation acceptance lens whole-acceptance-conformance" \
    "tier-two panel starts only after the final unit tier-one acceptance"
  panel_start_line="$(grep -n 'started concurrently' "$panel_events" | tail -1 | sed 's/:.*//')"
  panel_first_result_line="$(grep -n 'tier-two .* verdict:' "$panel_events" | sed -n '1s/:.*//p')"
  if [ -n "$panel_start_line" ] &&
     [ -n "$panel_first_result_line" ] &&
     [ "$panel_start_line" -lt "$panel_first_result_line" ]; then
    ok "tier-two panel starts all lens subprocesses before collecting results"
  else
    bad "tier-two panel did not record all starts before the first result"
  fi
  require_text "$(dry_run_artifact "tier-two-panel/independent-coherence.md")" "Verdict: FLAG" \
    "structured independent-coherence output is recorded as FLAG"
  require_text "$(dry_run_artifact "tier-two-panel/independent-coherence.md")" "Evidence: semantic sweep fixture names an unresolved mismatch" \
    "tier-two structured FLAG preserves evidence"
  require_panel_lens_prompt "tier-two-panel/whole-acceptance-conformance.md" "whole-acceptance-conformance"
  require_panel_lens_prompt "tier-two-panel/proof-integrity.md" "proof-integrity"
  require_panel_lens_prompt "tier-two-panel/independent-coherence.md" "independent-coherence"
  require_panel_lens_prompt "tier-two-panel/security-permissions.md" "security-permissions"
  require_panel_lens_prompt "tier-two-panel/red-team.md" "red-team"
  [ ! -e "$root/$name/intent/frame/phase-two/tier-two-panel/independent-coherence.md" ] \
    && ok "execute dry-run keeps tier-two artifacts out of the active work frame" \
    || bad "execute dry-run wrote tier-two artifacts into the active work frame"

  rm -rf "$fake_acceptance" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance"
  write_acceptance_output "$fake_acceptance/tier-one-unit-001" PASS \
    "real-run fake fixture must not be usable" \
    "HYPERCORE_ACCEPTANCE_FAKE_DIR is set outside dry-run"
  write_lean_frame "$route_with_one_unit" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" "$root/adapter/loop.sh" execute "$name" >"$tmp/real-fake-source.out" 2>"$tmp/real-fake-source.err"; then
    bad "loop execute rejects fake acceptance source in real runs"
  else
    ok "loop execute rejects fake acceptance source in real runs"
  fi
  require_text "$tmp/real-fake-source.err" "real execute refuses HYPERCORE_ACCEPTANCE_FAKE_DIR" \
    "loop execute explains fake acceptance is dry-run only"
  [ ! -e "$root/$name/intent/frame/phase-two/tier-one/unit-001.md" ] \
    && ok "real fake-source rejection writes no real tier-one artifact" \
    || bad "real fake-source rejection wrote a real tier-one artifact"

  fake_builder="$tmp/fake-builder"
  fake_check="$tmp/fake-check"
  rm -rf "$fake_acceptance" "$fake_builder" "$fake_check" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance" "$fake_builder" "$fake_check"
  write_builder_output "$fake_builder/implement-unit-001-fast-1" 0 \
    "fake fast builder attempt 1 reaches the mechanical check"
  write_builder_output "$fake_builder/implement-unit-001-fast-2" 0 \
    "fake fast builder attempt 2 reaches tier-one acceptance"
  write_builder_output "$fake_builder/implement-unit-001-fast-3" 0 \
    "fake fast builder attempt 3 reaches tier-one acceptance"
  write_builder_output "$fake_builder/implement-unit-001-strong-1" 0 \
    "fake strong builder attempt succeeds after escalation"
  write_fake_status "$fake_check/unit-001-fast-1" 1
  write_fake_status "$fake_check/unit-001-fast-2" 0
  write_fake_status "$fake_check/unit-001-fast-3" 0
  write_fake_status "$fake_check/unit-001-strong-1" 0
  write_acceptance_output "$fake_acceptance/tier-one-unit-001-fast-2" FLAG \
    "fast attempt 2 fixture keeps the unit unaccepted" \
    "tier-one fixture for fast attempt 2"
  write_acceptance_output "$fake_acceptance/tier-one-unit-001-fast-3" FLAG \
    "fast attempt 3 fixture exhausts the fast budget" \
    "tier-one fixture for fast attempt 3"
  write_acceptance_output "$fake_acceptance/tier-one-unit-001-strong-1" PASS \
    "strong attempt fixture accepts the escalated unit" \
    "tier-one fixture for strong attempt 1"
  write_lean_frame "$route_with_one_unit" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" \
    HYPERCORE_BUILDER_FAKE_DIR="$fake_builder" \
    HYPERCORE_CHECK_FAKE_DIR="$fake_check" \
    HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" \
    CODEX_STRONG_BUILDER_MODEL="gpt-5.3-codex" \
    "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/retry-escalation.out" 2>"$tmp/retry-escalation.err"; then
    ok "loop execute retries three fast builders then accepts a strong-builder escalation"
  else
    bad "loop execute retries three fast builders then accepts a strong-builder escalation"
  fi
  require_text "$tmp/retry-escalation.out" "-m gpt-5.5" \
    "fast builder dry-run command uses the gpt-5.5 builder default"
  require_text "$tmp/retry-escalation.out" "model_reasoning_effort=\\\"xhigh\\\"" \
    "fast builder dry-run command uses the builder effort default"
  require_text "$tmp/retry-escalation.out" "-m gpt-5.3-codex" \
    "strong builder dry-run command uses the strong-builder model knob"
  require_text "$tmp/retry-escalation.out" "fast builder attempt 1 for unit-001 failed: check.sh red" \
    "check failure consumes one fast-builder attempt"
  require_text "$tmp/retry-escalation.out" "fast builder attempt 2 for unit-001 failed: tier-one implementation-acceptance FLAG" \
    "tier-one FLAG consumes a fast-builder retry"
  require_text "$tmp/retry-escalation.out" "fast builder attempt 3 for unit-001 failed: tier-one implementation-acceptance FLAG" \
    "third fast-builder failure exhausts the fast budget"
  require_text "$tmp/retry-escalation.out" "escalating unit-001 to strong builder after 3 failed fast attempts" \
    "loop escalates the unit to a strong builder after the fast budget"
  require_text "$tmp/retry-escalation.out" "strong builder attempt 1 for unit-001 accepted" \
    "strong-builder escalation accepts only that unit"
  retry_handoff="$(dry_run_artifact "handoffs/unit-001.md")"
  require_text "$retry_handoff" "fake strong builder attempt succeeds after escalation" \
    "final handoff records the accepted strong-builder attempt"
  reject_text "$retry_handoff" "fake fast builder attempt 2" \
    "failed fast-builder handoff is overwritten by the accepted attempt"

  rm -rf "$fake_acceptance" "$fake_builder" "$fake_check" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance" "$fake_builder" "$fake_check"
  write_builder_output "$fake_builder/implement-unit-001-fast-1" 0 \
    "fake fast builder attempt 1 fails check"
  write_builder_output "$fake_builder/implement-unit-001-fast-2" 0 \
    "fake fast builder attempt 2 fails check"
  write_builder_output "$fake_builder/implement-unit-001-fast-3" 0 \
    "fake fast builder attempt 3 fails check"
  write_builder_output "$fake_builder/implement-unit-001-strong-1" 0 \
    "fake strong builder attempt still fails check"
  write_fake_status "$fake_check/unit-001-fast-1" 1
  write_fake_status "$fake_check/unit-001-fast-2" 1
  write_fake_status "$fake_check/unit-001-fast-3" 1
  write_fake_status "$fake_check/unit-001-strong-1" 1
  write_lean_frame "$route_with_one_unit" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" \
    HYPERCORE_BUILDER_FAKE_DIR="$fake_builder" \
    HYPERCORE_CHECK_FAKE_DIR="$fake_check" \
    HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" \
    "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/strong-stop.out" 2>"$tmp/strong-stop.err"; then
    bad "loop execute stops for the operator when the strong builder still fails"
  else
    ok "loop execute stops for the operator when the strong builder still fails"
  fi
  require_text "$tmp/strong-stop.err" "strong-builder attempt failed for unit-001" \
    "strong-builder failure reports the escalated failure"
  require_text "$tmp/strong-stop.err" "stays in flight" \
    "strong-builder failure keeps the work in flight for the operator"
  require_text "$tmp/strong-stop.out" "escalating unit-001 to strong builder after 3 failed fast attempts" \
    "strong-stop path escalates only after the fast budget"

  resume_cache="$tmp/resume-cache"
  rm -rf "$fake_acceptance" "$fake_builder" "$fake_check" "$resume_cache" "$root/$name/intent/frame/phase-two"
  mkdir -p "$fake_acceptance" "$fake_builder" "$fake_check" "$resume_cache"
  write_builder_output "$fake_builder/implement-unit-001-fast-1" 0 \
    "fake builder resume unit 1"
  write_builder_output "$fake_builder/implement-unit-002-fast-1" 0 \
    "fake builder resume unit 2"
  write_fake_status "$fake_check/unit-001-fast-1" 0
  write_fake_status "$fake_check/unit-002-fast-1" 0
  write_acceptance_output "$fake_acceptance/tier-one-unit-001-fast-1" PASS \
    "resume fixture accepts the first unit" \
    "tier-one fixture for unit-001 fast attempt 1"
  write_acceptance_output "$fake_acceptance/tier-one-unit-002-fast-1" PASS \
    "resume fixture accepts the second unit" \
    "tier-one fixture for unit-002 fast attempt 1"
  write_lean_frame "$route_with_two_units" two-way
  write_signoff
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" \
    HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR="$resume_cache" \
    HYPERCORE_BUILDER_FAKE_DIR="$fake_builder" \
    HYPERCORE_CHECK_FAKE_DIR="$fake_check" \
    HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" \
    "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/resume-first.out" 2>"$tmp/resume-first.err"; then
    ok "loop execute writes resumable unit cache records after accepted units"
  else
    bad "loop execute writes resumable unit cache records after accepted units"
  fi
  require_text "$tmp/resume-first.out" "cache miss for unit-001" \
    "first execute builds the first uncached unit"
  require_text "$tmp/resume-first.out" "cache miss for unit-002" \
    "first execute builds the second uncached unit"
  require_text "$resume_cache/cache/unit-001.key" "cache-key:" \
    "unit-001 cache record carries a cache key"
  require_text "$resume_cache/cache/unit-001.key" "base-key:" \
    "unit-001 cache record carries the signed-frame-derived base key"
  require_text "$resume_cache/cache/unit-001.key" "prior-state-key:" \
    "unit-001 cache record carries prior-unit state"
  require_text "$resume_cache/cache/unit-001.key" "loop-version-key:" \
    "unit-001 cache record carries loop implementation version"
  require_text "$resume_cache/cache/unit-001.key" "diff-key:" \
    "unit-001 cache record carries diff evidence"
  require_text "$resume_cache/cache/unit-001.key" "check-evidence: dry-run fake mechanical check green" \
    "unit-001 cache record carries green check evidence"
  require_text "$resume_cache/cache/unit-001.key" "tier-one-verdict: PASS" \
    "unit-001 cache record carries tier-one PASS evidence"
  resume_unit_002_cache="$(sed -nE 's/^cache-key:[[:space:]]*(.*)$/\1/p' "$resume_cache/cache/unit-002.key" | sed -n '1p')"

  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" \
    HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR="$resume_cache" \
    HYPERCORE_BUILDER_FAKE_DIR="$fake_builder" \
    HYPERCORE_CHECK_FAKE_DIR="$fake_check" \
    HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" \
    "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/resume-second.out" 2>"$tmp/resume-second.err"; then
    ok "loop execute skips unchanged accepted units on rerun"
  else
    bad "loop execute skips unchanged accepted units on rerun"
  fi
  require_text "$tmp/resume-second.out" "cache hit: skipping unit-001" \
    "rerun skips the unchanged first unit"
  require_text "$tmp/resume-second.out" "cache hit: skipping unit-002" \
    "rerun skips the unchanged second unit"
  reject_text "$tmp/resume-second.out" "fake builder resume unit 1" \
    "cache hit does not rerun the first unit builder"
  reject_text "$tmp/resume-second.out" "tier-one unit-001 verdict" \
    "cache hit does not rerun first unit tier-one acceptance"

  printf '\ncorrupted prior evidence\n' >> "$resume_cache/handoffs/unit-001.md"
  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" \
    HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR="$resume_cache" \
    HYPERCORE_BUILDER_FAKE_DIR="$fake_builder" \
    HYPERCORE_CHECK_FAKE_DIR="$fake_check" \
    HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" \
    "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/resume-third.out" 2>"$tmp/resume-third.err"; then
    ok "loop execute rebuilds cache misses and invalidates downstream units"
  else
    bad "loop execute rebuilds cache misses and invalidates downstream units"
  fi
  require_text "$tmp/resume-third.out" "cache miss for unit-001: handoff, diff, check evidence, or tier-one PASS changed" \
    "corrupted unit evidence causes a cache miss"
  require_text "$tmp/resume-third.out" "invalidating cached evidence for unit-002: upstream accepted state changed" \
    "changed prior-unit state invalidates downstream cached evidence"
  require_text "$tmp/resume-third.out" "fake builder resume unit 2" \
    "downstream invalidation rebuilds the second unit"
  resume_out_third="$(sed -nE 's/^cache-key:[[:space:]]*(.*)$/\1/p' "$resume_cache/cache/unit-002.key" | sed -n '1p')"
  [ -n "$resume_unit_002_cache" ] && [ -n "$resume_out_third" ] && [ "$resume_unit_002_cache" != "$resume_out_third" ] \
    && ok "downstream rebuild replaces the unit-002 cache key" \
    || bad "downstream rebuild replaces the unit-002 cache key"

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
require_text "$root/hypercore.md" \
  "operator-gate: tty" \
  "hypercore.md carries the operator-gate marker"
require_text "$root/hypercore.md" \
  "/dev/tty" \
  "hypercore.md carries the terminal liveness channel"
require_text "$root/hypercore.md" \
  "neutral, materially distinct options" \
  "hypercore.md carries neutral direction options"
require_text "$root/hypercore.md" \
  "requires the work number" \
  "hypercore.md carries informed sign-off confirmation"
require_text "$root/hypercore.md" \
  "not cryptographic non-repudiation" \
  "hypercore.md does not overclaim the operator gate"
require_text "$root/hypercore.md" \
  "structured verdicts that include rationale and evidence" \
  "hypercore.md carries structured implementation acceptance"
require_text "$root/hypercore.md" \
  "panel lenses started concurrently" \
  "hypercore.md carries concurrent tier-two panel execution"
require_text "$root/intent/collaboration.md" \
  "never chooses one for the operator" \
  "collaboration segment folds the neutral-options operator choice"
require_text "$root/intent/collaboration.md" \
  "deliberately allocated terminal" \
  "collaboration segment states the honest operator-gate limit"
require_text "$root/intent/loop.md" \
  "intent/frame/options.md" \
  "loop segment folds the neutral options artifact"
require_text "$root/intent/loop.md" \
  "B-ready gate token" \
  "loop segment folds the B-ready operator-gate token"
require_text "$root/intent/loop.md" \
  "admin form that cannot record gated operator direction for new work" \
  "loop segment folds the explicit-form legacy restriction"
require_text "$root/intent/adapter.md" \
  "terminal-gated operator-act helpers" \
  "adapter segment folds the gated operator-act helpers"
require_text "$root/intent/collaboration.md" \
  "rationale and concrete evidence" \
  "collaboration segment folds legible implementation acceptance"
require_text "$root/intent/collaboration.md" \
  "bounded proof-floor recovery" \
  "collaboration segment folds bounded build retry"
require_text "$root/intent/loop.md" \
  "a structured verdict" \
  "loop segment folds structured acceptance verdicts"
require_text "$root/intent/loop.md" \
  "fake-source required acceptance" \
  "loop segment folds acceptance source rejection"
require_text "$root/intent/loop.md" \
  "up to three fast" \
  "loop segment folds the fast-builder retry budget"
require_text "$root/intent/loop.md" \
  "execute is resumable" \
  "loop segment folds resumable execute"
require_text "$root/intent/loop.md" \
  "started concurrently" \
  "loop segment folds the concurrent tier-two panel"
require_text "$root/intent/adapter.md" \
  "resumable per-unit execute cache" \
  "adapter segment folds resumable execute materialization"
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
require_absent "$root/OPERATOR-ACTS-FINDINGS.md" \
  "operator-act scratch findings are removed from the live root"
require_absent "$root/PERFORMANCE-FINDINGS.md" \
  "performance scratch findings are removed from the live root"
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
  "neutral, materially distinct option" \
  "orient gate names neutral direction options"
require_text "$root/adapter/gates/orient.md" \
  "do not select an option" \
  "orient gate blocks machine option selection"
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
  "observable acceptance" \
  "frame gate requires observable acceptance"
require_text "$root/adapter/gates/frame.md" \
  "Excluded interpretation" \
  "frame gate requires excluded interpretation"
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
  "intent/frame/options.md" \
  "frame gate requires neutral direction options"
require_text "$root/adapter/gates/frame.md" \
  "operator-gate: tty" \
  "frame gate requires operator-gated acts"
require_text "$root/adapter/gates/frame.md" \
  "/dev/tty" \
  "frame gate names the terminal liveness channel"
require_text "$root/adapter/gates/frame.md" \
  "copied from a numbered option" \
  "frame gate ties direction to an option"
require_text "$root/adapter/gates/frame.md" \
  "signed-off-at:" \
  "frame gate requires signed-off-at in sign-off"
require_text "$root/adapter/gates/frame.md" \
  "work number" \
  "frame gate requires work-number sign-off confirmation"
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
require_text "$root/adapter/gates/check.md" \
  "tier-one implementation-acceptance" \
  "check gate names tier-one implementation acceptance"
require_text "$root/adapter/gates/check.md" \
  "RATIONALE:" \
  "check gate requires acceptance rationale"
require_text "$root/adapter/gates/check.md" \
  "EVIDENCE:" \
  "check gate requires acceptance evidence"
require_text "$root/adapter/gates/check.md" \
  "starting all required lenses concurrently" \
  "check gate carries concurrent tier-two panel execution"
require_text "$root/adapter/gates/check.md" \
  "deterministic lens paths" \
  "check gate carries deterministic panel artifact paths"
require_text "$root/adapter/gates/check.md" \
  "independent-coherence" \
  "check gate assigns one-way coherence to the panel"
require_text "$root/adapter/gates/implement.md" \
  "signed frame under \`intent/frame/\`" \
  "implement gate reads current work-node frames"
require_text "$root/adapter/gates/implement.md" \
  "lean handoff state" \
  "implement gate requires lean unit handoff state"
require_text "$root/adapter/gates/implement.md" \
  "signed-frame-derived cache state" \
  "implement gate describes resumable execute as orchestrator state"
require_text "$root/adapter/gates/archive.md" \
  "intent/frame/signoff.md" \
  "archive gate signs current work-node frames"
require_text "$root/adapter/gates/archive.md" \
  "tier-two implementation-acceptance" \
  "archive gate blocks one-way work without clean panel artifacts"
require_text "$root/adapter/gates/archive.md" \
  "real-source" \
  "archive gate rejects non-real acceptance artifacts"
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
  "intent/frame/options.md" \
  "Codex adapter names neutral direction options"
require_text "$root/adapter/codex.md" \
  "operator-gate: tty" \
  "Codex adapter carries the operator-gate marker"
require_text "$root/adapter/codex.md" \
  "/dev/tty" \
  "Codex adapter names the terminal liveness channel"
require_text "$root/adapter/codex.md" \
  "copied from the selected option" \
  "Codex adapter ties direction to selected option text"
require_text "$root/adapter/codex.md" \
  "work number" \
  "Codex adapter carries work-number sign-off confirmation"
require_text "$root/adapter/codex.md" \
  "does not prove cryptographic" \
  "Codex adapter does not overclaim the operator gate"
reject_text "$root/adapter/codex.md" \
  "--route|--constraint|--delegate <text-or->" \
  "Codex adapter no longer presents argument-transcribed direction as primary"
require_text "$root/adapter/codex.md" \
  "acceptance condition" \
  "Codex adapter carries acceptance condition"
require_text "$root/adapter/codex.md" \
  "observable acceptance" \
  "Codex adapter carries observable acceptance"
require_text "$root/adapter/codex.md" \
  "excluded interpretation" \
  "Codex adapter carries excluded interpretation"
require_text "$root/adapter/codex.md" \
  "signed frame directory" \
  "Codex adapter keeps phase two tied to the signed frame directory"
require_text "$root/adapter/codex.md" \
  "implementation-acceptance panel" \
  "Codex adapter carries one-way implementation acceptance"
require_text "$root/adapter/codex.md" \
  "structured phase-two acceptance artifacts" \
  "Codex adapter carries structured phase-two acceptance artifacts"
require_text "$root/adapter/codex.md" \
  "starting the required one-way tier-two lenses concurrently" \
  "Codex adapter carries concurrent tier-two panel execution"
reject_text "$root/adapter/codex.md" \
  "resumed across check and archive" \
  "Codex adapter no longer describes one resumed phase-two thread"
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
  'PHASE_TWO_ACCEPTANCE_DIR="$PHASE_TWO_FRAME_DIR/phase-two"' \
  "loop records phase-two acceptance state under the work frame"
require_text "$root/adapter/loop.sh" \
  '"$PHASE_TWO_TIER_ONE_DIR"' \
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
  '"observable acceptance"' \
  "loop requires observable acceptance"
require_text "$root/adapter/loop.sh" \
  '"excluded interpretation"' \
  "loop requires excluded interpretation"
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
  'frame_section_has_content "$file" "observable acceptance"' \
  "loop parses observable acceptance from canonical frame.md"
require_text "$root/adapter/loop.sh" \
  'frame_section_has_content "$file" "excluded interpretation"' \
  "loop parses excluded interpretation from canonical frame.md"
require_text "$root/adapter/loop.sh" \
  'frame_reversibility_value_from_file' \
  "loop parses exact reversibility tokens"
require_text "$root/adapter/loop.sh" \
  'direction_contract_errors_at()' \
  "loop validates structured direction"
require_text "$root/adapter/loop.sh" \
  'direction_options_contract_errors_at()' \
  "loop validates neutral direction options"
require_text "$root/adapter/loop.sh" \
  'options.md' \
  "loop names the neutral options artifact"
require_text "$root/adapter/loop.sh" \
  'direction_option_choice_from_tty()' \
  "loop selects direction from options through the operator gate"
require_text "$root/adapter/loop.sh" \
  'selected direction must be copied from a numbered option in options.md' \
  "loop ties direction text to a numbered option"
require_text "$root/adapter/loop.sh" \
  'operator selected none-of-these' \
  "loop handles none-of-these direction selections"
require_text "$root/adapter/loop.sh" \
  'direction aborted by operator' \
  "loop handles aborted direction selections"
require_text "$root/adapter/loop.sh" \
  'operator_gate_contract_errors_in_file()' \
  "loop parses operator-gate markers exactly"
require_text "$root/adapter/loop.sh" \
  '/dev/tty' \
  "loop operator gate uses /dev/tty"
require_text "$root/adapter/loop.sh" \
  'operator_gate_confirm_work "direction" "$work_name"' \
  "loop direction helper crosses the operator gate"
require_text "$root/adapter/loop.sh" \
  'signoff_contract_errors_at()' \
  "loop validates structured signoff"
require_text "$root/adapter/loop.sh" \
  'signoff_attestation_brief_at()' \
  "loop renders the sign-off attestation brief from the frame"
require_text "$root/adapter/loop.sh" \
  'operator_gate_confirm_signoff "$d" "$work_name" "$who"' \
  "loop signoff helper crosses the sign-off attestation gate"
require_text "$root/adapter/loop.sh" \
  'signed-off-at: %s' \
  "loop signoff helper writes signed-off-at"
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
  'CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")' \
  "reviewer subprocesses use literal approval never and read-only sandbox"
require_text "$root/adapter/loop.sh" \
  'codex_add_review_route_args' \
  "reviewer subprocesses use the separate strong review route"
require_text "$root/adapter/loop.sh" \
  'ACCEPTANCE_CMD=("${CODEX_CMD[@]}")' \
  "acceptance reviewer subprocesses use literal approval never and read-only sandbox"
require_text "$root/adapter/loop.sh" \
  'HYPERCORE_ACCEPTANCE_TIMEOUT_SECONDS' \
  "acceptance reviewer subprocesses have a bounded runtime override"
require_text "$root/adapter/loop.sh" \
  'timeout --kill-after=5s' \
  "acceptance reviewer subprocesses are timeout bounded"
require_text "$root/adapter/loop.sh" \
  'validate_review_model' \
  "loop validates CODEX_REVIEW_MODEL"
require_text "$root/adapter/loop.sh" \
  'CODEX_REVIEW_EFFORT:-xhigh' \
  "loop keeps review effort strong by default"
require_text "$root/adapter/loop.sh" \
  'CODEX_BUILDER_MODEL:-gpt-5.5' \
  "loop defaults fast builders to gpt-5.5 until the two-step plan/build lands"
require_text "$root/adapter/loop.sh" \
  'CODEX_BUILDER_EFFORT:-xhigh' \
  "loop applies a separate builder effort default"
require_text "$root/adapter/loop.sh" \
  'CODEX_STRONG_BUILDER_MODEL' \
  "loop exposes a strong-builder escalation model knob"
require_text "$root/adapter/loop.sh" \
  'malformed PASS/FLAG verdict; counted as FLAG' \
  "malformed reviewer output counts as FLAG"
require_text "$root/adapter/loop.sh" \
  '## reviewer diagnostics' \
  "review artifacts preserve diagnostic sections"
require_text "$root/adapter/loop.sh" \
  'selected-output-source: %s' \
  "review artifacts record diagnostic output source"
require_text "$root/adapter/loop.sh" \
  'acceptance_verdict_from_output()' \
  "loop parses implementation acceptance verdicts exactly"
require_text "$root/adapter/loop.sh" \
  'missing or malformed VERDICT field; counted as FLAG' \
  "malformed acceptance output counts as FLAG"
require_text "$root/adapter/loop.sh" \
  'missing or empty EVIDENCE field; counted as FLAG' \
  "evidence-free acceptance output counts as FLAG"
require_text "$root/adapter/loop.sh" \
  'source: %s' \
  "acceptance artifacts record a source marker"
require_text "$root/adapter/loop.sh" \
  'source-proof: %s' \
  "acceptance artifacts record source proof"
require_text "$root/adapter/loop.sh" \
  'real-reviewer' \
  "real reviewer source is represented explicitly"
require_text "$root/adapter/loop.sh" \
  'fake/self-test' \
  "fake acceptance source is represented explicitly"
require_text "$root/adapter/loop.sh" \
  'real execute refuses HYPERCORE_ACCEPTANCE_FAKE_DIR' \
  "real execute rejects fake acceptance source"
require_text "$root/adapter/loop.sh" \
  'phase_two_units_from_frame_file()' \
  "loop derives implementation units from the signed frame"
require_text "$root/adapter/loop.sh" \
  'PHASE_TWO_CACHE_DIR' \
  "loop stores per-unit execute cache records"
require_text "$root/adapter/loop.sh" \
  'phase_two_unit_base_cache_key()' \
  "loop computes signed-frame-derived per-unit cache base keys"
require_text "$root/adapter/loop.sh" \
  'phase_two_unit_evidence_cache_key()' \
  "loop folds handoff, diff, check, and tier-one evidence into cache keys"
require_text "$root/adapter/loop.sh" \
  'phase_two_unit_cache_hit()' \
  "loop validates cache hits before skipping units"
require_text "$root/adapter/loop.sh" \
  'cache hit: skipping $unit_id' \
  "loop skips unchanged accepted units on cache hits"
require_text "$root/adapter/loop.sh" \
  'invalidating cached evidence for $unit_id: $reason' \
  "loop invalidates downstream unit evidence when prior state changes"
require_text "$root/adapter/loop.sh" \
  'run_tier_one_acceptance()' \
  "loop runs tier-one implementation acceptance"
require_text "$root/adapter/loop.sh" \
  'run_unit_build_attempt()' \
  "loop wraps each unit build in an attempt boundary"
require_text "$root/adapter/loop.sh" \
  'for fast_attempt in 1 2 3' \
  "loop gives each unit a three-attempt fast-builder budget"
require_text "$root/adapter/loop.sh" \
  'builder-strong' \
  "loop routes exhausted units to a strong-builder escalation"
require_text "$root/adapter/loop.sh" \
  'strong-builder attempt failed for $unit_id' \
  "loop stops for the operator when the strong builder fails"
require_text "$root/adapter/loop.sh" \
  'real execute refuses HYPERCORE_BUILDER_FAKE_DIR' \
  "real execute rejects fake builder sources"
require_text "$root/adapter/loop.sh" \
  'real execute refuses HYPERCORE_CHECK_FAKE_DIR' \
  "real execute rejects fake check sources"
require_text "$root/adapter/loop.sh" \
  'Mechanical check immediately before this reviewer' \
  "tier-one acceptance prompt carries mechanical check evidence"
require_text "$root/adapter/loop.sh" \
  'RATIONALE: the frame-anchored reason for the verdict' \
  "tier-one and tier-two prompts require rationale"
require_text "$root/adapter/loop.sh" \
  'EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict' \
  "tier-one and tier-two prompts require evidence"
require_text "$root/adapter/loop.sh" \
  'cumulative worktree snapshot' \
  "tier-one acceptance prompt explains cumulative diff records"
require_text "$root/adapter/loop.sh" \
  'run_tier_two_panel()' \
  "loop runs the one-way tier-two implementation acceptance panel"
require_text "$root/adapter/loop.sh" \
  'run_tier_two_lens_acceptance()' \
  "loop isolates each tier-two lens in a per-lens worker"
require_text "$root/adapter/loop.sh" \
  'run_tier_two_lens_acceptance "$work_name" "$frame_rel" "$active_rel" "$lens" &' \
  "loop launches tier-two lens workers concurrently"
require_text "$root/adapter/loop.sh" \
  'wait "$pid"' \
  "loop waits for every concurrent tier-two lens"
require_text "$root/adapter/loop.sh" \
  'tier-two panel starting ${#TIER_TWO_PANEL_LENSES[@]} concurrent lenses' \
  "loop records deterministic concurrent panel start events"
require_text "$root/adapter/loop.sh" \
  'tier-two panel all lenses clean' \
  "loop preserves the all-lenses-clean panel gate"
require_text "$root/adapter/loop.sh" \
  'tier_two_lens_instruction()' \
  "loop gives each one-way panel lens a specific acceptance prompt"
require_text "$root/adapter/loop.sh" \
  'lens_instruction="$(tier_two_lens_instruction "$lens")"' \
  "loop threads live tier-two lens instructions inside the panel loop"
require_text "$root/adapter/loop.sh" \
  'For the whole-acceptance-conformance lens' \
  "loop has a whole-acceptance-conformance-specific panel prompt"
require_text "$root/adapter/loop.sh" \
  'For the proof-integrity lens' \
  "loop has a proof-integrity-specific panel prompt"
require_text "$root/adapter/loop.sh" \
  'For the independent-coherence lens' \
  "loop has an independent-coherence-specific panel prompt"
require_text "$root/adapter/loop.sh" \
  'For the security-permissions lens' \
  "loop has a security-permissions-specific panel prompt"
require_text "$root/adapter/loop.sh" \
  'For the red-team lens' \
  "loop has a red-team-specific panel prompt"
require_text "$root/adapter/loop.sh" \
  'required_tier_one_clean_for_panel' \
  "loop guards the one-way panel behind clean unit-level acceptance"
require_text "$root/adapter/loop.sh" \
  'required_tier_one_evidence_clean "tier-two panel"' \
  "loop explains blocked panel ordering when unit-level acceptance is incomplete"
require_text "$root/adapter/loop.sh" \
  'Do not describe prior, future, or expected acceptance artifacts' \
  "loop tells builders not to speculate about acceptance artifacts"
require_text "$root/adapter/loop.sh" \
  'Do not describe prior loop run state' \
  "loop tells builders not to carry stale run-state notes into handoffs"
require_text "$root/adapter/loop.sh" \
  'status --short --untracked-files=no' \
  "loop excludes unrelated untracked files from unit diff status"
require_text "$root/adapter/loop.sh" \
  '"whole-acceptance-conformance"' \
  "loop declares the required one-way panel lenses"
require_text "$root/adapter/loop.sh" \
  'required_acceptance_clean_for_archive' \
  "loop gates archive on clean required acceptance artifacts"
require_text "$root/adapter/loop.sh" \
  'required_tier_one_evidence_clean "archive"' \
  "loop validates tier-one artifacts before real archive"
require_text "$root/adapter/loop.sh" \
  'non-real $artifact_desc acceptance source' \
  "archive validation rejects non-real acceptance sources"
require_text "$root/adapter/loop.sh" \
  'two-way work skips one-way tier-two panel' \
  "loop keeps two-way work out of the one-way panel"
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
  'loop_event acceptance check' \
  "loop records acceptance verdicts in run events"
require_text "$root/adapter/loop.sh" \
  'loop_event archive-decision archive' \
  "loop records the archive decision in run events"
reject_text "$root/adapter/loop.sh" \
  'exec resume --json' \
  "loop no longer resumes one builder thread through phase-two judgement"
require_text "$root/adapter/loop.sh" \
  'print_phase_two_status' \
  "loop status reports phase-two run state"
require_text "$root/adapter/loop.sh" \
  'tier_two_panel=%s cache=%s' \
  "loop status exposes tier-two panel and resumable cache paths"
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
require_text "$root/adapter/loop.sh" \
  'operator_gate_confirm_signoff "$d" "$work_name" "$who"' \
  "loop signoff helper crosses the operator gate"
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
