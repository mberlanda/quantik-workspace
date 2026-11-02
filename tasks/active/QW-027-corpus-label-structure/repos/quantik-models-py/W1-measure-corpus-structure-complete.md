# W1 — Measure and document what the corpora actually contain

**Repository:** `quantik-models-py` · **Branch:** `docs/corpus-structure` · one PR
**Dispatch:** execute and record.

Corpora are quoted by row count, and the row count describes the value corpus while badly
misdescribing the policy corpus. Measure it, write it down. **No corpus is modified in this item.**

Known figures to verify rather than trust: policy labels are ~8% of rows (250,000 of v1's
3,087,356; 255,058 of v2's; 271,676 of v3's), flat across all three. Per-ply label counts at plies
7-12 are identical round numbers in every corpus (60k/60k/30k/20k/20k/20k) with zero at ply 13 —
a fixed sampling cap, not coverage.

## Steps

1. Measure, per corpus (v1, v2, v3): total rows, rows carrying a policy label, policy density, and
   the per-ply label table. Recompute; do not copy the numbers above.
2. Document both policy schemas with their real byte costs: v1's dense float32 `(N,64)` plus a
   weight (~282 bytes/row) versus v2/v3's `uint64 optimal_mask` (~30 bytes/row).
3. State the ply floor: no corpus reaches below ply 3, and plies 0-2 are 55 canonical positions
   that no model has seen.
4. Write it all into `docs/corpus-structure.md`, with the measured numbers and the command that
   produced each.

## Completion criteria

- Every number in the document is reproducible from a command in the document.
- The per-ply table makes the sampling cap visible as a cap, not as coverage.
- Both schemas appear with measured byte costs.
- No corpus file is modified: `git status` shows only the new document.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record which published figures your measurements confirmed and which they corrected.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
