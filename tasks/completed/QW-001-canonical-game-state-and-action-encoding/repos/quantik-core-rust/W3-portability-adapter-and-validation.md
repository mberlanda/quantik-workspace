# W3 — quantik-core-rust

Repository: `quantik-core-rust`
Branch: `qw-001/canonical-state-action-contract` (merged)

## Objective

Extend the repository-owned portability adapter for the same cases and
deterministic report shape as W1/W2: add the same
`remap_action_index`/`inverse_transform_index` pair (net new — Rust had no
action-index-level, or even `Move`-level, transform mapping before this),
and close the two real cross-stack validation gaps discovery found — see
`decisions.md` D2–D4.

## Implementation and scope

`allowed_paths` in `manifest.yaml`. `QuantikBoard::from_bitboard` was missing
overlap/line-conflict checks, and the portability-report adapter accepted a
state (`"Aa../..../..../...."` — balanced turn count, illegal same-shape/
same-line placement) that Python's report already rejected. Both closed via a
new shared `validation.rs` module (`InvalidStateReason`, matching Python's
`ValidationResult` names), used by the constructor, the portability report,
and `bench/contracts.rs`.

## Completion criteria and verification

- `cargo fmt`, `cargo clippy -D warnings`, `cargo test --workspace --all-features` clean.
- Does not rely on an unpublished contracts tag.

## Handoff

**Completed.** [quantik-core-rust#41](https://github.com/mberlanda/quantik-core-rust/pull/41),
merged at `56927700`. See `decisions.md` D4 for the two gap details.
