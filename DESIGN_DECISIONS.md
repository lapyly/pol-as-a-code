# Design Decisions

## Why Python policy functions

Policies are implemented as Python functions with metadata to support nuanced compliance logic and explicit evidence generation.

## Conflict model

- **Hard conflict**: one framework is compliant while another is non-compliant for same component.
- **Soft conflict**: one framework reports a conflict/risk signal while another remains compliant.

## Reporting

Markdown is the default output for readability and audit workflows; JSON is available for machine integration.

## Extensibility

Policies are grouped by framework module and loaded into a central `PolicyRegistry`.
Adding a new framework requires only:

1. new policy module
2. policy registrations
3. inclusion in `all_policies.py`
