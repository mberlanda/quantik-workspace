from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from quantik_workspace.cli import main

from helpers import minimal_manifest, write_json


class CliTests(unittest.TestCase):
    def test_repositories_list_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "workspace.yaml", minimal_manifest("repo"))
            output = StringIO()
            with redirect_stdout(output):
                code = main(["--workspace", str(root / "workspace.yaml"), "repos", "list"])
            self.assertEqual(code, 0)
            self.assertIn('"name": "repo"', output.getvalue())

    def test_invalid_release_input_has_meaningful_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "workspace.yaml", minimal_manifest("repo"))
            code = main(["--workspace", str(root / "workspace.yaml"), "release", "plan", "--repository", "repo", "--version", "1.2", "--id", "QREL-2026-001"])
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
