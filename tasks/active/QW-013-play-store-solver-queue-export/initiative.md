# QW-013: Play-Store Solver-Queue Export

> **Purpose:** Close the loop from human-played positions to the training
> corpus, using the same `to-solve.qfen.gz` artifact autoplay already produces.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md)

## Problem and motivation

The play service (QW-008) already extracts and stores every position a human
game visits (`game_positions`, `play.store.distinct_positions` — done, tested,
currently uncalled in production). Nothing turns that into solver input, so
positions people actually reach have never fed the corpus; only autoplay's
engine-explored positions have.

## Existing and desired behaviour

Existing, verified 2026-08-30: `src/quantik_models/play/export.py` and
`tests/test_play_export.py` **already exist in the working tree, untracked**
(`git status --porcelain` shows `?? src/quantik_models/play/export.py` and `??
tests/test_play_export.py`) — another session is actively implementing this
charter right now. The file present implements `export_queue`, converts
`game_positions.canonical_key` (a decimal string) against `ExactCorpus`'s
`uint64` keys through one explicit conversion, and writes `to-solve.qfen.gz` via
the existing `arena.pack.write_gzip`. Desired: the module lands reviewed, tested
end to end against the real games database, and merged.

## Contracts and repositories

`quantik-models-py` only. Touches `game-result.v1` only insofar as
`game_positions` is derived from a recorded `game-result.v1` row; no schema
change.

## Constraints and preserved invariants

- **Human game outcomes are never labels. Only positions travel.** `games.winner`
  is read only for reporting, never as a training signal.
- **The canonical-key trap is the one thing that must not regress.** Comparing
  the store's decimal-string keys against `ExactCorpus`'s `uint64` array without
  converting silently drops nothing and looks like success — this happened once
  already, at 35% of a 26,157-position queue, about twelve hours of solver time.
- Read-only against the games database — it is the one irreplaceable artifact in
  this project.
- Torch-free: nothing in this path needs torch.

## Migration and compatibility strategy

None — additive entry point, no format change; output is byte-compatible with
the existing autoplay-produced `to-solve.qfen.gz`.

## Release strategy and ordering

The full charter is written up as
[`briefs/play-solver-queue-export.md`](../../../briefs/play-solver-queue-export.md)
— that document is the plan; this packet links to it rather than duplicating it.
One PR, atomic commits, merged when CI is green.

## Risks and exclusions

Excludes any change to `game_positions` or `distinct_positions` themselves — if
the query needs something it does not provide, that is a separate decision, not
silently widened here.

## Acceptance criteria

See `manifest.yaml`.
