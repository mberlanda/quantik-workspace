# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-007-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts task

Define supported/unsupported fixture cases, capability metadata, tensor/action/
value validation, error classification, and inference comparison format. Keep
architecture evolution compatible or version the contract explicitly.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: the existing model-checkpoint-v1 doc/schema, plus a new fixtures directory (none exists yet — verified). `decisions`/`invariants` stay empty: decisions.md's five questions (first runtime format, supported architecture/dtype/device matrix, validation order, tolerance/fixtures, capability-negotiation owner) are open.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
