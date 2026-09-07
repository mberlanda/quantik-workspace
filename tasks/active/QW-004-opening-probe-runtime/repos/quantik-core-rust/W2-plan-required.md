# W2 — quantik-core-rust

Repository: `quantik-core-rust`
Branch: `plan/qw-004-quantik-core-rust` (one PR)

## Objective

# quantik-core-rust task

Implement probe generation/reading and an engine-facing abstraction only after
the contract is approved. Test representative and transformed orientations,
hits/misses, bounds, corrupt/truncated input, unsupported versions, and
deterministic output. Record size/latency evidence without inventing targets.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: the existing `opening_book.rs` to read probe source data from, a new `opening_probe.rs` module and `probe_builder` binary (matching the existing `book_builder.rs` pattern), and a new test file. depends_on W1 per the Objective ("only after the contract is approved"). `decisions`/`invariants` stay empty until W1 resolves the contract.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
