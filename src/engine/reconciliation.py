"""Recommendation generation for detected conflicts."""

from __future__ import annotations

from .models import Conflict


class ReconciliationEngine:
    """Enhances conflicts with targeted recommendations."""

    def reconcile(self, conflicts: list[Conflict]) -> list[Conflict]:
        """Return conflicts with tuned recommendations based on conflict taxonomy."""

        reconciled: list[Conflict] = []
        for conflict in conflicts:
            recommendation = conflict.recommendation
            if "logging" in conflict.component.lower():
                recommendation = (
                    "Retain logs for PCI scope, pseudonymize personal data after 90 days, "
                    "and enforce strict access controls."
                )
            elif "encryption" in conflict.component.lower():
                recommendation = "Adopt strongest approved cipher suite and retire legacy encryption."

            reconciled.append(
                Conflict(
                    conflict_id=conflict.conflict_id,
                    component=conflict.component,
                    frameworks=conflict.frameworks,
                    policy_ids=conflict.policy_ids,
                    conflict_type=conflict.conflict_type,
                    severity=conflict.severity,
                    summary=conflict.summary,
                    recommendation=recommendation,
                )
            )
        return reconciled
