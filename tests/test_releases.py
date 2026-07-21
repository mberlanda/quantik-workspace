from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from quantik_workspace.config import load_workspace
from quantik_workspace.releases import can_transition, validate_candidate, validate_lock, validate_release_mapping

from helpers import init_git, minimal_manifest, write_json


class ReleaseTests(unittest.TestCase):
    def test_release_state_transitions(self) -> None:
        self.assertTrue(can_transition("planned", "prepared"))
        self.assertTrue(can_transition("candidate-green", "tagged"))
        self.assertFalse(can_transition("planned", "tagged"))
        self.assertFalse(can_transition("completed", "failed"))

    def test_release_train_validation(self) -> None:
        value = {"id": "QREL-2026-001", "status": "planned", "producer": {"repository": "repo", "version": "1.2.0", "tag": "v1.2.0", "branch": "release/v1.2.0"}, "consumers": {}, "release_order": ["repo"]}
        self.assertEqual(validate_release_mapping(value), [])
        value["producer"]["tag"] = "v1.1.0"
        self.assertTrue(validate_release_mapping(value))

    def test_candidate_rejects_future_tag_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            commit = init_git(repo)
            (repo / "VERSION").write_text("1.2.0\n", encoding="utf-8")
            workflow = repo / ".github/workflows/candidate.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("steps:\n  - uses: mberlanda/quantik-core-contracts/actions/smoke@v1.2.0\n", encoding="utf-8")
            manifest = minimal_manifest("repo")
            manifest["repositories"]["repo"]["published_interfaces"] = {"github_actions": {"smoke": "actions/smoke"}}
            write_json(root / "workspace.yaml", manifest)
            release_dir = root / "releases/active/QREL-2026-001"
            write_json(release_dir / "release.yaml", {"id": "QREL-2026-001", "status": "prepared", "producer": {"repository": "repo", "previous_version": "1.1.0", "version": "1.2.0", "tag": "v1.2.0", "branch": "release/v1.2.0", "commit": commit}, "consumers": {}, "release_order": ["repo"]})
            config = load_workspace(root / "workspace.yaml")
            result = validate_candidate(config, "QREL-2026-001")
            self.assertEqual(result["status"], "failed")
            self.assertTrue(any("unpublished tag" in error for error in result["errors"]))

    def test_release_lock_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "workspace.yaml", minimal_manifest())
            lock = root / "lock.yaml"
            commit = "a" * 40
            write_json(lock, {"producer": {"repository": "mberlanda/repo", "version": "1.2.0", "tag": "v1.2.0", "commit": commit}, "interfaces": {"smoke": {"path": "actions/smoke", "ref": "v1.2.0", "commit": commit}}})
            self.assertEqual(validate_lock(load_workspace(root / "workspace.yaml"), lock), [])


if __name__ == "__main__":
    unittest.main()
