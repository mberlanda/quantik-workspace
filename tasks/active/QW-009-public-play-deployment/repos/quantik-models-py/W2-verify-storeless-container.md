# W2 — Prove `--no-store` survives inside the container

**Repository:** `quantik-models-py` · **Branch:** `docs/verify-storeless-container` · one PR
**Depends on:** W1 merged. **Dispatch:** execute and record.

Acceptance criterion 4 of this initiative is that `--no-store` behaviour is preserved *inside the
container*: no database is opened, and `POST /api/games` answers 503. It has been asserted but
never demonstrated against a built image — and the whole point of the public deployment is that a
visitor never sees a storage error.

## Steps

1. Build the image locally: `scripts/build_docker_image.sh` (read it first; it may need a Hub
   token for the weights pull).
2. Run it storeless, on a free port.
3. Record an actual transcript:
   - `GET /` returns HTML containing the app title;
   - `GET /api` returns JSON, and its recording-capability field reports that the server has no
     store;
   - `POST /api/games` returns **503**;
   - no database file exists inside the container afterwards
     (`docker exec … ls` on the expected path, or the equivalent).
4. Add the transcript to `docs/play-service.md` under a heading that names the image digest you
   tested, not just the tag — a tag moves, a digest does not.
5. If any step fails, that is the finding. Report it in the handoff and do not edit application
   code to make it pass; that would be a different work item.

## Completion criteria

- `docs/play-service.md` contains the transcript with the image digest.
- The 503 and the absent database file are both shown as real command output, not described.
- `python -m pytest -q` and `python -m mypy` clean.

## Handoff

Record the image digest, every command, and its real output.

## Execution contract

**Read first:** the repository's own `AGENTS.md` and `DEVELOPMENT.md`. Repository instructions
win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.
Before the PR run `python -m pytest -q` and `python -m mypy`, and report the real counts.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
