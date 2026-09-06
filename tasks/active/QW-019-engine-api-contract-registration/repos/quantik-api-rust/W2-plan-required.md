# W2 — quantik-api-rust

Repository: `quantik-api-rust`
Branch: `plan/qw-019-quantik-api-rust` (one PR)

## Objective

# quantik-api-rust

## Objective

Validate against the registered schema instead of comparing a string constant.

## Inputs

- `src/lib.rs:22` — `REQUEST_SCHEMA`.
- The registered schemas.

## Completion criteria

- A test rejects a request that matches the `schema` string but violates the schema —
  this is the case the current check cannot catch and is the point of the initiative.
- The fixtures in `quantik-core-contracts` are exercised from the Rust test suite.
- Handoff records the contract version pinned.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
