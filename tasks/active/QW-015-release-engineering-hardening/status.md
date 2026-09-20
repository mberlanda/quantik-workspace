# QW-015 Status

**not-started.** Nothing implemented.

Re-verified 2026-08-30 — the defect is still live:

- `quantik-core-contracts/scripts/validate_opening_book_summary.py:118` — the returned
  dict carries `contract_version`.
- same file, line 142 — `if rust_summary != python_summary: fail(...)`.
- `quantik-core-contracts/actions/opening-book-consistency/action.yml:23` —
  `default: "1.2.0"`.

Next action: acceptance criterion 1. It is a small diff in one file plus a test, and it
is the whole deadlock.

Full history: [`workstreams-archive.md`](../../../docs/history/workstreams-archive.md) §2.

## 2026-09-20 — W8 and W9 in review

Both portability adapters now run bare, which is what `workspace.yaml` declares:

- W8 [quantik-core-py#49](https://github.com/mberlanda/quantik-core-py/pull/49) — `--contracts-root` defaults
  to the sibling checkout (worktree-aware), `--output` defaults to stdout; 839 passed locally.
- W9 [quantik-core-rust#43](https://github.com/mberlanda/quantik-core-rust/pull/43) — the same defaults;
  fmt, clippy `-D warnings` and tests green.

Packet correction: W9's `allowed_paths` named `portability_report.rs`, which does not exist; the binary is
`quantik-portability-report.rs`. Fixed in the manifest.

Next after both merge: regenerate the compatibility matrix and check that it can finally report `supported`.
