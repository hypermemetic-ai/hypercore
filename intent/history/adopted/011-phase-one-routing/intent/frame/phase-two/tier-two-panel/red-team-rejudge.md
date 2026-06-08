OpenAI Codex v0.137.0
--------
workdir: /home/qqp/projects/hypercore
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ea4c6-22b5-7f81-8f04-c4558b65274e
--------
user
You are the 'red-team' lens of the one-way implementation-acceptance panel for hypercore work
node 011-phase-one-routing, re-judging after a fix. Previously you FLAGGED that the product-absence
scanner used word-boundary guards, so product tokens embedded in larger identifiers
(HYPERCORE_CODEX_BUILDER_MODEL, CodexHarness, Review_GPT-5) slipped through. That has now been
changed. Re-judge against the SIGNED FRAME (011-phase-one-routing/intent/frame/frame.md), whose
acceptance condition requires the materialization-pointer grammar to have NO loophole and NO
false positives on legitimate pointers.

Read the current `check.sh` scanner `contract_statement_product_absence()` (~line 71) and its
self-tests, and `git --no-pager diff check.sh`. Verify concretely:
1. Your prior reproducers are now CAUGHT: a contract-statement file containing
   `HYPERCORE_CODEX_BUILDER_MODEL`, `CodexHarness`, or `Review_GPT-5` now FAILS the scanner.
2. No NEW false positive: legitimate text and the whitelisted backticked pointers
   (`adapter/codex.md`, `AGENTS.md`, `adapter/codex-mounted.md`, `adapter/loop.sh`) still PASS,
   and the out-of-scope `codex-cockpit` mention still PASSES. `./check.sh` is green.
3. Any OTHER remaining loophole in the grammar, or any excluded-interpretation violation
   (second executor, proof-floor demotion, materialization removal, new gate, collaborator
   producing phase-two artifacts).

Return EXACTLY:
VERDICT: PASS
RATIONALE: <frame-anchored reason>
EVIDENCE: <concrete paths / command results / findings>
Use VERDICT: FLAG instead when a real loophole or violation remains. Treat uncertainty as FLAG.
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
I’ll verify this as a read-only acceptance review: first the signed frame contract, then the scanner and its test coverage, then targeted repro commands plus the full check.
exec
/bin/bash -lc "sed -n '1,220p' check.sh" in /home/qqp/projects/hypercore
exec
/bin/bash -lc "sed -n '1,220p' hypercore.md" in /home/qqp/projects/hypercore
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

    my $product = qr/(?:CODEX_[A-Za-z0-9_]*|gpt-[A-Za-z0-9._-]*|codex|claude|opus)/i;
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
  local tmp forbidden embedded pointer organizing

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

  embedded="$tmp/embedded.md"
  cat > "$embedded" <<'EOF'
# fixture

HYPERCORE_CODEX_BUILDER_MODEL appears as an embedded identifier.
EOF
  if ( fail=0; contract_statement_product_absence "$embedded" all \
    "embedded product token fixture" >"$tmp/embedded.out" 2>&1 ); then
    bad "contract product grammar rejects an embedded harness-product token"
  else
    ok "contract product grammar rejects an embedded harness-product token"
  fi
  require_text "$tmp/embedded.out" \
    'product token "CODEX_BUILDER_MODEL" is outside a whitelisted materialization pointer' \
    "contract product grammar failure names the embedded forbidden token"

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

 succeeded in 0ms:
# hypercore

hypercore is a way to keep a growing codebase coherent when the machine starts each
session with no memory.

The method has three tests:

- **scrutable**: a reader can recover what the system means.
- **sound**: nothing important rests on unproven ground.
- **fast**: work moves in small steps with little ceremony.

When those tests pull against each other, name the tension instead of hiding the tradeoff.

```text
operator purpose + written intent + checked material
        \              |              /
         \             |             /
          ---------- hypercore -------
```

## intent

Intent is the current written model of the system: what each part is meant to be, how it
behaves, and what it depends on.

It does not carry memory or rationale. The reason a statement exists lives in the work
that made it. The proof lives in checks on the material.

```text
intent says:     what is meant to be true
work records:    why this became true
checks prove:    whether the material still holds it
```

Work starts by reading the intent and the material. If something needed is not written,
it is not assumed.

## collaboration

The operator and the machine keep common ground written, but phase one is not proved by
field count. It is an arc: understanding before route, reversibility-sized scrutiny,
operator direction, lean recoverability, then sign-off.

- The operator sets purpose, constraints, acceptance, and open direction.
- The machine searches, synthesizes, drafts, executes, checks, and settles what is left
  open.
- Before a route is written, the machine gives a teach-back, at least one alternative
  framing, information-gain questions, and a reversibility classification.
- One-way work gets a small mechanical base review roster before route settlement:
  `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
  Optional reviewers are additive and advisory only; they cannot clear unresolved base or
  red-team flags.
- Direction and sign-off are the two anchored operator acts. On the legitimate helper
  path, each act crosses an operator gate that reads the decisive token from `/dev/tty`
  and records `operator-gate: tty`; this is terminal liveness for the helper path, which
  the default machine command path lacks. It is not cryptographic non-repudiation,
  tamper-evidence, file integrity, or proof an operator rather than a deliberately
  allocated terminal answered.
- Direction records a selected route, constraint, or explicit delegation with
  `direction-by:` and `direction-given-at:`. When direction needs a route choice, the
  machine drafts neutral, materially distinct options in `intent/frame/options.md`, and
  the operator picks one; the machine never writes direction for itself.
- The machine makes uncertainty, evidence, limits, and failure modes visible enough for
  the operator to rely on it, challenge it, redirect it, or stop it.
- Sign-off attests informed expectation and understanding, and still requires a complete
  lean frame plus the required phase-one acts; it is not earned by bloated field scanning.
  The helper renders a frame-derived brief and requires the work number before writing
  `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`.
- Phase-two acceptance is part of reliance calibration: before one-way adoption stamps the
  operator's endorsement, the built result is checked independently against what the
  operator signed, with structured verdicts that include rationale and evidence.
- Unresolved implementation-acceptance flags block archive and surface to the operator
  rather than being self-cleared, averaged away, or treated as warnings.
- When written ground is insufficient, the machine records the blocker and stops instead
  of fabricating content.

Feedback becomes durable: corrections, discovered facts, failed checks, and sweep flags
become intent, proof, machine statements, or debt.

## nodes

A node is a governed corpus. The root is a node; any node-local corpus entry with
`intent/` can be a child node too.

```text
node/
  intent/
    organizing-document.md
    <segment>.md
    machine-statements/<segment>.md
    history/
  leaf material
  child nodes
  active work nodes
```

The node boundary matters. A child is free except where a parent statement explicitly
reaches into it.

```text
parent node
  statement reach:
    node-local        -> parent only
    named child       -> one child
    direct children   -> every immediate child
    descendants       -> the tree below
```

An unmaterialized child slot is dormant. Do not invent its content.

## segments

Each node chooses its own segments in `intent/organizing-document.md`.

At the methodology root, the methodology has nine segments:

- foundations
- collaboration
- structure
- statements
- endorsement
- active-work
- loop
- sweep
- adapter

The governed work group names durable child nodes and mounted work governed by this root.

Each segment has:

- `intent/<segment>.md` for current statements.
- `intent/machine-statements/<segment>.md` for machine statements.

The methodology prose is this file. The mechanical check over nodes is `check.sh`.

## statements

A statement is plain, declarative, and strong enough to be wrong.

```text
good statement:  check.sh checks every node in the tree.
weak statement:  checks should probably cover most important things.
```

One name means one concept. Behavior and dependency are both written as statements.

Every statement must be ownable and checkable. If it is neither, the work turns it away.

## ownership

Ownership is the right to change a statement, not permission to break it.

```text
endorsed statement   -> operator owned
unendorsed statement -> machine owned
```

The machine never endorses, so unendorsed statements fall to the machine by default. Both
operator and machine are still bound by coherence.

Machine freedom is taken, not declared: when the operator leaves a choice open and the
machine settles it, the machine statement records that settlement.

## endorsement

Endorsement is per segment and per node.

```text
intent/<segment>.md

