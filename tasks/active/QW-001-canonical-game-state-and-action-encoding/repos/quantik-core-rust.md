# quantik-core-rust task

Objective: extend the repository-owned portability adapter for the same cases and deterministic report shape. Use existing bitboard/state/moves/symmetry/bench contract APIs; do not add workspace game logic.

Add focused Rust tests for parser versus constructor invalid-state boundaries, D4/shape/action mapping, canonical bytes, policy ordering/masks, and side-to-move value. Run fmt, clippy, and tests without relying on an unpublished contracts tag. Record exact commit and cross-produced evidence.
