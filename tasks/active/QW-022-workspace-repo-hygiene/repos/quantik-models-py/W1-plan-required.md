# W1 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-022-quantik-models-py` (one PR)

## Objective

# quantik-models-py

## Objective

Make `e2e-data-pipeline.yml`'s dependency on `quantik-core-py` explicit.

## Inputs

- `.github/workflows/e2e-data-pipeline.yml:78-79` — the unpinned checkout.
- `.github/workflows/tests.yml` — installs the published `quantik-core>=1.2` from PyPI,
  deliberately, and is the contrast to preserve rather than copy.

## Approach

Pin a `ref:` on the checkout. Add a comment saying what the workflow is asserting —
"these two heads integrate" — so the next reader does not merge the two workflows'
purposes.

## Completion criteria

- The checkout carries a `ref:`.
- A comment names what the job asserts and why it differs from `tests.yml`.
- The workflow passes at the pinned ref.
- Handoff records the ref pinned and how it is expected to be bumped.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `e2e-data-pipeline.yml` (the unpinned checkout, confirmed still present, no `ref:` set), plus `scripts/solve_opening.py` and `scripts/build_probe.py` — confirmed `.oracle-worktree/` (still present at the workspace root) is referenced by both, so criterion 3's "documented" branch applies, not "removed": the directory is real, load-bearing oracle tooling, just undocumented. decisions/invariants stay empty: decisions.md's four points are already resolved as unheaded prose.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
