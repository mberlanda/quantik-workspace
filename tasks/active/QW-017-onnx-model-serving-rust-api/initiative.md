# QW-017: ONNX Model Serving in the Rust API

> **Purpose:** Give `quantik-api-rust` a policy/value runtime, and replace a design
> recommendation whose stated premise has since become false.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-api-rust.md`](../../../context/repositories/quantik-api-rust.md)

## Problem and motivation

`quantik-api-rust/docs/model-serving.md` is the repo's only design document and it
opens with "Status: **decision not yet made.** This document exists to make it." It
recommends **candle**, and its central argument is that *the architecture has been
identical across all twelve checkpoints* — so the 97 lines of architecture code that
ONNX would save are a one-off, while the ~330-line `BatchedMCTS` port is unavoidable
either way.

That argument named its own reversal trigger, and the trigger has fired. **Four
architectures now exist** — `mlp`, `resnet`, `attn`, `cpool` — with genuinely different
module trees. The candle section describes only the ResNet's tensor names. Porting four
architectures by hand, and every future one, is a different proposition from porting one.

Two further facts postdate the document:

- **Every checkpoint already ships a verified ONNX graph** at opset 18 with dynamic
  batch, and `onnx_hash` is in the manifest and on the published Hub card. The
  document's objection — that `weights_hash` covers the safetensors while the server
  would run the ONNX file — was true when written and is not true now.
- **All four graphs use only 20 standard operators:** `Add, Concat, Conv, Div, Erf,
  Gather, Gemm, LayerNormalization, MatMul, Mul, ReduceMean, Relu, Reshape, Shape,
  Slice, Softmax, Squeeze, Tanh, Transpose, Unsqueeze`.

## Existing and desired behaviour

Existing: the gateway serves `random`, `minimax`, `mcts` and `beam` from `quantik-core`.
There is no network inference and no ML dependency.

Desired: the same gateway serves published checkpoints, behind a Cargo feature, with
the graph loaded from ONNX rather than a hand-ported architecture.

## Contracts and repositories

`quantik-api-rust` implements. `quantik-models-py` supplies the parity oracle and the
exported graphs; it is not modified except to expose fixtures.
`model-checkpoint.v1` is read. `tensor-board.v1` is the encoding that must be matched
exactly — see the trap below.

## The trap, stated once and prominently

`tensor-board.v1` pins only `[rows, 9, 4, 4]` and dtype. It does **not** choose a
channel layout, and two exist:

- **mover-relative** (`fastboard.encode_tensors`) — planes 0-3 belong to the side to
  move. **This is what every trained checkpoint uses.**
- **colour-ordered** (`quantik_core.ml_data.qfen_to_tensor`) — planes 0-3 are player 0.
  Nothing in training uses it.

`model-serving.md` originally specified the colour-ordered one; local commit `02bfcd1`
corrects it inline. A runtime built to the old text swaps the players on every position
where player 1 is to move: **no error, correct answers on half the positions,
confidently wrong on the other half.**

The discriminating fixture: QFEN `"A.../..../..../...."` has one piece, so
`side_to_move == 1`. **Mover-relative puts the 1.0 at channel 4; colour-ordered puts it
at channel 0.** A port that passes on even-ply positions and fails this one has exactly
this bug.

## Scope note — what changed underneath this initiative

When WORKSTREAMS §4 was written, the Rust API was the only way the visualizer could
play a network. It no longer is: the Python play service ([`QW-008`](../../completed/QW-008-local-play-service/initiative.md))
serves all four models plus the classical engines through one opponent registry, and
[`QW-009`](../QW-009-public-play-deployment/initiative.md) containerizes it.

So this initiative's justification is **distribution**, not capability: a single static
binary with no Python runtime. That is a real benefit and a narrower one than "the place
models get served". The rewritten `model-serving.md` should say so rather than let the
original rationale drift.

## Provenance

Migrated from WORKSTREAMS §4 ("Model serving in the Rust API — DECISION PENDING") and
§9 ("NN as an opt-in add-on"), which are folded together here: §9 is §4's packaging,
has no value without it, and its "candle and `hf-hub`" text is superseded by the
runtime reversal above.
