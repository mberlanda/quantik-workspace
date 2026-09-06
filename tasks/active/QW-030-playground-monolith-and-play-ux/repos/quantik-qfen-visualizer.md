# quantik-qfen-visualizer task

**Repository:** `quantik-qfen-visualizer` — dependency-free browser app, no
bundler, classic scripts, openable from `file://`.

**Objective:** turn the first screen from an engine debugger into a playground,
and put the debugger in a drawer at the bottom.

**Read before starting:** `AGENTS.md` in this repository. Two of its rules decide
how every task below is done.

**Relevant modules:** `index.html` (217 lines), `src/app.js` (714 — the DOM
wiring), `src/settings.js` (the persisted profile), `src/play.js` (the service
client), `src/engines.js` (the request literal — **do not change its shape**),
`src/styles.css` (908).

---

## The two rules that shape every task here

1. **A failing test comes first**, for any change to `src/*.js` logic. Not after,
   not "covered by an existing test". Write it, watch it fail, then implement.
2. **`node --test` does not verify a UI change.** The runner loads modules against
   a minimal DOM stub via `test/helpers/loadClassicScript.js`; it checks logic, not
   rendering. Serve `index.html` and look at it before calling anything done, and
   say in the PR what you looked at.

The consequence for design: **push logic into modules that never touch
`document`**, and keep `app.js` thin wiring. Each task below names the module to
put the testable part in. That split is not a style preference — it is the only
way the logic is testable at all here.

## Commit and PR discipline

**One logical change per commit. One PR per task V1–V5.** Branches `feat/…`,
`chore/…`, `fix/…`. Commit messages explain *why*; the diff shows what. No commit
trailers. `npm test` green before every PR.

The tasks are independent of each other and can land in any order, with one
exception: **V5 needs `quantik-models-py` M2 merged** to have anything to read.

---

## V1 — The lab drawer

**Branch:** `feat/lab-drawer`

Move into one `<details>` at the **bottom** of the page, collapsed by default:
the QFEN input and its Copy/Reset buttons, the seed input, the speed select, both
per-player controller selects, both remote endpoint URL fields, the service-base
override, and Export/Import trace.

**Keep every element id.** This is a relocation. The existing tests address these
ids and must keep passing untouched; if one breaks, you moved more than the DOM.

**Testable part — `src/layout.js` (new):** export the ordered list of advanced
control ids, a predicate over it, and read/write helpers for the drawer's
open/closed state in `localStorage` (same defensive `try`/`catch` shape
`settings.js` already uses for the theme — storage can throw, not just return
null). `test/layout.test.js` covers the default-closed state, that a persisted
open state survives a reload, and that a corrupt stored value falls back to
closed rather than throwing.

Label it for what it is — "Advanced", "Lab", "Under the hood" — not "Settings".
The existing Settings panel is theme colours and stays where it is.

---

## V2 — Modes of play

**Branch:** `feat/mode-chooser`

The first thing on the page. Four modes, prompted lightly — buttons or a segmented
control, not a form:

| mode | player 0 | player 1 |
|---|---|---|
| Play a model | human | engine |
| Watch two engines | engine | engine |
| Two players | human | human |
| Just the board | neither — the QFEN/analysis view the app is today |

Picking a mode sets the two controller selects that now live in the drawer. The
drawer stays the place to override them; the mode is the shortcut, not a
replacement.

**Testable part — `src/modes.js` (new):** `MODES` (id, label, one line of
description) and a pure `applyMode(profile, modeId)` returning the controller
assignment, with an unknown id falling back to a named default rather than
throwing. `test/modes.test.js` covers every mode's assignment, the fallback, and
that the mode round-trips through `settings.js`'s profile.

`settings.js` gains a `mode` field on the profile, normalized like the others.

**"Just the board" must stay reachable** — it is what the app is today and it is
the mode this repository's own name describes.

---

## V3 — How to play

**Branch:** `feat/how-to-play`

A collapsible explainer near the board, closed by default, open on a first visit
(reuse V1's storage helper if it landed; otherwise a local equivalent). Quantik's
rule is not guessable from the board:

- You place a shape on any empty square.
- You may **not** place a shape in a row, column, or 2×2 zone where your
  **opponent** already has that shape. Your own is fine.
- You win by completing a row, column, or zone with **four different shapes**, in
  either colour — whoever places the fourth wins, regardless of who owns the
  others.

**Check that wording against `quantik-core-contracts`' own rule statement before
writing it into the app**, and say in the PR which file you checked it against.
Two divergent statements of one rule is the failure to avoid; the contracts repo
is the source of truth.

**Testable part — `src/rules.js` (new):** export the rule text as structured data
(a title plus an ordered list of points) so `app.js` renders it rather than
holding a string. `test/rules.test.js` asserts the three group kinds and the
four-different-shapes win condition are all present — a cheap guard against
someone trimming the explainer down to something wrong.

---

## V4 — Make it feel like a playground

**Branch:** `chore/playground-styling`

`src/styles.css` only. **No logic, no `src/*.js` changes**, so this is the one
task with no failing test in front of it — and therefore the one where rendering
it is the entire verification. Screenshots in the PR.

What is being fixed: the page reads as an instrument panel. Every control has
equal visual weight, the board is one panel among several, and the first thing the
eye lands on is a monospace text field.

- The board is the largest thing on the page and is what loads first.
- The mode chooser and the primary action (New game) are the only prominent
  controls above the board.
- Assessment, evaluation bar and top-moves stay, quieter — they are genuinely
  interesting to a curious non-expert, and hiding them would be a loss.
- The drawer is visually recessive: no border-heavy panel, no accent colour.
- Keep the existing colour variables and the theme customization. Contrast has to
  survive both piece themes.

Do not add a dependency, a font CDN, or a build step. The app opens from
`file://` and that is a property worth more than any of those.

---

## V5 — Stay quiet when the server has no store

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

---

## Commands

```sh
nvm use          # lts/* from .nvmrc
npm test         # node --test
python3 -m http.server 5173 && open http://localhost:5173    # render it
```

## Expected artifacts

`src/layout.js`, `src/modes.js`, `src/rules.js`, changes to `src/play.js`,
`src/settings.js`, `src/app.js`, `index.html`, `src/styles.css`, and a test file
per new module. Five PRs.

## Completion criteria

Someone who has never seen Quantik opens the page, learns the rule, picks a mode,
and plays a game — without opening the drawer once. Everything in the drawer still
works exactly as it does today.

## Explicitly NOT in scope

- **The skill-level ladder.** No easy/medium/hard, no level→opponent mapping. It
  is blocked on QW-024's ply-0/ply-1 arena; QW-010 decision 4 rejected deriving it
  from the ply-3/6/9 tables that exist. Leave a place for it and put nothing in it.
- Puzzle mode (QW-011).
- Any change to the request body literal in `src/engines.js`.

## Handoff path

Create `tasks/active/QW-030-playground-monolith-and-play-ux/handoffs/` only once a
handoff exists.
