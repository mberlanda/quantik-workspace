

## 2026-09-20 — W7 merged: every work item is now completed

[contracts#31](https://github.com/mberlanda/quantik-core-contracts/pull/31) records the deadlock demonstration in `docs/consistency-checks.md`. Rust summary at 1.3.0 (sibling main) against a Python summary at 1.4.0, contracts on 1.3.0, no tag: main and the `v1.3.0` tag validators pass; the `v1.2.0` validator (control) fails "summaries differ"; an explicit `--expected-release 1.3.0` and a real one-edge difference still fail, so the check has not gone blind. **Limit:** the summaries are hand-built to the real depth-4 shape (11739 positions, 340680 edges), not engine-generated, and only the validator command ran, not the composite action or a live CI run. Contracts CI does not run pytest.

**Matrix regenerated 2026-11-02.** The portability adapters no longer exit 2 (their arguments are optional) and the cross-stack smoke passes for Python and Rust. **Not yet done, so the initiative stays active:** `supported` is still withheld, because the smoke ran on post-tag checkouts, not at the contracts tag, and covers 3 cases. Run it at the release tags, or decide that post-tag evidence is enough, then close.

## 2026-11-02 — 1.4.0 tagged on all three repos; resume here

Lockstep `v1.4.0` is tagged on contracts (722fe4c), core-py (c7517cb) and core-rust (6f8272d), each from a green merge commit. Recorded as QREL-2026-004 (workspace#39). The withdrawn 1.3.1 was removed (workspace#38).

**Next actions, in order:**

1. **Publish, by hand, from the tags.** PyPI: [core-py#51](https://github.com/mberlanda/quantik-core-py/issues/51). crates.io: [core-rust#48](https://github.com/mberlanda/quantik-core-rust/issues/48). Both issues carry the checkout-at-tag and publish commands. The core-py publish workflow runs only on a published GitHub Release and its last three runs failed with a trusted-publishing exchange error, so check the PyPI trusted-publisher setup first. The core-rust publish jobs are disabled (`if: ${{ false }}`).
2. **Re-run the portability smoke at the v1.4.0 tags** (check out each repo at `v1.4.0`, not main). If it passes, set the 1.4.0 matrix row to `supported` (`docs/generated/compatibility-matrix.json` and `.md`), regenerate with `reports generate`, and revert unrelated `repository-summary.md` churn. Or decide post-tag evidence is enough. Then close this initiative.
3. **Fix the changelog wording.** `quantik-core-contracts` `CHANGELOG.md` says the old `quantik.` prefix is rejected "from 1.5.0". 1.5.0 is no longer a separate release and the contract doc only says "next minor". Reword to match the doc.
4. After publishing, flip the "publish pending" notes in `docs/releases/release-plan.md` (ledger table and ladder row) and QREL-2026-004 `status.md` and `release.yaml` (`not_verified`).

Consumer records in QREL-2026-004 keep `current_*` at 1.3.0, the pattern QREL-2026-002 used. Say if they should read 1.4.0.

**Other open items, none started this session:** QW-024 and QW-026 are fully complete but unverified or unclosed; QW-002 W1 design approval; Decision review `0001`; ADR 0014; QW-012 seed text bookkeeping; CI for `quantik-api-rust` (a `ci.yml` with a pinned core-rust sibling checkout) and the visualizer (`npm test` on Node 22); a core-py `find_canonical_with_transform` wrapper; the redundant `quantik-api-rust` stash `api-rust-cargolock-2026-11` (drop on the user's say-so); and the stale branch `origin/copilot/47-add-example-to-pr-comment` in core-py.

**Repo state:** all six code repos are on `main`. Kept local branches: `exact-oracle`.
