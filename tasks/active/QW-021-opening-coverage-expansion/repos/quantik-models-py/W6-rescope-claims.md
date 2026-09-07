# W6 — Rescope every published claim that quotes 99.63%

**Repository:** `quantik-models-py` · **Branch:** `docs/rescope-generalization-claim` · one PR
**Depends on:** W5 merged. **Dispatch:** mechanical.

The 99.63% generalization figure was measured against a probe this initiative consumed. Every
place it is quoted as a live claim is now wrong, or right only about a partition that no longer
exists.

## Steps

1. Find every occurrence: `grep -rn "99.6\|99\.63" docs/ README.md src/`.
2. For each, either update it to the new partition's number from W5, or explicitly scope it —
   "measured against the pre-expansion partition (see `docs/opening-coverage-partition.md`)".
   Silence is not an option; an unqualified 99.63% is a claim about a probe that no longer exists.
3. List every occurrence and its disposition in the PR description.
4. Confirm `docs/models.md` reflects that the exact opening book remains preferred for opening
   play, per W1's decision 5 — a stronger network in the opening does not change which one answers.

## Completion criteria

- The grep returns no unqualified live use of the old figure.
- Every occurrence is listed in the PR description with its disposition.
- `docs/models.md` states the opening-book preference.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the grep output before and after.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
