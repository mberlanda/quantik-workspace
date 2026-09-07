# QW-030 Status

Created 2026-09-05, immediately after `quantik-models` 1.0.0 reached PyPI.

**Why now:** the release is what exposed the gap. `pip install quantik-models`
succeeds and then serves no app, because `play/__main__.py:28` resolves
`--static` through `parents[4]` to a sibling checkout that exists only inside the
`quantik-ns` workspace. Verified against the published wheel, from outside the
workspace tree.

**Scope set by the user, 2026-09-05:** one-port packaging plus the WS14 play UX
(this packet's V1–V5 and M1–M5), plus the two QW-009 leftovers that share the same
surface — the storeless 503 the client shows at the end of every game, and the
Docker image sourcing weights from the Hub rather than from local `runs/`. Puzzle
mode (QW-011) was considered and excluded.

**Relationship to the existing packets:**

- **QW-009** — this initiative delivers its criteria 3 and 4 (Hub weights at build
  time, `--no-store` preserved) and leaves criterion 5 (GHCR) untouched.
- **QW-010** — this initiative delivers the *shape* of the non-expert UI: the mode
  prompt, the how-to-play explainer, and the advanced disclosure that its sixth
  acceptance criterion asks to specify. It delivers **none** of the skill-level
  mapping, which stays blocked.
- **QW-024** — unchanged and still `ready-to-run`. It is the blocker on the
  ladder, and running it is the next action for QW-010, not for this packet.

**M1 done, 2026-09-06:** `quantik-models-py` PR #62, squash-merged at `d402e319`.
Vendors the app, re-points `DEFAULT_STATIC` at package data, and the CI smoke
test (fresh install, no sibling checkout) is green on macOS/Ubuntu/Windows ×
py3.12/py3.13. See `handoffs/quantik-models-py.md` for the full record,
including a scope deviation: the PR also fixed a real bug in
`play/server.py` (outside M1's `allowed_paths`) — `HTTPServer.server_bind`'s
reverse-DNS lookup was hanging macOS CI for ~30s per run, the actual cause
behind three earlier failed fix attempts. Flagged for coordinator review.

**M2–M4 implemented 2026-09-06, merged 2026-09-07.** All three
`quantik-models-py` work items are done, green (650 passed, mypy clean
on each branch), and now merged to `main` in order (#64→#65→#66, per the
user's 2026-09-07 go-ahead) — all three fast-forwarded clean, no conflicts.
See `handoffs/quantik-models-py.md` for the full record of each.

- **M2** (#64, `feat/api-advertises-recording`, squash-merged at `dd61dcd`):
  `GET /api` now reports `"recording": <bool>`. Unblocks visualizer V5.
- **M3** (#65, `feat/fetch-stage`, squash-merged at `ccae033`): `hub.stage()`
  + `--stage`/`--copy` on `quantik-models-fetch`. One gap found and fixed
  *within this pass*, before merge: the initial symlink-or-copy-on-OSError
  fallback doesn't cover the Docker case (a symlink into a build stage's own
  Hub cache resolves fine within that stage, then dangles once a later
  stage copies the directory alone) — added an explicit `--copy`/`copy=True`
  to force real files.
- **M4** (#66, `chore/docker-from-hub`, squash-merged at `e231abc`,
  **stacked on #65** — genuinely depends on `--copy`, merged right after
  it): the Docker image now builds from
  `quantik-models-py` alone (no sibling `quantik-qfen-visualizer` context)
  and fetches all four published weights from the Hub at build time
  instead of a hand-staged local `runs/` copy. Built and ran it for real —
  not just written the Dockerfile — and measured **498 MB** (four
  architectures; down from 553 MB after dropping the unused
  `model.safetensors` `--runtime onnx` never opens). `scripts/build_docker_image.sh`
  and `docker/staging/` are now stale and were flagged rather than
  silently left to look current — both fall outside M4's `allowed_paths`.

**V1 implemented and merged, 2026-09-06.** `quantik-qfen-visualizer`
PR #8 (`feat/lab-drawer`), squash-merged at `67656a2`: the QFEN box + Copy/Reset, seed, speed, both
per-player controller selects, both remote endpoint fields, the service-base
override, and Export/Import trace all move into one collapsed `<details id="advanced-drawer">`
at the bottom of the page, labeled "Advanced". Every element id kept
unchanged. New `src/layout.js` holds the ordered id list, a membership
predicate, and localStorage read/write for the drawer's open state (same
defensive shape as `settings.js`'s theme storage). `npm test` → 69/69
(63 existing + 6 new). Rendered and driven live via Claude in Chrome, including
a reload to confirm the open state persists. See `handoffs/quantik-qfen-visualizer.md`
for the full record, including a flagged scope deviation: adding `layout.js` as
a new classic script required a one-line update to `test/index.test.js`'s
exact-match script list, outside V1's `allowed_paths` — same pattern as M1's
`server.py` deviation. V2 and V3 will likely hit the identical conflict when
they add `modes.js` and `rules.js`.

**V2 implemented and merged, 2026-09-06.**
`quantik-qfen-visualizer` PR #9 was opened stacked on `feat/lab-drawer`
(both touch `app.js`); when the user asked to merge PRs one by one, merging
#8 first (squash) deleted that base branch and GitHub auto-closed #9 rather
than retargeting it, since a squash commit isn't an ancestor of the stacked
branch. Rebased `feat/mode-chooser` onto the new `main` (`git rebase --onto
main 8880327 feat/mode-chooser`, `8880327` being V1's pre-squash tip),
force-pushed, and reopened as **PR #10** with the same two commits and no
content changes; #10 squash-merged clean at `21d7b46`. Worth knowing for
V3–V5: **each stacked PR will need this same rebase-and-reopen once its
base branch gets squash-merged out from under it** — plan on it rather than
being surprised by another auto-close.
Four mode buttons — Play a model, Watch two
engines, Two players, Just the board — render as the first thing on the page.
New `src/modes.js` (`MODES` + pure `applyMode`) sets the drawer's two
controller selects; "Just the board" is a genuine pass-through, and an
unrecognized mode id resolves to that same pass-through rather than throwing.
`settings.js` gained a normalized `mode` field. Resolved both open decisions
in `decisions.md`: **D7** — the chooser persists across visits (new visitors
still see a neutral, unhighlighted prompt); **D8** — a classical-only roster
is offered under "Play a model" rather than hidden or disabled, with zero
special-case code since the opponent picker already shows whatever
`GET /api/opponents` returns. `npm test` → 77/77. Rendered and driven live via
Claude in Chrome: picked "Two players," confirmed both drawer selects flipped
to Human, reloaded and confirmed the highlight and controllers both
persisted, then picked "Just the board" and confirmed it passed the Human/Human
assignment through unchanged. Same `test/index.test.js` script-list deviation
as V1 (flagged in both PRs). Full record in `handoffs/quantik-qfen-visualizer.md`.

**V3 implemented and merged, 2026-09-06.** `quantik-qfen-visualizer` PR #11
(`feat/how-to-play`), branched fresh off the already-merged `main` (no
stacking, no rebase-and-reopen needed this time). New collapsible
`<details id="how-to-play">` sits directly above the board grid; new
`src/rules.js` holds a frozen `RULES` object (title + ordered points) and
localStorage read/write for the panel's open state, deliberately defaulting
to **open** on a first visit or on corrupt/missing storage — the opposite
default from `layout.js`'s drawer, since hiding the rules from someone who
might need them is the worse failure mode. Rule wording was checked against
three independent sources: `quantik-core-contracts/docs/game-state.md` (the
placement restriction, stated there as the `ILLEGAL_PLACEMENT` rule),
`quantik-core-rust`'s `game.rs`, and `quantik-core-py`'s `game_utils.py`
(both stating the win condition in "four distinct/different shapes,
regardless of colour" terms); all three agree. `npm test` → 85/85 (77
existing + 8 new). Rendered and driven live via Claude in Chrome: confirmed
the panel opens by default, collapsed it, reloaded and confirmed the closed
state persisted. Same `test/index.test.js` script-list deviation as V1/V2
(flagged in the PR). Squash-merged clean at `614d527` — a normal
fast-forward, no auto-close since V3 branched off already-merged `main`
rather than off another open PR. Full record in
`handoffs/quantik-qfen-visualizer.md`.

**V4 implemented and merged, 2026-09-07.** `quantik-qfen-visualizer` PR #12
(`chore/playground-styling`), branched fresh off the already-merged `main`,
`src/styles.css` only — no `index.html`, no `src/*.js`, so no
`test/index.test.js` script-list deviation this time (nothing to add a new
script tag for). Four commits, one concern each: (1) `order` on
`.workspace`'s top-level sections so the board paints right after the mode
chooser, ahead of the (now de-emphasized) game panel's secondary controls,
examples, and settings — DOM/tab order untouched, only paint order moves;
(2) real card styling for the mode chooser (unstyled since V2), selected
state reusing the existing `--player-0` teal via `color-mix()`; (3) widened
board, narrowed and quieted the side panel's cards; (4) recessive styling
for the advanced drawer and the how-to-play explainer — hairline border,
muted label, shared rotating-triangle disclosure, no accent colour on
either. `npm test` → 85/85, unchanged (CSS-only). Rendered and driven live
via Claude in Chrome at 1280×1000: confirmed the full visual order,
clicked a mode card to see the highlight, opened the drawer to confirm no
card chrome. A narrow-viewport check was attempted but the browser tool's
resize didn't visibly change the capture in this session — not chased
further; flagged as a follow-up in the handoff rather than silently
skipped. Squash-merged clean at `b9f5982`, plain fast-forward. Full record
in `handoffs/quantik-qfen-visualizer.md`.

**`quantik-models-py` M1–M4 are all merged** (`d402e31`, `dd61dcd`,
`ccae033`, `e231abc`).

**V5 implemented and merged, 2026-09-07.** `quantik-qfen-visualizer` PR #13
(`fix/no-store-is-not-an-error`), branched fresh off the already-merged
`main`. New `fetchCapabilities({baseUrl, fetch})` in `src/play.js` reads
`GET /api`'s `recording` field and defaults to `true` on anything but an
explicit `false` — an absent field (`decisions.md#D6`), an HTTP error, and
an unreachable service (a rejecting `fetch`) are all read the same way, so
a capability probe can never itself become an error banner. `recordGame`
gained a `recording` option: when off, it skips its POST entirely and
returns `{recorded: false, skipped: true}`. `app.js` fetches capabilities
once at startup and passes the answer through; a skip now reads "Not saved
— this server keeps no record of games." in the same message slot as every
other end-of-game outcome, not styled as an error. TDD: 7 new tests in
`test/play.test.js`, watched fail (`fetchCapabilities is not a function`)
before implementing. `npm test` → 92/92. No `test/index.test.js` deviation
this time — no new script tag. Rendered and driven live via Claude in
Chrome against a small local mock of a storeless server (`/api` →
`{"recording": false}`): confirmed via the page's own console that the real
wired functions skip the POST correctly, confirmed an unreachable `/api`
resolves to `{"recording": true}` with no thrown exception, then played a
full "Watch two engines" autoplay game to completion against the mock and
watched the end-of-game line read exactly the plain-fact message above,
with no HTTP status anywhere on the page. Squash-merged clean at `3d6e134`,
plain fast-forward. Full record in `handoffs/quantik-qfen-visualizer.md`.

**All of V1–V5 are now merged.** QW-030's `quantik-qfen-visualizer` side is
done.

**M5 implemented, 2026-09-07 — PR open, not merged.** `quantik-models-py`
PR #67 (`docs/one-port-playground`), five commits, all 12 CI checks green
(both `pytest (py3.12)` and `pytest (py3.13)`). Re-synced
`src/quantik_models/play/app/` against the now-finished visualizer `main`
(`3d6e134`, up from `6ae703d`) — every V1–V5 change, plus the three new
classic scripts. Fixed the `README.md` and `docs/play-service.md`
quickstarts, which had been quietly broken since before this initiative:
`quantik-models-play --models staging` implied a `staging/` directory that
did not exist without a prior checkout, and never named `--runtime onnx`
even though the `[serve]` extra doesn't install torch. Replaced with
`quantik-models-fetch --all --stage staging` (M3) then `--runtime onnx`,
and **verified both commands for real** against the live Hugging Face Hub
in a scratch directory before writing them down — real fetch, real
storeless server, `curl` against `/` and `/api`. Added a new
`docs/play-service.md` section on the vendored app (source of truth,
release-time-not-per-PR sync per D1–D3, `--static` for live-checkout
development) and documented `GET /api`'s `recording` field next to the
existing route list. Added the re-sync to `DEVELOPMENT.md`'s release
checklist as its own first step, chronologically ahead of the version bump
rather than physically next to the model-card step the packet named — the
two now cross-reference each other in the text; the reasoning is recorded
in `handoffs/quantik-models-py.md`. One `CHANGELOG.md` entry under
`Unreleased` covers the whole initiative, since M1–M4 merged without their
own. The one local `pytest` failure
(`test_checkpoint_fixture.py::test_fixture_manifest_validates_through_core_py`)
is a pre-existing, unrelated `contract_version` drift in the sibling
`quantik-core-py` checkout — confirmed present on `main` before this
branch's changes, and absent in CI (no sibling checkout there). Full record
in `handoffs/quantik-models-py.md`.

**Next action: none — this was the last work item in the initiative.**
V1–V5 and M1–M5 are all implemented; only PR #67's merge is outstanding,
and that is the user's call, same as M2–M4 were. Once #67 merges, every
acceptance criterion in `manifest.yaml` has shipping code behind it; closing
the initiative out (moving it to `tasks/completed/`) is a separate,
deliberate step for whoever does that, not implied by this record.
