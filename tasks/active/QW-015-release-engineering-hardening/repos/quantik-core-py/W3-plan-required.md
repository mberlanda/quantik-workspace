# W3 — quantik-core-py

Repository: `quantik-core-py`
Branch: `plan/qw-015-quantik-core-py` (one PR)

## Objective

# quantik-core-py

## Objective

Same as `quantik-core-rust`: drop `expected-release` from the PR-time job.

## Dependency

Blocked on `quantik-core-contracts` landing criteria 1 and 2.

## Completion criteria

- The PR-time workflow calls the action without `expected-release`.
- A PR touching only Python goes green while `quantik-core-rust` is on a different
  release. This is the concrete demonstration that the deadlock is gone.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
