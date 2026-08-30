# Current Architecture

> **Purpose:** The real shape of the Quantik system as of 2026-08-30 — what exists, what talks to what, and one honest consequence of the newest piece.
> **Load with:** [`repository-map.md`](repository-map.md) (ownership) · [`canonical-invariants.md`](canonical-invariants.md) (what must hold across it) · [`release-model.md`](release-model.md) (how the core three ship)

This file is not loaded automatically by `quantik-workspace context ...` — it is reachable
only through the links in `canonical-invariants.md` and `repository-map.md`. Read it
directly, or through one of those.

## The shape, as of 2026-08-30

Two engine cores — a Rust crate and a Python package — implement the same game rules and
validate against schemas owned by `quantik-core-contracts`. Neither core is authoritative
over the other; the contracts repo is (`canonical-invariants.md`, invariant 5).

`quantik-models-py` consumes both cores to train, evaluate, and — new as of a batch of
seven PRs merged 2026-08-29 across two repos — **serve** policy-value networks: dataset
materialization from solved positions, supervised training, the arena (engine-vs-engine
and engine-vs-oracle evaluation), checkpoint export to ONNX and Hugging Face, and now a
**play service**. It serves the browser visualizer, plays classical engines and trained
networks through one registry (addressed by an opponent id like `cpool@128` — see
`domain-glossary.md`), and records finished games to SQLite at
`~/.local/share/quantik/games.db`.

The roster size is **6 classical opponents plus 2 per discovered model** (`@0` raw policy
and `@128` MCTS), so it is a property of whichever model directory is staged, not of the
system. Verified 2026-08-30 against `play.opponents.roster`. Any fixed count quoted
elsewhere — WORKSTREAMS.md says 20, `quantik-models-py/docs/play-service.md` shows 14 in
an illustrative block — describes one machine's `runs/` on one day.

`quantik-api-rust` is an Axum HTTP gateway exposing the Rust engines — search, not
training or serving. It has no git remote (`repository-map.md`).

`quantik-qfen-visualizer` is a dependency-free browser app for playing and watching
engines. It speaks one contract, `quantik.engine-request.v1`, to *any* HTTP endpoint — the
Rust gateway and the Python play service are interchangeable backends to it, which is what
makes the next paragraph possible.

`quantik-workspace` (this repo) holds no game logic; it is the control plane described in
`docs/adr/0001-workspace-as-control-plane.md`. `articles` is a separate, unpublished
Substack drafting repo with no git remote.

## The consequence worth stating plainly

**The play service makes `quantik-api-rust` redundant for playing.** Both speak the same
request contract to the same visualizer, and the Python service already does it end to
end, with the real trained networks. What `quantik-api-rust` still has going for it is not
"playing" — it is being a *deployable single binary*: no Python runtime, no virtualenv, a
container that starts fast and ships small. Whether that justification survives depends on
workstream 4 (model serving inside the Rust API — a `candle` vs. `tract-onnx` decision,
pending as of 2026-08-30) landing at all.

Two things not yet true, worth not assuming: `quantik-api-rust` does not yet serve any
neural network, and nothing in this system has shipped as a public container. See
WORKSTREAMS.md §4 and §13 for the current state of both.
