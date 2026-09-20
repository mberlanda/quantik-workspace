# QW-018 Status

**specified-not-built.** The specification is this packet; no code exists.

Verified 2026-08-30 — `quantik-api-rust/src/lib.rs:192` still reads
`Ok((result.best_move, None))`.

Blocked on [`QW-019`](../QW-019-engine-api-contract-registration/initiative.md) by
decision 4.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §6.

## 2026-09-20 — W1 decided and merged

[contracts#27](https://github.com/mberlanda/quantik-core-contracts/pull/27) records the design in `docs/engine-response-v1.md`. All five recommendations were accepted 2026-09-20:

- **Compatibility:** register `engine-response.v2` with `certainty` required; v1 and its fixtures stay frozen.
- **`certainty`:** `estimate | proof`; minimax earns `proof` only when every score in the response is proven.
- **`engine_version`:** the artefact that decided the move (`model_id` for checkpoint engines; core revision, or the installed release string, for pure-core engines) plus an optional `engine_config`. Not comparable as strings across implementations; consumers key on `(engine_kind, engine_version, engine_config)`.
- **Shapes:** `candidates: [{action_index, score, unit}]` with `unit` in `visits|logit|prior|value`, and a flat `pv` array with `pv[0] == action_index`.

W2 registers v2 and moves the design half to `docs/engine-response-v2.md`. W3 needs a core accessor for per-move minimax scores and an MCTS visit list not collapsed by the transposition table. models-py pooling keys change to `(engine_kind, engine_version, engine_config)`.
