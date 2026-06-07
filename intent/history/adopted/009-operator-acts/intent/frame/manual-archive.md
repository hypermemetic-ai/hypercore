# manual archive - 009-operator-acts

The operator requested a one-time manual archive outside the loop, for the same structural
reason as 008: the loop's own one-way acceptance door is what this thread set out to
exercise, and the loop could not pass 009 through itself.

## why ordinary archive was impossible

- The tier-two one-way panel emitted five bare `FLAG` verdicts with no rationale — the
  blind-`FLAG` pathology recorded in `PERFORMANCE-FINDINGS.md`. With no memoization, every
  re-run rebuilt and re-reviewed all units; `009-operator-acts` ran ~10 times over ~3h on
  2026-06-07 without ever clearing.
- The operator made the five `FLAG`s legible by re-running each lens read-only with a
  rationale-and-evidence prompt (a prototype of the door-cure's "move A"). That surfaced
  real, actionable findings instead of reflex.

## what the legible review found, and its disposition

- **Finding 1 (whole-acceptance-conformance).** The `operator-gate:` parser hard-locked the
  literal `tty`, contradicting the signed route's requirement to keep the value syntax
  B-ready for a later `hmac:<...>` scheme. **Remediated:** the parser now accepts a
  `<scheme>` / `<scheme>:<value>` grammar, implements only the `tty` liveness scheme, and
  rejects a reserved `hmac:` value as unsupported-scheme (not malformed) — proven by a new
  `check.sh` test.
- **Finding 2 (independent-coherence).** The explicit
  `direct --route|--constraint|--delegate` form could still record a gated new-work
  direction from machine-supplied text, reopening the "machine proposed, operator
  rubber-stamped" weakness Route A set out to close. **Remediated:** explicit forms are now
  refused for new gated work; the numbered `options.md` selection through `/dev/tty` is the
  only path that records gated direction. Proven by new `check.sh` tests (explicit-form
  refusal; numbered-path `/dev/tty` refusal).
- **pty finding (red-team).** `operator-gate: tty` proves a controlling terminal answered,
  not that an operator rather than a deliberately allocated terminal (e.g. via `script`)
  did. **Remediated:** the liveness claim in `hypercore.md`, `adapter/codex.md`, and
  `adapter/gates/frame.md`, and in the folded `collaboration`/`loop`/`adapter` statements,
  is narrowed to say exactly that. The claim was only narrowed, never strengthened.
- **fake-dir hole (security-permissions, red-team).** `HYPERCORE_ACCEPTANCE_FAKE_DIR` is
  honored before the real read-only reviewer is spawned and can manufacture non-dry-run
  acceptance artifacts, bypassing reviewer isolation. **Deferred:** pre-existing 008
  machinery, outside 009's charter; recorded as a concrete door-cure item in
  `PERFORMANCE-FINDINGS.md`. This is also why the env force-PASS path was never used to
  adopt 009.

## honest limits of this record

- The recorded phase-two unit diffs, handoffs, and tier-one verdicts describe the original
  signed build. The Findings 1/2 and pty remediations were applied by the operator on top of
  that build, so the current worktree is ahead of the recorded unit diffs. `./check.sh` is
  green on the final tree, and a re-run of the legibility probe confirms Findings 1 and 2 are
  resolved and no longer flagged.
- The on-disk `phase-two/tier-two-panel/*.md` artifacts still carry their original bare
  `FLAG` verdicts. They are superseded by the legibility-probe record, not cleared by a clean
  panel run.

## manual archive action

Fold the signed 009 route plus the three remediations into current intent — the
`collaboration`, `loop`, and `adapter` segments and their machine statements — stamp those
segments with `qqp-dev`, add `check.sh` coverage that the three segments carry the new
operator-act contract, then record this work under adopted history. The 009 material
(`adapter/loop.sh`, `check.sh`, `hypercore.md`, `adapter/codex.md`, `adapter/gates/*`) was
built in place during phase two and is already current.

This is not a clean phase-two acceptance record and is not precedent for later work. The
durable fix for the blind door is the performance / door-cure loop tracked in
`PERFORMANCE-FINDINGS.md`.
