# Compliance Report

Generated at: 2026-03-10T13:12:58.762151+00:00
Policies evaluated: 8

## Framework Compliance Summary

| Framework | Compliance |
|---|---:|
| GDPR | 50.0% |
| ISO 27001 | 100.0% |
| PCI DSS | 100.0% |
| SOC2 | 100.0% |

## Control Evaluation

### data_residency

| Control | Framework | Status | Severity | Evidence |
|---|---|---|---|---|
| 44 | GDPR | COMPLIANT | MEDIUM | Configured transfer mechanism: SCC |

### encryption

| Control | Framework | Status | Severity | Evidence |
|---|---|---|---|---|
| A.10.1 | ISO 27001 | COMPLIANT | HIGH | Encryption enabled=True, algorithm=AES-256. |

### logging

| Control | Framework | Status | Severity | Evidence |
|---|---|---|---|---|
| 10.7 | PCI DSS | COMPLIANT | HIGH | Log retention configured to 365 days. |
| A.12.4.1 | ISO 27001 | COMPLIANT | MEDIUM | Centralized logging monitoring is enabled. |
| CC7.2 | SOC2 | COMPLIANT | MEDIUM | Incident logging is configured. |
| 5(1)(c) | GDPR | CONFLICT | HIGH | Personal data retained in logs beyond 90 days without pseudonymization; possible conflict with minimization principle. |

### network_security

| Control | Framework | Status | Severity | Evidence |
|---|---|---|---|---|
| 1.2 | PCI DSS | COMPLIANT | HIGH | Network segmentation is enabled. |

### vendor_management

| Control | Framework | Status | Severity | Evidence |
|---|---|---|---|---|
| CC9.2 | SOC2 | COMPLIANT | MEDIUM | Vendor risk monitoring is active. |

## Conflict Summary

### C-001

- Component: logging
- Frameworks: PCI DSS vs GDPR
- Type: soft_conflict
- Severity: MEDIUM
- Summary: Soft conflict on logging: one framework flagged risk/ambiguity while another requirement is satisfied.
- Recommendation: Retain logs for PCI scope, pseudonymize personal data after 90 days, and enforce strict access controls.

### C-002

- Component: logging
- Frameworks: ISO 27001 vs GDPR
- Type: soft_conflict
- Severity: MEDIUM
- Summary: Soft conflict on logging: one framework flagged risk/ambiguity while another requirement is satisfied.
- Recommendation: Retain logs for PCI scope, pseudonymize personal data after 90 days, and enforce strict access controls.

### C-003

- Component: logging
- Frameworks: SOC2 vs GDPR
- Type: soft_conflict
- Severity: MEDIUM
- Summary: Soft conflict on logging: one framework flagged risk/ambiguity while another requirement is satisfied.
- Recommendation: Retain logs for PCI scope, pseudonymize personal data after 90 days, and enforce strict access controls.
