# ADR 0009: ONNX Over Torch for Python Model Serving

## Context
A public play deployment needs to serve trained checkpoints without shipping a full
torch install. Measured in `quantik-models-py`'s venv: `torch` 529 MB installed against
`onnxruntime` 80 MB. `onnxruntime` is already a declared extra and already executes
graphs in this repo's own tests (`train/preflight.py`, `export/huggingface.py`).

## Decision
Serve inference through the exported ONNX graph and `onnxruntime`, not torch.
`selfplay.evaluator.Evaluator` is a one-method Protocol
(`(boards, legal) -> (priors, values)`) that `UniformEvaluator` already implements with
no torch import, and the exported graph signature (`board ['batch',9,4,4]` ->
`policy_logits ['batch',64]`, `value ['batch']`) matches that seam exactly. The first
deliverable is a torch-vs-ONNX agreement test on a real checkpoint, not the evaluator.

## Alternatives
Ship torch in the image because it is already a trusted dependency — rejected on the
measured 6.6x install-size difference plus CUDA-less wheel juggling a torch image needs.
Wait for `quantik-api-rust`'s candle-vs-ONNX decision to settle first — rejected; that
document (`quantik-api-rust/docs/model-serving.md`) weighed ONNX only against 97 of
roughly 500 lines saved on the Rust port, a different and unchanged argument. One graph
format serving both stacks is a new argument this decision does not ask that document to
re-open.

## Consequences
`OnnxEvaluator` must pass an agreement test before the Dockerfile is written. One
exported graph now serves both the Rust and Python stacks, so drift between them becomes
checkable rather than assumed away.
