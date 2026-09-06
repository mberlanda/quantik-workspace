# quantik-models-py task

**Repository:** `quantik-models-py` (currently at 1.0.0, published to PyPI)

**Objective:** make the installed package serve the browser app and the JSON API
on one port with no sibling checkout, teach `GET /api` to advertise whether it has
a store, and build the Docker image from published Hub weights.

**Read before starting:** `DEVELOPMENT.md` — "Invariants that are not negotiable"
and the release checklist. `docs/play-service.md`. `AGENTS.md`. Do not grep your
way in; the conclusions that matter here are written down and several are about
measurements that turned out to be wrong.

**Relevant modules:** `src/quantik_models/play/__main__.py` (`DEFAULT_STATIC`,
line 28), `play/server.py` (`_API_INDEX`, `_serve_static`, the `create_server`
factory), `play/registry.py` (`scan_models`), `src/quantik_models/hub.py`,
`pyproject.toml`, `MANIFEST.in`, `scripts/check_dist.py`, `docker/Dockerfile`,
`docker/NOTICE`.

**Required contracts release / wire IDs:** none. `quantik.engine-request.v1` and
`quantik.engine-response.v1` are untouched.

**Constraints:** the `mypy` gate is real — run it. The base install stays `numpy`
+ `quantik-core`; the vendored app is package data and adds no dependency. Say
what you actually ran.

---

## Commit and PR discipline

**One logical change per commit. One PR per milestone below. Do not stack
unrelated changes in one branch.** Each PR must be independently reviewable and
leave `main` green.

- Branches: `feat/…`, `fix/…`, `chore/…`, `docs/…`.
- Commit messages explain **why**, not what — the diff already shows what. A
  subject line under ~72 characters, then a body when the why is not obvious from
  the subject.
- **No commit trailers.** This repository commits as its owner: no
  `Co-Authored-By:`, no `Claude-Session:`. The eight commits behind PR #61 are the
  reference.
- Before opening each PR: `python -m pytest -q` and `python -m mypy`. Both, every
  time, and report the actual counts.

---

## M1 — Vendor the app, default `--static` to it

**Branch:** `feat/serve-app-from-package`

The one change that makes the package usable. `DEFAULT_STATIC` currently resolves
to `parents[4]/quantik-qfen-visualizer`, which from `site-packages` is a path that
does not exist.

1. `scripts/sync_visualizer.py` — copy `index.html` and `src/` from a sibling
   `quantik-qfen-visualizer` checkout (path as an argument, defaulting to
   `../quantik-qfen-visualizer`) into `src/quantik_models/play/app/`. Delete the
   destination first so a removed file does not survive. Write
   `app/SOURCE.json`: `{"repository": …, "commit": …, "synced": "YYYY-MM-DD"}`,
   with the commit read from `git -C <source> rev-parse HEAD`. Refuse to sync from
   a dirty source tree — a recorded commit that does not describe the bytes is
   worse than no record.
2. `play/__main__.py` — `DEFAULT_STATIC = Path(importlib.resources.files("quantik_models.play") / "app")`.
   Keep `--static` as an override, and say in its help text that it is how you
   serve a live visualizer checkout while working on it.
3. `pyproject.toml` — package data for `quantik_models.play` covering `app/**`.
   `MANIFEST.in` — ship it in the sdist too.
4. `scripts/check_dist.py` — assert both the wheel and the sdist contain
   `quantik_models/play/app/index.html`. This is the check that would have caught
   the whole class of bug being fixed here.
5. **Test — `tests/test_play_app_assets.py`:**
   - `DEFAULT_STATIC` exists and contains `index.html`.
   - **Every `<script src>` and `<link href>` in the vendored `index.html`
     resolves to a file inside the vendored tree.** This is the anti-rot check: a
     partial sync fails here instead of shipping a blank page.
   - `app/SOURCE.json` parses and carries a 40-character commit.
6. `.github/workflows/build.yml` — extend the existing console-script loop so
   `quantik-models-play --help` is covered, and add a step that starts the server
   on a free port with `--no-store`, fetches `/` and asserts the response is HTML
   containing the app title, then fetches `/api` and asserts JSON. Kill it after.

**Verify the thing this milestone exists for**, and report the transcript:

```sh
cd /tmp && python3 -m venv v && ./v/bin/pip install /path/to/dist/quantik_models-*.whl
./v/bin/python -c "from quantik_models.play.__main__ import DEFAULT_STATIC; print(DEFAULT_STATIC, DEFAULT_STATIC.is_dir())"
```

