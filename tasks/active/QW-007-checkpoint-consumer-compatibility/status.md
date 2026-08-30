# QW-007 Status

Plan required. Checkpoint production and manifest parsing exist; engine-side
weight loading and inference compatibility do not.

## 2026-08-30 reconciliation

Still `plan-required` for the actual scope of this initiative — **consumer-side**
inference in `quantik-core-py` and `quantik-core-rust`. Verified: neither repository
has any code path that loads `model-checkpoint.v1` weights or an ONNX/safetensors
graph for inference. `quantik-core-py/src/quantik_core/artifact_data.py` and
`contracts.py` only parse and validate the checkpoint *manifest* (`ModelCheckpointManifest`,
`parse_model_checkpoint_manifest`) — no tensors are loaded, no forward pass exists.

What has changed, and materially de-risks decision 1 (runtime/weights format) once
this is picked up:

- Every current checkpoint now ships a `model.onnx` graph alongside
  `weights.safetensors`, with a manifest-verified `onnx_hash`
  (`export/checkpoint.py`, `export/huggingface.py`).
- `quantik-models-py` already runs those ONNX graphs at inference time in its own
  test/preflight paths (`train/preflight.py`, `export/huggingface.py`), and
  `onnxruntime` is a declared extra there — see new initiative QW-009, which found
  `onnxruntime` (80 MB) against `torch` (529 MB) and confirmed the exported graph
  signature (`board [batch,9,4,4]` -> `policy_logits [batch,64]`, `value [batch]`)
  matches the project's one-method evaluator protocol exactly.
- Checkpoints are staged for and (pending an SSH key) will be pushed to Hugging Face
  (`brpoplpush/quantik-*`), so a portable, versioned artifact to build a Rust or
  Python consumer against will exist publicly, not just in a gitignored `runs/`.

None of this is the consumer surface itself — it is evidence for which format
(ONNX) that consumer surface should probably target first when this initiative is
picked up, from a different repo's use of the same graphs, not from work done in
`quantik-core-py`/`quantik-core-rust`.

Left active, unchanged in substance.
