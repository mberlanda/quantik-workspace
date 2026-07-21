from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from quantik_workspace.git import inspect

from helpers import init_git


class GitTests(unittest.TestCase):
    def test_missing_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            status = inspect(Path(directory) / "missing")
            self.assertFalse(status.exists)
            self.assertFalse(status.is_git)

    def test_clean_and_dirty_repository_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            commit = init_git(root)
            clean = inspect(root)
            self.assertEqual(clean.commit, commit)
            self.assertEqual(clean.branch, "main")
            self.assertFalse(clean.dirty)
            (root / "README.md").write_text("changed\n", encoding="utf-8")
            (root / "new.txt").write_text("new\n", encoding="utf-8")
            dirty = inspect(root)
            self.assertTrue(dirty.dirty)
            self.assertEqual(dirty.untracked, 1)

    def test_existing_non_git_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            status = inspect(Path(directory))
            self.assertTrue(status.exists)
            self.assertFalse(status.is_git)


if __name__ == "__main__":
    unittest.main()
