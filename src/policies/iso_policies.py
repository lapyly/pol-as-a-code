"""ISO 27001 policy implementations."""

from __future__ import annotations

from engine.models import PolicyMetadata, PolicyStatus, Severity
from engine.policy_base import RegisteredPolicy, build_result


def iso_logging_monitoring_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="iso_logging_monitoring_a12_4_1",
        framework="ISO 27001",
        control_id="A.12.4.1",
        component="logging",
        severity=Severity.MEDIUM,
        description="Event logs recording user activities should be produced and reviewed.",
    )
    enabled = bool(state.get("logging", {}).get("monitoring_enabled", False))
    return build_result(
        metadata=metadata,
        status=PolicyStatus.COMPLIANT if enabled else PolicyStatus.NON_COMPLIANT,
        evidence="Centralized logging monitoring is enabled." if enabled else "Monitoring is disabled.",
    )


def iso_encryption_management_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="iso_crypto_controls_a10_1",
        framework="ISO 27001",
        control_id="A.10.1",
        component="encryption",
        severity=Severity.HIGH,
        description="Use cryptographic controls to protect information.",
    )
    algorithm = state.get("encryption", {}).get("data_at_rest", {}).get("algorithm", "")
    enabled = bool(state.get("encryption", {}).get("data_at_rest", {}).get("enabled", False))
    is_strong = algorithm in {"AES-256", "ChaCha20-Poly1305"}
    status = PolicyStatus.COMPLIANT if enabled and is_strong else PolicyStatus.NON_COMPLIANT
    return build_result(
        metadata=metadata,
        status=status,
        evidence=f"Encryption enabled={enabled}, algorithm={algorithm or 'N/A'}.",
    )


POLICIES: list[RegisteredPolicy] = [
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="iso_logging_monitoring_a12_4_1",
            framework="ISO 27001",
            control_id="A.12.4.1",
            component="logging",
            severity=Severity.MEDIUM,
            description="Event logs recording user activities should be produced and reviewed.",
        ),
        evaluator=iso_logging_monitoring_policy,
    ),
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="iso_crypto_controls_a10_1",
            framework="ISO 27001",
            control_id="A.10.1",
            component="encryption",
            severity=Severity.HIGH,
            description="Use cryptographic controls to protect information.",
        ),
        evaluator=iso_encryption_management_policy,
    ),
]
