# Compatibility Policy

Additive changes are compatible only when existing readers safely ignore them. Required-field, interpretation, ordering, action-index, QFEN, or tensor-layout changes require a new wire major. Exact evidence must state producer/consumer commits, package versions, contracts release, wire IDs, fixture/artifact hashes, commands, and outcomes.

Do not mark support from documentation alone. Preserve and classify differences. Infrastructure failures do not prove incompatibility; repeated meaningful semantic drift creates tasks.
