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

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
