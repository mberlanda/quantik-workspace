# W1 — Register `engine-request.v1` and `engine-response.v1`

**Repository:** `quantik-core-contracts` · **Branch:** `feat/register-engine-contracts` · one PR

Two contracts are enforced in production but exist nowhere in the registry: `quantik-api-rust`
rejects any request whose `schema` field does not match a Rust `const`, and nothing keeps that
const in agreement with the JS literal or the Python service. This item makes them real. It is the
prerequisite for W2, W3 and W4, and for QW-018.

Register them under the **bare** names per `decisions.md#D3`, as a **JSON Schema 2020-12 pair**
per `decisions.md#D2`.

## The format, as actually spoken today

Read these three before writing the schemas; they are the specification:

- `quantik-api-rust/src/lib.rs` — `MoveRequest` / `MoveResponse` / `SearchConfig` structs
  (~lines 75-101), and `validate_request` (~line 118).
- `quantik-qfen-visualizer/src/engines.js` (~line 54) — the request the browser actually sends.
- `quantik-models-py/src/quantik_models/play/service.py` (~lines 33-34, 285-300) — the third
  implementation, and its response dict.

Observed request fields: `schema`, `qfen`, `side_to_move`, `legal_action_indices`, and an
optional `config` object (`max_depth`, `time_limit_ms`, `iterations`, `beam_width`, `rollouts`,
`seed`, each optional).

Observed response fields: `schema`, `action_index`, `engine_kind`, `engine_version`, `elapsed_ms`,
and optional extras that **differ between implementations** — Rust emits `value`, the Python
service also emits `win_probability`. Accept the union, mark both optional, and say in the docs
which implementation emits which. Do not change either implementation here — `decisions.md#D5`.

`action_index` is `0..=63` and `legal_action_indices` entries are `0..=63`
(`context/system/canonical-invariants.md#I6`). `side_to_move` is `0` or `1`.

## Steps

1. `schemas/engine-request-v1.json` and `schemas/engine-response-v1.json` — JSON Schema 2020-12
   (`"$schema": "https://json-schema.org/draft/2020-12/schema"`). Match the style of
   `schemas/observation-v1.json`. Required fields exactly as observed; `additionalProperties:
   false` on the top level so an unknown field is a test failure rather than a silent pass.
   `schema` is `const` the bare name.
2. `docs/engine-request-v1.md` and `docs/engine-response-v1.md` — follow
   `docs/search-summary-v1.md` for structure. State the three implementations by path, the
   optional-field divergence, and the `decisions.md#D3` rename migration.
3. `fixtures/engine-request/*.jsonl` and `fixtures/engine-response/*.jsonl` — JSONL, one payload
   per line, matching the existing `fixtures/search-summary/` layout. **Captured, not invented:**
   at least one real request from the visualizer, and one real response from each engine kind the
   Rust API serves plus one from the Python service. Include a request that carries `config` and
   one that omits it.
4. `contracts.json` — add two entries beside the existing fourteen:
   `{"id": "engine-request.v1", "major": 1, "schema": "schemas/engine-request-v1.json",
   "docs": "docs/engine-request-v1.md", "fixture_glob": "fixtures/engine-request/*.jsonl"}`
   and the response equivalent. Key them `engine_request` / `engine_response`, matching the
   underscore style of the existing keys.

## Completion criteria

```sh
# from the quantik-core-contracts checkout
python -m pytest -q                       # the repository's own suite
# from the quantik-workspace checkout
quantik-workspace validate contracts
quantik-workspace validate fixtures
```

- `validate contracts` lists `engine-request.v1` and `engine-response.v1` with non-null `schema`.
- `validate fixtures` reports `status: ok` and a non-zero checked count for both new globs — a
  glob that matches nothing passes vacuously, so confirm the count moved.
- Every captured fixture row validates. If a real captured payload does not validate, the schema
  is wrong, not the payload.
- `contracts.json` still validates against `schemas/contracts-manifest-v1.schema.json`.

## Handoff

Record the exact commands, the fixture counts before and after, and where each captured payload
came from (which engine, which client).

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md` and `README.md`. Repository
instructions win over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, the exact commands you
ran and their real output, and anything you could not finish.
