"""Command-line interface for the local defensive source checker."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .scanner import scan_tree


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bugs-bounty",
        description="Run bounded, read-only static checks on source you are authorized to review.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_parser = subparsers.add_parser("scan", help="scan a local source directory")
    scan_parser.add_argument("target", type=Path, help="directory containing authorized source code")
    scan_parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    try:
        findings, scanned_files = scan_tree(args.target)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps({"scanned_files": scanned_files, "finding_count": len(findings), "findings": findings}, indent=2))
    else:
        print(f"Scanned {scanned_files} file(s); {len(findings)} review finding(s).")
        for finding in findings:
            print(f"{finding['severity'].upper():8} {finding['path']}:{finding['line']} [{finding['rule_id']}] {finding['title']}")
            print(f"         {finding['remediation']}")
        if not findings:
            print("No configured patterns matched. This is not proof that the code is secure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
