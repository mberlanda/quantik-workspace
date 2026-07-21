from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from quantik_workspace.config import load_workspace
from quantik_workspace.reports import dependency_order
from quantik_workspace.releases import drift

from helpers import init_git, write_json


class DependencyDriftTests(unittest.TestCase):
    def test_dependency_order_places_provider_first_and_detects_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = {
                "version": 1, "workspace": {"name": "test", "repository_layout": "siblings"},
                "repositories": {name: {"url": "x", "path": name, "role": "x", "default_branch": "main", "versions": {"repository_source": None}} for name in ("contracts", "python", "models")},
                "dependencies": [
                    {"from": "python", "to": "contracts", "types": ["release-order"]},
                    {"from": "models", "to": "python", "types": ["release-order"]},
                ],
            }
            write_json(root / "workspace.yaml", manifest)
            config = load_workspace(root / "workspace.yaml")
            self.assertEqual(dependency_order(config), ["contracts", "python", "models"])
            manifest["dependencies"].append({"from": "contracts", "to": "models", "types": ["release-order"]})
            write_json(root / "workspace.yaml", manifest)
            with self.assertRaises(ValueError):
                dependency_order(load_workspace(root / "workspace.yaml"))

    def test_drift_detects_unpublished_action_and_missing_action_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            contracts = root / "contracts"
            consumer = root / "consumer"
            init_git(contracts)
            init_git(consumer)
            (contracts / "VERSION").write_text("1.2.0\n", encoding="utf-8")
            workflow = consumer / ".github/workflows/test.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("- uses: mberlanda/quantik-core-contracts/actions/missing@v1.2.0\n", encoding="utf-8")
            manifest = {
                "version": 1, "workspace": {"name": "test", "repository_layout": "siblings"},
                "repositories": {
                    "quantik-core-contracts": {"url": "x", "path": "contracts", "role": "contracts", "default_branch": "main", "versions": {"repository_source": {"path": "VERSION", "kind": "text"}, "release_mirrors": []}},
                    "consumer": {"url": "x", "path": "consumer", "role": "consumer", "default_branch": "main", "versions": {"repository_source": None, "release_mirrors": [], "supported_contracts_source": None}},
                }, "dependencies": []
            }
            write_json(root / "workspace.yaml", manifest)
            result = drift(load_workspace(root / "workspace.yaml"))
            kinds = {issue["kind"] for issue in result["issues"]}
            self.assertIn("unpublished-action-ref", kinds)
            self.assertIn("missing-action-path", kinds)


if __name__ == "__main__":
    unittest.main()
