# QW-003: Book-Guided Self-Play Runner

Upgrade the current Rust `selfplay_export` from empty-board MCTS-vs-MCTS into a
small, reproducible v1 runner that can sample safe book/frontier openings,
configure engine pairs, and preserve how each row was produced.

## Planning gate

Produce a design and implementation plan before code. Decide whether provenance
is additive `selfplay.v1` data, a companion run manifest, or a new wire version.
Resolve orientation and action remapping through QW-001 before serving moves
from canonical book entries.

## Exclusions

Model inference, H2H-informed active learning, and book write-back belong to
QW-005/QW-007. This task provides the deterministic runner they require.
