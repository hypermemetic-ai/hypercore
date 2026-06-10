# viewer as workbench: live loop, judgment queue, act in place

`w_b41a3744` · **open** · check: operator

on: `s_a6ea7c7a` — "The viewer is where the operator acts, not only reads: the loop is visible live as operat…"
fold when: the operator watches an operation land live, sees the queue of what awaits their judgment, and records a verdict or endorsement in the viewer without touching the CLI

## frame

- `wn_e0b7ab0e` the viewer today is read-mostly: one endorse button; every other verb — verdicts, amending, opening and folding work — flows through conversation with the machine. The operator wants to act on the system where they see it  (execute: machine, propose: machine)

## gather

- `wn_7e6f90c0` operator chose the three modes of interaction: watch the loop live (operations landing visibly in real time), be summoned to judge (a front-and-center queue of everything awaiting operator judgment), and act in the viewer (verdicts, endorsements, amendments, folds in place). Authoring intent directly in the viewer was offered and not chosen  (execute: machine, propose: operator)

## generate

- `wn_817645e0` live loop feed: the existing store fingerprint already re-derives the view; surface what changed — nodes that arrived since the last tick flash and a small feed names the recent moves  (execute: machine, propose: machine)
  - depends-on -> `wn_7e6f90c0` "operator chose the three modes of interaction: watch the lo…"
- `wn_d4038543` judgment queue: a front-and-center panel listing exactly what awaits the operator — pending endorsements, open operator-judged tests, folds awaiting confirmation — each item jumps to its node and offers the action  (execute: machine, propose: machine)
  - depends-on -> `wn_7e6f90c0` "operator chose the three modes of interaction: watch the lo…"
- `wn_d43648b0` act in place: verdict buttons on operator-judged tests, amend and strike on statements, fold confirmation on works — POST endpoints mapping one-to-one onto the verbs, every action recorded with the operator as warrant  (execute: machine, propose: machine)
  - depends-on -> `wn_7e6f90c0` "operator chose the three modes of interaction: watch the lo…"

## test

- `wn_01ba37d4` the judgment queue lists exactly what awaits the operator and drains as they act  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — CDP, 2026-06-10: the queue rendered 'awaiting your judgment (11)' with endorse rows; an operator-judged scratch test appeared in it and the recorded verdict drained the queue from 1 to 0
  - tests -> `wn_d4038543` "judgment queue: a front-and-center panel listing exactly wh…"
- `wn_294f80af` moves land in the open viewer as named feed entries and a flash, without a refresh  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — CDP, 2026-06-10: endpoint- and poll-driven reloads both produced named feed entries within two 3s ticks (test pass / statement amended / operator endorsed), each clickable to its node; arrivals flash via the visible stand-in when their work is closed
  - tests -> `wn_817645e0` "live loop feed: the existing store fingerprint already re-d…"
- `wn_41d436f8` the operator watches an operation land live, sees the queue of what awaits their judgment, and records a verdict or endorsement in the viewer without touching the CLI  (execute: machine, judge: operator, propose: machine)
  - verdict: **pass** — operator, via the viewer
  - tests -> `wn_d4038543` "judgment queue: a front-and-center panel listing exactly wh…"
  - tests -> `wn_d43648b0` "act in place: verdict buttons on operator-judged tests, ame…"
  - tests -> `wn_817645e0` "live loop feed: the existing store fingerprint already re-d…"
- `wn_9b596c72` the act-in-place endpoints map one-to-one onto the verbs and the gates hold  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — CDP + curl, 2026-06-10: /api/verdict recorded pass with grounds prefixed 'operator, via the viewer'; /api/amend rewrote the text and took ownership for the operator; /api/strike removed and renumbered; /api/fold without a commit refused with the gate's own words — re-verified against the live server
  - tests -> `wn_d43648b0` "act in place: verdict buttons on operator-judged tests, ame…"
