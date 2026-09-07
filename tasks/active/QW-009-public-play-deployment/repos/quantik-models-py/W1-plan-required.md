# W1 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-009-quantik-models-py` (one PR)

## Objective

# quantik-models-py task

Objective: build the torch-vs-ONNX agreement test first, against a real checkpoint
under `runs/`, not a synthetic tensor. Only once it passes, add `OnnxEvaluator`
(onnxruntime + numpy softmax, no torch import) implementing
`selfplay.evaluator.Evaluator`. Then a `Dockerfile` that pulls weights from the
Hub at build time (`brpoplpush/quantik-*`) rather than baking `runs/`, and a GHCR
publish workflow.

Relevant modules: `src/quantik_models/selfplay/evaluator.py` (the Protocol and
`UniformEvaluator` reference implementation), `export/huggingface.py` and
`train/preflight.py` (existing onnxruntime call sites to model the new evaluator
on), `play/server.py` (what the container ultimately serves).

Inputs and outputs: reads a `model.onnx` graph + `manifest.json` (`onnx_hash`
verified); outputs identical `(priors, values)` shape to `NetEvaluator`.

Required contracts release: current `quantik-core` 1.2.0; `model-checkpoint.v1`
unchanged.

Constraints: `OnnxEvaluator` must not import torch, even conditionally. The
agreement test's tolerance must be stated and justified, not defaulted.

Dependencies: QW-008 (the service this container packages).

Commands and focused tests: new `tests/test_onnx_evaluator.py` (agreement test);
`pytest -k onnx`.

Expected artifacts: `src/quantik_models/selfplay/onnx_evaluator.py` (or similar),
`Dockerfile`, a GHCR workflow file.

Completion criteria: agreement test passes against a real checkpoint with a
stated tolerance; image builds and runs `--no-store` with `POST /api/games`
still answering 503.

Handoff path: create `tasks/active/QW-009-public-play-deployment/handoffs/` only
once a handoff exists.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
