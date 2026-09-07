# W1 — Design the train/test partition, before anything is labelled

**Repository:** `quantik-models-py` · **Branch:** `docs/opening-coverage-partition` · one PR
**Dispatch:** judgment. **This is a hard gate: no labelling run starts until this is merged and
reviewed by a human.**

Plies 4-6 **are** the current held-out probe. Training on them destroys the probe and the 99.63%
generalization figure with it — a figure already quoted in published articles. Getting this wrong
is not recoverable by retraining, because the evidence that would detect the mistake is the thing
being consumed.

This item writes `docs/opening-coverage-partition.md` and changes nothing else.

## Decide and record

1. **The new partition.** Which plies and which positions are training, which are held out, and
   how the split is computed so it is reproducible from the enumerations on disk
   (`runs/canonical/level01.npy` … `level08.npy`).
2. **What happens to the old probe.** The current 99.63% figure is measured against a probe that
   this expansion consumes. State whether the old probe is retired, retained as a
   historical-only number, or reconstructed. Every option is acceptable; leaving it ambiguous is not.
3. **Coverage, not density.** ADR 0014's second finding is the warning: the v2→v3 step added
   323,568 more positions of the *same* shallow distribution and bought a measured zero. State
   explicitly that expansion targets plies **0-2**, which no corpus reaches at all, and how the
   design prevents re-densifying plies already covered.
4. **The comparison that will judge the result.** Name the arena and the lineup up front, because
   held-out accuracy has failed to predict play strength four times in this project. Deciding the
   success criterion after seeing the numbers is how the fifth failure happens.
5. **The opening book stays preferred.** Record that the exact opening book remains the answer for
   opening play regardless of how strong the network becomes there, and that the deployment
   reflects that.

## Completion criteria

- `docs/opening-coverage-partition.md` contains all five sections, each with a decision.
- The partition is reproducible: a reader can compute it from the `level0N.npy` files and the
  document alone.
- `git diff --stat` touches only that document.
- The PR is explicitly marked as requiring human review before W2 is dispatched.

## Handoff

Record the partition summary and the retired/retained decision for the old probe.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
