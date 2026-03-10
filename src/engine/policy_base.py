"""Interfaces and helpers for policy functions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .models import PolicyMetadata, PolicyResult, PolicyStatus

PolicyFunction = Callable[[dict[str, Any]], PolicyResult]


@dataclass(frozen=True)
class RegisteredPolicy:
    """Registered policy function with metadata."""

    metadata: PolicyMetadata
    evaluator: PolicyFunction


def build_result(
    *,
    metadata: PolicyMetadata,
    status: PolicyStatus,
    evidence: str,
    details: dict[str, Any] | None = None,
) -> PolicyResult:
    """Build a typed policy result from metadata and runtime values."""

    return PolicyResult(
        policy_id=metadata.policy_id,
        framework=metadata.framework,
        control_id=metadata.control_id,
        component=metadata.component,
        severity=metadata.severity,
        status=status,
        evidence=evidence,
        details=details or {},
    )
