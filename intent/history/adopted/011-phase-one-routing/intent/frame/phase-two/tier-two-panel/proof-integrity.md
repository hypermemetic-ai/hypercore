OpenAI Codex v0.137.0
--------
workdir: /home/qqp/projects/hypercore
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ea4ba-ad70-7222-83d0-52a6e034f46e
--------
user
You are the 'proof-integrity' lens of the one-way implementation-acceptance panel for hypercore work node
011-phase-one-routing. The operator (qqp-dev) signed the frame; phase two built the delta;
./check.sh is green. Judge the BUILT RESULT against the SIGNED FRAME through your lens only.
Do not debate other lenses.

Read: the signed frame 011-phase-one-routing/intent/frame/frame.md (acceptance condition,
observable acceptance, excluded interpretation, route) and the built changes via
`git --no-pager diff` plus the current state of the changed contract files
(intent/collaboration.md, intent/loop.md, intent/adapter.md and their machine-statements,
hypercore.md, intent/organizing-document.md) and material (adapter/codex.md, adapter/loop.sh,
check.sh). Intent edits are in the worktree (uncommitted), to be folded at archive.

Return EXACTLY:
VERDICT: PASS
RATIONALE: <frame-anchored reason>
EVIDENCE: <concrete paths / command results / findings>
Use VERDICT: FLAG instead when evidence is missing, stale, uncertain, or mismatched with the
signed frame. Treat uncertainty as FLAG.

Lens focus: Is the proof real, not a no-op? Does contract_statement_product_absence actually discriminate -- do the self-tests prove a forbidden token FAILS and a whitelisted pointer PASSES? Is ./check.sh green for the right reasons? Are the role-presence and held-default assertions genuine, not vacuous?
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
exec
/bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# frame - 011-phase-one-routing

## work

Addressed node: root (`.`).

Node-local work name: 011-phase-one-routing.

Target segments: `collaboration`, `loop`, `adapter` (intent and machine statements each).

Work in flight: this work node only. The root tree is otherwise clean; the `home` child
node has no active work folders. Three untracked sibling findings exist but are not work
nodes and address nothing here: `DECOMPOSITION-FINDINGS.md`, `WORK-NODE-COLLAPSE-FINDINGS.md`,
`TWO-STEP-BUILD-FINDINGS.md`. Two-step is conceptually adjacent (it splits judgeable intent
from implementation-completeness in phase two); the sweep treats it as parallel, not
colliding.

## problem

The methodology's contract names a single harness product — Codex — throughout the
`collaboration`, `loop`, and `adapter` intent, their machine statements, the adapter prose,
and `check.sh`. Two coupled defects follow.

1. The contract conflates *role* with *product*. A statement like "the Codex review roster"
   cannot separate the durable claim "an independent strong review floor exists" from the
   current setting "today that floor is filled by Codex." The `adapter` segment already holds
   the general truth that "an adapter is per harness; one node may be bound by more than one,"
   yet the surrounding contract contradicts it by hardcoding one product.

