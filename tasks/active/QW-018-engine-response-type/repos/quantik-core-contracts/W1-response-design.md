# W1 — Design the extended engine response

**Repository:** `quantik-core-contracts` · **Branch:** `docs/engine-response-candidates` · one PR
**Blocked on:** QW-019 W1 merged (`engine-response.v1` must be registered before it is extended).
**Dispatch:** judgment — capable model, human review.

The engine response returns a single move and discards everything the search already computed.
`quantik-api-rust/src/lib.rs:192` returns `Ok((result.best_move, None))` — `MinimaxResult.pv` is
populated on every search and thrown away. The network emits all 64 logits and a value per forward
pass; MCTS has visit counts; the oracle scores every legal move.

The deeper problem: **nothing distinguishes an estimate from a proof.** A tanh value and an exact
oracle result reach the client as the same kind of claim.

## Decide and record in `docs/engine-response-v1.md`

1. **Ranked candidates.** The field shape for ranked moves with per-move scores, and how the
   **unit** is carried — visits, logits, or exact values — labelled per candidate. A score whose
   unit is implicit is a number nobody can compare across engines.
2. **Principal variation.** Where an engine has one, how it is returned. Optional for engines that
   genuinely have none; say which those are.
3. **`certainty`.** A **required** field with exactly two values: `estimate` and `proof`. A network
   tanh value is always `estimate`; an exact oracle result is `proof`. No engine may omit it, and
   none may blur them. State that explicitly — it is the whole point of the field.
4. **`engine_version` for model engines** carries the `model_id`, not the core revision, so an
   exported game records which network played. Note the tension: QW-019's fixtures show the Python
   service already puts an opponent id here while the Rust API puts `CORE_REVISION`. Reconcile
   them, and say which each implementation must send.
5. **Backward compatibility.** How a client tolerates the new fields being absent from an older
   server, and how an older client tolerates their presence. Both directions.

## Completion criteria

- Five sections, each a decision.
- `certainty` is specified as required, with the two values and the rule for assigning them.
- Section 4 resolves the `engine_version` divergence rather than describing it.
- `git diff --stat` touches `docs/engine-response-v1.md` only.

## Handoff

Record the field shapes and the `engine_version` resolution.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
