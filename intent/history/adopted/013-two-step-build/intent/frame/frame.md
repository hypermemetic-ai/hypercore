# frame - 013-two-step-build

## work

Addressed node: root (hypercore)

Node-local work name: 013-two-step-build

Target segments: loop, adapter

Work in flight: Nothing else is in flight. The tree is clean after the two commits you made
today — the cache removal (91f12aa) and the draft Claude adapter (60fb127). Two related
scratch notes exist but are not adopted and not binding: DECOMPOSITION-FINDINGS.md and
WORK-NODE-COLLAPSE-FINDINGS.md. This work comes from TWO-STEP-BUILD-FINDINGS.md, which is
also a scratch note, not intent.

## problem

Today you sign one frame that has to do three jobs at once: it is what you read and approve,
what the builder implements from, and what the review panel judges the result against.
Serving all three, each work "unit" ends up being a whole dense feature. Example: in work
010, unit-003 packed model routing, the retry budget, escalation, an operator-stop, and
self-tests into a single paragraph, and the build trace shows the model figuring out
architecture, not just applying edits. Because units are that heavy, we do not trust a cheap
fast model to build them — so every build still runs on the expensive model (gpt-5.5), and
the cheap-model setting that 010 added has never actually built anything.

## constraints

- We are committed to the two-step shape: signed frame -> strong model writes a plan ->
  cheap model builds from the plan. Decided, not up for debate.
- The signed frame should be short and readable: clear, separate claims you can own and the
  panel can judge — not a pile of implementation detail.
- "Readable" has a floor: the panel must still be able to look at a result and call it wrong
  against a frame claim WITHOUT reading the code. Readable, never vague.
- The cheap model only ever does mechanical tasks. If a unit cannot be broken into
  mechanical tasks, the strong model builds it directly.
- The plan is a new place a bug can hide: a plan that looks right but does not match what you
  signed would ship a defect, so a check must confirm the plan matches the signed frame.
- The plan sits at the head of each unit's build (your earlier choice), not as one big plan
  for the whole phase.
- check.sh stays the proof floor and stays green. We extend 010's routing/retry/escalation
  and 008's acceptance checks; we do not replace them.
- When this ships, the default builder flips from the expensive model back to the cheap fast
  one (gpt-5.3-codex-spark), because it is now only doing mechanical tasks behind a real review.

## decision surface or open direction

One thing is genuinely yours to choose, and it is in options.md: do you want to be able to
read the strong model's plan before the cheap model builds from it? Option 1 keeps the plan
under the hood — you only sign the short frame and judge the result. Option 2 saves the plan
where you can read it if you want. Everything else — how we detect "cannot be broken down,"
and whether the plan-matches-frame check reuses the existing review or is its own — I settle
as the machine and record. Pick a route with ./direction.

Reversibility: one-way

## route

Option 2 — audited two-step (plan you can read), per your direction. Add a per-unit step to
phase two: before the cheap model builds a unit, the strong model writes a plan for that unit
and saves it under the work frame where you can read it (read-only, unsigned). The cheap fast
model (gpt-5.3-codex-spark, the new default builder) builds only from that plan and only does
mechanical tasks. Any unit the strong model cannot break into mechanical tasks it marks with
an explicit "non-decomposable" signal that a check confirms, and that unit is built by the
strong model directly. A dedicated plan-matches-frame check runs on each plan before its
build is trusted, separate from the existing tier-one review. The signed frame stays short
and judgeable — the panel can call a result wrong against a frame claim without reading code.
check.sh gains assertions for the plan step, the plan-model knob, the spark default, the
readable per-unit plan artifact, and the per-unit plan-match result. 010's routing/retry/
escalation and 008's acceptance tiers are extended, not replaced. On adoption, fold these
statements into the loop and adapter segments and flip the builder default to spark.

## acceptance condition

The loop gains a per-unit step where the strong model writes a plan before the cheap model
builds; the signed frame stays short but stays judgeable; a check confirms each plan matches
the signed frame before its build counts; units that cannot be broken down go to the strong
model; the default builder flips to the cheap fast model; check.sh proves all of it; and the
one-way review panel passes before we adopt.

## observable acceptance

- check.sh exits 0 and now also checks that: the loop and adapter intent describe the plan
  step and the plan-matches-frame check; loop.sh runs a strong-model plan step before the
  cheap build and exposes a knob for it; the default builder is gpt-5.3-codex-spark; and each
  unit needs a plan-match result on disk before its build is trusted.
- A dry-run of loop.sh execute shows, for each unit and in order: a plan written by the
  strong model, then a plan-match result, then the build, then the tier-one review.

## excluded interpretation

This work does NOT mean:

- making the frame vague — short is fine, unjudgeable is not; the panel must still catch a
  wrong result without reading code.
- letting the cheap model build whole features — it only does mechanical tasks; anything else
  goes to the strong model.
