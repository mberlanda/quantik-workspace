# Repository Map

- Contracts owns interoperability schemas, fixtures, validators, actions, and policies.
- Python owns readable/reference behavior and Python adapters.
- Rust owns optimized behavior, storage/search/exporters, and Rust adapters.
- Models owns tensor/action/value consumption, training/inference, and checkpoints.
- Workspace owns intent, typed dependency/release state, evidence, context, and drift reports.

Default local paths are siblings declared in `workspace.yaml`; overrides belong in ignored `workspace.local.yaml`.
