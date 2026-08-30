# Repository Map

> **Purpose:** Which of the 8 Quantik repos owns what, and where the detail lives.
> **Load with:** [`current-architecture.md`](current-architecture.md) (how they fit together) · [`domain-glossary.md`](domain-glossary.md) (terms) · [`canonical-invariants.md`](canonical-invariants.md) (what holds across all of them) · [`release-model.md`](release-model.md) (how the first four ship)

This file is loaded into every repository bundle — keep it a map, not a description.
Repository-specific detail belongs in `../repositories/<repo>.md`; add a row here only
when a new repository is added to the workspace.

| Repo | Owns | Detail |
| --- | --- | --- |
| `quantik-core-contracts` | Shared schemas, fixtures, validators, and the composite GitHub Actions both stacks call. `VERSION` is the source of truth; tagged first in a release. | [`../repositories/quantik-core-contracts.md`](../repositories/quantik-core-contracts.md) |
| `quantik-core-rust` | The `quantik-core` crate: bitboards, QFEN, symmetry, minimax/MCTS/beam search, opening-book generation, the exact oracle. Publishes to crates.io. | [`../repositories/quantik-core-rust.md`](../repositories/quantik-core-rust.md) |
| `quantik-core-py` | The `quantik-core` package: artifact readers, QFEN/bitboard helpers, tensor encoders, manifest validation. Publishes to PyPI. | [`../repositories/quantik-core-py.md`](../repositories/quantik-core-py.md) |
| `quantik-models-py` | Training, dataset materialization, autoplay, checkpoint export, evaluation, and the play service. **Not** published to PyPI. | [`../repositories/quantik-models-py.md`](../repositories/quantik-models-py.md) |
| `quantik-api-rust` | Axum HTTP gateway exposing the Rust engines. **No git remote.** | no packet yet |
| `quantik-qfen-visualizer` | Dependency-free browser app for playing and watching engines. Speaks `quantik.engine-request.v1` to any HTTP endpoint. | no packet yet |
| `quantik-workspace` | This repo — cross-repo drift checks, bounded AI context, task/release packets. | — |
| `articles` | Drafts and figures for the Substack series. **No git remote.** | no packet yet |

Versioning is lockstep across `quantik-core-contracts` / `quantik-core-rust` /
`quantik-core-py` only — `quantik-models-py`, the API, the visualizer, and `articles` each
version independently. See [`release-model.md`](release-model.md).
