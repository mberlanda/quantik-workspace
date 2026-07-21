# quantik-models-py Packet

Purpose: training views, policy/value network/training, inference/evaluation, and checkpoint export. Important modules: data materialization/dataset/labels, model spec/network, trainer, export/checkpoint. Version source/mirror: pyproject and package `__version__` (`0.1.0`). Inspected clean `main` at `ea8f32ad4fac8fdf4f9620e9a4163e08bb6f2469`.

Commands: pytest, smoke pipeline, materialize/train CLIs; mypy is available but not in CI. Contracts defaults/fixtures still say 1.1.0; CI uses mutable sibling branches. Sensitive areas: duplicate Python-core training views, divergent NPZ fields/weights, positive-visits mask versus legal mask, all-false mask behavior, output-contract naming, missing D4 action remapping.

Make tensor shapes, action indices, masks, value perspective, exact data/checkpoint contracts, and input revisions explicit in every handoff.
