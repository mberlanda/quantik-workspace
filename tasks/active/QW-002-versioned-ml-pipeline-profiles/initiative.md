# QW-002: Versioned ML Pipeline Profiles

## Problem and desired outcome

`quantik-models-py` owns the executable cross-repository pipeline, but
`run_smoke_pipeline.sh`, training wrappers, CI, and prose assemble parameters in
different places. Create one tier-independent runner with reviewable profiles
for smoke, CI, small, and target runs.

## Planning gate

No implementation plan exists. First produce a design and PR-sized plan that
decides the profile format, stage graph, override precedence, failure/resume
behavior, output provenance, and migration from current scripts. Implementation
must not start until that plan is approved.

## Constraints

- Keep repository-owned producers and readers as subprocess boundaries.
- Preserve current smoke behavior during migration.
- Do not put secrets or machine-specific checkout paths in committed profiles.
- A target profile is a reproducible configuration, not a claim that a target
  training run has completed.

## Acceptance

All run tiers use the same validated definition, emit effective configuration
and exact input revisions, and retain focused smoke coverage.
