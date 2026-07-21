# Repository Assessment

Assessment date: 2026-07-21. All sibling repositories were inspected in place and were treated as read-only. `quantik-core-py` already contained user changes; none of them were modified.

## Snapshot

| Repository | Purpose | Branch / inspected commit | Working tree | Default branch | Package / current checkout version | Published tags seen locally |
| --- | --- | --- | --- | --- | --- | --- |
| `quantik-core-py` | Readable Python engine and data adapters | `release/v1.2.0` / `728b03205707a8bb5a21afd091c6656b7c69c3fa` | **Dirty:** 13 modified files, no upstream | `main` | PyPI `quantik-core`; working tree `1.2.0`, committed source `1.1.0` | `v1.1.0`, `v1.0.0`, `v0.1.1` |
| `quantik-core-rust` | Optimized Rust engine, search, opening books, exporters | `release/v1.2.0` / `8360a573b35a6e5fc48288d9c35ef0eb1290b5a0` | Clean; upstream equal | `main` | crate `quantik-core` `1.2.0` | `v1.1.0` |
| `quantik-core-contracts` | Interoperability schemas, fixtures, validators, actions | `release/v1.2.0` / `beb26e7e07184b2fd61b9aef242358788400d861` | Clean; upstream equal | `main` | contracts repository `1.2.0` draft | `v1.1.0`, `v1.0.0` |
| `quantik-models-py` | Training views, policy/value model, checkpoints | `main` / `ea8f32ad4fac8fdf4f9620e9a4163e08bb6f2469` | Clean; upstream equal | `main` | PyPI `quantik-models` `0.1.0` | none |

The Python release branch is based on a commit whose `pyproject.toml` and supported-contract declaration are `1.1.0`; uncommitted release work changes them and associated fixtures/tests to `1.2.0`. The workspace records both facts and never treats the dirty values as committed evidence.

## `quantik-core-py`

- Build: setuptools via `pyproject.toml`, Python `>=3.12`. Main dependencies are NumPy, psutil, and zstandard; optional CBOR, Arrow, docs, benchmark, and development groups exist.
- Version sources: `pyproject.toml#/project/version` is authoritative. `importlib.metadata.version("quantik-core")` in `src/quantik_core/__init__.py` is derived. `src/quantik_core/contracts.py::SUPPORTED_CONTRACTS_RELEASE` is a separate supported-contract declaration.
- Commands: `.venv/bin/python -m pytest`; `./auto-lint.sh`; `./dev-check.sh`; Black, flake8, and mypy settings live in `pyproject.toml`/`.flake8`. Benchmarks are scripts/modules under `benchmarks/` and documented in `benchmarks/README.md`.
- CI/release: workflows include build, tests, integration, daily smoke, contracts, and publish. `publish.yml` owns package publication. The contracts workflow currently references `mberlanda/quantik-core-contracts/actions/validate-contracts@v1.1.0`, but discovery found no such action path in the contracts checkout. Its opening-book action and all `expected-release` inputs remain `1.1.0`.
- Public API: `quantik_core.__init__` exports bitboard `State`, `Move`, move validation/application/generation, QFEN, `QuantikBoard`, search engines/evaluation, symmetry, training-dataset views, telemetry, and contract declarations. Console scripts are `quantik-training-dataset` and `quantik-api-portability-report`.
- Formats/artifacts: QFEN, eight-plane bitboards, 16-byte payloads and 18-byte versioned state, CBOR, JSON/JSONL, SQLite opening books, NumPy training views, and optional Arrow/Parquet readers/writers. Committed contract fixtures are under `tests/fixtures/`.
- Contract state: the dirty checkout declares contracts `1.2.0`; HEAD declares `1.1.0`. Wire IDs include QFEN, bitboard, action index, self-play, tensor board, Arrow/Parquet self-play, opening book/summary, observation, game result, model checkpoint, and the working-tree addition `search-summary.v1`.
- Documentation convention: root operational documents plus `docs/`, `docs/superpowers/` plans, `CHANGELOG.md`, benchmark evidence, and focused module docs. Historical plans are not version mirrors.
- Drift risks: contract version, fixtures, tests, and workflows are duplicated; current workflow refs do not match the dirty candidate; training-dataset materialization overlaps models; QFEN parsing can be syntax-only unless validation is requested. Python's symmetry API can represent colour swaps, but default canonicalization uses D4 plus shape permutation without colour swap, matching the discovered Rust default; the misleading Python docstring still creates interpretation risk.

