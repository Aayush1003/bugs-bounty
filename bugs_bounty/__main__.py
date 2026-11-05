"""Command-line interface for the local defensive source checker."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from .scanner import scan_tree


def _folder_component(value: str) -> str:
    """Return a safe single folder/file name component for a local report."""
    component = re.sub(r"[^\w .-]", "_", value, flags=re.UNICODE).strip(" .")
    if not component or component in {".", ".."}:
        raise ValueError("app name, country, and platform must contain at least one safe character")
    return component


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bugs-bounty",
        description="Run bounded, read-only static checks on source you are authorized to review.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_parser = subparsers.add_parser("scan", help="scan a local source directory")
    scan_parser.add_argument("target", type=Path, help="directory containing authorized source code")
    scan_parser.add_argument("--format", choices=("text", "json"), default="text")
    scan_parser.add_argument(
        "--app-name",
        help="app name to include in findings (defaults to the source directory name)",
    )
    scan_parser.add_argument(
        "--country",
        default="Unknown (not provided)",
        help="country where the app is available or used; provide this manually (default: %(default)s)",
    )
    scan_parser.add_argument(
        "--platform",
        choices=("web", "mobile", "both", "unspecified"),
        default="unspecified",
        help="digital platform represented by this source (default: %(default)s)",
    )
    scan_parser.add_argument(
        "--report-dir",
        type=Path,
        help="also save JSON to <report-dir>/<country>/<platform>/<app-name>.json",
    )
    args = parser.parse_args(argv)

    app_name = args.app_name or args.target.name or "app"
    try:
        app_component = _folder_component(app_name)
        country_component = _folder_component(args.country)
        platform_component = _folder_component(args.platform)
        findings, scanned_files = scan_tree(args.target)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    annotated_findings = [
        {**finding, "app_name": app_name, "country": args.country, "platform": args.platform}
        for finding in findings
    ]
    report = {
        "app_name": app_name,
        "country": args.country,
        "platform": args.platform,
        "scanned_files": scanned_files,
        "finding_count": len(annotated_findings),
        "findings": annotated_findings,
    }

    if args.report_dir:
        report_path = (
            args.report_dir
            / country_component
            / platform_component
            / f"{app_component}.json"
        )
        try:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"error: could not write report: {exc}", file=sys.stderr)
            return 2

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(f"App: {app_name} | Country: {args.country} | Platform: {args.platform}")
        print(f"Scanned {scanned_files} file(s); {len(annotated_findings)} review finding(s).")
        for finding in annotated_findings:
            print(
                f"{finding['severity'].upper():8} {finding['path']}:{finding['line']} "
                f"[{finding['rule_id']}] {finding['title']} "
                f"(app: {finding['app_name']}; country: {finding['country']}; "
                f"platform: {finding['platform']})"
            )
            print(f"         {finding['remediation']}")
        if not findings:
            print("No configured patterns matched. This is not proof that the code is secure.")
        if args.report_dir:
            print(f"JSON report saved to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
