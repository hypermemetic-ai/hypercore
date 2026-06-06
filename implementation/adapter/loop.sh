#!/usr/bin/env bash
# hypercore loop orchestrator — the Claude Code adapter's rigid workflow.
#
# Drives one change through the loop's five gates (documentation/loop.md), in two phases
# split at the operator's sign-off:
#
#   phase one — orient, frame — is interactive: the operator and the agent frame the
#     change together, and the operator SIGNS OFF. The machine never signs off itself.
#   phase two — implement, check, archive — runs on a CLEARED session: a fresh, memoryless
#     `claude -p` re-derives the work from the written change folder alone. If a blank
#     agent can build it from the frame, the frame was complete.
#
# The gates and their order are the loop, already intent; this script only operationalizes
# them and blocks a gate whose preconditions fail. It states no rule of its own. Where this
# script and the intent disagree, the intent wins.
#
# Usage:
#   loop.sh start    <slug>              scaffold the change folder; print the orient gate
#   loop.sh frame    <slug>              check the frame is complete and ready for sign-off
#   loop.sh signoff  <slug> <operator>   record the operator's sign-off (the human gate)
#   loop.sh execute  <slug> [--dry-run]  run phase two on a cleared session
#   loop.sh status   <slug>              print the change's current phase
#
# Env: CLAUDE_BIN (default: claude), LOOP_BUDGET_USD (optional cap on phase-two spend).

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
GATES="$HERE/gates"
CHANGES="$ROOT/documentation/changes"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"
DRY_RUN="${DRY_RUN:-0}"
FRAME_FILES=(delta.md why.md proof.md endorsement.md plan.md)
GATE_OUTPUT=""   # the last gate's captured output, read by cmd_execute for the sweep verdict

die() { printf 'loop: %s\n' "$1" >&2; exit 1; }

new_uuid() {
  if command -v uuidgen >/dev/null 2>&1; then uuidgen
  else cat /proc/sys/kernel/random/uuid; fi
}

change_dir() { printf '%s/%s' "$CHANGES" "$1"; }

frame_complete() {
  local d f; d="$(change_dir "$1")"
  [ -d "$d" ] || return 1
  for f in "${FRAME_FILES[@]}"; do [ -s "$d/$f" ] || return 1; done
  return 0
}

signed_off() {
  local d; d="$(change_dir "$1")"
  [ -f "$d/endorsement.md" ] && grep -q '^signed-off-by:' "$d/endorsement.md"
}

check_green() { ( cd "$ROOT" && ./implementation/check.sh >/dev/null 2>&1 ); }

phase() {
  [ -d "$CHANGES/archive/$1" ] && { echo done; return; }
  signed_off "$1" && { echo execute; return; }
  echo frame
}

# a single phase-two gate, run on the one cleared session.
# args: <gate-name> <allowed-tools> <session-flag> <session-id> <prompt>
# session-flag is --session-id for the first gate (opens the cleared session) and
# --resume for the rest (continues it), so phase two clears once, then works.
run_gate() {
  local gate="$1" tools="$2" sflag="$3" sid="$4" prompt="$5" sys
  sys="$(cat "$GATES/$gate.md")"
  local -a cmd=(
    "$CLAUDE_BIN" -p
    --output-format json
    --permission-mode acceptEdits
    --allowedTools "$tools"
    --append-system-prompt "$sys"
    "$sflag" "$sid"
    --add-dir "$ROOT"
  )
  [ -n "${LOOP_BUDGET_USD:-}" ] && cmd+=(--max-budget-usd "$LOOP_BUDGET_USD")
  # the prompt goes on stdin, not as a trailing positional: --add-dir is variadic and would
  # otherwise swallow it as another directory, leaving claude -p with no prompt.

  printf '\n--- gate: %s (cleared session %s) ---\n' "$gate" "$sid"
  if [ "$DRY_RUN" = 1 ]; then printf '%q ' "${cmd[@]}"; printf '<<< stdin: %q\n' "$prompt"; return 0; fi
  # capture the gate's output so cmd_execute can read its verdict, still print it for the
  # operator, and still hard-stop on a non-zero gate exit exactly as before.
  GATE_OUTPUT="$(printf '%s' "$prompt" | "${cmd[@]}")" || die "gate $gate failed (claude -p exited non-zero)"
  printf '%s\n' "$GATE_OUTPUT"
}

cmd_start() {
  local slug="${1:-}" d; [ -n "$slug" ] || die "usage: loop.sh start <slug>"
  d="$(change_dir "$slug")"
  if [ ! -d "$d" ]; then
    mkdir -p "$d"
    printf '# delta — %s\n' "$slug" > "$d/delta.md"
    printf '# why — %s\n'   "$slug" > "$d/why.md"
    printf '# proof — %s\n' "$slug" > "$d/proof.md"
    printf '# plan — %s\n'  "$slug" > "$d/plan.md"
    printf '# endorsement — %s\n\n_pending._ The machine does not sign off.\n' "$slug" > "$d/endorsement.md"
    printf 'scaffolded %s\n' "$d"
  fi
  printf '\n=== gate: orient ===\n\n'; cat "$GATES/orient.md"
}

