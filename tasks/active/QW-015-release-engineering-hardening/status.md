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

**W8 and W9 merged** — core-py [#49](https://github.com/mberlanda/quantik-core-py/pull/49), core-rust [#43](https://github.com/mberlanda/quantik-core-rust/pull/43). Review found both PRs under-tested (W9 had no tests; W8 covered only the error path and failed `codecov/patch`); tests were added to each before merge, and the W9 mutation check was made to actually fail. Next: regenerate the compatibility matrix and see whether it can report `supported`.

## 2026-09-20 — W1 was already done

The wave-3 agent found the fix already on contracts `main`: `normalize_summary` in
`scripts/validate_opening_book_summary.py` returns the structural summary and the contract version separately,
and `main()` compares only the structural part. It landed in
[#23](https://github.com/mberlanda/quantik-core-contracts/pull/23) (v1.3.1), later folded into v1.3.0. The packet's
line references were stale and its allowed test path (`tests/test_validate_opening_book_summary.py`) does not exist;
the real file is `tests/test_opening_book_summary_validator.py`.

Both halves are already tested there (`test_differing_contract_versions_pass_without_expected_release` and
`test_expected_release_still_enforced_when_explicitly_passed`). The packet wanted one combined test; the split is
equivalent, so W1 is closed with no new PR. Lesson: check the packet's premise against `main` before dispatch.

## 2026-09-20 — W5 and W6 merged

- **W6** [contracts#25](https://github.com/mberlanda/quantik-core-contracts/pull/25) dropped the redundant
  `--expected-release 1.3.0` from `validate-contracts.yml`; `validate_contracts.py` already compares `VERSION` to
  `contracts.json` and every fixture to the manifest release, so no check is lost. The packet's grep criterion could not
  be met (`VERSION` has no extension; fixtures must carry the release by design), and `minimum_expected_contract_release`
  in `contracts.json` is a per-stack compatibility floor, not the release literal. Criterion amended, not chased.
  `actions/opening-book-consistency/action.yml` had already lost its default in #23.
- **W5** [contracts#26](https://github.com/mberlanda/quantik-core-contracts/pull/26) adds `scripts/release_preflight.py`
  (tag absent locally and on the remote, `VERSION` equals the tag, action paths exist at the ref; reads git objects,
  not the working tree) and a `preflight_only` dispatch input on `release-contracts.yml`. The tag-push job re-runs
  assertions 2 and 3 with `--tag-already-cut`, because the workflow is tag-triggered and assertion 1 cannot hold there.
- **Follow-ups:**
  - Contracts CI runs the contract validator, not the test suite, so W5's 13 tests are local evidence only.
  - The read-only `preflight` job inherits workflow-level `contents: write`.
  - The local tag check is inert in CI (`checkout` fetches no tags); the `ls-remote` check is the one that fires.
  - The preflight workflow path is unexercised until dispatched from `main`.
