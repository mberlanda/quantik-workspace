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

## 2026-09-20 — W1 in review

W1 is `in-review`: [quantik-models-py#69](https://github.com/mberlanda/quantik-models-py/pull/69) adds
`.github/workflows/publish-image.yml` (GHCR `ghcr.io/mberlanda/quantik-models-play`; triggers only on a
published release and `workflow_dispatch`, never on push to main; tags the release version and `latest`)
and documents the MIT-code / CC BY-NC-4.0-weights split in `docs/play-service.md`. pytest 652 passed,
5 skipped; mypy clean; 11/11 CI checks. Nothing publishes until a release is cut. W2 waits on the merge.
