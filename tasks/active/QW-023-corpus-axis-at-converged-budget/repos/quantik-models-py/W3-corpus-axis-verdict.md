# W3 — State the verdict on the corpus axis

**Repository:** `quantik-models-py` · **Branch:** `docs/corpus-axis-verdict` · one PR
**Depends on:** W2 merged. **Dispatch:** judgment — capable model, human review.

Both arms are now converged and one variable moved. This item says what that shows.

## Steps

1. Write the verdict into `docs/corpus-axis-converged.md`, in its first sentence: does shallow-ply
   coverage help, at converged budget, with one variable moved?
2. State it as **confirmed, weakened, or overturned** relative to ADR 0014's finding that shallow
   coverage is corpus-caused and epochs cannot buy it. **A null result is a real outcome** and must
   be recorded as one — this experiment exists precisely because the earlier evidence was the
   weakest form of the right answer.
3. Every claim must rest on a side-balanced number from W2, with the probe reported alongside.
4. If the arena and the probe disagree, say so explicitly and prefer the arena — held-out accuracy
   has failed to predict play strength four times in this project.

## Coordinator follow-up (not this item)

ADR 0014 lives at `quantik-workspace/docs/adr/0014-corpus-coverage-and-epoch-budget-are-separate-axes.md`,
in a repository that is not a dispatch target here. Updating it is a workspace change. State in
the handoff exactly what the ADR should now say, in a form that can be pasted in.

## Completion criteria

- The verdict is one of confirmed / weakened / overturned, in the first sentence.
- Every supporting number traces to W2's tables.
- The handoff contains ready-to-paste ADR 0014 text.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the verdict and the proposed ADR 0014 update.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
