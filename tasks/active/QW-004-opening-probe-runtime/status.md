

## 2026-09-20 — W3 merged

[core-rust#44](https://github.com/mberlanda/quantik-core-rust/pull/44) adds `SymmetryHandler::find_canonical_with_transform` (lowest `transform_index` on ties; `find_canonical` now delegates to it), `opening_probe.rs` (sorted 28-byte records, bytewise binary search, inverse-transform mapping, fail-fast errors, a legality tripwire that is a plain check so it is live in release builds) and a `probe_builder` bin. `allowed_paths` widened to `symmetry.rs` and `lib.rs`. Mutation checks: using `t*` instead of its inverse fails 6 tests, inverting the tie-break fails 4. Python-built probe files for the 5 valid fixture rows open in Rust and re-encode byte for byte. core-rust CI (fmt, clippy, test) passed on the merged head; CI clippy is newer than a pinned local toolchain (`chunks_exact` lint), which is why it caught what the agent's first run did not.

- **Fixture tests do not run in core-rust CI**: `rust.yml` checks out only this repo, so the two contracts-fixture tests skip as no-ops. The exact step (a contracts checkout plus `QUANTIK_CONTRACTS_DIR` and `QUANTIK_REQUIRE_FIXTURES=1`) is proposed in the PR body and not applied (outside `allowed_paths`). Until it lands, W4's cross-produced evidence is local only.
- **Judgment calls the paper left open, decided in W3** (W4 builds against them): no `verify=false` opt-out (checksum and sortedness always run); padding bytes are not checked; the builder derives `source_book.book_id` as SHA-256 over the projected rows because the Rust book has no `book_id` column (`--book-id` overrides); `coverage_complete` is true only when the book had no unsolved rows. These should be folded into `docs/opening-probe-v1.md`.
- **No owner yet:** the quantik-core-py analogue of `find_canonical_with_transform` (the packet's Python side). Same shape as the QW-018 core-accessor gap.
- `corrupt-action-above-63` is unchecked in Rust: the binary format cannot express it (action 64 does not fit a 64-bit set).
