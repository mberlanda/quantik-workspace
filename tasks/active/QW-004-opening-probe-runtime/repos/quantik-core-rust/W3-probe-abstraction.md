# W3 — Rust probe abstraction, fail-fast and orientation-correct

**Repository:** `quantik-core-rust` · **Branch:** `feat/opening-probe` · one PR
**Depends on:** W2 merged. **Dispatch:** mechanical, but the orientation logic deserves care.

Implement the probe against the registered contract. `docs/opening-probe-v1.md` in
`quantik-core-contracts` is the specification; this repository does not get to reinterpret it.

## Steps

1. `crates/quantik-core/src/opening_probe.rs` — loading, lookup, and the transform back into the
   caller's orientation per W1 section 3.
2. Fail fast on corrupt data, truncated files and incompatible versions, exactly as W1 section 5
   assigns. A miss is an ordinary `None`; corruption is an error. Do not collapse the two.
3. `crates/quantik-core/src/bin/probe_builder.rs` — build a probe from an existing opening book.
4. `crates/quantik-core/src/opening_book.rs` — only if W1 section 6 requires it.
5. `crates/quantik-core/tests/opening_probe.rs` — one test per registered fixture case: hit, miss,
   corrupt, incompatible version, **transformed move**. The transformed-move test must fail if you
   delete the inverse transform — verify by actually deleting it, watching it fail, then restoring.
   That is the check that catches the silent-wrong-move failure this contract exists to prevent.

## Completion criteria

```sh
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

All clean. Tests read the contracts fixtures from `../quantik-core-contracts/fixtures/opening-probe/`,
skipping with a clear message if that path is absent so a standalone checkout still builds.

## Handoff

Record the commands, the delete-the-transform check, and any place the contract was ambiguous.

## Execution contract

**Read first:** the repository's own `AGENTS.md`/`CONTRIBUTING.md`. Repository instructions win
over anything here.

One logical change per commit, one PR for this work item, `main` left green. Edit only the
`allowed_paths` this item declares in `manifest.yaml`; widening scope needs coordinator review.

Record in the handoff: item ID, branch, PR, starting and final revision, exact commands and their
real output, and anything you could not finish.
