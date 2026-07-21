# Compatibility Model

Compatibility is executable evidence, not similar API names. Adapters identify repository/version, contracts release, wire IDs, operation, input, output, and diagnostics. Reports classify contract violation, implementation bug, serialization difference, ordering difference, numerical tolerance, intentional implementation-specific behavior, missing coverage, or infrastructure failure.

The workspace compares reports but does not normalize away differences or implement Quantik operations. Unsupported adapters become repository tasks. Matrix status remains `unknown` or `migration` until exact evidence exists.
