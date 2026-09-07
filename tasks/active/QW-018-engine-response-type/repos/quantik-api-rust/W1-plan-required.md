# W1 — quantik-api-rust

Repository: `quantik-api-rust`
Branch: `plan/qw-018-quantik-api-rust` (one PR)

## Objective

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

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `src/lib.rs` — confirmed the discard at line 192 and the legality recomputation at 134-156 the Objective names. depends_on W2: the response can't extend a schema that doesn't exist yet (`engine-response.v1` isn't registered — verified, this initiative and QW-019 both need it created first). decisions/invariants stay empty — decisions.md's five points are already resolved (unheaded prose).

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
