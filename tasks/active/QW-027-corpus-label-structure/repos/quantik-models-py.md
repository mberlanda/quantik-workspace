# quantik-models-py

## Objective

Document what the corpora contain, make v1 mergeable, and label plies 0-2.

## Work items

1. **`docs/corpus-structure.md`** — policy density per corpus, the per-ply label
   table, the two schemas with their byte costs, and the ply floor. Linked from
   `docs/dev-data.md` and `docs/corpus-v3.md`.

2. **`data/policy_schema.py`** — `dense_to_mask` and `mask_to_dense`, with a
   round-trip test on a real v1 slice asserting bit-exactness both ways. The
   guard that makes it safe: refuse to convert a row whose `policy_target` is not
   uniform over its support, rather than silently discarding a weighting.

3. **`scripts/induct_shallow.py`** — read v3, assert its ply-3 key set equals
   `level03.npy`, induct down to ply 0, and write an `ExactCorpus` of 55 rows.
   The assert is the whole safety argument: back-induction from an *incomplete*
   level is silently wrong, and `induct()` already raises on a missing live
   child, so both halves are covered.

4. **`scripts/shallow_probe.py`** — score any checkpoint against the exact
   plies 0-2 targets, printing mass-on-optimal, argmax-optimal, normalised
   entropy and value sign **beside the random-legal-play baseline**.

5. **Merge** the 55 rows through `data/merge_corpus.py` to a new
   `exact-sampled-v4.npz`, hash recorded.

## Completion criteria

- `docs/corpus-structure.md` states all four properties with the measured numbers.
- The converter round-trips a real v1 slice bit-exactly and refuses a non-uniform row.
- `induct_shallow.py` reproduces 55 positions whose values match a direct oracle solve.
- `shallow_probe.py` prints the baseline on every row it reports.
- Focused tests pass; handoff records the commit and the new corpus hash.
