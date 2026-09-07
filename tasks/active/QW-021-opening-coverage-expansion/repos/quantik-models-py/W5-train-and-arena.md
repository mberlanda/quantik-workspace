# W5 — Train on the expanded corpus and judge it in the arena

**Repository:** `quantik-models-py` · **Branch:** `feat/opening-coverage-training` · one PR
**Depends on:** W4 merged. **Dispatch:** execute and record.

## Steps

1. Train on W4's corpus. Use the comparison and lineup **named in W1's document** — it was fixed
   before the numbers existed, deliberately. Do not substitute a different comparison now.
2. Evaluate in the **arena** against the current lineup, side-balanced, on an unspent seed
   (not `20260829`, `20260909`, `20261001`, `20261015`, or W2/W3's). Confirm unused by grep,
   and name it.
3. Report held-out accuracy against the **new** partition's probe, clearly labelled as the new
   partition. Do not compare it to the old 99.63% as though they measured the same thing — they
   do not, which is the whole reason W1 exists.
4. Record everything in `docs/opening-coverage-partition.md` under "Result".

## Completion criteria

- Arena results at the plies W1 named, side-balanced, with distinct-games checked first.
- The new probe number is labelled with its partition.
- No sentence compares the new probe to 99.63% without naming that the partitions differ.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the seed, arena margins, probe number, and the checkpoint path.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
