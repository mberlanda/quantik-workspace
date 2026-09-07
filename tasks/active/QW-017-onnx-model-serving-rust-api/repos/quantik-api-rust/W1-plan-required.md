# W1 — quantik-api-rust

Repository: `quantik-api-rust`
Branch: `plan/qw-017-quantik-api-rust` (one PR)

## Objective

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

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `docs/model-serving.md` (to rewrite), `src/lib.rs` (existing engine dispatch, verified: only `lib.rs`/`main.rs` exist today — genuinely greenfield for model inference), a new `model.rs` module, and `Cargo.toml` for the `--features model` gate. The new workspace ADR ("distinct from ADR 0009") lives in `quantik-workspace/docs/adr/`, a third repository this initiative doesn't list as a work item — noted here since `allowed_paths` can't span repositories.

depends_on W2: completion criterion 3 ("parity with the Python evaluator to a stated tolerance") needs W2's fixture set to exist first. decisions/invariants stay empty — decisions.md's seven points are already resolved (unheaded prose) but the Objective's own five-step approach is the operative plan here, not a decisions.md citation.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
