# Dependency Graph

Generated from `workspace.yaml`.

| Consumer | Provider | Dependency types |
| --- | --- | --- |
| `quantik-core-py` | `quantik-core-contracts` | contract, fixture, schema, github-action, release-order |
| `quantik-core-rust` | `quantik-core-contracts` | contract, fixture, schema, github-action, release-order |
| `quantik-models-py` | `quantik-core-contracts` | contract, schema, generated-data, release-order |
| `quantik-models-py` | `quantik-core-py` | build, runtime, generated-data, semantic-compatibility |
| `quantik-models-py` | `quantik-core-rust` | generated-data, semantic-compatibility |
| `quantik-core-py` | `quantik-core-rust` | semantic-compatibility |
| `quantik-api-rust` | `quantik-core-rust` | build, runtime |
| `quantik-qfen-visualizer` | `quantik-api-rust` | runtime, contract |
| `quantik-qfen-visualizer` | `quantik-models-py` | runtime, contract |
| `articles` | `quantik-models-py` | generated-data |

Release-order edges point from consumer to the provider that must be available first.
