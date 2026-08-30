# QW-009: Public Play Deployment — Storeless Docker

> **Purpose:** Ship the play service (QW-008) plus the visualizer as one public,
> storeless container, so games are playable without committing to collecting
> them.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/system/release-model.md`](../../../context/system/release-model.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

Storage is deliberately deferred — the point of shipping this publicly is to find
out whether the games are worth collecting before committing to collecting them.
`--no-store` already opens no database and `POST /api/games` already answers 503;
the server needs nothing new for that half. What is missing is the image itself,
and the runtime it serves inference through.

## Existing and desired behaviour

Existing: `quantik-models-py` has no ONNX evaluator, despite `onnxruntime` already
being a declared optional dependency (`[project.optional-dependencies].onnx`) and
already executing graphs in `train/preflight.py` and `export/huggingface.py`'s own
tests. `selfplay/evaluator.Evaluator` is a one-method Protocol —
`UniformEvaluator` already implements it torch-free in six lines. The exported
graph signature was verified against a real checkpoint
(`runs/lrsweep/sweep-cpool-6e-4/best/model.onnx`): input `board ['batch', 9, 4, 4]
float32`, outputs `policy_logits ['batch', 64]` and `value ['batch']` — matching
the Evaluator seam exactly.

Desired: `OnnxEvaluator` behind an agreement test proving it against the torch
path on a real checkpoint, then a Dockerfile that pulls weights from the Hub at
build time and carries the licence split honestly (weights CC-BY-NC-4.0, code
MIT).

## Contracts and repositories

`quantik-models-py` only, in this registry. The container also spans
`quantik-qfen-visualizer` (the static app served alongside the API) and possibly
`quantik-api-rust` (workstream 4's own runtime decision, made independently and
on the same measurement) — neither is a registered workspace repository; see
`decisions.md`. Touches `model-checkpoint.v1` only insofar as `OnnxEvaluator`
must read the same `onnx_hash`-verified graph the manifest already describes.

## Constraints and preserved invariants

- The torch-vs-ONNX agreement test is the load-bearing artifact, not
  `OnnxEvaluator` itself — "everything the image serves is decided by that test."
- Do not build a general plugin/runtime-negotiation system; two runtimes (torch
  for training, ONNX for serving) do not justify one.
- A public image must carry both licences — CC-BY-NC-4.0 (weights) and MIT
  (code) — visibly, not merged into one blanket statement.

## Migration and compatibility strategy

Additive: `OnnxEvaluator` is a new class beside the existing torch `NetEvaluator`,
selected by which extra is installed. No existing evaluator changes.

## Release strategy and ordering

1. Agreement test (blocking).
2. `OnnxEvaluator`.
3. Dockerfile + weight-pull-at-build-time.
4. GHCR publish, multi-arch (`linux/amd64` + `linux/arm64`).

## Risks and exclusions

Excludes the Rust-side model-serving decision (workstream 4, `quantik-api-rust`)
— same measurement, separate repository, separate initiative once
`quantik-api-rust` is registered. Excludes skill levels / how-to-play UI (QW-010)
and puzzle mode (QW-011), which do not require this initiative and can ship
independently.

## Acceptance criteria

See `manifest.yaml`.
