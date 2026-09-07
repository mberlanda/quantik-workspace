# W2 — Propagate the confirmed result into the docs that carry the caveat

**Repository:** `quantik-models-py` · **Branch:** `docs/patience-seed-caveat` · one PR
**Depends on:** W1 merged. **Dispatch:** mechanical.

Three documents currently carry a seed caveat that W1 either resolves or converts into a
correction. They must all move together, or the repository states two different things about the
same comparison.

## Steps

1. Read `docs/patience-arena-second-seed.md` (W1's output) and take its verdict as given. Do not
   re-derive it and do not re-run anything.
2. Update each of these to report the confirmed — or corrected — result, and remove the
   now-answered caveat:
   - `docs/decisions/0001-architecture-lineup.md`
   - `docs/shift-evaluation.md`
   - `docs/autoplay.md`
3. Each must link to `docs/patience-arena-second-seed.md` as the evidence, rather than restating
   its tables. One number, one home.
4. If W1's verdict was "reverses" or "inside noise", the architecture decision in
   `docs/decisions/0001-architecture-lineup.md` may no longer be supported by its stated evidence.
   **Do not silently rewrite the decision.** Record the discrepancy at the top of that file and
   flag it in the handoff for coordinator review.

## Completion criteria

- `grep -rn "20260829" docs/` returns only historical references that are explicitly labelled as
  the first run, never a live claim resting on it.
- All three documents point at the same evidence file.
- `python -m pytest -q` and `python -m mypy` clean.

## Coordinator follow-up (not this item)

QW-012 is already in `tasks/completed/`. Its `status.md` still describes a pending seed decision;
closing that text out is workspace bookkeeping, not a `quantik-models-py` change, and is not part
of this PR.

## Handoff

Record the three diffs and whether step 4's discrepancy path was triggered.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions
win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
