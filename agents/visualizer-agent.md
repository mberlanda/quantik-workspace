# Visualizer Agent

Apply `operating-contract.md`.

## Scope

`quantik-qfen-visualizer` only: the dependency-free browser app (`index.html`, `src/`)
that renders and plays QFEN positions, speaks the engine request/response contract to
any HTTP engine endpoint, and hosts puzzle mode.

## Inputs

Visualizer packet, the engine contract this change targets, and a failing test. Note
that the client-side contract is currently a hardcoded JS string literal
(`src/engines.js`), not yet a registered `quantik-core-contracts` schema — treat its
shape as provisional until it is registered.

## Outputs

`src/*.js` changes with the test that failed before them, focused `node --test`
coverage, and a rendered check (screenshot tooling or a local serve) before the change
is reported done.

## Permissions

`quantik-qfen-visualizer` only. No sibling or remote writes.

## Prohibited

- Any `src/*.js` behavior change without a failing test written first — this repo is
  strict TDD by convention, not by suggestion.
- Reporting a UI change as verified from `node --test` alone — the test runner checks
  QFEN/settings *logic* against a DOM stub, not what actually renders. The change must
  be actually rendered before it is called done.
- Adding a runtime dependency under `src/` or to `index.html`. `devDependencies` (test
  tooling, screenshot tooling) are fine; the shipped app stays classic-script,
  no-bundler, dependency-free.
- Treating the client's own reading of a game outcome as authoritative — the play
  service replays and re-derives the result server-side; the client's claim is recorded
  beside it, not instead of it.

## Verification

```
nvm use              # pins lts/* via .nvmrc
npm test               # node --test
npm run screenshot      # once screenshot tooling lands; until then, serve index.html
                         # locally and check manually
```

## Failure modes specific to this repo

- `quantik.engine-request.v1` / `quantik.engine-response.v1` are hardcoded
  independently here (`src/engines.js`) and in `quantik-api-rust/src/lib.rs`, with
  nothing keeping them in agreement. A change to the request/response shape here is a
  silent cross-repo break until both are registered as real contracts in
  `quantik-core-contracts`.
- The visualizer speaks QFEN strings at its wire boundary, but any model serving moves
  behind that boundary is trained on the mover-relative tensor encoding, not the
  colour-ordered one. A change that starts assuming board-tensor semantics rather than
  QFEN strings crosses into the same ambiguity a training-side change has to be careful
  about — see canonical invariants.
- A public, storeless deployment must never surface a storage error to a visitor: the
  client is expected to check `GET /api` for whether a store exists and stay quiet,
  rather than show `Not recorded: … 503` at the end of every game.

> **Load with:** [`../context/repositories/quantik-qfen-visualizer.md`](../context/repositories/quantik-qfen-visualizer.md) · [`../context/system/domain-glossary.md`](../context/system/domain-glossary.md) · [`../context/system/current-architecture.md`](../context/system/current-architecture.md)
