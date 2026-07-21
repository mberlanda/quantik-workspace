# Release Trains

Release trains separate producer candidate validation from immutable tagging, publication, external verification, and consumer adoption. Exact tags never move. Active manifests live in `active/`; audit locks live in `locks/`; complete trains move to `completed/`.
