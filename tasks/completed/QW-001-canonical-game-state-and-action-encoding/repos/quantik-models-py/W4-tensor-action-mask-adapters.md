# W4 — quantik-models-py

Repository: `quantik-models-py`
Branch: `qw-001/canonical-state-action-contract` (merged)

## Objective

Consume explicit tensor, action, legal-mask, transform, and value-perspective
contracts through documented adapters: make `[9,4,4]`, 64 shape-major
actions, all-legal versus visited-action masks, side-to-move values, and any
D4 augmentation/remapping explicit — against the real, tested
`remap_action_index`/`inverse_transform_index` contract W1–W3 shipped,
rather than inventing its own D4 action remapping.

## Implementation and scope

Was deliberately deferred, then landed the same day, after W1–W3, once
concurrent models-py work had settled. Most of what this item asked for
already existed and was correct — `[9,4,4]` mover-relative vs. colour-ordered
tensor layouts (`fastboard.encode_tensors`/`to_core_tensor`), 64 shape-major
actions throughout, and `legal_masks` already returning the full legal-action
enumeration. The one real, findable bug: `fastboard`'s internal `spatial`
D4 index enumerated the 8 transforms in numpy `rot90`/`fliplr` composition
order, not `quantik_core.symmetry.D4Index`'s order (rot90/rot270 and
reflH/reflD swapped) — invisible until this item's external contract gave
something to check against, since every prior self-check only compared the
module against itself.

`allowed_paths` in `manifest.yaml`.

## Completion criteria and verification

- `test_spatial_perms_match_core_d4_mappings`,
  `test_shape_perms_match_core_all_shape_perms`: lock both index spaces to
  `quantik_core`'s.
- `test_transform_actions_matches_core_remap_action_index`: all 192
  transforms × 64 actions, batched `fastboard.transform_actions` against
  scalar `SymmetryHandler.remap_action_index`.
- `test_transform_round_trips_through_core_inverse`: transform then
  `SymmetryHandler.inverse_transform_index` recovers the original boards
  and actions.
- `test_masked_log_softmax_all_false_row_is_uniform_not_nan`: the all-false
  mask case.
- `.venv/bin/python -m pytest -q` and `mypy` clean.

## Handoff

**Completed.** [quantik-models-py#63](https://github.com/mberlanda/quantik-models-py/pull/63),
merged `cb29681`, 2026-09-06. Verified locally both against the sibling
`../quantik-core-py` checkout (22 fastboard tests, all real) and against the
then-published `quantik-core` 1.2.0 wheel (the two contract-dependent tests
skip cleanly, reason string excludes "could not import" per
`quantik-models-py/DEVELOPMENT.md`'s CI guard). `quantik-core` 1.3.0 —
which adds `remap_action_index`/`inverse_transform_index` — published to
PyPI the same day; `quantik-models-py`'s own `pyproject.toml` floor was
bumped to `>=1.3,<2` in [#68](https://github.com/mberlanda/quantik-models-py/pull/68)
(Release 1.1.0), so the two tests no longer skip on a clean install either.
