# quantik-api-rust

## Objective

Extend the engine response with candidates, PV and `certainty`, and stop discarding
`MinimaxResult.pv`.

## Inputs

- `src/lib.rs:192` — `Ok((result.best_move, None))`, the discard.
- `src/lib.rs:134-156` — server-side legality recomputation; candidate lists are
  filtered against this, never the client's set.
- The registered `engine-response` schema from QW-019.

## Approach

Per engine kind, return what it has: minimax gives PV and exact-ish scores with
`certainty: proof` only where the oracle actually proved it; MCTS gives visit counts,
`estimate`; the network gives logits and a value, `estimate`, always.

## Completion criteria

- A test per engine kind asserts the candidate list is non-empty, in the declared
  units, and a subset of the server's legal set.
- A test asserts an engine cannot return a response without `certainty`.
- A test asserts the network path never reports `proof`.
- Handoff records the schema version implemented.