## `quantik-core-rust`

- Build: Cargo 2021 workspace, crate `quantik-core`; optional `arrow-parquet` feature. `crates/quantik-core/Cargo.toml#/package/version` is authoritative.
- Commands: `cargo test`; CI uses `cargo test --workspace --all-targets --all-features --locked`, `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets --all-features -- -D warnings`, and a release build. `Cargo.lock` is absent and ignored, so `--locked` is a probable clean-CI defect.
- CI/release: `.github/workflows/rust.yml`; binary-release and crates.io jobs exist but are disabled. It consumes `actions/opening-book-consistency@v1.1.0` with `expected-release: "1.1.0"` while source emits `1.2.0`.
- Public API: bitboard, board, moves, game, state, QFEN, D4/shape symmetry, minimax/MCTS/beam, opening-book database, benchmark contracts, and portability reporting. Several CLI binaries own validation, book generation/inspection, benchmarking, and portability reports.
- Formats/artifacts: QFEN; eight little-endian `u16` planes; 18-byte versioned state/canonical key; deterministic Python-compatible JSON; JSONL; optional Arrow/Parquet; SQLite; benchmark position JSON.
- Contract state: multiple source constants declare contracts release `1.2.0`; checked-in fixtures do too. Portability validation compares the contracts manifest, `VERSION`, and fixture release. Wire IDs are modeled separately.
- Documentation convention: `README.md`, `CHANGELOG.md`, benchmark/search docs, dated benchmark evidence, and historical `docs/superpowers/` material.
- Drift risks: one release value is duplicated across contract families; source and workflow expectations disagree; a stale test name still says 1.1.0; the changelog presents untagged 1.2.0 as released; canonicalization does not colour-swap; opening-book moves cannot always be mapped from canonical representatives; low-level and high-level terminal/invalid-state behavior differ.

## `quantik-core-contracts`

- Build: dependency-free Python validator scripts; no package manifest. Tests use `python3 -m unittest discover -s tests -v`.
- Version sources: `VERSION` is primary and `contracts.json#/release_version` is a required mirror. Both are `1.2.0`; the manifest status is `draft`.
- Commands verified during discovery: all 35 unit tests passed. `scripts/validate_contracts.py` validated 15 schema/metadata JSON files and 11 JSONL rows against `1.2.0`.
- CI/release: source validation, tag-triggered archive/GitHub Release packaging, reusable Python/Rust workflows, release smoke, and opening-book consistency. Composite actions are `actions/cross-language-smoke` and `actions/opening-book-consistency`. Reusable workflows check out the contracts repository without an exact ref; consumers must supply exact publication refs themselves.
- Published interfaces: repository-tag-versioned composite actions and reusable workflows; release archives include docs, schemas, fixtures, validators, actions, workflows, and a generated release manifest.
- Schemas/contracts: `qfen.v1`, `bitboard.v1`, `action-index.v1`, `selfplay.v1`, `tensor-board.v1`, `arrow-parquet-selfplay.v1`, `opening-book.v1`, `opening-book-summary.v1`, `observation.v1`, `game-result.v1`, `model-checkpoint.v1`, and `search-summary.v1`.
- Documentation convention: normative per-contract docs/schemas, implementation-status matrix, research notes, versioning/consistency guidance, and a root index.
- Drift risks: public README and consistency examples already use unpublished `@v1.2.0`; `docs/versioning.md` still uses current-looking `1.1.0` examples; candidate CI validates schemas directly but does not exercise the checked-out composite actions by relative path; the stable action path advertised by Python does not exist.

