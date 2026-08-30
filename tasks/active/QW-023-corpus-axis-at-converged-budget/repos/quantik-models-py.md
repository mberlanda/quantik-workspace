# quantik-models-py

## Objective

One converged training run on `exact-sampled-v2.npz` and one arena against
`patience-cpool`.

## Inputs

- `runs/train/patience-cpool/config.json` — the arm to match, one field changed.
- `runs/oracle/corpus/exact-sampled-v2.npz` — the corpus.
- `scripts/run_patience_lineup.sh`, `scripts/evaluate_lineup.sh`.
- `python -m quantik_models.eval.shift` — the shared probe, reported alongside.

## Approach

1. Smoke: `--epochs 4 --patience 2`, confirm `stopped_early` records in both
   directions. Idle-time one epoch and project.
2. Train at `--epochs 120 --patience 5`.
3. **Check it early-stopped.** If it hit 120, raise the cap and rerun; do not
   report it.
4. One arena, both arms, plies 3/6/9, side-balanced, fresh seed.
5. Shared probe over both `best/` directories.

## Completion criteria

- The run's `metrics.jsonl` shows fewer epochs than its cap.
- Arena and probe reported together, with the seat controlled and the single
  training seed named as a limitation.
- ADR 0014 updated with the outcome, including if it is null.
- Handoff records the run directory, epochs, arena seed and both artefacts.