cmd_frame() {
  local slug="${1:-}"; [ -n "$slug" ] || die "usage: loop.sh frame <slug>"
  frame_complete "$slug" || die "frame incomplete — need non-empty: ${FRAME_FILES[*]}"
  check_green || die "check.sh is red — fix before sign-off"
  if signed_off "$slug"; then
    printf 'frame complete and already signed off; next: loop.sh execute %s\n' "$slug"
  else
    printf 'frame complete and check.sh green. Awaiting the operator:\n'
    printf '  loop.sh signoff %s <operator>\n' "$slug"
  fi
}

cmd_signoff() {
  local slug="${1:-}" who="${2:-}"
  { [ -n "$slug" ] && [ -n "$who" ]; } || die "usage: loop.sh signoff <slug> <operator>"
  frame_complete "$slug" || die "cannot sign off an incomplete frame"
  check_green || die "check.sh is red — not signable"
  signed_off "$slug" && die "already signed off"
  printf '\nsigned-off-by: %s\n' "$who" >> "$(change_dir "$slug")/endorsement.md"
  printf 'signed off by %s. The session now clears; phase two re-derives from the frame:\n' "$who"
  printf '  loop.sh execute %s\n' "$slug"
}

cmd_execute() {
  local slug="${1:-}"; [ -n "$slug" ] || die "usage: loop.sh execute <slug> [--dry-run]"
  shift
  [ "${1:-}" = "--dry-run" ] && DRY_RUN=1
  signed_off "$slug" || die "not signed off — phase two is sealed until the operator signs off"

  # the session clears once at sign-off: one fresh id, opened by implement, resumed after.
  local sid; sid="$(new_uuid)"
  printf '=== phase two: cleared session %s, re-deriving %s from its frame ===\n' "$sid" "$slug"

  run_gate implement "Read Edit Write Bash" --session-id "$sid" \
    "Implement change $slug. Read only documentation/changes/$slug/ and the intent it references; build the delta in code."

  printf '\n--- gate: check (mechanical) ---\n'
  if [ "$DRY_RUN" = 1 ]; then
    printf '(dry-run) would run: ./implementation/check.sh\n'
  else
    check_green || die "check.sh red after implement — drift, stopping"
    printf 'check.sh green\n'
  fi
  run_gate check "Read Bash" --resume "$sid" \
    "Run the sweep on the built change $slug against the whole corpus; return coherent (bool) and notes."

  # honor the sweep's flag: read the check gate's verdict sentinel and, when it flags the
  # corpus incoherent — or when no verdict can be read — halt phase two and hand the flag to
  # the operator rather than folding the delta. The sweep flags; the operator (with the proof)
  # settles; no archive decision rests on the sweep itself. Skipped under --dry-run (no output).
  if [ "$DRY_RUN" != 1 ]; then
    case "$GATE_OUTPUT" in
      *"SWEEP_VERDICT: INCOHERENT"*)
        die "sweep flagged the corpus incoherent — phase two stops here for the operator; $slug stays in flight, not archived" ;;
      *"SWEEP_VERDICT: COHERENT"*)
        printf 'sweep verdict: coherent — proceeding to archive\n' ;;
      *)
        die "no readable sweep verdict — phase two stops here for the operator; could not confirm coherence, so $slug stays in flight, not archived" ;;
    esac
  fi

  run_gate archive "Read Edit Write" --resume "$sid" \
    "Archive $slug: fold its delta into the intent documents and stamp each touched segment's foot with the signed-off-by operator."
  printf '\n--- gate: archive (move) ---\n'
  if [ "$DRY_RUN" = 1 ]; then
    printf '(dry-run) would: check.sh green, then git mv documentation/changes/%s documentation/changes/archive/\n' "$slug"
  else
    check_green || die "check.sh red after fold — stopping before archive"
    git -C "$ROOT" mv "documentation/changes/$slug" "documentation/changes/archive/$slug"
    printf 'archived %s\n' "$slug"
  fi
}

cmd_status() {
  local slug="${1:-}"; [ -n "$slug" ] || die "usage: loop.sh status <slug>"
  printf '%s: phase=%s frame_complete=%s signed_off=%s\n' "$slug" "$(phase "$slug")" \
    "$(frame_complete "$slug" && echo yes || echo no)" \
    "$(signed_off "$slug" && echo yes || echo no)"
}

main() {
  local sub="${1:-}"; shift || true
  case "$sub" in
    start)   cmd_start   "$@";;
    frame)   cmd_frame   "$@";;
    signoff) cmd_signoff "$@";;
    execute) cmd_execute "$@";;
    status)  cmd_status  "$@";;
    *) die "usage: loop.sh {start|frame|signoff|execute|status} <slug> [...]";;
  esac
}
main "$@"
