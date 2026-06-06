#!/usr/bin/env bash
# hypercore structural check.
#
# Re-runs the mechanically-checkable statements of the intent against this
# corpus — the root node, and every child node nested under it. A node is any
# directory holding both documentation/ and implementation/; a project is a
# node, so the same checks run at every depth. Each line names the statement it
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

# --- one node: its organizing document, segments, and changes are well-formed ---
check_node() {
  local node=$1 label=$2
  local doc=$node/documentation
  local ms=$doc/machine-statements

  echo "$label — structure"
  [ -f "$doc/organizing-document.md" ] && ok "organizing document exists" \
    || bad "organizing document missing ($doc/organizing-document.md)"

  # segments = intent documents other than the organizing document
  local segs
  segs=$(find "$doc" -maxdepth 1 -name '*.md' ! -name 'organizing-document.md' \
           -printf '%f\n' 2>/dev/null | sed 's/\.md$//' | sort)

  echo "$label — segments"
  local s
  for s in $segs; do
    [ -f "$ms/$s.md" ] \
      && ok "$s has a machine-statements file" \
      || bad "$s has no machine-statements file ($ms/$s.md)"
    grep -q '^## machine' "$doc/$s.md" \
      && ok "$s has a ## machine section" \
      || bad "$s has no ## machine section"
    tail -n 3 "$doc/$s.md" | grep -q '^endorsed by ' \
      && ok "$s is endorsed at its foot" \
      || bad "$s has no foot endorsement"
  done

  echo "$label — changes"
  shopt -s nullglob
  local d f
  for d in "$doc"/changes/*/ "$doc"/changes/archive/*/; do
    [ "$d" = "$doc/changes/archive/" ] && continue   # archive/ is reserved, not a change
    for f in delta.md why.md proof.md endorsement.md plan.md; do
      [ -f "$d$f" ] \
        && ok "$(basename "$d") has $f" \
        || bad "$(basename "$d") missing $f"
    done
  done
}

# --- the methodology node alone must materialize its prose ---
echo "root — methodology"
[ -f "$root/implementation/hypercore.md" ] && ok "implementation/hypercore.md exists" \
  || bad "implementation/hypercore.md missing"

# --- the root node, then every child node nested anywhere beneath it ---
check_node "$root" "root"
while IFS= read -r d; do
  node=$(dirname "$d")
  [ "$node" = "$root" ] && continue            # the root is checked above
  [ -d "$node/implementation" ] || continue    # a node has both trees
  check_node "$node" "${node#"$root"/}"
done < <(find "$root" -type d -name documentation | sort)

echo
if [ $fail -eq 0 ]; then
  echo "all structural statements hold — root and every child node."
else
  echo "drift: a structural check fell."
fi
exit $fail
