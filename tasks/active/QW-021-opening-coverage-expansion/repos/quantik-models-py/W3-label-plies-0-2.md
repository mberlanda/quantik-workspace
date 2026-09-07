# W3 — Label plies 0-2 with the exact oracle

**Repository:** `quantik-models-py` · **Branch:** `feat/label-plies-0-2` · one PR
**Depends on:** W2 merged with a passing smoke run. **Dispatch:** execute and record.

Plies 0-2 are the plies no corpus reaches at all. The enumerations are already on disk; only
oracle labelling is missing.

## Steps

1. Follow `docs/opening-coverage-partition.md` exactly. If the partition and this packet ever
   disagree, the document wins.
2. Label per the partition, writing to a new output directory. Never overwrite an existing
   labelled set.
3. Print and record solved-of-total at start, and write progress as you go, so an interrupted run
   is legible without comparing `wc -l` across two files. (That absence is exactly why two earlier
   solves sat abandoned and unnoticed — see QW-028.)
4. If the run is interrupted, resume rather than restarting; record that you did.

## Completion criteria

- Every canonical live position at plies 0-2 in the partition carries an exact value.
- The output directory, position counts, and wall-clock are recorded in
  `docs/opening-coverage-partition.md`.
- Counts match the enumeration totals for those levels — state the expected and actual numbers.
- Nothing is merged into any existing corpus in this item.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record counts, wall-clock, output path, and any resume.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
