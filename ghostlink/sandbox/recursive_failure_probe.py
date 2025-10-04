"""Factory for the RECURSIVE_FAILURE_PROBE component."""
from __future__ import annotations

from ..factory import component_factory

RECURSIVE_FAILURE_PROBE = component_factory(__name__, "RECURSIVE_FAILURE_PROBE", "sandbox")

__all__ = ["RECURSIVE_FAILURE_PROBE"]
