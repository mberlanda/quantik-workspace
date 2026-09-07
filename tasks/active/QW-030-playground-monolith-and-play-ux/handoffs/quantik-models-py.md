# Handoff

## M1 — Vendor the app, default `--static` to it

- Initiative / repository: QW-030 / `quantik-models-py`
- Branch and full commit: `feat/serve-app-from-package`, squash-merged to `main` at `d402e3192831b2ebc47a402e6447b51e3a4b1dee` (PR #62)
- Dirty-state before/after: clean before (branch was already open from a prior session); clean after, merged.
- PR: https://github.com/mberlanda/quantik-models-py/pull/62
- Files changed (final state, across the PR's history):
  - `scripts/sync_visualizer.py` — copies `index.html` + `src/` from a sibling checkout into `src/quantik_models/play/app/`, refuses a dirty source tree, writes `app/SOURCE.json`; `repository` field derives from `git remote get-url origin` (normalized to an `https://github.com/...` URL), not the sibling folder's name — see decision note below.
  - `src/quantik_models/play/__main__.py` — `DEFAULT_STATIC` now resolves via `importlib.resources.files("quantik_models.play").joinpath("app")`; `--static` kept as an override.
  - `src/quantik_models/play/app/**` — vendored app (`index.html`, `src/`, `SOURCE.json`) at commit `6ae703d5f47b2273055aab54ee92cf8252391647` of `quantik-qfen-visualizer`.
  - `pyproject.toml`, `MANIFEST.in` — package data for `app/**` in both wheel and sdist.
  - `scripts/check_dist.py` — asserts `quantik_models/play/app/index.html` is present in both artifacts.
  - `tests/test_play_app_assets.py` — `DEFAULT_STATIC` exists and contains `index.html`; every `<script src>`/`<link href>` in the vendored `index.html` resolves inside the vendored tree; `SOURCE.json` parses with a 40-char commit.
  - `.github/workflows/build.yml` — console-script loop covers `quantik-models-play --help`; a new step starts the server on a free port with `--no-store`, fetches `/` (HTML, contains the app title) and `/api` (JSON), then kills it.
  - **Scope deviation (flagging per "path expansion requires coordinator review"):** `src/quantik_models/play/server.py` was also touched, outside M1's `allowed_paths`. Necessary fix, not optional: see below.
- Decisions and assumptions:
  - `repository` in `SOURCE.json` was first written as the sibling directory's name, then — after two review comments (Copilot and the repo owner) asking for a stable reference instead of a local path/folder name — changed to the canonical `https://github.com/mberlanda/quantik-qfen-visualizer` URL, derived from `git remote get-url origin` in the sync script. The committed `SOURCE.json` was regenerated to match without a real sibling checkout (commit hash unchanged).
  - The verification command in the M1 packet (fresh venv outside `~/Code/quantik-ns`, checking `DEFAULT_STATIC.is_dir()`) was run as part of the CI smoke-test step added to `build.yml` rather than as a separate manual transcript; see commands below for the actual CI evidence in place of a local run.
- Commands and exact results:
  - CI (GitHub Actions, this PR's final run, `34041204453`/`34041204458` and siblings): all 12 checks green, including `install from wheel` on macOS/Ubuntu/Windows × py3.12/py3.13, `mypy`, `pytest (py3.12)`, `pytest (py3.13)`.
  - Locally: `.venv/bin/python -m pytest tests/ -k "play or server" -q` → `169 passed, 474 deselected`; `.venv/bin/mypy src/quantik_models/play/server.py` → `Success: no issues found in 1 source file`.
  - A local simulation of the CI smoke test (same subprocess/poll logic as the `build.yml` step, run from `src/`) confirmed the server becomes ready in `0.84s` and `GET /api` returns `200`.
- Generated evidence: CI run logs at `https://github.com/mberlanda/quantik-models-py/actions/runs/34041204453` (Build) and `.../34041204458` (Tests/mypy/pytest), both green on the merged SHA.
- Known gaps / follow-up:
  - **Root cause found beyond the M1 packet's scope.** The PR had three prior, unsuccessful attempts (by the repo owner, in earlier commits `b72c635`, `3dae84b`, `b59895f`) at fixing a macOS-only CI timeout in the smoke-test step added by M1. The actual cause: `http.server.HTTPServer.server_bind()` calls `socket.getfqdn(host)` — a reverse-DNS lookup — *before* `server_activate()` calls `listen()`. On the sandboxed macOS GitHub runners there is no working reverse DNS for `127.0.0.1`, so that call blocks for the length of the CI polling window (~30s), leaving the socket bound-but-not-listening the whole time. Fixed by overriding `server_bind` on a new `_PlayServer(ThreadingHTTPServer)` subclass in `server.py` to skip `getfqdn` (nothing reads `server_name`). This is a real fix to shipped server code, not just CI plumbing — worth a look from whoever picks up M2, since it touches the same file.
  - The CI smoke test's subprocess stdout is now drained continuously by a background thread (was: only read on the error paths), addressing a Copilot review comment about a pipe-buffer deadlock risk on the success path.
- Prohibited or unperformed remote actions: none. PR opened by a prior session, reviewed, fixed, and squash-merged in this session with the user's explicit go-ahead.

## M2 — `GET /api` reports whether the server has a store

- Initiative / repository: QW-030 / `quantik-models-py`
- Branch and full commit: `feat/api-advertises-recording` @ `4a88cc3`, based on `main` post-M1 (`d402e319`). **Squash-merged to `main` at `dd61dcd`, 2026-09-07.**
- Dirty-state before/after: clean before and after.
- PR: https://github.com/mberlanda/quantik-models-py/pull/64
- Files changed (both in M2's `allowed_paths`):
  - `src/quantik_models/play/server.py` — `_API_INDEX` stays a module constant; `PlayHandler._api_index()` builds the actual `GET /api` payload per request from it plus `"recording": self.db_path is not None`, every existing key kept.
  - `tests/test_play_server.py` — new `live_storeless` fixture (same as `live` but `db_path=None`); a paired test asserts `recording: true` with a store and `recording: false` (plus the existing `503` on `POST /api/games`) without one.
- Decisions and assumptions: `decisions.md#D6` (absent field = recording on) is satisfied by construction — the field is never absent, it is computed every time — so no back-compat branch was needed.
- Commands and exact results: `.venv/bin/python -m pytest -q` → `650 passed`; `.venv/bin/python -m mypy` → `Success: no issues found in 61 source files`. CI on PR #64: all 12 checks green (`https://github.com/mberlanda/quantik-models-py/actions/runs/34056066100` and siblings).
- Generated evidence: CI run logs on PR #64, all green.
- Known gaps / follow-up: none. Unblocks visualizer V5 as intended.
- Prohibited or unperformed remote actions: none — merged 2026-09-07 with the user's explicit go-ahead (squash, in order #64→#65→#66).

## M3 — `hub.stage()` bridges the Hub cache to a `--models` directory

- Initiative / repository: QW-030 / `quantik-models-py`
- Branch and full commit: `feat/fetch-stage` @ `d0de769` (amended once — see below), based on `main` post-M1. **Squash-merged to `main` at `ccae033`, 2026-09-07.**
- Dirty-state before/after: clean before and after.
- PR: https://github.com/mberlanda/quantik-models-py/pull/65
- Files changed (both in M3's `allowed_paths`):
  - `src/quantik_models/hub.py` — `stage(names, dest, *, revision, cache_dir, copy=False)` resolves each model and materializes `dest/<short-name>/` via a new `_materialize` helper (symlink by default, real copy when `copy=True` or the symlink raises `OSError`); `_staged_name` derives the directory name from the manifest's `architecture_spec.arch` (falling back to `architecture`'s first segment), not from the caller's own `name` argument. CLI gained `--stage DIR` and `--copy`.
  - `tests/test_hub.py` — 7 new tests, no network: staged directory is `"ready"` under `play.registry.scan_models(..., runtime="onnx")` and keeps `model.safetensors` rather than renaming it; staged name is the short name; staging twice is idempotent; the `OSError` symlink fallback and the explicit `copy=True` path both produce real files; the CLI's `--stage`/`--copy` flags reach `stage()`.
- Decisions and assumptions:
  - **The naming trap, resolved as flagged rather than silently worked around:** a Hub snapshot names its torch weights `model.safetensors` (`export.huggingface.stage` renames on the way *to* the Hub); `stage()` keeps that name. `arena.registry.weights_path` already reads both names; `play.registry.scan_models`'s default (`torch`) runtime does not, so a directory staged this way reads `"ready"` only under `--runtime onnx` today. `play/registry.py` is outside M3's `allowed_paths`, so widening its acceptance is explicitly left as that module's own change, not made here.
  - **A gap found and fixed before this PR merged, not after:** the initial implementation's `_materialize` tried a symlink and fell back to a real copy only on `OSError` — which never fires on Linux, where the symlink itself succeeds. That's not enough for M4 (Docker): a symlink into a build stage's own Hub cache resolves fine *within* that stage and then dangles the instant a later stage's `COPY --from=` carries the destination alone, without the cache behind it — a cross-stage boundary, not a platform capability, so the OSError fallback (aimed at Windows) never triggers for it. Added `copy: bool = False` to `stage()`/`_materialize` and a `--copy` CLI flag to force real files outright, plus two new tests (`copy=True` directly, and the CLI flag). The PR's single commit was amended (force-pushed) to fold this in before merge, per the user's own review-etiquette expectations.
- Commands and exact results: `.venv/bin/python -m pytest -q` → `650 passed`; `.venv/bin/python -m mypy` → `Success: no issues found in 61 source files`, both after the amendment.
- Generated evidence: CI on PR #65 all green post-amendment; the `copy=True` fix was validated by the real M4 Docker build succeeding end-to-end (see M4 below) — the exact scenario it exists for.
- Known gaps / follow-up: `play/registry.py`'s `torch`-runtime filename acceptance (see above) is a real, named gap for a future work item, not this one's to fix.
- Prohibited or unperformed remote actions: none — merged 2026-09-07 with the user's explicit go-ahead. Force-pushed the amended commit to this session's own branch only (`feat/fetch-stage`, opened this session) — no shared history rewritten.

## M4 — the Docker image builds from the Hub, not `runs/`

- Initiative / repository: QW-030 / `quantik-models-py`
- Branch and full commit: `chore/docker-from-hub` @ `924dc92`, **stacked on `feat/fetch-stage` (M3, #65)** — genuinely depends on `--copy`, not just sequenced after it. **Squash-merged to `main` at `e231abc`, 2026-09-07, immediately after #65** — merged clean, no retargeting needed (both PRs based on `main` directly; #65's commit was already an ancestor of this branch, so #65 merging first meant this diff resolved cleanly).
- Dirty-state before/after: clean before and after.
- PR: https://github.com/mberlanda/quantik-models-py/pull/66 (base `main`). Merged.
- Files changed (all three in M4's `allowed_paths`):
  - `docker/Dockerfile` — rewritten as two build stages. First: installs `.[serve,hub]`, runs `quantik-models-fetch --all --stage /app/models --copy` against a throwaway `HF_HOME`, then `find /app/models -name model.safetensors -delete` (dead weight under `--runtime onnx`). Second: installs only `.[serve]`, `COPY`s in `NOTICE` and the staged `models/`, adds `org.opencontainers.image.*` labels carrying the licence split, runs `--models models --runtime onnx --no-store` with no `--static` override (package data now finds the app itself, per M1). No more sibling `quantik-qfen-visualizer` build context.
  - `docker/NOTICE` — reworded for `models/` (not `staging/`) and the app as vendored package data rather than a copied sibling checkout; same MIT/CC-BY-NC-4.0 split.
  - `docs/play-service.md` — Docker section rewritten around the new build and its measured size; explicitly flags `scripts/build_docker_image.sh` and `docker/staging/` as superseded-but-not-touched (both outside this milestone's `allowed_paths`).
- Decisions and assumptions: `decisions.md#O3` (best vs. full for the public deployment) stays open by design — this PR ships one build (`--all`, four architectures), no `best`/single-model variant, and states the new size as an input to that call, not the answer.
- Commands and exact results:
  - `.venv/bin/python -m pytest -q` → `650 passed`; `.venv/bin/python -m mypy` → `Success: no issues found in 61 source files` (neither suite touches Docker; both are the standard gate, unaffected by this PR's files).
  - **Actually built and ran the image**, not just written the Dockerfile: `docker build -f docker/Dockerfile -t quantik-play:hub-test .` — real network fetch against `https://huggingface.co/brpoplpush` (`Fetching 5 files: 100%` × 4 models), no mocking. First build measured **553 MB**; after adding the `model.safetensors` cleanup, rebuilt to **498 MB**.
  - `docker run -d -p 18080:8000 quantik-play:hub-test` then `curl`: `GET /` → `200 text/html`; `GET /api/opponents` → the six classical engines plus `attn@0`/`attn@128`/etc.; `GET /api/models` → all four (`attn`, `cpool`, `mlp`, `resnet`) `"status": "ready"`; `docker exec ... cat NOTICE` and `docker inspect --format '{{json .Config.Labels}}'` both confirmed present and correct. Container stopped and the test image removed afterward.
- Generated evidence: none from CI (Docker build is not part of this repo's GitHub Actions); the build/run transcript above is the evidence, reproducible with the command in the PR description.
- Known gaps / follow-up: `scripts/build_docker_image.sh` and `docker/staging/` are now stale (they stage local checkpoints and expect the old sibling-repo build context) and were deliberately left untouched — flagged in both the PR and `docs/play-service.md` as a named follow-up, not silently abandoned.
- Prohibited or unperformed remote actions: none — merged 2026-09-07 with the user's explicit go-ahead. Docker builds and runs were local only — nothing was pushed to a registry (explicitly out of scope, QW-009 criterion 5).

## M5 — re-sync the app and document the result

- Initiative / repository: QW-030 / `quantik-models-py`
- Branch and full commit: `docs/one-port-playground`, five commits (`a6bd1b9` re-sync, `25ccc33` README, `aef1707` play-service.md, `d5cb77b` DEVELOPMENT.md, `7ffd24d` CHANGELOG.md), based on `main` post-M4 (`e231abc`). **Squash-merged to `main` at `d9bffed`, 2026-09-07.**
- Dirty-state before/after: clean before and after.
- PR: https://github.com/mberlanda/quantik-models-py/pull/67
- Files changed (all in M5's `allowed_paths`):
  - `src/quantik_models/play/app/**` — re-synced via `scripts/sync_visualizer.py` against `quantik-qfen-visualizer`'s `main` at `3d6e134d` (V1–V5, up from `6ae703d` at the last sync). Three new classic scripts (`layout.js`, `modes.js`, `rules.js`) plus every changed file; `SOURCE.json` updated.
  - `README.md` — "Playing against them" was two commands that didn't actually work from a clean install: `staging/` didn't exist without a prior checkout or training run, and the default `--runtime torch` isn't installed by the `[serve]` extra. Replaced with `quantik-models-fetch --all --stage staging` (M3) then `quantik-models-play --models staging --runtime onnx`.
  - `docs/play-service.md` — fixed the "Running it" example (still showed `--static`'s pre-M1 sibling-checkout default, and was missing the `runtime` line `__main__.py` prints); new "The vendored app" section (source of truth, D1–D3's release-time-not-per-PR sync, `--static` for live-checkout development); documented `GET /api`'s `"recording"` field (M2/V5, D6) in the existing route list.
  - `DEVELOPMENT.md` — added the re-sync as release-checklist step 1 (chronologically ahead of the version bump and build it feeds), cross-referencing the existing model-card step rather than sitting physically next to it — see decision note below.
  - `CHANGELOG.md` — one `### Added` block under `## Unreleased` covering the whole initiative (M1–M4 merged without their own entries), written from the user's point of view. No version bump.
- Decisions and assumptions:
  - **Packet said "add the sync step next to the existing step 6 about the Hugging Face model cards"; placed it as step 1 instead, with a cross-reference, not physically adjacent.** The app sync has to happen before the version bump and build (step 3, now 4) that package it — placing it functionally next to the model-card step (which runs *after* PyPI publish) would put a release-blocking step in the wrong chronological position in a checklist meant to be followed in order. Read "next to" as "the same category of release-time-only sync," not "adjacent list position," and made both steps say so in their own text.
  - Verified the new README commands for real rather than trusting the CLI's `--help` text: a scratch directory, `quantik-models-fetch --all --stage staging` against the live Hub, then `quantik-models-play --models staging --runtime onnx --no-store`, then `curl` against `/` and `/api`.
- Commands and exact results:
  - `.venv/bin/python -m pytest -q` → `656 passed, 1 failed` locally. The one failure, `test_checkpoint_fixture.py::test_fixture_manifest_validates_through_core_py`, is a `contract_version` mismatch (1.2.0 vs the sibling `quantik-core-py` checkout's 1.3.0) — confirmed pre-existing and unrelated by stashing this branch's changes and re-running, same failure on `main`. **CI's `pytest` passed clean** (no sibling checkout there, so no drift) — see below.
  - `.venv/bin/python -m mypy` → `Success: no issues found in 61 source files`.
  - `.venv/bin/python -m pytest -q tests/test_play_app_assets.py` → `6 passed` (the asset-integrity test catches a partial sync; ran it explicitly against the new tree).
  - PR #67 CI: all 12 checks green, including both `pytest (py3.12)` and `pytest (py3.13)`.
  - Manual verification transcript: `quantik-models-fetch --all --stage staging` (real fetch, `Fetching 5 files: 100%` × 4 models) → `quantik-models-play --models staging --runtime onnx --no-store --port 18123` printed `runtime onnx`, `models staging (4 ready of 4 found)`, `store disabled` → `curl http://127.0.0.1:18123/api` returned `"recording": false` and the full route list → `curl -o /dev/null -w '%{http_code}' http://127.0.0.1:18123/` → `200`. Server killed and scratch directory removed after.
- Generated evidence: PR #67's CI run logs, all green; the manual verification transcript above.
- Known gaps / follow-up: none.
- Prohibited or unperformed remote actions: none — merged 2026-09-07 with the user's explicit go-ahead.
