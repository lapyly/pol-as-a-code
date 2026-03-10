"""Central policy registration entrypoint."""

from __future__ import annotations

from engine.policy_registry import PolicyRegistry

from .gdpr_policies import POLICIES as GDPR_POLICIES
from .iso_policies import POLICIES as ISO_POLICIES
from .pci_policies import POLICIES as PCI_POLICIES
from .soc2_policies import POLICIES as SOC2_POLICIES


def build_registry() -> PolicyRegistry:
    """Build registry with all available framework policies."""

    registry = PolicyRegistry()
    for policy in [*PCI_POLICIES, *ISO_POLICIES, *SOC2_POLICIES, *GDPR_POLICIES]:
        registry.register(policy)
    return registry
