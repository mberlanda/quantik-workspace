# W4 — quantik-models-py

Repository: `quantik-models-py`
Branch: `qw-001/canonical-state-action-contract` (not started — same branch
name W1–W3 used, since this initiative dispatches one branch per repository
under a shared name; nothing has been pushed to it in `quantik-models-py`)

## Objective

Consume explicit tensor, action, legal-mask, transform, and value-perspective
contracts through documented adapters: make `[9,4,4]`, 64 shape-major
actions, all-legal versus visited-action masks, side-to-move values, and any
D4 augmentation/remapping explicit — now against a real, tested
`remap_action_index` contract in both languages (W1–W3), rather than
inventing its own D4 action remapping.

## Implementation and scope

**Pending, not a design gap — deliberately deferred.** Per explicit user
instruction during the W1–W3 pass ("hold on quantik-models changes since
something else is happening at the same time"), this item was excluded from
that increment; see `status.md`'s "contracts + core-py + core-rust increment
landed, models-py deferred" entry. `allowed_paths` names the real files this
will touch (`fastboard.encode_tensors` is the mover-relative encoder; `I1`
in canonical-invariants documents why the colour-ordered
`quantik_core.ml_data.qfen_to_tensor` must not be confused with it) but is
provisional — start only once the concurrent models-py work status.md
references has settled.

## Completion criteria and verification

Not yet planned pending the sequencing decision above. At minimum: a test
asserting all-false-mask rejection/handling, and a transform round-trip test
against W1's fixture.

## Handoff

Not started. Record item ID, branch, PR, starting/final revisions, dependency
evidence, actual commands/results, and remaining blockers once unblocked.
