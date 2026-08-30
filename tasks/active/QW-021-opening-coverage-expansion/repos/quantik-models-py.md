# quantik-models-py

## Objective

Label plies 0-6 with the exact oracle, merge them into a corpus, retrain, and evaluate
in the arena — after replacing the held-out partition that this destroys.

## Inputs

- `runs/canonical/level01.npy` .. `level08.npy`, `counts.json` — the enumerations,
  already on disk.
- `runs/coverage.md` — where the 1,019,275 and 3,087,356 figures come from. Re-derive
  from `counts.json` before quoting them again.
- `data/merge_corpus.py` — the one path a corpus reaches training by.
- `docs/labeling-strategy.md` — labels come from the oracle, never from outcomes.
- `scripts/evaluate_lineup.sh` — the arena.

## Approach

1. Write the new partition design. No compute.
2. Smoke-solve a slice of one level. Record per-level throughput; do not extrapolate
   from a differently-shaped level.
3. Solve plies 0-6. Merge through `merge_corpus.py`.
4. Retrain under the protocol QW-012 settles, so the comparison is corpus-only.
5. Arena, controlling for seat, against the current lineup.
6. Update or scope every published quotation of the old generalization figure.

## Completion criteria

- The partition document exists and predates the first solve commit.
- The corpus is produced by `merge_corpus.py`, not a bespoke script.
- The write-up reports arena results with seat controlled, and states held-out accuracy
  separately and secondarily.
- Handoff lists every document and article that quoted 99.63% and what was done to each.