2. Phase one has no routing contract. Phase two already routes a *builder* role separately
   from the *review floor* (`loop.md`: "phase-two builders may be routed separately from
   reviewers... the fast-builder default is held at the strong model"). Phase one — the
   interactive design phase — names no roles and no config seam, so it cannot say that
   operator-facing judgment and corpus-facing throughput are different work that different
   harnesses may fill, nor that the strong review floor must stay independent of whoever
   framed the work.

The result: the contract cannot state "any capable harness may be the phase-one collaborator"
without contradicting the Codex-named statements around it, and cannot route phase-one labor
the way phase two already routes its builder.

## constraints

- Product-agnostic contract: no operator or machine *statement* in `collaboration`, `loop`,
  or `adapter` names a specific harness product — including config-knob identifiers that embed
  a product name. Statements describe config seams by role (a builder-model knob, a
  review-model knob, a collaborator-routing knob); a literal product-bearing identifier such
  as `CODEX_BUILDER_MODEL` is materialization, named only in `adapter/loop.sh` and `check.sh`,
  never in a contract statement.
- Three layers, not two. The de-naming sorts every product-named statement into: (a) a
  **methodology claim** (e.g. "an independent strong review floor exists") → role/config
  language; (b) a **capability requirement** — a statement that names a product today only
  because it encodes a behavioral assumption (entry-point loading, instruction-chain
  inheritance, structured exec-event streaming, cleared session-state preflight) → rephrased as
  "the harness must support X", product-agnostic but not overgeneralized to "any harness can";
  or (c) a **current-binding fact** → materialization, which stays product-named.
- Materialization stays product-specific: the adapter prose (`adapter/codex.md`), the harness
  entry point (`AGENTS.md`), the orchestrator's actual harness calls in `adapter/loop.sh`,
  config-knob *values*, and a designated current-binding section legitimately name the current
  binding. De-name the claims, not the mechanism.
- Preserve the proof floor: routing never demotes the review floor or acceptance tiers below
  current behavior, and the phase-one collaborator that frames a one-way work node must not be
  the review floor that scrutinizes it — the framer is not its own witness. (Today the review
  floor rides an ambient harness default rather than a checked, pinned strong model; whether
  011 pins a checked strong-review default or records the unpinned floor as debt is a route
  decision named below.)
- Preserve the five gates and the sign-off split: phase one interactive, phase two
  re-derives from the signed frame alone. No new gates.
- Preserve fastness: two-way work keeps skipping review and the panel.
- Hold defaults, strand nothing: every newly named role or config slot carries a held default
  that reproduces current behavior, mirroring how builder routing landed.
- Do not rewrite adopted history. Change only current corpus.
- Keep `./check.sh` green throughout, and make it prove both the product-name absence in the
  contract and the presence of the new role/config seams and held defaults.

## decision surface or open direction

Framing and scope are settled through operator deliberation, to be anchored by `./direction`:
a product-agnostic role/config contract that de-names the whole adapter contract. Statements
always describe config seams by role; the one genuine remaining fork is whether the *material*
config-knob identifiers (`CODEX_*` in `adapter/loop.sh`) are also neutralized. See
`intent/frame/options.md`. If the full scope cannot land coherently in one node, the work
shelves and re-frames smaller rather than weakening this acceptance condition.

Two route deliverables are load-bearing and must be made exact when the route is written: the
materialization-pointer grammar (so the product-absence check has no false positives on
legitimate pointers and no loophole), and the review-floor decision (pin a checked
strong-review default, or preserve current behavior and record the unpinned floor as debt).

Reversibility: one-way

## route

Adopt Option 1 (`contract-only-denaming`; `direction-by: qqp-dev`, `operator-gate: tty`):
de-name the whole harness-binding contract to role and capability terms, keep the
materialization product-specific including the `CODEX_*` knob identifiers, and add the
product-agnostic phase-one collaborator and review-floor roles.

### the three-layer sort

Every product-named line in a contract statement file is sorted into one of:

- **methodology claim** → rewritten in role/config language ("the Codex review roster" → "the
  review roster");
- **capability requirement** → rewritten as "the harness must support X", product-agnostic but
  not overgeneralized to "any harness" ("the Codex harness loads its adapter through a root
  `AGENTS.md`" → "the harness loads its adapter from a root entry point it reads at session
  start", with the concrete entry point named only in materialization);
- **current-binding fact** → moved into the materialization (`adapter/codex.md` prose,
  `adapter/loop.sh`, `check.sh`) and out of the statement files, leaving statements that point
  at the materialization by path only.

### the materialization-pointer grammar (this defines the check)

In a contract statement file, a harness-product token may appear ONLY inside a backtick-fenced
span whose content is a whitelisted materialization pointer: the binding paths `adapter/codex.md`,
`AGENTS.md`, `adapter/codex-mounted.md`, and the orchestrator path `adapter/loop.sh`. The scanned
product-token set (case-insensitive) is `codex`, `claude`, `opus`, `gpt-<n>`, and the knob
prefix `CODEX_`. A token outside a whitelisted fenced pointer fails. Knob identifiers
(`CODEX_BUILDER_MODEL`, `CODEX_STRONG_BUILDER_MODEL`, `CODEX_REVIEW_MODEL`, `CODEX_REVIEW_EFFORT`)
live only in `adapter/loop.sh` and `check.sh`; statements name them by role (the builder-model
knob, the strong-builder knob, the review-model knob, the review-effort knob). Out of scope, not
scanned: adopted/shelved history, scratch findings, child-node names (`codex-cockpit`), and the
mounted entry point itself; for `hypercore.md` and `intent/organizing-document.md` only the
adapter description is scanned, so the `home`/governed-work text naming `codex-cockpit` is
untouched.

### phase-one roles and routing seam (product-agnostic statements)

- `collaboration`: phase one decomposes into operator-facing judgment, owned by the
  **collaborator**, and corpus-facing throughput (research, the orient corpus read, the sweep
  map), which the collaborator may delegate; the collaborator is the harness that drives orient
  and frame.
- `collaboration`/`loop`: the **strong review floor** that scrutinizes a one-way frame is
  independent of the collaborator that framed it — the framer is not its own witness —
  generalizing the existing "the builder is not the witness of its own archive".
- `loop` (sibling to the existing phase-two builder-routing statement): phase-one labor is
  routable — the collaborator harness may differ from the phase-two executor harness, and
  breadth work may be delegated — while the review floor and acceptance tiers stay on the strong
  route.
- `adapter`: an adapter binds a harness to a phase; phase one and phase two may bind different
  harnesses (the standing "an adapter is per harness" already permits this); the current
  materialization binds one harness to both phases.
- Held defaults: the existing review-model and builder-model knobs are described by role with
  their current held defaults preserved (review/acceptance on the strong route; builder held at
  the strong model until two-step lands). The collaborator role defaults to the interactive
  harness that loads the adapter. No new orchestrator env knob is required: phase one is the
  interactive design phase and the orchestrator does not drive it.

### review-floor settlement (machine settlement of a delegated open choice)

The operator delegated the review-floor decision. Settled as **debt, not pin**: 011 preserves
current behavior and records as debt that the strong review floor is not yet mechanically pinned
to a checked strong model (it can ride an ambient harness default). The de-named statements
preserve the existing strong-floor intent without adding a proof 011 does not deliver; a future
loop pins a checked strong-review default.

### parent intent amendments

- `collaboration` (+ machine statements): de-name the review-roster and acceptance statements;
  add the collaborator/throughput partition and the review-floor-independent-of-collaborator
  statement.
- `loop` (+ machine statements): de-name builder-session, exec, and knob-identifier wording to
  role/capability terms; add the phase-one routing statement as a sibling to the phase-two
  builder-routing line.
- `adapter` (+ machine statements): the largest delta — sort every product-named statement
  through the three layers, move current-binding behavioral facts into `adapter/codex.md`, keep
  only whitelisted path pointers in statements, and add the per-phase binding statement.

### material amendments

- `hypercore.md`: de-name the adapter section to role/pointer language.
- `intent/organizing-document.md`: de-name the adapter bullet, leaving the `home`/`codex-cockpit`
  text untouched.
- `adapter/codex.md`: receives the current-binding behavioral facts moved out of the statements;
  stays the product-named materialization. Records two debts: the unpinned strong review floor,
  and the phase-one review reviewer prompt that assumes a signed route-settled frame and so
  cannot PASS a correctly-staged pre-direction frame.
- `adapter/loop.sh`: no behavior change; de-name only comments that restate contract; `CODEX_*`
  knob identifiers unchanged (Option 1).
- `check.sh`: add the product-absence check (the grammar above) over the enumerated statement
  files; assert the collaborator, throughput-delegation, review-floor-independence, and
  phase-one-routing statements are present; assert held defaults reproduce current routing when
  the knobs are unset. Self-tests: an unwhitelisted product token in a statement file FAILS; a
  whitelisted fenced pointer PASSES; a `codex-cockpit` mention in the home text PASSES; the new
  role statements are present.

Implementation units for phase two:

1. De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep
   so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md`
   and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and
   `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role;
   capability → "the harness must support X"; current-binding fact → moved into
   `adapter/codex.md`); add the collaborator, throughput-delegation,
   review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh`
   to drop assertions that require the old product-named wording and add the scoped
   product-absence check with the pointer grammar, the role-statement-presence assertions, and
   the held-default assertions. `./check.sh` is green at the unit boundary.
2. Add the `check.sh` self-tests for the grammar (an unwhitelisted product token in a statement
   file fails; a whitelisted fenced pointer passes; a `codex-cockpit` home-text mention passes;
   the role statements are present) and a held-defaults-reproduce-current-routing test; record
   the two debts in `adapter/codex.md` (the unpinned strong review floor; the phase-one review
   reviewer-prompt mismatch); and de-name any contract-restating comments in `adapter/loop.sh`.
   `./check.sh` is green at the unit boundary.

## acceptance condition

After adoption: the `collaboration`/`loop`/`adapter` contract (intent and machine statements),
the adapter prose, and `check.sh` express the harness binding in role and config terms with no
harness product named in any *statement*; a phase-one *collaborator* role and a phase-one
routing/delegation seam exist with held defaults that reproduce current behavior; the strong
review floor's independence from the framer is stated; and `./check.sh` is green.

## observable acceptance

- `./check.sh` exits zero after implementation and after the archive fold.
- A check asserts that no contract *statement* file — the enumerated set
  `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md`, their `machine-statements/`
  counterparts, and the adapter sections of `hypercore.md` and `intent/organizing-document.md`
  — contains a harness-product token (product names and product-bearing knob identifiers alike)
  except inside an exactly specified materialization-pointer grammar (a whitelisted fenced path
  reference such as `adapter/codex.md` or `AGENTS.md`, or a designated current-binding section).
  The check is scoped to those files only: adopted history, scratch findings, child-node names
  (e.g. `codex-cockpit`), and mounted-entrypoint material are out of scope. Capability-requirement
  statements pass because they name a required capability, not a product. The exact grammar and
  token set are fixed in the route.
- The contract names a phase-one collaborator role and a phase-one routing/delegation seam,
  each with a held default.
- A check asserts the "review floor independent of the framer" statement is present.
- The materialization still binds the current harness and still executes phase two:
  `adapter/codex.md` and `AGENTS.md` remain, and `adapter/loop.sh` still runs the executor.

## excluded interpretation

- Not a second phase-two executor. This introduces no new execution or build path; unlike the
  retired `001-remove-claude-adapter` Claude binding, phase two stays on the existing executor.
- Not a demotion of the proof floor. Routing never makes review or acceptance cheaper, and
  never lets the framer review its own work.
- Not a rename or removal of materialization. `adapter/loop.sh` still calls the executor;

exec
/bin/bash -lc 'git --no-pager diff --stat' in /home/qqp/projects/hypercore
 succeeded in 0ms:
 adapter/codex.md                           |  23 +++
 adapter/loop.sh                            |   2 +-
 check.sh                                   | 216 +++++++++++++++++++++++++++++
 hypercore.md                               |   4 +-
 intent/adapter.md                          |  55 ++++----
 intent/collaboration.md                    |   9 +-
 intent/loop.md                             |  28 ++--
 intent/machine-statements/adapter.md       |  36 ++---
 intent/machine-statements/collaboration.md |   2 +-
 intent/machine-statements/loop.md          |  24 ++--
 intent/organizing-document.md              |   4 +-
 11 files changed, 332 insertions(+), 71 deletions(-)

exec
/bin/bash -lc 'git --no-pager diff' in /home/qqp/projects/hypercore
 succeeded in 0ms:
diff --git a/adapter/codex.md b/adapter/codex.md
index f71f4cd..e0a8a53 100644
--- a/adapter/codex.md
+++ b/adapter/codex.md
@@ -15,6 +15,23 @@ intent and run the loop, not because you chose to, but because the workflow make
 gates unskippable. Pointing alone is a request; the orchestrator is how agreement is
 kept.
 
+## Current Harness Binding
+
+The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
+`adapter/codex.md`; it is the harness-mandated pointer and not where the adapter lives.
+Nested work under this root receives that entry point through the project instruction
+chain, so nested nodes do not carry their own adapter material.
+
+The current materialization binds Codex to both phase one and phase two. Phase one defaults
+to the interactive Codex harness that loaded this adapter. Phase two is driven by
+`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
+the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
+ids as current binding facts.
+
+The current materialization also keeps the `CODEX_*` environment knob names in
+`adapter/loop.sh`. Those names are implementation binding, while the intent states the
+builder-model, strong-builder, review-model, and review-effort roles.
+
 ## Orient before you touch anything
 
 First classify the request surface. Ordinary conversation, explanation, and read-only
@@ -113,6 +130,12 @@ as a checked statement, then dropped.
   empty node — not a fake app with invented sub-projects.
 - **Name in hypercore's own vocabulary** — node, segment, contract, mount, materialize,
   the loop. Reject domain words that collide with the methodology's own concepts.
+- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
+  to a checked strong model; it can still ride an ambient harness default. A future loop
+  pins it.
+- **Re-prompt phase-one one-way review.** The current phase-one one-way review reviewer
+  prompt assumes a signed, route-settled frame and therefore cannot PASS a correctly staged
+  pre-direction frame. A future loop re-prompts it for a pre-direction decision surface.
 
 ---
 This adapter is itself governed: the `adapter` segment is its intent, and the sweep reads
diff --git a/adapter/loop.sh b/adapter/loop.sh
index c20c43f..085604b 100755
--- a/adapter/loop.sh
+++ b/adapter/loop.sh
@@ -2792,7 +2792,7 @@ run_codex_gate() {
   printf '%s\n' "$GATE_OUTPUT"
 }
 
-# a single fresh phase-two Codex session.
+# a single fresh phase-two executor session.
 # args: <gate-name> <allowed-tools> <mode> <session-id> <prompt> [instruction-gate]
 # mode is start; every phase-two builder, acceptance reviewer, and archive actor is fresh.
 run_gate() {
diff --git a/check.sh b/check.sh
index 1f39843..51bffa5 100755
--- a/check.sh
+++ b/check.sh
@@ -68,6 +68,172 @@ reject_regular_file() {
   fi
 }
 
+contract_statement_product_absence_errors() {
+  local file=$1 scope=$2
+  HYPERCORE_CONTRACT_SCOPE="$scope" perl -0ne '
+    my $scope = $ENV{HYPERCORE_CONTRACT_SCOPE} || "all";
+    my $text = $_;
+
+    if ($scope eq "hypercore-adapter") {
+      if ($text =~ /^## adapter\n(.*?)(?=^## |\z)/ms) {
+        $text = $1;
+      } else {
+        print "$ARGV: missing ## adapter section\n";
+        exit 1;
+      }
+    } elsif ($scope eq "organizing-adapter") {
+      my @kept;
+      my $taking = 0;
+      for my $line (split /\n/, $text) {
+        if ($line =~ /^- \*\*adapter\*\*/) {
+          $taking = 1;
+        } elsif ($taking && $line =~ /^\s*$/) {
+          last;
+        }
+        push @kept, $line if $taking;
+      }
+      if (!@kept) {
+        print "$ARGV: missing adapter bullet\n";
+        exit 1;
+      }
+      $text = join("\n", @kept) . "\n";
+    }
+
+    my %allowed = map { $_ => 1 } (
+      "adapter/codex.md",
+      "AGENTS.md",
+      "adapter/codex-mounted.md",
+      "adapter/loop.sh",
+    );
+    my @spans;
+    while ($text =~ /`([^`\n]+)`/g) {
+      push @spans, [$-[1], $+[1], $1];
+    }
+
+    my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
+    while ($text =~ /$product/g) {
+      my ($start, $end, $token) = ($-[0], $+[0], $&);
+      my $ok = 0;
+      for my $span (@spans) {
+        if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) {
+          $ok = 1;
+          last;
+        }
+      }
+      next if $ok;
+      my $prefix = substr($text, 0, $start);
+      my $line = 1 + ($prefix =~ tr/\n//);
+      print "$ARGV:$line: product token \"$token\" is outside a whitelisted materialization pointer\n";
+      exit 1;
+    }
+  ' "$file"
+}
+
+contract_statement_product_absence() {
+  local file=$1 scope=$2 label=$3 output status
+  output="$(contract_statement_product_absence_errors "$file" "$scope" 2>&1)"
+  status=$?
+  if [ $status -eq 0 ]; then
+    ok "$label"
+  else
+    bad "$label ($output)"
+  fi
+  return $status
+}
+
+check_contract_statement_product_absence_self_tests() {
+  local tmp forbidden pointer organizing
+
+  echo "root - contract statement product grammar self-test"
+  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-contract-product-check.XXXXXX")" \
+    || { bad "contract product grammar self-test can create temporary space"; return; }
+
+  forbidden="$tmp/forbidden.md"
+  cat > "$forbidden" <<'EOF'
+# fixture
+
+the Codex review floor is named in a contract statement.
+EOF
+  if ( fail=0; contract_statement_product_absence "$forbidden" all \
+    "forbidden product token fixture" >"$tmp/forbidden.out" 2>&1 ); then
+    bad "contract product grammar rejects an unwhitelisted harness-product token"
+  else
+    ok "contract product grammar rejects an unwhitelisted harness-product token"
+  fi
+  require_text "$tmp/forbidden.out" \
+    'product token "Codex" is outside a whitelisted materialization pointer' \
+    "contract product grammar failure names the forbidden token"
+
+  pointer="$tmp/pointer.md"
+  cat > "$pointer" <<'EOF'
+# fixture
+
+the current root harness adapter is materialized as `adapter/codex.md`.
+EOF
+  if ( fail=0; contract_statement_product_absence "$pointer" all \
+    "whitelisted materialization pointer fixture" >"$tmp/pointer.out" 2>&1 ); then
+    ok "contract product grammar accepts a whitelisted materialization pointer"
+  else
+    bad "contract product grammar accepts a whitelisted materialization pointer"
+  fi
+
+  organizing="$tmp/organizing-document.md"
+  cat > "$organizing" <<'EOF'
+# organizing document
+
+- **adapter** -- the binding between a harness and the loop, materialized through `adapter/codex.md`.
+
+The **governed work** -- durable child nodes and mounted work under this root:
+
+- **home** -- home currently mounts codex-cockpit.
+EOF
+  if ( fail=0; contract_statement_product_absence "$organizing" organizing-adapter \
+    "out-of-scope governed-work product mention fixture" >"$tmp/organizing.out" 2>&1 ); then
+    ok "contract product grammar ignores out-of-scope governed-work child-node names"
+  else
+    bad "contract product grammar ignores out-of-scope governed-work child-node names"
+  fi
+
+  require_text "$root/intent/collaboration.md" \
+    "the phase-one collaborator is the harness role that drives orient and frame" \
+    "phase-one routing self-test sees the collaborator role assertion"
+  require_text "$root/intent/collaboration.md" \
+    "phase-one corpus-throughput work" \
+    "phase-one routing self-test sees the throughput-delegation assertion"
+  require_text "$root/intent/collaboration.md" \
+    "the framer is not its own witness" \
+    "phase-one routing self-test sees the independent-review-floor assertion"
+  require_text "$root/intent/loop.md" \
+    "phase-one labor may be routed by role" \
+    "phase-one routing self-test sees the phase-one routing assertion"
+  require_text "$root/intent/loop.md" \
+    "the collaborator role defaults to the interactive harness that loaded the adapter" \
+    "phase-one routing self-test sees the collaborator held default"
+  require_text "$root/intent/loop.md" \
+    "the fast-builder default is held at the strong model" \
+    "phase-one routing self-test sees the builder held default"
+  require_text "$root/intent/loop.md" \
+    "phase-one review stay on the" \
+    "phase-one routing self-test sees the review-floor held default"
+  require_text "$root/intent/adapter.md" \
+    "the phase-one collaborator role defaults to the interactive harness" \
+    "phase-one routing self-test sees the adapter collaborator default"
+  require_text "$root/adapter/codex.md" \
+    "to the interactive Codex harness that loaded this adapter" \
+    "phase-one routing self-test sees the current binding collaborator default"
+  require_text "$root/adapter/loop.sh" \
+    'CODEX_REVIEW_EFFORT:-xhigh' \
+    "phase-one routing self-test sees the review-effort held default"
+  require_text "$root/adapter/loop.sh" \
+    'CODEX_BUILDER_MODEL:-gpt-5.5' \
+    "phase-one routing self-test sees the builder-model held default"
+  require_text "$root/adapter/loop.sh" \
+    'CODEX_BUILDER_EFFORT:-xhigh' \
+    "phase-one routing self-test sees the builder-effort held default"
+
+  rm -rf "$tmp"
+}
+
 shopt -s nullglob
 HOME_GREENFIELD_CHECK_TMP=
 HOME_GREENFIELD_CHECK_MOUNT=
@@ -1696,6 +1862,56 @@ require_text "$root/intent/loop.md" \
 require_text "$root/intent/adapter.md" \
   "resumable per-unit execute cache" \
   "adapter segment folds resumable execute materialization"
+require_text "$root/intent/collaboration.md" \
+  "the phase-one collaborator is the harness role that drives orient and frame" \
+  "collaboration segment names the phase-one collaborator role"
+require_text "$root/intent/collaboration.md" \
+  "phase-one corpus-throughput work" \
+  "collaboration segment allows delegated phase-one throughput"
+require_text "$root/intent/collaboration.md" \
+  "the framer is not its own witness" \
+  "collaboration segment keeps the review floor independent of the framer"
+require_text "$root/intent/loop.md" \
+  "phase-one labor may be routed by role" \
+  "loop segment carries phase-one routing"
+require_text "$root/intent/loop.md" \
+  "the collaborator role defaults to the interactive harness that loaded the adapter" \
+  "loop segment holds the collaborator default"
+require_text "$root/intent/loop.md" \
+  "the fast-builder default is held at the strong model" \
+  "loop segment holds the builder default"
+require_text "$root/intent/loop.md" \
+  "phase-one review stay on the" \
+  "loop segment holds the strong review floor"
+require_text "$root/intent/adapter.md" \
+  "an adapter binds a harness to a phase" \
+  "adapter segment permits per-phase harness binding"
+require_text "$root/intent/adapter.md" \
+  "the phase-one collaborator role defaults to the interactive harness" \
+  "adapter segment holds the collaborator materialization default"
+require_text "$root/adapter/codex.md" \
+  "to the interactive Codex harness that loaded this adapter" \
+  "current binding records the collaborator held default"
+require_text "$root/adapter/codex.md" \
+  "builder-model, strong-builder, review-model, and review-effort roles" \
+  "current binding separates material knob names from role statements"
+contract_statement_product_absence "$root/intent/collaboration.md" all \
+  "collaboration intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/loop.md" all \
+  "loop intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/adapter.md" all \
+  "adapter intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/collaboration.md" all \
+  "collaboration machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/loop.md" all \
+  "loop machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/adapter.md" all \
+  "adapter machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/hypercore.md" hypercore-adapter \
+  "hypercore adapter section has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/organizing-document.md" organizing-adapter \
+  "organizing adapter bullet has no unscoped harness product token"
+check_contract_statement_product_absence_self_tests
 [ -x "$root/check.sh" ] \
   && ok "check.sh exists and is executable" \
   || bad "check.sh is missing or not executable"
diff --git a/hypercore.md b/hypercore.md
index 9db8bab..530d5a5 100644
--- a/hypercore.md
+++ b/hypercore.md
@@ -256,8 +256,8 @@ The adapter binds a harness to the methodology.
 harness loads adapter -> adapter points to intent + loop -> gates become enforceable
 ```
 
-For Codex, the root `AGENTS.md` points at the adapter. The adapter does not replace the
-intent; it routes the machine to the intent and makes the loop's gates rigid.
+For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
+replace the intent; it routes the machine to the intent and makes the loop's gates rigid.
 
 Phase one is interactive design work. Phase two is cleared, heads-down execution from the
 signed frame. If a gate precondition fails, the adapter blocks instead of warning.
diff --git a/intent/adapter.md b/intent/adapter.md
index d7bda9c..97528c2 100644
--- a/intent/adapter.md
+++ b/intent/adapter.md
@@ -19,23 +19,22 @@ a decision surface for substantive operator direction; after sign-off, implement
 and archive run through cleared sessions that re-derive each unit and acceptance review
 from the signed frame directory and lean phase-two handoff artifacts alone.
 direction and review are phase-one acts or artifacts, not loop gates.
-the Codex review roster for one-way phase-one work has a base roster of
+the review roster for one-way phase-one work has a base roster of
 `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
-the Codex implementation-acceptance reviewer for each phase-two unit is independent and
-read-only.
-the Codex tier-two implementation-acceptance panel for one-way work has required lenses
+the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
+the tier-two implementation-acceptance panel for one-way work has required lenses
 `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
 `security-permissions`, and `red-team`.
-the complete optional Codex review roster is `implementation-maintainability`,
+the complete optional review roster is `implementation-maintainability`,
 `security-permissions`, `operator-ergonomics`, `migration-compatibility`,
 `domain-evidence`, and `performance-cost`.
 optional reviewers are advisory additions and cannot override, outvote, average away, or
 dilute unresolved base-roster or red-team flags.
-the Codex adapter classifies the request surface before changing material: ordinary
+the adapter classifies the request surface before changing material: ordinary
 conversation and read-only inspection may proceed directly, while governed work starts or
 continues a work node.
-the Codex adapter rejects perceived simplicity, file count, convenience, and low risk as
-waivers for governed work.
+the adapter rejects perceived simplicity, file count, convenience, and low risk as waivers
+for governed work.
 on request the adapter renders a statement of the intent intelligible in plain language
 without altering it.
 the adapter carries only what the intent cannot yet reach the harness with -- the order to
@@ -43,6 +42,10 @@ read the intent first, and disciplines not yet written as statements; each is a
 folded into the intent by later work and then dropped.
 an adapter is per harness; one node may be bound by more than one, each loaded by its own
 harness.
+an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
+and the current materialization binds one harness to both phases.
+the phase-one collaborator role defaults to the interactive harness that loaded the
+adapter; no orchestrator routing knob is required until a materialization routes that role.
 the adapter material is materialized only at the methodology root, with the prose it routes
 to, and not in any nested node; a mounted external project may carry a target-local entry
 point that links to root-managed adapter material and routes direct-path work back to the
@@ -54,27 +57,29 @@ the intent has since absorbed, is caught as drift.
 
 ## machine
 the current root harness adapter is materialized as `adapter/codex.md`.
-the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
-`adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
-where the adapter lives.
-a machine working in a nested node under the root is bound by Codex including the root
-`AGENTS.md` in the project instruction chain from the project root to the current
-directory, so no node below the root carries its own adapter material.
+the current materialization binds the same harness to phase one and phase two; the
+phase-one collaborator is the interactive harness that loaded the adapter.
+the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
+the root entry is the harness's mandated pointer, holding nothing, not where the adapter
+lives.
+a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
+project instruction chain from the project root to the current directory, so no node below
+the root carries its own adapter material.
 a mounted external project may carry a target-local `AGENTS.md` entry point for
 direct-path openings; the entry point links to root-managed adapter material and routes
 back to the root adapter and loop instead of copying root adapter material into the
 mounted node.
 the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
-over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
-builder session from the signed frame, and acceptance reviewers and the archive actor are
-fresh sessions rather than resumes of the builder.
-the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
-`.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
+over the phase-two executor harness: each implementation unit opens a fresh builder
+session from the signed frame, and acceptance reviewers and the archive actor are fresh
+sessions rather than resumes of the builder.
+the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
+`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
 final outputs, acceptance artifact paths, and current pointers for the addressed work and
 root.
-the Codex loop streams inner `codex exec --json` events into the phase-two run state while
+the loop streams inner executor JSON events into the phase-two run state while
 printing concise progress, without changing the cleared-session contract.
-the Codex loop materializes separate builder and reviewer routing, structured acceptance
+the loop materializes separate builder and reviewer routing, structured acceptance
 artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
 then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
 one-way tier-two panel, and phase-one review subprocess crash diagnostics.
@@ -105,10 +110,10 @@ framing and requires `intent/frame/review.md` for one-way work.
 the frame gate prompt tells the machine not to write operator direction, not to collect
 direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
 red-team flags.
-the Codex adapter prose describes phase one as design-phase collaboration with direction
+the adapter prose describes phase one as design-phase collaboration with direction
 and review artifacts, while preserving phase two as cleared, heads-down execution from the
 signed frame directory and lean phase-two handoff artifacts.
-`check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
+`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
 validation, start scaffolding, direction/review helpers, operator-act gating through
 `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
 acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
@@ -117,8 +122,8 @@ builder/reviewer routing with bounded retry and strong escalation, resumable exe
 caching, the concurrent tier-two panel, the new operator-act and phase-two performance
 contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
 absence of the retired compatibility route still carry the contract.
-each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
-the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
+each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
+them in the executor gate prompt; the orchestrator owns gate order and preconditions and
 blocks a gate whose preconditions fail.
 sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
 in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
diff --git a/intent/collaboration.md b/intent/collaboration.md
index 83ab76a..49db957 100644
--- a/intent/collaboration.md
+++ b/intent/collaboration.md
@@ -5,10 +5,17 @@ collaboration is the working relation by which operator and machine keep the wor
 effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
 collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
 phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
+the phase-one collaborator is the harness role that drives orient and frame: it carries
+operator-facing judgment, surfaces understanding and options, and frames the signed route.
+phase-one corpus-throughput work -- research, the orient corpus read, and the sweep map --
+may be delegated by the collaborator when written ground preserves accountability and
+operator direction.
 before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
 one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
 the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
 optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
+for one-way work, the strong review floor that scrutinizes a frame is independent of the
+collaborator that framed it; the framer is not its own witness.
 review quality is not proved by artifact scanning; review artifacts record structured signal, unresolved flags, and disposition.
 direction and sign-off are the two anchored operator acts in phase one, and the machine performs neither for itself.
 operator direction is substantive: it records a selected route, constraint, or explicit delegation with `direction-by:`.
@@ -29,7 +36,7 @@ collaboration degrades gracefully: when written ground is insufficient, the mach
 
 ## machine
 phase-two handoff state is written as common ground for the operator and later tooling:
-the addressed work's current or recent gate, current unit, status, Codex thread id, latest
+the addressed work's current or recent gate, current unit, status, harness session id, latest
 message, failure reason, event history, run artifact paths, and phase-two acceptance
 artifact paths are recoverable from loop state files.
 
diff --git a/intent/loop.md b/intent/loop.md
index 08d4577..8bd5109 100644
--- a/intent/loop.md
+++ b/intent/loop.md
@@ -60,6 +60,10 @@ acceptance reviewer output counts as `FLAG`.
 acceptance artifacts record their source as real reviewer, dry-run/self-test, or
 fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
 fake-source required acceptance.
+phase-one labor may be routed by role: the collaborator drives operator-facing orient and
+frame work, corpus-throughput work may be delegated, and the collaborator may differ from
+the phase-two executor harness while phase-one review stays on the strong review floor.
+the collaborator role defaults to the interactive harness that loaded the adapter.
 phase-two builders may be routed separately from reviewers through a fast-builder model
 knob, while tier-one acceptance, tier-two acceptance, and phase-one review stay on the
 strong review floor; the fast-builder default is held at the strong model until the
@@ -104,11 +108,12 @@ corpus.
 `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
 act only on that addressed work.
 `loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
-runs and after recent failure or completion, including the active gate, status, Codex
-thread id, latest message, event history, and run artifact paths.
-before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
-the Codex binary is present and that Codex home/session state is writable; a failed
-preflight records failed run state and stops before `codex exec`.
+runs and after recent failure or completion, including the active gate, status, harness
+session id, latest message, event history, and run artifact paths.
+before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
+that the configured executor binary is present and that executor home/session state is
+writable; a failed preflight records failed run state and stops before the executor
+session starts.
 `loop.sh status <work-name>` reports the addressed work's current phase and, for
 non-historical work with phase-two state, the current or recent run's gate, status, state
 path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
@@ -163,12 +168,13 @@ optional reviewer verdicts cannot clear unresolved base-roster or red-team flags
 new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
 the work node's `intent/frame/signoff.md`.
 `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
-fresh Codex builder session for each unit, and records lean unit handoff, diff, and
-tier-one verdict artifacts under the work frame.
-`loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
-the strong model until the two-step plan/build work lands, separately from the strong review
-route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
-to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
+fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
+verdict artifacts under the work frame.
+`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
+the strong model until the two-step plan/build work lands, separately from the strong
+review route; it gives each unit a three-attempt fast-builder budget, escalates an
+exhausted unit through the strong-builder model knob, and stops for the operator when the
+strong builder fails.
 `loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
 approval `never` and literal sandbox `read-only`.
 `loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
diff --git a/intent/machine-statements/adapter.md b/intent/machine-statements/adapter.md
index 7a704b0..fddc96b 100644
--- a/intent/machine-statements/adapter.md
+++ b/intent/machine-statements/adapter.md
@@ -1,27 +1,29 @@
 # adapter -- machine statements
 
 the current root harness adapter is materialized as `adapter/codex.md`.
-the Codex harness loads its adapter through a root `AGENTS.md` symlinked to
-`adapter/codex.md`; the root entry is the harness's mandated pointer, holding nothing, not
-where the adapter lives.
-a machine working in a nested node under the root is bound by Codex including the root
-`AGENTS.md` in the project instruction chain from the project root to the current
-directory, so no node below the root carries its own adapter material.
+the current materialization binds the same harness to phase one and phase two; the
+phase-one collaborator is the interactive harness that loaded the adapter.
+the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
+the root entry is the harness's mandated pointer, holding nothing, not where the adapter
+lives.
+a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
+project instruction chain from the project root to the current directory, so no node below
+the root carries its own adapter material.
 a mounted external project may carry a target-local `AGENTS.md` entry point for
 direct-path openings; the entry point links to root-managed adapter material and routes
 back to the root adapter and loop instead of copying root adapter material into the
 mounted node.
 the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
-over the Codex phase-two harness: each implementation unit opens a fresh `codex exec`
-builder session from the signed frame, and acceptance reviewers and the archive actor are
-fresh sessions rather than resumes of the builder.
-the Codex loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
-`.hypercore/loop-runs`, with run-local state, event history, raw Codex gate streams, gate
+over the phase-two executor harness: each implementation unit opens a fresh builder
+session from the signed frame, and acceptance reviewers and the archive actor are fresh
+sessions rather than resumes of the builder.
+the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
+`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
 final outputs, acceptance artifact paths, and current pointers for the addressed work and
 root.
-the Codex loop streams inner `codex exec --json` events into the phase-two run state while
+the loop streams inner executor JSON events into the phase-two run state while
 printing concise progress, without changing the cleared-session contract.
-the Codex loop materializes separate builder and reviewer routing, structured acceptance
+the loop materializes separate builder and reviewer routing, structured acceptance
 artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
 then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
 one-way tier-two panel, and phase-one review subprocess crash diagnostics.
@@ -52,10 +54,10 @@ framing and requires `intent/frame/review.md` for one-way work.
 the frame gate prompt tells the machine not to write operator direction, not to collect
 direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
 red-team flags.
-the Codex adapter prose describes phase one as design-phase collaboration with direction
+the adapter prose describes phase one as design-phase collaboration with direction
 and review artifacts, while preserving phase two as cleared, heads-down execution from the
 signed frame directory and lean phase-two handoff artifacts.
-`check.sh` mechanically checks that the gate prompts, Codex adapter prose, loop frame
+`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
 validation, start scaffolding, direction/review helpers, operator-act gating through
 `/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
 acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
@@ -64,8 +66,8 @@ builder/reviewer routing with bounded retry and strong escalation, resumable exe
 caching, the concurrent tier-two panel, the new operator-act and phase-two performance
 contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
 absence of the retired compatibility route still carry the contract.
-each gate's instructions are held in a file in `adapter/gates/`; the Codex path includes them in
-the `codex exec` gate prompt; the orchestrator owns gate order and preconditions and
+each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
+them in the executor gate prompt; the orchestrator owns gate order and preconditions and
 blocks a gate whose preconditions fail.
 sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
 in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
diff --git a/intent/machine-statements/collaboration.md b/intent/machine-statements/collaboration.md
index 81e8f88..5058567 100644
--- a/intent/machine-statements/collaboration.md
+++ b/intent/machine-statements/collaboration.md
@@ -1,6 +1,6 @@
 # collaboration — machine statements
 
 phase-two handoff state is written as common ground for the operator and later tooling:
-the addressed work's current or recent gate, current unit, status, Codex thread id, latest
+the addressed work's current or recent gate, current unit, status, harness session id, latest
 message, failure reason, event history, run artifact paths, and phase-two acceptance
 artifact paths are recoverable from loop state files.
diff --git a/intent/machine-statements/loop.md b/intent/machine-statements/loop.md
index 8fbea36..ec719e2 100644
--- a/intent/machine-statements/loop.md
+++ b/intent/machine-statements/loop.md
@@ -8,12 +8,13 @@ corpus.
 `loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
 act only on that addressed work.
 `loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
-runs and after recent failure or completion, including the active gate, status, Codex
-thread id, current unit, latest message, failure reason, event history, run artifact
+runs and after recent failure or completion, including the active gate, status, harness
+session id, current unit, latest message, failure reason, event history, run artifact
 paths, and phase-two acceptance artifact paths.
-before launching the first phase-two Codex gate, `loop.sh execute <work-name>` checks that
-the Codex binary is present and that Codex home/session state is writable; a failed
-preflight records failed run state and stops before `codex exec`.
+before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
+that the configured executor binary is present and that executor home/session state is
+writable; a failed preflight records failed run state and stops before the executor
+session starts.
 `loop.sh status <work-name>` reports the addressed work's current phase and, for
 non-historical work with phase-two state, the current or recent run's gate, status, state
 path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
@@ -68,12 +69,13 @@ optional reviewer verdicts cannot clear unresolved base-roster or red-team flags
 new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
 the work node's `intent/frame/signoff.md`.
 `loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
-fresh Codex builder session for each unit, and records lean unit handoff, diff, and
-tier-one verdict artifacts under the work frame.
-`loop.sh execute <work-name>` routes builders through `CODEX_BUILDER_MODEL`, defaulting to
-the strong model until the two-step plan/build work lands, separately from the strong review
-route; it gives each unit a three-attempt fast-builder budget, escalates an exhausted unit
-to `CODEX_STRONG_BUILDER_MODEL`, and stops for the operator when the strong builder fails.
+fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
+verdict artifacts under the work frame.
+`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
+the strong model until the two-step plan/build work lands, separately from the strong
+review route; it gives each unit a three-attempt fast-builder budget, escalates an
+exhausted unit through the strong-builder model knob, and stops for the operator when the
+strong builder fails.
 `loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
 approval `never` and literal sandbox `read-only`.
 `loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
diff --git a/intent/organizing-document.md b/intent/organizing-document.md
index 2b37be7..43f21c1 100644
--- a/intent/organizing-document.md
+++ b/intent/organizing-document.md
@@ -19,8 +19,8 @@ leaf-materialized by `hypercore.md` and `check.sh`, divided along one axis:
   amendments, and node boundaries.
 - **adapter** -- the binding between a harness and the loop: what the harness loads at the
   start of work, promising agreement and enforcing it as a rigid workflow. Materialized at
-  the root by the methodology prose, the harness adapter (`AGENTS.md` for Codex), and the
-  orchestrator under `adapter/`.
+  the root by the methodology prose, the harness entry point (`AGENTS.md`), the current
+  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.
 
 The **governed work** -- durable child nodes and mounted work under this root:
 

exec
/bin/bash -lc "sed -n '1,260p' check.sh" in /home/qqp/projects/hypercore
 succeeded in 0ms:
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

contract_statement_product_absence_errors() {
  local file=$1 scope=$2
  HYPERCORE_CONTRACT_SCOPE="$scope" perl -0ne '
    my $scope = $ENV{HYPERCORE_CONTRACT_SCOPE} || "all";
    my $text = $_;

    if ($scope eq "hypercore-adapter") {
      if ($text =~ /^## adapter\n(.*?)(?=^## |\z)/ms) {
        $text = $1;
      } else {
        print "$ARGV: missing ## adapter section\n";
        exit 1;
      }
    } elsif ($scope eq "organizing-adapter") {
      my @kept;
      my $taking = 0;
      for my $line (split /\n/, $text) {
        if ($line =~ /^- \*\*adapter\*\*/) {
          $taking = 1;
        } elsif ($taking && $line =~ /^\s*$/) {
          last;
        }
        push @kept, $line if $taking;
      }
      if (!@kept) {
        print "$ARGV: missing adapter bullet\n";
        exit 1;
      }
      $text = join("\n", @kept) . "\n";
    }

    my %allowed = map { $_ => 1 } (
      "adapter/codex.md",
      "AGENTS.md",
      "adapter/codex-mounted.md",
      "adapter/loop.sh",
    );
    my @spans;
    while ($text =~ /`([^`\n]+)`/g) {
      push @spans, [$-[1], $+[1], $1];
    }

    my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
    while ($text =~ /$product/g) {
      my ($start, $end, $token) = ($-[0], $+[0], $&);
      my $ok = 0;
      for my $span (@spans) {
        if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) {
          $ok = 1;
          last;
        }
      }
      next if $ok;
      my $prefix = substr($text, 0, $start);
      my $line = 1 + ($prefix =~ tr/\n//);
      print "$ARGV:$line: product token \"$token\" is outside a whitelisted materialization pointer\n";
      exit 1;
    }
  ' "$file"
}

contract_statement_product_absence() {
  local file=$1 scope=$2 label=$3 output status
  output="$(contract_statement_product_absence_errors "$file" "$scope" 2>&1)"
  status=$?
  if [ $status -eq 0 ]; then
    ok "$label"
  else
    bad "$label ($output)"
  fi
  return $status
}

check_contract_statement_product_absence_self_tests() {
  local tmp forbidden pointer organizing

  echo "root - contract statement product grammar self-test"
  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-contract-product-check.XXXXXX")" \
    || { bad "contract product grammar self-test can create temporary space"; return; }

  forbidden="$tmp/forbidden.md"
  cat > "$forbidden" <<'EOF'
# fixture

the Codex review floor is named in a contract statement.
EOF
  if ( fail=0; contract_statement_product_absence "$forbidden" all \
    "forbidden product token fixture" >"$tmp/forbidden.out" 2>&1 ); then
    bad "contract product grammar rejects an unwhitelisted harness-product token"
  else
    ok "contract product grammar rejects an unwhitelisted harness-product token"
  fi
  require_text "$tmp/forbidden.out" \
    'product token "Codex" is outside a whitelisted materialization pointer' \
    "contract product grammar failure names the forbidden token"

  pointer="$tmp/pointer.md"
  cat > "$pointer" <<'EOF'
# fixture

the current root harness adapter is materialized as `adapter/codex.md`.
EOF
  if ( fail=0; contract_statement_product_absence "$pointer" all \
    "whitelisted materialization pointer fixture" >"$tmp/pointer.out" 2>&1 ); then
    ok "contract product grammar accepts a whitelisted materialization pointer"
  else
    bad "contract product grammar accepts a whitelisted materialization pointer"
  fi

  organizing="$tmp/organizing-document.md"
  cat > "$organizing" <<'EOF'
# organizing document

- **adapter** -- the binding between a harness and the loop, materialized through `adapter/codex.md`.

The **governed work** -- durable child nodes and mounted work under this root:

- **home** -- home currently mounts codex-cockpit.
EOF
  if ( fail=0; contract_statement_product_absence "$organizing" organizing-adapter \
    "out-of-scope governed-work product mention fixture" >"$tmp/organizing.out" 2>&1 ); then
    ok "contract product grammar ignores out-of-scope governed-work child-node names"
  else
    bad "contract product grammar ignores out-of-scope governed-work child-node names"
  fi

  require_text "$root/intent/collaboration.md" \
    "the phase-one collaborator is the harness role that drives orient and frame" \
    "phase-one routing self-test sees the collaborator role assertion"
  require_text "$root/intent/collaboration.md" \
    "phase-one corpus-throughput work" \
    "phase-one routing self-test sees the throughput-delegation assertion"
  require_text "$root/intent/collaboration.md" \
    "the framer is not its own witness" \
    "phase-one routing self-test sees the independent-review-floor assertion"
  require_text "$root/intent/loop.md" \
    "phase-one labor may be routed by role" \
    "phase-one routing self-test sees the phase-one routing assertion"
  require_text "$root/intent/loop.md" \
    "the collaborator role defaults to the interactive harness that loaded the adapter" \
    "phase-one routing self-test sees the collaborator held default"
  require_text "$root/intent/loop.md" \
    "the fast-builder default is held at the strong model" \
    "phase-one routing self-test sees the builder held default"
  require_text "$root/intent/loop.md" \
    "phase-one review stay on the" \
    "phase-one routing self-test sees the review-floor held default"
  require_text "$root/intent/adapter.md" \
    "the phase-one collaborator role defaults to the interactive harness" \
    "phase-one routing self-test sees the adapter collaborator default"
  require_text "$root/adapter/codex.md" \
    "to the interactive Codex harness that loaded this adapter" \
    "phase-one routing self-test sees the current binding collaborator default"
  require_text "$root/adapter/loop.sh" \
    'CODEX_REVIEW_EFFORT:-xhigh' \
    "phase-one routing self-test sees the review-effort held default"
  require_text "$root/adapter/loop.sh" \
    'CODEX_BUILDER_MODEL:-gpt-5.5' \
    "phase-one routing self-test sees the builder-model held default"
  require_text "$root/adapter/loop.sh" \
    'CODEX_BUILDER_EFFORT:-xhigh' \
    "phase-one routing self-test sees the builder-effort held default"

  rm -rf "$tmp"
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

exec
/bin/bash -lc "sed -n '241,520p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
  `adapter/codex.md` remains the current binding.
- Not a new gate and not field-count collaboration. It adds roles and config, not paperwork.
- Not a planner or executor. The phase-one collaborator's output ends at orient and frame
  artifacts (teach-back, options, frame, decision brief); it does not create implementation
  units, plan tasks, acceptance artifacts, or review evidence. This keeps the collaborator seam
  distinct from the queued two-step planner.

## proof state

Required proof: the observable-acceptance checks above, plus `check.sh` self-tests that a
product-named contract statement fails the product-absence check, and that the held defaults
reproduce current routing when the knobs are unset. Baseline `./check.sh` is green before
implementation (to be confirmed at the start of phase two).

Phase-one evidence: the governed one-way review roster ran (`intent/frame/review.md`); its base
flags reduced to a pre-direction staging artifact (route is TODO before direction, by gate
design) rather than a substantive defect, so a corrected independent decision review was run and
recorded at `intent/frame/review-supplementary.md`. Its substantive findings — the
capability-requirement layer, the exact pointer grammar, the scoped check, the collaborator
output boundary, and the unpinned review floor — are folded into the constraints, observable
acceptance, excluded interpretation, and route deliverables above.

## sweep

Map: `collaboration` owns role partition, reliance, and the new phase-one routing principle;
`loop` owns gate order and the routing statements (sibling to the existing phase-two
builder-routing line); `adapter` owns harness binding, materialization, and config seams;
`check.sh` proves it; `hypercore.md` summarizes it; `adapter/codex.md` is the current
materialization. The general rule "an adapter is per harness" already supports multi-harness
binding and does not conflict — this work makes the rest of the contract consistent with it.

Read: the change is coherent only if the de-naming lands across intent, machine statements,
prose, and `check.sh` together — a half-de-named contract is a worse smell than the current
uniform product naming (the same lesson `007` recorded: replace everywhere or nowhere). The
adjacency to `TWO-STEP-BUILD` is parallel, not colliding: that work routes the phase-two
builder; this routes phase-one labor; different phase, different knobs. No active work node
collides.

Verdict: coherent provided the contract is de-named atomically and the
materialization/config boundary holds.

## adoption claim

Adopt if the contract is product-agnostic (no harness product token in any contract
statement), the phase-one collaborator role and routing seam exist with held defaults, the
review-floor-independent-of-the-framer statement is present, the materialization still binds
the current harness, `./check.sh` proves all of this and is green, and the sweep is coherent.

## shelving claim

Shelve if the contract cannot be de-named without breaking the materialization boundary or
the proof floor; if the product-absence check proves too brittle (false positives on
legitimate materialization pointers); if the held defaults cannot reproduce current behavior;
or if the full scope cannot land coherently in one node, in which case the work shelves and
re-frames at a smaller scope rather than weakening this frame's acceptance condition.

exec
/bin/bash -lc "rg -n \"CODEX_(BUILDER_MODEL|STRONG_BUILDER_MODEL|REVIEW_MODEL|REVIEW_EFFORT|BUILDER_EFFORT)|gpt-5\\.5|xhigh|REVIEW_MODEL|BUILDER_MODEL|STRONG_BUILDER\" adapter/loop.sh check.sh" in /home/qqp/projects/hypercore
 succeeded in 0ms:
check.sh:225:    'CODEX_REVIEW_EFFORT:-xhigh' \
check.sh:228:    'CODEX_BUILDER_MODEL:-gpt-5.5' \
check.sh:231:    'CODEX_BUILDER_EFFORT:-xhigh' \
check.sh:1406:    CODEX_STRONG_BUILDER_MODEL="gpt-5.3-codex" \
check.sh:1412:  require_text "$tmp/retry-escalation.out" "-m gpt-5.5" \
check.sh:1413:    "fast builder dry-run command uses the gpt-5.5 builder default"
check.sh:1414:  require_text "$tmp/retry-escalation.out" "model_reasoning_effort=\\\"xhigh\\\"" \
check.sh:2381:  "loop validates CODEX_REVIEW_MODEL"
check.sh:2383:  'CODEX_REVIEW_EFFORT:-xhigh' \
check.sh:2386:  'CODEX_BUILDER_MODEL:-gpt-5.5' \
check.sh:2387:  "loop defaults fast builders to gpt-5.5 until the two-step plan/build lands"
check.sh:2389:  'CODEX_BUILDER_EFFORT:-xhigh' \
check.sh:2392:  'CODEX_STRONG_BUILDER_MODEL' \
adapter/loop.sh:39:#   CODEX_BUILDER_MODEL (default: gpt-5.5 until the two-step plan/build lands), CODEX_BUILDER_EFFORT (default: xhigh)
adapter/loop.sh:40:#   CODEX_STRONG_BUILDER_MODEL (optional strong-builder escalation model)
adapter/loop.sh:41:#   CODEX_STRONG_BUILDER_EFFORT (default: CODEX_REVIEW_EFFORT or xhigh)
adapter/loop.sh:42:#   CODEX_REVIEW_MODEL (optional strong review/acceptance model), CODEX_REVIEW_EFFORT (default: xhigh)
adapter/loop.sh:2653:      model="${CODEX_BUILDER_MODEL:-gpt-5.5}"
adapter/loop.sh:2654:      effort="${CODEX_BUILDER_EFFORT:-xhigh}"
adapter/loop.sh:2655:      codex_add_model_and_effort_args "$model" "$effort" CODEX_BUILDER_MODEL CODEX_BUILDER_EFFORT
adapter/loop.sh:2658:      model="${CODEX_STRONG_BUILDER_MODEL:-${CODEX_REVIEW_MODEL:-${CODEX_MODEL:-}}}"
adapter/loop.sh:2659:      effort="${CODEX_STRONG_BUILDER_EFFORT:-${CODEX_REVIEW_EFFORT:-xhigh}}"
adapter/loop.sh:2660:      codex_add_model_and_effort_args "$model" "$effort" CODEX_STRONG_BUILDER_MODEL CODEX_STRONG_BUILDER_EFFORT
adapter/loop.sh:3001:  local model=${CODEX_REVIEW_MODEL:-}
adapter/loop.sh:3002:  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
adapter/loop.sh:3003:  validate_codex_model_var CODEX_REVIEW_MODEL "$model"
adapter/loop.sh:3004:  validate_codex_effort_var CODEX_REVIEW_EFFORT "$effort"
adapter/loop.sh:3008:  local model=${CODEX_REVIEW_MODEL:-}
adapter/loop.sh:3009:  local effort=${CODEX_REVIEW_EFFORT:-xhigh}

exec
/bin/bash -lc 'rg -n "codex|claude|opus|gpt-[0-9]|CODEX_" intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md hypercore.md intent/organizing-document.md' in /home/qqp/projects/hypercore
 succeeded in 0ms:
intent/organizing-document.md:23:  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.
intent/organizing-document.md:28:  project nodes and governs them within itself. home currently mounts `codex-cockpit`.
intent/machine-statements/adapter.md:3:the current root harness adapter is materialized as `adapter/codex.md`.
intent/machine-statements/adapter.md:6:the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
hypercore.md:259:For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
intent/adapter.md:59:the current root harness adapter is materialized as `adapter/codex.md`.
intent/adapter.md:62:the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;

exec
/bin/bash -lc ./check.sh in /home/qqp/projects/hypercore
 succeeded in 40364ms:
  ok    hypercore adapter section has no unscoped harness product token
  ok    organizing adapter bullet has no unscoped harness product token
root - contract statement product grammar self-test
  ok    contract product grammar rejects an unwhitelisted harness-product token
  ok    contract product grammar failure names the forbidden token
  ok    contract product grammar accepts a whitelisted materialization pointer
  ok    contract product grammar ignores out-of-scope governed-work child-node names
  ok    phase-one routing self-test sees the collaborator role assertion
  ok    phase-one routing self-test sees the throughput-delegation assertion
  ok    phase-one routing self-test sees the independent-review-floor assertion
  ok    phase-one routing self-test sees the phase-one routing assertion
  ok    phase-one routing self-test sees the collaborator held default
  ok    phase-one routing self-test sees the builder held default
  ok    phase-one routing self-test sees the review-floor held default
  ok    phase-one routing self-test sees the adapter collaborator default
  ok    phase-one routing self-test sees the current binding collaborator default
  ok    phase-one routing self-test sees the review-effort held default
  ok    phase-one routing self-test sees the builder-model held default
  ok    phase-one routing self-test sees the builder-effort held default
  ok    check.sh exists and is executable
  ok    organizing document counts nine methodology segments
  ok    organizing document names collaboration as a methodology segment
  ok    intent/collaboration.md exists
  ok    intent/machine-statements/collaboration.md exists
root - flat paths
  ok    tracked live material/ paths are retired
  ok    adapter/codex.md exists
  ok    adapter/codex-mounted.md exists
  ok    adapter/loop.sh exists and is executable
  ok    bin/home-signoff exists and is executable
  ok    adapter/gates/orient.md exists
  ok    adapter/gates/frame.md exists
  ok    adapter/gates/implement.md exists
  ok    adapter/gates/check.md exists
  ok    adapter/gates/archive.md exists
  ok    home/intent/ exists
  ok    home/README.md exists
root - adapter design phase
  ok    AGENTS.md routes Codex into the methodology prose
  ok    AGENTS.md routes Codex into the loop
  ok    retired root adapter entry point is absent
  ok    retired adapter prose is absent
  ok    operator-act scratch findings are removed from the live root
  ok    performance scratch findings are removed from the live root
  ok    tracked ignore material does not hide retired local state
  ok    orient gate classifies the request surface
  ok    orient gate rejects simplicity-based loop bypass
  ok    orient gate names open direction for operator input
  ok    orient gate names neutral direction options
  ok    orient gate blocks machine option selection
  ok    orient gate names the addressed node
  ok    orient gate names the node-local work name
  ok    orient gate names target segments
  ok    orient gate names work in flight
  ok    orient gate requires teach-back
  ok    orient gate requires an alternative framing
  ok    orient gate requires information-gain questions
  ok    orient gate requires reversibility classification
  ok    orient gate forbids route writing
  ok    frame gate names the problem, constraints, and decision surface
  ok    frame gate requires observable acceptance
  ok    frame gate requires excluded interpretation
  ok    frame gate requires direction artifact
  ok    frame gate requires direction-by
  ok    frame gate requires substantive selected route
  ok    frame gate requires neutral direction options
  ok    frame gate requires operator-gated acts
  ok    frame gate names the terminal liveness channel
  ok    frame gate ties direction to an option
  ok    frame gate requires signed-off-at in sign-off
  ok    frame gate requires work-number sign-off confirmation
  ok    frame gate requires one-way review artifact
  ok    frame gate prevents optional reviewer override
  ok    frame gate waits for direction
  ok    frame gate names one-way review
  ok    frame gate names two-way reversibility
  ok    frame gate requires non-retrospective direction
  ok    check gate names the flat check command
  ok    check gate names tier-one implementation acceptance
  ok    check gate requires acceptance rationale
  ok    check gate requires acceptance evidence
  ok    check gate carries concurrent tier-two panel execution
  ok    check gate carries deterministic panel artifact paths
  ok    check gate assigns one-way coherence to the panel
  ok    implement gate reads current work-node frames
  ok    implement gate requires lean unit handoff state
  ok    implement gate describes resumable execute as orchestrator state
  ok    archive gate signs current work-node frames
  ok    archive gate blocks one-way work without clean panel artifacts
  ok    archive gate rejects non-real acceptance artifacts
  ok    Codex adapter describes phase one as design-phase collaboration
  ok    Codex adapter classifies the request surface
  ok    Codex adapter rejects simplicity-based loop bypass
  ok    Codex adapter carries teach-back before route
  ok    Codex adapter carries alternative framing before route
  ok    Codex adapter carries reversibility classification
  ok    Codex adapter names the root review helper
  ok    Codex adapter names the base review roster
  ok    Codex adapter makes optional reviewers advisory
  ok    Codex adapter names the root direction helper
  ok    Codex adapter blocks machine-authored direction
  ok    Codex adapter names neutral direction options
  ok    Codex adapter carries the operator-gate marker
  ok    Codex adapter names the terminal liveness channel
  ok    Codex adapter ties direction to selected option text
  ok    Codex adapter carries work-number sign-off confirmation
  ok    Codex adapter does not overclaim the operator gate
  ok    Codex adapter no longer presents argument-transcribed direction as primary
  ok    Codex adapter carries acceptance condition
  ok    Codex adapter carries observable acceptance
  ok    Codex adapter carries excluded interpretation
  ok    Codex adapter keeps phase two tied to the signed frame directory
  ok    Codex adapter carries one-way implementation acceptance
  ok    Codex adapter carries structured phase-two acceptance artifacts
  ok    Codex adapter carries concurrent tier-two panel execution
  ok    Codex adapter no longer describes one resumed phase-two thread
  ok    Codex adapter carries the decision surface
  ok    Codex adapter carries node-local work wording
  ok    Codex adapter describes adoption or shelving
  ok    Codex adapter names the root sign-off helper
  ok    mounted Codex entrypoint identifies root-managed adapter material
  ok    mounted Codex entrypoint names the governing root
  ok    mounted Codex entrypoint tells Codex to read local intent first
  ok    mounted Codex entrypoint routes through home resolve
  ok    mounted Codex entrypoint routes work through the resolved mount path
  ok    mounted Codex entrypoint points to the root adapter
  ok    mounted Codex entrypoint keeps local checks as proof only
  ok    mounted Codex entrypoint rejects fabrication
  ok    mounted signoff helper resolves the caller mount path
  ok    mounted signoff helper dispatches sign-off to the root loop
  ok    loop defaults phase two to Codex
  ok    loop defaults phase-two state under .hypercore/loop-runs
  ok    loop writes a run event JSONL file
  ok    loop writes a current run state file
  ok    loop writes an addressed-work current state pointer
  ok    loop writes a root current state pointer
  ok    loop records phase-two acceptance state under the work frame
  ok    loop creates the phase-two state directories
  ok    loop has a phase-two Codex preflight
  ok    loop declares required frame fields
  ok    loop validates the frame field contract
  ok    loop requires decision surface or open direction
  ok    loop requires reversibility
  ok    loop requires acceptance condition
  ok    loop requires observable acceptance
  ok    loop requires excluded interpretation
  ok    loop requires adoption or shelving claim
  ok    loop start scaffolds canonical frame.md
  ok    loop strictly parses route from canonical frame.md
  ok    loop parses acceptance condition as a strict label
  ok    loop parses observable acceptance from canonical frame.md
  ok    loop parses excluded interpretation from canonical frame.md
  ok    loop parses exact reversibility tokens
  ok    loop validates structured direction
  ok    loop validates neutral direction options
  ok    loop names the neutral options artifact
  ok    loop selects direction from options through the operator gate
  ok    loop ties direction text to a numbered option
  ok    loop handles none-of-these direction selections
  ok    loop handles aborted direction selections
  ok    loop parses operator-gate markers exactly
  ok    loop operator gate uses /dev/tty
  ok    loop direction helper crosses the operator gate
  ok    loop validates structured signoff
  ok    loop renders the sign-off attestation brief from the frame
  ok    loop signoff helper crosses the sign-off attestation gate
  ok    loop signoff helper writes signed-off-at
  ok    loop exposes direct command
  ok    loop rejects empty direction
  ok    loop rejects retrospective direction
  ok    loop exposes review command
  ok    loop declares the base review roster
  ok    loop declares complete optional review roster
  ok    reviewer subprocesses use literal approval never and read-only sandbox
  ok    reviewer subprocesses use the separate strong review route
  ok    acceptance reviewer subprocesses use literal approval never and read-only sandbox
  ok    acceptance reviewer subprocesses have a bounded runtime override
  ok    acceptance reviewer subprocesses are timeout bounded
  ok    loop validates CODEX_REVIEW_MODEL
  ok    loop keeps review effort strong by default
  ok    loop defaults fast builders to gpt-5.5 until the two-step plan/build lands
  ok    loop applies a separate builder effort default
  ok    loop exposes a strong-builder escalation model knob
  ok    malformed reviewer output counts as FLAG
  ok    review artifacts preserve diagnostic sections
  ok    review artifacts record diagnostic output source
  ok    loop parses implementation acceptance verdicts exactly
  ok    malformed acceptance output counts as FLAG
  ok    evidence-free acceptance output counts as FLAG
  ok    acceptance artifacts record a source marker
  ok    acceptance artifacts record source proof
  ok    real reviewer source is represented explicitly
  ok    fake acceptance source is represented explicitly
  ok    real execute rejects fake acceptance source
  ok    loop derives implementation units from the signed frame
  ok    loop stores per-unit execute cache records
  ok    loop computes signed-frame-derived per-unit cache base keys
  ok    loop folds handoff, diff, check, and tier-one evidence into cache keys
  ok    loop validates cache hits before skipping units
  ok    loop skips unchanged accepted units on cache hits
  ok    loop invalidates downstream unit evidence when prior state changes
  ok    loop runs tier-one implementation acceptance
  ok    loop wraps each unit build in an attempt boundary
  ok    loop gives each unit a three-attempt fast-builder budget
  ok    loop routes exhausted units to a strong-builder escalation
  ok    loop stops for the operator when the strong builder fails
  ok    real execute rejects fake builder sources
  ok    real execute rejects fake check sources
  ok    tier-one acceptance prompt carries mechanical check evidence
  ok    tier-one and tier-two prompts require rationale
  ok    tier-one and tier-two prompts require evidence
  ok    tier-one acceptance prompt explains cumulative diff records
  ok    loop runs the one-way tier-two implementation acceptance panel
  ok    loop isolates each tier-two lens in a per-lens worker
  ok    loop launches tier-two lens workers concurrently
  ok    loop waits for every concurrent tier-two lens
  ok    loop records deterministic concurrent panel start events
  ok    loop preserves the all-lenses-clean panel gate
  ok    loop gives each one-way panel lens a specific acceptance prompt
  ok    loop threads live tier-two lens instructions inside the panel loop
  ok    loop has a whole-acceptance-conformance-specific panel prompt
  ok    loop has a proof-integrity-specific panel prompt
  ok    loop has an independent-coherence-specific panel prompt
  ok    loop has a security-permissions-specific panel prompt
  ok    loop has a red-team-specific panel prompt
  ok    loop guards the one-way panel behind clean unit-level acceptance
  ok    loop explains blocked panel ordering when unit-level acceptance is incomplete
  ok    loop tells builders not to speculate about acceptance artifacts
  ok    loop tells builders not to carry stale run-state notes into handoffs
  ok    loop excludes unrelated untracked files from unit diff status
  ok    loop declares the required one-way panel lenses
  ok    loop gates archive on clean required acceptance artifacts
  ok    loop validates tier-one artifacts before real archive
  ok    archive validation rejects non-real acceptance sources
  ok    loop keeps two-way work out of the one-way panel
  ok    loop reports optional reviewer non-override
  ok    loop parses archive decision exactly and singularly
  ok    loop checks again after moving work history
  ok    loop no longer requires the problem/domain map
  ok    loop no longer requires the evidence standard
  ok    loop no longer requires operator expectation
  ok    loop start no longer scaffolds common-ground pile
  ok    loop start no longer scaffolds operator-deliberation pile
  ok    loop preflight checks the Codex binary
  ok    loop preflight resolves Codex home
  ok    loop preflight checks Codex session write permission
  ok    loop stops directly on preflight failure
  ok    loop preserves detailed preflight failure state
  ok    loop stores the raw Codex JSON event stream per gate
  ok    loop streams Codex JSON events while the gate runs
  ok    loop prints progress from streamed Codex events
  ok    loop no longer buffers the Codex JSON stream before progress
  ok    loop records acceptance verdicts in run events
  ok    loop records the archive decision in run events
  ok    loop no longer resumes one builder thread through phase-two judgement
  ok    loop status reports phase-two run state
  ok    loop status exposes tier-two panel and resumable cache paths
  ok    loop status can render phase-two run state as JSON
  ok    loop carries no retired binary setting
  ok    loop carries no retired budget setting
  ok    loop carries no retired gate runner
  ok    loop can infer the single signable work node
  ok    loop can infer sign-off operator from the environment
  ok    loop blocks ambiguous work inference
  ok    loop blocks ambiguous operator inference
  ok    root signoff helper dispatches to the loop
  ok    root signoff helper preserves explicit arguments
  ok    root signoff helper is executable
  ok    root direction helper dispatches to the loop
  ok    root direction helper preserves explicit arguments
  ok    root direction helper is executable
  ok    root review helper dispatches to the loop
  ok    root review helper preserves explicit arguments
  ok    root review helper is executable
  ok    loop keys new work sign-off to the signoff artifact
  ok    loop signoff helper crosses the operator gate
  ok    loop does not trust arbitrary frame text as sign-off
  ok    loop carries no retired changes path
  ok    loop carries no retired change-history path
  ok    loop carries no retired sign-off file
  ok    loop carries no retired compatibility constants
  ok    check.sh carries no retired changes path
  ok    check.sh carries no retired change-history path
  ok    check.sh carries no retired sign-off file
  ok    check.sh carries no retired compatibility constants
root - loop frame contract
  ok    loop start creates a temporary work node
  ok    loop start scaffolds intent/frame/frame.md
  ok    loop start scaffolds intent/frame/options.md
  ok    frame template includes exact reversibility slot
  ok    frame template includes acceptance condition
  ok    frame template includes observable acceptance
  ok    frame template includes excluded interpretation
  ok    frame template includes adoption claim
  ok    options template includes numbered option 1
  ok    options template includes numbered option 2
  ok    options template includes rejection choices
  ok    frame template no longer scaffolds operator deliberation pile
  ok    frame template no longer scaffolds common-ground pile
  ok    loop frame rejects a placeholder-only frame
  ok    loop frame explains missing required frame fields
  ok    loop frame rejects route content without direction
  ok    loop frame explains route-before-direction rejection
  ok    loop direct refuses explicit forms for new gated work
  ok    loop direct explains explicit-form refusal for new work
  ok    loop direct explicit form for new work writes no direction artifact
  ok    loop direct refuses after route content
  ok    loop direct explains retrospective direction refusal
  ok    loop direct refuses without /dev/tty
  ok    loop direct explains /dev/tty refusal
  ok    loop direct without /dev/tty writes no direction artifact
  ok    loop direct records a numbered options selection through /dev/tty
  ok    option-selected direction records the tty operator gate
  ok    loop direct copies the selected option summary into direction.md
  ok    loop direct renders neutral numbered options
  ok    loop direct none-of-these writes no direction
  ok    loop direct explains none-of-these selection
  ok    loop direct none-of-these leaves direction absent
  ok    loop direct abort writes no direction
  ok    loop direct explains abort selection
  ok    loop direct abort leaves direction absent
  ok    loop frame rejects direction without options.md
  ok    loop frame explains missing options.md
  ok    loop frame rejects options without abort handling
  ok    loop frame explains missing abort rejection choice
  ok    loop frame rejects recommended/default option markers
  ok    loop frame explains neutrality-relevant option rejection
  ok    loop frame rejects direction text not copied from options.md
  ok    loop frame explains direction/options mismatch
  ok    loop frame rejects retrospective direction timestamp
  ok    loop frame explains retrospective direction timestamp
  ok    direction artifact records the tty operator gate
  ok    loop frame rejects direction without operator-gate
  ok    loop frame explains missing direction operator-gate
  ok    loop frame rejects direction with invalid operator-gate
  ok    loop frame explains invalid direction operator-gate
  ok    loop frame rejects a reserved hmac operator-gate scheme not yet implemented
  ok    loop frame keeps operator-gate syntax B-ready while implementing only tty
  ok    direction artifact records direction-by
  ok    direction artifact records direction-given-at
  ok    direction artifact records exactly one substantive delegation
  ok    two-way work with direction and no review is frame-complete
  ok    loop signoff refuses without /dev/tty
  ok    loop signoff explains /dev/tty refusal
  ok    loop signoff without /dev/tty writes no signoff artifact
  ok    loop signoff requires the work number rather than the full work name
  ok    loop signoff renders a frame-derived attestation brief
  ok    loop signoff brief includes target segments
  ok    loop signoff brief includes reversibility
  ok    loop signoff brief includes route
  ok    loop signoff brief includes acceptance condition
  ok    loop signoff brief includes observable acceptance
  ok    loop signoff brief includes excluded interpretation
  ok    loop signoff prompts for the work number
  ok    loop signoff rejects full-name confirmation
  ok    loop signoff with wrong token writes no signoff artifact
  ok    bare signoff without operator-gate does not satisfy signed-off validation
  ok    loop execute rejects signoff without operator-gate
  ok    loop execute explains missing signoff operator-gate
  ok    loop execute explains missing signoff timestamp
  ok    timestamp-less signoff does not satisfy signed-off validation
  ok    loop execute rejects signoff without signed-off-at
  ok    loop execute explains missing timestamp on gated signoff
  ok    signoff with invalid operator-gate does not satisfy signed-off validation
  ok    loop execute rejects signoff with invalid operator-gate
  ok    loop execute explains invalid signoff operator-gate
  ok    signoff artifact records signed-off-at
  ok    signoff artifact records the tty operator gate
  ok    loop frame rejects missing observable acceptance
  ok    loop frame explains missing observable acceptance
  ok    loop frame rejects missing excluded interpretation
  ok    loop frame explains missing excluded interpretation
  ok    one-way work with direction but no review is rejected
  ok    loop frame explains missing one-way review
  ok    one-way work with direction and review is frame-complete
  ok    loop frame excludes direction/review/signoff from frame field parsing
  ok    loop frame reports missing route from canonical frame.md
  ok    loop review uses deterministic fake reviewer output in self-test
  ok    malformed reviewer output counts as FLAG
  ok    optional reviewer verdict is recorded as advisory
  ok    optional reviewers cannot clear base flags
  ok    review artifact preserves reviewer diagnostic section
  ok    review artifact records nonzero reviewer subprocess status
  ok    review artifact preserves nonzero reviewer diagnostic output
  ok    review artifact records diagnostic output source
  ok    loop review records optional flags without making them required
  ok    optional reviewer FLAG does not override clean base roster
  ok    optional reviewer FLAG is still recorded
  ok    optional reviewer flags have a separate advisory section
  ok    optional reviewer FLAG remains advisory
  ok    optional reviewer FLAG does not escalate base-roster disposition
  ok    loop frame rejects optional reviewer override of base flags
  ok    loop frame explains optional reviewers cannot clear base flags
  ok    loop execute blocks malformed tier-one acceptance output
  ok    loop execute explains tier-one required flag blocking
  ok    tier-one malformed output is recorded as FLAG
  ok    tier-one malformed output records actionable parser notes
  ok    tier-one prompt carries the pre-review mechanical check result
  ok    tier-one prompt explains cumulative diff records
  ok    execute dry-run keeps tier-one artifacts out of the active work frame
  ok    loop execute blocks evidence-free tier-one acceptance output
  ok    tier-one evidence-free output is recorded as FLAG
  ok    tier-one evidence-free output records the evidence defect
  ok    loop execute blocks structured tier-one FLAG output
  ok    tier-one structured FLAG preserves rationale
  ok    tier-one structured FLAG preserves evidence
  ok    two-way execute dry-run pays tier one and completes without one-way panel
  ok    two-way execute dry-run runs tier-one acceptance
  ok    two-way execute dry-run skips the one-way panel
  ok    tier-one dry-run fake acceptance records fake source
  ok    tier-one dry-run fake acceptance records non-real source proof
  ok    tier-one structured PASS preserves rationale
  ok    tier-one structured PASS preserves evidence
  ok    two-way execute dry-run writes no one-way panel verdicts
  ok    one-way execute dry-run blocks tier-two panel flags
  ok    loop execute explains one-way panel flag blocking
  ok    one-way tier-two panel reports concurrent lens start
  ok    one-way tier-two panel starts every lens before collecting results
  ok    tier-two panel records a concurrent panel start event
  ok    tier-two panel starts only after the final unit tier-one acceptance
  ok    tier-two panel starts all lens subprocesses before collecting results
  ok    structured independent-coherence output is recorded as FLAG
  ok    tier-two structured FLAG preserves evidence
  ok    tier-two whole-acceptance-conformance artifact names its own lens
  ok    tier-two whole-acceptance-conformance prompt is lens-specific
  ok    tier-two whole-acceptance-conformance prompt does not carry stale proof-integrity instruction
  ok    tier-two whole-acceptance-conformance prompt does not carry stale independent-coherence instruction
  ok    tier-two whole-acceptance-conformance prompt does not carry stale security-permissions instruction
  ok    tier-two whole-acceptance-conformance prompt does not carry stale red-team instruction
  ok    tier-two proof-integrity artifact names its own lens
  ok    tier-two proof-integrity prompt is lens-specific
  ok    tier-two proof-integrity prompt does not carry stale whole-acceptance-conformance instruction
  ok    tier-two proof-integrity prompt does not carry stale independent-coherence instruction
  ok    tier-two proof-integrity prompt does not carry stale security-permissions instruction
  ok    tier-two proof-integrity prompt does not carry stale red-team instruction
  ok    tier-two independent-coherence artifact names its own lens
  ok    tier-two independent-coherence prompt is lens-specific
  ok    tier-two independent-coherence prompt does not carry stale whole-acceptance-conformance instruction
  ok    tier-two independent-coherence prompt does not carry stale proof-integrity instruction
  ok    tier-two independent-coherence prompt does not carry stale security-permissions instruction
  ok    tier-two independent-coherence prompt does not carry stale red-team instruction
  ok    tier-two security-permissions artifact names its own lens
  ok    tier-two security-permissions prompt is lens-specific
  ok    tier-two security-permissions prompt does not carry stale whole-acceptance-conformance instruction
  ok    tier-two security-permissions prompt does not carry stale proof-integrity instruction
  ok    tier-two security-permissions prompt does not carry stale independent-coherence instruction
  ok    tier-two security-permissions prompt does not carry stale red-team instruction
  ok    tier-two red-team artifact names its own lens
  ok    tier-two red-team prompt is lens-specific
  ok    tier-two red-team prompt does not carry stale whole-acceptance-conformance instruction
  ok    tier-two red-team prompt does not carry stale proof-integrity instruction
  ok    tier-two red-team prompt does not carry stale independent-coherence instruction
  ok    tier-two red-team prompt does not carry stale security-permissions instruction
  ok    execute dry-run keeps tier-two artifacts out of the active work frame
  ok    loop execute rejects fake acceptance source in real runs
  ok    loop execute explains fake acceptance is dry-run only
  ok    real fake-source rejection writes no real tier-one artifact
  ok    loop execute retries three fast builders then accepts a strong-builder escalation
  ok    fast builder dry-run command uses the gpt-5.5 builder default
  ok    fast builder dry-run command uses the builder effort default
  ok    strong builder dry-run command uses the strong-builder model knob
  ok    check failure consumes one fast-builder attempt
  ok    tier-one FLAG consumes a fast-builder retry
  ok    third fast-builder failure exhausts the fast budget
  ok    loop escalates the unit to a strong builder after the fast budget
  ok    strong-builder escalation accepts only that unit
  ok    final handoff records the accepted strong-builder attempt
  ok    failed fast-builder handoff is overwritten by the accepted attempt
  ok    loop execute stops for the operator when the strong builder still fails
  ok    strong-builder failure reports the escalated failure
  ok    strong-builder failure keeps the work in flight for the operator
  ok    strong-stop path escalates only after the fast budget
  ok    loop execute writes resumable unit cache records after accepted units
  ok    first execute builds the first uncached unit
  ok    first execute builds the second uncached unit
  ok    unit-001 cache record carries a cache key
  ok    unit-001 cache record carries the signed-frame-derived base key
  ok    unit-001 cache record carries prior-unit state
  ok    unit-001 cache record carries loop implementation version
  ok    unit-001 cache record carries diff evidence
  ok    unit-001 cache record carries green check evidence
  ok    unit-001 cache record carries tier-one PASS evidence
  ok    loop execute skips unchanged accepted units on rerun
  ok    rerun skips the unchanged first unit
  ok    rerun skips the unchanged second unit
  ok    cache hit does not rerun the first unit builder
  ok    cache hit does not rerun first unit tier-one acceptance
  ok    loop execute rebuilds cache misses and invalidates downstream units
  ok    corrupted unit evidence causes a cache miss
  ok    changed prior-unit state invalidates downstream cached evidence
  ok    downstream invalidation rebuilds the second unit
  ok    downstream rebuild replaces the unit-002 cache key
root - retired user-facing path examples
  ok    README.md does not point to material/hypercore.md
  ok    README.md does not point to material/check.sh
  ok    README.md does not point to material/adapter
  ok    README.md does not point to material/home
  ok    README.md does not point to material/bin/home
  ok    README.md does not point to retired changes path
  ok    README.md does not point to retired change-history path
  ok    README.md does not name the retired nested route
  ok    README.md does not name retired sign-off file
  ok    hypercore.md does not point to material/hypercore.md
  ok    hypercore.md does not point to material/check.sh
  ok    hypercore.md does not point to material/adapter
  ok    hypercore.md does not point to material/home
  ok    hypercore.md does not point to material/bin/home
  ok    hypercore.md does not point to retired changes path
  ok    hypercore.md does not point to retired change-history path
  ok    hypercore.md does not name the retired nested route
  ok    hypercore.md does not name retired sign-off file
  ok    codex.md does not point to material/hypercore.md
  ok    codex.md does not point to material/check.sh
  ok    codex.md does not point to material/adapter
  ok    codex.md does not point to material/home
  ok    codex.md does not point to material/bin/home
  ok    codex.md does not point to retired changes path
  ok    codex.md does not point to retired change-history path
  ok    codex.md does not name the retired nested route
  ok    codex.md does not name retired sign-off file
  ok    codex-mounted.md does not point to material/hypercore.md
  ok    codex-mounted.md does not point to material/check.sh
  ok    codex-mounted.md does not point to material/adapter
  ok    codex-mounted.md does not point to material/home
  ok    codex-mounted.md does not point to material/bin/home
  ok    codex-mounted.md does not point to retired changes path
  ok    codex-mounted.md does not point to retired change-history path
  ok    codex-mounted.md does not name the retired nested route
  ok    codex-mounted.md does not name retired sign-off file
  ok    orient.md does not point to material/hypercore.md
  ok    orient.md does not point to material/check.sh
  ok    orient.md does not point to material/adapter
  ok    orient.md does not point to material/home
  ok    orient.md does not point to material/bin/home
  ok    orient.md does not point to retired changes path
  ok    orient.md does not point to retired change-history path
  ok    orient.md does not name the retired nested route
  ok    orient.md does not name retired sign-off file
  ok    frame.md does not point to material/hypercore.md
  ok    frame.md does not point to material/check.sh
  ok    frame.md does not point to material/adapter
  ok    frame.md does not point to material/home
  ok    frame.md does not point to material/bin/home
  ok    frame.md does not point to retired changes path
  ok    frame.md does not point to retired change-history path
  ok    frame.md does not name the retired nested route
  ok    frame.md does not name retired sign-off file
  ok    implement.md does not point to material/hypercore.md
  ok    implement.md does not point to material/check.sh
  ok    implement.md does not point to material/adapter
  ok    implement.md does not point to material/home
  ok    implement.md does not point to material/bin/home
  ok    implement.md does not point to retired changes path
  ok    implement.md does not point to retired change-history path
  ok    implement.md does not name the retired nested route
  ok    implement.md does not name retired sign-off file
  ok    check.md does not point to material/hypercore.md
  ok    check.md does not point to material/check.sh
  ok    check.md does not point to material/adapter
  ok    check.md does not point to material/home
  ok    check.md does not point to material/bin/home
  ok    check.md does not point to retired changes path
  ok    check.md does not point to retired change-history path
  ok    check.md does not name the retired nested route
  ok    check.md does not name retired sign-off file
  ok    archive.md does not point to material/hypercore.md
  ok    archive.md does not point to material/check.sh
  ok    archive.md does not point to material/adapter
  ok    archive.md does not point to material/home
  ok    archive.md does not point to material/bin/home
  ok    archive.md does not point to retired changes path
  ok    archive.md does not point to retired change-history path
  ok    archive.md does not name the retired nested route
  ok    archive.md does not name retired sign-off file
  ok    home does not point to material/hypercore.md
  ok    home does not point to material/check.sh
  ok    home does not point to material/adapter
  ok    home does not point to material/home
  ok    home does not point to material/bin/home
  ok    home does not point to retired changes path
  ok    home does not point to retired change-history path
  ok    home does not name the retired nested route
  ok    home does not name retired sign-off file
  ok    home-signoff does not point to material/hypercore.md
  ok    home-signoff does not point to material/check.sh
  ok    home-signoff does not point to material/adapter
  ok    home-signoff does not point to material/home
  ok    home-signoff does not point to material/bin/home
  ok    home-signoff does not point to retired changes path
  ok    home-signoff does not point to retired change-history path
  ok    home-signoff does not name the retired nested route
  ok    home-signoff does not name retired sign-off file
  ok    README.md does not point to material/hypercore.md
  ok    README.md does not point to material/check.sh
  ok    README.md does not point to material/adapter
  ok    README.md does not point to material/home
  ok    README.md does not point to material/bin/home
  ok    README.md does not point to retired changes path
  ok    README.md does not point to retired change-history path
  ok    README.md does not name the retired nested route
  ok    README.md does not name retired sign-off file
  ok    signoff does not point to material/hypercore.md
  ok    signoff does not point to material/check.sh
  ok    signoff does not point to material/adapter
  ok    signoff does not point to material/home
  ok    signoff does not point to material/bin/home
  ok    signoff does not point to retired changes path
  ok    signoff does not point to retired change-history path
  ok    signoff does not name the retired nested route
  ok    signoff does not name retired sign-off file
  ok    direction does not point to material/hypercore.md
  ok    direction does not point to material/check.sh
  ok    direction does not point to material/adapter
  ok    direction does not point to material/home
  ok    direction does not point to material/bin/home
  ok    direction does not point to retired changes path
  ok    direction does not point to retired change-history path
  ok    direction does not name the retired nested route
  ok    direction does not name retired sign-off file
  ok    review does not point to material/hypercore.md
  ok    review does not point to material/check.sh
  ok    review does not point to material/adapter
  ok    review does not point to material/home
  ok    review does not point to material/bin/home
  ok    review does not point to retired changes path
  ok    review does not point to retired change-history path
  ok    review does not name the retired nested route
  ok    review does not name retired sign-off file
root - home greenfield
  ok    home child node exists with intent/
  ok    home README exists at the flat mount surface
  ok    retired material/home path is absent
  ok    retired home/material mount point is absent
  ok    bin/home exists and is executable
  ok    home CLI explains the linked mount path
  ok    home CLI exposes mounted path resolution
  ok    home CLI explains root-managed direct-path entrypoints
  ok    home CLI explains the mounted Codex entrypoint link
  ok    home CLI explains the mounted signoff helper link
  ok    home CLI no longer says direct opens see only local shape
  ok    greenfield rejects path-like mount names
  ok    greenfield rejects targets inside the hypercore root
  ok    greenfield refuses non-empty targets
  ok    greenfield creates a temporary external project
  ok    greenfield refuses existing mount paths
  ok    greenfield target is a git repository
  ok    greenfield target has a local organizing document
  ok    greenfield target has a direct-path AGENTS.md entrypoint
  ok    greenfield target has an executable direct-path signoff helper
  ok    greenfield AGENTS.md points at the root-managed mounted Codex entrypoint
  ok    greenfield signoff points at the root-managed home signoff helper
  ok    greenfield AGENTS.md is not a generated regular file
  ok    greenfield signoff is not a generated regular file
  ok    greenfield target has no material/ tree
  ok    greenfield creates a mount symlink
  ok    greenfield mount symlink points at the external target
  ok    linked mounted project is discoverable as a child node
  ok    home resolve maps a target root to its mounted node path
  ok    home resolve maps a path inside the target to its mounted node path
  ok    home resolve without a path uses the current working directory
  ok    home resolve rejects paths outside mounted nodes
  ok    home resolve explains paths outside mounted nodes
  ok    greenfield does not copy root methodology prose
  ok    greenfield does not copy the root check script
  ok    greenfield does not copy the root adapter directory
  ok    greenfield does not copy the root bin directory
  ok    greenfield does not link the root AGENTS.md entry point
  ok    greenfield uses the mounted signoff entry point instead of copying root signoff
root - home mounted nodes
  ok    home/check-hypercore-home-check.oR1Ict target is a git repository
  ok    home/check-hypercore-home-check.oR1Ict AGENTS.md points at the root-managed mounted Codex entrypoint
  ok    home/check-hypercore-home-check.oR1Ict AGENTS.md is not a generated regular file
  ok    home/check-hypercore-home-check.oR1Ict signoff points at the root-managed home signoff helper
  ok    home/check-hypercore-home-check.oR1Ict signoff entrypoint is executable
  ok    home/check-hypercore-home-check.oR1Ict signoff is not a generated regular file
root - structure
  ok    documentation tree is retired
  ok    implementation tree is retired
  ok    intent tree exists
  ok    organizing document exists
root - segments
  ok    active-work has a machine-statements file
  ok    active-work has a ## machine section
  ok    active-work is endorsed at its foot
  ok    adapter has a machine-statements file
  ok    adapter has a ## machine section
  ok    adapter is endorsed at its foot
  ok    collaboration has a machine-statements file
  ok    collaboration has a ## machine section
  ok    collaboration is endorsed at its foot
  ok    endorsement has a machine-statements file
  ok    endorsement has a ## machine section
  ok    endorsement is endorsed at its foot
  ok    foundations has a machine-statements file
  ok    foundations has a ## machine section
  ok    foundations is endorsed at its foot
  ok    home has a machine-statements file
  ok    home has a ## machine section
  ok    home is endorsed at its foot
  ok    loop has a machine-statements file
  ok    loop has a ## machine section
  ok    loop is endorsed at its foot
  ok    statements has a machine-statements file
  ok    statements has a ## machine section
  ok    statements is endorsed at its foot
  ok    structure has a machine-statements file
  ok    structure has a ## machine section
  ok    structure is endorsed at its foot
  ok    sweep has a machine-statements file
  ok    sweep has a ## machine section
  ok    sweep is endorsed at its foot
root - history
  ok    root adopted work-node history directory remains readable
  ok    root adopted work-node history directory is held by git
  ok    root adopted work-node history/001-flatten-material-tree has a scoped NNN-slug name
  ok    root adopted work-node history/001-flatten-material-tree has intent/
  ok    root adopted work-node history/001-home-greenfield-setup has a scoped NNN-slug name
  ok    root adopted work-node history/001-home-greenfield-setup has intent/
  ok    root adopted work-node history/001-remove-claude-adapter has a scoped NNN-slug name
  ok    root adopted work-node history/001-remove-claude-adapter has intent/
  ok    root adopted work-node history/002-direct-path-greenfield-adapter has a scoped NNN-slug name
  ok    root adopted work-node history/002-direct-path-greenfield-adapter has intent/
  ok    root adopted work-node history/002-simplify-methodology-doc has a scoped NNN-slug name
  ok    root adopted work-node history/002-simplify-methodology-doc has intent/
  ok    root adopted work-node history/003-phase-two-observability has a scoped NNN-slug name
  ok    root adopted work-node history/003-phase-two-observability has intent/
  ok    root adopted work-node history/004-root-managed-greenfield-entrypoints has a scoped NNN-slug name
  ok    root adopted work-node history/004-root-managed-greenfield-entrypoints has intent/
  ok    root adopted work-node history/005-harden-loop-collaboration has a scoped NNN-slug name
  ok    root adopted work-node history/005-harden-loop-collaboration has intent/
  ok    root adopted work-node history/006-collaboration-deliberation has a scoped NNN-slug name
  ok    root adopted work-node history/006-collaboration-deliberation has intent/
  ok    root adopted work-node history/007-phase-one-collaboration has a scoped NNN-slug name
  ok    root adopted work-node history/007-phase-one-collaboration has intent/
  ok    root adopted work-node history/008-phase-two-acceptance has a scoped NNN-slug name
  ok    root adopted work-node history/008-phase-two-acceptance has intent/
  ok    root adopted work-node history/009-operator-acts has a scoped NNN-slug name
  ok    root adopted work-node history/009-operator-acts has intent/
  ok    root adopted work-node history/010-phase-two-performance has a scoped NNN-slug name
  ok    root adopted work-node history/010-phase-two-performance has intent/
  ok    root shelved work-node history directory remains readable
  ok    root shelved work-node history directory is held by git
011-phase-one-routing - structure
  ok    documentation tree is retired
  ok    implementation tree is retired
  ok    intent tree exists
  ok    organizing document exists
011-phase-one-routing - segments
011-phase-one-routing - history
999-check-loop-frame-contract-578907 - structure
  ok    documentation tree is retired
  ok    implementation tree is retired
  ok    intent tree exists
  ok    organizing document exists
999-check-loop-frame-contract-578907 - segments
999-check-loop-frame-contract-578907 - history
999-check-loop-frame-contract-580418 - structure
  ok    documentation tree is retired
  ok    implementation tree is retired
  ok    intent tree exists
  ok    organizing document exists
999-check-loop-frame-contract-580418 - segments
999-check-loop-frame-contract-580418 - history
home/check-hypercore-home-check.oR1Ict - structure
  ok    documentation tree is retired
  ok    implementation tree is retired
  ok    intent tree exists
  ok    organizing document exists
home/check-hypercore-home-check.oR1Ict - segments
home/check-hypercore-home-check.oR1Ict - history
home - structure
  ok    documentation tree is retired
  ok    implementation tree is retired
  ok    intent tree exists
  ok    organizing document exists
home - segments
  ok    mounting has a machine-statements file
  ok    mounting has a ## machine section
  ok    mounting is endorsed at its foot
home - history

all structural statements hold - root and every current child node.

exec
/bin/bash -lc "sed -n '1,80p' 011-phase-one-routing/intent/frame/signoff.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# signoff - 011-phase-one-routing

signed-off-by: qqp-dev
signed-off-at: 2026-06-08T00:22:49Z
operator-gate: tty

exec
/bin/bash -lc "nl -ba intent/collaboration.md | sed -n '1,60p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
     1	# collaboration
     2	
     3	operator-machine collaboration is a first-class methodology concern, separate from the loop mechanics that enforce it.
     4	collaboration is the working relation by which operator and machine keep the work scrutable, sound, and fast across memoryless sessions.
     5	effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
     6	collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
     7	phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
     8	the phase-one collaborator is the harness role that drives orient and frame: it carries
     9	operator-facing judgment, surfaces understanding and options, and frames the signed route.
    10	phase-one corpus-throughput work -- research, the orient corpus read, and the sweep map --
    11	may be delegated by the collaborator when written ground preserves accountability and
    12	operator direction.
    13	before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
    14	one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
    15	the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
    16	optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
    17	for one-way work, the strong review floor that scrutinizes a frame is independent of the
    18	collaborator that framed it; the framer is not its own witness.
    19	review quality is not proved by artifact scanning; review artifacts record structured signal, unresolved flags, and disposition.
    20	direction and sign-off are the two anchored operator acts in phase one, and the machine performs neither for itself.
    21	operator direction is substantive: it records a selected route, constraint, or explicit delegation with `direction-by:`.
    22	sign-off attests informed expectation and understanding, but it still requires the complete lean frame and required phase-one acts; it is not earned by bloated field scanning.
    23	a legitimate helper-written operator act crosses an operator gate that reads its decisive token from `/dev/tty` and records `operator-gate: tty`, staying simple enough that the operator confirms rather than transcribes.
    24	direction is a real operator choice: when the frame offers neutral, materially distinct numbered options, the helper copies the operator's selected option verbatim into `direction.md`; the machine may draft options but never chooses one for the operator.
    25	sign-off is informed at the moment of attestation: the helper renders the signed frame's route, acceptance condition, observable acceptance, excluded interpretation, reversibility, and target segments before it reads the confirming token.
    26	`operator-gate: tty` is a terminal-liveness marker for the helper path that the default machine command path lacks; it is not cryptographic non-repudiation, tamper-evidence, file integrity, or proof an operator rather than a deliberately allocated terminal answered.
    27	collaboration calibrates reliance: the machine makes its capabilities, limits, uncertainty, evidence, and failure modes visible enough for the operator to judge when to rely on it, challenge it, redirect it, or stop it.
    28	collaboration preserves operator agency without wasting motion: the machine asks before settling open direction or choices the artifacts cannot ground, and proceeds without interruption when the signed frame, intent, and checks give it enough written ground.
    29	phase-two acceptance is an operator-reliance concern, not only loop mechanics: before one-way adoption stamps the operator's endorsement, the machine makes the built result independently checkable against what the operator signed.
    30	implementation-acceptance scrutiny is independent of the builder's attestation; the builder does not become the witness that proves its own one-way archive.
    31	unresolved implementation-acceptance `FLAG`s are feedback material: they block archive and surface to the operator rather than being self-cleared, averaged away, outvoted, or treated as warnings.
    32	implementation-acceptance signal is legible: a required acceptance verdict carries a parseable `PASS` or `FLAG` plus rationale and concrete evidence enough for the operator or a later machine to act on a `FLAG`; uncertainty still flags, and legibility makes the door actionable without weakening it.
    33	build retry is bounded proof-floor recovery, not a structural re-decision: a builder may re-attempt a failed unit within the signed route, but structural mismatches, tier-two `FLAG`s, and an exhausted escalation budget still surface to the operator rather than being retried away.
    34	collaboration treats feedback as material: operator corrections, machine-discovered facts, failed checks, and sweep flags become intent, proof, machine statements, or debt rather than remaining transient chat.
    35	collaboration degrades gracefully: when written ground is insufficient, the machine records the blocker and decision surface and stops rather than fabricating content.
    36	
    37	## machine
    38	phase-two handoff state is written as common ground for the operator and later tooling:
    39	the addressed work's current or recent gate, current unit, status, harness session id, latest
    40	message, failure reason, event history, run artifact paths, and phase-two acceptance
    41	artifact paths are recoverable from loop state files.
    42	
    43	---
    44	endorsed by qqp-dev

exec
/bin/bash -lc "nl -ba adapter/loop.sh | sed -n '30,45p;2648,2662p;2998,3012p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    30	#   loop.sh [-C <node-path>] execute  <work-name> [--dry-run]  run phase two on a cleared session
    31	#   loop.sh [-C <node-path>] status   [--json] <work-name>     print the work node's current phase
    32	#
    33	# Env:
    34	#   LOOP_HARNESS=codex (default and only supported phase-two harness)
    35	#   HYPERCORE_LOOP_STATE_DIR (default: .hypercore/loop-runs under the root)
    36	#   HYPERCORE_OPERATOR (optional sign-off identity when <operator> is omitted)
    37	#   CODEX_BIN (default: codex), CODEX_APPROVAL (default: never)
    38	#   CODEX_WRITE_SANDBOX (default: workspace-write), CODEX_READ_SANDBOX (default: read-only)
    39	#   CODEX_BUILDER_MODEL (default: gpt-5.5 until the two-step plan/build lands), CODEX_BUILDER_EFFORT (default: xhigh)
    40	#   CODEX_STRONG_BUILDER_MODEL (optional strong-builder escalation model)
    41	#   CODEX_STRONG_BUILDER_EFFORT (default: CODEX_REVIEW_EFFORT or xhigh)
    42	#   CODEX_REVIEW_MODEL (optional strong review/acceptance model), CODEX_REVIEW_EFFORT (default: xhigh)
    43	#   HYPERCORE_PHASE_TWO_DRY_RUN_ACCEPTANCE_DIR (optional stable dry-run acceptance/cache dir for self-tests)
    44	
    45	set -euo pipefail
  2648	
  2649	codex_route_model_and_effort() {
  2650	  local route=$1 model="" effort=""
  2651	  case "$route" in
  2652	    builder-fast)
  2653	      model="${CODEX_BUILDER_MODEL:-gpt-5.5}"
  2654	      effort="${CODEX_BUILDER_EFFORT:-xhigh}"
  2655	      codex_add_model_and_effort_args "$model" "$effort" CODEX_BUILDER_MODEL CODEX_BUILDER_EFFORT
  2656	      ;;
  2657	    builder-strong)
  2658	      model="${CODEX_STRONG_BUILDER_MODEL:-${CODEX_REVIEW_MODEL:-${CODEX_MODEL:-}}}"
  2659	      effort="${CODEX_STRONG_BUILDER_EFFORT:-${CODEX_REVIEW_EFFORT:-xhigh}}"
  2660	      codex_add_model_and_effort_args "$model" "$effort" CODEX_STRONG_BUILDER_MODEL CODEX_STRONG_BUILDER_EFFORT
  2661	      ;;
  2662	    default)
  2998	}
  2999	
  3000	validate_review_model() {
  3001	  local model=${CODEX_REVIEW_MODEL:-}
  3002	  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
  3003	  validate_codex_model_var CODEX_REVIEW_MODEL "$model"
  3004	  validate_codex_effort_var CODEX_REVIEW_EFFORT "$effort"
  3005	}
  3006	
  3007	codex_add_review_route_args() {
  3008	  local model=${CODEX_REVIEW_MODEL:-}
  3009	  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
  3010	  validate_review_model
  3011	  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
  3012	  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")

exec
/bin/bash -lc "nl -ba intent/loop.md | sed -n '55,90p;155,180p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    55	`independent-coherence`, `security-permissions`, and `red-team`.
    56	the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
    57	this does not solve the deeper semantic-indexing problem.
    58	missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
    59	acceptance reviewer output counts as `FLAG`.
    60	acceptance artifacts record their source as real reviewer, dry-run/self-test, or
    61	fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
    62	fake-source required acceptance.
    63	phase-one labor may be routed by role: the collaborator drives operator-facing orient and
    64	frame work, corpus-throughput work may be delegated, and the collaborator may differ from
    65	the phase-two executor harness while phase-one review stays on the strong review floor.
    66	the collaborator role defaults to the interactive harness that loaded the adapter.
    67	phase-two builders may be routed separately from reviewers through a fast-builder model
    68	knob, while tier-one acceptance, tier-two acceptance, and phase-one review stay on the
    69	strong review floor; the fast-builder default is held at the strong model until the
    70	two-step plan/build work lands.
    71	a unit build attempts the fast builder first, retries a failed unit up to three fast
    72	attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
    73	builder after the fast budget, and returns to the operator if the strong attempt still
    74	fails.
    75	execute is resumable from the signed frame and on-disk artifacts: a passed unit's build and
    76	tier-one evidence is reused only when its cache key still matches the signed frame, unit
    77	proof obligation, relevant prior-unit state, loop implementation version, recorded diff, and
    78	green mechanical-check evidence, and a cache miss rebuilds the unit and invalidates
    79	downstream unit evidence.
    80	unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
    81	work node remains in flight for the operator.
    82	the checks re-run for every statement, not only the ones a work node touched.
    83	drift is a check that falls without work meaning to break it, and it surfaces wherever it
    84	happens.
    85	archive: adopt or shelve the work according to the signed frame.
    86	one-way archive cannot fold or stamp until required implementation-acceptance artifacts
    87	are present and clean.
    88	adoption folds accepted child statements and material into the parent, stamps each touched
    89	segment's foot with this operator, and records the work node as adopted history.
    90	shelving records the work node as shelved history without changing parent truth.
   155	`direction.md`, `review.md`, and `signoff.md` do not satisfy ordinary frame fields.
   156	new work frame completeness requires these recoverable fields: addressed node,
   157	node-local work name, target segments, work in flight, problem, constraints, decision
   158	surface or open direction, reversibility, route, acceptance condition, observable
   159	acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
   160	`reversibility:` is parsed as exactly `one-way` or `two-way`.
   161	`loop.sh start <work-name>` scaffolds `intent/frame/frame.md` with the lean fields.
   162	`loop.sh frame` and `loop.sh signoff` block new work whose frame is incomplete, whose
   163	direction is absent or malformed, whose direction appears retrospective, whose new-work
   164	direction or sign-off lacks the `operator-gate: tty` marker, or whose one-way frame lacks a
   165	review artifact.
   166	one-way review artifacts record base-role verdicts, unresolved flags, and disposition;
   167	optional reviewer verdicts cannot clear unresolved base-roster or red-team flags.
   168	new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
   169	the work node's `intent/frame/signoff.md`.
   170	`loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
   171	fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
   172	verdict artifacts under the work frame.
   173	`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
   174	the strong model until the two-step plan/build work lands, separately from the strong
   175	review route; it gives each unit a three-attempt fast-builder budget, escalates an
   176	exhausted unit through the strong-builder model knob, and stops for the operator when the
   177	strong builder fails.
   178	`loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
   179	approval `never` and literal sandbox `read-only`.
   180	`loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,

exec
/bin/bash -lc "nl -ba intent/adapter.md | sed -n '15,75p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    15	the rigid workflow is interactive through orient and frame as the design phase, and through
    16	sign-off as the human gate: before a route is written, the machine surfaces understanding,
    17	alternative framing, information-gain questions, reversibility, review where required, and
    18	a decision surface for substantive operator direction; after sign-off, implement, check,
    19	and archive run through cleared sessions that re-derive each unit and acceptance review
    20	from the signed frame directory and lean phase-two handoff artifacts alone.
    21	direction and review are phase-one acts or artifacts, not loop gates.
    22	the review roster for one-way phase-one work has a base roster of
    23	`contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
    24	the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
    25	the tier-two implementation-acceptance panel for one-way work has required lenses
    26	`whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
    27	`security-permissions`, and `red-team`.
    28	the complete optional review roster is `implementation-maintainability`,
    29	`security-permissions`, `operator-ergonomics`, `migration-compatibility`,
    30	`domain-evidence`, and `performance-cost`.
    31	optional reviewers are advisory additions and cannot override, outvote, average away, or
    32	dilute unresolved base-roster or red-team flags.
    33	the adapter classifies the request surface before changing material: ordinary
    34	conversation and read-only inspection may proceed directly, while governed work starts or
    35	continues a work node.
    36	the adapter rejects perceived simplicity, file count, convenience, and low risk as waivers
    37	for governed work.
    38	on request the adapter renders a statement of the intent intelligible in plain language
    39	without altering it.
    40	the adapter carries only what the intent cannot yet reach the harness with -- the order to
    41	read the intent first, and disciplines not yet written as statements; each is a debt,
    42	folded into the intent by later work and then dropped.
    43	an adapter is per harness; one node may be bound by more than one, each loaded by its own
    44	harness.
    45	an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
    46	and the current materialization binds one harness to both phases.
    47	the phase-one collaborator role defaults to the interactive harness that loaded the
    48	adapter; no orchestrator routing knob is required until a materialization routes that role.
    49	the adapter material is materialized only at the methodology root, with the prose it routes
    50	to, and not in any nested node; a mounted external project may carry a target-local entry
    51	point that links to root-managed adapter material and routes direct-path work back to the
    52	root adapter and loop.
    53	the adapter is not in the orient path; loading it is how orient begins, not part of the
    54	intent it routes to.
    55	the sweep reads the adapter against the intent, so a rule it has come to restate, or a debt
    56	the intent has since absorbed, is caught as drift.
    57	
    58	## machine
    59	the current root harness adapter is materialized as `adapter/codex.md`.
    60	the current materialization binds the same harness to phase one and phase two; the
    61	phase-one collaborator is the interactive harness that loaded the adapter.
    62	the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
    63	the root entry is the harness's mandated pointer, holding nothing, not where the adapter
    64	lives.
    65	a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
    66	project instruction chain from the project root to the current directory, so no node below
    67	the root carries its own adapter material.
    68	a mounted external project may carry a target-local `AGENTS.md` entry point for
    69	direct-path openings; the entry point links to root-managed adapter material and routes
    70	back to the root adapter and loop instead of copying root adapter material into the
    71	mounted node.
    72	the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    73	over the phase-two executor harness: each implementation unit opens a fresh builder
    74	session from the signed frame, and acceptance reviewers and the archive actor are fresh
    75	sessions rather than resumes of the builder.

exec
/bin/bash -lc "nl -ba check.sh | sed -n '68,239p;1388,1418p;2378,2394p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    68	  fi
    69	}
    70	
    71	contract_statement_product_absence_errors() {
    72	  local file=$1 scope=$2
    73	  HYPERCORE_CONTRACT_SCOPE="$scope" perl -0ne '
    74	    my $scope = $ENV{HYPERCORE_CONTRACT_SCOPE} || "all";
    75	    my $text = $_;
    76	
    77	    if ($scope eq "hypercore-adapter") {
    78	      if ($text =~ /^## adapter\n(.*?)(?=^## |\z)/ms) {
    79	        $text = $1;
    80	      } else {
    81	        print "$ARGV: missing ## adapter section\n";
    82	        exit 1;
    83	      }
    84	    } elsif ($scope eq "organizing-adapter") {
    85	      my @kept;
    86	      my $taking = 0;
    87	      for my $line (split /\n/, $text) {
    88	        if ($line =~ /^- \*\*adapter\*\*/) {
    89	          $taking = 1;
    90	        } elsif ($taking && $line =~ /^\s*$/) {
    91	          last;
    92	        }
    93	        push @kept, $line if $taking;
    94	      }
    95	      if (!@kept) {
    96	        print "$ARGV: missing adapter bullet\n";
    97	        exit 1;
    98	      }
    99	      $text = join("\n", @kept) . "\n";
   100	    }
   101	
   102	    my %allowed = map { $_ => 1 } (
   103	      "adapter/codex.md",
   104	      "AGENTS.md",
   105	      "adapter/codex-mounted.md",
   106	      "adapter/loop.sh",
   107	    );
   108	    my @spans;
   109	    while ($text =~ /`([^`\n]+)`/g) {
   110	      push @spans, [$-[1], $+[1], $1];
   111	    }
   112	
   113	    my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
   114	    while ($text =~ /$product/g) {
   115	      my ($start, $end, $token) = ($-[0], $+[0], $&);
   116	      my $ok = 0;
   117	      for my $span (@spans) {
   118	        if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) {
   119	          $ok = 1;
   120	          last;
   121	        }
   122	      }
   123	      next if $ok;
   124	      my $prefix = substr($text, 0, $start);
   125	      my $line = 1 + ($prefix =~ tr/\n//);
   126	      print "$ARGV:$line: product token \"$token\" is outside a whitelisted materialization pointer\n";
   127	      exit 1;
   128	    }
   129	  ' "$file"
   130	}
   131	
   132	contract_statement_product_absence() {
   133	  local file=$1 scope=$2 label=$3 output status
   134	  output="$(contract_statement_product_absence_errors "$file" "$scope" 2>&1)"
   135	  status=$?
   136	  if [ $status -eq 0 ]; then
   137	    ok "$label"
   138	  else
   139	    bad "$label ($output)"
   140	  fi
   141	  return $status
   142	}
   143	
   144	check_contract_statement_product_absence_self_tests() {
   145	  local tmp forbidden pointer organizing
   146	
   147	  echo "root - contract statement product grammar self-test"
   148	  tmp="$(mktemp -d "${TMPDIR:-/tmp}/hypercore-contract-product-check.XXXXXX")" \
   149	    || { bad "contract product grammar self-test can create temporary space"; return; }
   150	
   151	  forbidden="$tmp/forbidden.md"
   152	  cat > "$forbidden" <<'EOF'
   153	# fixture
   154	
   155	the Codex review floor is named in a contract statement.
   156	EOF
   157	  if ( fail=0; contract_statement_product_absence "$forbidden" all \
   158	    "forbidden product token fixture" >"$tmp/forbidden.out" 2>&1 ); then
   159	    bad "contract product grammar rejects an unwhitelisted harness-product token"
   160	  else
   161	    ok "contract product grammar rejects an unwhitelisted harness-product token"
   162	  fi
   163	  require_text "$tmp/forbidden.out" \
   164	    'product token "Codex" is outside a whitelisted materialization pointer' \
   165	    "contract product grammar failure names the forbidden token"
   166	
   167	  pointer="$tmp/pointer.md"
   168	  cat > "$pointer" <<'EOF'
   169	# fixture
   170	
   171	the current root harness adapter is materialized as `adapter/codex.md`.
   172	EOF
   173	  if ( fail=0; contract_statement_product_absence "$pointer" all \
   174	    "whitelisted materialization pointer fixture" >"$tmp/pointer.out" 2>&1 ); then
   175	    ok "contract product grammar accepts a whitelisted materialization pointer"
   176	  else
   177	    bad "contract product grammar accepts a whitelisted materialization pointer"
   178	  fi
   179	
   180	  organizing="$tmp/organizing-document.md"
   181	  cat > "$organizing" <<'EOF'
   182	# organizing document
   183	
   184	- **adapter** -- the binding between a harness and the loop, materialized through `adapter/codex.md`.
   185	
   186	The **governed work** -- durable child nodes and mounted work under this root:
   187	
   188	- **home** -- home currently mounts codex-cockpit.
   189	EOF
   190	  if ( fail=0; contract_statement_product_absence "$organizing" organizing-adapter \
   191	    "out-of-scope governed-work product mention fixture" >"$tmp/organizing.out" 2>&1 ); then
   192	    ok "contract product grammar ignores out-of-scope governed-work child-node names"
   193	  else
   194	    bad "contract product grammar ignores out-of-scope governed-work child-node names"
   195	  fi
   196	
   197	  require_text "$root/intent/collaboration.md" \
   198	    "the phase-one collaborator is the harness role that drives orient and frame" \
   199	    "phase-one routing self-test sees the collaborator role assertion"
   200	  require_text "$root/intent/collaboration.md" \
   201	    "phase-one corpus-throughput work" \
   202	    "phase-one routing self-test sees the throughput-delegation assertion"
   203	  require_text "$root/intent/collaboration.md" \
   204	    "the framer is not its own witness" \
   205	    "phase-one routing self-test sees the independent-review-floor assertion"
   206	  require_text "$root/intent/loop.md" \
   207	    "phase-one labor may be routed by role" \
   208	    "phase-one routing self-test sees the phase-one routing assertion"
   209	  require_text "$root/intent/loop.md" \
   210	    "the collaborator role defaults to the interactive harness that loaded the adapter" \
   211	    "phase-one routing self-test sees the collaborator held default"
   212	  require_text "$root/intent/loop.md" \
   213	    "the fast-builder default is held at the strong model" \
   214	    "phase-one routing self-test sees the builder held default"
   215	  require_text "$root/intent/loop.md" \
   216	    "phase-one review stay on the" \
   217	    "phase-one routing self-test sees the review-floor held default"
   218	  require_text "$root/intent/adapter.md" \
   219	    "the phase-one collaborator role defaults to the interactive harness" \
   220	    "phase-one routing self-test sees the adapter collaborator default"
   221	  require_text "$root/adapter/codex.md" \
   222	    "to the interactive Codex harness that loaded this adapter" \
   223	    "phase-one routing self-test sees the current binding collaborator default"
   224	  require_text "$root/adapter/loop.sh" \
   225	    'CODEX_REVIEW_EFFORT:-xhigh' \
   226	    "phase-one routing self-test sees the review-effort held default"
   227	  require_text "$root/adapter/loop.sh" \
   228	    'CODEX_BUILDER_MODEL:-gpt-5.5' \
   229	    "phase-one routing self-test sees the builder-model held default"
   230	  require_text "$root/adapter/loop.sh" \
   231	    'CODEX_BUILDER_EFFORT:-xhigh' \
   232	    "phase-one routing self-test sees the builder-effort held default"
   233	
   234	  rm -rf "$tmp"
   235	}
   236	
   237	shopt -s nullglob
   238	HOME_GREENFIELD_CHECK_TMP=
   239	HOME_GREENFIELD_CHECK_MOUNT=
  1388	  write_fake_status "$fake_check/unit-001-fast-2" 0
  1389	  write_fake_status "$fake_check/unit-001-fast-3" 0
  1390	  write_fake_status "$fake_check/unit-001-strong-1" 0
  1391	  write_acceptance_output "$fake_acceptance/tier-one-unit-001-fast-2" FLAG \
  1392	    "fast attempt 2 fixture keeps the unit unaccepted" \
  1393	    "tier-one fixture for fast attempt 2"
  1394	  write_acceptance_output "$fake_acceptance/tier-one-unit-001-fast-3" FLAG \
  1395	    "fast attempt 3 fixture exhausts the fast budget" \
  1396	    "tier-one fixture for fast attempt 3"
  1397	  write_acceptance_output "$fake_acceptance/tier-one-unit-001-strong-1" PASS \
  1398	    "strong attempt fixture accepts the escalated unit" \
  1399	    "tier-one fixture for strong attempt 1"
  1400	  write_lean_frame "$route_with_one_unit" two-way
  1401	  write_signoff
  1402	  if HYPERCORE_LOOP_STATE_DIR="$tmp/loop-runs" \
  1403	    HYPERCORE_BUILDER_FAKE_DIR="$fake_builder" \
  1404	    HYPERCORE_CHECK_FAKE_DIR="$fake_check" \
  1405	    HYPERCORE_ACCEPTANCE_FAKE_DIR="$fake_acceptance" \
  1406	    CODEX_STRONG_BUILDER_MODEL="gpt-5.3-codex" \
  1407	    "$root/adapter/loop.sh" execute "$name" --dry-run >"$tmp/retry-escalation.out" 2>"$tmp/retry-escalation.err"; then
  1408	    ok "loop execute retries three fast builders then accepts a strong-builder escalation"
  1409	  else
  1410	    bad "loop execute retries three fast builders then accepts a strong-builder escalation"
  1411	  fi
  1412	  require_text "$tmp/retry-escalation.out" "-m gpt-5.5" \
  1413	    "fast builder dry-run command uses the gpt-5.5 builder default"
  1414	  require_text "$tmp/retry-escalation.out" "model_reasoning_effort=\\\"xhigh\\\"" \
  1415	    "fast builder dry-run command uses the builder effort default"
  1416	  require_text "$tmp/retry-escalation.out" "-m gpt-5.3-codex" \
  1417	    "strong builder dry-run command uses the strong-builder model knob"
  1418	  require_text "$tmp/retry-escalation.out" "fast builder attempt 1 for unit-001 failed: check.sh red" \
  2378	  "acceptance reviewer subprocesses are timeout bounded"
  2379	require_text "$root/adapter/loop.sh" \
  2380	  'validate_review_model' \
  2381	  "loop validates CODEX_REVIEW_MODEL"
  2382	require_text "$root/adapter/loop.sh" \
  2383	  'CODEX_REVIEW_EFFORT:-xhigh' \
  2384	  "loop keeps review effort strong by default"
  2385	require_text "$root/adapter/loop.sh" \
  2386	  'CODEX_BUILDER_MODEL:-gpt-5.5' \
  2387	  "loop defaults fast builders to gpt-5.5 until the two-step plan/build lands"
  2388	require_text "$root/adapter/loop.sh" \
  2389	  'CODEX_BUILDER_EFFORT:-xhigh' \
  2390	  "loop applies a separate builder effort default"
  2391	require_text "$root/adapter/loop.sh" \
  2392	  'CODEX_STRONG_BUILDER_MODEL' \
  2393	  "loop exposes a strong-builder escalation model knob"
  2394	require_text "$root/adapter/loop.sh" \

exec
/bin/bash -lc 'git --no-pager status --short' in /home/qqp/projects/hypercore
 succeeded in 0ms:
A  011-phase-one-routing/intent/frame/direction.md
A  011-phase-one-routing/intent/frame/frame.md
A  011-phase-one-routing/intent/frame/options.md
A  011-phase-one-routing/intent/frame/review-supplementary.md
A  011-phase-one-routing/intent/frame/review.md
A  011-phase-one-routing/intent/frame/signoff.md
A  011-phase-one-routing/intent/organizing-document.md
 M adapter/codex.md
 M adapter/loop.sh
 M check.sh
 M hypercore.md
 M intent/adapter.md
 M intent/collaboration.md
 M intent/loop.md
 M intent/machine-statements/adapter.md
 M intent/machine-statements/collaboration.md
 M intent/machine-statements/loop.md
 M intent/organizing-document.md
?? 011-phase-one-routing/intent/frame/phase-two/
?? DECOMPOSITION-FINDINGS.md
?? TWO-STEP-BUILD-FINDINGS.md
?? WORK-NODE-COLLAPSE-FINDINGS.md

exec
/bin/bash -lc 'rg -n "Current Harness Binding|strong review floor|phase-one review reviewer" adapter/codex.md' in /home/qqp/projects/hypercore
 succeeded in 0ms:
18:## Current Harness Binding
133:- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned

exec
/bin/bash -lc 'rg -n "adapter/codex.md|codex-cockpit|AGENTS.md|adapter/loop.sh" hypercore.md intent/organizing-document.md intent/adapter.md intent/machine-statements/adapter.md' in /home/qqp/projects/hypercore
 succeeded in 0ms:
intent/machine-statements/adapter.md:3:the current root harness adapter is materialized as `adapter/codex.md`.
intent/machine-statements/adapter.md:6:the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
intent/machine-statements/adapter.md:9:a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
intent/machine-statements/adapter.md:12:a mounted external project may carry a target-local `AGENTS.md` entry point for
intent/machine-statements/adapter.md:16:the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
intent/machine-statements/adapter.md:30:`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
intent/organizing-document.md:22:  the root by the methodology prose, the harness entry point (`AGENTS.md`), the current
intent/organizing-document.md:23:  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.
intent/organizing-document.md:28:  project nodes and governs them within itself. home currently mounts `codex-cockpit`.
hypercore.md:259:For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
intent/adapter.md:59:the current root harness adapter is materialized as `adapter/codex.md`.
intent/adapter.md:62:the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
intent/adapter.md:65:a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
intent/adapter.md:68:a mounted external project may carry a target-local `AGENTS.md` entry point for
intent/adapter.md:72:the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
intent/adapter.md:86:`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.

exec
/bin/bash -lc "nl -ba adapter/codex.md | sed -n '15,42p;126,138p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    15	gates unskippable. Pointing alone is a request; the orchestrator is how agreement is
    16	kept.
    17	
    18	## Current Harness Binding
    19	
    20	The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
    21	`adapter/codex.md`; it is the harness-mandated pointer and not where the adapter lives.
    22	Nested work under this root receives that entry point through the project instruction
    23	chain, so nested nodes do not carry their own adapter material.
    24	
    25	The current materialization binds Codex to both phase one and phase two. Phase one defaults
    26	to the interactive Codex harness that loaded this adapter. Phase two is driven by
    27	`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
    28	the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
    29	ids as current binding facts.
    30	
    31	The current materialization also keeps the `CODEX_*` environment knob names in
    32	`adapter/loop.sh`. Those names are implementation binding, while the intent states the
    33	builder-model, strong-builder, review-model, and review-effort roles.
    34	
    35	## Orient before you touch anything
    36	
    37	First classify the request surface. Ordinary conversation, explanation, and read-only
    38	inspection can proceed directly when they do not need adoption or shelving. Governed work
    39	starts or continues a work node before material changes; perceived simplicity, small file
    40	count, convenience, or low risk never waives the loop for governed work.
    41	
    42	Read, in this order. This is where orient begins:
   126	Each line is a **debt**: carried here only until a later change folds it into the intent
   127	as a checked statement, then dropped.
   128	
   129	- **Never fabricate content.** An unmaterialized child node is a dormant slot — a real,
   130	  empty node — not a fake app with invented sub-projects.
   131	- **Name in hypercore's own vocabulary** — node, segment, contract, mount, materialize,
   132	  the loop. Reject domain words that collide with the methodology's own concepts.
   133	- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
   134	  to a checked strong model; it can still ride an ambient harness default. A future loop
   135	  pins it.
   136	- **Re-prompt phase-one one-way review.** The current phase-one one-way review reviewer
   137	  prompt assumes a signed, route-settled frame and therefore cannot PASS a correctly staged
   138	  pre-direction frame. A future loop re-prompts it for a pre-direction decision surface.

exec
/bin/bash -lc "nl -ba intent/organizing-document.md | sed -n '18,30p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    18	- **sweep** -- how coherence is checked across the corpus, work in flight, proposed parent
    19	  amendments, and node boundaries.
    20	- **adapter** -- the binding between a harness and the loop: what the harness loads at the
    21	  start of work, promising agreement and enforcing it as a rigid workflow. Materialized at
    22	  the root by the methodology prose, the harness entry point (`AGENTS.md`), the current
    23	  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.
    24	
    25	The **governed work** -- durable child nodes and mounted work under this root:
    26	
    27	- **home** -- the named child node at `home/`, with its own `intent/`, that mounts linked
    28	  project nodes and governs them within itself. home currently mounts `codex-cockpit`.
    29	
    30	Each segment has an intent document at `intent/<segment>.md` and a machine-statements file

exec
/bin/bash -lc "nl -ba intent/machine-statements/adapter.md | sed -n '1,24p;50,70p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
     1	# adapter -- machine statements
     2	
     3	the current root harness adapter is materialized as `adapter/codex.md`.
     4	the current materialization binds the same harness to phase one and phase two; the
     5	phase-one collaborator is the interactive harness that loaded the adapter.
     6	the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
     7	the root entry is the harness's mandated pointer, holding nothing, not where the adapter
     8	lives.
     9	a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
    10	project instruction chain from the project root to the current directory, so no node below
    11	the root carries its own adapter material.
    12	a mounted external project may carry a target-local `AGENTS.md` entry point for
    13	direct-path openings; the entry point links to root-managed adapter material and routes
    14	back to the root adapter and loop instead of copying root adapter material into the
    15	mounted node.
    16	the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
    17	over the phase-two executor harness: each implementation unit opens a fresh builder
    18	session from the signed frame, and acceptance reviewers and the archive actor are fresh
    19	sessions rather than resumes of the builder.
    20	the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
    21	`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
    22	final outputs, acceptance artifact paths, and current pointers for the addressed work and
    23	root.
    24	the loop streams inner executor JSON events into the phase-two run state while
    50	acceptance condition, observable acceptance, excluded interpretation, proof state, sweep,
    51	and adoption or shelving claim in `intent/frame/frame.md`.
    52	the frame gate prompt requires substantive `intent/frame/direction.md` before route
    53	framing and requires `intent/frame/review.md` for one-way work.
    54	the frame gate prompt tells the machine not to write operator direction, not to collect
    55	direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
    56	red-team flags.
    57	the adapter prose describes phase one as design-phase collaboration with direction
    58	and review artifacts, while preserving phase two as cleared, heads-down execution from the
    59	signed frame directory and lean phase-two handoff artifacts.
    60	`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
    61	validation, start scaffolding, direction/review helpers, operator-act gating through
    62	`/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
    63	acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
    64	acceptance legibility, acceptance source markers and fake-source rejection, separate
    65	builder/reviewer routing with bounded retry and strong escalation, resumable execute
    66	caching, the concurrent tier-two panel, the new operator-act and phase-two performance
    67	contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
    68	absence of the retired compatibility route still carry the contract.
    69	each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
    70	them in the executor gate prompt; the orchestrator owns gate order and preconditions and

exec
/bin/bash -lc "nl -ba intent/machine-statements/loop.md | sed -n '1,24p;64,78p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
     1	# loop -- machine statements
     2	
     3	a work address names the addressed node and one node-local work name in that node.
     4	when no node is named, the root node is assumed.
     5	`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node.
     6	`loop.sh start <work-name>` creates a work node directly under the addressed node's
     7	corpus.
     8	`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
     9	act only on that addressed work.
    10	`loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
    11	runs and after recent failure or completion, including the active gate, status, harness
    12	session id, current unit, latest message, failure reason, event history, run artifact
    13	paths, and phase-two acceptance artifact paths.
    14	before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
    15	that the configured executor binary is present and that executor home/session state is
    16	writable; a failed preflight records failed run state and stops before the executor
    17	session starts.
    18	`loop.sh status <work-name>` reports the addressed work's current phase and, for
    19	non-historical work with phase-two state, the current or recent run's gate, status, state
    20	path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
    21	run state for tooling.
    22	from the root, `./signoff` invokes the root loop sign-off gate and preserves any explicit
    23	arguments it receives.
    24	`loop.sh signoff <work-name> <operator>` remains the explicit sign-off form, and for new
    64	direction is absent or malformed, whose direction appears retrospective, whose new-work
    65	direction or sign-off lacks the `operator-gate: tty` marker, or whose one-way frame lacks a
    66	review artifact.
    67	one-way review artifacts record base-role verdicts, unresolved flags, and disposition;
    68	optional reviewer verdicts cannot clear unresolved base-roster or red-team flags.
    69	new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
    70	the work node's `intent/frame/signoff.md`.
    71	`loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
    72	fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
    73	verdict artifacts under the work frame.
    74	`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
    75	the strong model until the two-step plan/build work lands, separately from the strong
    76	review route; it gives each unit a three-attempt fast-builder budget, escalates an
    77	exhausted unit through the strong-builder model knob, and stops for the operator when the
    78	strong builder fails.

exec
/bin/bash -lc "nl -ba hypercore.md | sed -n '250,265p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
   250	
   251	## adapter
   252	
   253	The adapter binds a harness to the methodology.
   254	
   255	```text
   256	harness loads adapter -> adapter points to intent + loop -> gates become enforceable
   257	```
   258	
   259	For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
   260	replace the intent; it routes the machine to the intent and makes the loop's gates rigid.
   261	
   262	Phase one is interactive design work. Phase two is cleared, heads-down execution from the
   263	signed frame. If a gate precondition fails, the adapter blocks instead of warning.
   264	
   265	## collisions

exec
/bin/bash -lc 'find 011-phase-one-routing/intent/frame/phase-two -maxdepth 3 -type f -print | sort' in /home/qqp/projects/hypercore
 succeeded in 0ms:
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md

exec
/bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/phase-two/units/unit-001.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# phase-two unit - unit-001

unit: unit-001
status: running
updated-at: 2026-06-08T00:23:51Z
proof-obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.
handoff-path: 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
diff-path: 011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
tier-one-verdict-path: 011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md
cache-key-path: 011-phase-one-routing/intent/frame/phase-two/cache/unit-001.key
message: fast-1 builder session starting

exec
/bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# tier-one implementation acceptance - unit-001

reviewer: tier-one-unit-001-fast-1
Verdict: PASS
source: real-reviewer
source-proof: real reviewer subprocess completed through codex exec with literal approval never and literal sandbox read-only
Rationale: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
Evidence: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.
dry-run: no
Isolation: acceptance reviewer subprocesses are invoked with literal approval never and literal sandbox read-only.
Network isolation: not claimed by this adapter; the Codex CLI invocation is not represented as proof of network isolation.
Notes: structured acceptance verdict PASS with rationale and evidence

## prompt

Implementation-acceptance reviewer: tier one
Work: 011-phase-one-routing
Node: .
Unit: unit-001
Proof obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.
Signed frame directory: 011-phase-one-routing/intent/frame
Unit handoff: 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
Unit diff record: 011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
Mechanical check immediately before this reviewer: check.sh green

Read only the signed frame, the intent it references, the unit handoff, and the unit diff record.
The unit diff record is a cumulative worktree snapshot after this unit, so it may include other already-built or planned unit changes. Check whether the handoff and proof-obligation-relevant diff content make this unit a proof-advancing delta toward the operator-signed acceptance; do not flag solely because unrelated cumulative diff hunks are present.
Return exactly these required fields, with exactly one VERDICT line:
VERDICT: PASS
RATIONALE: the frame-anchored reason for the verdict
EVIDENCE: concrete artifact paths, command results, or missing evidence that supports the verdict

Use VERDICT: FLAG instead of VERDICT: PASS when the evidence is missing, stale, uncertain, or mismatched.

Treat uncertainty, missing evidence, or mismatch with the signed frame as FLAG.

## raw output

VERDICT: PASS
RATIONALE: The unit satisfies the signed unit-001 obligation as a proof-advancing delta: it de-names the scoped contract statements, adds the phase-one collaborator/delegation/review-floor/routing statements in the owning intent files, moves current binding facts into `adapter/codex.md`, and wires `check.sh` to enforce the scoped product-absence grammar and role/default assertions.
EVIDENCE: `011-phase-one-routing/intent/frame/frame.md` and `signoff.md` anchor the route and sign-off; `phase-two/handoffs/unit-001.md` reports `bash -n check.sh` and `./check.sh` green; `phase-two/diffs/unit-001.diff` shows the relevant edits. Current scoped files contain only whitelisted product pointers by targeted `rg`: contract hits are `adapter/codex.md`/`AGENTS.md` pointers, while `codex-cockpit` is outside the scanned organizing adapter scope. `check.sh` now contains `contract_statement_product_absence`, role-presence assertions, and held-default assertions.

exec
/bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# handoff - unit-001

unit: unit-001

proof obligation: De-name the contract statements and add the phase-one roles, updating `check.sh` in lockstep so it stays green. Across `intent/collaboration.md`, `intent/loop.md`, `intent/adapter.md` and their `machine-statements/` counterparts, plus the adapter sections of `hypercore.md` and `intent/organizing-document.md`, apply the three-layer sort (methodology claim → role; capability → "the harness must support X"; current-binding fact → moved into `adapter/codex.md`); add the collaborator, throughput-delegation, review-floor-independent-of-framer, and phase-one-routing statements; and update `check.sh` to drop assertions that require the old product-named wording and add the scoped product-absence check with the pointer grammar, the role-statement-presence assertions, and the held-default assertions. `./check.sh` is green at the unit boundary.

builder-output-path: /home/qqp/projects/hypercore/.hypercore/loop-runs/20260608T002351Z-root-011-phase-one-routing-pid310606/gates/implement-unit-001-fast-1.final.md

## builder final output

Built `unit-001`.

Changed files:
`adapter/codex.md`, `check.sh`, `hypercore.md`, `intent/adapter.md`, `intent/collaboration.md`, `intent/loop.md`, `intent/machine-statements/adapter.md`, `intent/machine-statements/collaboration.md`, `intent/machine-statements/loop.md`, `intent/organizing-document.md`.

Unit artifacts written:
`011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md`
`011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff`

Prepared checks:
`bash -n check.sh`
`./check.sh` - green after handoff/diff were written.

Proof gap: none for this unit.

exec
/bin/bash -lc "sed -n '1,240p' 011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# worktree diff record

Recorded at: 2026-06-08T00:32:50Z

## status

Tracked changes only; untracked files are excluded from this unit diff record.

A  011-phase-one-routing/intent/frame/direction.md
A  011-phase-one-routing/intent/frame/frame.md
A  011-phase-one-routing/intent/frame/options.md
A  011-phase-one-routing/intent/frame/review-supplementary.md
A  011-phase-one-routing/intent/frame/review.md
A  011-phase-one-routing/intent/frame/signoff.md
A  011-phase-one-routing/intent/organizing-document.md
 M adapter/codex.md
 M check.sh
 M hypercore.md
 M intent/adapter.md
 M intent/collaboration.md
 M intent/loop.md
 M intent/machine-statements/adapter.md
 M intent/machine-statements/collaboration.md
 M intent/machine-statements/loop.md
 M intent/organizing-document.md

## diff

diff --git a/adapter/codex.md b/adapter/codex.md
index f71f4cd..5999590 100644
--- a/adapter/codex.md
+++ b/adapter/codex.md
@@ -15,6 +15,23 @@ intent and run the loop, not because you chose to, but because the workflow make
 gates unskippable. Pointing alone is a request; the orchestrator is how agreement is
 kept.
 
+## Current Harness Binding
+
+The current root binding is Codex. The root `AGENTS.md` entry point is symlinked to
+`adapter/codex.md`; it is the harness-mandated pointer and not where the adapter lives.
+Nested work under this root receives that entry point through the project instruction
+chain, so nested nodes do not carry their own adapter material.
+
+The current materialization binds Codex to both phase one and phase two. Phase one defaults
+to the interactive Codex harness that loaded this adapter. Phase two is driven by
+`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
+the archive actor; the orchestrator records raw Codex JSON event streams and Codex thread
+ids as current binding facts.
+
+The current materialization also keeps the `CODEX_*` environment knob names in
+`adapter/loop.sh`. Those names are implementation binding, while the intent states the
+builder-model, strong-builder, review-model, and review-effort roles.
+
 ## Orient before you touch anything
 
 First classify the request surface. Ordinary conversation, explanation, and read-only
diff --git a/check.sh b/check.sh
index 1f39843..9a6faca 100755
--- a/check.sh
+++ b/check.sh
@@ -68,6 +68,73 @@ reject_regular_file() {
   fi
 }
 
+contract_statement_product_absence() {
+  local file=$1 scope=$2 label=$3 output status
+  output="$(HYPERCORE_CONTRACT_SCOPE="$scope" perl -0ne '
+    my $scope = $ENV{HYPERCORE_CONTRACT_SCOPE} || "all";
+    my $text = $_;
+
+    if ($scope eq "hypercore-adapter") {
+      if ($text =~ /^## adapter\n(.*?)(?=^## |\z)/ms) {
+        $text = $1;
+      } else {
+        print "$ARGV: missing ## adapter section\n";
+        exit 1;
+      }
+    } elsif ($scope eq "organizing-adapter") {
+      my @kept;
+      my $taking = 0;
+      for my $line (split /\n/, $text) {
+        if ($line =~ /^- \*\*adapter\*\*/) {
+          $taking = 1;
+        } elsif ($taking && $line =~ /^\s*$/) {
+          last;
+        }
+        push @kept, $line if $taking;
+      }
+      if (!@kept) {
+        print "$ARGV: missing adapter bullet\n";
+        exit 1;
+      }
+      $text = join("\n", @kept) . "\n";
+    }
+
+    my %allowed = map { $_ => 1 } (
+      "adapter/codex.md",
+      "AGENTS.md",
+      "adapter/codex-mounted.md",
+      "adapter/loop.sh",
+    );
+    my @spans;
+    while ($text =~ /`([^`\n]+)`/g) {
+      push @spans, [$-[1], $+[1], $1];
+    }
+
+    my $product = qr/(?<![A-Za-z0-9_])(?:codex|claude|opus|gpt-[0-9][A-Za-z0-9._-]*|CODEX_[A-Za-z0-9_]*)(?![A-Za-z0-9_])/i;
+    while ($text =~ /$product/g) {
+      my ($start, $end, $token) = ($-[0], $+[0], $&);
+      my $ok = 0;
+      for my $span (@spans) {
+        if ($start >= $span->[0] && $end <= $span->[1] && $allowed{$span->[2]}) {
+          $ok = 1;
+          last;
+        }
+      }
+      next if $ok;
+      my $prefix = substr($text, 0, $start);
+      my $line = 1 + ($prefix =~ tr/\n//);
+      print "$ARGV:$line: product token \"$token\" is outside a whitelisted materialization pointer\n";
+      exit 1;
+    }
+  ' "$file" 2>&1)"
+  status=$?
+  if [ $status -eq 0 ]; then
+    ok "$label"
+  else
+    bad "$label ($output)"
+  fi
+}
+
 shopt -s nullglob
 HOME_GREENFIELD_CHECK_TMP=
 HOME_GREENFIELD_CHECK_MOUNT=
@@ -1696,6 +1763,55 @@ require_text "$root/intent/loop.md" \
 require_text "$root/intent/adapter.md" \
   "resumable per-unit execute cache" \
   "adapter segment folds resumable execute materialization"
+require_text "$root/intent/collaboration.md" \
+  "the phase-one collaborator is the harness role that drives orient and frame" \
+  "collaboration segment names the phase-one collaborator role"
+require_text "$root/intent/collaboration.md" \
+  "phase-one corpus-throughput work" \
+  "collaboration segment allows delegated phase-one throughput"
+require_text "$root/intent/collaboration.md" \
+  "the framer is not its own witness" \
+  "collaboration segment keeps the review floor independent of the framer"
+require_text "$root/intent/loop.md" \
+  "phase-one labor may be routed by role" \
+  "loop segment carries phase-one routing"
+require_text "$root/intent/loop.md" \
+  "the collaborator role defaults to the interactive harness that loaded the adapter" \
+  "loop segment holds the collaborator default"
+require_text "$root/intent/loop.md" \
+  "the fast-builder default is held at the strong model" \
+  "loop segment holds the builder default"
+require_text "$root/intent/loop.md" \
+  "phase-one review stay on the" \
+  "loop segment holds the strong review floor"
+require_text "$root/intent/adapter.md" \
+  "an adapter binds a harness to a phase" \
+  "adapter segment permits per-phase harness binding"
+require_text "$root/intent/adapter.md" \
+  "the phase-one collaborator role defaults to the interactive harness" \
+  "adapter segment holds the collaborator materialization default"
+require_text "$root/adapter/codex.md" \
+  "to the interactive Codex harness that loaded this adapter" \
+  "current binding records the collaborator held default"
+require_text "$root/adapter/codex.md" \
+  "builder-model, strong-builder, review-model, and review-effort roles" \
+  "current binding separates material knob names from role statements"
+contract_statement_product_absence "$root/intent/collaboration.md" all \
+  "collaboration intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/loop.md" all \
+  "loop intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/adapter.md" all \
+  "adapter intent has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/collaboration.md" all \
+  "collaboration machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/loop.md" all \
+  "loop machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/intent/machine-statements/adapter.md" all \
+  "adapter machine statements have no unscoped harness product token"
+contract_statement_product_absence "$root/hypercore.md" hypercore-adapter \
+  "hypercore adapter section has no unscoped harness product token"
+contract_statement_product_absence "$root/intent/organizing-document.md" organizing-adapter \
+  "organizing adapter bullet has no unscoped harness product token"
 [ -x "$root/check.sh" ] \
   && ok "check.sh exists and is executable" \
   || bad "check.sh is missing or not executable"
diff --git a/hypercore.md b/hypercore.md
index 9db8bab..530d5a5 100644
--- a/hypercore.md
+++ b/hypercore.md
@@ -256,8 +256,8 @@ The adapter binds a harness to the methodology.
 harness loads adapter -> adapter points to intent + loop -> gates become enforceable
 ```
 
-For Codex, the root `AGENTS.md` points at the adapter. The adapter does not replace the
-intent; it routes the machine to the intent and makes the loop's gates rigid.
+For the current binding, `AGENTS.md` points at `adapter/codex.md`. The adapter does not
+replace the intent; it routes the machine to the intent and makes the loop's gates rigid.
 
 Phase one is interactive design work. Phase two is cleared, heads-down execution from the
 signed frame. If a gate precondition fails, the adapter blocks instead of warning.
diff --git a/intent/adapter.md b/intent/adapter.md
index d7bda9c..97528c2 100644
--- a/intent/adapter.md
+++ b/intent/adapter.md
@@ -19,23 +19,22 @@ a decision surface for substantive operator direction; after sign-off, implement
 and archive run through cleared sessions that re-derive each unit and acceptance review
 from the signed frame directory and lean phase-two handoff artifacts alone.
 direction and review are phase-one acts or artifacts, not loop gates.
-the Codex review roster for one-way phase-one work has a base roster of
+the review roster for one-way phase-one work has a base roster of
 `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
-the Codex implementation-acceptance reviewer for each phase-two unit is independent and
-read-only.
-the Codex tier-two implementation-acceptance panel for one-way work has required lenses
+the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
+the tier-two implementation-acceptance panel for one-way work has required lenses
 `whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
 `security-permissions`, and `red-team`.
-the complete optional Codex review roster is `implementation-maintainability`,
+the complete optional review roster is `implementation-maintainability`,
 `security-permissions`, `operator-ergonomics`, `migration-compatibility`,
 `domain-evidence`, and `performance-cost`.
 optional reviewers are advisory additions and cannot override, outvote, average away, or
 dilute unresolved base-roster or red-team flags.
-the Codex adapter classifies the request surface before changing material: ordinary
+the adapter classifies the request surface before changing material: ordinary
 conversation and read-only inspection may proceed directly, while governed work starts or
 continues a work node.
-the Codex adapter rejects perceived simplicity, file count, convenience, and low risk as
-waivers for governed work.
+the adapter rejects perceived simplicity, file count, convenience, and low risk as waivers
+for governed work.
 on request the adapter renders a statement of the intent intelligible in plain language
 without altering it.
 the adapter carries only what the intent cannot yet reach the harness with -- the order to

exec
/bin/bash -lc 'find 011-phase-one-routing/intent/frame/phase-two -maxdepth 5 -type f -print | sort' in /home/qqp/projects/hypercore
 succeeded in 0ms:
011-phase-one-routing/intent/frame/phase-two/diffs/unit-001.diff
011-phase-one-routing/intent/frame/phase-two/handoffs/unit-001.md
011-phase-one-routing/intent/frame/phase-two/tier-one/unit-001.md
011-phase-one-routing/intent/frame/phase-two/units/unit-001.md

codex
VERDICT: PASS
RATIONALE: The built result meets the signed frame’s proof obligations: the product-absence proof is active and discriminating, `./check.sh` is green while exercising it, and the role/default assertions point to real contract statements and executable routing defaults.
EVIDENCE: `./check.sh` exited 0 and reported OK for scoped product-absence checks, forbidden-token failure, forbidden-token message, and whitelisted-pointer pass; `check.sh:71` implements the scanner and `check.sh:144` adds fail/pass fixtures; `intent/collaboration.md:8`, `intent/collaboration.md:17`, `intent/loop.md:63`, `intent/loop.md:66`, and `adapter/loop.sh:2653`/`:2659`/`:3008` carry the role, review-floor, and held-default evidence.
hook: Stop
hook: Stop Completed
tokens used
113,073
VERDICT: PASS
RATIONALE: The built result meets the signed frame’s proof obligations: the product-absence proof is active and discriminating, `./check.sh` is green while exercising it, and the role/default assertions point to real contract statements and executable routing defaults.
EVIDENCE: `./check.sh` exited 0 and reported OK for scoped product-absence checks, forbidden-token failure, forbidden-token message, and whitelisted-pointer pass; `check.sh:71` implements the scanner and `check.sh:144` adds fail/pass fixtures; `intent/collaboration.md:8`, `intent/collaboration.md:17`, `intent/loop.md:63`, `intent/loop.md:66`, and `adapter/loop.sh:2653`/`:2659`/`:3008` carry the role, review-floor, and held-default evidence.
