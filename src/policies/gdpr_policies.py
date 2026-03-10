"""GDPR policy implementations."""

from __future__ import annotations

from engine.models import PolicyMetadata, PolicyStatus, Severity
from engine.policy_base import RegisteredPolicy, build_result


def gdpr_data_minimization_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="gdpr_data_minimization_5_1_c",
        framework="GDPR",
        control_id="5(1)(c)",
        component="logging",
        severity=Severity.HIGH,
        description="Personal data must be adequate, relevant and limited.",
    )
    logging_state = state.get("logging", {})
    retention_days = int(logging_state.get("retention_days", 0))
    has_personal_data = bool(logging_state.get("contains_personal_data", False))
    pseudonymized = bool(logging_state.get("pseudonymized", False))

    if has_personal_data and retention_days > 90 and not pseudonymized:
        return build_result(
            metadata=metadata,
            status=PolicyStatus.CONFLICT,
            evidence=(
                "Personal data retained in logs beyond 90 days without pseudonymization; "
                "possible conflict with minimization principle."
            ),
            details={"retention_days": retention_days, "pseudonymized": pseudonymized},
        )

    return build_result(
        metadata=metadata,
        status=PolicyStatus.COMPLIANT,
        evidence="Data minimization safeguards are present for logging data.",
    )


def gdpr_cross_border_transfer_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="gdpr_cross_border_44",
        framework="GDPR",
        control_id="44",
        component="data_residency",
        severity=Severity.MEDIUM,
        description="Transfers outside EU require lawful mechanism.",
    )
    transfer_mechanism = state.get("data_residency", {}).get("transfer_mechanism", "NONE")
    allowed = transfer_mechanism in {"SCC", "ADEQUACY", "BCR", "NONE"}
    return build_result(
        metadata=metadata,
        status=PolicyStatus.COMPLIANT if allowed else PolicyStatus.NON_COMPLIANT,
        evidence=f"Configured transfer mechanism: {transfer_mechanism}",
    )


POLICIES: list[RegisteredPolicy] = [
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="gdpr_data_minimization_5_1_c",
            framework="GDPR",
            control_id="5(1)(c)",
            component="logging",
            severity=Severity.HIGH,
            description="Personal data must be adequate, relevant and limited.",
        ),
        evaluator=gdpr_data_minimization_policy,
    ),
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="gdpr_cross_border_44",
            framework="GDPR",
            control_id="44",
            component="data_residency",
            severity=Severity.MEDIUM,
            description="Transfers outside EU require lawful mechanism.",
        ),
        evaluator=gdpr_cross_border_transfer_policy,
    ),
]
