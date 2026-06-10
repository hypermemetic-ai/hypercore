# the settlement

The operator decided on 2026-06-10, in conversation, to bind the alphabet
design: work nodes are operations (frame, gather, derive, generate, test,
commit); products are material on operation nodes; relations carry the
combinators (depends-on, tests, commits, reframes, decomposes-into);
roles live in props, and a commit's decide is the operator's,
non-delegable. Implementation landed as git commit 10b54ab; tests
wn_44b27c3f, wn_4559dcbf, wn_7aca437d, wn_ddb2f58c all pass.

Held open by design: synthesize/repair stay out (wn_6a9e4db2); test may
split into challenge/verdict (wn_efd59a7c). Decide from practice.
