from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from bugs_bounty.__main__ import main
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

    def test_report_is_saved_in_country_folder_and_labels_each_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = root / "local-app"
            app.mkdir()
            (app / "app.py").write_text('eval(user_input)\n', encoding="utf-8")
            report_dir = root / "reports"

            result = main([
                "scan", str(app), "--app-name", "Example App", "--country", "Canada",
                "--report-dir", str(report_dir), "--format", "json",
            ])

            report_path = report_dir / "Canada" / "Example App.json"
            self.assertEqual(result, 0)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["app_name"], "Example App")
            self.assertEqual(report["country"], "Canada")
            self.assertEqual(report["findings"][0]["app_name"], "Example App")
            self.assertEqual(report["findings"][0]["country"], "Canada")

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
