# BPMN conformance report

Plan: `backlog/docs/plans/assets/doc-28/plan.bpmn`

## Summary

- Flow nodes: 15
- Accounted: 15
- Unaccounted: 0
- Diverged: 0
- Unknown completion IDs: 0
- Strict verdict: PASS

## Per-element status

| ID | Name | Type | Status | Evidence / note |
| --- | --- | --- | --- | --- |
| activation_approved | Local activation approved | StartEvent | done | Evidence: backlog/tasks/task-19 - Activate-the-OpenWiki-maintainer-from-operator-merges.md |
| build_userscript | Build generic merge userscript | ServiceTask | done | Evidence: browser/openwiki-merge-activator.user.js |
| build_local_handler | Build validating local handler | ServiceTask | done | Evidence: bin/qq-openwiki-activate |
| extend_installer | Register local protocol safely | ServiceTask | done | Evidence: bin/install.sh |
| verification_entry | Verification entry | ExclusiveGateway | done | Evidence: tests/test-qq-openwiki-activate.sh |
| run_checks | Run focused bridge checks | ServiceTask | done | Evidence: https://github.com/hypermemetic-ai/qq/pull/55 |
| checks_green | Checks green? | ExclusiveGateway | done | Evidence: https://github.com/hypermemetic-ai/qq/pull/55 |
| fix_check_failures | Fix check failures | ServiceTask | skipped | Evidence: https://github.com/hypermemetic-ai/qq/pull/55<br>Note: The initial focused suite and every post-review rerun passed, so no failing-Check correction branch was taken. |
| fresh_context_review | Run fresh-context review | UserTask | done | Evidence: https://github.com/hypermemetic-ai/qq/pull/55 |
| confirmed_findings | Confirmed findings? | ExclusiveGateway | done | Evidence: bin/qq-openwiki-activate<br>Note: The accountable agent reproduced the GUI PATH, global agent-name collision, dispatch claim, XDG data-home, workspace-validation, marker durability, and agent-identity failure paths before correction. |
| fix_review_findings | Fix confirmed findings | ServiceTask | done | Evidence: tests/test-qq-openwiki-activate.sh |
| open_activation_pr | Open activation PR | ServiceTask | done | Evidence: https://github.com/hypermemetic-ai/qq/pull/55 |
| pr_green | PR green? | ExclusiveGateway | done | Evidence: https://github.com/hypermemetic-ai/qq/pull/55<br>Note: GitHub reported mergeable MERGEABLE and mergeStateStatus CLEAN with no applicable status checks. |
| fix_pr_failures | Fix PR failures | ServiceTask | skipped | Evidence: https://github.com/hypermemetic-ai/qq/pull/55<br>Note: No GitHub-side check or mergeability failure occurred. |
| green_handoff | Activation PR green | EndEvent | done | Evidence: https://github.com/hypermemetic-ai/qq/pull/55 |

## Unaccounted elements

None.

## Unknown completion IDs

None.

## Divergence summary

No elements diverged.
