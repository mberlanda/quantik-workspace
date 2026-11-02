# W4 — Record which container is the public deployment

**Repository:** `quantik-api-rust` · **Branch:** `docs/deployment-decision` · one PR
**Depends on:** W1 merged. **Dispatch:** judgment — small, but genuinely a decision.

Two containers will exist: this Rust API image, and the Python play container from QW-009. The
criterion asks for a recorded decision on which is the public deployment, or why both ship.

## Steps

1. Read QW-009's `docs/play-service.md` and ADR `0012-storeless-first-public-deployment.md` in the
   workspace before deciding — the storeless-first position is already recorded and this decision
   must sit inside it, not beside it.
2. Record in `README.md` (or `docs/deployment.md` if you prefer a separate home — say which): which
   image is the public deployment, or why both ship and what each is for.
3. State the consequence for the visualizer: which endpoint it points at by default.
4. If both ship, say which one a bug report should be filed against. Two public deployments with no
   stated owner is the outcome this criterion exists to prevent.

## Completion criteria

- The decision is recorded with its reasoning and the ADR 0012 relationship.
- The visualizer's default endpoint is stated.
- If both ship, the bug-report answer is explicit.

## Handoff

Record the decision and the documents you reconciled it against.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
