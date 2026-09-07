# W1 — Train the converged arm

**Repository:** `quantik-models-py` · **Branch:** `feat/corpus-axis-converged-run` · one PR
**Dispatch:** execute and record.

Every corpus comparison on disk compares a converged run against a capped one, or two capped runs.
`patience-cpool` (v1) early-stopped at 43 and is converged; `patience-cpool-v2` and `-v3` both ran
all 40 epochs and hit their cap, so neither is. ADR 0014's central finding rests on that mismatch.
This item produces the missing arm: the same architecture on the other corpus, with a cap high
enough that early stopping is the expected outcome.

**The hyperparameters are given. Do not tune them.**

- corpus `exact-sampled-v2.npz`
- architecture `cpool`, preset `medium`
- `--epochs 120 --patience 5`
- lr `6e-4`
- seed `20260828`

120 is deliberately far above the expected stopping point. It is a ceiling, not a target.

## Steps

1. Confirm `exact-sampled-v2.npz` is on disk and record its hash, so the run is traceable to an
   exact corpus.
2. Launch the run with exactly the parameters above, into a new output directory.
3. **Confirm it early-stopped.** Record the epoch it stopped at and the patience counter. A run
   that reaches 120 is not converged, and this initiative's conclusion cannot be drawn from it —
   if that happens, report it and stop. Do not raise the cap and rerun without coordinator review.
4. Record the shared probe numbers for the new checkpoint alongside the run metadata.

## Completion criteria

- `docs/corpus-axis-converged.md` exists and records: the corpus hash, the exact command, the stop
  epoch, the patience counter, and the probe numbers.
- The document states plainly whether the run converged.
- The checkpoint directory is named so W2 can find it.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the stop epoch, wall-clock time, and the checkpoint path.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
