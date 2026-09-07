# Handoff

- Initiative / repository: QW-001 / `quantik-core-py`
- Branch and full commit: `qw-001/canonical-state-action-contract` @ `1ace563f174afde73338077f88e946f1ba0357d3`
- Dirty-state before/after: clean before (fresh branch off `origin/main`, at Release 1.2.0); clean after (all changes committed). Note: the local `.venv`'s editable-install metadata was stale at package version `1.1.0` against `pyproject.toml`'s `1.2.0` — a pre-existing environment issue, unrelated to any git state — fixed by reinstalling (`pip install -e ".[dev,cbor,arrow]"`); no git-tracked files changed by that.
- PR: https://github.com/mberlanda/quantik-core-py/pull/47
- Files changed:
  - `src/quantik_core/symmetry.py` — new `SymmetryHandler.remap_action_index`/`inverse_transform_index` classmethods
  - `tests/test_symmetry.py` — new `TestActionIndexRemap` class (7 tests)
- Decisions and assumptions: see `../decisions.md`, decision 2. `remap_action_index` reuses the existing `D4_MAPPINGS`/`ALL_SHAPE_PERMS` tables and `_ensure_initialized()` lazy-init path rather than adding new tables.
- Commands and exact results:
  - `./auto-lint.sh` — reformatted `tests/test_symmetry.py` (autopep8 + black), no other changes
  - `./dev-check.sh` — first run failed at the pytest step on the pre-existing stale-`.venv` issue above (`test_api_portability_report_cli_writes_normalized_report`, unrelated to this change); after `pip install -e ".[dev,cbor,arrow]"`, a full re-run passed end to end: `835 passed, 1 skipped` (coverage 93.72%, threshold 90%), black clean, flake8 clean (both the critical-errors-only and full passes), mypy clean, `python -m build` succeeded, `twine check dist/*` PASSED on both the wheel and sdist
- Generated evidence: `tests/test_symmetry.py::TestActionIndexRemap::test_golden_cases_from_contracts_fixture` — 10 hardcoded cases copied from `quantik-core-contracts`' `fixtures/symmetry/symmetry-v1.json` `action_remap_cases`, which were themselves generated from this exact implementation (see the contracts repo's handoff) — so this is a locked cross-check, not an independent re-derivation.
- Known gaps / follow-up: none specific to this repo. `quantik-models-py`'s own D4/action-remapping work (its repo task, `repos/quantik-models-py.md`) can now consume this implementation instead of inventing its own — that work is explicitly deferred, per the user's instruction, to a separate pass.
- Prohibited or unperformed remote actions: none. PR opened, not merged — merge is the user's call.