## `quantik-models-py`

- Build: setuptools, Python `>=3.12`, package `quantik-models`; NumPy base with optional PyArrow, PyTorch/safetensors, pytest, and mypy. Authoritative version is `pyproject.toml#/project/version`; `src/quantik_models/__init__.py` mirrors `0.1.0`.
- Commands: `python -m pytest`, `scripts/run_smoke_pipeline.sh`, `quantik-models-materialize`, and `quantik-models-train`. No release, lint, format, or benchmark workflow is configured.
- CI/release: E2E data pipeline and train smoke only. They check out sibling default branches without exact refs. There are no actions, reusable workflows, tags, or releases.
- Public API: data materialization/datasets/labels, policy-value network/config, masked logits, trainer/config, and checkpoint export.
- Formats/artifacts: consumes observation/self-play JSONL and Parquet through Python-core adapters; writes compressed NPZ; exports safetensors, training reports, and `model-checkpoint.v1` manifests.
- Contract state: checkpoint defaults and inline self-play fixtures still say `1.1.0`; no explicit supported-contract constant exists. `policy-value.v1` and `policy-logits-64+value-tanh` are competing output identifiers.
- Documentation convention: focused model/tensor/training documents and a smoke-pipeline README.
- Drift risks: current source is incompatible with contracts/core Python 1.2.0; mutable-branch CI cannot prove a published combination; training views duplicate Python core with divergent NPZ fields, tag encoding, and label weights; self-play masks infer legality from positive visits; D4/action remapping is unimplemented.

## Canonical evidence summary

- Board: 4×4, row-major `0..15`; four shapes and two players; eight player/shape planes. Contracts `docs/game-state.md`, Python QFEN/core tests, and Rust `constants.rs` agree.
- Pieces/QFEN: A–D, uppercase player 0 and lowercase player 1; four top-to-bottom ranks. QFEN does not encode side to move.
- Moves: shape-major ordering and `action_index = shape * 16 + position`, producing 64 slots. The legal mask uses bit `action_index`.
- Legality: target empty; inventory bounded; opponent may not have the same shape in a touched row, column, or 2×2 zone. Parser-level validation is weaker than full game-state validation in both engines.
- Terminal/winner: a row, column, or 2×2 zone containing all four shapes wins independent of colour. Stalemate semantics are defined at higher board layers and require explicit compatibility evidence.
- Serialization: bitboard plane order is player 0 shapes 0–3 then player 1 shapes 0–3. Durable Rust state is version byte, flags, and eight little-endian `u16` planes. Cross-language deterministic JSON is tested separately.
- Symmetry: D4 transforms are implemented in both engines. Both consider shape relabeling for default canonicalization and do not colour-swap. Python can explicitly represent/apply a colour swap, so whether colour swap belongs to any future canonical contract remains an open decision.
- Models: tensors are float32 `[9,4,4]`; channels 0–7 are the bitboard planes and channel 8 is the side-to-move plane. Policy length is 64. Value is in `[-1,1]` from the row's side-to-move perspective.
- Deterministic identity: the Rust canonical 18-byte key is evidence-backed. No portable numeric hash contract exists.

## Dependency and release order

Contracts owns schemas/fixtures/actions. Python and Rust consume and implement them; models consumes contracted data through Python core and data produced by both engines. For contracts 1.2.0 the safe order is contracts candidate validation, immutable contracts tag/publication, published-action verification, Python/Rust adoption, model adoption, cross-stack evidence, then compatibility-matrix and release-lock completion. Repository package versions remain independent.

## Unresolved issues to task, not assume

1. Decide whether canonical equivalence includes colour swap and how transforms remap moves/actions.
2. Establish one supported-contract source in Rust and models.
3. Decide ownership/versioning of the derived training view and legal-action mask semantics.
4. Add checked-in cross-stack Parquet interchange evidence.
5. Align candidate action testing without depending on an unpublished exact tag.
6. Resolve the nonexistent `actions/validate-contracts` consumer path and the absent Rust lockfile policy.
