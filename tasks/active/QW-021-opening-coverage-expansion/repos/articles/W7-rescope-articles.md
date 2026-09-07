# W7 — Handle the articles that quote the old figure

**Repository:** `articles` · **Branch:** `docs/rescope-generalization-claim` · one PR
**Depends on:** W5 merged. **Dispatch:** mechanical.

Acceptance criterion 6 requires the articles quoting the 99.63% generalization figure to be listed
and handled — not just the code repository's docs.

## Steps

1. `grep -rn "99.6\|99\.63" .` across the articles repository, and list every occurrence with
   its file and whether that piece is published or still a draft.
2. For a **draft**: update the number to W5's, or scope it to the pre-expansion partition.
3. For a **published** piece: do not silently rewrite history. Add a dated note scoping the figure
   to the partition it was measured against, and flag the piece in the handoff so the author can
   decide whether a correction is warranted.
4. Follow this repository's conventions: no Markdown tables (Substack does not render them), and
   the `THE FULL-STACK MIND` wordmark on every figure.

## Completion criteria

- Every occurrence is listed with published/draft status and its disposition.
- No published piece is edited beyond an additive, dated scoping note.
- Repository conventions respected.

## Handoff

Record the full list and which pieces need an author decision.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
