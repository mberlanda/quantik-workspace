# W2 — quantik-core-py

Repository: `quantik-core-py`
Branch: `qw-001/canonical-state-action-contract` (merged)

## Objective

Implement `SymmetryHandler.remap_action_index`/`inverse_transform_index`
against the contract W1 defines, cross-checked against the pre-existing
`apply_symmetry_to_move` and against the contracts fixture's golden cases —
see `decisions.md` D1–D2.

## Implementation and scope

`allowed_paths` in `manifest.yaml`. No public-API semantics changed silently;
this is additive.

## Completion criteria and verification

- `tests/test_symmetry.py` covers the new pair against
  `fixtures/symmetry/symmetry-v1.json`'s golden cases.
- `./auto-lint.sh && ./dev-check.sh` clean end to end (black/flake8/mypy/build/twine).

## Handoff

**Completed.** [quantik-core-py#47](https://github.com/mberlanda/quantik-core-py/pull/47),
merged at `26bbbced`. 835 passed, 1 skipped. See `status.md` (2026-09-06 entry)
for the one pre-existing, unrelated `dev-check.sh` failure hit and fixed along
the way (a stale local `.venv` editable install, no git-tracked effect).
