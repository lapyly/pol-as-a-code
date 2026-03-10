"""Policy registration and lookup."""

from __future__ import annotations

from dataclasses import dataclass, field

from .policy_base import RegisteredPolicy


@dataclass
class PolicyRegistry:
    """In-memory policy registry with duplicate protection."""

    _policies: list[RegisteredPolicy] = field(default_factory=list)

    def register(self, policy: RegisteredPolicy) -> None:
        """Register a policy, enforcing unique policy IDs."""

        policy_ids = {entry.metadata.policy_id for entry in self._policies}
        if policy.metadata.policy_id in policy_ids:
            raise ValueError(f"Duplicate policy_id: {policy.metadata.policy_id}")
        self._policies.append(policy)

    def list(self) -> list[RegisteredPolicy]:
        """Return registered policies in insertion order."""

        return list(self._policies)
