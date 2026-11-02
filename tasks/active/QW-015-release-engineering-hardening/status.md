

## 2026-09-20 — W7 merged: every work item is now completed

[contracts#31](https://github.com/mberlanda/quantik-core-contracts/pull/31) records the deadlock demonstration in `docs/consistency-checks.md`. Rust summary at 1.3.0 (sibling main) against a Python summary at 1.4.0, contracts on 1.3.0, no tag: main and the `v1.3.0` tag validators pass; the `v1.2.0` validator (control) fails "summaries differ"; an explicit `--expected-release 1.3.0` and a real one-edge difference still fail, so the check has not gone blind. **Limit:** the summaries are hand-built to the real depth-4 shape (11739 positions, 340680 edges), not engine-generated, and only the validator command ran, not the composite action or a live CI run. Contracts CI does not run pytest.

**Matrix regenerated 2026-11-02.** The portability adapters no longer exit 2 (their arguments are optional) and the cross-stack smoke passes for Python and Rust. **Not yet done, so the initiative stays active:** `supported` is still withheld, because the smoke ran on post-tag checkouts, not at the contracts tag, and covers 3 cases. Run it at the release tags, or decide that post-tag evidence is enough, then close.
