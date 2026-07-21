# quantik-core-contracts task

Objective: own the normative fixture/schema interpretation for canonical state and action encoding.

Inputs: current `game-state.md`, storage schemas, portability fixture, discovered engine/model differences. Outputs: JSON Schema, small JSONL golden cases, Arrow/Parquet logical/physical schema metadata, migration notes, and source-mode action checks. Required wire IDs: qfen, bitboard, action-index, tensor-board, selfplay, and Arrow/Parquet selfplay v1 unless a breaking change is approved.

Tests: validator success/error cases; deterministic row ordering; duplicate/illegal action rejection; transform/action round-trips; release metadata; local composite-action invocation. Completion requires contract-review approval and no future-tag reference in candidate jobs.
