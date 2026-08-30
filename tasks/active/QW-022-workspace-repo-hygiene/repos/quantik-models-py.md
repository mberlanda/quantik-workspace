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
