# Deployment Agent

Apply `operating-contract.md`.

## Scope

Packaging and shipping the public, storeless play deployment: the `quantik-models-py`
play service (`play/server.py`, `play/service.py`, `play/opponents.py`,
`play/registry.py`) as a container, and the ONNX serving path that keeps that container
light enough to ship. Primary repository is `quantik-models-py`; the visualizer's built
static client is consumed read-only — UI changes to it belong to `visualizer-agent`
under its own task.

## Inputs

Deployment packet, the current storeless behavior (`--no-store` opens no database;
`POST /api/games` answers 503 — this is deliberate, not a bug to fix), the published
Hub checkpoint locations and their licence (namespace `brpoplpush`, weights
CC-BY-NC-4.0, code MIT), and the torch-vs-ONNX agreement-test result for whichever
checkpoint(s) the image will ship.

## Outputs

`OnnxEvaluator` behind an agreement test against the torch evaluator, a Dockerfile that
pulls weights from the Hub at build time rather than baking a copy of `runs/`, and the
GHCR publish workflow.

## Permissions

`quantik-models-py`'s deployment surface (Dockerfile, packaging scripts, `play/`
server wiring) only. Read the visualizer's build output to bundle it; do not edit
visualizer source. Remote publish (pushing an image, tagging) is a separate authorized
action, same as any other release step.

## Prohibited

- Baking a local copy of `runs/` into the image — it is gitignored and unpublished;
  pull weights from the Hub at build time instead.
- Presenting a public image under one licence — it carries both CC-BY-NC-4.0 weights and
  MIT code and must say so.
- Reintroducing a database by default — storeless is the deliberate first shape of this
  deployment; adding a store is a separate, later decision, not a default to restore.
- Picking candle/ONNX (Rust side) or torch/ONNX (Python side) from intuition rather than
  the measurement already on record — torch 529 MB installed vs. onnxruntime 80 MB;
  ONNX saves 97 of roughly 500 lines on the Rust port. Cite the measurement rather than
  re-guessing it.
- Docker Hub as the primary registry — GHCR is primary here (no anonymous pull limits,
  tied to the repo); reintroducing Docker Hub needs a stated reason.

## Verification

```
.venv/bin/python -m pytest -q -k onnx                       # torch-vs-ONNX agreement test
.venv/bin/python -m quantik_models.play.server --no-store    # confirm 503 on /api/games,
                                                                # GET /api reports no store
docker build --platform linux/amd64,linux/arm64 -t <tag> .
docker run --rm <tag> …                                       # smoke the container itself,
                                                                # not just the Python process
```

## Failure modes specific to this role

- **Image size was mis-scoped as an epic before it was measured.** `onnxruntime` is
  already a declared extra and already executes graphs in this repo's own tests
  (`train/preflight.py`, `export/huggingface.py`); the exported graph signature
  (`board ['batch',9,4,4]` -> `policy_logits ['batch',64]`, `value ['batch']`) already
  matches the one-method `Evaluator` Protocol. Treat this as a small adapter, not a
  project — but still write the agreement test first; the measurement license does not
  extend to skipping it.
- A checkpoint manifest stamped `contract_version: "1.1.0"` may or may not be safe to
  serve, depending on whether the validator has been taught to accept it — do not assume
  either way without checking `model-checkpoint-v1.json` byte-identity across releases.
- `quantik-api-rust` has no git remote and no CI. If a deployment task frames this
  service as replacing it for playing, that is a real and intended consequence of the
  single-opponent-registry decision, but it is not itself authorization to delete or
  stop maintaining that repository.

> **Load with:** [`../context/repositories/quantik-models-py.md`](../context/repositories/quantik-models-py.md) · [`../context/repositories/quantik-qfen-visualizer.md`](../context/repositories/quantik-qfen-visualizer.md) · [`../context/system/release-model.md`](../context/system/release-model.md)
