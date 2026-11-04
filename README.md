# bugs-bounty

**An open, defensive application-security research starter.** Find review-worthy code patterns, write clear reports, and help maintainers fix issues—only in software you own or have explicit permission to assess.

> This is a small local static checker, not an exploit framework, malware detector, AI agent, or guarantee that a project is secure. Findings are heuristics for human review; false positives and missed issues are expected.

## Quick start

Requires Python 3.10+; there are no third-party dependencies.

```bash
python -m bugs_bounty scan ./path-to-your-authorized-source
python -m bugs_bounty scan ./path-to-your-authorized-source --format json
python -m unittest discover -s tests -v
```

The scanner reads source files on your machine and prints findings to the terminal. It makes no network requests, does not execute scanned code, and does not change or delete files. Review output before sharing it: paths and line numbers can reveal private project structure.

## What it checks

The first pass reports selected high-signal patterns for human review, including hard-coded credential-like values, risky shell execution, dynamic evaluation, disabled TLS verification, and unsafe HTML insertion. It deliberately omits source snippets and credential values from reports. See [`bugs_bounty/rules.py`](bugs_bounty/rules.py) for the current rules and remediation advice.

It skips common dependency/build directories and symbolic links, and applies per-file and total-file limits. A clean scan does **not** establish that a project is safe. Use code review, dependency auditing, secret scanning, tests, and threat modeling too.

## Responsible use and reporting

- Scan only code you own or are explicitly authorized to assess.
- Follow the target's published bug bounty scope, rules, and disclosure timeline. Never test out-of-scope systems.
- Do not use this project to access, disrupt, persist in, or extract data from third-party systems.
- Report reproducible evidence privately to the maintainer; redact secrets and personal data. Do not publish a working exploit before coordinated disclosure.
- This project performs local static checks only. It does not crawl URLs, probe hosts, exploit vulnerabilities, or inspect running processes.

See [SECURITY.md](SECURITY.md) for reporting guidance and the [Code of Conduct](CODE_OF_CONDUCT.md) for community expectations.

## CyberShield relationship

This project is a separate, local source-code review tool; it does not connect to or control CyberShield. For host/process monitoring, see [Aayush1003/cyber-shield-ai-agent](https://github.com/Aayush1003/cyber-shield-ai-agent). Keep CyberShield bound to a trusted local machine: its existing administrative endpoints should not be exposed to the public internet without authentication and a security review. See its [security notes](https://github.com/Aayush1003/cyber-shield-ai-agent/blob/main/SECURITY.md).

## Further reading

- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [NIST Secure Software Development Framework (SP 800-218)](https://csrc.nist.gov/pubs/sp/800/218/final)
- [CWE: Common Weakness Enumeration](https://cwe.mitre.org/)

## Development

```bash
python -m unittest discover -s tests -v
```

Contributions should include tests and keep scans passive, local, bounded, and non-destructive. See [CONTRIBUTING.md](CONTRIBUTING.md).
