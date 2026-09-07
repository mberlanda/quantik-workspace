# W6 — Fold the 55 rows in through the normal path

**Repository:** `quantik-models-py` · **Branch:** `feat/merge-shallow-rows` · one PR
**Depends on:** W4 **and** W5 merged. **Dispatch:** mechanical.

## Steps

1. Merge W3's induced and W4's confirmed rows through
   `src/quantik_models/data/merge_corpus.py` into a **NEW** file with a **new hash**. Never an
   in-place rewrite: it makes every earlier result unreproducible.
2. Record the new file's name, hash, and per-ply row counts in `docs/corpus-structure.md`.
3. Update `docs/dev-data.md` and `docs/corpus-v3.md` to point at the new corpus where they
   describe the current one.
4. **Make no strength claim from 55 rows.** State explicitly in the document that whether shallow
   labels change play is settled by QW-024's arena, not here. 55 rows cannot support a claim about
   play strength and the document must say so rather than leaving the reader to infer it.

## Completion criteria

- A new corpus file with a new hash; previous corpora byte-identical (list them and say so).
- Per-ply counts recorded, non-zero at plies 0, 1 and 2.
- The no-strength-claim sentence is present.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the hash, the counts, and the untouched-corpora check.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
