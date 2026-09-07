# W4 — quantik-models-py

Repository: `quantik-models-py`
Branch: `plan/qw-019-quantik-models-py` (one PR)

## Objective

Validate the play service's request/response handling against the schema
W1 registers in `quantik-core-contracts`. `decisions.md#4` is explicit that
this is required: "All three implementations validate, including
`quantik-models-py` ... A contract validated by one of its three
implementations is a contract that describes one implementation." This
work item did not exist before this planning pass — `affected_repositories`
and `work_items` only listed `quantik-core-contracts`, `quantik-api-rust`
and `quantik-qfen-visualizer`, even though `problem` itself names "the
Python play service ... a third independent implementation of the same
wire format" and `decisions.md#4` names it as one of exactly three that
must validate. Added here, not silently left out.

## Implementation and scope

`allowed_paths` in `manifest.yaml`: `src/quantik_models/play/service.py` —
confirmed `REQUEST_SCHEMA = "quantik.engine-request.v1"` at line 33, and
the same string documented in `play/server.py`'s route docstring. Whatever
W1 settles on the `quantik.` prefix question (decisions.md#3, still open)
applies here identically to W2/W3. depends_on: W1.

`decisions`/`invariants` stay empty: the prefix question is the one
decisions.md leaves genuinely open; nothing else needs deciding for this
item specifically.

## Completion criteria and verification

Not yet planned. State observable acceptance checks and exact repository
commands here before dispatch — at minimum, a test that the service's
request/response handling validates against W1's registered schema.

## Handoff

Record item ID, branch, PR, starting/final revisions, dependency evidence,
actual commands/results, and remaining blockers.
