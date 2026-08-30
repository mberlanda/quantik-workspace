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
