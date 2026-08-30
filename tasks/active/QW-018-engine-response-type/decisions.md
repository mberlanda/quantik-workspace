# QW-018 Decisions

1. **`certainty: estimate | proof`, two values, required.** Rejected: a numeric
   confidence. A number invites arithmetic between a `tanh` output and a solved result,
   which is exactly the conflation the field exists to prevent. Two values cannot be
   averaged.

2. **Candidate scores stay in the engine's own units, labelled.** Rejected: normalising
   everything to a probability. Visit counts and logits normalise differently, and a
   normalised number hides which engine produced it. The client can normalise; the
   server should not pretend.

3. **`engine_version` is the `model_id` for model engines.** The core revision says
   which *code* ran, not which *network*. An exported game whose `engine_version` is a
   core commit is unattributable later. Shared with
   [`QW-017`](../QW-017-onnx-model-serving-rust-api/decisions.md) decision 6.

4. **QW-019 first.** Rejected: shipping the fields now and registering later. The
   response is already hardcoded in two repositories with nothing keeping them in
   agreement; adding five fields to both by hand doubles that debt.

5. **Additive only.** New fields are optional on the wire so an older visualizer
   against a newer server keeps working, and a newer visualizer must render an absent
   candidate list without error.
