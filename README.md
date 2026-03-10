# Policy-as-Code Reconciliation Engine

Python-based compliance analysis engine that evaluates one infrastructure state against multiple regulatory frameworks, detects cross-framework conflicts, and produces audit-ready reports.

## Features

- Multi-framework evaluation in one run (PCI DSS, ISO 27001, SOC2, GDPR)
- Conflict detection for hard/soft framework conflicts
- Reconciliation recommendations (for example, pseudonymization for log-retention tradeoffs)
- Markdown and JSON output
- Structured, typed policy model for maintainability

## Project structure

```text
src/
  engine/
  policies/
  reporting/
  main.py
tests/
  fixtures/
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
python src/main.py --state tests/fixtures/conflict_state.json --output output/sample_report.md --format markdown
```

## Example state schema

See files under `tests/fixtures/*.json` for representative infrastructure state snapshots.

## Security notes

- Policies are local Python functions only (no dynamic code execution).
- Runtime errors are captured as `UNKNOWN` outcomes for resilience.
- Sensitive values should not be logged in policy evidence.
