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

`allowed_paths` in `manifest.yaml`: `src/lib.rs` — confirmed the exact consts at lines 22-23 (`REQUEST_SCHEMA`/`RESPONSE_SCHEMA` = `"quantik.engine-request.v1"`/`"quantik.engine-response.v1"`). depends_on W1. decisions/invariants stay empty.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