- the plan becoming something you sign — the plan is build scaffolding, not intent.
- throwing away 010's routing/retries or 008's reviews — we build on them.
- treating "the strong model wrote a plan" as proof the plan is right — the plan-match check
  is required, not optional.

## proof state

Not proven until built: that check.sh enforces the plan step, the plan-match check, and the
builder flip, and that a dry-run shows the right order. 010 and 008 proofs must stay green.

## sweep

Where these ideas already live, and what must stay consistent:

- "builder held at the expensive model until two-step lands" appears in intent/loop.md,
  intent/machine-statements/loop.md, intent/adapter.md, intent/machine-statements/adapter.md,
  adapter/loop.sh (header + the CODEX_BUILDER_MODEL default + the note), adapter/codex.md,
  adapter/claude.md, and check.sh. Every "held until two-step lands" line must flip to
  "shipped; default is the cheap model." This is the main consistency job.
- Resume-on-disk was just rewritten (commit 91f12aa) to skip a unit that already has a clean
  tier-one PASS. The new plan and plan-match files add to what a resume must account for;
  keep that statement consistent.
- The plan-match check sits next to the existing tier-one review (008).
- 010's "retry three times then escalate to the strong model" and this work's "send
  un-breakdownable units straight to the strong model" must fit together, not fight.
- The collaboration segment's "keep the frame lean" language must stay consistent with the
  short-but-judgeable frame.
- Known issue we are NOT fixing here: the one-way review prompt assumes an already-signed
  frame, so it flags any pre-signoff frame (it flagged this one). Known gap, recorded by 011.

## implementation units

Implementation units for phase two:

1. Strong-model plan step plus a readable per-unit plan artifact. Add a planner model knob to
   adapter/loop.sh (defaulting to the strong model) and make execute run a strong-model plan
   sub-step at the head of each unit that writes a human-readable plan under the unit's
   phase-two tree before the build runs. Add the loop and adapter intent statements for the
   per-unit plan step and the readable plan artifact. Proof: check.sh asserts the planner knob
   exists and defaults to the strong model, the new statements are present, and a dry-run
   execute records a plan artifact before that unit's build artifact.
2. Plan-matches-frame check gating each plan. Add a dedicated independent strong read-only
   plan-faithfulness reviewer that checks each plan against the signed frame and returns a
   structured PASS or FLAG; execute requires a clean plan-match result before that unit's
   build is trusted, and an unresolved plan-match FLAG blocks the unit. Add the loop and
   adapter statements. Proof: check.sh asserts the plan-match check is required per unit and
   that a missing or failed plan-match blocks the build.
3. Non-decomposable units route to the strong builder. Let the planner emit an explicit
   non-decomposable signal that a check confirms; execute routes such a unit's build to the
   strong builder directly, as the proactive complement to 010's reactive three-fail
   escalation, without forcing a mechanical carve. Add the loop and adapter statements and
   keep them composed with the existing retry/escalate ladder. Proof: check.sh asserts the
   non-decomposable signal routes to the strong builder and does not break the existing ladder.
4. Short-but-judgeable frame altitude rule. Add the loop intent statement that the signed
   frame is held to the floor of judgeability — legible and falsifiable, not
   implementation-complete; the plan carries implementation-completeness; the panel must be
   able to FLAG a wrong result against a frame claim without reading code. Keep the
   collaboration segment's lean-frame language coherent with it. Proof: check.sh asserts the
   altitude statement is present and coherent across loop, adapter, and collaboration.
5. Flip the default builder to spark and flip "held until two-step lands" to "shipped." Change
   the CODEX_BUILDER_MODEL default in adapter/loop.sh from gpt-5.5 to gpt-5.3-codex-spark,
   update the header comment and the two-step note, and update intent/loop.md,
   intent/machine-statements/loop.md, intent/adapter.md, intent/machine-statements/adapter.md,
   adapter/codex.md, and adapter/claude.md so every "builder held at the strong model until
   two-step lands" clause becomes "two-step has shipped; the default builder is the cheap fast
   model behind the plan step and plan-match check." Proof: check.sh asserts the builder
   default token is gpt-5.3-codex-spark and that no "held until two-step lands" clause remains.

## adoption claim

Adopt: write the plan-step, the short-but-judgeable-frame rule, the plan-matches-frame check,
and the send-hard-units-to-the-strong-model rule into the loop and adapter segments; flip the
default builder to gpt-5.3-codex-spark; build the mechanism in loop.sh and the gate prompts;
prove it in check.sh; pass the one-way panel; and stamp your endorsement on the loop and
adapter segments.

## shelving claim

Shelve: if you reject both options or the build cannot be proven, record 013 as shelved
history without flipping the builder or adding the plan step; the builder stays on the
expensive model and the findings stay as scratch for a later try.
