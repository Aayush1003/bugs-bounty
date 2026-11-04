from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bugs_bounty.scanner import scan_tree


class ScannerTests(unittest.TestCase):
    def test_reports_reviewable_patterns_without_source_or_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.py").write_text(
                'api_key = "not-a-real-secret-value-123"\n'
                'subprocess.run(command, shell=True)\n', encoding="utf-8"
            )
            findings, scanned = scan_tree(root)
            self.assertEqual(scanned, 1)
            self.assertEqual([item["rule_id"] for item in findings], ["BB-SECRET-001", "BB-CMD-001"])
            self.assertNotIn("not-a-real-secret-value-123", repr(findings))
            self.assertNotIn("subprocess.run", repr(findings))

    def test_skips_dependencies_and_non_source_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "node_modules").mkdir()
            (root / "node_modules" / "vendor.js").write_text("eval(x)", encoding="utf-8")
            (root / "notes.txt").write_text("eval(x)", encoding="utf-8")
            findings, scanned = scan_tree(root)
            self.assertEqual((findings, scanned), ([], 0))

    def test_requires_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "file.py"
            file_path.write_text("pass", encoding="utf-8")
            with self.assertRaises(ValueError):
                scan_tree(file_path)


if __name__ == "__main__":
    unittest.main()
