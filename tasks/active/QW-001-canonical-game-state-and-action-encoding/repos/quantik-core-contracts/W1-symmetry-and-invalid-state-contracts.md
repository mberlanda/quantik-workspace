# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-001-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts task

Objective: own the normative fixture/schema interpretation for canonical state and action encoding.

Inputs: current `game-state.md`, storage schemas, portability fixture, discovered engine/model differences. Outputs: JSON Schema, small JSONL golden cases, Arrow/Parquet logical/physical schema metadata, migration notes, and source-mode action checks. Required wire IDs: qfen, bitboard, action-index, tensor-board, selfplay, and Arrow/Parquet selfplay v1 unless a breaking change is approved.

Tests: validator success/error cases; deterministic row ordering; duplicate/illegal action rejection; transform/action round-trips; release metadata; local composite-action invocation. Completion requires contract-review approval and no future-tag reference in candidate jobs.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
