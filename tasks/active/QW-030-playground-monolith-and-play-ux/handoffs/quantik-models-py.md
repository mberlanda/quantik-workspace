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
