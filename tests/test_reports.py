from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from quantik_workspace.config import load_workspace
from quantik_workspace.reports import task_dependency_map, task_dependency_markdown
from quantik_workspace.tasks import complete_task, create_task

from helpers import minimal_manifest, write_json


class TaskDependencyGraphTests(unittest.TestCase):
    def _workspace(self, root: Path):
        write_json(root / "workspace.yaml", minimal_manifest("repo"))
        (root / "repo").mkdir()
        (root / "repo/VERSION").write_text("1.0.0\n", encoding="utf-8")
        for path in ("agents/operating-contract.md", "context/system/repository-map.md", "context/system/canonical-invariants.md", "context/repositories/repo.md"):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {path}\n", encoding="utf-8")
        return load_workspace(root / "workspace.yaml")

    def test_blocked_by_excludes_completed_dependencies_and_marks_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._workspace(root)

            provider = create_task(config, "QW-001-provider", "Provider", ["repo"])
            provider_manifest = json.loads((provider / "manifest.yaml").read_text())
            provider_manifest["work_items"][0]["status"] = "completed"
            write_json(provider / "manifest.yaml", provider_manifest)
            complete_task(config, "QW-001")

            blocked = create_task(config, "QW-002-blocked", "Blocked", ["repo"])
            blocked_manifest = json.loads((blocked / "manifest.yaml").read_text())
            blocked_manifest["dependencies"] = ["QW-003"]
            blocked_manifest["complexity"] = "L"
            write_json(blocked / "manifest.yaml", blocked_manifest)

            ready = create_task(config, "QW-003-ready", "Ready", ["repo"])
            ready_manifest = json.loads((ready / "manifest.yaml").read_text())
            ready_manifest["dependencies"] = ["QW-001"]
            ready_manifest["complexity"] = "S"
            write_json(ready / "manifest.yaml", ready_manifest)

            graph = task_dependency_map(config)
            by_id = {item["id"]: item for item in graph["initiatives"]}

            self.assertTrue(by_id["QW-001"]["done"])
            self.assertEqual(by_id["QW-001"]["state"], "completed")

            self.assertFalse(by_id["QW-003"]["done"])
            self.assertEqual(by_id["QW-003"]["blocked_by"], [])  # QW-001 is done
            self.assertEqual(by_id["QW-003"]["complexity"], "S")

            self.assertEqual(by_id["QW-002"]["blocked_by"], ["QW-003"])  # QW-003 is not done

            markdown = task_dependency_markdown(config)
            self.assertIn("```mermaid", markdown)
            self.assertIn("QW-001 --> QW-003", markdown)
            self.assertIn("class QW-001 done", markdown)
            self.assertIn("class QW-002 blocked", markdown)
            self.assertIn("class QW-003 ready", markdown)


if __name__ == "__main__":
    unittest.main()
