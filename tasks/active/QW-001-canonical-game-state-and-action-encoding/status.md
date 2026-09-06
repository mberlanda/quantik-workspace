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
