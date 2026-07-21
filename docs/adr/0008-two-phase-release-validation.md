# ADR 0008: Two-Phase Release Validation

## Context
A candidate cannot depend on a tag that does not exist, while consumers need proof of the external exact ref.

## Decision
Validate checked-out candidate actions through relative paths; after immutable tagging/publication, validate exact external refs and assets.

## Alternatives
Pre-create/move tags, test only source, or test only published artifacts.

## Consequences
Circular release dependencies disappear and publication defects are visible. CI needs separate source and published modes; failures after publication require patch releases.
