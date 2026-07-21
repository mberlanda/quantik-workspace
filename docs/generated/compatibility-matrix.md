# Compatibility Matrix

Generated/assessed 2026-07-21. “Supported” is withheld unless exact cross-stack evidence exists.

| Contracts | Wire IDs | Python | Rust | Models | Action ref | Status | Evidence / notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.2.0 candidate | qfen, bitboard, action-index, selfplay, tensor-board, Arrow/Parquet selfplay, opening-book/summary, observation, game-result, model-checkpoint, search-summary v1 | dirty candidate working tree; committed base 1.1.0 | 1.2.0 candidate | 0.1.0 still declares 1.1.0 | no published v1.2.0 | migration | Contracts 35 tests + 15 metadata/schema files + 11 JSONL rows passed. Rust/Python source declarations and workflows differ; models is stale; source action smoke and exact published evidence are missing. |
| 1.1.0 published | subset documented in historical release | tag exists | tag exists | no tag/release evidence | v1.1.0 | unknown | Tags were observed, but this workspace run did not execute an exact 1.1.0 cross-stack compatibility suite. |

Machine-readable matrices must validate against `schemas/compatibility-matrix.schema.json`. QREL-2026-001 cannot become `supported` until producer verification and all required consumer evidence are recorded.
