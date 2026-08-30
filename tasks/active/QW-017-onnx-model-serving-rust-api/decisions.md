# QW-017 Decisions

1. **ONNX, not candle — reversing `model-serving.md`.** The document's argument rests on
   one architecture; there are four. ONNX now saves the architecture port for every
   present and future architecture, and the `weights_hash`/`onnx_hash` objection has been
   answered by the exporter. The old recommendation stays in the document marked
   superseded, with the evidence, because it was correct on the facts it had.

2. **This is a separate decision from ADR 0009.** ADR 0009 covers *Python* serving and
   its evidence is install size (torch 529 MB vs onnxruntime 80 MB). Neither number
   applies to a Rust binary. The Rust decision is argued from architecture count and the
   operator set, and needs its own ADR. Do not cite 0009 as though it settled this.

3. **`tract-onnx` vs `ort` is settled by loading all four graphs, not by argument.** The
   original doc preferred `tract` because `ort` was a release candidate. That is a
   maturity claim with a shelf life. `LayerNormalization` is fused and opset-17+, so it
   is the operator most likely to be missing — check it first, and record what the losing
   runtime actually did.

4. **Compile-time feature, not a plugin ABI.** Two engines do not justify a plugin
   system. `--features model` pulls the runtime in; without it the binary has no ML
   dependencies. Two images ship. Rejected: dynamic loading — all cost, no current use.

5. **Runtime model selection by environment variable**, e.g.
   `QUANTIK_MODELS=<model_id>,...`, resolved against manifests, hash-verified at load,
   **refusing** a mismatch. Serving zero models is valid. A "warn and continue" path is
   explicitly rejected: a mismatched hash is precisely the failure that otherwise
   presents as a subtly bad player.

6. **`engine_version` carries the `model_id`**, never a filename or display label, so an
   exported game records which network played. Shared with
   [`QW-018`](../QW-018-engine-response-type/initiative.md).

7. **The parity oracle is the Python play service**, which already runs these graphs
   against these fixtures. Rejected: hand-written expected tensors — they encode the
   author's belief about the layout, which is the thing under test.
