"""SOC 2 policy implementations."""

from __future__ import annotations

from engine.models import PolicyMetadata, PolicyStatus, Severity
from engine.policy_base import RegisteredPolicy, build_result


def soc2_incident_logging_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="soc2_incident_logging_cc7_2",
        framework="SOC2",
        control_id="CC7.2",
        component="logging",
        severity=Severity.MEDIUM,
        description="Monitor system components and operation anomalies.",
    )
    incident_logging = bool(state.get("logging", {}).get("incident_logging", False))
    return build_result(
        metadata=metadata,
        status=PolicyStatus.COMPLIANT if incident_logging else PolicyStatus.NON_COMPLIANT,
        evidence=(
            "Incident logging is configured." if incident_logging else "Incident logging is not configured."
        ),
    )


def soc2_vendor_risk_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="soc2_vendor_risk_cc9_2",
        framework="SOC2",
        control_id="CC9.2",
        component="vendor_management",
        severity=Severity.MEDIUM,
        description="Assess and manage third-party vendor risks.",
    )
    monitored = bool(state.get("vendor_management", {}).get("risk_monitoring_enabled", False))
    return build_result(
        metadata=metadata,
        status=PolicyStatus.COMPLIANT if monitored else PolicyStatus.NON_COMPLIANT,
        evidence=(
            "Vendor risk monitoring is active."
            if monitored
            else "Vendor risk monitoring is not enabled."
        ),
    )


POLICIES: list[RegisteredPolicy] = [
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="soc2_incident_logging_cc7_2",
            framework="SOC2",
            control_id="CC7.2",
            component="logging",
            severity=Severity.MEDIUM,
            description="Monitor system components and operation anomalies.",
        ),
        evaluator=soc2_incident_logging_policy,
    ),
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="soc2_vendor_risk_cc9_2",
            framework="SOC2",
            control_id="CC9.2",
            component="vendor_management",
            severity=Severity.MEDIUM,
            description="Assess and manage third-party vendor risks.",
        ),
        evaluator=soc2_vendor_risk_policy,
    ),
]
