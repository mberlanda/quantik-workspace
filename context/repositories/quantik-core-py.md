# quantik-core-py Packet

Purpose: readable/reference Python behavior and adapters. Important modules: core/state/QFEN, move/board/game utils/validator, symmetry, artifact/ml/training data, opening-book, search, telemetry, portability report. Public exports are in `quantik_core.__all__`.

Version source: `pyproject.toml`; supported release: `contracts.py`. Inspected commit `728b03205707a8bb5a21afd091c6656b7c69c3fa`; local `release/v1.2.0` has 13 uncommitted release edits and no upstream. Preserve them. Commands: `./auto-lint.sh`, then `./dev-check.sh` in the repository virtualenv.

Sensitive areas: layered invalid-state rules, canonical transform/move mapping, overlapping compact serialization, duplicated action/tensor logic, pickle trust boundary, training-view ownership. Contracts workflow is stale/inconsistent. Release/package publication belongs to its own workflow; never publish from a task packet.
