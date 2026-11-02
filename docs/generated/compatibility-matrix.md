# Compatibility Matrix

Reconciled 2026-09-07 against observed tags, published releases, and checked-out declarations;
portability evidence added 2026-11-02. “Supported” is withheld unless exact cross-stack evidence
exists. The portability smoke now passes for Python and Rust, but on post-tag checkouts and over
3 cases, so it is not yet tag-exact evidence.

| Contracts | Wire IDs | Python | Rust | Models | Action ref | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1.4.0 | 18 registered | 1.4.0 (tag v1.4.0, publish pending) declaring contracts 1.4.0 | 1.4.0 (tag v1.4.0, publish pending) declaring contracts 1.4.0 | 1.1.0, contracts release derived from quantik-core-py at runtime | v1.4.0 | partially-supported | Tagged 2026-11-02 on contracts, core-py and core-rust; PyPI and crates.io publish pending (still 1.3.0). Portability smoke passed 2026-11-02 on post-tag checkouts, but tag-exact evidence is not yet recorded, so `supported` stays withheld. |
| 1.3.0 | 14 registered | 1.3.0 (tag v1.3.0) declaring contracts 1.3.0 | 1.3.0 (tag v1.3.0) declaring contracts 1.3.0 | 1.1.0, contracts release derived from quantik-core-py at runtime | v1.3.0 | partially-supported | Declarations agree across the trio and all tags/releases are published. Portability smoke passed 2026-11-02 on post-tag checkouts, not the v1.3.0 tags. |
| 1.2.0 | 12 registered | 1.2.0 (tag v1.2.0) | 1.2.0 (tag v1.2.0) | no static declaration | v1.2.0 | deprecated | Superseded by 1.3.0. Recorded for history; not a migration target. |
| 1.1.0 | 0 registered | tag exists | tag exists | no tag/release evidence | v1.1.0 | unknown | Retained from the 2026-07-21 assessment. |

Machine-readable matrices must validate against `schemas/compatibility-matrix.schema.json`.
