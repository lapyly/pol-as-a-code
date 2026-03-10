"""Domain models for the policy reconciliation engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class PolicyStatus(str, Enum):
    """Possible outcomes for a policy evaluation."""

    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"


class Severity(str, Enum):
    """Severity level for controls and conflicts."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class PolicyMetadata:
    """Static policy metadata used for reporting and conflict checks."""

    policy_id: str
    framework: str
    control_id: str
    component: str
    severity: Severity
    description: str


@dataclass(frozen=True)
class PolicyResult:
    """Single policy evaluation result."""

    policy_id: str
    framework: str
    control_id: str
    component: str
    severity: Severity
    status: PolicyStatus
    evidence: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Conflict:
    """Represents a cross-framework conflict."""

    conflict_id: str
    component: str
    frameworks: tuple[str, str]
    policy_ids: tuple[str, str]
    conflict_type: str
    severity: Severity
    summary: str
    recommendation: str


@dataclass(frozen=True)
class ComplianceReport:
    """Final report container used by output formatters."""

    generated_at: datetime
    evaluation_count: int
    results: list[PolicyResult]
    conflicts: list[Conflict]
    framework_compliance: dict[str, float]

    @staticmethod
    def now(
        *,
        results: list[PolicyResult],
        conflicts: list[Conflict],
        framework_compliance: dict[str, float],
    ) -> "ComplianceReport":
        """Create a timestamped report with UTC timezone."""

        return ComplianceReport(
            generated_at=datetime.now(timezone.utc),
            evaluation_count=len(results),
            results=results,
            conflicts=conflicts,
            framework_compliance=framework_compliance,
        )
