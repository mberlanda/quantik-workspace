# Repository Boundaries

- `quantik-core-py`: Python domain behavior, public Python API, tests/benchmarks, serialization adapters, and contract declaration.
- `quantik-core-rust`: optimized behavior and representations, Rust API/tests/benchmarks, adapters, and contract declaration. Optimization cannot redefine semantics silently.
- `quantik-core-contracts`: interoperability authority for schemas, fixtures, validators, wire IDs, compatibility/version policy, actions/workflows, and migrations. It is not automatic semantic authority for uncontracted ambiguity.
- `quantik-models-py`: model/tensor/action/value interpretation, data readers, training/inference/evaluation/checkpoints, and contract declaration. It cannot depend on undocumented engine internals.
- `quantik-workspace`: orchestration metadata, reports, task/release state, context, locks, and drift checks. It owns no engine/model implementation.
