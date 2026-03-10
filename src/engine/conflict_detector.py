"""Conflict detection across framework policy results."""

from __future__ import annotations

from itertools import combinations

from .models import Conflict, PolicyResult, PolicyStatus, Severity


class ConflictDetector:
    """Identifies hard and soft conflicts for same infrastructure component."""

    def detect(self, results: list[PolicyResult]) -> list[Conflict]:
        """Detect conflicts by comparing policy outcomes per component."""

        conflicts: list[Conflict] = []
        grouped: dict[str, list[PolicyResult]] = {}

        for result in results:
            grouped.setdefault(result.component, []).append(result)

        sequence = 1
        for component, component_results in grouped.items():
            for first, second in combinations(component_results, 2):
                if first.framework == second.framework:
                    continue

                conflict = self._build_conflict_if_any(component, first, second, sequence)
                if conflict:
                    conflicts.append(conflict)
                    sequence += 1

        return conflicts

    def _build_conflict_if_any(
        self,
        component: str,
        first: PolicyResult,
        second: PolicyResult,
        sequence: int,
    ) -> Conflict | None:
        first_status = first.status
        second_status = second.status

        hard_conflict = {
            first_status,
            second_status,
        } == {PolicyStatus.COMPLIANT, PolicyStatus.NON_COMPLIANT}

        if hard_conflict:
            return Conflict(
                conflict_id=f"C-{sequence:03d}",
                component=component,
                frameworks=(first.framework, second.framework),
                policy_ids=(first.policy_id, second.policy_id),
                conflict_type="hard_conflict",
                severity=Severity.HIGH,
                summary=(
                    f"Hard conflict on {component}: {first.framework}={first.status.value}, "
                    f"{second.framework}={second.status.value}"
                ),
                recommendation="Apply regional policy separation or compensating controls.",
            )

        soft_conflict = PolicyStatus.CONFLICT in {first_status, second_status}
        if soft_conflict:
            return Conflict(
                conflict_id=f"C-{sequence:03d}",
                component=component,
                frameworks=(first.framework, second.framework),
                policy_ids=(first.policy_id, second.policy_id),
                conflict_type="soft_conflict",
                severity=Severity.MEDIUM,
                summary=(
                    f"Soft conflict on {component}: one framework flagged risk/ambiguity "
                    "while another requirement is satisfied."
                ),
                recommendation="Document risk tradeoff and apply data minimization controls.",
            )

        return None
