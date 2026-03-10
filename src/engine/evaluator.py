"""Policy evaluation orchestration."""

from __future__ import annotations

import logging
from collections import defaultdict
from time import perf_counter
from typing import Any

from .models import PolicyResult, PolicyStatus
from .policy_registry import PolicyRegistry

logger = logging.getLogger(__name__)


class PolicyEvaluator:
    """Executes registered policies against infrastructure state."""

    def __init__(self, registry: PolicyRegistry) -> None:
        self.registry = registry

    def evaluate(self, state: dict[str, Any]) -> list[PolicyResult]:
        """Run all policies and return results.

        Any policy failure is captured as UNKNOWN to avoid stopping execution.
        """

        results: list[PolicyResult] = []

        for registered in self.registry.list():
            start = perf_counter()
            try:
                result = registered.evaluator(state)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Policy execution failed: %s", registered.metadata.policy_id)
                result = PolicyResult(
                    policy_id=registered.metadata.policy_id,
                    framework=registered.metadata.framework,
                    control_id=registered.metadata.control_id,
                    component=registered.metadata.component,
                    severity=registered.metadata.severity,
                    status=PolicyStatus.UNKNOWN,
                    evidence="Policy execution error",
                    details={"error": str(exc)},
                )

            elapsed_ms = (perf_counter() - start) * 1000
            result.details.setdefault("runtime_ms", round(elapsed_ms, 3))
            results.append(result)

        return results


def framework_compliance(results: list[PolicyResult]) -> dict[str, float]:
    """Calculate compliance percentages per framework."""

    buckets: dict[str, list[PolicyResult]] = defaultdict(list)
    for result in results:
        buckets[result.framework].append(result)

    summary: dict[str, float] = {}
    for framework, values in buckets.items():
        compliant_count = sum(1 for item in values if item.status == PolicyStatus.COMPLIANT)
        summary[framework] = round((compliant_count / len(values)) * 100, 2)

    return summary
