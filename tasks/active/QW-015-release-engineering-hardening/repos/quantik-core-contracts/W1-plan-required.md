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

**Criteria 1, 2 and 5 are already shipped** — `quantik-core-contracts`
release v1.3.1 ([#23](https://github.com/mberlanda/quantik-core-contracts/pull/23),
tag `a6c1b10`), "fix the opening-book-consistency release deadlock":
`normalize_summary` deliberately keeps `contract_version` out of the
structural-equality dict (docstring explains exactly the fusion bug
`problem` describes), and `action.yml`'s `expected-release` default is
`""`, not a hardcoded release.

**Criteria 3 and 4 have real, verified gaps, not yet planned:**
- `.github/workflows/validate-contracts.yml:23` still hardcodes
  `--expected-release 1.3.1` — exactly the "hardcoded release string
  outside VERSION" criterion 4 asks a grep to find nothing of. It should
  derive from `VERSION` (e.g. `--expected-release "$(cat VERSION)"`), not
  be bumped by hand each release.
- `release-contracts.yml` already asserts `VERSION` matches the tag
  (`test "$(cat VERSION)" = "$version"`) but does not assert the tag
  doesn't already exist, nor that downstream action paths resolve at that
  ref — criterion 3 only partially met.

`allowed_paths` covers both the already-shipped files (for reference) and
the two workflows with the remaining gap. `decisions`/`invariants` stay
empty — decisions.md's four points are already resolved (unheaded prose,
same as QW-009) and don't need re-deciding for this narrower remaining
scope.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository commands here before dispatch.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence, actual commands/results, and remaining blockers.
