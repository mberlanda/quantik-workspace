from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from quantik_workspace.versions import SemVer, classify_occurrence, read_version_source, scan_action_references, scan_occurrences


class VersionTests(unittest.TestCase):
    def test_semver_parse_compare_and_prerelease(self) -> None:
        self.assertLess(SemVer.parse("1.1.9"), SemVer.parse("1.2.0"))
        self.assertLess(SemVer.parse("1.2.0-rc.1"), SemVer.parse("1.2.0"))
        self.assertEqual(str(SemVer.parse("v2.3.4")), "2.3.4")
        with self.assertRaises(ValueError):
            SemVer.parse("1.2")

    def test_read_text_json_toml_and_pattern_sources(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "VERSION").write_text("1.2.0\n", encoding="utf-8")
            (root / "manifest.json").write_text(json.dumps({"release": {"version": "1.2.0"}}), encoding="utf-8")
            (root / "pyproject.toml").write_text('[project]\nversion = "3.4.5"\n', encoding="utf-8")
            (root / "source.py").write_text('SUPPORTED = "1.2.0"\n', encoding="utf-8")
            self.assertEqual(read_version_source(root, {"path": "VERSION", "kind": "text"}), "1.2.0")
            self.assertEqual(read_version_source(root, {"path": "manifest.json", "kind": "json", "pointer": "/release/version"}), "1.2.0")
            self.assertEqual(read_version_source(root, {"path": "pyproject.toml", "kind": "toml", "pointer": "project.version"}), "3.4.5")
            self.assertEqual(read_version_source(root, {"path": "source.py", "pattern": r'SUPPORTED = "(?P<version>[^"]+)"'}), "1.2.0")

    def test_occurrence_classification_and_action_refs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow = root / ".github/workflows/contracts.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("- uses: mberlanda/quantik-core-contracts/actions/smoke@v1.1.0\n  expected-release: \"1.2.0\"\n", encoding="utf-8")
            refs = scan_action_references(root)
            self.assertEqual(refs[0]["ref"], "v1.1.0")
            self.assertEqual(refs[1]["expected_release"], "1.2.0")
            occurrences = scan_occurrences(root)
            self.assertTrue(any(item["classification"] == "consumer action reference" for item in occurrences))
            self.assertEqual(classify_occurrence("fixtures/old.jsonl", '"contract_version":"1.0.0"'), "fixture metadata")


if __name__ == "__main__":
    unittest.main()
