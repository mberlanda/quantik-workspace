from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from quantik_workspace.config import load_workspace
from quantik_workspace.reports import (
    dispatch_board,
    dispatch_board_markdown,
    task_dependency_map,
    task_dependency_markdown,
)
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


class DispatchBoardTests(unittest.TestCase):
    def _workspace(self, root: Path):
        write_json(root / "workspace.yaml", minimal_manifest("repo"))
        (root / "repo").mkdir()
        (root / "repo/VERSION").write_text("1.0.0\n", encoding="utf-8")
        for path in ("agents/operating-contract.md", "context/system/repository-map.md", "context/system/canonical-invariants.md", "context/repositories/repo.md"):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {path}\n", encoding="utf-8")
        return load_workspace(root / "workspace.yaml")

    def test_a_work_item_is_ready_only_once_its_dependency_is_completed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._workspace(root)
            path = create_task(config, "QW-100-example", "Example", ["repo"])

            manifest = json.loads((path / "manifest.yaml").read_text())
            first = manifest["work_items"][0]
            first.update({"status": "planned", "complexity": "S", "dispatch": "mechanical"})
            second = dict(first)
            second.update({
                "id": "W2", "branch": "feat/second", "packet": "repos/repo/W2-second.md",
                "depends_on": ["W1"], "complexity": "M", "dispatch": "judgment",
            })
            manifest["work_items"] = [first, second]
            write_json(path / "manifest.yaml", manifest)
            (path / "repos/repo/W2-second.md").write_text("# W2\n", encoding="utf-8")

            by_id = {row["work_item"]: row for row in dispatch_board(config)}
            self.assertTrue(by_id["W1"]["ready"])
            self.assertFalse(by_id["W2"]["ready"])
            self.assertEqual(by_id["W2"]["unmet_dependencies"], ["W1"])
            self.assertEqual(by_id["W2"]["dispatch"], "judgment")

            # Completing W1 releases W2.
            manifest["work_items"][0]["status"] = "completed"
            write_json(path / "manifest.yaml", manifest)
            by_id = {row["work_item"]: row for row in dispatch_board(config)}
            self.assertTrue(by_id["W2"]["ready"])

            markdown = dispatch_board_markdown(config)
            self.assertIn("# Dispatch Board", markdown)
            self.assertIn("`QW-100`", markdown)

    def test_plan_required_items_are_never_ready(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._workspace(root)
            create_task(config, "QW-101-unplanned", "Unplanned", ["repo"])
            # create_task scaffolds plan-required items; context generation refuses them, so the
            # board must not advertise them as pickable.
            rows = dispatch_board(config)
            self.assertTrue(rows)
            self.assertFalse(any(row["ready"] for row in rows))


if __name__ == "__main__":
    unittest.main()
