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

**Four of five acceptance criteria are already met — verified in the code,
not assumed:**

1. `tests/test_onnx_evaluator_agreement.py` exists:
   `test_onnx_and_torch_evaluators_agree_on_a_real_checkpoint` builds a real
   `cpool` checkpoint via `export_checkpoint` and compares `OnnxEvaluator`
   against `NetEvaluator`.
2. `OnnxEvaluator` is implemented (`src/quantik_models/selfplay/evaluator.py`,
   wired through `arena/registry.load_onnx_evaluator`/`build_agent`), no
   torch import.
3. `docker/Dockerfile` pulls weights from the Hub at build time
   (`RUN pip install ... '.[serve,hub]'`, comment: "no local runs/
   checkpoint") — this is QW-030 M4
   ([quantik-models-py#66](https://github.com/mberlanda/quantik-models-py/pull/66)).
4. `--no-store` 503 behavior is in place: `play/server.py:257` raises
   `ServiceError(503, "this service was started without a game store")`.

**The one real gap:** no CI workflow publishes the image to GHCR yet.
`scripts/build_docker_image.sh` only builds locally
(`docker build -f docker/Dockerfile ...`); no `.github/workflows/*.yml`
references `ghcr.io` or a `docker push`. `allowed_paths` names a new
`publish-image.yml` for that step, plus the two files above for context.

This initiative's own tracking had drifted from the code (top-level
`status` was `not-started`) — corrected to `largely-complete`. `decisions`
here are already resolved in `decisions.md` (not headed sections, but
settled prose: runtime is ONNX, visualizer/api-rust out of formal scope,
GHCR over Docker Hub) rather than left open like most other initiatives'
`decisions.md` files — still not cited via `decisions.md#Heading` since
none of the four decisions has an addressable heading to reference.
`invariants` stays empty: nothing in `canonical-invariants.md` bears on
image publishing.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