... statements ...

## machine
... machine statements ...

---
endorsed by <operator>
```

Changing a segment means taking on the segment's whole operator set. There is no partial
endorsement. If a segment becomes too large to own, split it or move suitable statements
under `## machine`.

A work frame carries sign-off. On adoption, that sign-off stamps each touched segment.

## active work

Active work is a child node directly under the addressed node.

```text
002-simplify-methodology-doc/
  intent/
    frame/
```

A work node can propose parent intent or parent material amendments without making them
current. Until adoption accepts the amendment, the parent intent remains current.

Adoption folds accepted child statements and material into the parent and records history.
Shelving records history without changing parent truth.

## loop

Every work node that needs adoption or shelving goes through five gates.

```text
orient -> frame -> implement -> check -> archive
\___ phase one ___/  \______ phase two _____/
          |
       sign-off
```

- **orient**: read the intent, work in flight, and material conventions.
- **frame**: after substantive direction exists, write the problem, constraints, route,
  reversibility, acceptance condition, observable acceptance, excluded interpretation,
  proof state, target segments, work in flight, sweep, and adoption or shelving claim.
- **implement**: after sign-off, build from the written frame in green proof-advancing
  units.
- **check**: run mechanical checks and independent structured implementation acceptance;
  one-way work gets a required implementation-acceptance panel before archive, with the

exec
/bin/bash -lc "sed -n '1,220p' intent/organizing-document.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# organizing document

hypercore's intent is held in two groups of segments, one document each.

The **methodology** -- the nine segments describing the rules themselves,
leaf-materialized by `hypercore.md` and `check.sh`, divided along one axis:

- **foundations** -- the premise, the three properties, and what the intent is.
- **collaboration** -- how operator and machine work together: role partition, common
  ground, reliance calibration, control, feedback, handoff, and graceful failure.
- **structure** -- the reserved intent tree, how the corpus is laid out, and how a node
  nests inside another.
- **statements** -- what a statement is, and ownership.
- **endorsement** -- who stands behind a set, per segment and per work, and where the node
  boundary stops it.
- **active-work** -- the work-node lifecycle and the root contract for active child work.
- **loop** -- the five gates a work node goes through.
- **sweep** -- how coherence is checked across the corpus, work in flight, proposed parent
  amendments, and node boundaries.
- **adapter** -- the binding between a harness and the loop: what the harness loads at the
  start of work, promising agreement and enforcing it as a rigid workflow. Materialized at
  the root by the methodology prose, the harness entry point (`AGENTS.md`), the current
  binding (`adapter/codex.md`), and the orchestrator under `adapter/`.

The **governed work** -- durable child nodes and mounted work under this root:

- **home** -- the named child node at `home/`, with its own `intent/`, that mounts linked
  project nodes and governs them within itself. home currently mounts `codex-cockpit`.

Each segment has an intent document at `intent/<segment>.md` and a machine-statements file
at `intent/machine-statements/<segment>.md`. A child node is a directory or settled linked
entry point carrying its own `intent/`; a mounted project is a child node of home, a
separate corpus exposed through `home/<name>` as a symbolic link to its own repository.

This is two groups, not a tag: nothing is partitioned twice. A tag is added only the first
time a real second partition of the whole corpus forces it, not before.

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
/bin/bash -lc 'git --no-pager diff -- check.sh' in /home/qqp/projects/hypercore
 succeeded in 0ms:
