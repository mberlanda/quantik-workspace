from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from quantik_workspace.config import load_workspace
from quantik_workspace.context import ContextBudgetExceeded, initiative_context, repository_context
from quantik_workspace.tasks import create_task, validate_initiative, validate_tasks

from helpers import minimal_manifest, write_json


class TaskContextTests(unittest.TestCase):
    def _workspace(self, root: Path):
        write_json(root / "workspace.yaml", minimal_manifest("repo"))
        (root / "repo").mkdir()
        (root / "repo/VERSION").write_text("1.0.0\n", encoding="utf-8")
        for path in ("context/system/repository-map.md", "context/system/canonical-invariants.md", "context/repositories/repo.md"):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"# {path}\n", encoding="utf-8")
        return load_workspace(root / "workspace.yaml")

    def test_create_validate_and_select_task_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._workspace(root)
            path = create_task(config, "QW-123-example", "Example", ["repo"])
            self.assertEqual(validate_initiative(path, {"repo"}), [])
            self.assertEqual(validate_tasks(config)["status"], "ok")
            bundle = initiative_context(config, "QW-123", "repo", budget=5000)
            self.assertIn("repository task", bundle.text)
            self.assertIn("repos/repo.md", bundle.text)

    def test_task_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            self.assertTrue(validate_initiative(path, {"repo"}))

    def test_repository_context_budget_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._workspace(root)
            (root / "context/repositories/repo.md").write_text("x" * 5000, encoding="utf-8")
            with self.assertRaises(ContextBudgetExceeded):
                repository_context(config, "repo", budget=100)


if __name__ == "__main__":
    unittest.main()
