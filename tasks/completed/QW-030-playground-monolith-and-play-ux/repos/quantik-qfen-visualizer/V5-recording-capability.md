# V5 — Stay quiet when the server has no store

**Branch:** `fix/no-store-is-not-an-error`

**Depends on `quantik-models-py` M2**, which adds `"recording": <bool>` to
`GET /api`.

Today `app.js:448` POSTs the finished game unconditionally and `app.js:457` prints
`Not recorded: ${error.message}` — so against the storeless public server, every
game ends in what looks like an error. It is not one; it is the configuration
working as designed.

**Testable part — `src/play.js`:** add `fetchCapabilities({ baseUrl })` reading
`GET /api`, and have `recordGame` decline to POST when recording is off. Treat an
absent field as `true` — an older server that does not report is a server that
does record. `test/play.test.js` covers: recording on → POST happens; off → no
POST and no throw; `/api` unreachable → falls back to attempting the POST, because
a network failure is not evidence of a storeless server.

`app.js` calls it once at startup and stores the answer. When recording is off,
the end-of-game message says what happened to the game — "not saved" as a plain
fact, once, not an error — or says nothing. **A visitor must never see an HTTP
status code.**

## Execution contract


1. **A failing test comes first**, for any change to `src/*.js` logic. Not after,
   not "covered by an existing test". Write it, watch it fail, then implement.
2. **`node --test` does not verify a UI change.** The runner loads modules against
   a minimal DOM stub via `test/helpers/loadClassicScript.js`; it checks logic, not
   rendering. Serve `index.html` and look at it before calling anything done, and
   say in the PR what you looked at.

The consequence for design: **push logic into modules that never touch
`document`**, and keep `app.js` thin wiring. This packet names the module to
put the testable part in. That split is not a style preference — it is the only
way the logic is testable at all here.


**One logical change per commit. One PR for this work item.** Branches `feat/…`,
`chore/…`, `fix/…`. Commit messages explain *why*; the diff shows what. No commit
trailers. `npm test` green before every PR.

## Scope and handoff

Edit only the manifest allowed paths. Record exact starting and final revisions, branch, PR, commands and results, and dependency evidence in a work-item-specific handoff. Path expansion requires coordinator review.

Decision references: `decisions.md#D6`.

No skill ladder, puzzle mode, or engine request-shape changes. Preserve file:// support and dependency-free classic scripts.
