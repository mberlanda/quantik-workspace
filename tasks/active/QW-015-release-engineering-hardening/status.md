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
