# W2 — `quantik-api-rust` speaks the registered names

**Repository:** `quantik-api-rust` · **Branch:** `feat/engine-contract-names` · one PR
**Depends on:** W1 merged (the schema files must exist to validate against).

Rename the two consts to the registered bare names, accept the old spelling on input for one
minor cycle, and validate against the registered schema in this repository's own tests
(`decisions.md#D3`, `decisions.md#D4`).

## Steps

1. `src/lib.rs` — `REQUEST_SCHEMA` and `RESPONSE_SCHEMA` (~lines 23-24) become
   `"engine-request.v1"` and `"engine-response.v1"`.
2. `src/lib.rs` — add `pub const REQUEST_SCHEMA_LEGACY: &str = "quantik.engine-request.v1";`
   with a comment naming `decisions.md#D3` and the fact that it is removed at the next minor.
3. `src/lib.rs` — `validate_request` (~line 118) accepts `REQUEST_SCHEMA` **or**
   `REQUEST_SCHEMA_LEGACY`. Update the rejection message to name the accepted spelling only:
   the legacy form is tolerated, not advertised.
4. `src/lib.rs` — the response is unchanged in shape and now carries the bare name automatically
   through `RESPONSE_SCHEMA`.
5. `src/lib.rs`, `mod tests` (~line 294) — the two existing tests that post `REQUEST_SCHEMA`
   keep passing. Add:
   - a test posting `REQUEST_SCHEMA_LEGACY` that expects `200`;
   - a test posting `"engine-request.v2"` that expects the existing rejection status;
   - a test asserting the serialized response's `schema` field is exactly `"engine-response.v1"`.
6. **Schema validation (`decisions.md#D4`).** Add a dev-dependency on a JSON Schema validator
   (`jsonschema` is already in the ecosystem; pin an exact version in `Cargo.toml` under
   `[dev-dependencies]`) and a test that validates one serialized `MoveResponse` against
   `../quantik-core-contracts/schemas/engine-response-v1.json`. Skip the test with a clear
   message if that path does not exist, so a standalone checkout still builds.

## Completion criteria

```sh
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

All three clean. The new tests fail if you revert step 3, and the schema-validation test fails if
you change a response field name — check both by actually reverting, then restoring.

## Handoff

Record the commands and their real output, and the exact validator crate and version you pinned.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md` and `README.md`. Repository
instructions win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
