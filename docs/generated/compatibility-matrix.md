# Compatibility Matrix

Reconciled 2026-09-07 against observed tags, published releases, and checked-out declarations.
“Supported” is withheld unless exact cross-stack evidence exists — and today it does not,
because the repository-owned portability adapters cannot be invoked as declared.

| Contracts | Wire IDs | Python | Rust | Models | Action ref | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.1 | 14 registered | 1.3.0 declaring contracts 1.3.0; consumes the v1.3.1 action | 1.3.0 declaring contracts 1.3.0 | 1.1.0, contracts release derived from quantik-core-py at runtime | v1.3.1 | partially-supported | `supported` is withheld: no cross-stack portability smoke has run. Both repository-owned adapters exit 2 because workspace.yaml declares them without their required --contracts-root/--output arguments. |
| 1.3.0 | 14 registered | 1.3.0 (tag v1.3.0) declaring contracts 1.3.0 | 1.3.0 (tag v1.3.0) declaring contracts 1.3.0 | 1.1.0, contracts release derived from quantik-core-py at runtime | v1.3.0 | partially-supported | Declarations agree across the trio and all tags/releases are published; cross-stack smoke not executed. |
| 1.2.0 | 12 registered | 1.2.0 (tag v1.2.0) | 1.2.0 (tag v1.2.0) | no static declaration | v1.2.0 | deprecated | Superseded by 1.3.0/1.3.1. Recorded for history; not a migration target. |
| 1.1.0 | 0 registered | tag exists | tag exists | no tag/release evidence | v1.1.0 | unknown | Retained from the 2026-07-21 assessment. |

Machine-readable matrices must validate against `schemas/compatibility-matrix.schema.json`.
