# W2 — quantik-core-rust

Repository: `quantik-core-rust`
Branch: `plan/qw-015-quantik-core-rust` (one PR)

## Objective

# quantik-core-rust

## Objective

Drop `expected-release` from the PR-time job that calls the composite action, once
the action's default is removed.

## Dependency

Blocked on `quantik-core-contracts` landing criteria 1 and 2. Removing the input
before the default is gone changes nothing — the literal still applies.

## Completion criteria

- The PR-time workflow calls the action without `expected-release`.
- A PR touching only Rust goes green while `quantik-core-py` is on a different release.
- The tag build still checks out `quantik-core-py` at the same ref; that ordering is
  unchanged by this initiative and must be shown still working.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
