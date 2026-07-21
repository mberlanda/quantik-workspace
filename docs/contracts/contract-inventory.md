# Contract Inventory

The inspected contracts 1.2.0 draft registers `qfen.v1`, `bitboard.v1`, `action-index.v1`, `selfplay.v1`, `tensor-board.v1`, `arrow-parquet-selfplay.v1`, `opening-book.v1`, `opening-book-summary.v1`, `observation.v1`, `game-result.v1`, `model-checkpoint.v1`, and `search-summary.v1`.

`quantik-core-contracts` owns these interfaces. Python and Rust implement most; models consumes the tensor/action/data/checkpoint subset. Implementation coverage and current gaps are recorded in discovery and should be regenerated from exact commits before declaring support.
