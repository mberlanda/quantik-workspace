# quantik-models-py adoption — QREL-2026-001

- Previous contracts release: `None`
- Target contracts release: `1.2.0`
- Adoption status: `derived`
- Adopted tag: `—`
- Adopted commit: `—`

quantik-models-py declares no static contracts release: `export/checkpoint.py::_supported_contract_version()` reads `quantik_core.contracts.SUPPORTED_CONTRACTS_RELEASE` at runtime, so it follows quantik-core-py by construction. Nothing to adopt separately.

Recorded retroactively on 2026-09-07 from the observed tag and checked-out declaration,
not from a guarded consumer-adoption run.
