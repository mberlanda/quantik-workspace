# quantik-api-rust Packet

> **Purpose:** standalone Axum HTTP gateway exposing the `quantik-core-rust` engines (minimax, MCTS, beam) over `quantik.engine-request.v1`.
> **Load with:** [`quantik-core-rust.md`](quantik-core-rust.md), [`quantik-qfen-visualizer.md`](quantik-qfen-visualizer.md) (its client), [`../system/domain-glossary.md`](../system/domain-glossary.md)

## Ownership

Owns the HTTP surface only: `GET /health`, `GET /v1/engines`, `POST /v1/move/{minimax,mcts,beam}`. Every request is re-validated for legality against `quantik-core` before an engine runs. Does **not** own game rules or search algorithms — those belong to `quantik-core-rust`; this repo is a thin adapter plus its own dev-CORS/tracing/config concerns. Responses include the pinned core revision as engine provenance.

## Toolchain (verified 2026-08-30)

- `Cargo.toml`: package `quantik-api`, version `0.1.0`, edition 2021, `license = "MIT"`, `publish = false`.
- Dev dependency on `quantik-core` via a sibling path (`../quantik-core-rust/crates/quantik-core`). For an independently deployed build the README documents replacing it with a pinned git rev (`rev = "2b35565…"`), since this checkout otherwise floats on the sibling's working tree.
- Commands, all run and passing 2026-08-30: `cargo test --workspace` (3 tests), `cargo clippy --workspace --all-targets --all-features -- -D warnings` (clean), `cargo fmt --all -- --check` (clean), `cargo run --release` (binds `127.0.0.1:8000` by default, override with `QUANTIK_API_ADDR`).
- **No CI workflow** — `.github/workflows` does not exist (verified 2026-08-30), matching WORKSTREAMS.md's "no CI" note.
- No `AGENTS.md` in this repo.

## Git — corrects the workspace record (verified 2026-08-30)

**This repo has a working GitHub remote**, contrary to WORKSTREAMS.md's workstream 12 ("`quantik-api-rust` has no git remote. Local commits only, on one machine.") and the root `CLAUDE.md` repo table. Verified three ways: `git remote -v` shows `origin git@github.com:mberlanda/quantik-api-rust.git`; `git ls-remote origin` resolves `HEAD`/`refs/heads/main` to the same SHA as local `HEAD` (`f814093`, 2026-08-29 16:57); and `github.com/mberlanda/quantik-api-rust` loads as a public repo with 4 commits and an MIT license. Local `main` reports "clean — nothing to commit" against `origin/main` — fully in sync, nothing stranded on one machine. **This should be corrected wherever the "no remote" claim is repeated**, including workstream 12 and the repo table in the workspace root `CLAUDE.md`.

One consequence: `docs/model-serving.md`'s mover-relative-encoding correction, which WORKSTREAMS.md describes as "local commit `02bfcd1`, unpushed," is also pushed — it is commit `02bfcd1` in the now-synced history above.

## Current state, 2026-08-30

`docs/model-serving.md` still has an open runtime decision (candle vs. ONNX, via `tract-onnx`) for running the policy/value network inside this gateway — not yet picked. That decision, and the Dockerize-this-service workstream, both depend on this repo and are tracked in the workspace root `WORKSTREAMS.md` (workstreams 4 and 8), not duplicated here.