diff --git a/check.sh b/check.sh
index 1f39843..894e1e7 100755
--- a/check.sh
+++ b/check.sh
@@ -68,6 +68,188 @@ reject_regular_file() {
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
+    my $product = qr/(?:CODEX_[A-Za-z0-9_]*|gpt-[A-Za-z0-9._-]*|codex|claude|opus)/i;
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
+  local tmp forbidden embedded pointer organizing
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
+  embedded="$tmp/embedded.md"
+  cat > "$embedded" <<'EOF'
+# fixture
+
+HYPERCORE_CODEX_BUILDER_MODEL appears as an embedded identifier.
+EOF
+  if ( fail=0; contract_statement_product_absence "$embedded" all \
+    "embedded product token fixture" >"$tmp/embedded.out" 2>&1 ); then
+    bad "contract product grammar rejects an embedded harness-product token"
+  else
+    ok "contract product grammar rejects an embedded harness-product token"
+  fi
+  require_text "$tmp/embedded.out" \
+    'product token "CODEX_BUILDER_MODEL" is outside a whitelisted materialization pointer' \
+    "contract product grammar failure names the embedded forbidden token"
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
@@ -1696,6 +1878,56 @@ require_text "$root/intent/loop.md" \
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

codex
The frame’s load-bearing point is the pointer grammar: only exact backticked materialization paths may carry product tokens in statement scope, while embedded product tokens in identifiers must still be rejected. I’m now testing the scanner itself with those exact reproducers, including the two variants not covered by the built-in embedded fixture.
exec
/bin/bash -lc "nl -ba check.sh | sed -n '60,180p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
    60	}
    61	
    62	reject_regular_file() {
    63	  local path=$1 label=$2
    64	  if [ -f "$path" ] && [ ! -L "$path" ]; then
    65	    bad "$label ($path is a regular file)"
    66	  else
    67	    ok "$label"
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
   113	    my $product = qr/(?:CODEX_[A-Za-z0-9_]*|gpt-[A-Za-z0-9._-]*|codex|claude|opus)/i;
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
   145	  local tmp forbidden embedded pointer organizing
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
   167	  embedded="$tmp/embedded.md"
   168	  cat > "$embedded" <<'EOF'
   169	# fixture
   170	
   171	HYPERCORE_CODEX_BUILDER_MODEL appears as an embedded identifier.
   172	EOF
   173	  if ( fail=0; contract_statement_product_absence "$embedded" all \
   174	    "embedded product token fixture" >"$tmp/embedded.out" 2>&1 ); then
   175	    bad "contract product grammar rejects an embedded harness-product token"
   176	  else
   177	    ok "contract product grammar rejects an embedded harness-product token"
   178	  fi
   179	  require_text "$tmp/embedded.out" \
   180	    'product token "CODEX_BUILDER_MODEL" is outside a whitelisted materialization pointer' \

exec
/bin/bash -lc "sed -n '1,260p' intent/loop.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# loop

every work node that needs adoption or shelving goes through five gates: orient, frame,
implement, check, archive.
governed work is not optional by perceived simplicity, file count, risk, or convenience
when it changes governed material or needs adoption or shelving.
orient and frame are the design phase: understanding, scrutiny, operator direction, route
framing, and sign-off happen there before phase two begins.
direction and review are phase-one acts or artifacts inside orient and frame, not new loop
gates.
when a work node's direction is still open, the machine states the problem, constraints,
decision surface, reversibility, and information needed from the operator before settling
the route.
before a route is written, governed work has substantive operator direction recorded in
`intent/frame/direction.md`.
new work that needs route selection carries `intent/frame/options.md` with neutral,
materially distinct numbered options, and the operator's direction is one option selected
through `/dev/tty` and recorded with `operator-gate: tty`.
direction and sign-off for new work are terminal-gated operator acts; the `operator-gate:`
token is `tty` today and the field stays open to a later keyed scheme such as `hmac:<...>`.
one-way work has `intent/frame/review.md` before route framing and sign-off; two-way work
skips review unless the operator requests it.
before sign-off, a new work frame carries lean recoverability fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, observable
acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
`observable acceptance` names the concrete command, state, check, or externally inspectable
condition that phase-two acceptance can test.
`excluded interpretation` names what the work must not mean.
implementation autonomy begins after sign-off: phase two builds from the signed frame in
green proof-advancing units, and stops when the frame is incomplete, a check fails, or
required implementation acceptance returns `FLAG`.
orient: read the intent documents, the work in flight across the node tree, and the
material's conventions; search the web for what you do not know; ask the operator what the
artifacts cannot tell you; do not guess.
frame: write enough of the addressed work node's intent and material to make the proposed
work scrutable, including proposed parent amendments where the work needs them, and run the
sweep over the whole corpus and work in flight across the node tree.
implement: build in proof-advancing units from the signed frame.
an implementation unit is the smallest proof-advancing delta that leaves `./check.sh`
green; units are vertical slices, so statements, material, and checks land together when
the work requires all three.
check: prove each statement with checks on the material, and run the phase-two acceptance
scrutiny required by the signed frame and reversibility.
`./check.sh` is green at every phase-two unit boundary and before any acceptance verdict
or archive fold is trusted.
after each implementation unit, a fresh independent read-only implementation-acceptance
reviewer reads the signed frame, unit proof obligation, unit diff, and lean unit handoff,
then returns a structured verdict: exactly one `PASS` or `FLAG` with required rationale and
concrete evidence.
for one-way work, a required tier-two implementation-acceptance panel runs before archive,
its lenses started concurrently after every required tier-one artifact is clean; two-way
work does not run that panel unless later intent explicitly requires it.
the one-way tier-two panel lenses are `whole-acceptance-conformance`, `proof-integrity`,
`independent-coherence`, `security-permissions`, and `red-team`.
the `independent-coherence` lens carries the semantic sweep judgement for one-way archive;
this does not solve the deeper semantic-indexing problem.
missing, malformed, nonzero, unsupported-source, evidence-free, or non-`PASS`/`FLAG`
acceptance reviewer output counts as `FLAG`.
acceptance artifacts record their source as real reviewer, dry-run/self-test, or
fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
fake-source required acceptance.
phase-one labor may be routed by role: the collaborator drives operator-facing orient and
frame work, corpus-throughput work may be delegated, and the collaborator may differ from
the phase-two executor harness while phase-one review stays on the strong review floor.
the collaborator role defaults to the interactive harness that loaded the adapter.
phase-two builders may be routed separately from reviewers through a fast-builder model
knob, while tier-one acceptance, tier-two acceptance, and phase-one review stay on the
strong review floor; the fast-builder default is held at the strong model until the
two-step plan/build work lands.
a unit build attempts the fast builder first, retries a failed unit up to three fast
attempts when `./check.sh` or tier-one acceptance fails, escalates that unit to the strong
builder after the fast budget, and returns to the operator if the strong attempt still
fails.
execute is resumable from the signed frame and on-disk artifacts: a passed unit's build and
tier-one evidence is reused only when its cache key still matches the signed frame, unit
proof obligation, relevant prior-unit state, loop implementation version, recorded diff, and
green mechanical-check evidence, and a cache miss rebuilds the unit and invalidates
downstream unit evidence.
unresolved required tier-one or tier-two `FLAG`s halt phase two before archive; the active
work node remains in flight for the operator.
the checks re-run for every statement, not only the ones a work node touched.
drift is a check that falls without work meaning to break it, and it surfaces wherever it
happens.
archive: adopt or shelve the work according to the signed frame.
one-way archive cannot fold or stamp until required implementation-acceptance artifacts
are present and clean.
adoption folds accepted child statements and material into the parent, stamps each touched
segment's foot with this operator, and records the work node as adopted history.
shelving records the work node as shelved history without changing parent truth.
large work breaks into related work at frame, and related work is an ordinary work node in
the node it alters.
a coordinating work node remains responsible for its plan: before it adopts or shelves,
related unfinished work is either resolved in its own node or carried as explicit debt.
two work nodes touching the same intent document is a smell, caused by concurrency or
orthogonality.
concurrent work is sequenced by the loop's gates: first to adopt wins, and later work builds
on the in-flight or adopted material it reads across the node tree.
an orthogonal collision is fixed in the taxonomy, preferring more documents over more
mechanism.

## machine
a work address names the addressed node and one node-local work name in that node.
when no node is named, the root node is assumed.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node.
`loop.sh start <work-name>` creates a work node directly under the addressed node's
corpus.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work and
act only on that addressed work.
`loop.sh execute <work-name>` exposes phase-two run state for the addressed work while it
runs and after recent failure or completion, including the active gate, status, harness
session id, latest message, event history, and run artifact paths.
before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
that the configured executor binary is present and that executor home/session state is
writable; a failed preflight records failed run state and stops before the executor
session starts.
`loop.sh status <work-name>` reports the addressed work's current phase and, for
non-historical work with phase-two state, the current or recent run's gate, status, state
path, event path, and latest message; `loop.sh status --json <work-name>` renders the same
run state for tooling.
from the root, `./signoff` invokes the root loop sign-off gate and preserves any explicit
arguments it receives.
`loop.sh signoff <work-name> <operator>` remains the explicit sign-off form, and for new
work it renders a concise frame-derived attestation brief through `/dev/tty`, requires the
work number as the confirming token, and writes `signed-off-by:`, `signed-off-at:`, and
`operator-gate: tty`.
`loop.sh signoff` infers the work name only when exactly one frame-complete unsigned work
node exists in the addressed node; otherwise it blocks and asks for `<work-name>`.
`loop.sh signoff` infers the operator from `HYPERCORE_OPERATOR` when set, otherwise from
the addressed node's current intent foot endorsements when exactly one operator is present;
otherwise it blocks and asks for `<operator>`.
from the root, `./direction` invokes `loop.sh direct` and preserves explicit arguments.
`loop.sh direct [<work-name> [<operator>]]` with no direction form renders the neutral
numbered options from `intent/frame/options.md` through `/dev/tty` and copies the operator's
selected option verbatim into `intent/frame/direction.md`, accepting a bare number, `n` for
none-of-these, or `q` for abort.
the explicit `loop.sh direct ... --route|--constraint|--delegate <text-or->` form is an
admin form that cannot record gated operator direction for new work; only the narrow
gate-introducing bootstrap work may record direction without the numbered selection.
`loop.sh direct` rejects empty or placeholder direction, multiple direction forms, an
existing valid direction artifact, a malformed existing direction artifact, and direction
after route content is already present.
`intent/frame/options.md` records numbered options with `kind`, `summary`, `reversibility`,
and `tradeoff`, plus `none` and `abort` rejection choices, and carries no recommendation
marker.
`direction.md` contains `direction-by:`, `direction-given-at:`, `operator-gate: tty`, and
exactly one non-placeholder `selected-route:`, `constraint:`, or `delegation:` copied from a
numbered option.
`operator-gate:` is a B-ready gate token, either `tty` or a reserved `<scheme>:<value>` such
as a later `hmac:<...>`, and only the `tty` liveness scheme is implemented.
from the root, `./review` invokes `loop.sh review` and preserves explicit arguments.
`loop.sh review <work-name> [--add <role>]...` seats the base review roster and any valid
optional complete-roster roles, then writes `intent/frame/review.md`.
new work frame completeness is checked from the canonical `intent/frame/frame.md` only;
`direction.md`, `review.md`, and `signoff.md` do not satisfy ordinary frame fields.
new work frame completeness requires these recoverable fields: addressed node,
node-local work name, target segments, work in flight, problem, constraints, decision
surface or open direction, reversibility, route, acceptance condition, observable
acceptance, excluded interpretation, proof state, sweep, and adoption or shelving claim.
`reversibility:` is parsed as exactly `one-way` or `two-way`.
`loop.sh start <work-name>` scaffolds `intent/frame/frame.md` with the lean fields.
`loop.sh frame` and `loop.sh signoff` block new work whose frame is incomplete, whose
direction is absent or malformed, whose direction appears retrospective, whose new-work
direction or sign-off lacks the `operator-gate: tty` marker, or whose one-way frame lacks a
review artifact.
one-way review artifacts record base-role verdicts, unresolved flags, and disposition;
optional reviewer verdicts cannot clear unresolved base-roster or red-team flags.
new work sign-off records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty` in
the work node's `intent/frame/signoff.md`.
`loop.sh execute <work-name>` derives implementation units from the signed frame, starts a
fresh builder session for each unit, and records lean unit handoff, diff, and tier-one
verdict artifacts under the work frame.
`loop.sh execute <work-name>` routes builders through the builder-model knob, defaulting to
the strong model until the two-step plan/build work lands, separately from the strong
review route; it gives each unit a three-attempt fast-builder budget, escalates an
exhausted unit through the strong-builder model knob, and stops for the operator when the
strong builder fails.
`loop.sh execute <work-name>` runs implementation-acceptance reviewers with literal
approval `never` and literal sandbox `read-only`.
`loop.sh execute <work-name>` writes structured acceptance artifacts with a verdict,
rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
`loop.sh execute <work-name>` caches per-unit build and tier-one evidence under a
signed-frame-derived key, skips unchanged accepted units on rerun, and rebuilds cache misses
while invalidating downstream evidence.
`loop.sh execute <work-name>` treats malformed, evidence-free, or unsupported-source
implementation-acceptance output as `FLAG`, blocks unresolved required flags, and runs the
concurrent one-way tier-two panel before archive.
`loop.sh execute <work-name>` records the addressed work in node-local history after archive.

---
endorsed by qqp-dev

exec
/bin/bash -lc "sed -n '1,240p' intent/collaboration.md" in /home/qqp/projects/hypercore
exec
/bin/bash -lc "nl -ba check.sh | sed -n '180,260p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
   180	    'product token "CODEX_BUILDER_MODEL" is outside a whitelisted materialization pointer' \
   181	    "contract product grammar failure names the embedded forbidden token"
   182	
   183	  pointer="$tmp/pointer.md"
   184	  cat > "$pointer" <<'EOF'
   185	# fixture
   186	
   187	the current root harness adapter is materialized as `adapter/codex.md`.
   188	EOF
   189	  if ( fail=0; contract_statement_product_absence "$pointer" all \
   190	    "whitelisted materialization pointer fixture" >"$tmp/pointer.out" 2>&1 ); then
   191	    ok "contract product grammar accepts a whitelisted materialization pointer"
   192	  else
   193	    bad "contract product grammar accepts a whitelisted materialization pointer"
   194	  fi
   195	
   196	  organizing="$tmp/organizing-document.md"
   197	  cat > "$organizing" <<'EOF'
   198	# organizing document
   199	
   200	- **adapter** -- the binding between a harness and the loop, materialized through `adapter/codex.md`.
   201	
   202	The **governed work** -- durable child nodes and mounted work under this root:
   203	
   204	- **home** -- home currently mounts codex-cockpit.
   205	EOF
   206	  if ( fail=0; contract_statement_product_absence "$organizing" organizing-adapter \
   207	    "out-of-scope governed-work product mention fixture" >"$tmp/organizing.out" 2>&1 ); then
   208	    ok "contract product grammar ignores out-of-scope governed-work child-node names"
   209	  else
   210	    bad "contract product grammar ignores out-of-scope governed-work child-node names"
   211	  fi
   212	
   213	  require_text "$root/intent/collaboration.md" \
   214	    "the phase-one collaborator is the harness role that drives orient and frame" \
   215	    "phase-one routing self-test sees the collaborator role assertion"
   216	  require_text "$root/intent/collaboration.md" \
   217	    "phase-one corpus-throughput work" \
   218	    "phase-one routing self-test sees the throughput-delegation assertion"
   219	  require_text "$root/intent/collaboration.md" \
   220	    "the framer is not its own witness" \
   221	    "phase-one routing self-test sees the independent-review-floor assertion"
   222	  require_text "$root/intent/loop.md" \
   223	    "phase-one labor may be routed by role" \
   224	    "phase-one routing self-test sees the phase-one routing assertion"
   225	  require_text "$root/intent/loop.md" \
   226	    "the collaborator role defaults to the interactive harness that loaded the adapter" \
   227	    "phase-one routing self-test sees the collaborator held default"
   228	  require_text "$root/intent/loop.md" \
   229	    "the fast-builder default is held at the strong model" \
   230	    "phase-one routing self-test sees the builder held default"
   231	  require_text "$root/intent/loop.md" \
   232	    "phase-one review stay on the" \
   233	    "phase-one routing self-test sees the review-floor held default"
   234	  require_text "$root/intent/adapter.md" \
   235	    "the phase-one collaborator role defaults to the interactive harness" \
   236	    "phase-one routing self-test sees the adapter collaborator default"
   237	  require_text "$root/adapter/codex.md" \
   238	    "to the interactive Codex harness that loaded this adapter" \
   239	    "phase-one routing self-test sees the current binding collaborator default"
   240	  require_text "$root/adapter/loop.sh" \
   241	    'CODEX_REVIEW_EFFORT:-xhigh' \
   242	    "phase-one routing self-test sees the review-effort held default"
   243	  require_text "$root/adapter/loop.sh" \
   244	    'CODEX_BUILDER_MODEL:-gpt-5.5' \
   245	    "phase-one routing self-test sees the builder-model held default"
   246	  require_text "$root/adapter/loop.sh" \
   247	    'CODEX_BUILDER_EFFORT:-xhigh' \
   248	    "phase-one routing self-test sees the builder-effort held default"
   249	
   250	  rm -rf "$tmp"
   251	}
   252	
   253	shopt -s nullglob
   254	HOME_GREENFIELD_CHECK_TMP=
   255	HOME_GREENFIELD_CHECK_MOUNT=
   256	LOOP_FRAME_CHECK_WORK=
   257	
   258	cleanup_home_greenfield_self_test() {
   259	  [ -n "${HOME_GREENFIELD_CHECK_MOUNT:-}" ] && rm -f "$HOME_GREENFIELD_CHECK_MOUNT"
   260	  [ -n "${HOME_GREENFIELD_CHECK_TMP:-}" ] && rm -rf "$HOME_GREENFIELD_CHECK_TMP"

 succeeded in 0ms:
# collaboration

operator-machine collaboration is a first-class methodology concern, separate from the loop mechanics that enforce it.
collaboration is the working relation by which operator and machine keep the work scrutable, sound, and fast across memoryless sessions.
effective collaboration is complementarity, not maximal automation: the operator sets purpose, constraints, acceptance, and open direction; the machine searches, synthesizes, drafts, executes, checks, and settles only what the intent and operator leave open.
collaboration keeps common ground recoverable without treating field count as proof of collaboration quality.
phase one is an arc: understanding before route, scrutiny sized by reversibility, operator direction, lean recoverability, and sign-off.
the phase-one collaborator is the harness role that drives orient and frame: it carries
operator-facing judgment, surfaces understanding and options, and frames the signed route.
phase-one corpus-throughput work -- research, the orient corpus read, and the sweep map --
may be delegated by the collaborator when written ground preserves accountability and
operator direction.
before a route is written, the machine gives a teach-back, at least one alternative framing, information-gain questions, and a reversibility classification.
one-way work requires distinct-route scrutiny before route settlement, including a mechanically spawned base review roster.
the base review roster is `contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`; optional reviewers are additive and advisory only.
optional reviewers cannot override, outvote, average away, or dilute unresolved base-roster or red-team flags.
for one-way work, the strong review floor that scrutinizes a frame is independent of the
collaborator that framed it; the framer is not its own witness.
review quality is not proved by artifact scanning; review artifacts record structured signal, unresolved flags, and disposition.
direction and sign-off are the two anchored operator acts in phase one, and the machine performs neither for itself.
operator direction is substantive: it records a selected route, constraint, or explicit delegation with `direction-by:`.
sign-off attests informed expectation and understanding, but it still requires the complete lean frame and required phase-one acts; it is not earned by bloated field scanning.
a legitimate helper-written operator act crosses an operator gate that reads its decisive token from `/dev/tty` and records `operator-gate: tty`, staying simple enough that the operator confirms rather than transcribes.
direction is a real operator choice: when the frame offers neutral, materially distinct numbered options, the helper copies the operator's selected option verbatim into `direction.md`; the machine may draft options but never chooses one for the operator.
sign-off is informed at the moment of attestation: the helper renders the signed frame's route, acceptance condition, observable acceptance, excluded interpretation, reversibility, and target segments before it reads the confirming token.
`operator-gate: tty` is a terminal-liveness marker for the helper path that the default machine command path lacks; it is not cryptographic non-repudiation, tamper-evidence, file integrity, or proof an operator rather than a deliberately allocated terminal answered.
collaboration calibrates reliance: the machine makes its capabilities, limits, uncertainty, evidence, and failure modes visible enough for the operator to judge when to rely on it, challenge it, redirect it, or stop it.
collaboration preserves operator agency without wasting motion: the machine asks before settling open direction or choices the artifacts cannot ground, and proceeds without interruption when the signed frame, intent, and checks give it enough written ground.
phase-two acceptance is an operator-reliance concern, not only loop mechanics: before one-way adoption stamps the operator's endorsement, the machine makes the built result independently checkable against what the operator signed.
implementation-acceptance scrutiny is independent of the builder's attestation; the builder does not become the witness that proves its own one-way archive.
unresolved implementation-acceptance `FLAG`s are feedback material: they block archive and surface to the operator rather than being self-cleared, averaged away, outvoted, or treated as warnings.
implementation-acceptance signal is legible: a required acceptance verdict carries a parseable `PASS` or `FLAG` plus rationale and concrete evidence enough for the operator or a later machine to act on a `FLAG`; uncertainty still flags, and legibility makes the door actionable without weakening it.
build retry is bounded proof-floor recovery, not a structural re-decision: a builder may re-attempt a failed unit within the signed route, but structural mismatches, tier-two `FLAG`s, and an exhausted escalation budget still surface to the operator rather than being retried away.
collaboration treats feedback as material: operator corrections, machine-discovered facts, failed checks, and sweep flags become intent, proof, machine statements, or debt rather than remaining transient chat.
collaboration degrades gracefully: when written ground is insufficient, the machine records the blocker and decision surface and stops rather than fabricating content.

## machine
phase-two handoff state is written as common ground for the operator and later tooling:
the addressed work's current or recent gate, current unit, status, harness session id, latest
message, failure reason, event history, run artifact paths, and phase-two acceptance
artifact paths are recoverable from loop state files.

---
endorsed by qqp-dev

exec
/bin/bash -lc "sed -n '1,260p' intent/adapter.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
# adapter

the adapter is the binding between a harness and the methodology: it promises the harness
acts in agreement with the intent and the loop.
a harness begins each session memoryless, reaching the work only through what it loads;
absent the adapter, agreement is left to chance.
the adapter points the harness at the intent and the loop -- the single source of truth --
and drives it through them; pointing alone is a request, agreement is enforced.
the adapter's specifics are a rigid workflow over the loop's gates: each gate's
preconditions must hold before the next is allowed, and a gate whose preconditions fail
blocks rather than warns.
the rigid workflow restates no rule: the gates and their order are the loop, already
intent; the workflow operationalizes them, and where workflow and intent disagree, the
intent wins.
the rigid workflow is interactive through orient and frame as the design phase, and through
sign-off as the human gate: before a route is written, the machine surfaces understanding,
alternative framing, information-gain questions, reversibility, review where required, and
a decision surface for substantive operator direction; after sign-off, implement, check,
and archive run through cleared sessions that re-derive each unit and acceptance review
from the signed frame directory and lean phase-two handoff artifacts alone.
direction and review are phase-one acts or artifacts, not loop gates.
the review roster for one-way phase-one work has a base roster of
`contract-checkability`, `soundness-fit`, `simplicity-fastness`, and `red-team`.
the implementation-acceptance reviewer for each phase-two unit is independent and read-only.
the tier-two implementation-acceptance panel for one-way work has required lenses
`whole-acceptance-conformance`, `proof-integrity`, `independent-coherence`,
`security-permissions`, and `red-team`.
the complete optional review roster is `implementation-maintainability`,
`security-permissions`, `operator-ergonomics`, `migration-compatibility`,
`domain-evidence`, and `performance-cost`.
optional reviewers are advisory additions and cannot override, outvote, average away, or
dilute unresolved base-roster or red-team flags.
the adapter classifies the request surface before changing material: ordinary
conversation and read-only inspection may proceed directly, while governed work starts or
continues a work node.
the adapter rejects perceived simplicity, file count, convenience, and low risk as waivers
for governed work.
on request the adapter renders a statement of the intent intelligible in plain language
without altering it.
the adapter carries only what the intent cannot yet reach the harness with -- the order to
read the intent first, and disciplines not yet written as statements; each is a debt,
folded into the intent by later work and then dropped.
an adapter is per harness; one node may be bound by more than one, each loaded by its own
harness.
an adapter binds a harness to a phase; phase one and phase two may bind different harnesses,
and the current materialization binds one harness to both phases.
the phase-one collaborator role defaults to the interactive harness that loaded the
adapter; no orchestrator routing knob is required until a materialization routes that role.
the adapter material is materialized only at the methodology root, with the prose it routes
to, and not in any nested node; a mounted external project may carry a target-local entry
point that links to root-managed adapter material and routes direct-path work back to the
root adapter and loop.
the adapter is not in the orient path; loading it is how orient begins, not part of the
intent it routes to.
the sweep reads the adapter against the intent, so a rule it has come to restate, or a debt
the intent has since absorbed, is caught as drift.

## machine
the current root harness adapter is materialized as `adapter/codex.md`.
the current materialization binds the same harness to phase one and phase two; the
phase-one collaborator is the interactive harness that loaded the adapter.
the harness loads its adapter through a root `AGENTS.md` symlinked to `adapter/codex.md`;
the root entry is the harness's mandated pointer, holding nothing, not where the adapter
lives.
a machine working in a nested node under the root is bound by the root `AGENTS.md` in the
project instruction chain from the project root to the current directory, so no node below
the root carries its own adapter material.
a mounted external project may carry a target-local `AGENTS.md` entry point for
direct-path openings; the entry point links to root-managed adapter material and routes
back to the root adapter and loop instead of copying root adapter material into the
mounted node.
the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
over the phase-two executor harness: each implementation unit opens a fresh builder
session from the signed frame, and acceptance reviewers and the archive actor are fresh
sessions rather than resumes of the builder.
the loop records phase-two run state under `HYPERCORE_LOOP_STATE_DIR`, defaulting to
`.hypercore/loop-runs`, with run-local state, event history, raw harness gate streams, gate
final outputs, acceptance artifact paths, and current pointers for the addressed work and
root.
the loop streams inner executor JSON events into the phase-two run state while
printing concise progress, without changing the cleared-session contract.
the loop materializes separate builder and reviewer routing, structured acceptance
artifacts with source markers and fake-source rejection, the per-unit fast-builder retry
then strong-builder escalation ladder, a resumable per-unit execute cache, the concurrent
one-way tier-two panel, and phase-one review subprocess crash diagnostics.
`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
the root node is the default addressed node.
`loop.sh -C <node-path> <gate> <work-name>` addresses work in a child node, including a
linked mounted child when `<node-path>` is its mount path.
`loop.sh start <work-name>` creates a work node directly under the addressed node.
`loop.sh frame`, `signoff`, `execute`, and `status` resolve the addressed node-local work
and act only on that addressed work.
`loop.sh execute <work-name>` records only the addressed node-local work in that node's
history.
the orchestrator creates, signs, executes, and records only addressed node-local work
nodes.
the gate prompts use addressed-node and node-local work wording and point cleared sessions
at the addressed work frame.
the orient gate prompt requires the machine to classify the request surface, name the
addressed node, node-local work name, target segments, work in flight, teach-back,
alternative framing, information-gain questions, reversibility classification, and any
open direction that needs an operator decision before the frame settles a route.
the orient gate prompt tells the machine not to write a route or operator direction.
the frame gate prompt requires addressed node, node-local work name, target segments, work
in flight, problem, constraints, decision surface or open direction, reversibility, route,
acceptance condition, observable acceptance, excluded interpretation, proof state, sweep,
and adoption or shelving claim in `intent/frame/frame.md`.
the frame gate prompt requires substantive `intent/frame/direction.md` before route
framing and requires `intent/frame/review.md` for one-way work.
the frame gate prompt tells the machine not to write operator direction, not to collect
direction retrospectively, and not to let optional reviewer verdicts clear base-roster or
red-team flags.
the adapter prose describes phase one as design-phase collaboration with direction
and review artifacts, while preserving phase two as cleared, heads-down execution from the
signed frame directory and lean phase-two handoff artifacts.
`check.sh` mechanically checks that the gate prompts, adapter prose, loop frame
validation, start scaffolding, direction/review helpers, operator-act gating through
`/dev/tty` with B-ready `operator-gate:` markers and numbered-option direction, review and
acceptance isolation settings, strict frame parsing, phase-two acceptance gating, structured
acceptance legibility, acceptance source markers and fake-source rejection, separate
builder/reviewer routing with bounded retry and strong escalation, resumable execute
caching, the concurrent tier-two panel, the new operator-act and phase-two performance
contract in the `collaboration`, `loop`, and `adapter` segments, and current-material
absence of the retired compatibility route still carry the contract.
each gate's instructions are held in a file in `adapter/gates/`; the harness path includes
them in the executor gate prompt; the orchestrator owns gate order and preconditions and
blocks a gate whose preconditions fail.
sign-off for new work records `signed-off-by:`, `signed-off-at:`, and `operator-gate: tty`
in the work-node frame's `intent/frame/signoff.md`; the orchestrator seals phase two until
sign-off is present, and the machine never writes it for itself.
the root `./direction` and `./signoff` helpers are terminal-gated operator-act helpers for
new work: direction selects a numbered option from `intent/frame/options.md` through
`/dev/tty`, and sign-off renders a frame-derived brief and reads the work number through
`/dev/tty`, each writing `operator-gate: tty`; the explicit argument forms are admin forms
that cannot record gated operator acts for new work.
`operator-gate: tty` records that the legitimate helper path crossed the current harness's
terminal-liveness check, which the default machine command path lacks; it does not prove
network isolation, cryptographic non-repudiation, tamper-evidence, file integrity, or that
an operator rather than a deliberately allocated terminal answered.
at the check gate the orchestrator records tier-one implementation acceptance for each
unit, records the concurrent one-way tier-two panel when required, and halts phase two
before archive when required acceptance flags remain unresolved.

---
endorsed by qqp-dev

codex
The scanner no longer uses word-boundary guards: its regex scans `CODEX_...`, `gpt-...`, `codex`, `claude`, and `opus` anywhere in the text, then only suppresses matches located inside an exact allowed backticked pointer. I’m also checking the current intent files for the excluded-interpretation concerns, not just the regex.
codex
The managed sandbox is read-only even for `/tmp`, so fixture files via `mktemp` cannot be created here. I’m rerunning the same scanner probes through process substitution, which gives the scanner a file-like stream without writing temporary files.
exec
/bin/bash -lc "source <(sed -n '71,130p' check.sh)
run_fail() {
  name="'$1
  text=$2
  if out=$(contract_statement_product_absence_errors <(printf '"'# fixture\\n\\n%s\\n' \""'$text") all 2>&1); then
    printf '"'FAIL-TEST %s: UNEXPECTED PASS\\n' \""'$name"
  else
    printf '"'FAIL-TEST %s: caught: %s\\n' \""'$name" "$out"
  fi
}
run_pass() {
  name=$1
  text=$2
  scope=${3:-all}
  if out=$(contract_statement_product_absence_errors <(printf '"'# fixture\\n\\n%s\\n' \""'$text") "$scope" 2>&1); then
    printf '"'PASS-TEST %s: passed\\n' \""'$name"
  else
    printf '"'PASS-TEST %s: UNEXPECTED FAIL: %s\\n' \""'$name" "$out"
  fi
}
run_fail hypercore_codex '"'HYPERCORE_CODEX_BUILDER_MODEL appears as an embedded identifier.'
run_fail codex_harness 'CodexHarness appears as an embedded identifier.'
run_fail review_gpt 'Review_GPT-5 appears as an embedded identifier.'
run_pass legitimate_text 'the phase-one collaborator uses role language without product names.'
run_pass pointer_codex 'pointer: "'`adapter/codex.md`.'"'
run_pass pointer_agents 'pointer: "'`AGENTS.md`.'"'
run_pass pointer_mounted 'pointer: "'`adapter/codex-mounted.md`.'"'
run_pass pointer_loop 'pointer: "'`adapter/loop.sh`.'"'
if out="'$(contract_statement_product_absence_errors <(printf '"'# organizing document\\n\\n- **adapter** -- materialized through "'`adapter/codex.md`.'"\\n\\nThe **governed work** -- durable child nodes and mounted work under this root:\\n\\n- **home** -- home currently mounts codex-cockpit.\\n') organizing-adapter 2>&1); then
  printf 'PASS-TEST codex-cockpit-out-of-scope: passed\\n'
else
  printf 'PASS-TEST codex-cockpit-out-of-scope: UNEXPECTED FAIL: %s\\n' \""'$out"
fi' in /home/qqp/projects/hypercore
 succeeded in 0ms:
FAIL-TEST hypercore_codex: caught: /dev/fd/62:3: product token "CODEX_BUILDER_MODEL" is outside a whitelisted materialization pointer
FAIL-TEST codex_harness: caught: /dev/fd/63:3: product token "Codex" is outside a whitelisted materialization pointer
FAIL-TEST review_gpt: caught: /dev/fd/63:3: product token "GPT-5" is outside a whitelisted materialization pointer
PASS-TEST legitimate_text: passed
PASS-TEST pointer_codex: passed
PASS-TEST pointer_agents: passed
PASS-TEST pointer_mounted: passed
PASS-TEST pointer_loop: passed
PASS-TEST codex-cockpit-out-of-scope: passed

codex
The targeted scanner probes match the frame: all three prior reproducers fail, the four whitelisted pointer forms pass, ordinary role-language text passes, and `codex-cockpit` is ignored when outside the adapter bullet scope. I’m running the full mechanical check next; the sandbox already showed it may block temp-file self-tests, so I’ll separate environmental failure from material findings if that happens.
exec
/bin/bash -lc ./check.sh in /home/qqp/projects/hypercore
codex
`./check.sh` is running longer than the first output window and has already passed the product-absence checks, built-in product grammar self-tests, role/default assertions, and a large set of loop-frame and acceptance-gate checks. I’m waiting for the process to finish before issuing the verdict.
 succeeded in 41989ms:
  ok    contract product grammar rejects an unwhitelisted harness-product token
  ok    contract product grammar failure names the forbidden token
  ok    contract product grammar rejects an embedded harness-product token
  ok    contract product grammar failure names the embedded forbidden token
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
  ok    home/check-hypercore-home-check.E0Fa2h target is a git repository
  ok    home/check-hypercore-home-check.E0Fa2h AGENTS.md points at the root-managed mounted Codex entrypoint
  ok    home/check-hypercore-home-check.E0Fa2h AGENTS.md is not a generated regular file
  ok    home/check-hypercore-home-check.E0Fa2h signoff points at the root-managed home signoff helper
  ok    home/check-hypercore-home-check.E0Fa2h signoff entrypoint is executable
  ok    home/check-hypercore-home-check.E0Fa2h signoff is not a generated regular file
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
home/check-hypercore-home-check.E0Fa2h - structure
  ok    documentation tree is retired
  ok    implementation tree is retired
  ok    intent tree exists
  ok    organizing document exists
home/check-hypercore-home-check.E0Fa2h - segments
home/check-hypercore-home-check.E0Fa2h - history
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

codex
The full `./check.sh` completed with exit code 0 and ended with “all structural statements hold - root and every current child node.” I’m doing one last targeted sweep against the signed frame’s excluded interpretations before I return the structured verdict.
exec
/bin/bash -lc 'git --no-pager diff --name-only' in /home/qqp/projects/hypercore
 succeeded in 0ms:
adapter/codex.md
adapter/loop.sh
check.sh
hypercore.md
intent/adapter.md
intent/collaboration.md
intent/loop.md
intent/machine-statements/adapter.md
intent/machine-statements/collaboration.md
intent/machine-statements/loop.md
intent/organizing-document.md

exec
/bin/bash -lc 'git --no-pager diff --stat' in /home/qqp/projects/hypercore
 succeeded in 0ms:
 adapter/codex.md                           |  23 +++
 adapter/loop.sh                            |   2 +-
 check.sh                                   | 232 +++++++++++++++++++++++++++++
 hypercore.md                               |   4 +-
 intent/adapter.md                          |  55 +++----
 intent/collaboration.md                    |   9 +-
 intent/loop.md                             |  28 ++--
 intent/machine-statements/adapter.md       |  36 ++---
 intent/machine-statements/collaboration.md |   2 +-
 intent/machine-statements/loop.md          |  24 +--
 intent/organizing-document.md              |   4 +-
 11 files changed, 348 insertions(+), 71 deletions(-)

exec
/bin/bash -lc "sed -n '130,240p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
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
/bin/bash -lc "rg -n \"second executor|phase-two executor|executor harness|collaborator.*phase-two|new gate|proof floor|review floor|strong review|materialization|adapter/loop\\.sh|gates:|goes through five gates|CODEX_|gpt-5\\.5|source: real-reviewer|source: fake|fake acceptance|HYPERCORE_ACCEPTANCE_FAKE_DIR\" intent/collaboration.md intent/loop.md intent/adapter.md intent/machine-statements/collaboration.md intent/machine-statements/loop.md intent/machine-statements/adapter.md adapter/codex.md adapter/loop.sh hypercore.md intent/organizing-document.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
intent/collaboration.md:17:for one-way work, the strong review floor that scrutinizes a frame is independent of the
intent/loop.md:3:every work node that needs adoption or shelving goes through five gates: orient, frame,
intent/loop.md:61:fake/self-test; real execute refuses fake acceptance, and real archive refuses dry-run or
intent/loop.md:65:the phase-two executor harness while phase-one review stays on the strong review floor.
intent/loop.md:69:strong review floor; the fast-builder default is held at the strong model until the
intent/loop.md:97:concurrent work is sequenced by the loop's gates: first to adopt wins, and later work builds
intent/loop.md:113:before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
intent/loop.md:181:rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
intent/loop.md:182:dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
adapter/codex.md:25:The current materialization binds Codex to both phase one and phase two. Phase one defaults
adapter/codex.md:27:`adapter/loop.sh`, which invokes fresh `codex exec` sessions for builders, reviewers, and
adapter/codex.md:31:The current materialization also keeps the `CODEX_*` environment knob names in
adapter/codex.md:32:`adapter/loop.sh`. Those names are implementation binding, while the intent states the
adapter/codex.md:53:## The rigid workflow — `adapter/loop.sh`
adapter/codex.md:133:- **Pin the strong review floor.** The strong review floor is not yet mechanically pinned
hypercore.md:204:Every work node that needs adoption or shelving goes through five gates.
intent/machine-statements/loop.md:14:before launching the first phase-two executor gate, `loop.sh execute <work-name>` checks
intent/machine-statements/loop.md:82:rationale, evidence, and a `source:` marker, refuses `HYPERCORE_ACCEPTANCE_FAKE_DIR` outside
intent/machine-statements/loop.md:83:dry-run, and lets real archive accept only `source: real-reviewer` required acceptance.
intent/machine-statements/adapter.md:4:the current materialization binds the same harness to phase one and phase two; the
intent/machine-statements/adapter.md:16:the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
intent/machine-statements/adapter.md:17:over the phase-two executor harness: each implementation unit opens a fresh builder
intent/machine-statements/adapter.md:30:`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.
adapter/loop.sh:37:#   CODEX_BIN (default: codex), CODEX_APPROVAL (default: never)
adapter/loop.sh:38:#   CODEX_WRITE_SANDBOX (default: workspace-write), CODEX_READ_SANDBOX (default: read-only)
adapter/loop.sh:39:#   CODEX_BUILDER_MODEL (default: gpt-5.5 until the two-step plan/build lands), CODEX_BUILDER_EFFORT (default: xhigh)
adapter/loop.sh:40:#   CODEX_STRONG_BUILDER_MODEL (optional strong-builder escalation model)
adapter/loop.sh:41:#   CODEX_STRONG_BUILDER_EFFORT (default: CODEX_REVIEW_EFFORT or xhigh)
adapter/loop.sh:42:#   CODEX_REVIEW_MODEL (optional strong review/acceptance model), CODEX_REVIEW_EFFORT (default: xhigh)
adapter/loop.sh:56:CODEX_BIN="${CODEX_BIN:-codex}"
adapter/loop.sh:57:CODEX_APPROVAL="${CODEX_APPROVAL:-never}"
adapter/loop.sh:58:CODEX_WRITE_SANDBOX="${CODEX_WRITE_SANDBOX:-workspace-write}"
adapter/loop.sh:59:CODEX_READ_SANDBOX="${CODEX_READ_SANDBOX:-read-only}"
adapter/loop.sh:184:  printf './adapter/loop.sh'
adapter/loop.sh:330:  command -v "$CODEX_BIN" >/dev/null 2>&1 \
adapter/loop.sh:331:    || phase_two_preflight_fail "Codex binary '$CODEX_BIN' is not on PATH" "$work_name" \
adapter/loop.sh:334:  if [ -n "${CODEX_HOME:-}" ]; then
adapter/loop.sh:335:    codex_home=$CODEX_HOME
adapter/loop.sh:338:      || phase_two_preflight_fail "HOME is unset and CODEX_HOME is not set, so Codex home cannot be resolved" "$work_name" \
adapter/loop.sh:2125:      printf 'fake acceptance loaded from HYPERCORE_ACCEPTANCE_FAKE_DIR in dry-run; rejected by real archive'
adapter/loop.sh:2152:  if [ -n "${HYPERCORE_ACCEPTANCE_FAKE_DIR:-}" ]; then
adapter/loop.sh:2154:      || die "real execute refuses HYPERCORE_ACCEPTANCE_FAKE_DIR; fake acceptance is dry-run/self-test only"
adapter/loop.sh:2155:    fake_file="$HYPERCORE_ACCEPTANCE_FAKE_DIR/$reviewer_key"
adapter/loop.sh:2159:          fake_file="$HYPERCORE_ACCEPTANCE_FAKE_DIR/$(printf '%s' "$reviewer_key" | sed -E 's/-(fast|strong)-[0-9]+$//')"
adapter/loop.sh:2167:      output="missing fake acceptance reviewer output for $reviewer_key"
adapter/loop.sh:2183:  command -v "$CODEX_BIN" >/dev/null 2>&1 \
adapter/loop.sh:2184:    || die "acceptance review cannot spawn Codex reviewers: Codex binary '$CODEX_BIN' is not on PATH"
adapter/loop.sh:2195:  CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")
adapter/loop.sh:2197:  ACCEPTANCE_CMD=("${CODEX_CMD[@]}")
adapter/loop.sh:2551:    *Edit*|*Write*) printf '%s' "$CODEX_WRITE_SANDBOX" ;;
adapter/loop.sh:2552:    *)              printf '%s' "$CODEX_READ_SANDBOX" ;;
adapter/loop.sh:2644:  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
adapter/loop.sh:2645:  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
adapter/loop.sh:2653:      model="${CODEX_BUILDER_MODEL:-gpt-5.5}"
adapter/loop.sh:2654:      effort="${CODEX_BUILDER_EFFORT:-xhigh}"
adapter/loop.sh:2655:      codex_add_model_and_effort_args "$model" "$effort" CODEX_BUILDER_MODEL CODEX_BUILDER_EFFORT
adapter/loop.sh:2658:      model="${CODEX_STRONG_BUILDER_MODEL:-${CODEX_REVIEW_MODEL:-${CODEX_MODEL:-}}}"
adapter/loop.sh:2659:      effort="${CODEX_STRONG_BUILDER_EFFORT:-${CODEX_REVIEW_EFFORT:-xhigh}}"
adapter/loop.sh:2660:      codex_add_model_and_effort_args "$model" "$effort" CODEX_STRONG_BUILDER_MODEL CODEX_STRONG_BUILDER_EFFORT
adapter/loop.sh:2663:      model="${CODEX_MODEL:-}"
adapter/loop.sh:2664:      effort="${CODEX_EFFORT:-}"
adapter/loop.sh:2665:      codex_add_model_and_effort_args "$model" "$effort" CODEX_MODEL CODEX_EFFORT
adapter/loop.sh:2675:  CODEX_CMD=("$CODEX_BIN" -a "$CODEX_APPROVAL" -s "$sandbox" -C "$ROOT")
adapter/loop.sh:2677:  [ -n "${CODEX_PROFILE:-}" ] && CODEX_CMD+=(-p "$CODEX_PROFILE")
adapter/loop.sh:2693:    start)  CODEX_CMD+=(exec --json -o "$final" -) ;;
adapter/loop.sh:2721:    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
adapter/loop.sh:2742:    printf '%q ' "${CODEX_CMD[@]}"; printf '<<< stdin: %q\n' "$combined"
adapter/loop.sh:2757:  printf '%s' "$combined" | "${CODEX_CMD[@]}" | while IFS= read -r line || [ -n "$line" ]; do
adapter/loop.sh:2795:# a single fresh phase-two executor session.
adapter/loop.sh:3001:  local model=${CODEX_REVIEW_MODEL:-}
adapter/loop.sh:3002:  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
adapter/loop.sh:3003:  validate_codex_model_var CODEX_REVIEW_MODEL "$model"
adapter/loop.sh:3004:  validate_codex_effort_var CODEX_REVIEW_EFFORT "$effort"
adapter/loop.sh:3008:  local model=${CODEX_REVIEW_MODEL:-}
adapter/loop.sh:3009:  local effort=${CODEX_REVIEW_EFFORT:-xhigh}
adapter/loop.sh:3011:  [ -n "$model" ] && CODEX_CMD+=(-m "$model")
adapter/loop.sh:3012:  [ -n "$effort" ] && CODEX_CMD+=(-c "model_reasoning_effort=\"$effort\"")
adapter/loop.sh:3092:  command -v "$CODEX_BIN" >/dev/null 2>&1 \
adapter/loop.sh:3093:    || die "review cannot spawn Codex reviewers: Codex binary '$CODEX_BIN' is not on PATH"
adapter/loop.sh:3108:  CODEX_CMD=("$CODEX_BIN" -a never -s read-only -C "$ROOT")
adapter/loop.sh:3110:  REVIEW_CMD=("${CODEX_CMD[@]}")
adapter/loop.sh:3453:  if [ "$DRY_RUN" != 1 ] && [ -n "${HYPERCORE_ACCEPTANCE_FAKE_DIR:-}" ]; then
adapter/loop.sh:3454:    die "real execute refuses HYPERCORE_ACCEPTANCE_FAKE_DIR; fake acceptance is dry-run/self-test only"
intent/adapter.md:9:the adapter's specifics are a rigid workflow over the loop's gates: each gate's
intent/adapter.md:46:and the current materialization binds one harness to both phases.
intent/adapter.md:48:adapter; no orchestrator routing knob is required until a materialization routes that role.
intent/adapter.md:60:the current materialization binds the same harness to phase one and phase two; the
intent/adapter.md:72:the rigid workflow is materialized as `adapter/loop.sh`, realizing the two-phase shape
intent/adapter.md:73:over the phase-two executor harness: each implementation unit opens a fresh builder
intent/adapter.md:86:`adapter/loop.sh` accepts one node-local work name in the addressed node for new work.

exec
/bin/bash -lc "sed -n '240,360p' 011-phase-one-routing/intent/frame/frame.md" in /home/qqp/projects/hypercore
 succeeded in 0ms:
- Not a rename or removal of materialization. `adapter/loop.sh` still calls the executor;
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

codex
The changed-file set is scoped to the signed frame’s target/material files, and the diff stat shows `adapter/loop.sh` changed by one comment line plus the `check.sh` scanner/test addition. I’m checking that no product-token sweep gaps remain in the enumerated statement scopes.
exec
/bin/bash -lc "git --no-pager diff -- intent/adapter.md intent/machine-statements/adapter.md | sed -n '1,240p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
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

exec
/bin/bash -lc "git --no-pager diff -- intent/loop.md intent/machine-statements/loop.md | sed -n '1,220p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
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

exec
/bin/bash -lc 'git --no-pager diff -- adapter/loop.sh' in /home/qqp/projects/hypercore
 succeeded in 0ms:
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

exec
/bin/bash -lc "git --no-pager diff -- intent/collaboration.md intent/machine-statements/collaboration.md adapter/codex.md hypercore.md intent/organizing-document.md | sed -n '1,260p'" in /home/qqp/projects/hypercore
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
 

codex
One detail from the full check: its greenfield self-test created a transient mounted child during the run, then the script continued through mounted-node checks and exited cleanly. I’m checking the worktree state now so the evidence doesn’t hide leftover test material.
exec
/bin/bash -lc 'git status --short' in /home/qqp/projects/hypercore
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
/bin/bash -lc "ls -la home | sed -n '1,120p'" in /home/qqp/projects/hypercore
 succeeded in 0ms:
total 16
drwxrwxr-x  3 qqp qqp 4096 Jun  7 20:10 .
drwxrwxr-x 12 qqp qqp 4096 Jun  7 20:10 ..
-rw-rw-r--  1 qqp qqp 1035 Jun  6 20:35 README.md
lrwxrwxrwx  1 qqp qqp   32 Jun  6 22:07 codex-cockpit -> /home/qqp/projects/codex-cockpit
drwxrwxr-x  3 qqp qqp 4096 Jun  6 20:21 intent

exec
/bin/bash -lc "find home -maxdepth 1 -type l -name 'check-hypercore-home-check.*' -print" in /home/qqp/projects/hypercore
 succeeded in 0ms:
codex
VERDICT: PASS
RATIONALE: The signed frame’s pointer grammar is now enforced without the prior embedded-token loophole, legitimate whitelisted materialization pointers still pass, and the implementation preserves the signed excluded boundaries.
EVIDENCE: `check.sh:71-129` scans product tokens anywhere and exempts only exact allowed backticked pointers; targeted probes caught `HYPERCORE_CODEX_BUILDER_MODEL`, `CodexHarness`, and `Review_GPT-5`, while role-language text, `adapter/codex.md`, `AGENTS.md`, `adapter/codex-mounted.md`, `adapter/loop.sh`, and out-of-scope `codex-cockpit` passed; `./check.sh` exited 0 with “all structural statements hold”; `git --no-pager diff -- adapter/loop.sh` shows only a comment de-name, so no second executor/materialization removal/new gate/proof-floor demotion/collaborator phase-two artifact path found.
hook: Stop
hook: Stop Completed
tokens used
94,662
VERDICT: PASS
RATIONALE: The signed frame’s pointer grammar is now enforced without the prior embedded-token loophole, legitimate whitelisted materialization pointers still pass, and the implementation preserves the signed excluded boundaries.
EVIDENCE: `check.sh:71-129` scans product tokens anywhere and exempts only exact allowed backticked pointers; targeted probes caught `HYPERCORE_CODEX_BUILDER_MODEL`, `CodexHarness`, and `Review_GPT-5`, while role-language text, `adapter/codex.md`, `AGENTS.md`, `adapter/codex-mounted.md`, `adapter/loop.sh`, and out-of-scope `codex-cockpit` passed; `./check.sh` exited 0 with “all structural statements hold”; `git --no-pager diff -- adapter/loop.sh` shows only a comment de-name, so no second executor/materialization removal/new gate/proof-floor demotion/collaborator phase-two artifact path found.
