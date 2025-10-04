"""Factory for the MIRROR_FAULT_SPAWNER component."""
from __future__ import annotations

from ..factory import component_factory

MIRROR_FAULT_SPAWNER = component_factory(__name__, "MIRROR_FAULT_SPAWNER", "sandbox")

__all__ = ["MIRROR_FAULT_SPAWNER"]
