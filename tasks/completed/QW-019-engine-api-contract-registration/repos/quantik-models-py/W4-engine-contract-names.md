# W4 — `quantik-models-py` play service speaks the registered names

**Repository:** `quantik-models-py` · **Branch:** `feat/engine-contract-names` · one PR
**Depends on:** W1 merged.

The play service is the third independent implementation of this wire format
(`decisions.md#D4`). Same rename, same one-cycle acceptance of the old spelling
(`decisions.md#D3`).

**Do not touch `src/quantik_models/play/app/` in this item.** That tree is a vendored copy of the
visualizer and is re-synced by W5, after W3 lands. Editing it here creates a conflict with the
sync and a copy that no longer matches its recorded source commit.

## Steps

1. `src/quantik_models/play/service.py` (~lines 33-34) — `REQUEST_SCHEMA = "engine-request.v1"`,
   `RESPONSE_SCHEMA = "engine-response.v1"`. Add
   `LEGACY_REQUEST_SCHEMA = "quantik.engine-request.v1"` with a comment naming `decisions.md#D3`.
2. `src/quantik_models/play/service.py` — the request-validation path accepts either spelling.
   The module docstring (~lines 4-5) names both contracts; update it to the bare names.
3. `src/quantik_models/play/server.py` (~line 49) — the endpoint description string still reads
   `"quantik.engine-request.v1 in, quantik.engine-response.v1 out"`. Update it. This string is
   served from `/api`, so it is user-visible documentation, not a comment.
4. `tests/test_play_service.py` — add: a request with the legacy spelling is accepted; a request
   with an unknown schema is rejected with the existing status; the response dict's `schema` is
   exactly `"engine-response.v1"`.
5. **Schema validation (`decisions.md#D4`).** Add a test that validates one real service response
   against `../quantik-core-contracts/schemas/engine-response-v1.json`, skipping with a clear
   message when that path is absent. Note the service emits `win_probability` where the Rust API
   emits `value`; W1's schema accepts both as optional, so this must pass unchanged.

## Completion criteria

```sh
python -m pytest -q
python -m mypy
grep -rn "quantik\.engine-" src/quantik_models/ --include="*.py"
```

- Both suites clean; report the actual counts.
- The grep returns only the `LEGACY_REQUEST_SCHEMA` constant and its comment. Any other hit in a
  `.py` file is a miss. Hits under `play/app/` are expected and belong to W5.

## Handoff

Record commands, counts, and the exact grep output.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md` and `README.md`. Repository
instructions win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
