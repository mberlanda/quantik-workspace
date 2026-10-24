# QW-019 Status

**not-started.**

Verified 2026-08-30:

- `quantik-api-rust/src/lib.rs:22` — the Rust `const`.
- `quantik-qfen-visualizer/src/engines.js:54` — the JS literal.
- Neither string appears in `quantik-core-contracts/contracts.json` or `schemas/`.

Blocks [`QW-018`](../QW-018-engine-response-type/initiative.md).

Next action: register the request schema with a fixture from a real visualizer request.
The response schema follows and is where QW-018's fields land.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §7.

## 2026-09-20 — W1 in review

W1 is `in-review`: [quantik-core-contracts#24](https://github.com/mberlanda/quantik-core-contracts/pull/24)
registers `engine-request.v1` / `engine-response.v1` (schemas, docs, captured fixtures: 6 request rows,
13 response rows) and teaches `scripts/validate_contracts.py` to validate them. 54 tests pass (44 + 10);
with the dispatch disabled 11 fail, restored 54 pass.

Coordinator decisions taken during W1 (the packet was wrong or silent on these):

- **`allowed_paths` widened** to `scripts/validate_contracts.py` and `tests/test_contracts_validator.py`.
  The script routes every non-`search-summary` row to the self-play validator, so registering the contracts
  without a dispatch left contracts `main` red; it could not be a separate item.
- **Captured fixtures carry the bare `schema` name.** Both live servers still accept and emit only the
  prefixed `quantik.engine-*.v1` (the D3 migration is W2/W4). The only edit to a captured payload is that
  one field; the docs say so.
- **The request schema keeps `const` of the bare name**; D3's accept-both window is server behaviour during
  migration, not a property of the payload schema.
- **The Python play service emits `value` and `policy`, not `win_probability`** (which belongs to the separate
  `quantik-play.analysis.v1`). D5 stands: the schema accepts the union; reconciling is QW-018's.
- `quantik-workspace validate fixtures` does not validate payloads against their schema (only that `schema`
  is a string and `contract_version` matches); the rows were checked with `jsonschema` 2020-12 instead.
  A gap worth its own item.

W2-W5 wait on the merge.

**W1 merged** — [#24](https://github.com/mberlanda/quantik-core-contracts/pull/24). Advisor review of the schema/fixtures found no defect; the real `jsonschema` 2020-12 validator accepts all 6 request and 13 response rows. W2-W5 are now ready.

## 2026-09-20 — W2, W3, W4 merged

- W2 [api-rust#2](https://github.com/mberlanda/quantik-api-rust/pull/2), W3
  [visualizer#14](https://github.com/mberlanda/quantik-qfen-visualizer/pull/14), W4
  [models-py#71](https://github.com/mberlanda/quantik-models-py/pull/71). Merged in that order, because the old
  gateway rejects the bare request name. Each accepts the legacy `quantik.engine-request.v1` for one minor cycle (D3)
  and never emits it. api-rust and models-py validate responses against the registered schema in their own tests (D4).
- **W4 `allowed_paths` widened** to `tests/test_play_server.py`: an existing assertion pinned the old response name.
- The W2 packet named start revision `f814093`, but `origin/main` was `043b544`. The packets can go stale.
- Bundle assumptions that were wrong: the models-py move response has no `win_probability` (it emits `value` and
  `policy`), the local contracts checkout was stale, `jsonschema` is not a models-py dependency, and mypy is not
  in its CI.

Follow-ups, none blocking:

- No test validates a *request* against `engine-request-v1.json`. The legacy spelling is not a valid instance of the
  schema, so that asymmetry is deliberate (D3) but untested.
- models-py: `jsonschema` is not in the dev extras and CI does not clone contracts, so the D4 schema test skips there.
  The api-rust contract test panics on a missing checkout unless `QUANTIK_SKIP_CONTRACT_TESTS=1`.
- `quantik-qfen-visualizer/README.md:72` still shows the old request name. Fold into W5.
- api-rust `Cargo.lock` records `quantik-core` as 1.3.0 (sibling drift). Fold into the QW-020 `CORE_REV` sync item.

W5 is now ready.

## 2026-09-20 — W5 merged

[models-py#72](https://github.com/mberlanda/quantik-models-py/pull/72) re-vendored the visualizer via
`scripts/sync_visualizer.py` (`SOURCE.json` now records visualizer `9f21762`, #14); no hand edits under `app/`.
The local visualizer checkout was behind, so the sync ran from a fresh worktree of `origin/main`.

Left over, outside W5's `allowed_paths`:

- `quantik-qfen-visualizer/README.md:72` still shows `quantik.engine-request.v1` (a one-line fix in that repo).
- The OpenAPI 3.1 document is a separate contracts item (D2).

All five QW-019 items are `completed`; QW-018 is unblocked.
