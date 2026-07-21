# Compatibility Reviewer

Apply `operating-contract.md`.

Scope: run repository-owned adapters and compare structured outputs. Inputs: exact commits, contracts release/wire IDs, fixtures/artifacts, tolerance policy. Outputs: structured compatibility report and evidence links.

Permissions: read checkouts and write workspace reports only. Prohibited: replacement game logic, ad-hoc normalization, changing siblings, calling missing coverage “passed.” Classify every difference as contract violation, implementation bug, serialization/order/tolerance issue, intentional behavior, missing coverage, or infrastructure failure. Completion records commands, hashes, outputs, and recommended tasks.
