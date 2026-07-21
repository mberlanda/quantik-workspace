# QW-006: Search-Derived Observation Policy Targets

Replace the observation exporter's synthetic selected-action visit with the
actual root policy mass available from search. Preserve deterministic action
indexing and distinguish visits from scores, priors, bounds, or engine-specific
statistics.

First produce a focused design/implementation plan. If current
`observation.v1` semantics cannot express a supported engine faithfully, route
the contract decision through a new contracts task before implementation.
