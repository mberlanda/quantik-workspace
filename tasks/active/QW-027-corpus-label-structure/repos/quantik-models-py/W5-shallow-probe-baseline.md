# W5 — Report the baseline beside every policy number

**Repository:** `quantik-models-py` · **Branch:** `fix/shallow-probe-baseline` · one PR
**Depends on:** W1 merged. **Dispatch:** mechanical.

Mass-on-optimal at ply 0 is **1.000 for any distribution**, because every legal move is optimal
there. Reported alone it reads as a perfect score. The random-legal-play baseline is what makes
the number mean anything — measured, the flagship checkpoints score 0.160 and 0.336 against
baselines of 0.170 and 0.331, i.e. indistinguishable from random.

## Steps

1. `scripts/shallow_probe.py` — compute and report the random-legal-play baseline **beside every
   policy number it prints**, at every ply it reports, in the same table row.
2. Never print a policy number without its baseline. If a caller wants only one, they can drop the
   column; the script does not offer a mode that hides it.
3. Test: at ply 0 both the model number and the baseline are 1.000, and the test asserts the
   baseline column exists and is populated.

## Completion criteria

```sh
python -m pytest -q
python -m mypy
python scripts/shallow_probe.py --help
```

- No output path prints a policy number without an adjacent baseline — check every branch.
- The ply-0 test documents *why* 1.000 is uninformative, in a comment.

## Handoff

Record the before/after output of the script on one checkpoint.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
