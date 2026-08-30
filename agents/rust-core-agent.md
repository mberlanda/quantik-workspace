# Rust Core Agent

Apply `operating-contract.md`.

## Scope

`quantik-core-rust` only: constants/bitboard/moves/game/board/state/QFEN/symmetry,
minimax/MCTS/beam search, opening-book generation, the exact oracle, CLI binaries,
`bench::contracts`, portability report. Published to crates.io as `quantik-core`.

## Inputs

Rust packet, initiative task, approved contracts candidate, and the invariants a change
must preserve — bitboard plane order, canonical-key derivation, the action-index
formula.

## Outputs

Rust implementation/tests, adapter artifacts, and a handoff that reports
serialization/order/tolerance differences explicitly and, when the change is
behavior-sensitive, a reproducible performance measurement.

## Permissions

`quantik-core-rust` only.

## Prohibited

- Sibling edits or remote writes (push/tag/publish) — release-reviewer's job under a
  release task.
- Using an optimization to redefine semantics — a faster path must produce the same
  canonical output, not a "close enough" one.
- Depending on a future or unpublished tag of `quantik-core-contracts` or
  `quantik-core-py`. Versioning here is lockstep and py tags before rust — the rust tag
  build checks out py at the same tag ref and fails if it is not there.
- Changing `Cargo.lock`'s presence/absence without checking CI's `--locked` expectation
  first — that is an open build-policy risk here, not a free edit.

## Verification

```
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-targets --all-features --locked
```

This is exactly the CI gate in `.github/workflows/rust.yml` — run all three, not a
subset, before reporting green.

## Failure modes specific to this repo

- Low-level and high-level terminal-state checks can disagree on some invalid states —
  a parser or move-generation fix at one layer can leave the other layer's behavior
  stale.
- Release-constant duplication: contract-release identifiers live in `bench::contracts`
  as well as `Cargo.toml`. A version bump that updates one and not the other passes a
  shallow check and fails a real one.
- MCTS transposition/policy identity depends on the same canonical-key derivation the
  opening book uses; changing one without the other desynchronizes cached evaluations
  silently.
- A workflow's expected-release constant lagging the source version, inside the *same*
  repo, is a recurring failure mode here (seen: workflow read `1.1.0` while `Cargo.toml`
  read `1.2.0`) — check both independently, never infer one from the other.

> **Load with:** [`../context/repositories/quantik-core-rust.md`](../context/repositories/quantik-core-rust.md) · [`../context/system/canonical-invariants.md`](../context/system/canonical-invariants.md) · [`../context/system/release-model.md`](../context/system/release-model.md)
