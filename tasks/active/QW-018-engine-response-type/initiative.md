# QW-018: Engine Response Type — Candidates, PV, Certainty

> **Purpose:** Return what the engines already computed, and stop presenting an
> estimate and a proof as the same kind of answer.
> **Load with:** [`context/repositories/quantik-api-rust.md`](../../../context/repositories/quantik-api-rust.md),
> [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md)

## Problem and motivation

The response is the bottleneck, not the engines. Everything below is computed at the
call site and discarded:

- **Ranked candidates.** The network emits all 64 logits plus a value on every forward
  pass; argmax is the caller's choice, made too early. MCTS has visit counts. The exact
  oracle scores every legal move.
- **Principal variation.** `MinimaxResult.pv` is populated on every search.
  `quantik-api-rust/src/lib.rs:192` returns `Ok((result.best_move, None))` — verified
  still true 2026-08-30.
- **`certainty`.** The cheapest field and the most valuable one. A network's `tanh`
  value is an estimate and never a proof; the exact oracle is certain. The same endpoint
  currently returns both with nothing to tell them apart.

No new algorithms are needed. This is a response type.

## Existing and desired behaviour

Existing: one `action_index` plus metadata. The client cannot show why, cannot show
what was close, and cannot tell a guess from a solved position.

Desired: the move, a ranked candidate list in the engine's own units, a PV where one
exists, and an explicit `certainty`.

## Contracts and repositories

`quantik-api-rust` implements. The response shape belongs in
`quantik-core-contracts` — but `engine-response.v1` is not registered anywhere today,
which is [`QW-019`](../QW-019-engine-api-contract-registration/initiative.md). Extending
an unregistered phantom contract would deepen the problem, so **QW-019 comes first**.

## Constraints and preserved invariants

- **`win_probability = (value + 1) / 2` is exact** — Quantik has no draws, and both
  terminal conditions are losses for the side to move. A probability may be derived
  from a value without qualification; what needs qualifying is whether the *value* was
  estimated or proved. That is the `certainty` field, and it is not the same question.
- **Legality is recomputed server-side** and the client's claim is not trusted
  (`src/lib.rs:134-156`). Candidate lists must be filtered by the server's own legal
  set, not the client's.
- **Units are never mixed.** Visit counts, logits and exact values are not comparable;
  each candidate list says which it is in.

## Provenance

Migrated from WORKSTREAMS §6 ("API response type — SPECIFIED, NOT BUILT"). The
`lib.rs:192` claim was re-verified on 2026-08-30.
