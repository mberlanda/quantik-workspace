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