It must be run from **outside** `~/Code/quantik-ns` — inside
the workspace the old sibling path resolves and the bug hides. That is exactly how
it survived to 1.0.0.

---

## M2 — `GET /api` says whether there is a store

**Branch:** `feat/api-advertises-recording`

`_API_INDEX` in `play/server.py` is a module-level constant, so it cannot know
whether `db_path` is set. Make the `/api` payload a function of the handler's
`db_path` and add `"recording": <bool>`. Keep every existing key.

**Tests** in the existing server test module: storeless → `recording` is `false`
and `POST /api/games` still answers 503; with a store → `recording` is `true`.
Assert both in the same test file so the pair cannot drift apart.

This unblocks visualizer **V5**. Land it before V5 is reviewed.

---

## M3 — Stage Hub weights into a directory

**Branch:** `feat/fetch-stage`

`play.registry.scan_models` scans a directory of checkpoints. `hub` fetches into
the Hugging Face cache. Nothing bridges them, which is why the Docker image bakes
in `runs/train/*/best`.

Add `--stage <dir>` to `quantik-models-fetch` (and a `stage()` function beside
`prefetch()` in `hub.py`): for each requested model, resolve it, then materialize
`<dir>/<short-name>/` from the snapshot so that `--models <dir>` picks it up
unchanged. Symlink if the platform allows and copy otherwise — a Docker layer
needs real files, so make the copy path the one that is tested.

**Tests:** a staged directory satisfies `scan_models` and yields `status ==
"ready"`; the staged name matches the short name, not the Hub repo id; staging
twice is idempotent. Use the existing Hub test doubles — **do not hit the network
in tests.**

Note the naming trap: `export.huggingface.stage` renames `weights.safetensors` to
`model.safetensors` on the way to the Hub, and `arena.registry` reads both. A
staged directory must keep whichever name the snapshot has.

---

## M4 — Docker builds from the published weights

**Branch:** `chore/docker-from-hub`

`docker/Dockerfile` currently installs `.[serve]` and copies local checkpoints.

- Install `.[serve,hub]`.
- `RUN quantik-models-fetch --all --stage /app/models` in its own layer, with
  `HF_HOME` set to a build-time path so the cache does not bloat the final image.
  Use a build stage if that is what it takes to leave the cache behind.
- Run with `--models /app/models --runtime onnx --no-store`.
- Carry `docker/NOTICE` into the image and reference it from the image labels.
  Weights are CC BY-NC 4.0; the code is MIT. An image that ships weights without
  the notice is the mistake to avoid.
- Re-measure the image size and update the table in `docs/play-service.md`. The
  recorded figures are 441 MB (`best`) and 498 MB (`full`) from local weights —
  state the new number, and do not carry the old one forward as if it still held.

**Do not push anything to GHCR.** Publication is QW-009 criterion 5 and is not in
scope here.

---

## M5 — Re-sync the app and document the result

**Branch:** `docs/one-port-playground` (last to land)

1. Re-run `scripts/sync_visualizer.py` after V1–V5 have merged. This PR's diff is
   the vendored app plus documentation and nothing else.
2. `README.md` — the "Playing against them" section becomes two commands and no
   caveats. It currently implies a checkout.
3. `docs/play-service.md` — a section on the vendored app: where it comes from,
   that `quantik-qfen-visualizer` is the source of truth, how to serve a live
   checkout with `--static` while working on it, and the new `recording` field on
   `GET /api`.
4. `DEVELOPMENT.md` — add re-running the sync script to the release checklist,
   next to the existing step 6 about the Hugging Face model cards. A release that
   ships a stale app is the failure mode this step prevents.
5. `CHANGELOG.md` — under `## Unreleased`. The version bump is not yours to make.

---

## Commands and focused tests

```sh
python -m pytest -q                       # full suite; 637 passed at 1.0.0
python -m pytest tests/test_play_app_assets.py tests/test_play_server.py -q
python -m mypy                            # a gate, not advice
python -m build && python scripts/check_dist.py dist/
```

## Expected artifacts

`scripts/sync_visualizer.py`, `src/quantik_models/play/app/**` (vendored),
`tests/test_play_app_assets.py`, the `recording` field, `--stage`, a Hub-sourced
`docker/Dockerfile`, and the four documentation updates. Five PRs.

## Completion criteria

A wheel built from `main`, installed in a venv outside the workspace tree, serves
the app and the API on `http://localhost:8000` from `quantik-models-play` alone —
demonstrated, with the transcript, not asserted.

## Handoff path

Create `tasks/active/QW-030-playground-monolith-and-play-ux/handoffs/` only once a
handoff exists.
