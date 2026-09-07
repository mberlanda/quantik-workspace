# W1 — quantik-core-contracts

Repository: `quantik-core-contracts`
Branch: `qw-001/canonical-state-action-contract` (merged)

## Objective

Own the normative fixture/schema interpretation for canonical state and
action encoding: correct `docs/symmetry-transposition.md` from the
documented 8-element D4 group to the real 192-element D4 × shape-permutation
group both engines already compute over, contract the
`remap_action_index`/`inverse_transform_index` pair, and add the
invalid-state-validation-boundaries section — see `decisions.md` D1–D6.

## Implementation and scope

`allowed_paths` in `manifest.yaml`. Two new normative fixtures
(`fixtures/symmetry/symmetry-v1.json`, `fixtures/invalid-states/invalid-state-v1.json`)
generated from and cross-checked against the real Python implementation, both
registered in `contracts.json` and wired into `scripts/validate_contracts.py`
(a from-scratch, dependency-free D4/shape-perm reimplementation) and both CI
workflows.

## Completion criteria and verification

- `scripts/validate_contracts.py` passes with both new fixtures registered.
- `tests/test_contracts_validator.py` covers the new fixtures.
- No future-tag reference in candidate jobs.

## Handoff

**Completed.** [quantik-core-contracts#21](https://github.com/mberlanda/quantik-core-contracts/pull/21),
merged at `1934c73d`. See `decisions.md` and `status.md` (2026-09-06 entry) for
the full account.
