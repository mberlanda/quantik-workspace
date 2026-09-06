# M1 — Vendor the app, default `--static` to it

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

## Execution contract

**Read before starting:** repository `AGENTS.md`, `DEVELOPMENT.md` invariants and release checklist. Base dependencies remain numpy + quantik-core; the app adds no dependency. Run `python -m pytest -q` and `python -m mypy` before the PR and report actual results.

**One logical change per commit. One PR for this work item. Do not stack
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

## Scope and handoff

Edit only the manifest allowed paths. Record exact starting and final revisions, branch, PR, commands and results, and dependency evidence in a work-item-specific handoff. Path expansion requires coordinator review.

Decision references: `decisions.md#D1`, `decisions.md#D2`, `decisions.md#D3`, `decisions.md#D5`.
