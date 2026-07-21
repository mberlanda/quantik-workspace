# Action Versioning

Composite actions and reusable workflows follow the contracts repository tag unless a separate lifecycle ADR is approved. Use readable exact refs such as `@v1.2.0`; record their resolved full SHA in the release lock. Never move exact tags.

Candidate source mode uses `uses: ./actions/<name>` after checkout and derives expected release from `VERSION`. Published mode invokes `mberlanda/quantik-core-contracts/actions/<name>@vX.Y.Z` exactly as a consumer would.
