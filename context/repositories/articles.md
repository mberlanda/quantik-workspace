# articles Packet

> **Purpose:** drafts, figure-generation scripts, and generated images for the Quantik Substack series.
> **Load with:** [`quantik-models-py.md`](quantik-models-py.md) (the source of every plotted number), [`../system/repository-map.md`](../system/repository-map.md)

## Ownership

Owns article Markdown, figure generators (`make_figures.py`, `make_release_figures.py`, `make_preview.py`, `watermark.py`), a claims-verification script (`verify_claims.py`), and the committed `images/` and `fonts/` used to render them.

Does **not** own any run data. Every plotted figure is generated *from* `quantik-models-py/runs/` (gitignored) and cross-checked against it by `verify_claims.py`, so nothing here reproduces from a fresh clone of this repo alone — `quantik-models-py` must be checked out as a sibling with real run reports present.

## Toolchain (verified 2026-08-30)

No packaging file (no `pyproject.toml`/`requirements.txt`) — scripts run through `quantik-models-py`'s own virtualenv:

```sh
quantik-models-py/.venv/bin/python articles/make_figures.py       # Parts V/VI/VII figures, from run reports
quantik-models-py/.venv/bin/python articles/make_release_figures.py  # the-deadlock's diagram figures (12-15)
quantik-models-py/.venv/bin/python articles/verify_claims.py      # checks every quoted number against runs/
```

No test suite, no lint, no CI (`.github/workflows` does not exist, verified 2026-08-30 — matches WORKSTREAMS.md's "no CI" note). No `AGENTS.md`; `README.md` is the operating document — regeneration commands, the per-figure catalog, and the five-step Substack publishing checklist all live there. Don't restate the wordmark spec or publishing steps here; load the README.

## Publishing target

Substack, by manual copy-paste — there is no package or registry. The draft body (everything below the front matter) pastes directly; images upload separately at the `![...]` markers since Substack does not resolve relative paths.

## Conventions

No Markdown tables anywhere — Substack does not render them (`grep '^|' *.md` returns nothing in the drafts; this is enforced by convention, not tooling). Every figure carries the `THE FULL-STACK MIND` wordmark to an exact typographic spec — see `README.md`, not restated here.

## Git — confirms the workspace record (verified 2026-08-30)

**No git remote** (`git remote -v` is empty; `git ls-remote` fails with "No remote configured to list refs from") — matches WORKSTREAMS.md and the root `CLAUDE.md`. Local commits only, on one machine. `HEAD` `7d8b75b` (2026-08-27 22:59).

## Current state, 2026-08-30

Three "Season Two" drafts (`part-v-the-tournament.md`, `part-vi-the-apprentice.md`, `part-vii-the-audit.md`, ~1,900–2,050 words each) are already committed on local `main`, with `verify_claims.py` reporting **ALL CLAIMS VERIFIED**. **They are not mentioned anywhere in the workspace root `WORKSTREAMS.md`**, which tracks only the unrelated `the-deadlock.md` piece under workstream 3 — a tracking gap worth closing, not a contradiction to resolve by picking a side.

`the-deadlock.md` itself (workstream 3: draft complete, unpublished, ~2,750 words against a 1,750–2,050-word house length) is present but **not yet committed** — `git status` shows it and its four figures, plus `make_preview.py`/`make_release_figures.py`/`preview-the-deadlock.html`/`preview.css`, as untracked, and `README.md` as modified. Since there is no remote, an uncommitted draft here exists in exactly one place.
