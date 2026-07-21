from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from quantik_workspace.config import ConfigurationError, find_manifest, load_data, load_workspace
from quantik_workspace.validation import validate_workspace

from helpers import minimal_manifest, write_json


class ConfigTests(unittest.TestCase):
    def test_manifest_and_local_path_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "workspace.yaml", minimal_manifest("../default"))
            (root / "workspace.local.yaml").write_text("repositories:\n  repo:\n    path: /tmp/override-repo\n", encoding="utf-8")
            config = load_workspace(root / "workspace.yaml")
            self.assertEqual(config.repository_path("repo"), Path("/tmp/override-repo").resolve())
            self.assertEqual(config.repositories["repo"]["role"], "test")

    def test_json_is_valid_yaml_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "workspace.yaml"
            write_json(path, {"version": 1})
            self.assertEqual(load_data(path), {"version": 1})

    def test_find_manifest_honors_environment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "custom.yaml"
            write_json(path, minimal_manifest())
            with patch.dict(os.environ, {"QUANTIK_WORKSPACE_FILE": str(path)}):
                self.assertEqual(find_manifest(Path("/")), path.resolve())

    def test_invalid_repository_definition_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = minimal_manifest()
            del manifest["repositories"]["repo"]["url"]
            write_json(root / "workspace.yaml", manifest)
            (root / "schemas").mkdir()
            write_json(root / "schemas/workspace.schema.json", {"type": "object"})
            result = validate_workspace(load_workspace(root / "workspace.yaml"))
            self.assertEqual(result["status"], "failed")
            self.assertTrue(any(".url" in error for error in result["errors"]))

    def test_missing_manifest_is_clear(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigurationError):
                find_manifest(Path(directory))


if __name__ == "__main__":
    unittest.main()
