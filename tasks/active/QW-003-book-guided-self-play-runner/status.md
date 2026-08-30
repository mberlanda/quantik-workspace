# QW-003 Status

Plan required. Plain MCTS self-play exists; book guidance, engine pairs, and
provenance do not.

## 2026-08-30 reconciliation

Still `plan-required`. Verified in code: `quantik-core-rust/crates/quantik-core/examples/selfplay_export.rs`
takes only `--games`, `--iterations`, `--seed`, `--out` — no book, opening, or
engine-pair flags, and both sides are still `MCTSEngine` from the empty board.
Nothing built since this initiative was written changes that. Its dependency,
QW-001, is also still open (see that initiative's status).

Left active, unchanged in substance.
