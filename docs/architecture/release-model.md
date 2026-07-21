# Release Model

Version axes are independent: repository/package version, whole contracts release, wire-contract ID, action ref, workflow expectation, and supported-contract declaration. Candidate validation uses checked-out source/relative actions. Published validation uses the exact immutable tag that consumers invoke.

States: planned → prepared → candidate-green → tagged → published → producer-verified → consumer-updates-open → consumer-compatible → completed. `failed` and `rolled-back` are terminal side states. Tagging and publication are separate guarded commands. Exact tags never move; published defects require a patch release.
