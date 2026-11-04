# Contributing

Thanks for helping improve defensive, responsible security research.

- Keep checks local, passive, bounded, and non-destructive; do not add target probing, exploit automation, credential collection, or code execution.
- Add unit tests for new rules and scanner behavior. Use harmless synthetic fixtures, never real credentials.
- Do not include matched source lines or secret values in output.
- Document false-positive limitations and provide actionable remediation.
- Only test systems you own or are explicitly authorized to assess.

Run tests with `python -m unittest discover -s tests -v`.
