# W3 — quantik-core-rust

Repository: `quantik-core-rust`
Branch: `plan/qw-007-quantik-core-rust` (one PR)

## Objective

# quantik-core-rust task

Implement fail-fast manifest/runtime compatibility and the approved inference
adapter. Keep optional runtime dependencies feature-gated. Test malformed and
unsupported artifacts, tensor/action/value checks, reference inference parity,
and search integration boundaries.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: a new `inference.rs` module and test file, plus `Cargo.toml` for the optional, feature-gated runtime dependency the Objective asks for (matching the existing `arrow-parquet` optional-feature pattern). Same namespace-collision caveat as W2 — `bench/checkpoint.rs` is unrelated. depends_on W1.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
