# QW-001 Status

Prepared, not executed. Discovery evidence and repository tasks exist. Contract decisions and fixture design must precede implementation changes.

## 2026-08-30 reconciliation

Still `plan-required` in substance (manifest says `planned`, but no fixture design or
adapter work exists). Verified in code, not assumed:

- `quantik-core-rust`'s observation exporter (`bench/contracts.rs::observation_v1_row`)
  still writes a synthetic one-hot `policy_visits`, confirming the action-index/value
  questions this initiative exists to settle are still live (see QW-006, which is the
  same defect from the training-target side).
- `quantik-models-py` gained a second, **mover-relative** tensor encoding
  (`fastboard.encode_tensors`) distinct from the color-ordered
  `quantik_core.ml_data.qfen_to_tensor` this initiative's `tensor-board.v1` scope already
  named — see `quantik-ns/WORKSTREAMS.md` workstream 4. This sharpens open decision 2
  (action/orientation mapping): a runtime built to the wrong encoding is silently wrong on
  half of all positions, which is exactly the class of bug decision 2 is meant to prevent.
  No fixture or contract change has been made in response yet.

Left active. No repository has produced the D4/action-remapping adapters or fixtures this
initiative specifies.
