# Data Flows

Readable flow: contracts JSON Schema + JSONL golden cases → engine-owned adapters → deterministic reports → workspace comparison/classification.

Bulk flow: engine self-play/search exporters → Arrow IPC or Parquet with logical/physical schema, contracts release, and generator metadata → Python-core readers → model materialization/training → checkpoint manifest/evaluation evidence.

Release flow: producer source candidate → relative-action validation → immutable tag/publication → exact external action verification → consumer tasks → compatibility matrix/lock. Workspace files carry state; implementation artifacts remain with their owners.
