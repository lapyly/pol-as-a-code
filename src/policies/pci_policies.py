"""PCI DSS policy implementations."""

from __future__ import annotations

from engine.models import PolicyMetadata, PolicyStatus, Severity
from engine.policy_base import RegisteredPolicy, build_result


def pci_log_retention_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="pci_log_retention_10_7",
        framework="PCI DSS",
        control_id="10.7",
        component="logging",
        severity=Severity.HIGH,
        description="Retain audit logs for at least one year.",
    )
    retention_days = int(state.get("logging", {}).get("retention_days", 0))
    if retention_days >= 365:
        return build_result(
            metadata=metadata,
            status=PolicyStatus.COMPLIANT,
            evidence=f"Log retention configured to {retention_days} days.",
            details={"retention_days": retention_days},
        )
    return build_result(
        metadata=metadata,
        status=PolicyStatus.NON_COMPLIANT,
        evidence=f"Log retention configured to {retention_days} days (requires >= 365).",
        details={"retention_days": retention_days},
    )


def pci_network_segmentation_policy(state: dict) -> object:
    metadata = PolicyMetadata(
        policy_id="pci_network_segmentation_1_2",
        framework="PCI DSS",
        control_id="1.2",
        component="network_security",
        severity=Severity.HIGH,
        description="Implement and maintain network segmentation.",
    )
    segmented = bool(state.get("network_security", {}).get("segmented", False))
    status = PolicyStatus.COMPLIANT if segmented else PolicyStatus.NON_COMPLIANT
    evidence = (
        "Network segmentation is enabled."
        if segmented
        else "Network segmentation is not enabled for cardholder data scope."
    )
    return build_result(metadata=metadata, status=status, evidence=evidence)


POLICIES: list[RegisteredPolicy] = [
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="pci_log_retention_10_7",
            framework="PCI DSS",
            control_id="10.7",
            component="logging",
            severity=Severity.HIGH,
            description="Retain audit logs for at least one year.",
        ),
        evaluator=pci_log_retention_policy,
    ),
    RegisteredPolicy(
        metadata=PolicyMetadata(
            policy_id="pci_network_segmentation_1_2",
            framework="PCI DSS",
            control_id="1.2",
            component="network_security",
            severity=Severity.HIGH,
            description="Implement and maintain network segmentation.",
        ),
        evaluator=pci_network_segmentation_policy,
    ),
]
