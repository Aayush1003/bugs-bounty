"""Bounded, read-only source tree scanner. It never follows symlinks or uses the network."""

from __future__ import annotations

import os
from pathlib import Path

from .rules import RULES

SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".h", ".hpp", ".html", ".java",
    ".js", ".jsx", ".kt", ".php", ".py", ".rb", ".rs", ".ts", ".tsx",
}
IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
    "vendor", "dist", "build", "__pycache__", ".next", ".tox",
}
MAX_FILES = 2_000
MAX_FILE_BYTES = 1_000_000


def scan_tree(target: Path) -> tuple[list[dict[str, str | int]], int]:
    """Scan a caller-selected local directory; return findings and files read."""
    root = target.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("target must be a directory")

    findings: list[dict[str, str | int]] = []
    scanned = 0
    for current, dirs, names in os.walk(root, followlinks=False):
        current_path = Path(current)
        # Do not recurse into symlinked or commonly generated directories.
        dirs[:] = [
            name for name in dirs
            if name not in IGNORED_DIRS and not (current_path / name).is_symlink()
        ]
        for name in sorted(names):
            path = current_path / name
            if path.suffix.lower() not in SOURCE_SUFFIXES or path.is_symlink():
                continue
            if scanned >= MAX_FILES:
                return findings, scanned
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            scanned += 1
            relative = path.relative_to(root).as_posix()
            for line_number, line in enumerate(text.splitlines(), start=1):
                for rule in RULES:
                    if rule.pattern.search(line):
                        # Intentionally do not include source excerpts or matched values.
                        findings.append({
                            "rule_id": rule.rule_id,
                            "title": rule.title,
                            "severity": rule.severity,
                            "path": relative,
                            "line": line_number,
                            "remediation": rule.remediation,
                        })
    return findings, scanned
