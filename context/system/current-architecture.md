# Current Architecture

Both engines use eight player/shape bitboard planes and QFEN. Contracts 1.2.0 draft covers core state/action/data/checkpoint/search interfaces. Rust produces most bulk/search artifacts; Python provides readable adapters and training projections; models consumes Python-core readers and emits NPZ/checkpoints. Compatibility uses repository-owned portability reports and shared fixtures, with known cross-stack Parquet evidence gaps.
