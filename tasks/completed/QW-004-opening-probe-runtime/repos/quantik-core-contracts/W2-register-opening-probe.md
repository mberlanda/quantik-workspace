# W2 — Register `opening-probe.v1` with fixtures

**Repository:** `quantik-core-contracts` · **Branch:** `feat/register-opening-probe` · one PR
**Depends on:** W1 merged and reviewed. **Dispatch:** mechanical.

Implement exactly what `docs/opening-probe-v1.md` specifies. If you have to choose, that is a gap
in W1 — send it back rather than deciding here.

## Steps

1. `schemas/opening-probe-v1.json` — JSON Schema 2020-12, matching the style of
   `schemas/observation-v1.json`. `additionalProperties: false` at the top level.
2. `fixtures/opening-probe/*.jsonl` — normative fixtures covering, one row each at minimum:
   a hit, a miss, a corrupt entry, an incompatible version, and a **transformed move** (a position
   whose representative differs from the position itself, exercising W1 section 3's example).
   These are the contract's teeth; a fixture set without the transformed-move case does not test
   the thing most likely to be wrong.
3. `contracts.json` — register `opening-probe.v1` with `schema`, `docs`, and `fixture_glob`,
   keyed `opening_probe` to match the existing underscore style.
4. If W1 section 6 requires changes to `docs/opening-book-v1.md`,
   `docs/opening-book-summary-v1.md` or `schemas/opening-book-v1.json`, make exactly those.

## Completion criteria

```sh
python -m pytest -q                       # contracts' own suite
quantik-workspace validate contracts      # from the workspace checkout
quantik-workspace validate fixtures
```

- `validate contracts` lists `opening-probe.v1` with a non-null schema.
- `validate fixtures` checked-count increases — a glob matching nothing passes vacuously, so
  confirm the number moved.
- Every fixture row validates against the schema.

## Handoff

Record fixture counts before and after, and the five covered cases.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
