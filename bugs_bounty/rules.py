"""Small heuristic rules; matches are prompts for review, not confirmed vulnerabilities."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    rule_id: str
    title: str
    severity: str
    pattern: re.Pattern[str]
    remediation: str


RULES = (
    Rule(
        "BB-SECRET-001",
        "Possible hard-coded credential",
        "high",
        re.compile(r"(?i)\b(?:api[_-]?key|client[_-]?secret|password|passwd|access[_-]?token|secret[_-]?key)\b\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"),
        "Verify whether the value is a real secret; revoke exposed credentials and load secrets from a managed secret store.",
    ),
    Rule(
        "BB-CMD-001",
        "Shell execution enabled",
        "high",
        re.compile(r"(?i)\bsubprocess\.(?:run|popen|call|check_call|check_output)\s*\([^\n]*\bshell\s*=\s*True"),
        "Avoid shell=True; pass a fixed executable and argument list, and validate any user-controlled arguments.",
    ),
    Rule(
        "BB-EVAL-001",
        "Dynamic evaluation",
        "medium",
        re.compile(r"\b(?:eval|exec)\s*\("),
        "Avoid evaluating dynamically supplied strings; use a constrained parser or explicit dispatch instead.",
    ),
    Rule(
        "BB-TLS-001",
        "TLS certificate verification disabled",
        "high",
        re.compile(r"(?i)(?:verify\s*=\s*False|CERT_NONE)"),
        "Keep certificate validation enabled and configure the correct trusted certificate authority if needed.",
    ),
    Rule(
        "BB-XSS-001",
        "Potential unsafe HTML insertion",
        "medium",
        re.compile(r"(?:dangerouslySetInnerHTML|\.innerHTML\s*=)"),
        "Do not insert untrusted content as HTML; use safe text rendering or a well-maintained HTML sanitizer.",
    ),
)
