# quantik-models-py Packet

> **Purpose:** training, dataset materialization, autoplay/arena, checkpoint export, evaluation, and the play HTTP service.
> **Load with:** [`https://github.com/mberlanda/quantik-models-py/blob/main/AGENTS.md`](https://github.com/mberlanda/quantik-models-py/blob/main/AGENTS.md), [`../system/current-architecture.md`](../system/current-architecture.md), [`quantik-core-py.md`](quantik-core-py.md), [`quantik-core-contracts.md`](quantik-core-contracts.md)

Important modules: data materialization/dataset/labels, model spec/network, trainer, export/checkpoint, and `play/` (server, service, registry of ~20 opponents, SQLite game recorder, puzzle generator — added 2026-08-30, see `AGENTS.md`). Version source/mirror: pyproject and package `__version__` (`0.1.0`). Inspected clean `main` at `9a29d30` (2026-08-30); two untracked files present that day (`play/export.py`, `tests/test_play_export.py`), not yet committed.

**Repo-local instructions are in `AGENTS.md`** (added 2026-08-30) — load it for the venv/extras setup, the torch-vs-torch-free module boundary, the three CI workflows and what each protects, and the standing measurement-discipline conclusions. Do not duplicate its content here.

Commands: `.venv/bin/python -m pytest -q` (520 tests collected, verified 2026-08-30); `mypy` is a declared `[dev]` extra but **is not wired into any script or CI gate** — do not claim a type check passed unless you ran it yourself. Contracts defaults/fixtures still say 1.1.0; CI uses mutable sibling branches for `e2e-data-pipeline.yml` only — `tests.yml` deliberately installs the *published* `quantik-core` from PyPI instead. Sensitive areas: duplicate Python-core training views, divergent NPZ fields/weights, positive-visits mask versus legal mask, all-false mask behavior, output-contract naming, missing D4 action remapping.

**Publishing: `quantik-models` is NOT on PyPI** (verified 2026-08-30 — `pypi.org/pypi/quantik-models/json` returns 404; only `quantik-core` is published). Trained checkpoints are published separately, as safetensors + ONNX model repositories on Hugging Face under `brpoplpush` (verified live 2026-08-30) — see the publishing entry point `python -m quantik_models.export.huggingface` and `scripts/stage_hub_repos.sh`; nothing in the tooling itself uploads.

Make tensor shapes, action indices, masks, value perspective, exact data/checkpoint contracts, and input revisions explicit in every handoff.
