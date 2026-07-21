# Failure and Recovery

- Candidate failure: fix version/source/action/fixture issues before tagging.
- Tag validation failure: do not publish; correct source and create the intended tag only when preconditions pass.
- Published producer failure: do not move the exact tag; prepare a patch release and mark the affected release incompatible/failed as appropriate.
- Consumer failure: keep the producer immutable; fix/revert the consumer, publish a contracts patch, or declare the newly identified break.
- Infrastructure failure: record diagnostics separately and retry without changing compatibility status.
