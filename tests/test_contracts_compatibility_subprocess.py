from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from quantik_workspace.compatibility import invoke_adapter, validate_report
from quantik_workspace.contracts import validate_jsonl
from quantik_workspace.subprocesses import CommandError, run


class BoundaryTests(unittest.TestCase):
    def test_jsonl_success_and_validation_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.jsonl"
            path.write_text('{"schema":"selfplay.v1","contract_version":"1.2.0"}\n', encoding="utf-8")
            self.assertEqual(validate_jsonl(path, expected_release="1.2.0"), [])
            self.assertTrue(validate_jsonl(path, expected_release="1.1.0"))
            path.write_text("not json\n", encoding="utf-8")
            self.assertTrue(validate_jsonl(path))

    def test_subprocess_failure_is_structured(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cwd = Path(directory)
            with self.assertRaises(CommandError):
                run(["sh", "-c", "echo failed >&2; exit 7"], cwd)
            result = invoke_adapter("repo", "test", ["sh", "-c", "exit 9"], cwd)
            self.assertEqual(result.category, "infrastructure failure")

    def test_compatibility_report_parser(self) -> None:
        valid = {"schema": "quantik-compatibility-report.v1", "results": [{"category": "missing coverage"}]}
        self.assertEqual(validate_report(valid), [])
        valid["results"][0]["category"] = "mystery"
        self.assertTrue(validate_report(valid))


if __name__ == "__main__":
    unittest.main()
