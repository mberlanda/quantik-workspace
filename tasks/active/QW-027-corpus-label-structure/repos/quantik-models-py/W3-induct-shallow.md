# W3 — Back-induct plies 0-2, guarded by a completeness assertion

**Repository:** `quantik-models-py` · **Branch:** `feat/induct-shallow` · one PR
**Depends on:** W2 merged. **Dispatch:** mechanical.

Plies 0-2 are 55 canonical positions no corpus reaches. They can be labelled by back-induction
from v3's ply-3 rows — but **back-induction from an incomplete level is silently wrong**, so the
guard is the point of this item, not an extra.

## Steps

1. `scripts/induct_shallow.py` — back-induct values for plies 0-2 from v3's ply-3 rows.
2. **Before inducting, assert that v3's ply-3 key set equals the complete canonical
   `runs/canonical/level03.npy`.** Not a count comparison — a set comparison. If it fails, abort
   and report which keys are missing. A count can match while the sets differ.
3. Only positions travel to the corpus and labels come only from the exact oracle or exact
   induction over it (`context/system/canonical-invariants.md#I4`). Nothing here derives a label
   from a game outcome.
4. Test with a deliberately incomplete ply-3 set and assert the run aborts with the missing keys
   named.

## Completion criteria

```sh
python -m pytest -q
python -m mypy
python scripts/induct_shallow.py --help
```

- The completeness assertion is a set comparison, and its failure path is tested.
- 55 positions are produced across plies 0-2; state the per-ply breakdown.
- No corpus is written in this item — the output is a standalone artefact W6 merges.

## Handoff

Record the per-ply counts and the completeness-check result.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
