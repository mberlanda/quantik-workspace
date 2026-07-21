# QW-007: Checkpoint Consumer Compatibility

Define and implement the consumer boundary for `model-checkpoint.v1`. This task
does not choose a runtime by assumption: it first evaluates the smallest viable
format/runtime set, portability, package cost, determinism, and deployment
constraints, then specifies fail-fast behavior and reference inference evidence.

Model-guided search and the feedback loop depend on this surface but are not
implemented here.
