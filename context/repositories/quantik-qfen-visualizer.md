# quantik-qfen-visualizer Packet

> **Purpose:** dependency-free browser app for playing Quantik, watching engines play, and exporting game traces.
> **Load with:** [`https://github.com/mberlanda/quantik-qfen-visualizer/blob/main/AGENTS.md`](https://github.com/mberlanda/quantik-qfen-visualizer/blob/main/AGENTS.md), [`quantik-api-rust.md`](quantik-api-rust.md), [`quantik-models-py.md`](quantik-models-py.md), [`../system/domain-glossary.md`](../system/domain-glossary.md)

## Ownership

Owns: QFEN parsing/rendering/board analysis (`qfen.js`), turn state and legal-move application for the UI (`game.js`), two local browser engines (random, tactical) plus a portable remote-HTTP adapter (`engines.js`), lossless `quantik.game-trace.v1` export/import with replay validation (`trace.js`), and interaction/rendering only in `app.js`.

Does **not** own legality authority for production play. The README is explicit: "the remote engine should remain authoritative and independently validate every requested position/action with `quantik-core-py` or `quantik-core-rust`." The browser rules engine exists to make the standalone (no-backend) build playable, not as a source of truth.

Speaks `quantik.engine-request.v1` to any HTTP endpoint: `POST {qfen, side_to_move, legal_action_indices}` → `{action_index}`, action indices `shape*16 + position` (see `../system/domain-glossary.md`). An engine on another origin must allow CORS; opening over `file://` is possible but HTTP serving is recommended.

## Toolchain (verified 2026-08-30)

- Node via `nvm`; `.nvmrc` pins `lts/*`, `package.json` requires `node >=22`.
- `npm test` → `node --test`. **63/63 pass.** No test-framework dependency (`node:test` + `node:assert`); DOM-touching modules load against a stub via `test/helpers/loadClassicScript.js`, not a real DOM.
- No lint script in `package.json` — only `"test"` is defined. Do not invent a lint command.
- No build step. `index.html` and `src/*.js` are classic scripts on purpose — `devDependencies` may exist for tooling (tests, screenshots) but nothing under `src/` or `index.html` may depend on them at runtime.
- No CI workflow present (`.github/workflows` does not exist, verified 2026-08-30) — WORKSTREAMS.md's CI table lists this repo as "not checked"; it is more precisely "no workflow to check."
- `package.json` is `"private": true`, version `0.2.0` — not published to npm.

## Repo-local instructions

**`AGENTS.md`** mandates TDD — a failing test before any `src/*.js` logic change — plus atomic commits, one PR per change, and `feat/…`/`fix/…`/`chore/…` branch naming. It also flags that `node --test` verifies QFEN/settings *logic* only, not rendering: a UI change needs an actual render check before being called done. Load it rather than trusting a paraphrase.

## Git (verified 2026-08-30)

Has a GitHub remote, `git@github.com:mberlanda/quantik-qfen-visualizer.git`. `HEAD` `9c080f5` (2026-08-29 23:35).

## Current state, 2026-08-30

The play service in `quantik-models-py` (`play/server.py`) now serves this app plus roughly 20 opponents over HTTP, and records games unless started `--no-store`. Three requested-but-not-started workstreams land here:

- **Puzzle mode UI** — the generator (`quantik_models.play.puzzles`) is done and produces a themed JSON pack; this repo still needs the pack committed and a picker built. Needs no play service — static JSON only.
- **Skill-level / "how to play" UX** — replace the raw ~20-opponent roster with easy/medium/hard, derived from arena numbers (not guessed), plus a collapsible rules explainer.
- **Public storeless deployment** — the browser client currently tries to record a game even with no store configured and would show a `503` error; it should read `GET /api` and stay quiet when no store is present.
