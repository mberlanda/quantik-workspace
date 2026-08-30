# QW-009 Decisions

1. **Runtime is ONNX, not torch — decided, not open.** Measured 2026-08-30:
   `torch` 529 MB installed vs `onnxruntime` 80 MB (6.6x), before CUDA-less wheel
   juggling a torch image would also need. `onnxruntime` is already trusted
   (already a declared extra, already executing graphs in tests). Rejected
   alternative: ship torch and accept the larger image — rejected because the
   size difference is large and unforced, not because torch would not work.
2. **`quantik-qfen-visualizer` and `quantik-api-rust` are not carried as formal
   `affected_repositories`.** Neither is registered in `workspace.yaml`. Adding
   them is out of this task's scope. The container's visualizer half and any
   Rust-side serving decision are described in prose only.
3. **Open:** whether the image ships all four trained architectures or one. Not
   decided — the torch-vs-ONNX question was the blocker; this is the next
   decision once `OnnxEvaluator` exists.
4. **Open:** GHCR vs Docker Hub is decided in favor of GHCR (rate limits, tied to
   the repo), inherited from the reasoning already recorded for workstream 8 —
   not re-litigated here, but not yet implemented either.
