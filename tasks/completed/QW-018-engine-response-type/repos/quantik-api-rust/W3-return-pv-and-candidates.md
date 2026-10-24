# W3 — Stop discarding the principal variation

**Repository:** `quantik-api-rust` · **Branch:** `feat/engine-response-candidates` · one PR
**Depends on:** W2 merged. **Dispatch:** mechanical.

## Steps

1. `src/lib.rs:192` — `Ok((result.best_move, None))` discards `MinimaxResult.pv`, which is
   populated on every search. Return it.
2. Populate ranked candidates with per-move scores in the units this engine actually produced, each
   labelled per W1 section 1: minimax exact values, MCTS visit counts, network logits. Do not
   normalise across engines — the label exists so the client can tell them apart.
3. `certainty`: `proof` only for exact results, `estimate` for everything derived from a network
   value. Never default it; every response path sets it explicitly.
4. `engine_version` for model engines carries the `model_id` per W1 section 4, not `CORE_REVISION`.
5. Tests in `mod tests`: a minimax response carries a non-empty PV; an MCTS response carries
   visit-unit candidates; an exact result is `proof` and a network result is `estimate`; a model
   engine's `engine_version` is the model id.

## Completion criteria

```sh
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

- All clean.
- The PV test fails if you restore `None` at line 192 — verify by restoring it, watching it fail,
  then reverting.
- Every response path sets `certainty`; grep the constructors and confirm none relies on a default.

## Handoff

Record the commands and the PV revert check.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
