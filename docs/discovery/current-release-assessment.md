# Current Release Assessment

## State observed

The release being prepared is contracts `1.2.0`. `quantik-core-contracts` and `quantik-core-rust` are clean `release/v1.2.0` checkouts. `quantik-core-py` has a local `release/v1.2.0` branch with uncommitted 1.2.0 changes and no upstream. `quantik-models-py` remains on clean `main` and embeds contracts 1.1.0.

The current stable contracts tag visible locally is `v1.1.0`; there is no `v1.2.0`. Therefore 1.2.0 is a candidate, not a published release.

## Producer version sources

| Occurrence | Value | Classification | Action |
| --- | --- | --- | --- |
| `quantik-core-contracts/VERSION` | `1.2.0` | authoritative version | retain |
| `contracts.json#/release_version` | `1.2.0` | required mirror | retain |
| `contracts.json#/status` | `draft` | candidate state | retain until release policy permits transition |
| schemas/fixtures/docs with 1.2.0 metadata | `1.2.0` | fixture metadata / source assertions | retain where tied to candidate artifacts |
| `.github/workflows/validate-contracts.yml` | `--expected-release 1.2.0` | candidate expectation | preferably derive from `VERSION` |
| `actions/opening-book-consistency/action.yml` default | `1.2.0` | action input default | verify in source mode |
| README / `docs/consistency-checks.md` external `@v1.2.0` | `v1.2.0` | published action reference | defer as “current stable”; mark candidate or keep `@v1.1.0` until publication |
| `docs/versioning.md` implementation/examples | `1.1.0` | documentation example with current-looking semantics | clarify as example or update after publication; do not blind replace |
| research-note 1.1.0 values | `1.1.0` | historical record | retain |

Source validation is green: 35 contracts tests and the full local validator passed. Candidate CI does not directly invoke the future tag, so there is no current producer circular dependency. However, it also does not exercise both candidate composite actions via relative paths. Add source-mode jobs using `./actions/cross-language-smoke` and `./actions/opening-book-consistency`, deriving the expected release from `VERSION`.

## Consumer drift

### Rust

Rust source/crate/fixtures declare 1.2.0, but `.github/workflows/rust.yml` uses `actions/opening-book-consistency@v1.1.0` and `expected-release: "1.1.0"`. Its generated summary is 1.2.0, so this is directly inconsistent. Changing only the ref to `@v1.2.0` now would create the forbidden unpublished-tag dependency. The candidate task should check out contracts source and invoke the relative action; the consumer publication task should pin `@v1.2.0` only after producer verification.

### Python

The committed Python source is 1.1.0; the dirty working tree is an in-progress 1.2.0 bump across package metadata, contract declaration, fixtures, tests, and docs. Its contracts workflow still uses 1.1.0 and advertises a `validate-contracts` action path that is absent from the contracts repository. Preserve these user changes and create a repository task to resolve the action path, source-mode candidate validation, and later exact published refs.

### Models

`src/quantik_models/export/checkpoint.py` and `tests/test_materialize.py` still embed 1.1.0, with no supported-contract declaration. CI checks out mutable sibling default branches. The models adoption task must update the checkpoint default and live fixtures/assertions, add an explicit declaration, pin verified inputs, and retain historical planning references.

## Changes that belong now versus later

Producer candidate work now:

- derive candidate expectations from `VERSION` where practical;
- run composite actions from checked-out relative paths;
- add release notes and a release-train record;
- distinguish “current stable v1.1.0” from “next planned 1.2.0” in public docs;
- validate that the tag will be exactly `v1.2.0` at the approved commit.

Wait until publication and producer verification:

- public examples that claim `@v1.2.0` is usable;
- Python/Rust/models exact action refs and supported-release adoption;
- compatibility matrix status `supported`;
- stable-release documentation and release locks.

## Recommended sequence

1. Create QREL-2026-001 in `planned` state with producer commit `beb26e7e07184b2fd61b9aef242358788400d861`.
2. Add/verify source-mode action tests without the future tag; keep release state `prepared` until green.
3. Resolve producer documentation timing and candidate assertions; validate candidate.
4. Record the approved producer commit, create immutable annotated `v1.2.0`, and publish separately.
5. Verify tag, GitHub Release, archive/checksum, and both external action paths; write a lock with tag and full SHA.
6. Execute repository-scoped Python and Rust adoption tasks; do not overwrite the current dirty Python checkout.
7. Execute models adoption and derived-data compatibility checks.
8. Update the evidence-backed matrix and complete the train only after required consumers are green.

Required work is represented in `releases/active/QREL-2026-001/` and `tasks/active/QW-001-canonical-game-state-and-action-encoding/`; no sibling file, tag, release, branch, or remote was changed.
