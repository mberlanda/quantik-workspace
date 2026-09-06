# QW-001 Status

Prepared, not executed. Discovery evidence and repository tasks exist. Contract decisions and fixture design must precede implementation changes.

## 2026-08-30 reconciliation

Still `plan-required` in substance (manifest says `planned`, but no fixture design or
adapter work exists). Verified in code, not assumed:

- `quantik-core-rust`'s observation exporter (`crates/quantik-core/src/bench/contracts.rs`)
  still writes a synthetic one-hot `policy_visits`, confirming the action-index/value
  questions this initiative exists to settle are still live (see QW-006, which is the
  same defect from the training-target side).
- `quantik-models-py` gained a second, **mover-relative** tensor encoding
  (`fastboard.encode_tensors`) distinct from the color-ordered
  `quantik_core.ml_data.qfen_to_tensor` this initiative's `tensor-board.v1` scope already
  named — see [`WORKSTREAMS.md`](../../../docs/history/workstreams-archive.md) workstream 4. This sharpens open decision 2
  (action/orientation mapping): a runtime built to the wrong encoding is silently wrong on
  half of all positions, which is exactly the class of bug decision 2 is meant to prevent.
  No fixture or contract change has been made in response yet.

Left active. No repository has produced the D4/action-remapping adapters or fixtures this
initiative specifies.

## 2026-09-06 — "isn't this already implemented?"

Asked, and checked rather than answered from the packet. **It is not, and the
confusion is the packet's own problem statement.** Its first clause says state
identity, canonicalization, action remapping, masks and value perspective "are
implemented across engines and models" — true, and it is why this reads as done.
The deliverable is the clause after it: *one executable cross-stack contract*
over that behaviour. That does not exist.

Verified in the repositories, not assumed:

- `quantik-core-contracts/fixtures/` holds `search-summary/`, `selfplay/`,
  `api-portability/` and `parquet/` only. There are **no normative fixtures for
  canonicalization, symmetry, action indices, legal masks or value perspective** —
  acceptance criterion 1.
- `action-index.v1` and `tensor-board.v1` are registered in `contracts.json` with
  `"schema": null` and no file under `schemas/`. They are documentation entries,
  not executable contracts.
- No repository has produced the D4 / action-remapping adapters criterion 3 asks
  for structurally identical reports from.

Also corrected above: the observation exporter is at
`crates/quantik-core/src/bench/contracts.rs`, not `bench/contracts.rs`. The path
had been wrong since the 2026-08-30 reconciliation; the file it names is real and
the surrounding claim is unchanged, but the one-hot `policy_visits` detail was
**not** re-verified in this pass and should not be treated as freshly confirmed.

Still active.

## 2026-09-06 — contracts + core-py + core-rust increment landed, models-py deferred

Implemented, not just decided. All six open decisions in `decisions.md` are
resolved, grounded in what both engine implementations actually did before
this change (verified by reading the code, cross-referenced between
languages, not assumed). PRs:

- [quantik-core-contracts#21](https://github.com/mberlanda/quantik-core-contracts/pull/21) —
  corrects `docs/symmetry-transposition.md` from the 8-element D4 group to
  the real 192-element D4 × shape-permutation group both implementations
  already compute over; adds the `remap_action_index`/`inverse_transform_index`
  contract (`transform_index = d4_index*24 + shape_perm_index`, 0..191);
  adds `docs/game-state.md#invalid-state-validation-boundaries`; adds two
  new normative fixtures, `fixtures/symmetry/symmetry-v1.json` and
  `fixtures/invalid-states/invalid-state-v1.json`, both generated from and
  cross-checked against the real Python implementation rather than
  hand-derived; registers both in `contracts.json`, wires them into
  `scripts/validate_contracts.py` (with a from-scratch, dependency-free
  D4/shape-perm reimplementation) and both CI workflows.
- [quantik-core-py#47](https://github.com/mberlanda/quantik-core-py/pull/47) —
  adds `SymmetryHandler.remap_action_index`/`inverse_transform_index`,
  cross-checked against the existing `apply_symmetry_to_move` and against
  the contracts fixture's golden cases. `auto-lint.sh` and `dev-check.sh`
  both run clean end to end: 835 passed, 1 skipped, black/flake8/mypy/build/
  twine all pass. The first `dev-check.sh` run failed at the pytest step on
  a pre-existing, unrelated issue (`test_api_portability_report_cli_writes_normalized_report`
  failing because the local `.venv`'s editable install was stale at package
  version `1.1.0` against `pyproject.toml`'s `1.2.0`) — fixed by
  reinstalling the editable package (a local environment refresh, no
  git-tracked effect), then the full gate passed.
- [quantik-core-rust#41](https://github.com/mberlanda/quantik-core-rust/pull/41) —
  adds the same `remap_action_index`/`inverse_transform_index` pair (net
  new: Rust had no action-index-level, or even Move-level, transform
  mapping before this). Also fixes two real cross-stack validation gaps
  discovery found: `QuantikBoard::from_bitboard` was missing overlap/
  line-conflict checks, and the portability-report adapter accepted a
  state (`"Aa../..../..../...."`, balanced turn count but an illegal
  same-shape/same-line placement) that Python's report already rejected.
  Both closed via a new shared `validation.rs` module. `cargo fmt`,
  `cargo clippy -D warnings`, and `cargo test --workspace --all-features`
  are clean.

**Deliberately not done in this pass, per explicit user instruction**
("hold on quantik-models changes since something else is happening at the
same time"): the `quantik-models-py` repo task
(`repos/quantik-models-py.md`) — explicit tensor/action/mask/transform/
value-perspective contracts, `[9,4,4]` mover-relative vs. colour-ordered
disambiguation at the consumer, all-legal vs. visited-action mask tests.
Also not done, found but out of scope for QW-001 specifically (see
decisions.md's "Explicitly out of scope" section): the synthetic one-hot
`policy_visits` in Rust's `bench/contracts.rs::observation_v1_row`
(QW-006's problem), and porting the near-terminal blocked-side-loss QFEN
already proven in Rust's hermetic test suite into the actual shared
`fixtures/api-portability/game-state-v1.json`.

**Next**, when models-py work resumes: it can now consume a real, tested
`remap_action_index` contract in both languages instead of inventing its
own D4 action remapping, which is exactly what `repos/quantik-models-py.md`
asks for ("any D4 augmentation/remapping explicit").
