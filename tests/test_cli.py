from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from bugs_bounty.__main__ import main


class CliTests(unittest.TestCase):
    def test_platform_is_in_report_metadata_and_folder_layout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "source"
            target.mkdir()
            report_dir = root / "reports"
            output = io.StringIO()

            with patch("bugs_bounty.__main__.scan_tree", return_value=([], 2)):
                with contextlib.redirect_stdout(output):
                    result = main([
                        "scan",
                        str(target),
                        "--app-name",
                        "Example App",
                        "--country",
                        "Canada",
                        "--platform",
                        "mobile",
                        "--report-dir",
                        str(report_dir),
                        "--format",
                        "json",
                    ])

            report_path = report_dir / "Canada" / "mobile" / "Example App.json"
            self.assertEqual(result, 0)
            self.assertTrue(report_path.is_file())
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["country"], "Canada")
            self.assertEqual(report["platform"], "mobile")
            self.assertEqual(json.loads(output.getvalue()), report)

    def test_platform_defaults_to_unspecified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            with patch("bugs_bounty.__main__.scan_tree", return_value=([], 0)):
                with contextlib.redirect_stdout(output):
                    result = main(["scan", directory, "--format", "json"])

            self.assertEqual(result, 0)
            self.assertEqual(json.loads(output.getvalue())["platform"], "unspecified")

    def test_rejects_platform_folder_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            errors = io.StringIO()
            with patch("bugs_bounty.__main__.scan_tree", return_value=([], 0)):
                with contextlib.redirect_stderr(errors):
                    result = main([
                        "scan",
                        directory,
                        "--platform",
                        "../mobile",
                    ])

            self.assertEqual(result, 2)
            self.assertIn("invalid choice", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
