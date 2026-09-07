# W2 — Smoke-label one slice before committing hours

**Repository:** `quantik-models-py` · **Branch:** `feat/opening-label-smoke` · one PR
**Depends on:** W1 merged **and** human-reviewed. **Dispatch:** execute and record.

Project discipline: no expensive run starts before a small one has confirmed throughput and
correctness. QW-028 exists because two multi-hour solves were abandoned without anyone noticing.

## Steps

1. Read `docs/opening-coverage-partition.md`. Label a **small slice of one level only**, per its
   partition.
2. Confirm correctness: spot-check labelled values against an independent exact solve of the same
   positions. Agreement must be exact, not approximate — these are game-theoretic values.
3. Measure and record throughput: positions per second, and the extrapolated wall-clock for the
   full plies 0-2 set. Note that a per-ply extrapolation in this project has already been wrong by
   more than an order of magnitude, so present the estimate with that caveat and take it on an
   idle machine.
4. Record all of it in `docs/opening-coverage-partition.md` under a "Smoke run" heading.

## Completion criteria

- The slice size, the exact command, throughput, and the extrapolated full cost are recorded.
- The independent spot-check is reported as exact agreement, or the run is reported as failed.
- No full solve is started in this item.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record throughput, the extrapolation, and the spot-check result.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
