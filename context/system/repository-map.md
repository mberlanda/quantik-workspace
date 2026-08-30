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
| `quantik-api-rust` | Axum HTTP gateway exposing the Rust engines. | [`../repositories/quantik-api-rust.md`](../repositories/quantik-api-rust.md) |
| `quantik-qfen-visualizer` | Dependency-free browser app for playing and watching engines. Speaks `quantik.engine-request.v1` to any HTTP endpoint. | [`../repositories/quantik-qfen-visualizer.md`](../repositories/quantik-qfen-visualizer.md) |
| `quantik-workspace` | This repo — cross-repo drift checks, bounded AI context, task/release packets. | — |
| `articles` | Drafts and figures for the Substack series. **No git remote.** | [`../repositories/articles.md`](../repositories/articles.md) |

## Where the artifacts are published

**Trained model weights are not in any git repository.** `runs/` in `quantik-models-py`
is gitignored, so a checkout of this workspace contains no checkpoints. The weights are
published as Hugging Face model repositories under the **`brpoplpush`** namespace, one
per architecture, each carrying safetensors, an ONNX graph, the `model-checkpoint.v1`
manifest, and a card with `weights_hash` and `onnx_hash`:

| architecture | model repository |
| --- | --- |
| `cpool` | <https://huggingface.co/brpoplpush/quantik-cpool-c191-b6> |
| `attn` | <https://huggingface.co/brpoplpush/quantik-attn-d192-b6> |
| `resnet` | <https://huggingface.co/brpoplpush/quantik-resnet-c128-b6> |
| `mlp` | <https://huggingface.co/brpoplpush/quantik-mlp-h455-b4> |

All four verified public 2026-08-30 (HTTP 200, `private: false`). The repo id carries the
size suffix — `quantik-cpool` alone is **not** a valid id. Weights are **CC BY-NC 4.0**;
the code that produced them is MIT. Not an OSI licence, deliberately: every OSI licence
permits royalty-free commercial use, which is the one thing this reserves.

`scripts/stage_hub_repos.sh` in `quantik-models-py` stages a directory per model, and
`python -m quantik_models.export.huggingface` is the publishing entry point. **Nothing in
the codebase downloads weights at runtime** — the Hub is an upload destination today, and
a runtime fetch is scoped in [`QW-009`](../../tasks/active/QW-009-public-play-deployment/initiative.md)
and [`QW-017`](../../tasks/active/QW-017-onnx-model-serving-rust-api/initiative.md).

The staged layout — one subdirectory per model holding `manifest.json` and weights — is
exactly what the play service's model registry scans, so a staged Hub repository is a
model directory with no conversion.

**Development data is published too, as two private Hugging Face *dataset* repos.**
`runs/` in `quantik-models-py` is ~1.3 GB of solver output, corpora, enumerations, the
held-out probe, every checkpoint and every arena result. It is gitignored and lives on
one machine, and a model repo does not help — it carries weights and a card, not the
corpus the weights were fitted to.

| dataset repository | holds | rewritten |
| --- | --- | --- |
| [`brpoplpush/quantik-dev-data`](https://huggingface.co/datasets/brpoplpush/quantik-dev-data) | solver output, corpora, enumerations, probe, opening book | never — appended to only |
| `brpoplpush/quantik-dev-runs` | checkpoints (with resume state), sweeps, autoplay, evaluations | every training generation |

Split **by churn, not subject**: Hub history is permanent, so the churny half would
otherwise inflate the history of the irreplaceable half. `quantik-dev-runs` can be
squashed to reclaim space; `quantik-dev-data` never has to be.

To work with them, from `quantik-models-py`:

```bash
git lfs install
git clone git@hf.co:datasets/brpoplpush/quantik-dev-data runs/devdata
scripts/sync_dev_data.sh          # clone-or-pull, re-stage, show diff; never pushes
```

**A clone is not a working tree.** The layout is `<group>/runs/...`, so nothing under
`runs/devdata/` is on a path the trainer looks at — restoring means
`cp -r runs/devdata/corpora/runs/ .`. See
[`dev-data.md`](https://github.com/mberlanda/quantik-models-py/blob/main/docs/dev-data.md).

Package registries, for contrast: `quantik-core` publishes to
[crates.io](https://crates.io/crates/quantik-core) and
[PyPI](https://pypi.org/project/quantik-core/). **`quantik-models` is not on PyPI**
(404, verified 2026-08-30) and is not currently intended to be — see
[`quantik-models-py.md`](../repositories/quantik-models-py.md).

Versioning is lockstep across `quantik-core-contracts` / `quantik-core-rust` /
`quantik-core-py` only — `quantik-models-py`, the API, the visualizer, and `articles` each
version independently. See [`release-model.md`](release-model.md).
