# W4 — Merge through the normal corpus path

**Repository:** `quantik-models-py` · **Branch:** `feat/merge-opening-corpus` · one PR
**Depends on:** W3 merged. **Dispatch:** mechanical.

The labelled positions become a corpus the same way every other corpus does — through
`src/quantik_models/data/merge_corpus.py`. No bespoke path.

## Steps

1. Merge W3's labelled output into a **new** corpus file with a **new hash**. Never rewrite an
   existing corpus in place: an in-place rewrite makes every earlier result unreproducible.
2. Record the new file's name, hash, row count, and per-ply row counts.
3. Verify the merged corpus contains rows at plies 0-2 and that the per-ply distribution matches
   the partition's intent — coverage extended, not shallow density re-added.
4. Update `docs/labeling-strategy.md` with the new corpus and how it was produced.

## Completion criteria

```sh
python -m pytest -q
python -m mypy
```

- A new corpus file exists with a new hash; the previous corpora are untouched (list them and say so).
- Per-ply row counts are recorded and include non-zero counts at plies 0, 1 and 2.
- `docs/labeling-strategy.md` names the new corpus.

## Handoff

Record the hash, row counts per ply, and the untouched-corpora check.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
