# W2 — quantik-core-py

Repository: `quantik-core-py`
Branch: `plan/qw-007-quantik-core-py` (one PR)

## Objective

# quantik-core-py task

Implement the approved compatibility validator and Python engine adapter over
public APIs without duplicating the trainer. Test unsupported formats,
architectures, shapes, actions, values, devices, and reference inference rows.
Preserve the current dirty release worktree.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: a new `inference.py` module and test file — verified nothing like it exists (`benchmarks/checkpoint.py` and Rust's `bench/checkpoint.rs` are a false-positive namespace collision: resumable *benchmark-run* checkpointing, unrelated to model weights). depends_on W1. `decisions`/`invariants` stay empty pending W1.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
