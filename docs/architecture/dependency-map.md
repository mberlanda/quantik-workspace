# Dependency Map

Dependencies are typed independently: build, runtime, contract, fixture, schema, generated-data, semantic-compatibility, GitHub Action, and release-order. Consumer-to-provider edges live in `workspace.yaml`; generated machine/Markdown views are under `docs/generated/`.

Contracts releases precede implementation adoption. Python and Rust semantic work may proceed independently once candidate contracts are fixed. Models follows stable data/action/tensor interpretations while retaining its independent package version.
