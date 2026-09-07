# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `plan/qw-015-quantik-core-contracts` (one PR)

## Objective

# quantik-core-contracts

## Objective

Split the fused check. `scripts/validate_opening_book_summary.py` must compare game
facts only, and `actions/opening-book-consistency/action.yml` must stop defaulting
`expected-release`.

## Inputs

- `scripts/validate_opening_book_summary.py` — `normalize_summary` (the returned dict,
  line 118) and `main` (the equality, line 142).
- `actions/opening-book-consistency/action.yml` — line 23.

## Approach

Keep `contract_version` parsed and validated as a string, keep the
`--expected-release` comparison, and omit the key from the dict the two
implementations are compared on. Nothing else about the function changes.

## Completion criteria

- A test builds two summaries identical except for `contract_version` and asserts:
  the equality passes; `--expected-release` on the older one fails. Both directions,
  because a check that never fails is not a check.
- `grep -rn 'default: "1\.' actions/` returns nothing for a release literal.
- Handoff records the commit and the two workflow files downstream must update.

## Implementation and scope

Not yet planned. Replace this item's placeholder `allowed_paths` in `manifest.yaml` with explicit repository-relative paths, select the `decisions`/`invariants` references it actually needs, and split into further work items wherever another branch/PR is needed.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
