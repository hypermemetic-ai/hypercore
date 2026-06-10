# the work loop speaks the operation alphabet

`w_423ff83b` · **folded** · check: operator

on: `s_3729cb59` — "An operation is one move on the problem state, of six kinds: frame, gather, derive, gener…"
fold when: work nodes are operations (frame, gather, derive, generate, test, commit), their products are material on those nodes, relations carry the combinators, and roles live in props
folded: 2026-06-10T08:49:39+00:00
produces:
- `s_d4bd1b45` — "Nodes are operations. Intent statements are not nodes: they live in their own store with …"
- `s_5365a11a` — "Relations between operations carry the combinators. depends-on is the causal link from a …"

## generate

- `wn_6a9e4db2` synthesize and repair stay out until the primitive-vs-compound contest resolves; adopt only if real work keeps wanting them  (execute: machine, propose: machine)
- `wn_8302514e` work-fold's machine check reads test operations' verdicts instead of check nodes  (execute: machine, propose: machine)
  - depends-on -> `wn_8d5935e3` "replace work-add kinds step/candidate/check/result with the…"
- `wn_8d5935e3` replace work-add kinds step/candidate/check/result with the six operations; products become material on operation nodes, not node kinds  (execute: machine, propose: machine)
- `wn_b91eab58` relation types carry the combinators: depends-on as causal link, tests, commits, reframes, decomposes-into  (execute: machine, propose: machine)
- `wn_c9884850` roles as props on each operation (propose, execute, judge, decide); decide on a commit is the operator's and cannot be delegated  (execute: machine, propose: machine)
- `wn_efd59a7c` test may want to split into challenge and verdict; decide from practice, not theory  (execute: machine, propose: machine)

## test

- `wn_44b27c3f` work-add accepts only the six operations; legacy kinds are refused  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — exercised on a sandbox copy of the repo, 2026-06-10: all refusal paths and the full gauntlet ran
  - tests -> `wn_8d5935e3` "replace work-add kinds step/candidate/check/result with the…"
- `wn_4559dcbf` combinators wire as relations: tests, commits binds a generate only, reframes a frame only, depends-on, decomposes-into; path traverses them  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — exercised on a sandbox copy of the repo, 2026-06-10: all refusal paths and the full gauntlet ran
  - tests -> `wn_b91eab58` "relation types carry the combinators: depends-on as causal …"
- `wn_7aca437d` roles land in props with kind defaults; a commit's decide cannot be delegated to the machine  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — exercised on a sandbox copy of the repo, 2026-06-10: all refusal paths and the full gauntlet ran
  - tests -> `wn_c9884850` "roles as props on each operation (propose, execute, judge, …"
- `wn_ddb2f58c` work-fold's machine gate reads test verdicts and requires a commit as settlement; render and load round-trip survive  (execute: machine, judge: machine, propose: machine)
  - verdict: **pass** — exercised on a sandbox copy of the repo, 2026-06-10: all refusal paths and the full gauntlet ran
  - tests -> `wn_8302514e` "work-fold's machine check reads test operations' verdicts i…"

## commit

- `wn_666eca0f` the work loop speaks the alphabet: six operation kinds, combinators as relations, roles in props  (decide: operator, execute: machine, propose: machine)
  - depends-on -> `wn_b91eab58` "relation types carry the combinators: depends-on as causal …"
  - depends-on -> `wn_8302514e` "work-fold's machine check reads test operations' verdicts i…"
  - depends-on -> `wn_c9884850` "roles as props on each operation (propose, execute, judge, …"
  - commits -> `wn_8d5935e3` "replace work-add kinds step/candidate/check/result with the…"

## material

- [the work loop speaks the operation alphabet](m_b6be8d2e.md) (result) — on the work
- operation set — research panel findings (document) → `research/operation-set-findings.md` — on the work
- [the settlement](m_b2bc67b2.md) (document) — on wn_666eca0f
