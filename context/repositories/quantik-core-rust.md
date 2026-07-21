# quantik-core-rust Packet

Purpose: optimized engine/search/storage/exporters and Rust adapters. Important modules: constants/bitboard/moves/game/board/state/QFEN/symmetry, minimax/MCTS/beam, opening book, `bench::contracts`, portability, and CLI binaries.

Version source: crate Cargo.toml; contract release constants live in bench contracts. Inspected clean `release/v1.2.0` at `8360a573b35a6e5fc48288d9c35ef0eb1290b5a0`; latest tag `v1.1.0`. Commands: cargo fmt, clippy, tests, build. `Cargo.lock` is ignored/absent while CI uses `--locked`, an unresolved build-policy risk.

Sensitive areas: low/high-level terminal differences, invalid parser layers, deterministic Python-compatible JSON, canonical action mapping, opening-book canonical representatives, MCTS transposition/policy identity, duplicated release constants. Workflow action/expectation is still 1.1.0 while source is 1.2.0.
