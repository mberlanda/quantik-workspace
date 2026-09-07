# W4 — Confirm the induced values against a direct oracle solve

**Repository:** `quantik-models-py` · **Branch:** `feat/confirm-shallow-induction` · one PR
**Depends on:** W3 merged. **Dispatch:** execute and record.

The induced values must not be accepted on the strength of the induction alone. Solve levels 1 and
2 directly, root-only, and compare.

## Steps

1. Run a direct root-only oracle solve of canonical levels 2 and 1.
2. Compare every induced value against the directly solved one. Agreement must be **exact** —
   these are game-theoretic values, not estimates.
3. Any disagreement is a finding, not a rounding issue. Report it and stop; do not adjust the
   induction to match.
4. Record the comparison in `docs/corpus-structure.md`: how many positions, the command, the result.

## Completion criteria

- Every induced value at levels 1 and 2 is compared against a direct solve.
- The document records exact agreement, or the disagreement and its size.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the counts, the command, and the agreement result.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
