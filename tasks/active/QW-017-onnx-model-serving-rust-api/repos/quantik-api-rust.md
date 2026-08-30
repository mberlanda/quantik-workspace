# quantik-api-rust

## Objective

Load an ONNX policy/value graph behind a Cargo feature and serve it through the
existing engine interface, with an encoder proven mover-relative.

## Inputs

- `docs/model-serving.md` — to rewrite; keep the superseded recommendation visible.
- `src/lib.rs` — the existing engine dispatch and the legality recomputation at
  `src/lib.rs:134-156`, which the model path must also go through.
- Published manifests at <https://huggingface.co/brpoplpush> — `onnx_hash`,
  `weights_hash`, `architecture_spec`, `model_id`.

## Approach

1. Rewrite the design document; write the ADR. Nothing else starts before this.
2. Load all four graphs in `tract-onnx` and in `ort`. Record what happens to
   `LayerNormalization`. Choose from the result.
3. Encoder, ~20 lines. Its first test is the discriminating fixture, written before the
   encoder.
4. Inference behind `--features model`; hash-verified load; refuse on mismatch.
5. `BatchedMCTS` port, ~330 lines. Unavoidable under either runtime; sequence it last.

## Completion criteria

- `cargo test` covers: the mover-relative fixture; a refused hash mismatch; parity with
  the Python evaluator to a stated tolerance.
- `cargo build` without `--features model` produces a binary with no ML dependency —
  demonstrated from the dependency tree, not asserted.
- Handoff records the runtime chosen, the evidence that chose it, and the tolerance.
