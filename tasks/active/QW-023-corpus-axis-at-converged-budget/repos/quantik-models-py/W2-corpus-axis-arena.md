# W2 — Arena the two converged arms

**Repository:** `quantik-models-py` · **Branch:** `feat/corpus-axis-arena` · one PR
**Depends on:** W1 merged, **and** W1 having reported a converged run. **Dispatch:** execute and record.

One arena, two agents: `patience-cpool` (the v1 converged arm) and W1's new checkpoint.

## Steps

1. Read W1's `docs/corpus-axis-converged.md` and confirm it reports early stopping. If it does
   not, stop — there is no comparison to run yet.
2. Run one arena containing both checkpoints at start plies **3, 6 and 9**, side-balanced.
3. The seed must not be `20260829` or `20260909` (both spent), nor `20261001` (QW-024), nor
   `20261015` (QW-026). Confirm your choice is unused with a grep before launching and name it in
   the write-up.
4. Check the distinct-games / independence line before reading any win rate. A degenerate pairing
   is not reportable.
5. Append the arena results to `docs/corpus-axis-converged.md`: per-ply, side-balanced, with the
   shared probe numbers **alongside** the arena rather than instead of them.

## Completion criteria

- Results for all three start plies, split by seat.
- The seed is named and shown unused.
- Probe and arena numbers appear together.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the seed, the distinct-games numbers, and the key margins.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
