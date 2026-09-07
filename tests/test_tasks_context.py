from __future__ import annotations

from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
import json
import os
import shutil
import tempfile
import unittest

from quantik_workspace.cli import main
from quantik_workspace.config import load_workspace
from quantik_workspace.context import ContextBudgetExceeded, initiative_context, repository_context
from quantik_workspace.tasks import create_task, migrate_task, task_status, validate_initiative, validate_tasks

from helpers import minimal_manifest, write_json


class TaskContextTests(unittest.TestCase):
    def _workspace(self, root: Path):
        write_json(root / "workspace.yaml", minimal_manifest("repo"))
        (root / "repo").mkdir()
        (root / "repo/VERSION").write_text("1.0.0\n", encoding="utf-8")
        for path in ("agents/operating-contract.md", "context/system/repository-map.md", "context/system/canonical-invariants.md", "context/repositories/repo.md"):
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
            with self.assertRaisesRegex(ValueError, "requires planning"):
                initiative_context(config, "QW-123", "repo", work_item="W1")
            self.assertTrue((path / "repos/repo/W1-implementation.md").is_file())

    def test_optional_plan_is_composed_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._workspace(root)
            path = create_task(config, "QW-124-planned", "Planned", ["repo"])
            # Legacy initiatives keep their repository-wide planning behavior.
            manifest = json.loads((path / "manifest.yaml").read_text())
            manifest.pop("work_items")
            write_json(path / "manifest.yaml", manifest)
            (path / "repos/repo.md").write_text("Legacy packet")
            self.assertNotIn("plan.md", initiative_context(config, "QW-124", "repo", budget=5000).text)
            (path / "plan.md").write_text("# Charter\n\nThe delegable plan.\n", encoding="utf-8")
            bundle = initiative_context(config, "QW-124", "repo", budget=5000)
            self.assertIn("tasks/active/QW-124-planned/plan.md", bundle.sources)
            self.assertIn("The delegable plan.", bundle.text)
            self.assertEqual(validate_initiative(path, {"repo"}), [])

    def test_migrate_legacy_task_to_atomic_work_items(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._workspace(root)
            path = create_task(config, "QW-126-legacy", "Legacy", ["repo"])
            manifest = json.loads((path / "manifest.yaml").read_text())
            manifest.pop("work_items")
            write_json(path / "manifest.yaml", manifest)
            shutil.rmtree(path / "repos/repo")
            (path / "repos/repo.md").write_text("Objective: do the thing.\n", encoding="utf-8")
            migrated = migrate_task(config, "QW-126")
            self.assertEqual(migrated, path)
            self.assertFalse((path / "repos/repo.md").exists())
            packet = path / "repos/repo/W1-plan-required.md"
            self.assertTrue(packet.is_file())
            self.assertIn("Objective: do the thing.", packet.read_text())
            new_manifest = json.loads((path / "manifest.yaml").read_text())
            item = new_manifest["work_items"][0]
            self.assertEqual(item, {
                "id": "W1", "repository": "repo", "packet": "repos/repo/W1-plan-required.md",
                "branch": "plan/qw-126-repo", "status": "plan-required",
                "allowed_paths": ["REPLACE_WITH_EXPLICIT_PATHS"], "decisions": [], "invariants": [], "depends_on": [],
            })
            # Original initiative-level status is left untouched by migration.
            self.assertEqual(new_manifest["status"], manifest["status"])
            self.assertEqual(validate_initiative(path, {"repo"}), [])
            with self.assertRaisesRegex(ValueError, "already uses"):
                migrate_task(config, "QW-126")
            output = StringIO()
            with redirect_stdout(output):
                code = main(["--workspace", str(config.root / "workspace.yaml"), "task", "migrate", "QW-999"])
            self.assertNotEqual(code, 0)

    def _atomic(self, root):
        config = self._workspace(root)
        config.data["workspace"]["context_budget_tokens"] = 12000
        path = create_task(config, "QW-125-atomic", "Atomic", ["repo"])
        manifest = json.loads((path / "manifest.yaml").read_text())
        manifest["status"] = "planned"
        item = manifest["work_items"][0]
        item.update(status="planned", allowed_paths=["src/app.py"],
                    decisions=["decisions.md#D1"],
                    invariants=["context/system/canonical-invariants.md#Relevant"])
        (path / item["packet"]).write_text("SELECTED_PACKET")
        (path / "decisions.md").write_text("# Decisions\n## D1\nSELECTED_DECISION\n## D2\nSECRET_DECISION")
        (root / "context/system/canonical-invariants.md").write_text("# Invariants\n## Relevant\nSELECTED_INVARIANT\n## Other\nSECRET_INVARIANT")
        sibling = dict(item, id="W2", packet="repos/repo/W2-other.md", branch="feat/other", decisions=[])
        (path / sibling["packet"]).write_text("SECRET_SIBLING")
        manifest["work_items"].append(sibling)
        for name in ("initiative.md", "status.md", "plan.md"):
            (path / name).write_text("SECRET_PLANNING")
        write_json(path / "manifest.yaml", manifest)
        return config, path, manifest

    def test_atomic_isolation_and_live_git_state(self):
        with tempfile.TemporaryDirectory() as directory:
            config, path, manifest = self._atomic(Path(directory))
            with patch("quantik_workspace.context.inspect") as inspect:
                inspect.return_value.to_dict.return_value = dict(branch="current", commit="abc123", dirty=True)
                bundle = initiative_context(config, "QW-125", "repo", work_item="W1")
            for selected in ("SELECTED_PACKET", "SELECTED_DECISION", "SELECTED_INVARIANT", "abc123", "current", "dirty=True", "src/app.py", "6000"):
                self.assertIn(selected, bundle.text)
            self.assertNotIn("SECRET", bundle.text)
            self.assertIn("agents/operating-contract.md", bundle.sources)
            self.assertEqual(len(bundle.sources), 5)
            with self.assertRaisesRegex(ValueError, "requires --work-item"):
                initiative_context(config, "QW-125", "repo")
            with self.assertRaisesRegex(ValueError, "unknown work item"):
                initiative_context(config, "QW-125", "repo", work_item="BAD")
            with self.assertRaisesRegex(ValueError, "unknown work item"):
                initiative_context(config, "QW-125", "wrong", work_item="W1")

    def test_atomic_budget_and_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            config, path, manifest = self._atomic(Path(directory))
            output = StringIO()
            with redirect_stdout(output):
                code = main(["--workspace", str(config.root / "workspace.yaml"), "context", "task", "QW-125", "repo", "--work-item", "W1", "--budget", "4000"])
            self.assertEqual(code, 0)
            self.assertIn("SELECTED_PACKET", output.getvalue())
            (path / manifest["work_items"][0]["packet"]).write_text("x" * 25000)
            with self.assertRaises(ContextBudgetExceeded):
                initiative_context(config, "QW-125", "repo", work_item="W1")
            self.assertGreater(initiative_context(config, "QW-125", "repo", budget=10000, work_item="W1").approximate_tokens, 6000)
            with patch.dict(os.environ, {"QUANTIK_CONTEXT_BUDGET_TOKENS": "100"}):
                with self.assertRaises(ContextBudgetExceeded):
                    initiative_context(config, "QW-125", "repo", work_item="W1")
            with self.assertRaisesRegex(ValueError, "positive"):
                initiative_context(config, "QW-125", "repo", budget=0, work_item="W1")

    def test_atomic_invalid_manifests(self):
        with tempfile.TemporaryDirectory() as directory:
            config, path, manifest = self._atomic(Path(directory))
            for field, value in (("id", "W2"), ("packet", "../outside.md"), ("packet", "missing.md"),
                                 ("allowed_paths", ["../escape"]), ("allowed_paths", []),
                                 ("branch", "feat/other"), ("decisions", ["decisions.md#Missing"]),
                                 ("depends_on", ["UNKNOWN"]), ("repository", "unknown")):
                with self.subTest(field=field, value=value):
                    bad = deepcopy(manifest)
                    bad["work_items"][0][field] = value
                    write_json(path / "manifest.yaml", bad)
                    self.assertTrue(validate_initiative(path, {"repo"}))
            for value in (None, {}, [], [None]):
                bad = dict(manifest, work_items=value)
                write_json(path / "manifest.yaml", bad)
                self.assertTrue(validate_initiative(path, {"repo"}))
                self.assertEqual(validate_tasks(config)["status"], "failed")
            write_json(path / "manifest.yaml", manifest)
            packet = path / manifest["work_items"][0]["packet"]
            packet.unlink()
            outside = config.root / "outside.md"
            outside.write_text("PRIVATE")
            packet.symlink_to(outside)
            self.assertTrue(validate_initiative(path, {"repo"}))

    def test_status_lists_items_and_cycles_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            config, path, manifest = self._atomic(Path(directory))
            result = task_status(config)
            self.assertEqual(result["status"], "ok")
            self.assertEqual([item["id"] for item in result["initiatives"][0]["work_items"]], ["W1", "W2"])
            manifest["work_items"][0]["depends_on"] = ["W2"]
            manifest["work_items"][1]["depends_on"] = ["W1"]
            write_json(path / "manifest.yaml", manifest)
            self.assertIn("cyclic", " ".join(validate_initiative(path, {"repo"})))

    def test_missing_required_input_and_reference_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            config, path, manifest = self._atomic(Path(directory))
            (config.root / "agents/operating-contract.md").unlink()
            with self.assertRaisesRegex(ValueError, "missing or out-of-scope"):
                initiative_context(config, "QW-125", "repo", work_item="W1")
            manifest["work_items"][0]["invariants"] = ["context/system/canonical-invariants.md#Missing"]
            write_json(path / "manifest.yaml", manifest)
            self.assertEqual(validate_tasks(config)["status"], "failed")

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
