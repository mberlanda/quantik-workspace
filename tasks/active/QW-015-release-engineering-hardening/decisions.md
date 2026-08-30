# QW-015 Decisions

1. **Exclude `contract_version` from the equality; keep it for `--expected-release`.**
   The alternative — keeping the fused check and always passing matching versions — is
   what produced the deadlock. Rejected because it makes every cross-stack PR a release
   event.

2. **Delete the action's `default: "1.2.0"`, do not merely stop passing the input.**
   Verified 2026-08-30 at `action.yml:23`. A default is an invisible constraint: a
   caller that omits the input reads as unconstrained and is not. Rejected alternative:
   change the default to the current release — same failure, later.

3. **The schema is not versioned for this.** `opening-book-summary.v1` is unchanged.
   The validator compares a subset of what it parses; that is a validator policy, not a
   wire-format change. Rejected: a `v2` summary without `contract_version` — it would
   remove information that the `--expected-release` assertion legitimately needs.

4. **Lockstep is kept as a policy.** This initiative is often described as "dropping
   lockstep". It is not. contracts / rust / py continue to share one version number;
   what changes is that the *opening-book agreement check* stops being the mechanism
   that enforces it.
