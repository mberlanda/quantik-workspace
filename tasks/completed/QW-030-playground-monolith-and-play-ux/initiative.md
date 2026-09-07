# QW-030: The Playground — One-Port Monolith and Non-Expert Play UX

> **Purpose:** Make the browser app and the play API one installable thing on one
> port, and turn the first screen from an engine debugger into a playground —
> without giving up the debugger.
> **Load with:** [`context/system/canonical-invariants.md`](../../../context/system/canonical-invariants.md),
> [`context/repositories/quantik-models-py.md`](../../../context/repositories/quantik-models-py.md),
> [`context/repositories/quantik-qfen-visualizer.md`](../../../context/repositories/quantik-qfen-visualizer.md)

## Problem and motivation

`quantik-models` 1.0.0 published to PyPI on 2026-09-05. Installing it gets you the
API and no app:

```python
# src/quantik_models/play/__main__.py:28
DEFAULT_STATIC = Path(__file__).resolve().parents[4] / "quantik-qfen-visualizer"
```

`parents[4]` is the `quantik-ns` workspace root. From a wheel in
`site-packages`, it points at nothing, and `_serve_static` answers
`404 {"error": "no static directory is configured"}`. So the one-port
arrangement — which QW-009 already proved works, and which the Docker image
already ships — is reachable only by cloning two repositories side by side.
That is the gap between "the package is published" and "someone can play it".

The second half is what they would see if they got there. The current first
screen is a QFEN text field, two dropdowns of controllers, a seed input, two raw
endpoint-override URL fields, and Export/Import trace buttons. Every one of those
is worth keeping and none of them is a reasonable thing to hand a visitor who
wants to play a game. QW-010 named the audience problem; this initiative fixes the
*shape* of the screen, and deliberately leaves the skill-level ladder alone.

## Existing and desired behaviour

| | existing | desired |
|---|---|---|
| install | two checkouts, sibling-relative `--static` | `pip install 'quantik-models[serve,hub]'`, one command |
| ports | one already, but only via `--static` or Docker | one, by default, from the package |
| first screen | QFEN box + controller matrix + endpoint URLs | a mode of play, a board, and a bottom drawer |
| rules | not stated anywhere in the app | a collapsible explainer |
| storeless server | client POSTs anyway, shows `Not recorded: … 503` | client asks, records nothing, says nothing |
| Docker weights | baked from local `runs/train/*/best` | pulled from `brpoplpush` at build time |

## Contracts and repositories

Two repositories, no contracts touched. `quantik.engine-request.v1` and
`quantik.engine-response.v1` are unchanged: this initiative adds a **capability
field to `GET /api`**, which is the service's own index route and not a
registered schema. The client's request literal in `src/engines.js` stays exactly
as it is.

The dependency edge `quantik-qfen-visualizer -> quantik-models-py` already exists
in `workspace.yaml` as `["runtime", "contract"]`. This initiative adds a *build*
edge in the other direction — `quantik-models-py` vendors the visualizer's built
output — which is why the sync is one-way and mechanical, and why the vendored
copy records the commit it came from.

## Constraints and preserved invariants

1. **`quantik-qfen-visualizer` stays dependency-free and `file://`-openable.**
   No bundler, no runtime dependency under `src/` or in `index.html`, classic
   scripts only. The vendored copy is a byte copy, not a build product; if it ever
   needs a build step, that is a new decision, not an implementation detail.
2. **The visualizer is strict TDD by convention.** No `src/*.js` behaviour change
   without a failing test written first. Its test runner uses a DOM stub, not a
   real DOM, so testable logic goes in modules that never touch `document` and
   `app.js` stays thin wiring.
3. **A UI change is not verified by `node --test`.** It has to be rendered.
4. **No skill-level ladder.** QW-010 decision 4 explicitly rejected deriving
   levels from the existing ply-3/6/9 tables, because a published ladder is hard
   to change once players have opinions about it and the ply-0 arena (QW-024,
   `ready-to-run`) is one run rather than a research programme. At ply 0 every
   checkpoint is uniform to three decimal places, so the phase a human game starts
   in is unmeasured for every model. This initiative prepares the slot and ships
   no numbers into it.
5. **The debugger survives.** Everything moved into the drawer keeps its element
   id and its behaviour. This is a relocation, not a removal — the existing tests
   that address those ids should keep passing.
6. **The weights are CC BY-NC 4.0 and the code is MIT.** Any image or artifact
   that carries weights carries `docker/NOTICE`.

## Migration and compatibility strategy

Additive throughout. `--static` keeps working and keeps overriding, which is how
someone developing the visualizer against a live checkout will run it. A client
that does not read the new `GET /api` capability field behaves exactly as it does
today. No stored profile, recorded game, or QFEN string changes shape.

## Release strategy and ordering

`quantik-models-py` **M1** first: it creates the target the visualizer work is
aimed at. `quantik-models-py` **M2** before visualizer **V5**, because V5 needs
something to read. The visualizer PRs V1–V5 are independent of each other and can
land in any order. `quantik-models-py` **M5** re-syncs the vendored app and is the
last thing to land.

The vendored copy is **not** re-synced per visualizer PR. Sync is a release-time
step, so the app under `src/quantik_models/play/app/` lags `main` of the
visualizer between M1 and M5 by design.

A `quantik-models` release is cut by hand — see the release checklist in
`DEVELOPMENT.md`. Tagging does not publish: `publish.yml` is written for PyPI
trusted publishing and the publisher was never registered, so its upload job fails
while `verify` and `build` pass.

## Risks and exclusions

**Excluded:** the skill-level ladder (QW-010, blocked on QW-024), puzzle mode
(QW-011), GHCR publication (QW-009 criterion 5 — this initiative makes the image
correct, it does not push it), and any change to the engine request/response
schemas.

**Risk: the vendored copy silently rots.** Mitigated by `app/SOURCE.json` plus a
test that every asset `index.html` references exists in the vendored tree — a
partial or stale sync that drops a file fails CI. A sync that is merely *old*
does not, and is caught by the release checklist instead.

**Risk: the drawer becomes where features go to die.** The drawer is for controls
that already exist. Anything new that a player needs belongs on the main surface.

**Risk: `quantik-models-play` with no staged models looks broken.** With
`[serve,hub]` and no `--models` directory, `scan_models` finds nothing and the
roster is the six classical opponents. That is a complete playground, and the
empty-roster case must read as a deliberate state in the UI, not as a failure.

## Acceptance criteria

See `manifest.yaml`.
