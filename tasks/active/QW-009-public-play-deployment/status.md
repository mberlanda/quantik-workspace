# QW-009 Status

Created 2026-08-30, during reconciliation. Not started.

Requested 2026-08-29. The framing changed 2026-08-30: it was recorded as blocked
on a user decision ("~1 GB image vs build an evaluator first" made the two sides
sound comparable), and that framing was corrected once measured — torch/onnxruntime
is 529 MB vs 80 MB, and the exported graph signature already matches the
project's evaluator seam. So the blocking decision is resolved; the blocking
*work* (the agreement test, then the evaluator, then the Dockerfile) has not
started. Verified: no `OnnxEvaluator` class, no `Dockerfile`, no GHCR workflow
exist anywhere under `quantik-models-py`.

Next action: build the torch-vs-ONNX agreement test against a real checkpoint
before writing `OnnxEvaluator` — the test is what the rest of this initiative is
decided by, not the other way round.
